#!/usr/bin/env python3
"""試金石條件反射路由（2026-10-02）

教練：「只要發生這樣的情境，立刻參照檔案庫裡的哪幾個，讓它不重複犯錯，這個機制就值錢了。」
把 knowledges/反射索引.json 裡的每一筆「刺激→反射」接到 AI 的四個時刻：
  prompt    教練說話時      （UserPromptSubmit）
  pre_tool  AI 要動手前     （PreToolUse，可提醒、可擋）
  post_tool AI 看到結果時   （PostToolUse）
  reply     AI 要回話時     （Stop，只放零誤判的 block 規則）
用法：settings.json 各事件呼叫 `reflex_router.py <moment>`，stdin 是 hook 的 JSON。
命中紀錄寫 state/reflex_hits.log——用來看哪條反射有在動、哪條從沒觸發（觸發條件寫錯或已過時）。
任何錯誤一律安靜放行，不能因為反射系統壞掉而卡住工作。
"""
import datetime
import json
import os
import re
import sys
import time

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 本機與雲端工作頁都適用
INDEX = os.path.join(WS, "knowledges/反射索引.json")
HITS = os.environ.get("REFLEX_HITS_LOG") or os.path.join(WS, "state/reflex_hits.log")  # 測試時指到別處，別汙染真實統計
SEEN_DIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "reflex_seen")
MAX_PER_FIRE = 3
SELF = re.compile(r"反射索引|reflex_(router|backtest)|render_situation_directory")


def load_reflexes(moment):
    with open(INDEX, encoding="utf-8") as f:
        # 有寫 agents 的只給小龍蝦指定分身用（例如 BNI 官方條文），軍師這邊不比
        return [r for r in json.load(f)["reflexes"] if r.get("moment") == moment and not r.get("agents")]


def text_for(moment, evt):
    """各時刻要比對的文字。"""
    if moment == "prompt":
        return evt.get("prompt") or ""
    if moment == "reply":
        return last_assistant_text(evt)
    ti = evt.get("tool_input") or {}
    if moment == "post_tool":
        # 只看「改了哪個檔」＋「工具回傳了什麼」，不看指令內容：
        # 2026-10-02 首次實戰誤判——指令裡只是寫文件提到 429/MiniMax，就被當成真的收到 429。
        resp = response_text(evt.get("tool_response"))
        if len(resp) > 20000:
            resp = resp[:10000] + "\n" + resp[-10000:]  # 錯誤常在最後，頭尾都留
        return "\n".join([str(ti.get("file_path") or ti.get("path") or ""), resp])
    return "\n".join(str(ti.get(k) or "") for k in ("command", "file_path", "path", "url", "content", "new_string"))


def response_text(resp):
    """工具回傳的原文。Bash 回傳 {stdout, stderr…}：取原文保留換行（json.dumps 會壓成一行，逐行比對失效）；
    originalFile 是改檔前的整份內容、不是結果，不比對。"""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        parts = [v for k, v in resp.items() if isinstance(v, str) and k != "originalFile"]
        if parts:
            return "\n".join(parts)
    return json.dumps(resp, ensure_ascii=False)


