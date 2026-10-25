#!/usr/bin/env python3
"""小龍蝦卡死看門員（2026-10-25 教練：「不能每次都等我發現問題你再來解決」）。

背景：Telegram 訊息處理超過 300 秒會被系統判定卡住並重試，但內建規則要「失敗 8 次且滿 24 小時」
才放棄——對話太長、整理對話（compaction）每次都逾時時，就會每 8 分鐘重試一次、整整一天，
期間該分身不回話、還一直燒 MiniMax 額度（10/24～10/25 巴哈 peipei 群組就是這樣卡了兩天）。

做法：跟著小龍蝦當天的日誌（tail，事件觸發不是定時檢查）。「逾時」＝真人訊息排隊 5 分鐘還沒被接手：
- 第 1 次逾時：中斷該聊天室正在跑的背景工作（子任務回報、分身互傳訊息等），讓真人訊息先處理（10/25 晚巴哈案）。
- 第 2 次逾時：把那個聊天室的對話刪掉重開（原紀錄系統會自動封存成 .zst，不會遺失）。
兩種處理都直接發 Telegram 通知教練，並附上它原本在忙什麼。
- 對話塞爆、整理也救不回來（日誌「Auto-compaction failed … Preserving existing session mapping for <對話>」）：
  直接把那段對話封存重開，通知教練可以再說一次（10/25 19:24 頂級特助案；送出的英文錯誤通知由
  外掛 url-typo-guard 換成中文「【軍師轉達】…看門員會自動幫它換新對話」，這裡負責讓那句話成真）。
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
TOOL_RE = re.compile(r"偵測工具呼叫: (\w+) agent: (\w+)")
OVERFLOW_RE = re.compile(r"Auto-compaction failed \(.*?Preserving existing session mapping for (agent:([a-z_]+):[^\s\"]+?)\.?\"")
CLAIM_RE = re.compile(r"terminal session persistence failed session=(agent:([a-z_]+):telegram:(?:group|direct):[^\s]+) run=\S+ error=SessionTranscriptWriterClaimReboundError")
CLAIM_FAILS_BEFORE_RESET = 2  # 同一段對話 10 分鐘內寫入失敗 2 次（等於教練連傳兩則都沒回）就換新對話
claim_fails = {}
OVERFLOW_COOLDOWN = 300  # 同一段對話 5 分鐘內只處理一次（一次塞爆常連寫好幾行）
overflow_done = {}
INBOUND_RE = re.compile(r"Inbound message telegram:[a-z]+:(-?\d+) -> @(\w+)")
last_bot_for_chat = {}  # 聊天室 → 最近收到訊息的機器人帳號名稱
_bot_accounts = {}
recent_tools = []  # (時間, 分身, 工具)，只留最近 15 分鐘，用來告訴教練它剛才在忙什麼


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


def bot_accounts(cfg):
    """機器人名稱（@xxx）→ 設定檔裡的帳號代號（bot_peipei 等），向 Telegram 問一次就記住。"""
    if not _bot_accounts:
        for acc, v in cfg["channels"]["telegram"]["accounts"].items():
            try:
                r = json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{v['botToken']}/getMe", timeout=20).read())
                _bot_accounts[r["result"]["username"].lower()] = acc
            except Exception as e:
                log(f"查機器人名稱失敗 {acc}：{e}")
    return _bot_accounts


def agent_for(cfg, chat, account):
    """照設定檔的分派規則：先找「這個帳號＋這個群組」的專屬規則，沒有才用「這個帳號」的預設分身。"""
    fallback = None
    for b in cfg.get("bindings", []):
        m = b.get("match", {})
        if m.get("channel") != "telegram" or m.get("accountId") != account:
            continue
        peer = m.get("peer")
        if peer and str(peer.get("id")) == chat:
            return b["agentId"]
        if not peer and fallback is None:
            fallback = b["agentId"]
    return fallback


def find_session(lane):
    """lane 長得像 telegram:-5115910257；用「哪個機器人收到訊息 → 分派給哪個分身」找出確定的那段對話，
    找不到就回 None（寧可只通知，也不要動錯分身——10/25 測試時差點選到頂級特助 main）。"""
    chat = lane.split(":", 1)[-1]
    cfg = json.loads(CONFIG.read_text())
    bot = last_bot_for_chat.get(chat)
    account = bot_accounts(cfg).get(bot.lower()) if bot else None
    agent = agent_for(cfg, chat, account) if account else None
    if not agent:
        log(f"判斷不出 {lane} 屬於哪個分身（機器人 {bot}、帳號 {account}）")
        return None
    code, out = run_openclaw("sessions", "--agent", agent, "--json", "--limit", "all")
    rows = json.JSONDecoder().raw_decode(out[out.index("{"):])[0].get("sessions", [])
    for r in rows:
        if r["key"] in (f"agent:{agent}:telegram:group:{chat}", f"agent:{agent}:telegram:direct:{chat}"):
            r.setdefault("agentId", agent)
            return r
    return None


def activity(agent):
    cut = time.time() - 900
    recent_tools[:] = [t for t in recent_tools if t[0] >= cut]
    counts = {}
    for _, a, tool in recent_tools:
        if a == agent:
            counts[tool] = counts.get(tool, 0) + 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:5]
    return "、".join(f"{k}×{v}" for k, v in top) or "（沒有工具紀錄）"


def run_kind(run_id):
    if not run_id:
        return "沒有正在跑的工作"
    if "skill-workshop" in run_id:
        return "自動技能整理"
    if run_id.startswith("announce:") or ":subagent:" in run_id:
        return "子任務回報（它自己派出去的小幫手回來交件）"
    return "一般工作"


def abort_session(s):
    code, out = run_openclaw("gateway", "call", "sessions.abort", "--json", "--params",
                             json.dumps({"key": s["key"], "agentId": s["agentId"]}))
    try:
        res = json.JSONDecoder().raw_decode(out[out.index("{"):])[0]
    except Exception:
        res = {}
    return res.get("abortedRunId"), out[-300:]


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
    if key in st["handled"]:
        save_state(st)
        return
    if n < STALLS_BEFORE_RESET:
        save_state(st)
        try:
            s = find_session(lane)
            if not s:
                return
            run_id, out = abort_session(s)
            log(f"中斷背景工作：{s['key']} → {run_id or '沒有可中斷的'}\n{out}")
            if run_id:
                notify(
                    f"🛠️ 小龍蝦自動解卡：分身「{s['agentId']}」在 {lane} 有真人訊息排隊 5 分鐘沒被接手。\n"
                    f"它原本在忙：{run_kind(run_id)}；最近 15 分鐘用的工具：{activity(s['agentId'])}。\n"
                    "已中斷那件背景工作，讓它先回這則訊息。"
                )
        except Exception as e:
            log(f"中斷失敗：{e}")
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
            f"對話約 {s.get('totalTokens') or '?'} tokens；最近 15 分鐘用的工具：{activity(s['agentId'])}）。\n"
            + ("已把這段對話封存重開，它會接著回覆那則訊息。" if ok else "自動重開失敗，請叫軍師處理。")
        )
    except Exception as e:
        log(f"處理失敗：{e}")
        notify(f"⚠️ 小龍蝦卡住：{lane} 自動解卡時出錯（{e}），請叫軍師處理。")


def handle_overflow(key, agent, dry_run=False, reason="對話太長、整理不動了"):
    now = time.time()
    if now - overflow_done.get(key, 0) < OVERFLOW_COOLDOWN:
        return
    overflow_done[key] = now
    log(f"偵測到對話壞掉（{reason}）：{key}")
    if dry_run:
        print(f"[試跑] 會執行：openclaw sessions delete {key} --agent {agent} --yes")
        return
    try:
        code, out = run_openclaw("sessions", "delete", key, "--agent", agent, "--yes")
        ok = code == 0 and "Deleted session" in out
        log(f"{'已重開' if ok else '重開失敗'}：{key}\n{out[-400:]}")
        where = "跟您的私訊" if key == f"agent:{agent}:main" else key.split(":", 2)[-1]
        notify(
            f"【軍師轉達】分身「{agent}」在{where}的對話{reason}，"
            + ("看門員已自動換成新對話（舊紀錄有封存），現在可以把剛剛那句話再說一次。" if ok else "看門員自動換新對話失敗，請叫軍師處理。")
        )
    except Exception as e:
        log(f"重開塞爆對話失敗：{e}")
        notify(f"【軍師轉達】分身「{agent}」對話塞爆，自動換新對話時出錯（{e}），請叫軍師處理。")


def handle_claim(key, agent, dry_run=False):
    now = time.time()
    fails = [t for t in claim_fails.get(key, []) if now - t < 600] + [now]
    claim_fails[key] = fails
    if len(fails) >= CLAIM_FAILS_BEFORE_RESET:
        claim_fails[key] = []
        handle_overflow(key, agent, dry_run, reason="寫入紀錄一直失敗、傳訊息都沒回")


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
        i = INBOUND_RE.search(line)
        if i:
            last_bot_for_chat[i.group(1)] = i.group(2)
            continue
        o = OVERFLOW_RE.search(line)
        if o:
            handle_overflow(o.group(1), o.group(2))
            continue
        c = CLAIM_RE.search(line)
        if c:
            handle_claim(c.group(1), c.group(2))
            continue
        t = TOOL_RE.search(line)
        if t:
            recent_tools.append((time.time(), t.group(2), t.group(1)))
            continue
        if "handler-timeout" in line and "spooled update" in line:  # 每次逾時會寫兩行，只算這一行
            m = STALL_RE.search(line)
            if m:
                handle(m.group(1), m.group(2), st)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--test-overflow":
        ACTION_LOG = Path("/dev/null")
        o = OVERFLOW_RE.search(sys.argv[2])
        print(o.groups() if o else None)
        if o:
            handle_overflow(o.group(1), o.group(2), dry_run=True)
    elif len(sys.argv) > 2 and sys.argv[1] == "--test-claim":
        ACTION_LOG = Path("/dev/null")
        c = CLAIM_RE.search(sys.argv[2])
        print(c.groups() if c else None)
        if c:
            handle_claim(c.group(1), c.group(2), dry_run=True)
            handle_claim(c.group(1), c.group(2), dry_run=True)
    elif len(sys.argv) > 2 and sys.argv[1] == "--test-line":
        m = STALL_RE.search(sys.argv[2])
        print(m.groups() if m else None)
    else:
        follow()
