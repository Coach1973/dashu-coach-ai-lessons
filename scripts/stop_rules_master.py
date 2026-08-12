#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stop hook 總管（2026-08-12 全面體檢後合併）

起因：原本 Stop 事件註冊了 12 支獨立腳本，其中 10 支各自 `cat` 同一份
transcript jsonl 再用 python3/jq 解析一次——同一份檔案被重複讀 10 次，
對話越長成本越高（教練 2026-08-12 全面體檢時抓到）。

本檔把那 10 支「檢查類」腳本合併成單一程序：
  - transcript 只讀一次、只解析一次，共用給所有檢查
  - 程式啟動次數 12 → 3（本檔 + session_end_auto_push + session_end_distill_push）

🔴 合併原則（不是重寫）：每一條檢查的偵測字串、白名單、警告文字、log 路徑、
   以及「擋下(exit 2)還是只提醒(exit 0)」的分級，全部一字不差照抄自原腳本。
   原腳本保留在 scripts/ 不刪除，隨時可比對／回退。

原腳本對應表：
  A rule12_porter_check.sh              擋
  B rule05_hash_check.sh                擋
  C rule_taiwan_time_check.sh           擋
  D rule07_polling_check.sh             擋
  E rule03_verify_before_answer_check.sh 提醒
  F rule08_ask_when_clear_check.sh      提醒
  G rule_proactive_session_reminder_check.sh 提醒
  H delivery_check.sh                   擋
  I rule_traditional_chinese_check.sh   擋
  J rule_html_chrome_check.sh           擋

