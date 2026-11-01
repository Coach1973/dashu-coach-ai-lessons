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
from datetime import datetime, timedelta, timezone
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
TM_PLIST = Path("/Library/Preferences/com.apple.TimeMachine.plist")  # 終端機讀得到；排程(launchd)沒有完整磁碟取用會 PermissionError（2026-10-05 實測，tmutil 查詢也被擋）
BACKUP_MARK = WS / "logs" / "tm_last_started.json"  # 排程讀不到上面那份時，退而讀本腳本自己 startbackup 成功時留的時間（UTC）
BACKUP_STALE_DAYS = 3

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
    # 卡死看門員（2026-10-25）：同一則訊息逾時第 2 次就自動重開那段對話並通知教練；它停了就沒人解卡
    wd = launchd_running("com.coach.openclaw-stall-watchdog")
    if wd == "running":
        ok("小龍蝦卡死看門員")
    else:
        bad("小龍蝦卡死看門員", f"狀態={wd}，重啟：launchctl kickstart -k gui/$(id -u)/com.coach.openclaw-stall-watchdog")


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


def check_handoff_mirror():
    """接力棒鏡像（workspace/CLAUDE.md）超過一天沒更新＝同步被擋或壞掉。
    2026-10-14 發現：格式防呆把正常接力棒也擋掉，每 5 分鐘默默失敗、停在 10/01 兩週沒人發現。"""
    md = Path.home() / ".openclaw/workspace/CLAUDE.md"
    m = re.search(r"最後同步：(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", md.read_text(encoding="utf-8")[:2000]) if md.exists() else None
    if not m:
        bad("接力棒鏡像", "CLAUDE.md 找不到「最後同步」時間", "🟡")
        return
    age = datetime.now() - datetime.strptime(m.group(1), "%Y-%m-%d %H:%M")
    if age > timedelta(hours=26):
        bad("接力棒鏡像", f"CLAUDE.md 已 {age.days} 天沒同步（看 /tmp/sync_handoff.log）", "🟡")
    else:
        ok("接力棒鏡像")


