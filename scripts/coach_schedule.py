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
  coach_schedule.py remind --id <id>                   # 提醒排程到點時呼叫，送提醒到巴哈群組
  coach_schedule.py daily-report [--date YYYY-MM-DD] [--send]   # 每日行程報告（今天行程＋可約空檔＋預約頁），--send 貼到巴哈群組

2026-10-13 教練：榮樹下的時間由邱裕榮先定、對象之後才定。邱裕榮在 LINE 群組講「哪一場訪問誰」
→ 群組小龍蝦（schedule-context 外掛）呼叫 set-guest → 巴哈助理群組收到「教練，幾月幾號榕樹下要跟某某訪談」，
並排一個開始前 1 小時的提醒（openclaw cron 一次性工作，id 記在事件的 reminder_job；改對象就換新、刪行程就一起刪）。
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


def today():
    return dt.datetime.now(TZ).date()


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(d):
    d["updated_at"] = dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
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
        if iso in r.get("skip", []):
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


def free_slots(d, data, win_start, win_end, minutes=60):
    busy = [(s, e) for s, e, _ in blocks_on(d, data)]
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


def check(data, d, start=None, minutes=60, private=False):
    win = data.get("interview_window", {"start": "19:00", "end": "22:00"})
    ws, we = hm(win["start"]), hm(win["end"])
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
    slots = free_slots(d, data, ws, we, minutes)
    lines.append(
        f"  {win['start']}-{win['end']} 可訪談空檔："
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


def guest_text(ev):
    if not ev.get("guest"):
        return ""
    return ev["guest"] + (f"（{ev['guest_field']}）" if ev.get("guest_field") else "")


def rongshuxia_upcoming(data, days=60):
    now = dt.datetime.now(TZ)
    out = []
    for e in data.get("events", []):
        if not is_rongshuxia(e) or e.get("allday"):
            continue
        start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
        if now <= start <= now + dt.timedelta(days=days):
            out.append(e)
    return sorted(out, key=lambda e: (e["date"], e["start"]))


def _oc():
    """直接用 node 跑 openclaw：網站服務、排程的 PATH 不一定有 node"""
    node = os.path.expanduser("~/.nvm/versions/node/v24.21.0/bin/node")
    mjs = os.path.expanduser("~/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/openclaw.mjs")
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


def daily_report(data, d):
    """2026-10-13 教練：佩佩老師用手寫筆記本記行程，巴哈助理群組每天一則報告，一看就知道今天行程與可約空檔。"""
    win = data.get("interview_window", {"start": "10:00", "end": "22:00"})
    ws, we = hm(win["start"]), hm(win["end"])
    lines = [f"☀️ {day_label(d)} 教練今日行程"]
    bs = blocks_on(d, data)
    for s_, e_, ev in bs:
        when = "整天" if (s_, e_) == (0, 1440) else f"{fmt(s_)}–{fmt(e_)}"
        title = ev["title"].replace("（待確認）", "")
        lines.append(f"・{when} {title}" + (f"（{ev['where']}）" if ev.get("where") else "") + ("（待確認）" if ev.get("tentative") else ""))
    if not bs:
        lines.append("・今天沒有排行程")
    allday = any((s_, e_) == (0, 1440) for s_, e_, _ in bs)
    if d == today():
        now = dt.datetime.now(TZ)
        ws = max(ws, ((now.hour * 60 + now.minute + 59) // 60) * 60)
    free = [] if allday else free_slots(d, data, ws, we)
    lines.append("")
    lines.append("🟢 今天還可以約：" + ("、".join(f"{fmt(a)}–{fmt(b)}" for a, b in free) if free else "今天已經排滿了"))
    nxt = []
    for i in range(1, 8):
        dd = d + dt.timedelta(days=i)
        if any((s_, e_) == (0, 1440) for s_, e_, _ in blocks_on(dd, data)):
            nxt.append(f"{day_label(dd)} 整天有行程")
            continue
        fs = free_slots(dd, data, hm(win["start"]), hm(win["end"]))
        nxt.append(f"{day_label(dd)} " + ("、".join(f"{fmt(a)}–{fmt(b)}" for a, b in fs) if fs else "已排滿"))
    lines.append("📆 接下來 7 天可約（10:00–22:00 內）：\n" + "\n".join(f"・{x}" for x in nxt))
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
    rs = sub.add_parser("rongshuxia")
    rs.add_argument("--days", type=int, default=60)
    sg = sub.add_parser("set-guest")
    sg.add_argument("--id", required=True)
    sg.add_argument("--guest", required=True)
    sg.add_argument("--field", default="")
    sg.add_argument("--by", default="")
    rm_ = sub.add_parser("remind")
    rm_.add_argument("--id", required=True)
    dr = sub.add_parser("daily-report")
    dr.add_argument("--date")
    dr.add_argument("--send", action="store_true")
    args = p.parse_args()

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
        save(data)
        print(f"✅ 已寫入行程總表 id={ev['id']}")
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
    elif args.cmd == "confirm":
        hit = [e for e in data["events"] if e["id"] == args.id]
        if not hit:
            raise SystemExit(f"找不到 id={args.id}")
        hit[0].pop("tentative", None)
        # 預約頁新格式（有 booking_type）確認後就是乾淨的類型名稱，例：榮樹下訪談
        hit[0]["title"] = (f"榮樹下訪談：{hit[0]['guest']}" if hit[0].get("guest") else
                           hit[0].get("booking_type") or hit[0]["title"].replace("（待確認）", "（已確認）"))
        save(data)
        print(f"✅ 已確認 id={args.id}：{hit[0]['date']} {hit[0].get('start','')} {hit[0]['title']}")
        print(hit[0].get("note", ""))
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
        rem = schedule_reminder(ev)
        save(data)
        d = dt.date.fromisoformat(ev["date"])
        when = f"{day_label(d)} {ev['start']}-{ev['end']}"
        tent = "（這個時段還在等教練確認）" if ev.get("tentative") else ""
        ok, err = send_baha(f"📅 教練，{when} 榮樹下我們要訪談 {guest_text(ev)}{tent}\n"
                            f"{('（' + args.by + '在 LINE 榮樹下群組登記的）') if args.by else ''}\n{rem}")
        print(f"✅ 已登記：{when} 榮樹下訪談，對象 {guest_text(ev)}{tent}")
        print("✅ 已通知巴哈助理群組" if ok else f"⚠️ 通知巴哈助理群組失敗：{err}")
        print(rem)
    elif args.cmd == "remind":
        hit = [e for e in data["events"] if e["id"] == args.id]
        if not hit:
            print("行程已刪除，不提醒")
            return
        ev = hit[0]
        g = guest_text(ev)
        ok, err = send_baha(f"⏰ 教練，1 小時後（{ev['start']}）榮樹下訪談" + (f"：{g}" if g else "（訪談對象還沒填）"))
        print("✅ 已提醒" if ok else f"⚠️ 提醒送出失敗：{err}")
    elif args.cmd == "daily-report":
        d = dt.date.fromisoformat(args.date) if args.date else today()
        msg = daily_report(data, d)
        if args.send:
            ok, err = send_baha(msg)
            print("✅ 已貼到巴哈助理群組" if ok else f"⚠️ 貼到巴哈助理群組失敗：{err}")
        else:
            print(msg)
    elif args.cmd == "sync-tainan":
        n = sync_tainan(data)
        save(data)
        print(f"✅ 大台南行事曆線上場次已同步 {n} 筆")


if __name__ == "__main__":
    main()
