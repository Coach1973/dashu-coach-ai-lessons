#!/usr/bin/env python3
"""查某天活動「目前報名幾人」（2026-10-18，給小龍蝦／夥伴問人數用）

起因：佩君老師 10/15～10/17 問了 4 次「目前報名幾人」，小龍蝦試登入後台 9 次失敗、
給了舊數字；另一個分身說「手上沒有資料」。報名資料就在本機 event.db，一行查得到。

用法：python3 query_signups.py 10/19        （也吃 1019、2026-10-19、今天、明天、slug；「近期」＝接下來 5 場）
只輸出場次與人數，不輸出任何人名電話（夥伴也可能在群組問）。
報名人數教練預設不公開（show_live_count），只回答教練本人與夥伴，不回答一般會員。
"""
import datetime
import os
import re
import sqlite3
import sys

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event.db")


def parse_day(arg, today):
    a = arg.strip()
    if a in ("今天", "today"):
        return today
    if a in ("明天", "tomorrow"):
        return today + datetime.timedelta(days=1)
    m = re.fullmatch(r"(?:(20\d\d)[-/年.])?(\d{1,2})[-/月.](\d{1,2})日?", a) or re.fullmatch(r"(\d{2})(\d{2})", a)
    if not m:
        return None
    g = m.groups()
    year, mo, da = (int(g[0]) if len(g) == 3 and g[0] else today.year), int(g[-2]), int(g[-1])
    try:
        return datetime.date(year, mo, da)
    except ValueError:
        return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    arg = " ".join(sys.argv[1:])
    today = datetime.date.today()
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    day = parse_day(arg, today)
    if arg.strip() in ("近期", "upcoming"):
        rows = con.execute(
            "select id, name, event_date, start_time, status from events where event_date>=? and coalesce(status,'active')='active' "
            "order by event_date, start_time limit 5", (today.isoformat(),)
        ).fetchall()
    elif day:
        rows = con.execute(
            "select id, name, event_date, start_time, status from events where event_date=? order by start_time", (day.isoformat(),)
        ).fetchall()
    else:
        rows = con.execute("select id, name, event_date, start_time, status from events where slug=?", (arg.strip(),)).fetchall()
    if not rows:
        what = f"{day.month}/{day.day}" if day else arg
        print(f"大樹報名系統裡 {what} 沒有場次，所以查不到報名人數。"
              "這場可能是外部單位自己收報名（例如 BNI 官方培訓、合作單位的表單），要問主辦單位。")
        return
    now = datetime.datetime.now().strftime("%m/%d %H:%M")
    for eid, name, d, t, status in rows:
        n, last = con.execute("select count(*), max(created_at) from signups where event_id=?", (eid,)).fetchone()
        dd = datetime.date.fromisoformat(d)
        when = f"{dd.month}/{dd.day}" + (f" {t}" if t else "")
        tail = f"，最新一筆 {last[5:16].replace('-', '/')}" if last else ""
        flag = "" if (status or "active") == "active" else f"（狀態：{status}）"
        print(f"{when}「{name}」{flag}：目前 {n} 筆報名（{now} 即時查詢{tail}）")


if __name__ == "__main__":
    main()