def check_verbatim_vault():
    """逐字保險箱（教練每句話的永久存檔）。2026-10-30 體檢：對話存放位置 9/16 換了，收割程式一直印「新收 0 句」
    當成功，群組停收 6 週沒人發現。這裡每天驗：全部來源超過 6 小時沒新增、或有新的對話檔沒人收，就報。"""
    r = subprocess.run([sys.executable, str(WS / "scripts" / "recall.py"), "--check"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        ok("逐字保險箱")
    else:
        bad("逐字保險箱", (r.stdout.strip() or r.stderr.strip() or "檢查失敗")[:200] + "（叫軍師查 scripts/recall.py）")


def check_agent_boot_files():
    """分身開機檔每檔有字數上限（預設 2 萬，openclaw.json 各分身可設 bootstrapMaxChars），超過中間被截掉
    （2026-10-30 巴哈 MEMORY.md 9 天從 2 萬長到 2.9 萬）。2026-11-02：原本一律用 2 萬判斷，大台南小幫手上限是 4 萬卻被誤報。
    分身自己寫有 safety-locks 長期記憶上限鎖擋；系統自動搬進來的（Promoted From Short-Term Memory）擋不到，這裡每天量。"""
    cfg = json.loads(OPENCLAW_JSON.read_text())
    over = []
    entries = cfg["agents"]["entries"]   # 找不到就讓它報錯，不能掃 0 個分身還報正常
    default_limit = int(cfg["agents"].get("defaults", {}).get("bootstrapMaxChars") or 20000)
    for aid, a in entries.items():
        limit = int(a.get("bootstrapMaxChars") or default_limit)
        ws = Path(str(a.get("workspace") or "").replace("~", str(HOME), 1))
        for name in ("AGENTS.md", "SOUL.md", "MEMORY.md", "USER.md", "IDENTITY.md"):
            f = ws / name
            if f.is_file():
                n = len(f.read_text(encoding="utf-8", errors="ignore"))
                if n > limit:
                    over.append(f"{aid}/{name} {n:,}字（上限{limit:,}）")
    if not entries:
        bad("分身開機檔", "openclaw.json 讀不到分身清單", "🟡")
    elif over:
        bad("分身開機檔", "超過上限會被截掉：" + "、".join(over) + "（叫軍師把過期段落搬封存）", "🟡")
    else:
        ok("分身開機檔")


def check_line_push_gate():
    """LINE 推播閘門（教練 2026-10-20 常設禁令：沒有教練許可，LINE 小龍蝦不得使用會扣額度的推播）。
    閘門是補在 LINE 外掛檔案裡的；外掛更新換世代目錄會把它洗掉，沒人知道＝禁令默默失效。
    這裡每天檢查，被洗掉就自動補回（補回後要重啟主程式才生效，所以仍然報 🔴 讓人處理）。"""
    gate = Path.home() / ".openclaw/workspace/scripts/line_push_gate_patch.py"
    r = subprocess.run([sys.executable, str(gate), "--check"], capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        ok("LINE推播閘門")
        return
    subprocess.run([sys.executable, str(gate)], capture_output=True, text=True, timeout=30)
    bad("LINE推播閘門", "閘門被外掛更新洗掉，已自動補回；需要重啟主程式（launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway）才生效")


def check_cloud_rules_pack():
    """雲端對話規則包（教練 2026-10-20：雲端對話很笨、做完停在問同不同意）。
    ①每個雲端倉庫線上要有跟 Mac 來源同版的規則包，過期/不見就當場重新同步；
    ②雲端交件（claude/* 分支）超過 24 小時沒人接手 → 報 🟡（接手流程見 knowledges/雲端對話規則與接手流程.md）。"""
    script = Path.home() / ".openclaw/workspace/scripts/cloud/sync_rules_to_repos.py"
    r = subprocess.run([sys.executable, str(script), "status"], capture_output=True, text=True, timeout=120)
    bad_lines = [l for l in r.stdout.splitlines() if l.startswith(("❌", "⚠️"))]
    if bad_lines:
        subprocess.run([sys.executable, str(script), "--force"], capture_output=True, text=True, timeout=300)
        bad("雲端規則包", "已自動重新同步：" + "；".join(bad_lines), "🟡")
    else:
        ok("雲端規則包")
    old = []
    pend = WS / "state" / "cloud_branch_pending"
    for f in pend.glob("*.json") if pend.exists() else []:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            if d.get("status") == "pending" and (datetime.now() - datetime.fromisoformat(d["first_seen"])).total_seconds() > 86400:
                old.append(f'{d["repo"]}/{d["branch"]}')
        except Exception:
            continue
    if old:
        bad("雲端交件待接手", "超過 24 小時沒人接手：" + "、".join(old), "🟡")
    else:
        ok("雲端交件待接手")


def check_cron_jobs():
    db = sqlite3.connect(f"file:{CRON_DB}?mode=ro", uri=True)
    failing = []
    for name, js in db.execute("select name, state_json from cron_jobs where enabled=1"):
        st = json.loads(js or "{}")
        # 鎖死不能跑指令的分身(yang/yijing，extensions/safety-locks 的 SANDBOXED_AGENTS)，系統自帶的每週技能整理
        # 一定被擋，屬預期，不報。看分身名稱、不看錯誤字樣：安全鎖改版後訊息從 Exec blocked 變成 Ls failed，舊判斷失效（10/14）
        if name in ("skill-collection-review-yijing", "skill-collection-review-yang"):
            continue
        if st.get("consecutiveErrors", 0) > 0 or st.get("lastDeliveryStatus") == "failed":
            failing.append(name)
    if failing:
        bad("小龍蝦排程任務", "最近執行失敗：" + "、".join(failing), "🟡")
    else:
        ok("小龍蝦排程任務")


VERSION_SEEN = WS / "state" / "openclaw_version_seen.json"


def check_versions(vps_state, prev_state):
    """2026-09-24教練：系統升級了我卻今天才知道。Mac的版本變動由 version-change-notify hook 在
    主程式啟動當下通知；這裡補兩種hook抓不到的：程式檔已被換掉但主程式還沒重啟（下次重啟就變版），
    以及VPS版本跟前一天不同。"""
    parts, vps_version = [], vps_state.get("app_version") or ""
    try:
        seen = json.loads(VERSION_SEEN.read_text())
        on_disk = json.loads((Path(seen["root"]) / "package.json").read_text())["version"]
        parts.append(f"Mac小龍蝦 {seen['version']}")
        if on_disk != seen["version"]:
            bad("小龍蝦版本", f"程式檔已被換成 {on_disk}，但主程式還在跑 {seen['version']}，下次重啟就會變新版", "🟡")
    except Exception as e:
        parts.append("Mac小龍蝦 讀不到")
        bad("小龍蝦版本", f"讀不到版本紀錄（{type(e).__name__}）", "🟡")
    if vps_version:
        parts.append(f"VPS小龍蝦 {vps_version}")
        prev = prev_state.get("vps_version")
        if prev and prev != vps_version:
            bad("VPS小龍蝦版本", f"版本變了：{prev} → {vps_version}，如果不是教練安排的升級請叫軍師查", "🟡")
    return "🔖 版本：" + "｜".join(parts), vps_version


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


def last_backup():
    """回傳 (最後一次備份的台灣時間, 距今幾天)；讀 Time Machine 設定檔裡的備份日期（UTC）。"""
    import plistlib
    try:
        p = plistlib.loads(TM_PLIST.read_bytes())
        dates = [d for dest in p.get("Destinations", []) for d in dest.get("SnapshotDates", [])]
    except PermissionError:
        dates = [datetime.fromisoformat(json.loads(BACKUP_MARK.read_text())["startedAtUTC"])]
    if not dates:
        return None, None
    last = max(dates)
    age = (datetime.now(timezone.utc).replace(tzinfo=None) - last).total_seconds() / 86400
    return last + timedelta(hours=8), age


def backup_when_healthy(dry):
    """2026-10-02 教練交辦（取代每小時自動備份）：好的時候才備份。
    點名沒有紅燈 → 備份一次；有紅燈 → 不備份，保住上一份健康的。連續 3 天沒備到 → 點名提醒。"""
    try:
        last_tw, age = last_backup()
    except Exception as e:
        last_tw, age = None, None
        bad("Mac備份", f"讀不到備份紀錄（{type(e).__name__}）", "🟡")
    last_txt = f"{last_tw:%m/%d %H:%M}" if last_tw else "無"
    reds = [n for level, n, _ in problems if level == "🔴"]
    if reds:
        line = f"💾 備份：有紅燈，今天不備份（保住 {last_txt} 那份健康的）"
    elif dry:
        line = f"💾 備份：全員正常，會備份一次（測試模式不執行）｜上一份 {last_txt}"
    else:
        r = subprocess.run(["/usr/bin/tmutil", "startbackup"], capture_output=True, text=True)
        if r.returncode == 0:
            BACKUP_MARK.write_text(json.dumps({"startedAtUTC": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}))
            line = f"💾 備份：全員正常，已自動備份一次｜上一份 {last_txt}"
        else:
            line = f"💾 備份：啟動失敗｜上一份 {last_txt}"
            bad("自動備份", f"啟動失敗：{(r.stderr or r.stdout).strip()[:120]}", "🟡")
    if age is not None and age >= BACKUP_STALE_DAYS:
        bad("Mac備份", f"已經 {int(age)} 天沒有備份（上一份 {last_txt}）", "🟡")
    return line


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
        prev_state = json.loads(STATE_OUT.read_text())
    except Exception:
        prev_state = {}
    version_line, vps_version = check_versions(vps, prev_state)
    # 2026-10-02 起「下載」資料夾放外接SSD(~/Downloads 是捷徑)，SSD沒接上＝下載會失敗
    if Path("/Volumes/953-SSD/下載").is_dir():
        ok("外接SSD")
    else:
        bad("外接SSD", "953-SSD 沒有接上，「下載」資料夾打不開")
    try:
        check_public_urls()
        check_cron_jobs()
        check_handoff_mirror()
        check_verbatim_vault()
        check_agent_boot_files()
        check_line_push_gate()
        check_cloud_rules_pack()
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

    # 夥伴分身私有備份庫每日推一次（2026-10-02 體檢：原本只靠手動，曾積 15 天沒上雲）
    if dry:
        partner_line = "☁️ 夥伴分身備份：測試模式不執行"
    else:
        r = subprocess.run(["/bin/bash", str(WS / "scripts" / "backup_partner_agents.sh")],
                           capture_output=True, text=True, timeout=180)
        partner_line = f"☁️ 夥伴分身備份：{r.stdout.strip() or '無輸出'}"
        if r.returncode != 0:
            bad("夥伴分身備份", r.stdout.strip()[:120] or "執行失敗", "🟡")

    backup_line = backup_when_healthy(dry)

    # 賈維斯成績單（2026-10-30 教練拍板）：每週一算四個數字，變差就自動跑體檢（測試模式不啟動）
    scorecard = []
    if datetime.now().weekday() == 0 or "--scorecard" in sys.argv:
        r = subprocess.run([sys.executable, str(WS / "scripts" / "jarvis_scorecard.py")] + ([] if dry else ["--trigger"]),
                           capture_output=True, text=True, timeout=120)
        scorecard = ["", *(r.stdout.strip() or "📈 賈維斯成績單：沒有輸出，叫軍師查 scripts/jarvis_scorecard.py").splitlines()]

    weekday = "一二三四五六日"[datetime.now().weekday()]
    head = "✅ 全員正常" if not problems else f"⚠️ {len(problems)}項需要注意"
    lines = [f"🩺 每日全隊點名 {datetime.now():%m/%d}（{weekday}）{datetime.now():%H:%M} 台灣時間", head, ""]
    for level, name, why in problems:
        lines.append(f"{level} {name}：{why}")
    if problems:
        lines.append("")
    lines.append("✅ " + "、".join(oks))
    lines += ["", "📊 昨日使用（排除教練本人與測試帳號）", *usage, "", version_line, backup_line, partner_line, *scorecard, "",
              "（每天08:10送出；08:30前沒收到這則＝系統出事，直接叫軍師）"]
    msg = "\n".join(lines)

    STATE_OUT.write_text(json.dumps({
        "lastRunAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "problems": [{"level": l, "name": n, "why": w} for l, n, w in problems],
        "oks": oks, "usage": usage, "vps_version": vps_version,
    }, ensure_ascii=False, indent=1))

    if dry:
        print(msg)
        return
    subprocess.run([str(NOTIFY), msg], check=False)


if __name__ == "__main__":
    main()
