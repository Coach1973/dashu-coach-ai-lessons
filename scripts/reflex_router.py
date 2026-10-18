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
import tempfile
import time

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 本機與雲端工作頁都適用
INDEX = os.path.join(WS, "knowledges/反射索引.json")
HITS = os.environ.get("REFLEX_HITS_LOG") or os.path.join(WS, "state/reflex_hits.log")  # 測試時指到別處，別汙染真實統計
SEEN_DIR = os.path.join(tempfile.gettempdir(), "reflex_seen")  # Windows 沒有 /tmp
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
                # 2026-10-17：桌面版收尾框（wrap_up 的 recap／ask）也是講給教練聽的話，一起比對
                elif isinstance(c, dict) and c.get("type") == "tool_use" and str(c.get("name", "")).endswith("wrap_up"):
                    ti = c.get("input") or {}
                    texts.append("\n".join(str(ti.get(k) or "") for k in ("recap", "ask")))
    return "\n".join(reversed(texts))


def ran_in_turn(evt, needle):
    """這一輪（從教練最後一句話之後）AI 有沒有跑過含 needle 的 Bash 指令。"""
    path = evt.get("transcript_path") or ""
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[-400:]
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "user" and not d.get("isMeta"):
            c = d.get("message", {}).get("content")
            if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)):
                break
        if d.get("type") == "assistant":
            for c in d.get("message", {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_use" and needle in str((c.get("input") or {}).get("command") or ""):
                    return True
    return False


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


TM_PLIST = "/Library/Preferences/com.apple.TimeMachine.plist"
BACKUP_FRESH_HOURS = 6


def backup_needed(text):
    """升級指令前（2026-10-02 教練定的備份規則二：系統升級前一定備份）。
    Mac 上 6 小時內沒有 Time Machine 備份就回傳說明；指令自己先備份、遠端（ssh）、非 Mac 都不擋。"""
    if sys.platform != "darwin" or re.search(r"\bssh\b", text) or re.search(r"tmutil\s+startbackup\b[^\n]*(-b\b|--block)", text):
        return ""
    try:
        import plistlib
        with open(TM_PLIST, "rb") as f:
            dates = [d for dest in plistlib.load(f).get("Destinations", []) for d in dest.get("SnapshotDates", [])]
    except Exception:
        dates = []
    last = "讀不到"
    if dates:
        newest = max(dates)  # UTC
        hours = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - newest).total_seconds() / 3600
        if hours < BACKUP_FRESH_HOURS:
            return ""
        last = (newest + datetime.timedelta(hours=8)).strftime("%m/%d %H:%M")
    return (f"上一份備份是 {last}（台灣時間），已超過 {BACKUP_FRESH_HOURS} 小時。"
            "請把指令改成先備份再升級：tmutil startbackup --block && <原本的升級指令>（等備份跑完才會升級）。")


CORPUS_FILE = os.path.join(WS, "state/coach_corpus.jsonl")
VOCAB_SEEN = os.environ.get("COACH_VOCAB_SEEN") or os.path.join(WS, "state/coach_vocab_seen.json")
LAT_WORD = re.compile(r"(?<![A-Za-z0-9_\-./~])[A-Za-z]{4,15}(?![A-Za-z0-9_\-/])")


def _prompt_words(text):
    """教練本人打的話裡的英文詞（小寫）。貼上的內容、系統提示、程式碼、網址、路徑都不算。"""
    t = re.sub(r"<pasted_content.*?</pasted_content[^>]*>", "", text, flags=re.S)
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S)
    t = re.sub(r"```.*?```|`[^`\n]*`|https?://\S+|\S*[/\\]\S*", "", t, flags=re.S)
    if len(t) > 300:
        return set()  # 長篇多半是貼上的輸出，不抽查
    han = len(re.findall(r"[\u4e00-\u9fff]", t))
    lat = len(re.findall(r"[A-Za-z]", t))
    if han < lat:
        return set()  # 英文為主（貼終端機輸出、英文稿）不是語音輸入的中文句
    return {w.lower() for w in LAT_WORD.findall(t)}


