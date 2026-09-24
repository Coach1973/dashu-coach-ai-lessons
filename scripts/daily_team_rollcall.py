#!/usr/bin/env python3
"""每日全隊點名（2026-09-24 教練交辦，團隊協作體檢第1項）。

每天 08:10 由 launchd 觸發一次，把所有AI的綠燈/紅燈＋昨日使用人數彙成一則訊息，
走 notify_coach.sh（直連Telegram官方API，不經過小龍蝦主程式，小龍蝦掛了照樣送得出去）。

為什麼要「平安也報」：過去機制多半「出事才報」，「沒收到訊息」分不出是平安還是
連報警的都掛了（09-21小龍蝦停擺3天沒人知道）。每天固定一則，08:30前沒收到＝出事。

使用人數一律由程式直接數對話資料庫，不叫AI讀摘要猜（幕僚長晨報讀DREAMS.md，從沒報過人數）。

用法：
    daily_team_rollcall.py            # 檢查並送出
    daily_team_rollcall.py --dry-run  # 只印出，不送
"""
import json
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HOME = Path.home()
WS = HOME / ".openclaw" / "workspace"
OPENCLAW_JSON = HOME / ".openclaw" / "openclaw.json"
HERMES_ENV = HOME / ".hermes" / ".env"
HERMES_HEARTBEAT = HOME / ".hermes" / "state" / "gateway.heartbeat"
LINE_STATE = WS / "logs" / "line_bots_healthcheck_state.json"
VPS_STATE = WS / "logs" / "vps_healthcheck_state.json"
CRON_DB = HOME / ".openclaw" / "state" / "openclaw.sqlite"
STATE_OUT = WS / "logs" / "daily_rollcall_state.json"
NOTIFY = WS / "scripts" / "notify_coach.sh"

COACH_LINE_IDS = {"u895a0ad8e49d75f8303dc3d067282dc0", "u168903487f0ba2b666ddc62b854de351"}
TEST_ID_MARKERS = ("test", "diag", "health", "xxxx")
PENDING_ALARM = 3  # 機器人未讀訊息累積到這個數就代表沒人在收

TELEGRAM_BOTS = [("bot_main", "小龍蝦"), ("bot_kong", "孔大哥小幫手"), ("bot_peipei", "佩佩老師小幫手")]
LINE_AGENTS = [("bni_tainan", "大台南小幫手"), ("jiaolian_thoughts", "教練都在想什麼")]
PUBLIC_URLS = [
    ("LINE入口", "https://openclaw.bymyway.com/health"),
    ("活動報名站", "https://event.bymyway.com/"),
    ("名片系統", "https://namecard.bymyway.com/"),
]

today = datetime.now().strftime("%Y-%m-%d")
problems = []  # (燈號, 項目, 說明)
oks = []


def ok(name):
    oks.append(name)


def bad(name, why, level="🔴"):
    problems.append((level, name, why))


def launchd_running(label):
    out = subprocess.run(["/bin/launchctl", "print", f"gui/{subprocess.getoutput('id -u')}/{label}"],
                         capture_output=True, text=True).stdout
    m = re.search(r"^\s*state = (\S+)", out, re.M)
    return m.group(1) if m else "找不到"


def http_status(url, timeout=10):
    # Cloudflare 會對 Python 預設 User-Agent 回 403，帶一般瀏覽器標頭才測得到真實狀態
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 (team-rollcall)"})
    opener = urllib.request.build_opener(NoRedirect)
    try:
        return opener.open(req, timeout=timeout).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def tg_bot(token):
    base = f"https://api.telegram.org/bot{token}"
    json.load(urllib.request.urlopen(f"{base}/getMe", timeout=10))
    return json.load(urllib.request.urlopen(f"{base}/getWebhookInfo", timeout=10))["result"].get("pending_update_count", 0)


def check_xiaolongxia():
    state = launchd_running("ai.openclaw.gateway")
    code = http_status("http://127.0.0.1:18789/health", 5)
    if state == "running" and code == 200:
        ok("小龍蝦主程式")
    else:
        bad("小龍蝦主程式", f"狀態={state}，健康檢查回應={code}")


def check_telegram_bots():
    accounts = json.loads(OPENCLAW_JSON.read_text())["channels"]["telegram"]["accounts"]
    bots = [(label, accounts.get(key, {}).get("botToken")) for key, label in TELEGRAM_BOTS]
    m = re.search(r"^TELEGRAM_BOT_TOKEN=(.+)$", HERMES_ENV.read_text(), re.M) if HERMES_ENV.exists() else None
    bots.append(("赫米斯", m.group(1).strip().strip("'\"") if m else None))
    for label, token in bots:
        if not token:
            bad(label, "找不到機器人金鑰")
            continue
        try:
            pending = tg_bot(token)
        except Exception as e:
            bad(label, f"Telegram查不到這個機器人（{type(e).__name__}）")
            continue
        if pending >= PENDING_ALARM:
            bad(label, f"有{pending}則訊息沒被讀取，收訊可能卡住了")
        else:
            ok(label)


