#!/usr/bin/env python3
"""教練行程總表（2026-10-12 建立）

一份檔案，三個地方共用：
  - 巴哈助理（Telegram，peipei）：教練丟行程 → add 寫進來
  - LINE 小龍蝦在「榮樹下談公益」群組（rongshuxia）：對方丟時間 → 外掛先用 check 判斷行不行
  - 大台南培訓行事曆：sync-tainan 只抓 ZOOM 線上場次（實體在北科大／安平路的不是教練的行程，教練 10/12 親定）

資料檔：workspace/knowledges/教練行程總表.json（唯一真相源）

用法：
  coach_schedule.py add --date 2026-10-17 [--start 19:00 --end 21:00 | --allday] --title 台北演講 [--where 台北] [--source 巴哈] [--kind interview] [--tentative]
  coach_schedule.py add-weekly --weekday 5 --start 21:00 --end 22:00 --title LRC週報會議 [--since 2026-09-26]
  coach_schedule.py remove --id <id>
  coach_schedule.py check --date 2026-10-20 [--start 19:30 --minutes 60]
  coach_schedule.py list [--days 60]
  coach_schedule.py sync-tainan
  coach_schedule.py rongshuxia [--days 60]            # 未來的榮樹下訪談（含 id 與訪談對象）
  coach_schedule.py set-guest --id <id> --guest 王小明 [--field 綠能] [--by 邱裕榮]   # 登記對象＋通知巴哈＋排開始前 1 小時提醒
  coach_schedule.py remind --id <id>                   # 提醒排程到點時呼叫，同時送 LINE 榮樹下群組＋巴哈群組
  coach_schedule.py sync-reminders                     # 幫所有「已確定」的未來榮樹下訪談補排前 1 小時提醒（漏的才補）
  coach_schedule.py open-slots [--count 5 | --days 7]  # 最近 N 個可訪談時段／最近 N 天逐天可約時段（跟預約頁同一套算法；LINE 群有人問「最近五場／一週／半個月」用）
  coach_schedule.py daily-report [--date YYYY-MM-DD] [--send]   # 每日行程報告（今天行程＋可約空檔＋預約頁），--send 貼到巴哈群組

2026-10-13 教練：榮樹下的時間由邱裕榮先定、對象之後才定。邱裕榮在 LINE 群組講「哪一場訪問誰」
→ 群組小龍蝦（schedule-context 外掛）呼叫 set-guest → 巴哈助理群組收到「教練，幾月幾號榕樹下要跟某某訪談」，
並排一個開始前 1 小時的提醒（openclaw cron 一次性工作，id 記在事件的 reminder_job；改對象就換新、刪行程就一起刪）。
2026-10-13 教練再要求：不管有沒有填對象，只要榮樹下訪談「確定」了（add／confirm／set-guest），就排前 1 小時提醒，
到點同時發 LINE 榮樹下群組和巴哈群組：「一個小時之後即將有 Podcast 訪談，請提早做好準備，上線做準備」。待確認的不排。
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
import urllib.request
import uuid
from html import unescape

DATA = os.environ.get("COACH_SCHEDULE_DATA") or os.path.expanduser("~/.openclaw/workspace/knowledges/教練行程總表.json")  # 測試可指到複本
TAINAN_URL = "https://tainan-calender.netlify.app/"
WEEK = "一二三四五六日"
TZ = dt.timezone(dt.timedelta(hours=8))
SESSION = 60  # 一場訪談 1 小時
BUFFER = 30   # 兩場訪談之間的緩衝（教練 2026-10-19）；跟預約頁 coach_schedule_view.py 同一套，兩邊要一起改


def today():
    return dt.datetime.now(TZ).date()


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(d):
    d["updated_at"] = dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    # 2026-11-01 巴哈直接讀原始檔，把 weekday=0（週一）當成週日，提醒佩佩老師把週一的會寫成今晚：每筆都寫上中文星期，讀檔的人不用自己換算
    for r in d.get("recurring", []):
        if isinstance(r.get("weekday"), int):
            r["星期"] = "每週" + WEEK[r["weekday"]]
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(DATA), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, DATA)


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def fmt(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def day_label(d):
    return f"{d.month}/{d.day}（{WEEK[d.weekday()]}）"


def blocks_on(d, data):
    """回傳那一天所有忙碌時段：[(start_min, end_min, event)]，整天＝(0,1440)"""
    out = []
    iso = d.isoformat()
    for e in data["events"]:
        if e.get("covered_by_google"):
            continue
        if e["date"] <= iso <= e.get("end_date", e["date"]):
            if e.get("allday"):
                out.append((0, 1440, e))
            else:
                out.append((hm(e["start"]), hm(e["end"]), e))
    for r in data.get("recurring", []):
        if d.weekday() != r["weekday"]:
            continue
        if r.get("since") and iso < r["since"]:
            continue
        if r.get("until") and iso > r["until"]:
            continue
        if iso in r.get("skip", []) or iso in r.get("gskip", []):
            continue
        out.append((hm(r["start"]), hm(r["end"]), r))
    return sorted(out, key=lambda x: x[0])


def describe(b, private=False):
    s, e, ev = b
    when = "整天" if (s, e) == (0, 1440) else f"{fmt(s)}-{fmt(e)}"
    if private:
        # 教練 2026-10-13：行程已公開，外人也看得到行程名稱（不給地點、備註）；預約頁的預約只顯示類型，不秀預約者
        if ev.get("guest"):
            what = f"榮樹下訪談：{guest_text(ev)}"
        elif ev.get("source") == "預約頁":
            what = ev.get("booking_type") or "榮樹下訪談"
        else:
            what = ev["title"].replace("（待確認）", "").replace("（已確認）", "")
    else:
        what = ev["title"] + (f"（{ev['where']}）" if ev.get("where") else "")
    flag = "（待確認）" if ev.get("tentative") else ""
    return f"{when} {what}{flag}"


def is_interview(ev):
    """訪談類行程前後各留 BUFFER 分鐘（跟預約頁 coach_schedule_view._is_interview 同一套）。每週固定行程不算——
    週四那列「休息（訪談間隔）」本身就是緩衝，不能再加一圈。"""
    if "weekday" in ev:
        return False
    return ev.get("kind") == "interview" or bool(ev.get("guest")) or "訪談" in str(ev.get("title", ""))


def free_slots(d, data, win_start, win_end, minutes=60):
    busy = []
    for s, e, ev in blocks_on(d, data):
        if d.weekday() == 3 and str(ev.get("title", "")).startswith("線上"):
            continue  # 教練 2026-10-15：週四的線上聚會／學習保留，但訪談優先，不擋預約（跟預約頁一致）
        if d.weekday() == 2 and str(ev.get("title", "")).startswith("團隊週會"):
            continue  # 教練 2026-11-02：週三團隊週會掛線旁聽，訪談優先，不擋預約（跟預約頁一致）
        if is_interview(ev):
            s, e = s - BUFFER, e + BUFFER  # 教練 2026-10-19：已有訪談的前後各留半小時
        busy.append((s, e))
    busy.sort()
    slots, cur = [], win_start
    for s, e in busy:
        if e <= cur or s >= win_end:
            continue
        if s - cur >= minutes:
            slots.append((cur, min(s, win_end)))
        cur = max(cur, e)
    if win_end - cur >= minutes:
        slots.append((cur, win_end))
    return slots


def session_starts(d, data, a, b):
    """一場 SESSION 分鐘＋場間緩衝 BUFFER：每個空檔每 90 分鐘一個起點（19:00、20:30、22:00…）"""
    out = []
    for s_, e_ in free_slots(d, data, a, b, SESSION):
        t = s_
        while t + SESSION <= e_:
            out.append(t)
            t += SESSION + BUFFER
    return out


def win_start(data, d, default="10:00"):
    """白天可約窗口的起點。2026-10-23 教練：週六 9:30 起（總表 interview_window_start_by_weekday，鍵＝星期幾、0＝週一），
    其他天照 interview_window。跟預約頁 coach_schedule_view._win_start 同一套"""
    start = data.get("interview_window", {"start": default})["start"]
    return hm(data.get("interview_window_start_by_weekday", {}).get(str(d.weekday()), start))


def day_and_eve_starts(d, data):
    """(白天起點, 晚上起點)；白天最後一場要在晚上開始前留出緩衝。跟預約頁 coach_schedule_view._day_slots 同一套"""
    eve = data.get("evening_window", {"start": "19:00", "end": "22:00"})
    ws, es, ee = win_start(data, d), hm(eve["start"]), hm(eve["end"])
    return session_starts(d, data, ws, es - BUFFER), session_starts(d, data, es, ee)


def sessions_text(starts):
    return "、".join(f"{fmt(t)}–{fmt(t + SESSION)}" for t in starts)


def check(data, d, start=None, minutes=60, private=False):
    win = data.get("interview_window", {"start": "19:00", "end": "22:00"})
    ws, we = win_start(data, d, "19:00"), hm(win["end"])
    blocks = blocks_on(d, data)
    lines = [f"{day_label(d)}"]
    if start is not None:
        s, e = start, start + minutes
        hit = [b for b in blocks if b[0] < e and b[1] > s]
        if hit and all(b[2].get("soft") for b in hit):
            lines.append(f"  {fmt(s)}-{fmt(e)} ⚠️ 只撞到例行事項（教練說遇到重要會議可以調整，要請教練確認）：" + "；".join(describe(b, private) for b in hit))
        elif hit:
            lines.append(f"  {fmt(s)}-{fmt(e)} ❌ 不行，撞到：" + "；".join(describe(b, private) for b in hit))
        else:
            lines.append(f"  {fmt(s)}-{fmt(e)} ✅ 可以（教練這段沒有行程）")
    if blocks:
        lines.append("  當天行程：" + "；".join(describe(b, private) for b in blocks))
    else:
        lines.append("  當天行程：沒有")
    if minutes == SESSION:
        day_t, eve_t = day_and_eve_starts(d, data)
        lines.append(f"  可訪談時段（一場 1 小時，兩場之間留 {BUFFER} 分鐘緩衝）：" + (sessions_text(day_t + eve_t) or "沒有"))
    else:
        slots = free_slots(d, data, ws, we, minutes)
        lines.append(
            f"  {fmt(ws)}-{win['end']} 可訪談空檔（訪談前後各留 {BUFFER} 分鐘）："
            + ("、".join(f"{fmt(a)}-{fmt(b)}" for a, b in slots) if slots else "沒有")
        )
    return "\n".join(lines)


def listing(data, days=60, private=False):
    t = today()
    out = []
    for i in range(days):
        d = t + dt.timedelta(days=i)
        bs = blocks_on(d, data)
        if bs:
            out.append(f"{d.isoformat()} {day_label(d)}：" + "；".join(describe(b, private) for b in bs))
    return "\n".join(out)


BAHA_GROUP = "-5115910257"  # Telegram「佩佩老師的巴哈助理」


def notify_baha(ev):
    """榮樹下群組排定的訪談，通知巴哈助理群組（教練在那邊看所有行程、請巴哈設提醒）"""
    import subprocess
    d = dt.date.fromisoformat(ev["date"])
    when = "整天" if ev.get("allday") else f"{ev['start']}-{ev['end']}"
    msg = (f"📅 新行程（{ev.get('source', '')}，已寫進教練行程總表）\n"
           f"{day_label(d)} {when} {ev['title']}" + (f"（{ev['where']}）" if ev.get("where") else ""))
    cmd = [*_oc(), "message", "send", "--channel", "telegram", "--account", "bot_peipei",
           "--target", BAHA_GROUP, "-m", msg]
    if os.environ.get("COACH_SCHEDULE_DRYRUN"):
        cmd.append("--dry-run")  # 測試用：印出要送的內容，不真的送
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    print("✅ 已通知巴哈助理群組" if r.returncode == 0 else f"⚠️ 通知巴哈助理群組失敗：{(r.stderr or r.stdout)[-300:]}")


def is_rongshuxia(ev):
    t = ev.get("title", "")
    return ev.get("booking_type") == "榮樹下訪談" or t.startswith("榮樹下訪談") or t.startswith("訪談預約（待確認）")


def guest_form_url(ev):
    """榮樹下來賓資料表網址（2026-10-14）：每場訪談一組隨機代碼，拿到網址的來賓才填得到；表單在 event-signup/rongtree_guest.py。"""
    if not ev.get("form_token"):
        import secrets
        ev["form_token"] = secrets.token_urlsafe(9)
    return f"https://event.bymyway.com/rongtree/guest/{ev['form_token']}"


def guest_text(ev):
    """訪談對象。巴哈登記的場次常常只有把名字寫在標題（「榮樹下訪談：趙敏玄」）、沒填 guest 欄位，
    提醒訊息也要看得到名字，所以 guest 欄位空著時用標題後面那段（跟 event-signup/rongtree_guest.py 的 _event_guest 同一套）。"""
    g = ev.get("guest")
    if not g:
        t = (ev.get("title") or "").strip()
        g = t.split("：", 1)[1].strip() if t.startswith("榮樹下訪談：") else ""
    if not g:
        return ""
    return g + (f"（{ev['guest_field']}）" if ev.get("guest_field") else "")


def is_google_twin(ev, events):
    """同一場榮樹下訪談會在總表裡有兩筆：一筆是預約頁／巴哈登錄的正本（帶來賓、預約人），
    另一筆是 sync_google 從教練 Google 日曆讀進來的鏡像（id 每次同步還會重新編號）。
    2026-11-05：提醒迴圈沒有濾掉鏡像，於是每同步一次就多排一個提醒 cron（11/5、11/8 各多到 5 個），
    18:30 會在巴哈群組貼兩次同一場訪談。鏡像一律不排提醒、不單獨提醒。"""
    if ev.get("source") != "Google日曆":
        return False
    return any(o.get("id") != ev.get("id") and o.get("source") != "Google日曆"
               and o.get("date") == ev.get("date") and o.get("start") == ev.get("start")
               and is_rongshuxia(o) for o in events)


def rongshuxia_upcoming(data, days=60):
    now = dt.datetime.now(TZ)
    events = data.get("events", [])
    out = []
    for e in events:
        if not is_rongshuxia(e) or e.get("allday"):
            continue
        if is_google_twin(e, events):
            continue
        start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
        if now <= start <= now + dt.timedelta(days=days):
            out.append(e)
    return sorted(out, key=lambda e: (e["date"], e["start"]))


def _oc():
    """直接用 node 跑 openclaw：網站服務、排程的 PATH 不一定有 node"""
    node = os.path.expanduser("~/.nvm/versions/node/v24.22.2/bin/node")
    mjs = os.path.expanduser("~/.nvm/versions/node/v24.22.2/lib/node_modules/openclaw/openclaw.mjs")
    if os.path.exists(node) and os.path.exists(mjs):
        return [node, mjs]
    import shutil
    return [shutil.which("openclaw") or "openclaw"]


def send_baha(msg):
    import subprocess
    cmd = [*_oc(), "message", "send", "--channel", "telegram", "--account", "bot_peipei", "--target", BAHA_GROUP, "-m", msg]
    if os.environ.get("COACH_SCHEDULE_DRYRUN"):
        cmd.append("--dry-run")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return r.returncode == 0, (r.stderr or r.stdout)[-300:]


def cancel_reminder(ev):
    import subprocess
    job = ev.pop("reminder_job", None)
    if job and not os.environ.get("COACH_SCHEDULE_DRYRUN"):
        subprocess.run([*_oc(), "cron", "rm", job], capture_output=True, text=True, timeout=60)


LINE_GROUP = "C2f85a1e6010c4be676b93c5386da3d66"  # LINE「榮樹下談公益」群組


LINE_PUSH_FLAG = os.path.expanduser("~/.openclaw/workspace/state/LINE_REMINDER_PUSH_ENABLED")


def send_line_group(msg):
    """LINE 主動推播（沒人說話、到點自己發）要扣官方帳號額度（目前每月 200 則、群組每則按人數算），教練 2026-10-13 要求不要用。
    預設關閉；要開就建立 state/LINE_REMINDER_PUSH_ENABLED。群組內「有人說話時的回覆」不扣額度，改由群組小龍蝦在回覆時順便提醒（見 soon 指令）。"""
    if not os.path.exists(LINE_PUSH_FLAG):
        return None, "LINE 推播已關閉（省額度）"
    import subprocess
    cmd = [*_oc(), "message", "send", "--channel", "line", "--account", "default", "--target", LINE_GROUP, "-m", msg]
    if os.environ.get("COACH_SCHEDULE_DRYRUN"):
        cmd.append("--dry-run")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return r.returncode == 0, (r.stderr or r.stdout)[-300:]


def ensure_reminder(ev, force=False, events=None):
    """已確定的未來榮樹下訪談 → 排前 1 小時提醒；待確認、已排過（沒要求重排）、已過期都不動。回傳說明文字或 None"""
    if ev.get("allday") or ev.get("tentative") or not is_rongshuxia(ev):
        return None
    if events is None:
        events = []
    if is_google_twin(ev, events):
        return None  # Google 日曆同步出來的鏡像：正本已經會提醒，這裡再排一次就是重複通知
    if ev.get("reminder_job") and not force:
        return None
    return schedule_reminder(ev)


def schedule_reminder(ev):
    """開始前 1 小時提醒（已過就不排）。到點跑 remind --id，當下再讀總表，對象改過或行程刪了都以最新為準。"""
    import subprocess
    cancel_reminder(ev)
    start = dt.datetime.fromisoformat(f"{ev['date']}T{ev['start']}:00+08:00")
    at = start - dt.timedelta(hours=1)
    if at <= dt.datetime.now(TZ) + dt.timedelta(minutes=2):
        return "（開始前 1 小時已經過了，不排提醒）"
    argv = ["/usr/bin/python3", "-I", os.path.abspath(__file__), "remind", "--id", ev["id"]]
    cmd = [*_oc(), "cron", "add", "--name", f"榮樹下訪談提醒 {ev['date']} {ev['start']}",
           "--at", at.isoformat(timespec="seconds"), "--tz", "Asia/Taipei",
           "--command-argv", json.dumps(argv), "--no-deliver", "--delete-after-run", "--json"]
    if os.environ.get("COACH_SCHEDULE_DRYRUN"):
        return f"（測試：會在 {at.strftime('%m/%d %H:%M')} 提醒）"
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    m = re.search(r'"id"\s*:\s*"([^"]+)"', r.stdout or "")
    if r.returncode != 0 or not m:
        return f"⚠️ 提醒沒排成功：{(r.stderr or r.stdout)[-200:]}"
    ev["reminder_job"] = m.group(1)
    return f"已排好 {at.strftime('%m/%d %H:%M')} 提醒（開始前 1 小時）"


def booking_url():
    try:
        t = open(os.path.expanduser("~/.openclaw/workspace/state/coach_schedule_token.txt")).read().strip()
        return f"https://event.bymyway.com/schedule/{t}/" if t else ""
    except OSError:
        return ""


def open_slots(data, count=5):
    """2026-10-15 教練：任何 LINE 群有人問「最近五場可以訪談的時間」都要答得出來。
    跟預約頁（coach_schedule_view.py）同一套算法：晚上時段（evening_window）一場 1 小時、兩場之間留 30 分鐘（每 90 分鐘一個起點）；
    今天只算「現在起 1 小時之後」的起點；整天有行程的日子跳過。晚上排不滿 count 個才往白天補。"""
    now = dt.datetime.now(TZ)
    earliest = now.hour * 60 + now.minute + 60

    def starts(d, part):  # part：0＝白天、1＝晚上
        return [t for t in day_and_eve_starts(d, data)[part] if d > today() or t >= earliest]

    def allday(d):
        return any((s_, e_) == (0, 1440) for s_, e_, _ in blocks_on(d, data))

    picked = []
    for i in range(60):
        d = today() + dt.timedelta(days=i)
        if allday(d):
            continue
        picked += [(d, t) for t in starts(d, 1)]
        if len(picked) >= count:
            break
    picked = picked[:count]
    if len(picked) < count:  # 晚上不夠才補白天（很少發生）
        for i in range(60):
            d = today() + dt.timedelta(days=i)
            if allday(d):
                continue
            for t in starts(d, 0):
                if (d, t) not in picked:
                    picked.append((d, t))
        picked = sorted(picked)[:count]
    return [f"{day_label(d)} {fmt(t)}–{fmt(t + 60)}" for d, t in picked]


def open_days(data, days):
    """2026-10-15 教練：問「最近 3 天／一個禮拜／半個月」→ 逐天列出可訪談時段（晚上為主，白天另列）。
    同一套算法（訪談前後留緩衝、每 90 分鐘一個起點、整天有行程跳過）；今天只算現在起 1 小時之後。整天有行程或排滿的日子不列。"""
    now = dt.datetime.now(TZ)
    earliest = ((now.hour * 60 + now.minute + 60) + 59) // 60 * 60

    def sessions(d, part):  # part：0＝白天、1＝晚上；列「一場一場」的時段，不列整段空檔（整段空檔會讓人挑到沒留緩衝的起點）
        return sessions_text([t for t in day_and_eve_starts(d, data)[part] if d > today() or t >= earliest])

    out = []
    for i in range(days):
        d = today() + dt.timedelta(days=i)
        if any((s_, e_) == (0, 1440) for s_, e_, _ in blocks_on(d, data)):
            continue
        night, day = sessions(d, 1), sessions(d, 0)
        if not (night or day):
            continue
        out.append(f"{day_label(d)} " + (f"晚上 {night}" if night else "晚上排滿") + (f"｜白天 {day}" if day else ""))
    return out


def daily_report(data, d):
    """2026-10-13 教練：佩佩老師用手寫筆記本記行程，巴哈助理群組每天一則報告，一看就知道今天行程與可約空檔。"""
    lines = [f"☀️ {day_label(d)} 教練今日行程"]
    bs = blocks_on(d, data)
    for s_, e_, ev in bs:
        when = "整天" if (s_, e_) == (0, 1440) else f"{fmt(s_)}–{fmt(e_)}"
        title = ev["title"].replace("（待確認）", "")
        lines.append(f"・{when} {title}" + (f"（{ev['where']}）" if ev.get("where") else "") + ("（待確認）" if ev.get("tentative") else ""))
    if not bs:
        lines.append("・今天沒有排行程")
    allday = any((s_, e_) == (0, 1440) for s_, e_, _ in bs)
    now = dt.datetime.now(TZ)
    earliest = ((now.hour * 60 + now.minute + 59) // 60) * 60 if d == today() else 0
    free = [] if allday else [t for part in day_and_eve_starts(d, data) for t in part if t >= earliest]
    lines.append("")
    lines.append(f"🟢 今天還可以約（一場 1 小時，兩場之間留 {BUFFER} 分鐘緩衝）：" + (sessions_text(free) if free else "今天已經排滿了"))
    # 2026-10-23 教練親令：最多只列今天、明天、後天三天，不要佔版面
    nxt = []
    for i in range(1, 3):
        dd = d + dt.timedelta(days=i)
        if any((s_, e_) == (0, 1440) for s_, e_, _ in blocks_on(dd, data)):
            nxt.append(f"{day_label(dd)} 整天有行程")
            continue
        fs = [t for part in day_and_eve_starts(dd, data) for t in part]
        nxt.append(f"{day_label(dd)} " + (sessions_text(fs) if fs else "已排滿"))
    lines.append(f"📆 明天、後天可約（一場 1 小時，兩場之間留 {BUFFER} 分鐘緩衝）：\n" + "\n".join(f"・{x}" for x in nxt))
    url = booking_url()
    if url:
        lines.append("")
        lines.append("👉 要約教練：開預約頁，點時間，再選「咖啡會議／電話回訪／入會訪談」就送出（不用填資料）：")
        lines.append(url)
    return "\n".join(lines)


# ---------- 大台南行事曆 ----------
def clean_title(title):
    """教練 10/13：線上一定是 Zoom 線上，名稱後面不用再括號寫「Zoom 線上」「網路會議」。"""
    return re.sub(r"\s*[\(（]\s*(Zoom\s*線上|ZOOM線上|網路會議|線上)\s*[\)）]", "", title or "", flags=re.I).strip()


def simplify_tainan_title(title):
    """教練 10/13 要求行事曆名稱簡短明確：同步進來的名稱去掉括號備註、MSP／LTRT 只留代碼。"""
    t = clean_title(re.sub(r"\s*[\(（]適逢[^\)）]*[\)）]", "", title))
    if "MSP" in t:
        return "MSP"
    if t.startswith("LTRT"):
        return "LTRT"
    return t


def parse_tainan(html_text):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", html_text, flags=re.S)
    t = unescape(re.sub(r"<[^>]+>", "\n", t))
    L = [l.strip() for l in t.split("\n") if l.strip() and l.strip() not in ("🕒", "📍", "📹")]
    year = today().year
    m = re.search(r"(20\d\d)\s*全年度行事曆", t)
    if m:
        year = int(m.group(1))
    events = []
    for k, l in enumerate(L):
        m1 = re.match(r"^(\d{2})/(\d{2})\(", l)
        m2 = re.match(r"^(\d{2})(\d{2})-(\d{2})(\d{2})\(", l)
        if not (m1 or m2) or k + 3 >= len(L):
            continue
        title, tm, where = L[k + 1], L[k + 2], L[k + 3]
        if "ZOOM" not in where.upper() and "線上" not in where:
            continue  # 只收線上（教練 10/12：實體的 M1/M2 等不是教練的行程）
        tmm = re.match(r"^(\d{1,2}:\d{2})-(\d{1,2}:\d{2})$", tm)
        if not tmm:
            continue
        if m1:
            start_d = end_d = dt.date(year, int(m1.group(1)), int(m1.group(2)))
        else:
            start_d = dt.date(year, int(m2.group(1)), int(m2.group(2)))
            end_d = dt.date(year, int(m2.group(3)), int(m2.group(4)))
        s, e = tmm.groups()
        ev = {
            "id": f"tainan-{start_d.isoformat()}-{len(events)}",
            "date": start_d.isoformat(),
            "start": f"{int(s.split(':')[0]):02d}:{s.split(':')[1]}",
            "end": f"{int(e.split(':')[0]):02d}:{e.split(':')[1]}",
            "title": simplify_tainan_title(title),
            "where": "ZOOM線上",
            "source": "大台南行事曆",
        }
        if end_d != start_d:
            ev["end_date"] = end_d.isoformat()
        events.append(ev)
    return events


def sync_tainan(data):
    req = urllib.request.Request(TAINAN_URL, headers={"User-Agent": "coach-schedule/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        html_text = r.read().decode("utf-8", "replace")
    new = parse_tainan(html_text)
    if not new:
        raise SystemExit("大台南行事曆抓不到任何線上場次，可能網站改版，保留舊資料不覆蓋")
    # 教練改過時間的同步場次（例如 LTRT 與 RPL 撞期時 LTRT 改 20:00-21:00）：每次同步後重新套用，不會被來源蓋回去
    for o in data.get("tainan_overrides", []):
        for ev in new:
            if ev["date"] == o["date"] and ev["title"] == o["title"]:
                ev["start"], ev["end"] = o["start"], o["end"]
    keep = [e for e in data["events"] if e.get("source") != "大台南行事曆"]
    data["events"] = keep + new
    data["tainan_synced_at"] = dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    return len(new)


def google_title(title, d, start):
    """Google 行程照教練 10/13 定的名稱規則改名（見 simplify_tainan_title）；回傳 None＝教練說不是行程，不列入。
    只改總表裡的顯示名稱，不動教練的 Google 日曆。"""
    t = simplify_tainan_title(title)
    if t.startswith("公告") or "歸仁學法點" in t or "倒垃圾" in t:
        return None  # 教練 10/13：公告主持人提醒、歸仁學法點不是行程；倒垃圾回收＝總表固定的「家務時間」
    wd = d.weekday()
    if wd == 0 and start == "20:00" and "諮詢會議" in t:
        return None  # 教練 10/13：週一 20:00-21:00 的諮詢會議刪除（教練的是 21:00-22:00）
    if t == "學法":
        return "線上學習"
    if t in ("BNI全台交流", "線上學習-成功見証分享會") or (wd in (0, 3) and start == "17:30" and "分享會" in t):
        return "分享會"
    if 1 <= wd <= 4 and start and start < "10:00" and ("例會" in t or t == "真鑽會議"):
        return "BNI 例會"
    if wd == 1 and start == "21:30" and "真誠分會固定上線" in t:
        return "團隊會議"
    if wd == 2 and "方碩方" in t:
        return "團隊週會"
    return t


GCAL_ACCOUNT = "bymyway7@gmail.com"
GCAL_MAP = os.path.expanduser("~/.openclaw/workspace/state/gcal_sync_map.json")
GCAL_PUSH_SOURCES = ("預約頁", "巴哈", "coach", "教練")  # 大台南行事曆是官方來源，不往教練日曆寫


def _gog(*args, timeout=60):
    import subprocess
    r = subprocess.run(["/opt/homebrew/bin/gog", "-a", GCAL_ACCOUNT, "--no-input", *args],
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def google_summary(ev):
    """寫進教練 Google 日曆的名稱：跟預約頁／報告顯示的一樣；預約者姓名電話不寫。"""
    if ev.get("guest"):
        t = f"榮樹下訪談：{guest_text(ev)}"
    elif ev.get("source") == "預約頁":
        t = ev.get("booking_type") or "榮樹下訪談"
    else:
        t = ev["title"]
    t = t.replace("（待確認）", "").replace("（已確認）", "")
    return t + ("（待確認）" if ev.get("tentative") else "")


def _gcal_times(ev):
    if ev.get("allday"):
        last = dt.date.fromisoformat(ev.get("end_date", ev["date"]))
        return ev["date"], (last + dt.timedelta(days=1)).isoformat(), True   # 整天行程結束日不含
    return f"{ev['date']}T{ev['start']}:00+08:00", f"{ev['date']}T{ev['end']}:00+08:00", False


def push_google(data):
    """把總表裡「Google 還沒有」的行程寫進教練 Google 日曆（用 gog，教練已授權的帳號）。
    - 新增：預約頁／巴哈／榮樹下訪談等行程，Google 同時段已有就不寫（covered_by_google）。
    - 更新：之前由這支程式寫過的行程，名稱或時間改了（待確認→確認、改時間）就同步更新。
    - 刪除：之前由這支程式寫過、現在總表已移除的預約（取消預約）才刪；第一批由連接器手動補寫的 16 筆不自動刪。
    編號對照存 state/gcal_sync_map.json（總表 id → Google 行程編號；snap＝寫進去時的內容）。回傳 (新增, 更新, 刪除, 失敗訊息)"""
    try:
        with open(GCAL_MAP, encoding="utf-8") as f:
            m = json.load(f)
    except OSError:
        m = {"說明": "行程總表id→Google日曆event id", "map": {}}
    gmap, snap = m.setdefault("map", {}), m.setdefault("snap", {})
    today_s, added, updated, removed, errs = today().isoformat(), 0, 0, 0, []
    live = {e["id"]: e for e in data["events"]}
    for e in data["events"]:
        if e.get("source") not in GCAL_PUSH_SOURCES:
            continue
        if e.get("end_date", e["date"]) < today_s:
            continue
        frm, to, allday = _gcal_times(e)
        summ = google_summary(e)
        sig = f"{summ}|{frm}|{to}|{e.get('where', '')}"
        gid = gmap.get(e["id"])
        if gid is None:
            if e.get("covered_by_google"):
                continue
            args = ["calendar", "create", GCAL_ACCOUNT, "--summary", summ, "--from", frm, "--to", to, "--json", "--results-only"]
            if allday:
                args.append("--all-day")
            if e.get("where"):
                args += ["--location", e["where"]]
            rc, out, err = _gog(*args)
            mm = re.search(r'"id"\s*:\s*"([^"]+)"', out)
            if rc != 0 or not mm:
                errs.append(f"新增失敗 {e['date']} {summ}：{(err or out)[-160:]}")
                continue
            gmap[e["id"]], snap[e["id"]] = mm.group(1), sig
            added += 1
        elif e["id"] in snap and snap[e["id"]] != sig:
            args = ["calendar", "update", GCAL_ACCOUNT, gid, "--summary", summ, "--from", frm, "--to", to]
            if e.get("where"):
                args += ["--location", e["where"]]
            rc, out, err = _gog(*args)
            if rc != 0:
                errs.append(f"更新失敗 {e['date']} {summ}：{(err or out)[-160:]}")
                continue
            snap[e["id"]] = sig
            updated += 1
    for sid in [k for k in list(snap) if k not in live]:   # 只處理本程式寫過的；預約被取消＝總表已移除
        rc, out, err = _gog("calendar", "delete", GCAL_ACCOUNT, gmap[sid], "-y")
        if rc == 0:
            gmap.pop(sid, None), snap.pop(sid, None)
            removed += 1
        else:
            errs.append(f"刪除失敗 {sid}：{(err or out)[-160:]}")
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(GCAL_MAP), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    os.replace(tmp, GCAL_MAP)
    return added, updated, removed, errs


CANCELLABLE = ("預約頁", "巴哈", "coach", "教練")


def cancel_item(data, item_id, date_s):
    """預約頁「取消」按鈕用。單次行程＝整筆刪；每週固定行程＝只取消 date_s 那一天（加進 skip）。
    連同 Google 日曆裡我們寫過的那一筆、前 1 小時提醒一起清掉。只動總表自己的行程，來自 Google 日曆或大台南官方的不動。
    回傳 (訊息, 錯誤)。"""
    ev = next((e for e in data["events"] if e["id"] == item_id), None)
    if ev is not None:
        if ev.get("source") not in CANCELLABLE:
            return None, "這筆行程來自 Google 日曆或官方行事曆，請到來源那邊取消"
        cancel_reminder(ev)
        data["events"] = [e for e in data["events"] if e["id"] != item_id]
        label = f"{ev['date']} {ev.get('start', '整天')} {google_summary(ev)}"
        gid_key = item_id
    else:
        r = next((x for x in data.get("recurring", []) if x["id"] == item_id), None)
        if r is None:
            return None, "找不到這筆行程（可能剛被取消了）"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_s or ""):
            return None, "日期格式不正確"
        r.setdefault("skip", [])
        if date_s not in r["skip"]:
            r["skip"].append(date_s)
        label = f"{date_s} {r['start']} {r['title']}（只取消這一次）"
        gid_key = None
    try:  # 之前寫進教練 Google 日曆的那一筆（含第一批補寫的）也刪掉
        with open(GCAL_MAP, encoding="utf-8") as f:
            m = json.load(f)
        gid = m.get("map", {}).get(gid_key) if gid_key else None
        if gid:
            rc, out, err = _gog("calendar", "delete", GCAL_ACCOUNT, gid, "-y")
            if rc != 0:
                label += "（Google 日曆那筆沒刪成功，請手動刪）"
            else:
                m["map"].pop(gid_key, None)
                m.get("snap", {}).pop(gid_key, None)
                with open(GCAL_MAP, "w", encoding="utf-8") as f:
                    json.dump(m, f, ensure_ascii=False, indent=1)
    except OSError:
        pass
    return label, None


def ensure_fresh(max_age=60):
    """用到行程資料的當下才去看一次 Google 日曆（超過 max_age 秒沒看才看）。教練 10/13：不輪詢、不通知通道，
    有人打開預約頁／預約／巴哈報行程／查空檔的那一刻，當下現看，永遠是最新的，連「刪除」也不會漏。
    Google 讀不到就用現有資料，不影響原本動作。"""
    import fcntl
    import time
    if not DATA.endswith("教練行程總表.json"):
        return
    try:
        if time.time() - load().get("google_synced_epoch", 0) < max_age:
            return
        with open(DATA + ".lock", "w") as lockf:
            fcntl.flock(lockf, fcntl.LOCK_EX)
            d = load()
            if time.time() - d.get("google_synced_epoch", 0) < max_age:   # 等鎖的時候別人剛看過
                return
            sync_google(d)
            save(d)
    except (Exception, SystemExit) as ex:  # noqa: BLE001
        print(f"（Google 日曆這次沒讀到，先用現有行程：{ex}）", file=sys.stderr)


def sync_google(data, days=120):
    """讀教練 Google 日曆（非公開 iCal，唯讀）進總表，來源標「Google日曆」。Google 是教練親手維護的，同時段以它為準，
    總表裡跟它重複的手動／大台南項目標 covered_by_google，不再雙列。"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gcal_ical
    d0 = today()
    got = gcal_ical.events_between(gcal_ical.fetch(), d0, d0 + dt.timedelta(days=days))
    if len(got) < 5:
        raise SystemExit("Google 日曆只讀到 %d 筆，可能網址失效，保留舊資料不覆蓋" % len(got))
    seen, new, merged_starts = set(), [], {}
    # 2026-11-05：Google 事件的 id 以前每次同步都重新編號（gcal-<日期>-<序號>），提醒 cron 掛在舊 id 上就變成孤兒，
    # 每同步一次就多排一個重複提醒。這裡改用「舊事件的同一組時間＋名稱」沿用舊 id，id 固定、reminder_job 也跟著留著。
    old_gcal = {}
    for e in data.get("events", []):
        if e.get("source") == "Google日曆":
            old_gcal.setdefault((e.get("date"), e.get("start"), e.get("end"), e.get("title")), e)
    # 排序加標題：Google 讀回來的順序不一定每次一樣，同一時間的兩場會互換位置、id 就跟著跳。
    # 固定排序讓 id 穩定，提醒 cron 不會因為對調而變成孤兒。
    for g in sorted(got, key=lambda g: (g["date"], g["start"] or "", g["title"], g["end"] or "")):
        title = google_title(g["title"], dt.date.fromisoformat(g["date"]), g["start"])
        if title is None:
            continue
        for o in data.get("tainan_overrides", []):  # 教練改過時間的（LTRT／RPL 撞期）Google 讀進來一樣照改
            if not g["allday"] and o["date"] == g["date"] and o["title"] == title:
                g = {**g, "start": o["start"], "end": o["end"]}
        key = (g["date"], g["start"], g["end"], title)
        if key in seen:
            continue  # Google 裡 Cal.com 同步造成的重複只在這裡合併，不動教練日曆
        seen.add(key)
        old = old_gcal.get((g["date"], g.get("start"), g.get("end"), title))
        ev = {"id": (old or {}).get("id") or "gcal-%s-%d" % (g["date"], len(new)),
              "date": g["date"], "title": title, "source": "Google日曆"}
        if old and old.get("reminder_job"):
            ev["reminder_job"] = old["reminder_job"]  # 沿用舊提醒（id 固定了就不會重複排）
        if g["allday"]:
            ev["allday"] = True
            if g.get("end_date") and g["end_date"] != g["date"]:
                ev["end_date"] = g["end_date"]
        else:
            ev["start"], ev["end"] = g["start"], g["end"]
        last = new[-1] if new else None
        if (last and not ev.get("allday") and not last.get("allday") and last["date"] == ev["date"]
                and last["title"] == ev["title"] and ev["start"] < last["end"]):
            last["end"] = max(last["end"], ev["end"])  # 改名後同名又重疊（例：真鑽會議 06:00＋真鑽分會週例會 06:30）合成一筆
            merged_starts.setdefault(ev["date"], set()).add(ev["start"])  # 被合併那筆的開始時間也要拿去比對總表
            continue
        new.append(ev)
    data["events"] = [e for e in data["events"] if e.get("source") != "Google日曆"] + new
    gstart = {k: set(v) for k, v in merged_starts.items()}  # 日期 → 該日 Google 行程的開始時間集合
    gallday = set()
    for e in new:
        if e.get("allday"):
            gallday.add(e["date"])
        else:
            gstart.setdefault(e["date"], set()).add(e["start"])
    gtitled = {}  # 日期 → [(開始, 結束, 名稱)]：同名又重疊也算同一件（例：Google 06:00 BNI 例會 vs 總表固定 06:30）
    for e in new:
        if not e.get("allday"):
            gtitled.setdefault(e["date"], []).append((e["start"], e["end"], e["title"]))

    def in_google(date, start, end, title):
        return start in gstart.get(date, ()) or any(t == title and s < end and start < x
                                                     for s, x, t in gtitled.get(date, ()))

    try:
        with open(GCAL_MAP, encoding="utf-8") as f:
            pushed = set(json.load(f).get("map", {}))   # 已寫進 Google 的總表行程：以 Google 那筆為準，名稱不同也不雙列
    except OSError:
        pushed = set()
    cov = 0
    for e in data["events"]:
        # 2026-11-02：已帶 covered_by_google 旗標的也要每次重驗；Google 那筆不見了旗標就拿掉，否則預約頁的預約變隱形、空檔還顯示有空
        if (e.get("source") in ("巴哈", "教練", "大台南行事曆") and not e.get("guest")) or (e["id"] in pushed and e.get("source") != "Google日曆") \
                or (e.get("covered_by_google") and e.get("source") != "Google日曆"):
            hit = (e["date"] in gallday) if e.get("allday") else (
                e["start"] in gstart.get(e["date"], ()) if e["id"] in pushed else in_google(e["date"], e["start"], e["end"], e["title"]))
            e["covered_by_google"] = bool(hit)
            cov += bool(hit)
            if not hit:
                e.pop("covered_by_google", None)
    for r in data.get("recurring", []):
        r["gskip"] = [(d0 + dt.timedelta(days=i)).isoformat() for i in range(days + 1)
                      if (d0 + dt.timedelta(days=i)).weekday() == r["weekday"]
                      and in_google((d0 + dt.timedelta(days=i)).isoformat(), r["start"], r["end"], r["title"])]
    data["google_synced_at"] = dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    data["google_synced_epoch"] = int(__import__("time").time())
    return len(new), cov


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--date", required=True)
    a.add_argument("--end-date")
    a.add_argument("--start")
    a.add_argument("--end")
    a.add_argument("--allday", action="store_true")
    a.add_argument("--title", required=True)
    a.add_argument("--where", default="")
    a.add_argument("--source", default="巴哈")
    a.add_argument("--kind", default="busy", choices=["busy", "interview"])
    a.add_argument("--tentative", action="store_true")
    a.add_argument("--note", default="")
    a.add_argument("--notify-baha", action="store_true", help="寫入後在「佩佩老師的巴哈助理」群組貼一則通知")
    w = sub.add_parser("add-weekly")
    w.add_argument("--weekday", type=int, required=True, help="0=週一 … 6=週日")
    w.add_argument("--start", required=True)
    w.add_argument("--end", required=True)
    w.add_argument("--title", required=True)
    w.add_argument("--since")
    w.add_argument("--until")
    w.add_argument("--source", default="巴哈")
    w.add_argument("--tentative", action="store_true")
    r = sub.add_parser("remove")
    r.add_argument("--id", required=True)
    c = sub.add_parser("check")
    c.add_argument("--date", required=True)
    c.add_argument("--start")
    c.add_argument("--minutes", type=int, default=60)
    c.add_argument("--private", action="store_true")
    l = sub.add_parser("list")
    l.add_argument("--days", type=int, default=60)
    l.add_argument("--private", action="store_true")
    cf = sub.add_parser("confirm")
    cf.add_argument("--id", required=True)
    sub.add_parser("sync-tainan")
    sub.add_parser("sync-google")
    sub.add_parser("push-google")
    cx = sub.add_parser("cancel")
    cx.add_argument("--id", required=True)
    cx.add_argument("--date", default="")
    sub.add_parser("ensure-fresh")
    rs = sub.add_parser("rongshuxia")
    rs.add_argument("--days", type=int, default=60)
    sg = sub.add_parser("set-guest")
    sg.add_argument("--id", required=True)
    sg.add_argument("--guest", required=True)
    sg.add_argument("--field", default="")
    sg.add_argument("--by", default="")
    gf = sub.add_parser("guest-form")
    gf.add_argument("--id", required=True)
    ef = sub.add_parser("ensure-forms")
    ef.add_argument("--days", type=int, default=60)
    rm_ = sub.add_parser("remind")
    rm_.add_argument("--id", required=True)
    sub.add_parser("sync-reminders")
    so = sub.add_parser("soon")
    so.add_argument("--minutes", type=int, default=120)
    dr = sub.add_parser("daily-report")
    dr.add_argument("--date")
    dr.add_argument("--send", action="store_true")
    os_ = sub.add_parser("open-slots")
    os_.add_argument("--count", type=int, default=5)
    os_.add_argument("--days", type=int, default=0)  # 給了 --days 就改成逐天列出
    args = p.parse_args()

    if args.cmd in ("add", "remove", "confirm", "set-guest", "check", "list", "soon", "rongshuxia", "daily-report",
                    "open-slots", "ensure-fresh") and not os.environ.get("COACH_SCHEDULE_DRYRUN"):
        ensure_fresh()
    data = load()
    if args.cmd == "add":
        dt.date.fromisoformat(args.date)
        ev = {"id": uuid.uuid4().hex[:8], "date": args.date, "title": clean_title(args.title), "source": args.source}
        if args.end_date:
            dt.date.fromisoformat(args.end_date)
            ev["end_date"] = args.end_date
        if args.allday or not args.start:
            ev["allday"] = True
        else:
            if not args.end:
                raise SystemExit("有 --start 就要給 --end（或用 --allday）")
            hm(args.start), hm(args.end)
            ev["start"], ev["end"] = args.start, args.end
        for k in ("where", "note"):
            if getattr(args, k):
                ev[k] = getattr(args, k)
        if args.kind != "busy":
            ev["kind"] = args.kind
        if args.tentative:
            ev["tentative"] = True
        data["events"].append(ev)
        rem = ensure_reminder(ev, events=data.get("events", []))
        save(data)
        print(f"✅ 已寫入行程總表 id={ev['id']}")
        if rem:
            print(f"⏰ {rem}")
        print(check(data, dt.date.fromisoformat(args.date)))
        if args.notify_baha:
            notify_baha(ev)
    elif args.cmd == "add-weekly":
        rv = {"id": uuid.uuid4().hex[:8], "weekday": args.weekday, "start": args.start, "end": args.end,
              "title": clean_title(args.title), "source": args.source}
        for k in ("since", "until"):
            if getattr(args, k):
                rv[k] = getattr(args, k)
        if args.tentative:
            rv["tentative"] = True
        data.setdefault("recurring", []).append(rv)
        save(data)
        print(f"✅ 已寫入每週固定行程 id={rv['id']}：每週{WEEK[args.weekday]} {args.start}-{args.end} {args.title}")
    elif args.cmd == "remove":
        for e in data["events"]:
            if e["id"] == args.id:
                cancel_reminder(e)
        n0 = len(data["events"]) + len(data.get("recurring", []))
        data["events"] = [e for e in data["events"] if e["id"] != args.id]
        data["recurring"] = [e for e in data.get("recurring", []) if e["id"] != args.id]
        if n0 == len(data["events"]) + len(data["recurring"]):
            raise SystemExit(f"找不到 id={args.id}")
        save(data)
        print(f"✅ 已刪除 id={args.id}")
    elif args.cmd == "cancel":
        import fcntl
        with open(DATA + ".lock", "w") as lockf:
            fcntl.flock(lockf, fcntl.LOCK_EX)
            data = load()
            msg, err = cancel_item(data, args.id, args.date)
            if err:
                print(err)
                raise SystemExit(1)
            save(data)
        print(f"✅ 已取消：{msg}")
    elif args.cmd == "confirm":
        hit = [e for e in data["events"] if e["id"] == args.id]
        if not hit:
            raise SystemExit(f"找不到 id={args.id}")
        hit[0].pop("tentative", None)
        # 預約頁新格式（有 booking_type）確認後就是乾淨的類型名稱，例：榮樹下訪談
        hit[0]["title"] = (f"榮樹下訪談：{hit[0]['guest']}" if hit[0].get("guest") else
                           hit[0].get("booking_type") or hit[0]["title"].replace("（待確認）", "（已確認）"))
        rem = ensure_reminder(hit[0], events=data.get("events", []))
        save(data)
        print(f"✅ 已確認 id={args.id}：{hit[0]['date']} {hit[0].get('start','')} {hit[0]['title']}")
        print(hit[0].get("note", ""))
        if rem:
            print(f"⏰ {rem}")
    elif args.cmd == "check":
        start = hm(args.start) if args.start else None
        print(check(data, dt.date.fromisoformat(args.date), start, args.minutes, args.private))
    elif args.cmd == "list":
        print(listing(data, args.days, args.private) or "接下來沒有行程")
    elif args.cmd == "rongshuxia":
        evs = rongshuxia_upcoming(data, args.days)
        for e in evs:
            d = dt.date.fromisoformat(e["date"])
            flag = "（待教練確認）" if e.get("tentative") else ""
            print(f"id={e['id']}｜{day_label(d)} {e['start']}-{e['end']}{flag}｜對象：{guest_text(e) or '還沒填'}")
        if not evs:
            print("接下來沒有榮樹下訪談")
    elif args.cmd == "set-guest":
        hit = [e for e in rongshuxia_upcoming(data, 365) if e["id"] == args.id]
        if not hit:
            raise SystemExit(f"找不到這場榮樹下訪談 id={args.id}（只能登記未來的榮樹下訪談）")
        ev = hit[0]
        guest = re.sub(r"\s+", " ", args.guest).strip()[:40]
        field = re.sub(r"\s+", " ", args.field).strip().strip("-－—").strip()[:30]
        if not guest:
            raise SystemExit("訪談對象不能空白")
        ev["guest"] = guest
        if field:
            ev["guest_field"] = field
        else:
            ev.pop("guest_field", None)
        if args.by:
            ev["guest_by"] = args.by[:20]
        if not ev.get("tentative"):
            ev["title"] = f"榮樹下訪談：{guest}"
        rem = ensure_reminder(ev, force=True, events=data.get("events", [])) or "（這個時段還在待確認，教練確認後才會排提醒）"
        form = guest_form_url(ev)
        save(data)
        d = dt.date.fromisoformat(ev["date"])
        when = f"{day_label(d)} {ev['start']}-{ev['end']}"
        tent = "（這個時段還在等教練確認）" if ev.get("tentative") else ""
        ok, err = send_baha(f"📅 教練，{when} 榮樹下我們要訪談 {guest_text(ev)}{tent}\n"
                            f"{('（' + args.by + '在 LINE 榮樹下群組登記的）') if args.by else ''}\n{rem}")
        print(f"✅ 已登記：{when} 榮樹下訪談，對象 {guest_text(ev)}{tent}")
        print("✅ 已通知巴哈助理群組" if ok else f"⚠️ 通知巴哈助理群組失敗：{err}")
        print(rem)
        print("📝 來賓資料表（請轉給來賓填寫，交回後 AI 會整理成來賓卡給主持人）：")
        print(form)
    elif args.cmd == "guest-form":
        hit = [e for e in data["events"] if e["id"] == args.id and is_rongshuxia(e)]
        if not hit:
            raise SystemExit(f"找不到這場榮樹下訪談 id={args.id}")
        url = guest_form_url(hit[0])
        save(data)
        print(url)
    elif args.cmd == "ensure-forms":
        # 榮樹下網頁「訪談嘉賓前置作業」區（2026-10-14 教練）：接下來每場訪談都要有來賓資料表網址
        evs = rongshuxia_upcoming(data, args.days)
        new = [e for e in evs if not e.get("form_token")]
        for e in new:
            guest_form_url(e)
        if new:
            save(data)
        print(f"接下來 {len(evs)} 場榮樹下訪談，新配 {len(new)} 個來賓資料表網址")
    elif args.cmd == "remind":
        hit = [e for e in data["events"] if e["id"] == args.id]
        if not hit:
            print("行程已刪除，不提醒")
            return
        ev = hit[0]
        if is_google_twin(ev, data.get("events", [])):
            print("這是 Google 日曆同步出來的重複紀錄，不提醒")
            return
        if ev.get("tentative"):
            print("這場又變回待確認，不提醒")
            return
        mins = (dt.datetime.fromisoformat(f"{ev['date']}T{ev['start']}:00+08:00") - dt.datetime.now(TZ)).total_seconds() / 60
        if not (-5 <= mins <= 90) and not os.environ.get("COACH_SCHEDULE_DRYRUN"):
            print(f"行程時間已改（現在離開始還有 {int(mins)} 分鐘），這個提醒作廢")
            return
        g = guest_text(ev)
        text = f"⏰ 一個小時之後（{ev['start']}）即將有 Podcast 訪談" + (f"（訪談對象：{g}）" if g else "") + "，請提早做好準備，上線做準備。"
        ok1, err1 = send_line_group(text)
        ok2, err2 = send_baha(text)
        l1 = "不推播（省額度）" if ok1 is None else ("✅" if ok1 else "⚠️ 失敗 " + err1)
        print(f"LINE 榮樹下群組：{l1}｜巴哈群組：{'✅' if ok2 else '⚠️ 失敗 ' + err2}")
        if not (ok1 or ok2):
            raise SystemExit(1)
    elif args.cmd == "soon":
        now = dt.datetime.now(TZ)
        for e in rongshuxia_upcoming(data, 1):
            if e.get("tentative"):
                continue
            start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
            m = int((start - now).total_seconds() // 60)
            if 0 <= m <= args.minutes:
                g = guest_text(e)
                print(f"{e['start']} 開始（還有 {m} 分鐘）" + (f"，訪談對象：{g}" if g else ""))
    elif args.cmd == "sync-reminders":
        n = 0
        for e in rongshuxia_upcoming(data, 60):
            r = ensure_reminder(e, events=data.get("events", []))
            if r:
                n += 1
                print(f"{e['date']} {e['start']}：{r}")
        save(data)
        print(f"✅ 補排了 {n} 個提醒")
    elif args.cmd == "daily-report":
        d = dt.date.fromisoformat(args.date) if args.date else today()
        msg = daily_report(data, d)
        if args.send:
            for e in rongshuxia_upcoming(data, 14):   # 順手補排漏掉的提醒
                ensure_reminder(e, events=data.get("events", []))
            save(data)
            ok, err = send_baha(msg)
            print("✅ 已貼到巴哈助理群組" if ok else f"⚠️ 貼到巴哈助理群組失敗：{err}")
        else:
            print(msg)
    elif args.cmd == "sync-tainan":
        n = sync_tainan(data)
        save(data)
        print(f"✅ 大台南行事曆線上場次已同步 {n} 筆")
    elif args.cmd == "sync-google":
        import fcntl  # 跟預約頁 book() 用同一把鎖，避免同步剛好蓋掉一筆新預約
        with open(DATA + ".lock", "w") as lockf:
            fcntl.flock(lockf, fcntl.LOCK_EX)
            data = load()
            n, cov = sync_google(data)
            save(data)
        print(f"✅ Google 日曆已同步 {n} 筆（總表原有 {cov} 筆因 Google 已有而不重複計）")
        if not os.environ.get("COACH_SCHEDULE_NO_PUSH"):
            with open(DATA + ".lock", "w") as lockf:
                fcntl.flock(lockf, fcntl.LOCK_EX)
                a_, u_, r_, errs = push_google(load())
            print(f"📤 寫回 Google：新增 {a_}、更新 {u_}、刪除 {r_}" + ("".join("\n⚠️ " + x for x in errs)))
    elif args.cmd == "open-slots":
        rows = open_days(data, args.days) if args.days else open_slots(data, args.count)
        print("\n".join(rows) if rows else "這段期間沒有可約時段")
    elif args.cmd == "ensure-fresh":
        pass  # 上面已經 ensure_fresh 過了
    elif args.cmd == "push-google":
        a_, u_, r_, errs = push_google(load())
        print(f"📤 寫回 Google：新增 {a_}、更新 {u_}、刪除 {r_}" + ("".join("\n⚠️ " + x for x in errs)))


def main_then_push():
    """巴哈助理／LINE 小龍蝦用 add／remove／confirm／set-guest 改了總表，當下就寫回教練 Google 日曆（失敗不影響原本動作，15 分鐘的同步會補）。"""
    main()
    if len(sys.argv) > 1 and sys.argv[1] in ("add", "remove", "confirm", "set-guest") and not os.environ.get("COACH_SCHEDULE_DRYRUN") \
            and not os.environ.get("COACH_SCHEDULE_NO_PUSH") and DATA.endswith("教練行程總表.json"):
        try:
            import fcntl
            with open(DATA + ".lock", "w") as lockf:
                fcntl.flock(lockf, fcntl.LOCK_EX)
                a_, u_, r_, errs = push_google(load())
            if a_ or u_ or r_ or errs:
                print(f"📤 已寫回 Google 日曆：新增 {a_}、更新 {u_}、刪除 {r_}" + ("".join("\n⚠️ " + x for x in errs)))
        except Exception as ex:  # noqa: BLE001
            print(f"⚠️ 寫回 Google 日曆沒成功（15 分鐘後的同步會補）：{ex}")


if __name__ == "__main__":
    main_then_push()
