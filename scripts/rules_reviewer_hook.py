#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
守則審查員（Stop hook，2026-10-17 教練選定方案 B）

AI 每回完一輪話，叫 Haiku 拿「特助心法 21 條原文」對照這一輪：教練原話、AI 做的動作（保留錯誤字樣）、
AI 最後回覆，抓「有證據的明確違反」，記進帳本。觀察期（至 2026-10-20）只記錄、不擋教練。

鐵則（2026-10-16 十幾小時事故教訓，試金石＋記憶 feedback_hooks_must_fail_open_never_block_coach）：
  這支程式任何錯誤、逾時、沒網路、找不到檔 → 一律 exit 0 放行，絕不擋教練。
設計重點：
  - 21 條原文每次即時從 特助心法.md 讀，不另存副本（避免兩份不同步）
  - 子程序 claude -p 從空資料夾、--setting-sources local 啟動，不載入任何 CLAUDE.md／hook，不會遞迴
  - 非互動對話（entrypoint 是 sdk-*：小龍蝦／機器人的 claude -p 自動任務）跳過，不白花額度
  - 輸出：distill/rules_reviewer.log（給人看）＋ distill/rules_reviewer_ledger.jsonl（統計用）
"""
import sys, os, re, json, subprocess, tempfile, hashlib, time
from datetime import datetime

HOME = os.path.expanduser("~")
WORKSPACE = os.path.join(HOME, ".openclaw", "workspace")
RULES_FILE = os.path.join(WORKSPACE, "特助心法.md")
LOG = os.path.join(WORKSPACE, "distill", "rules_reviewer.log")
LEDGER = os.path.join(WORKSPACE, "distill", "rules_reviewer_ledger.jsonl")
CHILD_CWD = os.path.join(tempfile.gettempdir(), "rules_reviewer_cwd")
MIN_REPLY_CHARS = 60
TIMEOUT_SEC = 40
MAX_INPUT_CHARS = 16000
ERR = re.compile(r"error|not found|no matches|no such|錯誤|失敗|denied|blocked|exit code [1-9]|Traceback|command not found", re.I)

SYSTEM_PROMPT = """你是「特助守則審查員」。下面會給你：①特助心法 21 條守則原文 ②教練（大樹教練）這一輪說的話 ③AI 這一輪做的動作與結果（錯誤字樣已完整保留）④AI 最後回給教練的話。
你的工作：只抓「有證據的明確違反」，並指出是第幾條、出問題的那一句原文、為什麼違反。

判斷重點（這幾條最常犯、程式用關鍵字抓不到）：
- #03 回答前沒先驗證：下了結論，但這一輪的動作裡沒有對應的查證；或動作結果明明是錯誤／找不到（例如指令報 no matches found、not found），回覆卻說成「沒有／沒裝／查不到」；或把「未來會發生什麼」的預測講成確定的事。
- #15 該說「不知道／沒查」卻硬給答案。
- #18 教練的話裡出現陌生詞、語音可能聽錯的詞，AI 沒先問就直接去查或照字面做。
- #12 叫教練自己複製貼上／手動操作，但那件事 AI 其實能做。
- #10 對教練用了他聽不懂的專業術語、沒解釋（教練熟悉這些詞，不算違反：小龍蝦、軍師、賈維斯、接力棒、試金石、反射、守則、特助、commit、hook、Discord、LINE、Telegram、OpenClaw、Mac、VPS、MiniMax、Opus、Sonnet、Haiku、REA、Plaud、GitHub、Netlify、Cloudflare、NotebookLM）。

不算違反（不要抓）：
- 回覆裡明確標了「推論」「沒查到」「不確定」「我不知道」的句子。
- 閒聊、道謝、純轉述教練原話。
- 只是風格偏好、可以講得更好，但沒有違反任何一條。
- 你沒有證據的事——證據看不到就不要猜；拿不準就不要抓。