def check_hermes_process():
    state = launchd_running("ai.hermes.gateway")
    age = time.time() - HERMES_HEARTBEAT.stat().st_mtime if HERMES_HEARTBEAT.exists() else None
    if state == "running" and age is not None and age < 600:
        ok("赫米斯主程式")
    else:
        why = f"狀態={state}" + (f"，心跳已{int(age // 60)}分鐘沒更新" if age is not None else "，找不到心跳檔")
        bad("赫米斯主程式", why)


def check_state_file(path, name):
    """讀各自健檢寫下的結果；今天沒跑本身就是紅燈（VPS健檢曾整段缺天沒人發現）。"""
    if not path.exists():
        bad(name, "找不到健檢結果檔")
        return {}
    st = json.loads(path.read_text())
    last = st.get("lastCheckAt", "")
    if not last.startswith(today):
        bad(name, f"今天的健檢沒有跑（最後一次：{last or '無'}）")
    elif st.get("status") == "OK":
        ok(name)
    else:
        detail = "；".join(r for r in st.get("results", []) if not r.startswith("✅"))
        bad(name, f"{st.get('status')}：{detail}", "🟡" if st.get("status") == "WARN" else "🔴")
    return st


def check_public_urls():
    for label, url in PUBLIC_URLS:
        code = http_status(url)
        if 200 <= code < 400:
            ok(label)
        else:
            bad(label, f"對外網址打不開（{f'回應{code}' if code else '沒有回應'}）")


def check_cron_jobs():
    db = sqlite3.connect(f"file:{CRON_DB}?mode=ro", uri=True)
    failing = []
    for name, js in db.execute("select name, state_json from cron_jobs where enabled=1"):
        st = json.loads(js or "{}")
        if st.get("consecutiveErrors", 0) > 0 or st.get("lastDeliveryStatus") == "failed":
            failing.append(name)
    if failing:
        bad("小龍蝦排程任務", "最近執行失敗：" + "、".join(failing), "🟡")
    else:
        ok("小龍蝦排程任務")


def line_usage(agent):
    db = sqlite3.connect(f"file:{HOME}/.openclaw/agents/{agent}/agent/openclaw-agent.sqlite?mode=ro", uri=True)
    rows = db.execute(
        """select w.session_key, count(*), max(e.created_at) from transcript_events e
           join session_windows w on w.session_id = e.session_id
           where w.session_key like '%:line:%'
             and json_extract(e.event_json, '$.message.role') = 'user'
             and e.created_at > ?
           group by w.session_key""",
        (int((time.time() - 7 * 86400) * 1000),),
    ).fetchall()
    cut24 = (time.time() - 86400) * 1000
    users24, msgs24, users7 = set(), 0, set()
    for key, n, last in rows:
        peer = key.split(":")[-1].lower()
        if peer in COACH_LINE_IDS or any(t in peer for t in TEST_ID_MARKERS):
            continue
        users7.add(peer)
        if last > cut24:
            users24.add(peer)
            msgs24 += db.execute(
                """select count(*) from transcript_events e join session_windows w on w.session_id = e.session_id
                   where w.session_key = ? and json_extract(e.event_json, '$.message.role') = 'user' and e.created_at > ?""",
                (key, int(cut24)),
            ).fetchone()[0]
    return len(users24), msgs24, len(users7)


def main():
    dry = "--dry-run" in sys.argv
    for fn in (check_xiaolongxia, check_telegram_bots, check_hermes_process):
        try:
            fn()
        except Exception as e:
            bad(fn.__name__, f"檢查程式本身出錯：{e}")
    check_state_file(LINE_STATE, "LINE三個小幫手")
    vps = check_state_file(VPS_STATE, "VPS小龍蝦")
    try:
        check_public_urls()
        check_cron_jobs()
    except Exception as e:
        bad("網址/排程檢查", f"檢查程式本身出錯：{e}")

    usage = []
    for agent, label in LINE_AGENTS:
        try:
            u24, m24, u7 = line_usage(agent)
            usage.append(f"{label}：{u24}人（{m24}則）｜近7天{u7}人")
        except Exception as e:
            usage.append(f"{label}：讀不到資料（{type(e).__name__}）")
    if "users_24h" in vps:
        usage.append(f"VPS小龍蝦：{vps['users_24h']}人（{vps.get('msgs_24h', 0)}則）｜近7天{vps.get('users_7d', '?')}人")

    weekday = "一二三四五六日"[datetime.now().weekday()]
    head = "✅ 全員正常" if not problems else f"⚠️ {len(problems)}項需要注意"
    lines = [f"🩺 每日全隊點名 {datetime.now():%m/%d}（{weekday}）{datetime.now():%H:%M} 台灣時間", head, ""]
    for level, name, why in problems:
        lines.append(f"{level} {name}：{why}")
    if problems:
        lines.append("")
    lines.append("✅ " + "、".join(oks))
    lines += ["", "📊 昨日使用（排除教練本人與測試帳號）", *usage, "",
              "（每天08:10送出；08:30前沒收到這則＝系統出事，直接叫軍師）"]
    msg = "\n".join(lines)

    STATE_OUT.write_text(json.dumps({
        "lastRunAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "problems": [{"level": l, "name": n, "why": w} for l, n, w in problems],
        "oks": oks, "usage": usage,
    }, ensure_ascii=False, indent=1))

    if dry:
        print(msg)
        return
    subprocess.run([str(NOTIFY), msg], check=False)


if __name__ == "__main__":
    main()