行為對齊：原本 Claude Code 會把 12 支全部跑完、各自輸出警告、任一支 exit 2
就擋下。本檔同樣「全部檢查跑完、收集所有訊息、任一條命中擋下才 exit 2」，
不做提早跳出，確保提醒不會因為前面有人擋下就消失。
"""

import sys, json, re, os
from datetime import datetime

HOME = os.path.expanduser("~")
DISTILL_DIR = os.path.join(HOME, ".openclaw", "workspace", "distill")

BAR = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


def log_violation(logname, body):
    """照抄原腳本的違規記錄格式：時間 + session 前 8 碼 + 命中內容 + ---"""
    try:
        os.makedirs(DISTILL_DIR, exist_ok=True)
        path = os.path.join(DISTILL_DIR, logname)
        with open(path, "a", encoding="utf-8") as f:
            f.write("[%s] session=%s\n" % (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), SESSION_SHORT))
            if body:
                f.write(body)
            f.write("---\n")
        return path
    except Exception:
        return os.path.join(DISTILL_DIR, logname)


# ────────────────────────────────────────────────
# 讀 stdin（Claude Code 傳進來的 hook payload）
# ────────────────────────────────────────────────
try:
    RAW = sys.stdin.read()
    DATA = json.loads(RAW) if RAW.strip() else {}
except Exception:
    sys.exit(0)

# 已經循環過一次了，本次放行（避免無限迴圈）——所有原腳本共用的保護機制
if DATA.get("stop_hook_active") in (True, "true"):
    sys.exit(0)

TRANSCRIPT = DATA.get("transcript_path") or ""
SESSION_ID = DATA.get("session_id") or "unknown"
SESSION_SHORT = SESSION_ID[:8]

if not TRANSCRIPT or not os.path.isfile(TRANSCRIPT):
    sys.exit(0)

# ────────────────────────────────────────────────
# 🔴 這裡就是本次合併的重點：transcript 只讀一次、只解析一次
# ────────────────────────────────────────────────
try:
    with open(TRANSCRIPT, encoding="utf-8") as f:
        RAW_LINES = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)

EVENTS = []
for l in RAW_LINES:
    try:
        EVENTS.append(json.loads(l))
    except Exception:
        EVENTS.append(None)


def _content_list(evt):
    c = (evt.get("message") or {}).get("content")
    return c if isinstance(c, list) else []


# 1) 最後一條 assistant 的純文字（給教練看的最終回覆）
LAST_TEXT = ""
for evt in reversed(EVENTS):
    if not isinstance(evt, dict):
        continue
    if evt.get("type") == "assistant":
        content = (evt.get("message") or {}).get("content")
        if isinstance(content, list):
            LAST_TEXT = "\n".join(
                c.get("text", "") for c in content
                if isinstance(c, dict) and c.get("type") == "text")
        elif isinstance(content, str):
            LAST_TEXT = content
        break

LAST_LINES = LAST_TEXT.split("\n") if LAST_TEXT else []

# 2) 這一整回合的 assistant 文字 + Write/Edit/Bash 工具輸入（rule07 用）
#    照抄原腳本：往回掃到上一個 user 事件為止，設計寫進檔案也要抓得到
_segments = []
for evt in reversed(EVENTS):
    if not isinstance(evt, dict):
        continue
    t = evt.get("type")
    if t == "user":
        break
    if t != "assistant":
        continue
    for c in _content_list(evt):
        if not isinstance(c, dict):
            continue
        ctype = c.get("type")
        if ctype == "text":
            _segments.append(c.get("text", ""))
        elif ctype == "tool_use":
            name = c.get("name", "")
            inp = c.get("input") or {}
            if name in ("Write", "Edit"):
                _segments.append(inp.get("content", "") or "")
                _segments.append(inp.get("new_string", "") or "")
            elif name == "Bash":
                _segments.append(inp.get("command", "") or "")
TURN_TEXT = "\n".join(reversed(_segments))
TURN_LINES = TURN_TEXT.split("\n") if TURN_TEXT else []

# 3) 這一輪有沒有碰過原始 UTC timestamp（rule_taiwan_time 用）
#    照抄原腳本兩個防誤報設計：跳過 attachment 事件、跳過信封層 timestamp 欄位
_last_user_idx = None
for i in range(len(EVENTS) - 1, -1, -1):
    evt = EVENTS[i]
    if not isinstance(evt, dict):
        continue
    if evt.get("type") == "user":
        content = (evt.get("message") or {}).get("content")
        if isinstance(content, str) or (isinstance(content, list) and any(
                isinstance(c, dict) and c.get("type") == "text" for c in content)):
            _last_user_idx = i
            break
if _last_user_idx is None:
    _last_user_idx = 0


def _extract_texts(node):
    texts = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "timestamp":
                continue  # 信封層的事件時間戳，不算「AI 處理過的內容」
            if k == "text" and isinstance(v, str):
                texts.append(v)
            elif k == "content" and isinstance(v, str):
                texts.append(v)
            else:
                texts.extend(_extract_texts(v))
    elif isinstance(node, list):
        for item in node:
            texts.extend(_extract_texts(item))
    return texts


_content_texts = []
for evt in EVENTS[_last_user_idx:]:
    if not isinstance(evt, dict):
        continue
    if evt.get("type") == "attachment":
        continue  # UserPromptSubmit hook 注入的守則提醒（內含 Z 格式範例）不算
    _content_texts.extend(_extract_texts(evt.get("message", evt)))
TOUCHED_UTC = bool(re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z",
                             "\n".join(_content_texts)))

# 4) HTML 改動 vs Chrome 開啟證據（rule_html_chrome 用，只看最近 100 筆事件）
HTML_EDIT_IDX = -1
HTML_FILES = []
CHROME_EVIDENCE_IDX = -1
for i, evt in enumerate(EVENTS[-100:]):
    if not isinstance(evt, dict) or evt.get("type") != "assistant":
        continue
    for c in _content_list(evt):
        if not isinstance(c, dict) or c.get("type") != "tool_use":
            continue
        name = c.get("name", "")
        tin = c.get("input") or {}
        if name in ("Edit", "Write"):
            fp = str(tin.get("file_path", ""))
            if fp.lower().endswith(".html"):
                HTML_EDIT_IDX = i
                if fp not in HTML_FILES:
                    HTML_FILES.append(fp)
        if name == "Bash":
            command = str(tin.get("command", ""))
            if re.search(r"open\s+-a\s+\"?Google Chrome\"?", command, re.IGNORECASE):
                CHROME_EVIDENCE_IDX = i
            m = re.search(
                r"\b(?:cp|mv|rsync|git\s+add)\s+(?:[\w.-]+\s+)*([~./][\w./~-]*\.html)\b",
                command)
            if m:
                HTML_EDIT_IDX = i
                if m.group(1) not in HTML_FILES:
                    HTML_FILES.append(m.group(1))

# 5) 這輪有沒有查過記憶檔/SOP（rule03 肯定式誤判的免責證據，只看最近 40 筆）
HAS_MEMORY_CHECK = False
for evt in EVENTS[-40:]:
    if not isinstance(evt, dict) or evt.get("type") != "assistant":
        continue
    for c in _content_list(evt):
        if not isinstance(c, dict) or c.get("type") != "tool_use":
            continue
        name = c.get("name", "")
        tin = c.get("input") or {}
        target = "%s%s%s" % (tin.get("file_path", ""), tin.get("pattern", ""),
                             tin.get("path", ""))
        if name in ("Grep", "Read") and ("memory" in target or "SOP" in target
                                         or "特助心法" in target or "試金石" in target):
            HAS_MEMORY_CHECK = True

# 6) 真實對話輪數（proactive reminder 用，與 session_length_hook.sh 同一套算法）
TURNS = 0
for evt in EVENTS:
    if not isinstance(evt, dict) or evt.get("type") != "user":
        continue
    c = (evt.get("message") or {}).get("content")
    if isinstance(c, str) and c.strip():
        TURNS += 1
    elif isinstance(c, list):
        has_text = any(isinstance(b, dict) and b.get("type") == "text" for b in c)
        has_tr = any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c)
        if has_text and not has_tr:
            TURNS += 1

# ────────────────────────────────────────────────
# 檢查結果收集
# ────────────────────────────────────────────────
MESSAGES = []   # 要輸出到 stderr 的訊息
BLOCK = False   # 有任一「擋下級」命中就 exit 2


def strip_quotes(line):
    """剝掉「…」內容：引號內是舉例/引用，不是真的在做那件事"""
    return re.sub(r"「[^」]*」", "", line)


# ════════════════════════════════════════════════
# A. 守則#12 搬運工句型（擋）—— 原 rule12_porter_check.sh
# ════════════════════════════════════════════════
A_PATTERNS = [
    "請你複製", "請你貼", "請您複製", "請您貼", "請您回傳", "請你回傳",
    "麻煩你貼", "麻煩您貼", "麻煩你複製", "麻煩您複製", "麻煩你回傳",
    "麻煩貼一下", "麻煩複製", "請貼一下", "請複製一下", "請幫我貼",
    "請幫我複製", "可以複製貼上", "請把這段貼", "請把結果貼",
    "請把輸出貼", "請把這段複製",
]
A_WHITELIST = re.compile(
    r"禁止|不要|不應|不准|不會|不可|違反|列舉|引用|以下|清單|句型|守則|原文|案例|範例|示例|例如|諸如|偵測到|命中|示範|black\?list|black list|偵測|抓到|grep|hook|測試")

if LAST_TEXT:
    hits = []
    for line in LAST_LINES:
        if A_WHITELIST.search(line):
            continue
        clean = strip_quotes(line)
        for p in A_PATTERNS:
            if p in clean:
                hits.append("  • 偵測到「%s」" % p)
    if hits:
        body = "\n".join(sorted(set(hits))) + "\n\n"
        path = log_violation("rule12_violations.log", body)
        MESSAGES.append(
            "\n🚨 守則#12 違規偵測（系統 grep，deterministic check）\n" + BAR + "\n"
            "剛才回覆出現「叫教練搬運」的禁止句型：\n" + body +
            "\n📜 守則#12 原文（特助心法.md）：\n"
            "  「永遠不要叫用戶幫你複製這個、貼上那個、再回傳這個。」\n"
            "  「只要是任何 AI 能夠做到的事，你都不應該說你做不到。」\n\n"
            "✅ 正確做法（請立刻重做）：\n"
            "  1. 自己用 Bash/Read/Grep 工具拿到需要的資訊\n"
            "  2. 如果真的拿不到（例如教練手機上的截圖），明確說「我拿不到 X，需要您 Y」\n"
            "     而不是用「請貼一下/麻煩複製」這種搬運工句型\n"
            "  3. 重新生成回覆，去掉所有禁止句型\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# B. 守則#05 完成聲明缺 commit hash（擋）—— 原 rule05_hash_check.sh
# ════════════════════════════════════════════════
B_PATTERNS = [
    "完成了", "已修好", "已修完", "已修", "已修。", "修好了", "已處理",
    "處理好了", "已上傳", "已推送", "已 push", "推上去了", "推上 GitHub",
    "已部署", "已交付", "已建立", "已建立完成", "已設定", "設定好了",
    "已建立好", "已改完", "已改好", "改完了", "改好了", "已建置",
    "建置完成", "建置好了", "建好了", "已建好", "任務完成", "task 完成",
    "任務結束", "已就緒", "搞定", "完成！", "修完！", "搞定！",
]
B_WHITELIST = re.compile(
    r"守則|不要|不應|不准|不會|不可|違反|列舉|引用|以下|清單|句型|原文|案例|範例|示例|例如|諸如|偵測|命中|示範|black.list|blacklist|討論|如果|假如|假設|除非|不然|等您|等教練|先不要|等一下|抱歉|無法|失敗|錯誤|不可|沒辦法|未完成|未通過|未驗證|未提交|可考慮|考慮|思考|想|應該|也許|或許|先看|先看您|先看一下|先給您看|想要|要|希望|建議|推薦|還沒|還不|尚未|等您|請您|待|或許|也許|大概|可能|約|預估|先|等等|先確認|先看")

if LAST_TEXT:
    hits = []
    for line in LAST_LINES:
        if B_WHITELIST.search(line):
            continue
        for p in B_PATTERNS:
            if p in line:
                hits.append("  • 偵測到「%s」" % p)
                break
    if hits and not re.search(r"\b[0-9a-f]{7,40}\b", LAST_TEXT, re.IGNORECASE):
        body = "\n".join(sorted(set(hits))) + "\n\n"
        path = log_violation("rule05_violations.log", body)
        MESSAGES.append(
            "\n🚨 守則#05 違規偵測（系統 grep，deterministic check）\n" + BAR + "\n"
            "剛才回覆出現「完成聲明」，但找不到 commit hash：\n" + body +
            "\n📜 守則#05 原文（特助心法.md）：\n"
            "  「只有你做了 commit hash（雲端紀錄）才能証明你留下痕跡。」\n"
            "  「說了做不到，就會影響信任感的建立。」\n\n"
            "✅ 正確做法（請立刻補上 hash）：\n"
            "  1. 確認 git commit 已做，複製 7 碼短 hash（例：3b9ab393）\n"
            "  2. 在回覆中明確標示：「commit 3b9ab393」或「hash: 3b9ab393」\n"
            "  3. 如果是純說明（沒做事），把「修好了/完成了」等詞刪掉，改用「已修」開頭描述\n"
            "  4. 如果不該 commit（例如教練說「先看」），刪掉完成詞或加「待 commit」\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# C. 時間鐵律：碰過 UTC 卻沒講台灣時間（擋）—— 原 rule_taiwan_time_check.sh
# ════════════════════════════════════════════════
if TOUCHED_UTC and LAST_TEXT:
    has_clock = bool(re.search(r"[0-9]{1,2}:[0-9]{2}|[0-9]{1,2}[點时]", LAST_TEXT))
    has_tw = bool(re.search(r"台灣時間|台湾时间|\+8|GMT\+8|UTC\+8", LAST_TEXT))
    if has_clock and not has_tw:
        path = log_violation("rule_taiwan_time_violations.log", "")
        MESSAGES.append(
            "\n🕐🔒 時間鎖違規偵測（系統 grep，deterministic check）\n" + BAR + "\n"
            "這一輪你讀取/處理過原始 UTC timestamp（含 \"T..:..:..Z\" 格式），\n"
            "回覆裡也出現了時鐘數字，但完全沒有講「台灣時間」或「+8」換算字樣。\n\n"
            "📜 時間鐵律（教練 2026-06-09 親罵後寫死，案例38 再犯一次）：\n"
            "  「跟教練講時間 → 永遠先換算成台灣時間（Asia/Taipei，UTC+8）」\n"
            "  「看到 Z 結尾自動 +8 呈現，禁止口語講 UTC 時間當台灣時間」\n\n"
            "✅ 正確做法（請立刻檢查並修正）：\n"
            "  1. 回頭檢查剛才報給教練的每一個時鐘數字，是不是直接抄了 UTC 的 HH:MM\n"
            "  2. 全部 +8 小時重新換算（注意跨日：UTC 16:00 以後會跨到台灣隔天）\n"
            "  3. 回覆中明確標示「台灣時間」字樣，讓教練一眼確認你有換算過\n"
            "  4. 如果這次真的不需要報時間（只是剛好文字裡出現數字），可忽略此提醒\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# D. 守則#07 輪詢設計（擋）—— 原 rule07_polling_check.sh
# ════════════════════════════════════════════════
D_PATTERNS = [
    r"每.*分鐘.*檢查", r"每.*分鐘.*看一次", r"每.*分鐘.*跑一次",
    r"每隔.*分鐘", r"每隔.*秒", r"定時.*檢查", r"定時.*輪詢",
    r"cron.*檢查", r"cron.*輪詢", r"背景.*每.*分鐘", r"輪詢.*機制",
]
D_WHITELIST = re.compile(
    r"守則|案例|教訓|之前|已經|過去|糾正|檢討|反省|不要再|避免再|不應該|不能再|同一個地方|同一場對話|連續.*次|拆除|改成事件|改用事件|事件驅動|事件觸發|拿掉|廢除|退役|取消|移除輪詢|零輪詢|非輪詢|不是輪詢|不用輪詢|沒有輪詢|一次性排程|delete-after-run")

if TURN_TEXT:
    hits = []
    for line in TURN_LINES:
        if D_WHITELIST.search(line):
            continue
        for p in D_PATTERNS:
            if re.search(p, line):
                hits.append("  • 偵測到疑似輪詢設計：「%s...」" % line[:60])
                break
    if hits and not re.search(
            r"事件驅動不可行|沒有現成的事件掛鉤|系統不支援事件觸發|只能用輪詢是因為", TURN_TEXT):
        body = "\n".join(sorted(set(hits))) + "\n"
        path = log_violation("rule07_polling_violations.log", body)
        MESSAGES.append(
            "\n🚨 守則#07 輪詢設計偵測（系統 grep，deterministic check）\n" + BAR + "\n"
            "這一輪回覆裡出現「定時/每X分鐘檢查」的輪詢設計：\n" + body +
            "\n📜 守則#07 原文（特助心法.md）：\n"
            "  「不要在同一個地方跌倒兩次，就是最大的成功。」\n"
            "  「不可能不犯錯，但不要一直犯同樣的錯。」\n\n"
            "2026-07-02 教練已對同一個錯誤糾正 3 次（心跳燈塔/蒸餾提煉/自動開通），\n"
            "這是第 4 次以後的自動攔截，不能再靠記性。\n\n"
            "✅ 停下來自問：\n"
            "  1. 這件事有沒有現成的事件掛鉤（hook/signal/webhook/restart-policy）可以直接觸發？\n"
            "  2. 如果真的沒有，在回覆裡明確寫出「事件驅動不可行，因為XXX」再繼續。\n"
            "  3. 如果只是在討論/引用過去案例，把這句話改寫得更明確是在「回顧」不是「提議」。\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# E. 守則#03 未查證就交付（提醒，不擋）—— 原 rule03_verify_before_answer_check.sh
# ════════════════════════════════════════════════
E_GUESS = [
    r"應該是", r"應該可以", r"應該沒問題", r"大概是", r"我猜", r"猜測",
    r"推測應該", r"可能是因為", r"瞎猜", r"亂猜", r"自行判斷",
    r"自己判斷.{0,4}(而)?沒.{0,2}問",
]
E_CONFIDENT = [
    r"之前沒發現的", r"發現.{0,4}漏洞", r"這是.{0,4}漏洞",
    r"完全沒有.{0,4}(攔截|防護|保護)",
]
E_WHITELIST = re.compile(
    r"不確定|需要查證|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|已驗證|已確認|測試通過|查證後|實測|跑過.*確認|讀取.*確認")

if LAST_TEXT:
    guess_hits, confident_hits = [], []
    for line in LAST_LINES:
        if E_WHITELIST.search(line):
            continue
        for p in E_GUESS:
            if re.search(p, line):
                guess_hits.append("  • 偵測到疑似未查證就交付：「%s...」" % line[:60])
                break
        for p in E_CONFIDENT:
            if re.search(p, line):
                confident_hits.append(
                    "  • 偵測到疑似肯定式誤判（沒hedge詞卻宣稱發現問題）：「%s...」" % line[:60])
                break
    # 已經查過記憶檔 → 這則肯定式宣稱是有根據的，不算違規
    if HAS_MEMORY_CHECK:
        confident_hits = []
    hits = guess_hits + confident_hits
    if hits:
        body = "\n".join(hits) + "\n"
        path = log_violation("rule03_verify_violations.log", body)
        MESSAGES.append(
            "\n🌱 守則#03 未查證交付偵測（系統 grep，Warn 級提醒，非強制擋死）\n" + BAR + "\n"
            "這一輪回覆裡出現「應該是/大概/我猜」這類猜測語言：\n" + body +
            "\n📜 守則#03 原文：\n"
            "  「在回答用戶之前，一定要先經過自我驗證再給出答案。」\n\n"
            "2026-07-02 教練查過去32天對話紀錄：這條守則已被違反至少6次，\n"
            "跟案例37的HTML問題同樣頻率，這是機關化提醒，不是又一次空談。\n\n"
            "✅ 停下來自問：\n"
            "  1. 這句話的內容，我剛才真的用工具查證過嗎？還是憑印象講的？\n"
            "  2. 如果沒查證 → 現在補查，或誠實說「不確定，需要查證」（守則#15）。\n"
            "  3. 如果已經查證過 → 把查證過程講出來（怎麼查的、結果是什麼），\n"
            "     不要只寫結論。\n\n"
            "本次為提醒，不阻擋回覆送出；違規記錄已寫入：%s\n" % path + BAR + "\n")

# ════════════════════════════════════════════════
# F. 守則#08 多此一舉徵詢（提醒，不擋）—— 原 rule08_ask_when_clear_check.sh
# ════════════════════════════════════════════════
F_PATTERNS = [
    r"要不要我", r"是否需要我", r"您希望我", r"需要我.*嗎", r"要我.*嗎",
    r"要不要.*進行", r"是否.*繼續",
]
F_WHITELIST = re.compile(
    r"不可逆|刪除|危險|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|方向不明|方向模糊|不確定您想要|多種.*(方式|方案|解讀)")

if LAST_TEXT:
    hits = []
    for line in LAST_LINES:
        if F_WHITELIST.search(line):
            continue
        for p in F_PATTERNS:
            if re.search(p, line):
                hits.append("  • 偵測到疑似多此一舉的徵詢：「%s...」" % line[:60])
                break
    if hits:
        body = "\n".join(hits) + "\n"
        path = log_violation("rule08_ask_violations.log", body)
        MESSAGES.append(
            "\n🌱 守則#08 多此一舉徵詢偵測（系統 grep，Warn 級提醒，非強制擋死）\n" + BAR + "\n"
            "這一輪回覆裡出現「要不要我/是否需要」這類徵詢語言：\n" + body +
            "\n📜 守則#08 原文：\n"
            "  「除非這個決定是不可逆的，否則就應該立即去執行。」\n\n"
            "2026-07-02 教練查過去32天對話紀錄：這條守則已被違反至少6次，\n"
            "跟案例37的HTML問題同樣頻率，這是機關化提醒，不是又一次空談。\n\n"
            "✅ 停下來自問（E06方向分流鐵律）：\n"
            "  1. 這件事教練的方向真的模糊嗎？還是其實已經說清楚了，我在多問？\n"
            "  2. 這個決定不可逆嗎？不可逆才需要問，可逆的話直接做。\n"
            "  3. 如果方向真的不清楚 → 保留這句問話，這是對的。\n"
            "  4. 如果方向其實清楚 → 刪掉徵詢語言，直接改成「我要做 X」的陳述句。\n\n"
            "本次為提醒，不阻擋回覆送出；違規記錄已寫入：%s\n" % path + BAR + "\n")

# ════════════════════════════════════════════════
# G. 守則#11 主動提醒開新視窗（提醒，不擋）
#    原 rule_proactive_session_reminder_check.sh
# ════════════════════════════════════════════════
G_THRESHOLD, G_BAND = 20, 10
if TURNS >= G_THRESHOLD:
    cur_band = (TURNS // G_BAND) * G_BAND
    marker = "/tmp/session_proactive_mentioned_%s" % SESSION_ID
    last_mentioned = 0
    try:
        if os.path.isfile(marker):
            with open(marker) as f:
                last_mentioned = int((f.read() or "0").strip() or 0)
    except Exception:
        last_mentioned = 0
    if cur_band > last_mentioned:
        if re.search(r"開新視窗|開新的對話|新對話框|總結.{0,4}上傳|換新視窗|/clear", LAST_TEXT):
            try:
                with open(marker, "w") as f:
                    f.write(str(cur_band))
            except Exception:
                pass
        else:
            MESSAGES.append(
                "\n🌱 守則#11 主動關懷偵測（系統 grep，Warn 級提醒）\n" + BAR + "\n"
                "本場已約 %s 輪，session_length_hook 已經提醒過，但這輪回覆\n" % TURNS +
                "沒有主動跟教練提「建議開新視窗/總結上傳」——這是靠教練自己問才處理的。\n\n"
                "2026-07-02 教練親口：這條記憶檔 feedback_proactive_session_reminder.md\n"
                "早在2026-05-20就寫「視窗長度由我主動管，不等教練追問」，機制存在但沒兌現。\n\n"
                "✅ 下一輪回覆時，主動加一句提醒（不用等教練問）。\n" + BAR + "\n")

# ════════════════════════════════════════════════
# H. 交付自檢門：宣稱完成卻零憑證（擋）—— 原 delivery_check.sh
# ════════════════════════════════════════════════
H_CLAIM = re.compile(
    r"(完成了|做好了|已完成|已上線|已部署|已修復|修好了|大功告成|全部搞定|已交付|上線了|搞定了)")
H_EVIDENCE = re.compile(
    r"(commit|hash|\b[0-9a-f]{8,40}\b|✅|測試|驗證|通過|結果代碼|HTTP[ /]|exit 0|全過|憑證|跑過|實測|對比|du -sh)",
    re.IGNORECASE)
H_WHITELIST = re.compile(
    r"(還沒|尚未|未完成|不算|將會|預計|待|如果|等教練|要怎麼|怎麼樣才|是否|嗎[?？]|案例|守則|句型|偵測|hook|測試)")

if LAST_TEXT:
    claimed = False
    for ln in LAST_LINES:
        if H_WHITELIST.search(ln):
            continue
        if H_CLAIM.search(strip_quotes(ln)):
            claimed = True
            break
    if claimed and not H_EVIDENCE.search(LAST_TEXT):
        MESSAGES.append(
            "\n📦🔒 交付自檢門（守則 #03 + #05 自動對照）\n" + BAR + "\n"
            "剛才的回覆宣稱「完成了」，但整段找不到任何憑證。\n"
            "教練原話：「我真的不想當監工，都是很基本的問題，我卻要人工發現。」\n\n"
            "交付前先回答三問，並把證據放進回覆：\n"
            "  ① 我自己打開/跑過/看過成果了嗎？→ 附上輸出或測試結果\n"
            "  ② 數量、編號、規格跟教練要求的一致嗎？→ 數過再說\n"
            "  ③ 有 commit hash 或可驗證的痕跡嗎？→ 沒有 hash 不算完成（守則 #05）\n\n"
            "請先實際驗證，把憑證補進回覆再交付。\n" + BAR)
        BLOCK = True

# ════════════════════════════════════════════════
# I. 繁體字鎖（擋）—— 原 rule_traditional_chinese_check.sh
# ════════════════════════════════════════════════
I_SIMPLIFIED = (
    "这|讲|们|读|时|间|触|设|帐|额|门|儿|发|开|关|报|华|归|图|网|页|数|应|术|处|"
    "战|显|复|备|环|层|阶|观|议|语|记|认|识|让|从|众|学|国|说|话|现|会|对|还|过|"
    "动|转|输|变|传|车|军|阵|队|员|团|独|电|视|频|络|该|种|样|专|习|亲|头|简|构|"
    "济|导|济|计|谁|难|临|尽|尝|双|书|终|绝|细|统|继|绍")

if LAST_TEXT:
    found = sorted(set(re.findall(I_SIMPLIFIED, LAST_TEXT)))
    if found:
        matched = "、".join(found)
        try:
            os.makedirs(DISTILL_DIR, exist_ok=True)
            lp = os.path.join(DISTILL_DIR, "rule_traditional_chinese_violations.log")
            with open(lp, "a", encoding="utf-8") as f:
                f.write("[%s] session=%s matched=%s\n" % (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), SESSION_SHORT, matched))
        except Exception:
            lp = os.path.join(DISTILL_DIR, "rule_traditional_chinese_violations.log")
        MESSAGES.append(
            "\n🈶🔒 繁體字鎖違規偵測（系統 grep，deterministic check）\n" + BAR + "\n"
            "這一輪回覆裡偵測到疑似簡體字：%s\n\n" % matched +
            "📜 全繁體中文鐵律（教練唯一指定，試金石案例44 二犯，2026-07-10）：\n"
            "  「對話全程繁體中文，不夾簡體、不夾英文」\n\n"
            "✅ 正確做法（請立刻檢查並修正）：\n"
            "  1. 回頭逐字檢查剛才的回覆，把上面列出的每個字改成繁體對應字\n"
            "  2. 常見對照：这→這 讲→講 们→們 读→讀 时→時 间→間 设→設 额→額 发→發 开→開 关→關\n"
            "  3. 重新輸出乾淨的繁體版本給教練，不要只回覆這次有改就好，要整段重新確認過一遍\n\n"
            "違規記錄已寫入：%s\n" % lp + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# J. HTML 預覽 Chrome 查證鎖（擋）—— 原 rule_html_chrome_check.sh
# ════════════════════════════════════════════════
if HTML_EDIT_IDX >= 0 and not CHROME_EVIDENCE_IDX > HTML_EDIT_IDX:
    MESSAGES.append(
        "\n🔴🔒 HTML 預覽 Chrome 查證鎖（deterministic check，非自稱，案例46）\n" + BAR + "\n"
        "這一輪對話改過 .html 檔（%s），\n" % "、".join(HTML_FILES) +
        "但找不到「這次改動之後執行過 open -a \"Google Chrome\"」的紀錄。\n\n"
        "2026-06-17 教練親口定稿：唯一指定開啟 HTML 的瀏覽器 = Google Chrome，\n"
        "絕不依賴 Claude Code 內建無頭瀏覽器工具（preview_screenshot/preview_snapshot）\n"
        "的截圖當作「教練已看過」的證據——那是 AI 自我除錯用，不是教練親眼看過的替代品。\n"
        "2026-07-11 案例46：這條鐵律定稿後至少第四次被踩。\n\n"
        "✅ 停下來立刻執行：\n"
        "  1. open -a \"Google Chrome\" <改動後的檔案路徑或網址>\n"
        "  2. 確認畫面正確後，再回覆教練「已改好，已用 Chrome 開給您看」\n"
        "  3. 不要用「我已經截圖確認過」取代這一步——兩者不是同一件事\n" + BAR + "\n")
    BLOCK = True

# ────────────────────────────────────────────────
# 輸出：所有訊息一起送到 stderr，任一擋下級命中就 exit 2
# ────────────────────────────────────────────────
if MESSAGES:
    sys.stderr.write("\n".join(MESSAGES))

sys.exit(2 if BLOCK else 0)