只輸出一個 JSON 物件，不要任何其他文字，格式：
{"violations":[{"rule":3,"quote":"AI 回覆裡出問題的那一句原文（照抄，30 字內）","reason":"一句白話繁體中文，說明違反哪條、證據是什麼"}]}
沒有明確違反就輸出 {"violations":[]}。最多列 3 筆，最確定的排前面。"""


def ok_exit():
    sys.exit(0)


def read_rules():
    with open(RULES_FILE, encoding="utf-8") as f:
        lines = f.read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("**01."))
    i21 = next(i for i, l in enumerate(lines) if l.startswith("**21."))
    end = next((i for i in range(i21, len(lines)) if lines[i].strip() == "---"), len(lines))
    return "\n".join(lines[start:end]).strip()


def strip_tags(s):
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S)
    s = re.sub(r"<(?:ide_[a-z_]+|local-command-[a-z]+|command-[a-z]+)>.*?</(?:ide_[a-z_]+|local-command-[a-z]+|command-[a-z]+)>", "", s, flags=re.S)
    return s.strip()


def user_text(evt):
    """真人打的話（排除工具回音）；沒有文字回傳 None"""
    content = (evt.get("message") or {}).get("content")
    if isinstance(content, str):
        return strip_tags(content) or None
    if isinstance(content, list):
        texts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
        if texts:
            return strip_tags("\n".join(texts)) or None
    return None


def result_text(c):
    x = c.get("content")
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return "\n".join(i.get("text", "") for i in x if isinstance(i, dict))
    return ""


def clip(s, n):
    s = s.strip()
    return s if len(s) <= n else s[:n] + "…"


def build_turn(events):
    """回傳 (教練原話, 動作紀錄文字, 最後 assistant 文字, entrypoint)"""
    entry = ""
    for e in events:
        if isinstance(e, dict) and e.get("entrypoint"):
            entry = e["entrypoint"]
            break
    last_idx = None
    for i in range(len(events) - 1, -1, -1):
        e = events[i]
        if isinstance(e, dict) and e.get("type") == "user" and user_text(e):
            last_idx = i
            break
    if last_idx is None:
        return "", "", "", entry
    coach = user_text(events[last_idx]) or ""
    actions, final_text = [], ""
    for e in events[last_idx + 1:]:
        if not isinstance(e, dict):
            continue
        t = e.get("type")
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        if t == "assistant":
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    final_text = c.get("text", "")
                elif c.get("type") == "tool_use":
                    inp = json.dumps(c.get("input") or {}, ensure_ascii=False)
                    actions.append("【動作】%s %s" % (c.get("name", ""), clip(inp, 300)))
        elif t == "user":
            for c in content:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    txt = result_text(c)
                    errs = [l for l in txt.split("\n") if ERR.search(l)]
                    if errs:
                        actions.append("【結果·含錯誤字樣】" + "\n".join(clip(l, 400) for l in errs[:8]))
                    elif txt.strip():
                        actions.append("【結果】" + clip(txt, 300))
    return coach, "\n".join(actions), final_text, entry


def log_line(text):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass


def main():
    if os.environ.get("RULES_REVIEWER_CHILD") == "1":
        ok_exit()
    if len(sys.argv) >= 3 and sys.argv[1] == "--worker":  # 背景工人：資料從暫存檔讀
        with open(sys.argv[2], encoding="utf-8") as f:
            raw = f.read()
        try:
            os.remove(sys.argv[2])
        except Exception:
            pass
    else:
        raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    if data.get("stop_hook_active") in (True, "true"):
        ok_exit()
    tp = data.get("transcript_path") or ""
    sid = (data.get("session_id") or "unknown")
    if not tp or not os.path.isfile(tp):
        ok_exit()
    if not (len(sys.argv) >= 3 and sys.argv[1] == "--worker") and os.environ.get("RULES_REVIEWER_SYNC") != "1":
        # 觀察期：丟到背景跑（約 15 秒），教練不用等；hook 本身立刻放行
        fd, tmp = tempfile.mkstemp(prefix="rules_reviewer_", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(raw)
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "--worker", tmp],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True, close_fds=True)
        ok_exit()
    events = []
    with open(tp, encoding="utf-8") as f:
        for l in f:
            if l.strip():
                try:
                    events.append(json.loads(l))
                except Exception:
                    pass
    coach, actions, last_in_file, entry = build_turn(events)
    if entry.startswith("sdk"):
        ok_exit()  # 小龍蝦／機器人的自動任務，不審
    reply = (data.get("last_assistant_message") or last_in_file or "").strip()
    if len(reply) < MIN_REPLY_CHARS:
        ok_exit()
    key = hashlib.md5((sid + reply).encode("utf-8")).hexdigest()[:12]

    body = "【教練這一輪說的話】\n%s\n\n【AI 這一輪做的動作與結果】\n%s\n\n【AI 最後回給教練的話】\n%s" % (
        clip(coach, 2500), actions or "（沒有動作）", clip(reply, 5000))
    if len(body) > MAX_INPUT_CHARS:  # 動作紀錄最長，優先砍中段
        keep = MAX_INPUT_CHARS // 2
        body = body[:keep] + "\n…（中段省略）…\n" + body[-keep:]
    prompt = "【守則 21 條原文】\n%s\n\n%s" % (read_rules(), body)

    os.makedirs(CHILD_CWD, exist_ok=True)
    env = dict(os.environ, RULES_REVIEWER_CHILD="1")
    t0 = time.time()
    proc = subprocess.run(
        ["claude", "-p", "--model", "haiku", "--setting-sources", "local", "--strict-mcp-config",
         "--tools", "", "--system-prompt", SYSTEM_PROMPT],
        input=prompt, capture_output=True, text=True, timeout=TIMEOUT_SEC, cwd=CHILD_CWD, env=env)
    out = (proc.stdout or "").strip()
    secs = round(time.time() - t0, 1)
    m = re.search(r"\{.*\}", out, flags=re.S)
    violations = []
    parse_ok = False
    if m:
        try:
            violations = json.loads(m.group(0)).get("violations", []) or []
            parse_ok = True
        except Exception:
            pass
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not parse_ok:
        log_line("[%s] session=%s key=%s 審查員回傳讀不懂（%.1f 秒）：%s\n---\n" % (now, sid[:8], key, secs, clip(out or proc.stderr or "", 200)))
        ok_exit()
    log_line("[%s] session=%s key=%s %.1f秒 抓到 %d 筆\n" % (now, sid[:8], key, secs, len(violations)) +
             "".join("  #%s｜%s｜%s\n" % (v.get("rule"), clip(str(v.get("quote", "")), 60), clip(str(v.get("reason", "")), 120)) for v in violations) + "---\n")
    with open(LEDGER, "a", encoding="utf-8") as f:
        if not violations:
            f.write(json.dumps({"t": now, "session": sid[:8], "key": key, "secs": secs, "rule": None}, ensure_ascii=False) + "\n")
        for v in violations:
            f.write(json.dumps({"t": now, "session": sid[:8], "key": key, "secs": secs, "rule": v.get("rule"),
                                "quote": v.get("quote"), "reason": v.get("reason")}, ensure_ascii=False) + "\n")
    ok_exit()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as e:  # 壞了就放行，絕不擋教練
        try:
            log_line("[%s] 審查員自己出錯（已放行）：%s: %s\n---\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type(e).__name__, clip(str(e), 200)))
        except Exception:
            pass
        sys.exit(0)
