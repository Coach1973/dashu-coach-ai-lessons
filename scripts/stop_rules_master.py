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

import sys, json, re, os, time, subprocess
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


def _is_real_user_prompt(evt):
    """type=='user' 事件裡，只有『真人打的話』才算真正的回合邊界。
    Claude Code 把工具執行結果也記成 type=='user'（content 是
    [{"type":"tool_result",...}]），沒有任何 text 區塊——那不是教練
    講話，只是工具回音。用這個判斷式排除掉工具回音，才不會一輪對話
    中間隨便一個工具呼叫的回音就被誤判成『上一句教練說的話』，
    害往回掃描提早打住（2026-08-27 案例：rule07 因此瞎眼超過一個月）。"""
    content = (evt.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    if isinstance(content, list):
        return any(isinstance(c, dict) and c.get("type") == "text" for c in content)
    return False


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
#    往回掃到「上一句教練真人講的話」為止，設計寫進檔案也要抓得到
#    🔴 2026-08-27 修復：原本用 `t == "user"` 當邊界，但工具執行結果
#       (tool_result) 在 transcript 裡也是 type=="user"，一輪對話只要
#       呼叫超過一次工具，掃描就會被最近一次工具回音提早打斷，抓不到
#       更早之前（同一輪）講的違規內容。改用 _is_real_user_prompt()
#       只在遇到「真人真的講話」的 user 事件才停止，工具回音直接跳過。
_DETECTOR_WORK = re.compile(r"rule07_polling_violations|stop_rules_master|_D_EVERY|D_PATTERNS|D_WHITELIST")
_segments = []
for evt in reversed(EVENTS):
    if not isinstance(evt, dict):
        continue
    t = evt.get("type")
    if t == "user" and _is_real_user_prompt(evt):
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
            # 🔴 2026-10-06 改設計（同日第 2 次誤判）：維護偵測器本身時，工具輸入裡的規則原始碼、回測腳本、
            # 測試字串（每小時查一次…）一定會命中規則D，那是在修偵測器、不是提議輪詢。工具輸入只要提到偵測器自己
            # （規則D的違規紀錄／stop_rules_master／D_PATTERNS／迴歸測試腳本）整段不掃；助手講的話（text）照掃。
            _tool_texts = []
            if name in ("Write", "Edit"):
                _tool_texts = [inp.get("content", "") or "", inp.get("new_string", "") or ""]
            elif name == "Bash":
                _tool_texts = [inp.get("command", "") or ""]
            # 2026-11-10：用 Edit 改偵測器本身時，new_string 可能只有白名單片段、沒有上面那些名字，也要整段不掃
            if any(_DETECTOR_WORK.search(t) for t in _tool_texts) \
                    or _DETECTOR_WORK.search(inp.get("file_path", "") or "") \
                    or "test_stop_rules_master" in (inp.get("file_path", "") or ""):
                continue
            _segments.extend(_tool_texts)
TURN_TEXT = "\n".join(reversed(_segments))
TURN_LINES = TURN_TEXT.split("\n") if TURN_TEXT else []

# 3) 這一輪有沒有碰過原始 UTC timestamp（rule_taiwan_time 用）
#    照抄原腳本兩個防誤報設計：跳過 attachment 事件、跳過信封層 timestamp 欄位
_last_user_idx = None
for i in range(len(EVENTS) - 1, -1, -1):
    evt = EVENTS[i]
    if not isinstance(evt, dict):
        continue
    if evt.get("type") == "user" and _is_real_user_prompt(evt):
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
def _event_epoch(evt):
    """事件信封上的時間（ISO、結尾 Z）轉成秒數；讀不到回傳 None。"""
    from datetime import datetime, timezone
    try:
        return datetime.strptime(str((evt or {}).get("timestamp", ""))[:19], "%Y-%m-%dT%H:%M:%S") \
            .replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        return None


def _html_written_by_bash(command, window_start):
    """Bash 指令寫出（或 git add）的 .html 路徑。
    cp／mv／rsync 看「目的地」（最後一個參數），不是來源：2026-10-06 把舊頁面複製出去備份，
    抓到的是來源，被誤判成「改過」，之後約 100 個動作每輪都重複跳出（記憶 feedback_stop_hook_regex_false_positive）。
    目的地是資料夾或帶 $變數／萬用字元，指不出目的地檔案時，改指來源頁面（沒有具體檔名的就略過）；
    來源 .html 全都是存在、而且在這段事件之前就沒再動過＝原樣複製舊頁面，沒有新內容要查證，略過。"""
    out = []
    m = re.search(r"\bgit\s+add\s+(?:[\w.-]+\s+)*([~./][\w./~-]*\.html)\b", command)
    if m:
        out.append(m.group(1))
    # 範圍照舊規則：只看以 ~ . / 開頭、沒有變數的具體路徑（相對路徑的 `cp index.html index.html.bak` 備份指令舊規則就不算，維持）
    concrete = lambda p: "$" not in p and "*" not in p and re.match(r"[~./]", p) is not None
    # 只認「指令位置」的 cp/mv/rsync（開頭、換行、; & | ( 之後，或 do／then 之後）；被引號包住的文字（測試腳本、commit 訊息）不算
    for seg in re.finditer(r"(?:^|[\n;&|(]|\bdo\b|\bthen\b)[ \t]*(?:sudo[ \t]+)?(?:cp|mv|rsync)\s+([^&;|\n)]*)", command):
        args = []
        for tok in seg.group(1).split():
            if not re.fullmatch(r"[\w./~$*{}\"'@%+=:,-]+", tok):
                break  # 遇到不像檔名的字（中文標點等）＝這是文字敘述不是指令參數（commit 訊息裡寫到 rsync 會被誤抓）
            if not tok.startswith("-"):
                args.append(tok.strip("'\""))
        if len(args) < 2:
            continue
        srcs, dest = args[:-1], args[-1]
        html_srcs = [s for s in srcs if s.lower().endswith(".html") and concrete(s)]
        named = [dest] if dest.lower().endswith(".html") and concrete(dest) else html_srcs
        if not named:
            continue
        if window_start is not None and html_srcs and all(
                os.path.isfile(os.path.expanduser(s)) and os.path.getmtime(os.path.expanduser(s)) < window_start
                for s in html_srcs):
            continue
        out.extend(named)
    return out


_HTML_WINDOW_START = next((t for t in (_event_epoch(e) for e in EVENTS[-100:]) if t is not None), None)
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
            for _written in _html_written_by_bash(command, _HTML_WINDOW_START):
                HTML_EDIT_IDX = i
                if _written not in HTML_FILES:
                    HTML_FILES.append(_written)

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
# A2. 叫教練自己動手操作（擋）—— 2026-09-25 新增
#   起因：Hermes 登入自動跳出，原因在 AI 自己管得到的設定檔，AI 卻先開系統設定
#   叫教練「您在裡面找、關掉開關、麻煩您看一下」，連帶把視窗開到副螢幕。
#   放行：同一行明講「只有您/教練能」（逼 AI 先確認真的只有教練能做並說出原因）。
# ════════════════════════════════════════════════
A2_PATTERNS = [
    r"(?<![幫替為給])您(在裡面|在畫面上|在清單裡)?(找|點(?!名|頭)|按|勾|取消|關掉|打開|拖|切換|輸入)(?!的)",   # 「您輸入的是」是在描述，不是叫人做；「您點名的」＝教練指出的，不是叫人點（2026-10-05 同一場誤判兩次）
    r"(請|麻煩)您(看一下|確認一下|到|去|進入|打開|點(?!頭)|按|關|找|試)",
    r"(?<!是)您自己(去|來|改|關|開|點|按|操作|設定|處理|動手)(?!的)",   # 「那是您自己關的」是陳述事實，不是叫人做
]
A2_ALLOW = re.compile(r"只有您|只有教練|您本人|密碼|簡訊|驗證碼|連結|網址|不用|不需要|不必|免|Haiku|Sonnet|Opus|模型")  # 2026-10-30：亮燈規則本身要求寫「建議切換到 Sonnet」，被這條當成叫教練動手（8 次中常見）

if LAST_TEXT:
    hits2 = []
    for line in LAST_LINES:
        if A_WHITELIST.search(line) or A2_ALLOW.search(line):
            continue
        clean = strip_quotes(line)
        for p in A2_PATTERNS:
            m = re.search(p, clean)
            if m:
                hits2.append("  • 「%s」← %s" % (m.group(0), clean.strip()[:60]))
    if hits2:
        body = "\n".join(sorted(set(hits2))) + "\n\n"
        path = log_violation("rule12_handback_violations.log", body)
        MESSAGES.append(
            "\n🚨 守則#12 叫教練自己動手偵測（系統檢查）\n" + BAR + "\n"
            "剛才回覆叫教練自己操作電腦：\n" + body +
            "✅ 請立刻重做：\n"
            "  1. 這件事 AI 自己做得到嗎？設定檔、腳本、launchd、視窗位置、檔案——都是 AI 自己改\n"
            "  2. 做完、親眼驗證完，再回報結果\n"
            "  3. 真的只有教練能做（密碼、簡訊碼、系統安全開關），同一句要寫明\n"
            "     「我已經做了X，只剩這步只有您能做，因為Y」\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# A2b. 給教練「選單路徑步驟」卻沒先幫他打開（擋）—— 2026-10-02 新增
#   起因：A2 看到「只有您能做＋密碼」就放行，AI 就寫「到系統設定 → 時光機 → 選項，把備份頻率改成手動」，
#   教練光找這些步驟就花不少時間。教練 10/02 原話：「直接幫我開到備份頻率，甚至選好手動，只留我輸密碼，這才叫真的省事」。
#   放行：同一則回覆寫明 AI 已經把畫面打開到那一步（已幫您打開／已開到…）。
# ════════════════════════════════════════════════
# 至少兩段箭頭才算選單路徑（回測 2461 則歷史回覆：一段箭頭的「A→B」多半是「對應到」，誤判一半；兩段命中 6 則全是真的叫教練照路徑找）
A2B_PATH = re.compile(r"(系統設定|偏好設定|設定|控制台|選單|後台)[^\n→；;。，,]{0,12}→[^\n→；;。，,]{1,15}→")
A2B_DONE = re.compile(r"已(經)?(幫您)?(打開|開到|開好|跳到|切到|叫出)")

if LAST_TEXT and not A2B_DONE.search(LAST_TEXT):
    hits2b = []
    for line in LAST_LINES:
        if A_WHITELIST.search(line):
            continue
        clean = strip_quotes(line)
        m = A2B_PATH.search(clean)
        if m:
            hits2b.append("  • 「%s」← %s" % (m.group(0), clean.strip()[:60]))
    if hits2b:
        body = "\n".join(sorted(set(hits2b))) + "\n\n"
        path = log_violation("rule12_handback_violations.log", body)
        MESSAGES.append(
            "\n🚨 守則#12 給教練選單步驟偵測（系統檢查）\n" + BAR + "\n"
            "剛才回覆要教練自己照「設定 → … → …」找畫面：\n" + body +
            "✅ 請立刻重做：\n"
            "  1. 先替教練打開到那一步：系統設定用 open 'x-apple.systempreferences:<面板代號>'\n"
            "     （時光機＝com.apple.Time-Machine-Settings.extension；代號查 /System/Library/ExtensionKit/Extensions/*.appex）\n"
            "  2. 要密碼的指令放進 App 終端機分頁跑 sudo，畫面停在輸入密碼，教練只要打密碼\n"
            "  3. 回覆寫「我已經打開到X，只剩輸入密碼」，不列路徑叫教練找\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# A3. 模型分工標示（擋）—— 2026-09-25 教練親定
#   教練每丟一則 ≥15 字的話，這一輪回覆裡要有「🔵」「🟢」或「🟣」亮燈（2026-10-09 加 🔵 Haiku），
#   讓教練不用猜提醒什麼時候出現。注入端：model_tier_advisor.sh。
# ════════════════════════════════════════════════
_SKIP_PREFIX = ("<local-command", "<command-", "[SYSTEM NOTIFICATION", "<task-notification", "Caveat:")


def _prompt_text(evt):
    c = (evt.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    return "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")


_last_idx, _last_prompt = None, ""
for i in range(len(EVENTS) - 1, -1, -1):
    ev = EVENTS[i]
    if isinstance(ev, dict) and ev.get("type") == "user" and _is_real_user_prompt(ev):
        t = _prompt_text(ev).strip()
        if t and not t.startswith(_SKIP_PREFIX):
            _last_idx, _last_prompt = i, t
            break

if _last_idx is not None and len(_last_prompt) >= 15:
    _texts = []
    for ev in EVENTS[_last_idx + 1:]:
        if isinstance(ev, dict) and ev.get("type") == "assistant":
            _texts += [c.get("text", "") for c in _content_list(ev)
                       if isinstance(c, dict) and c.get("type") == "text"]
    # 2026-11-04 教練抓到：舊版只看「這一輪任何一段文字有燈」，開頭亮過一次，後面每則回覆都不用亮。
    # 改成：最後一則回覆（教練實際讀到的那則）的第一行必須有燈。
    _last_reply = _texts[-1] if _texts else ""
    _first_line = next((l for l in _last_reply.split("\n") if l.strip()), "")
    if _texts and not any(m in _first_line for m in ("🔵", "🟢", "🟣")):
        path = log_violation("model_tier_label_missing.log", "  • 教練：%s\n\n" % _last_prompt[:60])
        MESSAGES.append(
            "\n🚨 模型分工亮燈缺漏（教練 2026-09-25 親定，2026-10-09 改三燈號，2026-11-04 改成逐則檢查）\n" + BAR + "\n"
            "最後這一則回覆的第一行沒有亮燈（每一則回覆都要自己亮，不能靠前面亮過）。請補一則回覆，第一行寫：\n"
            "  「🔵 這件 Haiku 就能做」「🟢 這件 Sonnet 就能做」或「🟣 這件是 Opus 等級（理由：…）」\n"
            "規則：knowledges/模型分工規則_Opus與Sonnet.md\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# A4. 收工口令（總／總結）這一輪沒有 commit hash＝沒收工（擋）—— 2026-11-08 教練糾正
#   教練只打「總」，我反問「是要說總結嗎」。hook 其實有認出來，是我沒照做；
#   源頭改成：口令句的最後一則回覆沒有 commit hash 就擋，逼它當場收工，不准反問。
# ════════════════════════════════════════════════
_SHUTDOWN_RE = re.compile(r"^[\s]*(總結|總)[\s。！!，,]*$|^總結[，,]|總結上傳|總結一下")
if _last_idx is not None and _SHUTDOWN_RE.search(_last_prompt):
    _sd_texts = []
    for ev in EVENTS[_last_idx + 1:]:
        if isinstance(ev, dict) and ev.get("type") == "assistant":
            _sd_texts += [c.get("text", "") for c in _content_list(ev)
                          if isinstance(c, dict) and c.get("type") == "text"]
    _sd_all = "\n".join(_sd_texts)
    if _sd_texts and not re.search(r"\b[0-9a-f]{7,40}\b", _sd_all):
        path = log_violation("shutdown_cue_not_executed.log", "  • 教練：%s\n\n" % _last_prompt[:30])
        MESSAGES.append(
            "\n🚨 收工口令沒執行（執行細則 N9：聽到就直接做，不問「要不要」）\n" + BAR + "\n"
            "教練說「%s」＝收工暗號，但這一輪回覆沒有 commit hash。請立刻：\n"
            "  濃縮本場 300~500 字 → 更新接力棒 → 依 N8 判斷記憶 → commit + push 給 hash。\n"
            "單字「總」「開」也是口令，不准反問「您是要說總結嗎」。\n"
            "違規記錄已寫入：%s\n" % (_last_prompt[:10], path) + BAR + "\n")
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
            # 同一小句內「不是／沒有／未…修好了」是否定句，不是完成聲明
            if p in line and not re.search(r"(不是|並非|沒有|沒能|未能)[^，。；！？,.;!?\n]{0,8}" + re.escape(p), line):
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
    # 2026-10-30：「凌晨 3:29」「下午 4:24」是換算後的口語寫法，也算有講台灣時間（本週 16 次裡多半是這種誤判）
    # 2026-11-10 賈維斯體檢：「昨晚 8:55」「今早 08:52」也是換算後的口語寫法，被誤擋過
    has_tw = bool(re.search(r"台灣時間|台湾时间|\+8|GMT\+8|UTC\+8|凌晨|清晨|早上|上午|中午|下午|傍晚|晚上|半夜|昨晚|今晚|今早|明早", LAST_TEXT))
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
_D_TIME_UNIT = r"(?:分鐘|秒|小時)"
_D_VERB = r"(?:檢查|看一次|跑一次|掃一次|掃描|查一次|查詢|讀取|巡邏|巡查|處理|監控|盯著|盯着)"
# 2026-10-06 改設計：「每」後面必須緊接（隔）數字（可省略，如「每小時」）＋時間單位，「每次開工…多2秒檢查」不再被誤傷
_D_EVERY = r"每(?:隔|過)?\s*[0-9一二兩三四五六七八九十幾]*\s*(?:個)?"
D_PATTERNS = [
    r"%s%s.*%s" % (_D_EVERY, _D_TIME_UNIT, _D_VERB),
    r"每隔\s*[0-9一二兩三四五六七八九十幾]*\s*(?:個)?%s" % _D_TIME_UNIT,
    # 2026-10-06 改設計：「指定時間／設定時間／規定時限」的「定時」是別的詞的中間兩個字，不是「定時輪詢」；
    # 「定」前面是 X定 成詞的字就不算（「固定時間跑一次…檢查」是真的定時排程，所以「固」不排除），與關鍵動詞最多隔 20 個字
    r"(?<![指設規約預限選確決協判認鎖假肯否])定時.{0,20}(?:檢查|輪詢|掃描|查詢|處理)",
    r"cron.*(?:檢查|輪詢|掃描|查詢|處理)",
    r"背景.*%s%s" % (_D_EVERY, _D_TIME_UNIT),
    r"輪詢.*機制",
]
D_WHITELIST = re.compile(
    r"守則|案例|教訓|之前|已經|過去|糾正|檢討|反省|不要再|避免再|不應該|不能再|同一個地方|同一場對話|連續.*次|拆除|改成事件|改用事件|事件驅動|事件觸發|拿掉|廢除|退役|取消|移除輪詢|零輪詢|非輪詢|不是輪詢|不用輪詢|沒有輪詢|一次性排程|delete-after-run"
    r"|誤判|回顧|內建|既有排程|第三方|原廠設計|本身的排程|已關閉|已停用|已disable|disable|系統保護排程|heartbeat"
    r"|輪詢設計偵測|輪詢偵測"  # 2026-09-24：提到偵測器本身的名字不是提議輪詢
    # 2026-09-18 補強：討論過去事件/賈維斯計畫脈絡常被誤判
    r"|討論|決策|裁定|親定|欽定|覆核|拍板|裁示|指示|交付"
    r"|賈維斯|Phase[12345]|階段|計畫|計劃|規劃|劇本|套用|改寫|改為|改用|調整|決議"
    r"|不再|未來|新制|新規則|新規範|下次"
    # 2026-10-05：否定寫法（「不排定時輪詢」「事件到了才跑」）是在說不輪詢，不是提議，被誤判過
    r"|不(?:排|設|做|採用?|走|用)(?:定時|每隔|輪詢|排程輪詢)|沒有(?:定時|排程輪詢)|事件到了才(?:跑|做|同步)"
    # 2026-11-10 賈維斯體檢：「這不是定時檢查，是結束當下就重啟」被誤擋
    r"|不是定時|非定時|結束(?:的)?當下"
    r"|當初|當時|曾經|曾|那次|那次事故|那次事件"
    r"|應該是.*因為|因為.{0,30}(已經|改用|改成)|討論.{0,30}(改成|改用|廢除|退役)"
    # 2026-09-18 教練親自觸發第2起：介紹/列舉stop_rules_master自身13條規則時
    # 會提到「輪詢設計(D)」這種規則代稱，是在講規則叫什麼名字，不是在提議
    r"|13條規則|規則\(?[A-M]\)?|stop_rules_master|Stop hook規則|rule0[0-9]|品質稽核機制|AI團隊"
    # 2026-10-02：寫反射索引（knowledges/反射索引.json）時，「防止輪詢」的規則原文本身含定時字眼，是規則定義不是提議
    r'|"(match|say|situation|level|rank|title)"\s*:|\bS:"|條件反射|反射索引')

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
            "✅ 停下來，照順序想（前面能做就不要往後走；2026-10-13 試金石案例120 加第 1 步）：\n"
            "  1. 用的人要用的那一刻，能不能當下去拿？（用到才現看＋一分鐘快取，例：預約頁一打開才讀 Google 日曆）\n"
            "  2. 我們自己系統裡的事一發生就觸發？（教練說一句、檔案一改、訊息一到、hook/signal/restart-policy）\n"
            "  3. 對方系統主動通知（webhook）？先實測會不會漏、會不會過期要續約（Google 日曆通知漏刪除、7 天要換）。\n"
            "  4. 真的都不行，才在回覆裡寫「事件驅動不可行，因為XXX」，並講清一天跑幾次。\n"
            "  5. 如果只是在討論/引用過去案例，把這句話改寫得更明確是在「回顧」不是「提議」。\n\n"
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
# E2. 判斷題沒查就回答（擋下要求補查更正）—— 2026-10-17 教練：「先回答、答錯、再推翻自己，反反覆覆」
#     E 只抓「應該／大概」這類猜測字；最傷人的是講得很肯定的錯（案例125「您的帳號還沒開」），
#     所以改看行為：教練問原因／能不能／是不是，這一輪卻一個查證工具都沒用就給了答案。
#     問句規則與反射 R-VERIFY-BEFORE-ANSWER 共用（knowledges/反射索引.json），只改那一處。
# ════════════════════════════════════════════════
E2_BOOKKEEPING = re.compile(r"^(mcp__ccd_turn__|mcp__ccd_session__mark_chapter$|ToolSearch$|TodoWrite$)")
E2_DEFER_OR_EVIDENCE = re.compile(
    r"我先去了解|先去了解|我先查|先查清楚|我去查|查完再|還沒查|需要查證|我不確定|不知道|"
    r"查到的|實測|已驗證|已確認|剛才查|前面查|紀錄顯示|日誌顯示")


def _e2_question_re():
    try:
        idx = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledges", "反射索引.json")
        with open(idx, encoding="utf-8") as f:
            for r in json.load(f)["reflexes"]:
                if r.get("id") == "R-VERIFY-BEFORE-ANSWER":
                    return re.compile(r["match"])
    except Exception:
        pass
    return None


_E2_Q = _e2_question_re()
# 2026-10-30：系統自動附上的 <system-reminder>（其他對話框完成通知等）不是教練問的，先拿掉再判斷
_e2_prompt = re.sub(r"(<|&lt;)system-reminder>.*?((<|&lt;)/system-reminder>|$)", "", _last_prompt, flags=re.S).strip()
if (_E2_Q and _last_idx is not None and LAST_TEXT and _e2_prompt and _E2_Q.search(_e2_prompt)
        and not _last_prompt.startswith("Stop hook feedback")):
    _e2_tools = 0
    for ev in EVENTS[_last_idx + 1:]:
        if isinstance(ev, dict) and ev.get("type") == "assistant":
            for c in _content_list(ev):
                if isinstance(c, dict) and c.get("type") == "tool_use" and not E2_BOOKKEEPING.search(c.get("name", "")):
                    _e2_tools += 1
    if _e2_tools == 0 and not E2_DEFER_OR_EVIDENCE.search(LAST_TEXT):
        body = "  • 教練問：「%s」→ 這一輪 0 次查證就回答了\n" % _e2_prompt.replace("\n", " ")[:60]
        path = log_violation("rule03_verify_violations.log", "[E2 判斷題零查證]\n" + body)
        MESSAGES.append(
            "\n🔎 判斷題沒查就回答（系統偵測，2026-10-17 教練要求的「先查再答」標準）\n" + BAR + "\n" + body +
            "\n教練問的是原因／能不能／是不是，這一輪卻沒用任何工具看第一手證據就給了答案。\n"
            "📜 三大信念一：「真誠：說真話，辦真事，一切歸於真實。」\n\n"
            "✅ 現在就做：\n"
            "  1. 用工具查證剛才的答案（設定檔實際值、日誌、指令輸出、原始紀錄）\n"
            "  2. 回一則短更正，把話分成：查到的（附證據）／我的推論／還沒查的\n"
            "  3. 如果答案全是前面已查證過的，說是哪一步查到的即可\n\n"
            "違規記錄已寫入：%s\n" % path + BAR + "\n")
        BLOCK = True

# ════════════════════════════════════════════════
# F2. 守則#08／細則N2「不用問的一直問」（擋，2026-11-04）
#    F 只提醒擋不住（教練 10/28～11/04 又重複提醒約 8 次）。
#    高信心句型（要不要我／要我…嗎／還是先…？）出現在結尾幾行就擋一次；
#    N2 第①關的事（花錢、對外、不可逆、要教練登入）與「方向不明」自動放行，
#    或在同一則訊息寫一行【只有您能決定：…】自述是哪一關（會留紀錄）。
#    出錯一律放行（2026-10-16 教訓）。偵測邏輯在 scripts/ask_gate.py，測試：scripts/test_ask_gate.py
# ════════════════════════════════════════════════
F2_HIT = False
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ask_gate import should_block as _ask_should_block
    if LAST_TEXT:
        _f2_block, _f2_hits = _ask_should_block(LAST_TEXT)
        if _f2_block:
            F2_HIT = True
            _f2_body = "\n".join("  • %s：「%s」" % (n, t) for n, t in _f2_hits) + "\n"
            _f2_path = log_violation("rule08_ask_violations.log", "[F2 擋下]\n" + _f2_body)
            MESSAGES.append(
                "\n🔴 不用問的一直問（系統擋下一次，執行細則 N2）\n" + BAR + "\n" + _f2_body +
                "\n你在結尾向教練討許可。N2：方向清楚 → 直接執行，不問「要做嗎」。\n"
                "請三選一，改好再回覆：\n"
                "  A. 這件事在教練這次交辦的範圍內 → 刪掉問句，直接做，做完回報憑證。\n"
                "  B. 是範圍外的「順手」項目 → 不做也不問，寫進接力棒「🔧AI自己的工作清單」（N7）。\n"
                "  C. 真的只有教練能決定（花錢／代表他對外發言／不可逆／需他本人登入／他自己的內容與喜好）\n"
                "     → 保留問句，並在同一則訊息加一行：【只有您能決定：<是哪一種>】\n"
                "三關：①只有教練能做 ②教練沒答過（先查接力棒與記憶）③現在不問會卡住。\n"
                "違規記錄已寫入：%s\n" % _f2_path + BAR + "\n")
            BLOCK = True
except Exception:
    pass

# ════════════════════════════════════════════════
# F3. 回報固定「結論一句＋您要做什麼」（擋一次，2026-11-04 交辦 ⑥）
#    只檢查「這一輪有做事」（有非記帳工具呼叫）的回覆；純閒聊不擋。
#    回覆裡沒有「您要做什麼：」那一行就擋一次（寫「您要做什麼：沒有，不用做」即可放行）。
#    出錯一律放行。
# ════════════════════════════════════════════════
F3_MARK = re.compile(r"(?m)^\s*(?:[>\-*#]+\s*)?\**您要做什麼\**\s*[:：]")
try:
    if LAST_TEXT and not F2_HIT:
        _f3_turn_start = 0
        for _i, _e in enumerate(EVENTS):
            if isinstance(_e, dict) and _e.get("type") == "user" and _is_real_user_prompt(_e) \
                    and not _prompt_text(_e).lstrip().startswith(("Stop hook feedback", "<system-reminder")):
                _f3_turn_start = _i
        _f3_tools = 0
        _f3_wrapped = False
        for _e in EVENTS[_f3_turn_start:]:
            if isinstance(_e, dict) and _e.get("type") == "assistant":
                for _x in _content_list(_e):
                    if isinstance(_x, dict) and _x.get("type") == "tool_use" \
                            and not E2_BOOKKEEPING.search(_x.get("name", "")):
                        _f3_tools += 1
                    # 2026-11-10 賈維斯體檢（教練核准）：這一輪已呼叫 wrap_up，桌面版下一步框就是
                    # 「結論＋您要做什麼」（有 ask＝要教練做的事，沒有 ask＝沒有，不用做），不必在文字再擋一次
                    if isinstance(_x, dict) and _x.get("type") == "tool_use" \
                            and _x.get("name", "") == "mcp__ccd_turn__wrap_up":
                        _f3_wrapped = True
        if _f3_tools > 0 and not _f3_wrapped and not F3_MARK.search(LAST_TEXT):
            _f3_body = "  • 這一輪做了 %d 次工具操作，回覆末尾沒有「您要做什麼：」那一行\n" % _f3_tools
            _f3_path = log_violation("rule_report_format_violations.log", "[F3 擋下]\n" + _f3_body)
            MESSAGES.append(
                "\n🔴 回報格式缺「您要做什麼」（系統擋下一次，2026-11-04 交辦 ⑥）\n" + BAR + "\n" + _f3_body +
                "\n做事的回報固定兩行收尾，改好再回覆：\n"
                "  結論：<一句話講做完了什麼或查到什麼>\n"
                "  您要做什麼：<需要教練做的一件事>，沒有就寫「沒有，不用做」\n"
                "違規記錄已寫入：%s\n" % _f3_path + BAR + "\n")
            BLOCK = True
except Exception:
    pass

# ════════════════════════════════════════════════
# F. 守則#08 多此一舉徵詢（提醒，不擋）—— 原 rule08_ask_when_clear_check.sh
# ════════════════════════════════════════════════
F_PATTERNS = [
    r"要不要我", r"是否需要我", r"您希望我", r"需要我.*嗎", r"要我.*嗎",
    r"要不要.*進行", r"是否.*繼續",
    # 2026-10-02 教練反問「為什麼要改／不做為什麼不做」：「我等你決定」「要不要把X」「還是先Y？」舊句型全漏抓
    # （回測30天 assistant 文字 4.1 萬行命中 83 行，多數是能自己判斷卻推回教練）
    r"等(你|您)(決定|裁示|拍板)", r"要不要把.*[？?]", r"還是先.*[？?]",
]
F_WHITELIST = re.compile(
    r"不可逆|刪除|危險|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|方向不明|方向模糊|不確定您想要|多種.*(方式|方案|解讀)")

if LAST_TEXT and not F2_HIT:
    hits = []
    for line in LAST_LINES:
        if F_WHITELIST.search(line):
            continue
        for p in F_PATTERNS:
            if re.search(p, strip_quotes(line)):   # 引號內是在引用句型，不算自己在徵詢
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
            "✅ 停下來自問（執行細則N2：什麼時候可以問教練）：\n"
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
        "  2. 確認畫面正確後回報教練：Mac 螢幕上的 Chrome 只有人坐在 Mac 前才看得到，教練用手機或遠端時看不到、不算交付，不要寫「已開給您看／已在 Mac 開過」。要交付就放到教練打得開的 https 網址（獨立一行），用 curl 驗證狀態 200 和內容再給（2026-10-04 教練抓到）\n"
        "  3. 不要用「我已經截圖確認過」取代這一步——兩者不是同一件事\n" + BAR + "\n")
    BLOCK = True

# ════════════════════════════════════════════════
# K. 記憶寫了但沒進索引（提醒，不擋）—— 2026-08-25 賈維斯體檢新增
#    守則#01「記不住，肯定就用不出來」：MEMORY.md 是唯一會載進 context 的索引，
#    記憶檔沒收錄進去 = 下次 session 根本讀不到 = 等於沒寫。
#    只看最近 24 小時碰過的檔案，避免每次噴出一長串舊帳。
# ════════════════════════════════════════════════
BRAIN_DIR = os.path.expanduser("~/.openclaw/workspace/claude-brain")
try:
    _idx_path = os.path.join(BRAIN_DIR, "MEMORY.md")
    with open(_idx_path, encoding="utf-8") as f:
        _idx_text = f.read()
    _linked = set(re.findall(r"\]\(([^)]+\.md)\)", _idx_text))
    # 2026-10-16：舊記憶從 10/14 起正式收在 MEMORY_ARCHIVE_INDEX.md（MEMORY.md 有連過去），
    # 只看 MEMORY.md 會把「今天補改的舊記憶」誤報成漏收。兩份索引都算。
    try:
        with open(os.path.join(BRAIN_DIR, "MEMORY_ARCHIVE_INDEX.md"), encoding="utf-8") as f:
            _linked |= set(re.findall(r"\]\(([^)]+\.md)\)", f.read()))
    except Exception:
        pass
    _cutoff = time.time() - 86400
    _missing = []
    for _fn in os.listdir(BRAIN_DIR):
        if not _fn.endswith(".md") or _fn in ("MEMORY.md", "MEMORY_ARCHIVE_INDEX.md") or _fn.startswith("daily_"):
            continue
        if _fn in _linked:
            continue
        if os.path.getmtime(os.path.join(BRAIN_DIR, _fn)) >= _cutoff:
            _missing.append(_fn)
    if _missing:
        MESSAGES.append(
            "\n🧠 記憶索引漏收提醒（deterministic check，2026-08-25 體檢立法）\n" + BAR + "\n"
            "這 24 小時內寫了記憶檔，但 MEMORY.md 索引沒有收錄：\n" +
            "".join("  • %s\n" % m for m in sorted(_missing)) +
            "\n📜 守則#01：「如果你記不住用戶說的話，你就是不在乎」\n"
            "  「記不住，肯定就用不出來。」\n\n"
            "⚠️ MEMORY.md 是唯一會自動載進新對話的索引檔。\n"
            "  記憶檔沒進索引 = 下次開新對話框讀不到 = 這次寫的等於白寫。\n\n"
            "✅ 立刻補上（一行就好）：\n"
            "  - [標題(日期)](檔名.md) — 一句話說明什麼情況要用它\n" + BAR + "\n")
except Exception:
    pass

# 🔴🔴🔴 2026-09-06再修正：教練連續追問「為什麼一直忘記」後查明——過去這條規則
# 只檢查「這個名字有沒有出現在coach888/index.html任何地方」，等於只要隨便塞進
# 哪個分類都會通過檢查。教練實際只會看「大樹常用」跟「後臺系統」這兩個分類，
# 但因為檢查標準太鬆，我一直把新項目塞進「保留（尚未推Netlify）」這種教練不會
# 點開的分類，防呆機制覺得「有放就好」直接放行，教練卻永遠找不到——錯誤因此
# 一直複製自己，不是記性問題，是檢查標準本身不夠嚴格。已改成：只承認出現在
# 「大樹常用」(changyong) 或「後臺系統」(houtai) 這兩個分類裡才算真的收錄，
# 放在其他分類一律視同沒收錄，逼自己每次都要放在教練真的會看的地方。
_COACH888_VISIBLE_SECTIONS = ("changyong", "houtai")


def _extract_visible_section_html(full_html):
    """只留下「大樹常用」+「後臺系統」這兩個分類的HTML片段，其餘分類(保留/
    不公開/BNI專用等)的內容一律不算數——這是防呆機制真正在乎的範圍，不是
    整份檔案的任何角落。"""
    chunks = []
    for section_id in _COACH888_VISIBLE_SECTIONS:
        start_marker = f'<div class="grid" data-section="{section_id}">'
        end_marker = f'<button class="btn-add-item" data-section="{section_id}">'
        s = full_html.find(start_marker)
        e = full_html.find(end_marker)
        if s != -1 and e != -1 and e > s:
            chunks.append(full_html[s:e])
    return "\n".join(chunks)


# 🔴 2026-10-14 假陽性修正：coach888 畫面實際讀的是伺服器同步狀態（/api/coach888/state），
# 不是 git 裡的靜態 index.html（2026-09-24 查證）；coach888_register_admin.py 也只寫伺服器。
# 只查靜態檔會讓「已收進大樹常用」的項目一直被擋。改成兩邊都查，任一邊命中就算收錄。
def _coach888_server_visible_text():
    try:
        import urllib.request
        req = urllib.request.Request("https://event.bymyway.com/api/coach888/state",
                                     headers={"User-Agent": "Mozilla/5.0", "Origin": "https://coach1973.github.io"})
        with urllib.request.urlopen(req, timeout=4) as r:
            state = json.loads(r.read().decode("utf-8"))
        layout = json.loads(state.get("coach888_layout") or "{}")
        items = json.loads(state.get("coach888_items") or "{}")
        out = []
        for sec in _COACH888_VISIBLE_SECTIONS:
            for u in layout.get(sec, []):
                out.append(u)
                out.append(str((items.get(u) or {}).get("name", "")))
        return "\n".join(out)
    except Exception:
        return ""


# ════════════════════════════════════════════════
# L. 新網站上線但沒收錄進coach888作品一覽（擋）—— 2026-09-04教練親定
#    起因：tainan-shangquan網站上線後漏放coach888，教練回報「怎麼我看不到」
#    才發現，這是v179「7新站+1後台工具全漏」之後同款坑第二次發作。
#    教練原話：「請寫入SOP新的網頁做好一律收錄，不要再讓我提醒」——
#    純文字SOP靠AI自己記得會再忘第三次，改成deterministic check：
#    只要這次對話執行過 `gh repo create ... --public`（=新公開網站上線的
#    唯一入口動作），就檢查本機coach888/index.html有沒有提到這個repo名稱，
#    沒有就擋下 Stop，逼自己補完才能收工。
# ════════════════════════════════════════════════
NEW_PUBLIC_REPOS = []
for evt in EVENTS[-300:]:
    if not isinstance(evt, dict) or evt.get("type") != "assistant":
        continue
    for c in _content_list(evt):
        if not isinstance(c, dict) or c.get("type") != "tool_use" or c.get("name") != "Bash":
            continue
        command = str((c.get("input") or {}).get("command", ""))
        # 🔴 2026-09-04當場修復：command裡若含heredoc定界符(<<)，代表這段文字
        # 是「寫進檔案的內容」而非「真的要執行的指令」——本規則上線當天就被
        # 自己寫的測試heredoc(cat > test.jsonl << 'EOF' ... gh repo create ...)
        # 誤判成真的建立過repo，教練直接把Stop hook的假警報轉貼回來才發現。
        # 含heredoc的command一律跳過此規則偵測，避免同一種假陽性再犯。
        if re.search(r"<<[-~]?\s*['\"]?\w+['\"]?", command):
            continue
        for m in re.finditer(r"gh\s+repo\s+create\s+[\w.-]+/([\w.-]+)[^\n&|;]*--public", command):
            name = m.group(1)
            if name.lower() not in ("coach888",) and name not in NEW_PUBLIC_REPOS:
                NEW_PUBLIC_REPOS.append(name)

# 🔴 2026-09-06補強：漏洞——上面只認`gh repo create --public`，但這次的真實案例是
# 在「既有」repo(ai-go)裡新增一個頁面(curation-inject.html)，沒有建新repo，完全繞過
# 上面的偵測。教練當場抓到（策展一鍵注入頁面沒收錄coach888），這是同一種坑第三次發作。
# 補一個更寬的訊號：commit message裡出現「新增...頁面/網站/工具/系統」這類措辭，
# 代表這輪對話交付了一個「使用者看得到的新東西」，一樣要檢查有沒有進coach888。
#
# 🔴🔴 2026-09-06當晚第四次發作後查明：這條規則從建立那刻起就是死的。
# 兩個獨立bug疊在一起：①上面沿用L1的heredoc排除邏輯，把含`<<'EOF'`的command整段
# 跳過——但commit message一律用heredoc包多行文字是系統prompt明文規定的標準做法
# （見Bash工具說明「ALWAYS pass the commit message via a HEREDOC」），等於這條
# 規則對100%的正常commit都會跳過，從來沒有真的檢查過任何一次commit。
# ②就算不跳過，`-m\s+["']新增`這個anchor要求「新增」緊接在-m後面的引號之後，
# heredoc格式是`-m "$(cat <<'EOF'`，真正的文字內容在下一行，永遠對不上這個anchor。
# 已修復：①拿掉heredoc排除(這條規則的風險跟L1不同——L1排除heredoc是怕heredoc
# 內容本身在「寫一個含假指令文字的測試檔案」，L2只是找commit message裡的中文
# 措辭，heredoc內的文字才是要抓的目標，不该跳過) ②拿掉`-m\s+["']`這個anchor，
# 改成整個command字串裡找`新增`+詞尾，不要求緊接在-m後面 ③詞尾清單太窄
# （只有頁面/網站/工具/系統4個詞），這次真實案例寫的是「新增...後台管理頁」
# （頁面的簡寫「頁」），已補上頁/後台/平台/管理頁/入口這幾種常見簡寫。
NEW_NAMED_ITEMS = []
NEW_NAMED_FILES = {}   # 2026-10-14：名稱 -> 同一個 commit 指令裡出現的 xxx.html 檔名（改名後仍可用網址比對）
for evt in EVENTS[-300:]:
    if not isinstance(evt, dict) or evt.get("type") != "assistant":
        continue
    for c in _content_list(evt):
        if not isinstance(c, dict) or c.get("type") != "tool_use" or c.get("name") != "Bash":
            continue
        command = str((c.get("input") or {}).get("command", ""))
        # 🔴 2026-09-19第二次發現：`"git commit" not in command`只看子字串存在，
        # 抓不出「這段文字是不是真的在呼叫git commit」——本場修這條規則本身時，
        # 寫了一支python heredoc測試腳本，裡面用字串變數存了一行範例文字
        # `commit_msg_legit = 'git commit -m "新增「大台南策展中心」後台管理頁..."'`
        # 純粹是測試資料，這個Bash command從頭到尾沒有真的執行過一次git commit，
        # 但因為子字串比對命中，一樣被當成「這輪真的commit了」去抓「新增OO」
        # 措辭，變成同一個假陽性用不同commit又跳出來一次。改用位置感知的
        # regex：只有「git commit」前面是字串開頭/換行/`;`/`&&`/`||`/`|`（也就是
        # 真的在shell命令的位置上，不是被包在引號裡當一段文字）才算數。
        _commit = re.search(r"(^|\n|;|&&|\|\||\|)\s*git\s+commit\b", command)
        if not _commit:
            continue
        # 🔴 2026-10-05 第三次假陽性（設計修正，不再補白名單）：同一個 Bash 指令裡，commit 前面常有
        # 測試／回測用的 python 範例句（"新增了金質獎章頁面"），而且 commit 訊息自己會用「新增…」當範例引用。
        # 所以：①只掃 git commit 之後的文字（真正的 commit 訊息在這之後）；②跳過緊接在「『（【[ 之後的「新增」
        # ——那是被引用的範例句，不是宣告（真宣告 `-m "新增XX頁面"` 前面是 ASCII 引號，仍抓得到）。
        for m in re.finditer(
            r"(?<![「『（(【\[])新增([^\n\"'：:]{1,30}(?:頁面|頁|網站|網頁|工具|系統|後台|平台|管理頁|入口))",
            command[_commit.end():],
        ):
            name = m.group(1).strip()
            if not name or name in NEW_NAMED_ITEMS:
                continue
            # 🔴 2026-10-05發現：「新增【的】分會之光主頁（看不到）」這種描述既有東西的句子
            # （commit 訊息引用教練的問話）會被抓成候選名稱，同一場 session 反覆跳出。
            # 真正的「新增OO頁面」宣告不會以助詞「的」開頭，這種視為散文子句不當候選
            # （不濾「了」：「新增了金質獎章頁面」是真的宣告，回測時發現會漏掉）。
            if name[0] == "的":
                continue
            # 🔴 2026-09-19發現：自由文字commit訊息裡的完整子句（例如「新增「海餅乾
            # 俱樂部」卡片，連到該案例網站」）會被這個regex從「新增」抓到最近的
            # 後綴詞為止，把中間整段逗號子句都當成候選名稱——這種字串永遠不會
            # 出現在coach888的連結文字裡，等於每次都是假陽性，而且因為上面
            # EVENTS[-300:]每次Stop都重新掃描歷史commit，同一個假陽性會在同一場
            # session裡無限重複跳出，不會隨著已經澄清/已經處理過而消失。
            # 真正的「新增OO頁面」宣告用語是乾淨的短名詞（通常<=16字、不含逗號/
            # 句號/頓號），這裡加一層過濾，超長或含這些標點的視為抓錯範圍（多半
            # 是中文散文夾帶的子句），不當成候選名稱。注意：不能拿「「」」引號當
            # 過濾條件——中文專有名詞常用「」包起來，這樣會把真正該抓到的合法
            # 案例也一起濾掉（實測「「大台南策展中心」後台管理頁」這個文件裡
            # 記載的真實案例，含「」但不含逗號/句號，必須留著才抓得到）。
            if len(name) > 16 or re.search(r"[，。、]", name):
                continue
            # 🔴 2026-10-16 同場第二次假陽性（改設計）：「新增 2 個技能（網站打不開…」被抓成「2 個技能（網站」。
            # 後綴詞（網站／頁面…）落在還沒關上的括號裡＝那是括號內的說明，不是被新增東西的名字。
            if name.count("（") > name.count("）") or name.count("(") > name.count(")"):
                continue
            NEW_NAMED_ITEMS.append(name)
            NEW_NAMED_FILES[name] = [f for f in set(re.findall(r"([\w-]+\.html)\b", command)) if f != "index.html"]

if NEW_NAMED_ITEMS:
    try:
        with open(os.path.join(HOME, "github_repos", "coach888", "index.html"), encoding="utf-8") as f:
            COACH888_HTML_2 = f.read()
    except Exception:
        COACH888_HTML_2 = None
    if COACH888_HTML_2 is not None:
        VISIBLE_HTML_2 = _extract_visible_section_html(COACH888_HTML_2) + "\n" + _coach888_server_visible_text()
        # commit訊息裡的措辭是「XX頁面」，但coach888連結文字通常不帶這個後綴字，
        # 兩種寫法都查一次，任一種命中就算已收錄，避免措辭差異造成假陽性。
        # 2026-09-06再修正：只在「大樹常用」「後臺系統」範圍內找，不是整份檔案
        # 任何角落——放在「保留」等教練不會看的分類一樣視同沒收錄。
        def _in_html(n):
            core = re.sub(r"(?:頁面|頁|網站|網頁|工具|系統|後台|平台|管理頁|入口)$", "", n).strip()
            return (n in VISIBLE_HTML_2 or (core and core in VISIBLE_HTML_2)
                    or any(f in VISIBLE_HTML_2 for f in NEW_NAMED_FILES.get(n, [])))
        missing_named = [n for n in NEW_NAMED_ITEMS if not _in_html(n)]
        if missing_named:
            in_wrong_section = [n for n in missing_named if n in COACH888_HTML_2 or (re.sub(r"(?:頁面|頁|網站|網頁|工具|系統|後台|平台|管理頁|入口)$", "", n).strip() in COACH888_HTML_2)]
            MESSAGES.append(
                "\n🔴🔒 coach888作品一覽收錄鎖・第二層（deterministic check，2026-09-06二次補強）\n" + BAR + "\n"
                "這次對話的commit訊息裡出現「新增OO頁面/網站/工具/系統」這類措辭，\n"
                "但在「大樹常用」／「後臺系統」這兩個教練實際會看的分類裡查不到：\n" +
                "".join("  • %s%s\n" % (n, "（在檔案別處找到，但放錯分類）" if n in in_wrong_section else "") for n in missing_named) +
                "\n這條規則只認「大樹常用」跟「後臺系統」兩個分類算真的收錄——放進\n"
                "「保留」等其他分類，教練一樣找不到，等同沒收錄。\n\n"
                "✅ 立刻執行，收工前不能跳過：\n"
                "  1. 確認這個新東西是不是「教練或訪客會用到的獨立頁面/工具」\n"
                "     （如果只是內部程式檔案、不是給人看的頁面，可以忽略這條提醒）\n"
                "  2. 是的話，打開 ~/github_repos/coach888/index.html，放進「大樹常用」\n"
                "     或「後臺系統」其中一個分類（已經放在其他分類的話，用剪的搬過去）\n"
                "  3. commit + push，curl驗證coach1973.github.io/coach888/正式站已生效\n" + BAR + "\n")
            BLOCK = True

if NEW_PUBLIC_REPOS:
    try:
        with open(os.path.join(HOME, "github_repos", "coach888", "index.html"), encoding="utf-8") as f:
            COACH888_HTML = f.read()
    except Exception:
        COACH888_HTML = None
    if COACH888_HTML is not None:
        VISIBLE_HTML = _extract_visible_section_html(COACH888_HTML) + "\n" + _coach888_server_visible_text()
        missing_repos = [r for r in NEW_PUBLIC_REPOS if r not in VISIBLE_HTML]
        if missing_repos:
            in_wrong_section = [r for r in missing_repos if r in COACH888_HTML]
            MESSAGES.append(
                "\n🔴🔒 coach888作品一覽收錄鎖（deterministic check，2026-09-06二次補強）\n" + BAR + "\n"
                "這次對話用 `gh repo create ... --public` 建立了新網站repo，\n"
                "但在「大樹常用」／「後臺系統」這兩個教練實際會看的分類裡查不到：\n" +
                "".join("  • %s%s\n" % (r, "（在檔案別處找到，但放錯分類）" if r in in_wrong_section else "") for r in missing_repos) +
                "\n教練原話：「請寫入SOP新的網頁做好一律收錄，不要再讓我提醒」。\n"
                "只認「大樹常用」跟「後臺系統」算真的收錄——放進「保留」等其他\n"
                "分類，教練一樣找不到，等同沒收錄（這是第三次因為這樣被抓到）。\n\n"
                "✅ 立刻執行，收工前不能跳過：\n"
                "  1. 打開 ~/github_repos/coach888/index.html，放進「大樹常用」\n"
                "     （新項目一律放該分類第一項）或「後臺系統」\n"
                "  2. 加入這個新網站的連結+名稱，其餘項目num自動+1\n"
                "  3. commit + push，curl驗證coach1973.github.io/coach888/正式站已生效\n"
                "  4. 如果這個repo其實不是要給教練/會員看的網站（例如純備份/工具型\n"
                "     repo），下次建立時改用 `gh repo create ... --private`，這條鎖\n"
                "     只認 --public，不會誤攔私有備份repo\n" + BAR + "\n")
            BLOCK = True

# ════════════════════════════════════════════════
# M. coach888結構性稽核（擋）—— 2026-09-06教練連續4次「找不到/有沒有收錄」後建立
#    跟L/L2不一樣：完全不看commit訊息措辭，每一輪都無條件直接讀
#    event-signup/app.py的真實路由 vs coach888實際內容比對，不會被
#    「我這次剛好沒把新增兩個字寫進commit訊息」這種文字遊戲繞過去。
#    只有超出scripts/coach888_audit_baseline.txt既定基準線的「新」缺漏
#    才會擋收工——已知、教練已首肯保留現狀的舊項目不會每次都卡。
# ════════════════════════════════════════════════
try:
    _audit_script = os.path.join(HOME, ".openclaw", "workspace", "scripts", "audit_coach888_coverage.py")
    audit_result = subprocess.run(
        ["python3", _audit_script, "--strict"],
        capture_output=True, text=True, timeout=15,
    )
    if audit_result.returncode == 1:
        MESSAGES.append(
            "\n🔴🔒 coach888結構性稽核鎖（deterministic check，不看措辭，2026-09-06建立）\n" + BAR + "\n"
            + audit_result.stdout +
            "\n這條規則直接讀程式碼路由清單比對coach888，跟commit訊息怎麼寫無關。\n\n"
            "✅ 立刻執行：\n"
            "  1. 確認這是不是真的要給教練/訪客看的獨立頁面\n"
            "  2. 是的話，補進coach888「大樹常用」「後臺系統」或「bymyway自架版」\n"
            "  3. 如果決定暫不收錄(如純技術端點/待啟用)，把路徑加進\n"
            "     scripts/coach888_audit_baseline.txt並寫清楚為什麼，這樣不會\n"
            "     每次都卡在同一個已經想清楚的決定上\n" + BAR + "\n")
        BLOCK = True
except Exception:
    pass  # 稽核腳本本身故障不該擋住教練收工，靜默跳過

# ════════════════════════════════════════════════
# N. 照抄鎖（擋）—— 2026-10-21 my-tools 改 11 版後建立
#    教練說過「一模一樣／照抄／比照 X」→ 這場對話之後改到 ~/github_repos 的網頁，
#    收工前必須跑過 scripts/parity_check.py 而且「缺 0 項」。
#    不看 AI 怎麼說，只看有沒有真的跑、跑出來缺幾項。
#    教練明說可以不一樣的項目寫進目標倉庫 .parity-allow。
#    任何例外一律放行（hook 壞了不能擋教練，見 feedback_hooks_must_fail_open）。
# ════════════════════════════════════════════════
try:
    _IDENT = re.compile(r"一模一樣|照抄|(比照|照著|依照|參考|跟)[^。！？\n]{0,14}(作品一覽|作品總覽|那個網站|那一頁|那頁|那套)")
    _REPO = os.path.join(HOME, "github_repos") + os.sep
    _ident_idx, _last_edit_idx, _last_pass_idx = None, None, None
    _edited, _pending = [], {}
    for _i, _e in enumerate(EVENTS):
        if not isinstance(_e, dict):
            continue
        _t, _c = _e.get("type"), (_e.get("message") or {}).get("content")
        if _t == "user" and _is_real_user_prompt(_e):
            _txt = _c if isinstance(_c, str) else " ".join(
                x.get("text", "") for x in _c if isinstance(x, dict) and x.get("type") == "text")
            if not _txt.lstrip().startswith(("Stop hook feedback", "<system-reminder")) and _IDENT.search(_txt):
                if _ident_idx is None:
                    _ident_idx = _i
        if _t == "assistant" and isinstance(_c, list):
            for _x in _c:
                if not (isinstance(_x, dict) and _x.get("type") == "tool_use"):
                    continue
                _inp = _x.get("input") or {}
                _fp = str(_inp.get("file_path") or "")
                _cmd = str(_inp.get("command") or "")
                if _x.get("name") in ("Edit", "Write") and _fp.startswith(_REPO) and _fp.endswith((".html", ".js")):
                    _last_edit_idx = _i; _edited.append(_fp)
                if _x.get("name") == "Bash" and "parity_check.py" in _cmd:
                    _pending[_x.get("id")] = _i
                if _x.get("name") == "Bash" and re.search(r"(>{1,2}|\btee|sed -i\S*|\bcp|\bmv)\s+[^|;&]*github_repos/\S+\.(html|js)\b|github_repos/\S*\s*&&[^|;]*\bbuild\.py", _cmd):
                    _last_edit_idx = _i; _edited.append(_cmd[:60])
        if _t == "user" and isinstance(_c, list):
            for _x in _c:
                if isinstance(_x, dict) and _x.get("type") == "tool_result" and _x.get("tool_use_id") in _pending:
                    _out = _x.get("content")
                    _out = _out if isinstance(_out, str) else json.dumps(_out, ensure_ascii=False)
                    if "缺 0 項" in _out:
                        _last_pass_idx = _i
    if _ident_idx is not None and _last_edit_idx is not None and _last_edit_idx > _ident_idx \
            and (_last_pass_idx is None or _last_pass_idx < _last_edit_idx):
        MESSAGES.append(
            "\n🔴🔒 照抄鎖（deterministic check，2026-10-21 my-tools 改 11 版後建立）\n" + BAR + "\n"
            "教練在這場說過「一模一樣／照抄／比照」，你也改了網頁：\n  " + "\n  ".join(_edited[-3:]) + "\n"
            "但改完之後沒有跑過照抄對照器，或跑出來還有缺。\n\n"
            "✅ 立刻執行：\n"
            "  1. python3 ~/.openclaw/workspace/scripts/parity_check.py <標準答案.html> <你改的頁>\n"
            "  2. 缺的項目照抄補上（以標準答案的程式為底，不要另寫一套）\n"
            "  3. 跑到「缺 0 項」才算交付；教練明說可以不一樣的，寫進目標倉庫 .parity-allow\n" + BAR + "\n")
        log_violation("rule_parity_copy_violations.log", "edited=%s\n" % _edited[-3:])
        BLOCK = True
except Exception:
    pass

# ════════════════════════════════════════════════
# O. 含糊指稱鎖（擋）—— 2026-10-21 教練：「你給了一句非常模糊的話，害我去搜尋是不是這兩條」
#    回覆講到「一條／某個／那個…網址、連結、群組、機器人、網站」，卻沒寫出是哪一個，教練只能自己猜。
#    同類第二次（第一次 10/18 群組沒寫全名，記憶 feedback_always_name_the_group_bot_site_in_full），
#    照執行細則 N8 改機制、不加記憶。只看最後給教練的回覆；引用（> 開頭、「」內）與程式碼區塊不算。
#    一條／某個＝同一段要寫出來；這條／那個＝整則回覆或教練剛貼的話裡有寫出來就算。
#    網址／連結要有 http、網域或 `/路徑`；群組／機器人／網站要有「全名」或網址。做／建／開一個新網站不算。
# ════════════════════════════════════════════════
try:
    # 回測 333 則真實回覆後收緊（10/21）：中間只准隔 4 個字，或「…的…」修飾（一條帶 key= 的策展上傳網址）；
    # 半形逗號、頓號也斷句；同一個／哪一個／每一個／各有一個／沒有一個／十一個（數字）／貼了一個（自己做的測試）
    # 不是在指某一條，不算；「某個」中文多半是泛指（以後要停掉某個網站），不列入
    _SEP = r"[^。！？，,、；;：:\n]"
    _VAGUE = re.compile(r"(一條|一個|另一條|另一個|有條|那條|那個|這條|這個)"
                        r"(?:%s{0,4}?|%s{0,12}?的%s{0,6}?)(短網址|網址|連結|群組|機器人|網站)" % (_SEP, _SEP, _SEP))
    # 這條／那個：上下文接得上就不算含糊——看這一則、教練剛說的話、再往前兩輪的對話
    _recent, _seen_prompts = [], 0
    for _e in reversed(EVENTS):
        if not isinstance(_e, dict):
            continue
        if _e.get("type") == "user" and _is_real_user_prompt(_e):
            _recent.append(_prompt_text(_e))
            _seen_prompts += 1
            if _seen_prompts >= 3:
                break
        elif _e.get("type") == "assistant":
            _recent += [c.get("text", "") for c in _content_list(_e) if isinstance(c, dict) and c.get("type") == "text"]
    _URL_ID = re.compile(r"https?://|\b[A-Za-z0-9-]+\.(?:com|io|tw|app|net|org|me)\b|`/[^`\s]+`")
    _NAME_ID = re.compile(r"「[^」]{2,}」|『[^』]{2,}』|https?://|\b[A-Za-z0-9-]+\.(?:com|io|tw|app|net|org|me)\b")
    _vague_hits, _para, _paras, _in_code = [], [], [], False
    for _ln in LAST_LINES + [""]:
        if _ln.strip().startswith("```"):
            _in_code = not _in_code
            continue
        if _in_code or _ln.lstrip().startswith(">"):
            continue
        if _ln.strip():
            _para.append(_ln)
        elif _para:
            _paras.append("\n".join(_para))
            _para = []
    _whole = "\n".join(_recent)
    for _blk in _paras:
        _plain = strip_quotes(_blk)
        for _m in _VAGUE.finditer(_plain):
            _before = _plain[max(0, _m.start() - 2):_m.start()]
            if re.search(r"[做建開架蓋新加設寫弄同哪每任各十百千萬零〇二三四五六七八九兩幾0-9]$", _before) \
                    or _before in ("沒有", "各有") or re.fullmatch(r"[做建開架蓋新加設寫弄貼造]了", _before):
                continue
            _need = _URL_ID if _m.group(2) in ("短網址", "網址", "連結") else _NAME_ID
            _scope = _whole if _m.group(1) in ("那條", "那個", "這條", "這個") else _blk
            if not _need.search(_scope):
                _vague_hits.append(_m.group(0))
    if _vague_hits:
        MESSAGES.append(
            "\n🔴🔒 含糊指稱鎖（2026-10-21 教練：「你給了一句非常模糊的話，害我去搜尋是不是這兩條」）\n" + BAR + "\n"
            "回覆裡講到下面這些，卻沒寫出到底是哪一個，教練只能自己猜：\n" +
            "".join("  • %s\n" % h for h in _vague_hits[:5]) +
            "\n✅ 立刻改寫回覆：\n"
            "  • 網址／連結：寫出完整網址；含金鑰就寫網址開頭＋項目全名＋在哪一頁哪個分類\n"
            "  • 群組／機器人／網站：寫「全名」\n"
            "  • 教練要的是看一次就懂，不是自己去對是哪一條\n" + BAR + "\n")
        log_violation("rule_vague_reference_violations.log", "".join("  • %s\n" % h for h in _vague_hits[:5]))
        BLOCK = True
except Exception:
    pass

# ════════════════════════════════════════════════
# P. 「教練沒講過」鎖（擋）—— 2026-10-24 教練：「就因為你的一句我沒講過，我就得再叫小龍蝦去翻找對話紀錄」
#    軍師只用「LK888＋佩佩」窄關鍵字 grep 一次，沒找到就回「紀錄裡找不到這句」；其實 9/17 原話寫「產業鍊SOP」，
#    hook 也早就寫明孔大哥／佩佩老師能用。同類第二次以上（試金石案例 125 先查再答），照 N8 改機制：
#    最後回覆裡說「找不到／沒講過／從來沒有」教練說的話，這一輪卻沒跑 recall.py --said（同義詞＋已做進系統的證據）→ 擋下。
#    任何例外一律放行（hook 壞了不能擋教練）。
# ════════════════════════════════════════════════
try:
    _ABSENT = re.compile(
        r"(找不到|查不到|搜不到|沒找到|沒有找到|查無)[^。！？\n]{0,24}(你|您|教練)[^。！？\n]{0,10}(說|講|交代|提|吩咐|要求|指示)過"
        r"|(你|您|教練)[^。！？\n]{0,6}(從來|從未|根本)?(沒有|沒|不曾|未曾|從未)[^。！？\n]{0,6}(說|講|交代|提|吩咐|開)過"
        r"|(紀錄|記錄|對話|原話)[^。！？\n]{0,14}(找不到|查不到|搜不到|沒找到|沒有找到|查無)[^。！？\n]{0,6}(這句|這段|這件|這個指示|這個交代|這些話)")
    _absent_hits = []
    for _ln in LAST_LINES:
        if _ln.lstrip().startswith(">"):
            continue
        _m = _ABSENT.search(strip_quotes(_ln))
        if _m and not re.search(r"不准|禁止|不要說|不能說|鎖|案例|句型|我錯|錯在|承認|violations", _ln):
            _absent_hits.append(_m.group(0))
    if _absent_hits:
        _turn_start = 0
        for _i, _e in enumerate(EVENTS):
            if isinstance(_e, dict) and _e.get("type") == "user" and _is_real_user_prompt(_e) \
                    and not _prompt_text(_e).lstrip().startswith(("Stop hook feedback", "<system-reminder")):
                _turn_start = _i
        _ran = False
        for _e in EVENTS[_turn_start:]:
            if isinstance(_e, dict) and _e.get("type") == "assistant":
                for _x in _content_list(_e):
                    if isinstance(_x, dict) and _x.get("type") == "tool_use" and _x.get("name") == "Bash" \
                            and "recall.py" in str((_x.get("input") or {}).get("command", "")) \
                            and "--said" in str((_x.get("input") or {}).get("command", "")):
                        _ran = True
        if not _ran:
            MESSAGES.append(
                "\n🔴🔒 「教練沒講過」鎖（2026-10-24 教練：「就因為你的一句我沒講過，我就得再叫小龍蝦去翻找對話紀錄」）\n" + BAR + "\n"
                "回覆裡說教練沒講過／找不到教練的話：\n" + "".join("  • %s\n" % h for h in _absent_hits[:3]) +
                "這一輪卻沒跑過全面查證。\n\n"
                "✅ 立刻執行：\n"
                "  1. python3 ~/.openclaw/workspace/scripts/recall.py --said <人> <主題>（例：--said 佩佩 LK888；同義詞自動展開，也查設定檔／hook／分身說明檔）\n"
                "  2. 有找到 → 改寫回覆，引用原話時間或檔案行號，直接承認教練說過\n"
                "  3. 真的查無 → 只准寫「我用 X、Y 這些詞查了原話和系統設定，沒找到」，問教練大概哪天、哪個群說的；不准寫「您沒講過」\n" + BAR + "\n")
            log_violation("rule_coach_never_said_violations.log", "".join("  • %s\n" % h for h in _absent_hits[:3]))
            BLOCK = True
except Exception:
    pass

# ════════════════════════════════════════════════
# Q. 「網址要完整可點」鎖（擋）—— 2026-11-11 教練：「後面那兩個星星是你把它寫到超連結當中，我點進去是亂碼，還得手動移掉」
#    10/02 Telegram 通知網址緊貼括號（案例97）同一類第二次。照 N8 改機制：
#    最後回覆裡的網址被 ** 包住，或後面緊貼中文字／全形標點 → 擋下，改成網址單獨一行、前後不加任何符號。
#    任何例外一律放行。
# ════════════════════════════════════════════════
try:
    _URLCH = r"[A-Za-z0-9\-._~:/?#@!$&'+,;=%]"
    _BADURL = re.compile(
        r"\*\*\s*https?://" + _URLCH + r"+"            # ** 開頭包網址
        r"|https?://" + _URLCH + r"*\*+"               # 網址尾巴黏著 *
        r"|https?://" + _URLCH + r"+[　-〿＀-￯一-鿿]")  # 後面緊貼中文或全形標點
    _bad_hits = []
    _in_fence = False
    for _ln in LAST_LINES:
        if _ln.lstrip().startswith("```"):
            _in_fence = not _in_fence
            continue
        if _in_fence or _ln.lstrip().startswith(">"):
            continue
        _ln2 = re.sub(r"`[^`]*`", "", _ln)   # 反引號包住的是範例，不算
        if re.search(r"案例|錯誤示範|違規|violations", _ln2):
            continue
        _m = _BADURL.search(_ln2)
        if _m:
            _bad_hits.append(_m.group(0)[:80])
    if _bad_hits:
        MESSAGES.append(
            "\n🔴🔗 「網址要完整可點」鎖（2026-11-11 教練：網址後面的兩個星星被寫進連結，點進去是亂碼，還得手動刪）\n" + BAR + "\n"
            "回覆裡的網址格式會讓連結點不開：\n" + "".join("  • %s\n" % h for h in _bad_hits[:3]) +
            "✅ 改成：網址自己單獨一行，前後不加 ** 、括號、標點、中文字；要強調就強調網址上面那句話。\n" + BAR + "\n")
        log_violation("rule_url_clickable_violations.log", "".join("  • %s\n" % h for h in _bad_hits[:3]))
        BLOCK = True
except Exception:
    pass

# ────────────────────────────────────────────────
# 輸出：所有訊息一起送到 stderr，任一擋下級命中就 exit 2
# ────────────────────────────────────────────────
if MESSAGES:
    sys.stderr.write("\n".join(MESSAGES))

sys.exit(2 if BLOCK else 0)