def check_unfamiliar(text):
    """教練話裡出現他歷史上沒用過的英文詞（Typeless 常把中文聽成英文）：回傳說明，叫我先問、不要先查。
    詞庫＝教練原話庫（state/coach_corpus.jsonl，短句、非貼上）＋這支程式自己看過的詞（同一個詞只提醒一次）。
    任何一步壞掉都回空字串放行（寧可漏報，不能擋教練說話）。"""
    try:
        words = _prompt_words(text)
        if not words:
            return ""
        known = set()
        with open(CORPUS_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                if not o.get("pasted") and len(o.get("text", "")) <= 300:
                    known |= {w.lower() for w in LAT_WORD.findall(o.get("text", ""))}
        try:
            with open(VOCAB_SEEN, encoding="utf-8") as f:
                seen = set(json.load(f))
        except (OSError, ValueError):
            seen = set()
        new = sorted(w for w in words if w not in known and w not in seen)
        try:
            tmp = VOCAB_SEEN + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(sorted(seen | words), f, ensure_ascii=False)
            os.replace(tmp, VOCAB_SEEN)
        except OSError:
            pass
        if not new:
            return ""
        return ("這句話裡有教練歷史上沒用過的詞：" + "、".join(new[:3]) +
                "。先別查、先別動手：對照上下文，接不上或不像教練平常的用語，第一句就問"
                "「請問您說的是『…』嗎？是不是語音輸入錯誤？」，教練確認真有這個東西才去查。")
    except Exception:
        return ""


def _pending_path(session):
    return os.path.join(SEEN_DIR, f"{session}_pending_reply")


def save_pending_reply(session, body):
    """回話時的 remind 級反射：回話已經送出、沒辦法插話（Stop 只能擋），
    原本只記 log、AI 永遠看不到（2026-10-18 查到 5 條、15 次命中全都沒出聲）。
    改成留到教練下一句話時一起送上。"""
    try:
        os.makedirs(SEEN_DIR, exist_ok=True)
        with open(_pending_path(session), "a", encoding="utf-8") as f:
            f.write(body + "\n")
    except Exception:
        pass


def take_pending_reply(session):
    try:
        p = _pending_path(session)
        with open(p, encoding="utf-8") as f:
            s = f.read().strip()
        os.remove(p)
        return s
    except Exception:
        return ""


def log_hit(moment, rid, level):
    try:
        with open(HITS, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{moment}\t{rid}\t{level}\n")
    except Exception:
        pass


def main():
    moment = sys.argv[1] if len(sys.argv) > 1 else ""
    # Windows 預設用 cp950 讀 stdin，中文全變亂碼、反射一條都比不到（2026-10-02 模擬實測），一律照 UTF-8 讀
    evt = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    if moment == "reply" and evt.get("stop_hook_active"):
        return  # 已經因為擋下在重答，不再擋第二次，避免無限循環
    tool = evt.get("tool_name") or ""
    session = evt.get("session_id") or "nosession"
    text = text_for(moment, evt) or ""  # 空字串也要比：有的反射只看工具名稱（例如操作 Chrome 前）
    if moment == "reply":
        text = strip_code(text)
    elif moment in ("pre_tool", "post_tool") and SELF.search(text + "\n" + str((evt.get("tool_input") or {}).get("command") or "")):
        return  # 正在改反射系統本身：指令裡本來就寫滿各種刺激字，跳出來全是誤判（post_tool 的 text 不含指令，回測輸出的歷史範例會誤觸，所以另外看指令）

    reminds, blocks = [], []
    for r in load_reflexes(moment):
        try:
            if r.get("tool") and not re.fullmatch(r["tool"], tool):
                continue
            if not re.search(r["match"], text):
                continue
            if r.get("unless_fresh_file"):  # 教練明說要放行時 touch 通行證檔，10 分鐘有效
                try:
                    if time.time() - os.path.getmtime(os.path.join(WS, r["unless_fresh_file"])) < 600:
                        continue
                except OSError:
                    pass
        except re.error:
            continue  # 一條寫壞只跳過那一條，不能讓同時刻的其他反射一起失效
        if r.get("check") == "weekday":
            detail = check_weekday(text)
            if not detail:
                continue
            r = {**r, "say": r["say"] + detail + "。請改好；拿不準就問教練。"}
        elif r.get("check") == "deliver_opened":
            if ran_in_turn(evt, "deliver_open"):
                continue  # 這一輪已經用 deliver_open.sh 跳出來了，放行
        elif r.get("check") == "backup_recent":
            detail = backup_needed(text)
            if not detail:
                continue
            r = {**r, "say": r["say"] + detail}
        elif r.get("check") == "unfamiliar_terms":
            detail = check_unfamiliar(text)
            if not detail:
                continue
            r = {**r, "say": r["say"] + detail}
        if r.get("level") == "block":
            blocks.append(r)
        elif r.get("check") or r.get("repeat") or not seen_before(session, r["id"]):  # 核對類每次錯都要講；repeat＝每次命中都講（例如「先查再答」）
            reminds.append(r)
    reminds.sort(key=lambda x: not x.get("repeat"))  # 每次都要講的排前面，不被 3 條上限擠掉
    hits = (blocks + reminds)[:MAX_PER_FIRE]
    pending = take_pending_reply(session) if moment == "prompt" else ""
    if not hits and not pending:
        return
    for r in hits:
        log_hit(moment, r["id"], r.get("level", "remind"))

    body = "\n".join(f"• {r['say']}（出處：{r['source']}）" for r in hits)
    head = "⚡ 條件反射（試金石經驗，系統依當下情境自動調出）："
    msg = f"{head}\n{body}" if hits else ""
    if pending:
        msg = (msg + "\n" if msg else "") + "⚡ 上一輪回覆踩到（這一輪起照做）：\n" + pending

    if moment == "reply":
        if blocks:
            print(json.dumps({"decision": "block", "reason": msg + "\n請改好再回覆教練。"}))  # 純 ASCII：Windows cp950 印不出 ⚡ 會被安靜吞掉
        elif hits:
            save_pending_reply(session, body)
        return
    event_name = {"prompt": "UserPromptSubmit", "pre_tool": "PreToolUse", "post_tool": "PostToolUse"}[moment]
    out = {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": msg}}
    if moment == "pre_tool" and blocks:
        out["hookSpecificOutput"]["permissionDecision"] = "deny"
        out["hookSpecificOutput"]["permissionDecisionReason"] = msg
    print(json.dumps(out))  # 純 ASCII，理由同上


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
