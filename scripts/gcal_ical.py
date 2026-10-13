#!/usr/bin/env python3
"""讀教練 Google 日曆的非公開 iCal，展開重複行程，回傳一段日期範圍內的行程。

只取標題與時間（不碰描述，描述裡有 Zoom 密碼）。純標準庫，因為 coach_schedule.py 用 python3 -I 跑。
網址放 ~/.openclaw/credentials/google_calendar_private_ical_url.txt（不進 git）。
"""
import datetime as dt
import os
import re
import urllib.request

URL_FILE = os.path.expanduser("~/.openclaw/credentials/google_calendar_private_ical_url.txt")
TZ = dt.timezone(dt.timedelta(hours=8))
DAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def fetch():
    url = open(URL_FILE).read().strip()
    req = urllib.request.Request(url, headers={"User-Agent": "coach-schedule/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _unfold(text):
    return re.sub(r"\r?\n[ \t]", "", text).replace("\r\n", "\n")


def _unescape(s):
    return s.replace("\\,", ",").replace("\\;", ";").replace("\\n", " ").replace("\\\\", "\\")


def _dt(val, params):
    """回傳 (datetime 台灣時間, 是否整天)。"""
    val = val.strip()
    if "VALUE=DATE" in params or re.fullmatch(r"\d{8}", val):
        d = dt.datetime.strptime(val[:8], "%Y%m%d")
        return d.replace(tzinfo=TZ), True
    if val.endswith("Z"):
        return dt.datetime.strptime(val, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc).astimezone(TZ), False
    return dt.datetime.strptime(val[:15], "%Y%m%dT%H%M%S").replace(tzinfo=TZ), False


def _props(block):
    """block 內每行 → dict[name] = [(params, value)]"""
    out = {}
    for line in block.split("\n"):
        if ":" not in line:
            continue
        head, _, val = line.partition(":")
        name, _, params = head.partition(";")
        out.setdefault(name.upper(), []).append((params.upper(), val))
    return out


def _rule(s):
    r = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            r[k.upper()] = v
    return r


def _expand(start, rule, until_limit, exdates):
    """產生 start 之後所有重複起點（≤ until_limit）。支援 DAILY／WEEKLY／MONTHLY（BYMONTHDAY 或 BYDAY+BYSETPOS）。"""
    freq = rule.get("FREQ")
    interval = int(rule.get("INTERVAL", 1))
    count = int(rule["COUNT"]) if "COUNT" in rule else None
    limit = until_limit
    if "UNTIL" in rule:
        u, _ = _dt(rule["UNTIL"], "")
        limit = min(limit, u)
    out, n = [], 0
    day = start.date()
    t = start.timetz()
    byday = [d[-2:] for d in rule.get("BYDAY", "").split(",") if d]
    cur = day
    guard = 0
    while guard < 4000:
        guard += 1
        cands = []
        if freq == "DAILY":
            cands = [cur]
            nxt = cur + dt.timedelta(days=interval)
        elif freq == "WEEKLY":
            monday = cur - dt.timedelta(days=cur.weekday())
            wk = byday or [DAYS[start.weekday()]]
            cands = [monday + dt.timedelta(days=DAYS.index(w)) for w in wk]
            nxt = monday + dt.timedelta(weeks=interval)
        elif freq == "MONTHLY":
            y, m = cur.year, cur.month
            if "BYMONTHDAY" in rule:
                try:
                    cands = [dt.date(y, m, int(rule["BYMONTHDAY"]))]
                except ValueError:
                    cands = []
            elif byday and "BYSETPOS" in rule:
                w = DAYS.index(byday[0])
                days = [dt.date(y, m, d) for d in range(1, 32) if _valid(y, m, d) and dt.date(y, m, d).weekday() == w]
                k = int(rule["BYSETPOS"])
                cands = [days[k - 1] if k > 0 else days[k]] if days and abs(k) <= len(days) else []
            else:
                try:
                    cands = [dt.date(y, m, start.day)]
                except ValueError:
                    cands = []
            nm = m + interval
            nxt = dt.date(y + (nm - 1) // 12, (nm - 1) % 12 + 1, 1)
        else:
            return [start]
        for c in sorted(cands):
            if c < day:
                continue
            s = dt.datetime.combine(c, t)
            if s > limit:
                return out
            n += 1
            if count and n > count:
                return out
            if s.replace(tzinfo=TZ) not in exdates:
                out.append(s)
        if nxt > limit.date():
            break
        cur = nxt
    return out


def _valid(y, m, d):
    try:
        dt.date(y, m, d)
        return True
    except ValueError:
        return False


def events_between(text, d0, d1):
    """回傳 [{'date','start','end','allday','title','uid'}]，d0~d1 含頭尾（date）。"""
    text = _unfold(text)
    blocks = text.split("BEGIN:VEVENT")[1:]
    lo = dt.datetime.combine(d0, dt.time(0), TZ)
    hi = dt.datetime.combine(d1, dt.time(23, 59), TZ)
    overrides = {}  # (uid, 原始起點) → 例外版本 block
    masters = []
    for b in blocks:
        b = b.split("END:VEVENT")[0]
        p = _props(b)
        if "RECURRENCE-ID" in p:
            rid, _ = _dt(p["RECURRENCE-ID"][0][1], p["RECURRENCE-ID"][0][0])
            overrides[(p["UID"][0][1], rid)] = p
        else:
            masters.append(p)
    res = []

    def emit(p, s, e, allday):
        if (p.get("STATUS") or [("", "")])[0][1].strip().upper() == "CANCELLED":
            return
        if "[總表:" in (p.get("DESCRIPTION") or [("", "")])[0][1]:
            return  # 這是行程總表寫進 Google 的分身，不要再讀回總表（會重複）
        title = _unescape((p.get("SUMMARY") or [("", "")])[0][1]).strip()
        if allday:
            last = (e - dt.timedelta(days=1)).date() if e else s.date()
            if last < d0 or s.date() > d1:
                return
            res.append({"date": s.date().isoformat(), "end_date": last.isoformat(), "start": None, "end": None,
                        "allday": True, "title": title, "uid": p["UID"][0][1]})
        else:
            if s > hi or e < lo:
                return
            res.append({"date": s.date().isoformat(), "start": s.strftime("%H:%M"), "end": e.strftime("%H:%M") if e.date() == s.date() else "23:59",
                        "allday": False, "title": title, "uid": p["UID"][0][1]})

    for p in masters:
        if "DTSTART" not in p:
            continue
        s, allday = _dt(p["DTSTART"][0][1], p["DTSTART"][0][0])
        if "DTEND" in p:
            e, _ = _dt(p["DTEND"][0][1], p["DTEND"][0][0])
        else:
            e = s + (dt.timedelta(days=1) if allday else dt.timedelta(hours=1))
        dur = e - s
        if "RRULE" not in p:
            emit(p, s, e, allday)
            continue
        ex = set()
        for params, v in p.get("EXDATE", []):
            for one in v.split(","):
                ex.add(_dt(one, params)[0])
        for st in _expand(s, _rule(p["RRULE"][0][1]), hi, ex):
            st = st.replace(tzinfo=TZ)
            ov = overrides.get((p["UID"][0][1], st))
            if ov:  # 這一次被改過：用改後的時間與標題
                os_, oall = _dt(ov["DTSTART"][0][1], ov["DTSTART"][0][0])
                oe, _ = _dt(ov["DTEND"][0][1], ov["DTEND"][0][0]) if "DTEND" in ov else (os_ + dur, False)
                emit(ov, os_, oe, oall)
            else:
                emit(p, st, st + dur, allday)
    return res
