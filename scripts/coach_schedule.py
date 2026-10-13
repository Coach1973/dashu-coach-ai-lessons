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

DATA = os.path.expanduser("~/.openclaw/workspace/knowledges/教練行程總表.json")
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
        if ev.get("source") == "預約頁":
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
    cmd = ["openclaw", "message", "send", "--channel", "telegram", "--account", "bot_peipei",
           "--target", BAHA_GROUP, "-m", msg]
    if os.environ.get("COACH_SCHEDULE_DRYRUN"):
        cmd.append("--dry-run")  # 測試用：印出要送的內容，不真的送
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    print("✅ 已通知巴哈助理群組" if r.returncode == 0 else f"⚠️ 通知巴哈助理群組失敗：{(r.stderr or r.stdout)[-300:]}")


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
        hit[0]["title"] = hit[0].get("booking_type") or hit[0]["title"].replace("（待確認）", "（已確認）")
        save(data)
        print(f"✅ 已確認 id={args.id}：{hit[0]['date']} {hit[0].get('start','')} {hit[0]['title']}")
        print(hit[0].get("note", ""))
    elif args.cmd == "check":
        start = hm(args.start) if args.start else None
        print(check(data, dt.date.fromisoformat(args.date), start, args.minutes, args.private))
    elif args.cmd == "list":
        print(listing(data, args.days, args.private) or "接下來沒有行程")
    elif args.cmd == "sync-tainan":
        n = sync_tainan(data)
        save(data)
        print(f"✅ 大台南行事曆線上場次已同步 {n} 筆")


if __name__ == "__main__":
    main()