def last_assistant_text(evt):
    path = evt.get("transcript_path") or ""
    if not os.path.exists(path):
        return ""
    texts = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[-400:]
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "user" and not d.get("isMeta"):
            c = d.get("message", {}).get("content")
            # 真正的使用者發言（不是工具結果）＝這一輪的起點
            if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)):
                break
        if d.get("type") == "assistant":
            for c in d.get("message", {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "text":
                    texts.append(c["text"])
    return "\n".join(reversed(texts))


def strip_code(s):
    """回覆裡的程式碼區塊與行內程式碼不比對（那是在展示，不是給教練點的網址）。"""
    s = re.sub(r"```.*?```", "", s, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", s)


def seen_before(session, rid):
    """remind 級同一場對話同一條只出現一次，避免變成背景噪音。"""
    os.makedirs(SEEN_DIR, exist_ok=True)
    mark = os.path.join(SEEN_DIR, f"{session}_{rid}")
    if os.path.exists(mark):
        return True
    open(mark, "w").close()
    return False


WEEKDAY = "一二三四五六日"
DATE_RE = re.compile(r"(?:(20\d\d)\s*[/年-]\s*)?(\d{1,2})\s*[/月]\s*(\d{1,2})\s*日?\s*[（(]\s*(?:週|星期|禮拜)?([一二三四五六日天])\s*[）)]")


def check_weekday(text):
    """「9/16（二）」這種日期，星期對不起來就回傳說明。沒寫年份時，今年或明年對得上就算對（跨年活動）。"""
    this_year = int(time.strftime("%Y"))
    bad = []
    for m in DATE_RE.finditer(text):
        y, mo, da, wd = m.groups()
        wd = "日" if wd == "天" else wd
        years = [int(y)] if y else [this_year, this_year + 1]
        try:
            right = [WEEKDAY[datetime.date(yy, int(mo), int(da)).weekday()] for yy in years]
        except ValueError:
            continue
        if wd not in right:
            bad.append(f"{m.group(0).strip()} 應該是星期{right[0]}")
    return "；".join(dict.fromkeys(bad))[:300]


def log_hit(moment, rid, level):
    try:
        with open(HITS, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{moment}\t{rid}\t{level}\n")
    except Exception:
        pass


def main():
    moment = sys.argv[1] if len(sys.argv) > 1 else ""
    evt = json.load(sys.stdin)
    if moment == "reply" and evt.get("stop_hook_active"):
        return  # 已經因為擋下在重答，不再擋第二次，避免無限循環
    tool = evt.get("tool_name") or ""
    session = evt.get("session_id") or "nosession"
    text = text_for(moment, evt) or ""  # 空字串也要比：有的反射只看工具名稱（例如操作 Chrome 前）
    if moment == "reply":
        text = strip_code(text)
    elif moment in ("pre_tool", "post_tool") and SELF.search(text):
        return  # 正在改反射系統本身：指令裡本來就寫滿各種刺激字，跳出來全是誤判

    reminds, blocks = [], []
    for r in load_reflexes(moment):
        try:
            if r.get("tool") and not re.fullmatch(r["tool"], tool):
                continue
            if not re.search(r["match"], text):
                continue
        except re.error:
            continue  # 一條寫壞只跳過那一條，不能讓同時刻的其他反射一起失效
        if r.get("check") == "weekday":
            detail = check_weekday(text)
            if not detail:
                continue
            r = {**r, "say": r["say"] + detail + "。請改好；拿不準就問教練。"}
        if r.get("level") == "block":
            blocks.append(r)
        elif r.get("check") or not seen_before(session, r["id"]):  # 核對類每次錯都要講，不只講一次
            reminds.append(r)
    hits = (blocks + reminds)[:MAX_PER_FIRE]
    if not hits:
        return
    for r in hits:
        log_hit(moment, r["id"], r.get("level", "remind"))

    body = "\n".join(f"• {r['say']}（出處：{r['source']}）" for r in hits)
    head = "⚡ 條件反射（試金石經驗，系統依當下情境自動調出）："
    msg = f"{head}\n{body}"

    if moment == "reply":
        if blocks:
            print(json.dumps({"decision": "block", "reason": msg + "\n請改好再回覆教練。"}, ensure_ascii=False))
        return
    event_name = {"prompt": "UserPromptSubmit", "pre_tool": "PreToolUse", "post_tool": "PostToolUse"}[moment]
    out = {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": msg}}
    if moment == "pre_tool" and blocks:
        out["hookSpecificOutput"]["permissionDecision"] = "deny"
        out["hookSpecificOutput"]["permissionDecisionReason"] = msg
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
