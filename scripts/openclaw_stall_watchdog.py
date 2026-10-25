#!/usr/bin/env python3
"""小龍蝦卡死看門員（2026-10-25 教練：「不能每次都等我發現問題你再來解決」）。

背景：Telegram 訊息處理超過 300 秒會被系統判定卡住並重試，但內建規則要「失敗 8 次且滿 24 小時」
才放棄——對話太長、整理對話（compaction）每次都逾時時，就會每 8 分鐘重試一次、整整一天，
期間該分身不回話、還一直燒 MiniMax 額度（10/24～10/25 巴哈 peipei 群組就是這樣卡了兩天）。

做法：跟著小龍蝦當天的日誌（tail，事件觸發不是定時檢查），同一則訊息第 2 次逾時時，
把那個聊天室的對話刪掉重開（原紀錄系統會自動封存成 .zst，不會遺失），並直接發 Telegram 通知教練。
"""
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/tmp/openclaw")
STATE = Path.home() / ".openclaw/workspace/state/openclaw_stall_watchdog.json"
ACTION_LOG = Path.home() / ".openclaw/workspace/state/openclaw_stall_watchdog.log"
CONFIG = Path.home() / ".openclaw/openclaw.json"
OPENCLAW = Path.home() / ".nvm/versions/node/v24.21.0/bin/openclaw"
COACH_CHAT_ID = "6124913915"
STALL_RE = re.compile(r"stalled for event (\d+) on lane ([^\s]+) after \d+ms; applying retry policy \(handler-timeout\)")
STALLS_BEFORE_RESET = 2


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with ACTION_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"counts": {}, "handled": []}


def save_state(st):
    st["handled"] = st["handled"][-200:]
    STATE.write_text(json.dumps(st, ensure_ascii=False))


def run_openclaw(*args, timeout=180):
    p = subprocess.run([str(OPENCLAW), *args], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def find_session(lane):
    """lane 長得像 telegram:-5115910257；找出所有分身裡對應這個聊天室、最近有動的那一段對話。"""
    chat = lane.split(":", 1)[-1]
    code, out = run_openclaw("sessions", "--all-agents", "--json", "--limit", "all")
    rows = json.JSONDecoder().raw_decode(out[out.index("{"):])[0].get("sessions", [])
    hits = [r for r in rows if r["key"].endswith(f":{chat}") and ":subagent:" not in r["key"]]
    hits.sort(key=lambda r: r.get("updatedAt") or 0, reverse=True)
    return hits[0] if hits else None


def notify(text):
    try:
        token = json.loads(CONFIG.read_text())["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps({"chat_id": COACH_CHAT_ID, "text": text}).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        log(f"通知教練失敗：{e}")


def handle(event_id, lane, st):
    key = f"{event_id}|{lane}"
    st["counts"][key] = st["counts"].get(key, 0) + 1
    n = st["counts"][key]
    log(f"偵測到卡住：訊息 {event_id}（{lane}）第 {n} 次逾時")
    if n < STALLS_BEFORE_RESET or key in st["handled"]:
        save_state(st)
        return
    st["handled"].append(key)
    save_state(st)
    try:
        s = find_session(lane)
        if not s:
            log(f"找不到 {lane} 對應的對話，只通知")
            notify(f"⚠️ 小龍蝦卡住：{lane} 同一則訊息已逾時 {n} 次，但我找不到對應對話，請叫軍師查。")
            return
        code, out = run_openclaw("sessions", "delete", s["key"], "--agent", s["agentId"], "--yes")
        ok = code == 0 and "Deleted session" in out
        log(f"{'已重開' if ok else '重開失敗'}：{s['key']}（{s.get('totalTokens')} tokens）\n{out[-400:]}")
        notify(
            f"🛠️ 小龍蝦自動解卡：分身「{s['agentId']}」在 {lane} 卡住（同一則訊息逾時 {n} 次，"
            f"對話約 {s.get('totalTokens') or '?'} tokens）。\n"
            + ("已把這段對話封存重開，它會接著回覆那則訊息。" if ok else "自動重開失敗，請叫軍師處理。")
        )
    except Exception as e:
        log(f"處理失敗：{e}")
        notify(f"⚠️ 小龍蝦卡住：{lane} 自動解卡時出錯（{e}），請叫軍師處理。")


def follow():
    st = load_state()
    cur, f = None, None
    while True:
        path = LOG_DIR / f"openclaw-{datetime.now():%Y-%m-%d}.log"
        if path != cur and path.exists():
            if f:
                f.close()
            f = path.open("r", encoding="utf-8", errors="replace")
            if cur is None:
                f.seek(0, 2)  # 啟動時只看之後新寫的，不重算舊的
            cur = path
        line = f.readline() if f else ""
        if not line:
            time.sleep(1)  # tail -f 等新行，不是定時掃描
            continue
        if "handler-timeout" in line and "spooled update" in line:  # 每次逾時會寫兩行，只算這一行
            m = STALL_RE.search(line)
            if m:
                handle(m.group(1), m.group(2), st)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--test-line":
        m = STALL_RE.search(sys.argv[2])
        print(m.groups() if m else None)
    else:
        follow()
