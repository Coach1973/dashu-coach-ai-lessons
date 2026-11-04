#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依場地查報名名單（一行指令，2026-11-05）

起因：11/04 佩君老師問「7 月至今 KR 養生廚房的參加名單」，佩佩沒有現成指令，
      翻記憶檔、舊備份、日曆、官網猜場地花了 5 分鐘，傳 CSV 又試錯資料夾 4 分鐘。

用法：
  python3 ~/.openclaw/workspace/scripts/venue_signups.py "KR養生廚房" --since 2026-07-01
  （--until YYYY-MM-DD 可選；關鍵字比對場地／地區／地址／活動名稱）

輸出：
  ① 符合的場次與每場人數（含同行）  ② 場地「沒登記」的場次（照實講，不要猜）
  ③ CSV 直接寫進 ~/.openclaw/media/outbound/，message 傳檔用印出的路徑
"""
import argparse, csv, os, sqlite3, sys
from collections import defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    from registration_report import party_size
except Exception:
    def party_size(_):
        return 1, False, False

DB = os.path.expanduser("~/.openclaw/workspace/event-signup/event.db")
OUT = os.path.expanduser("~/.openclaw/media/outbound")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--since", default="2000-01-01")
    ap.add_argument("--until", default="2999-12-31")
    a = ap.parse_args()
    kw = a.keyword.strip().lower()

    c = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    c.row_factory = sqlite3.Row
    evs = c.execute("select * from events where event_date between ? and ? order by event_date",
                    (a.since, a.until)).fetchall()
    hit, unknown, cancelled = [], [], []
    for e in evs:
        blob = " ".join(str(e[k] or "") for k in ("venue", "location", "address", "name")).lower()
        if kw in blob:
            (cancelled if (e["status"] or "") == "cancelled" else hit).append(e)
        elif not (e["venue"] or "").strip() and (e["status"] or "") != "cancelled":
            unknown.append(e)

    rows, per = [], {}
    for e in hit:
        rs = c.execute("""select a.name, a.phone, a.company_title, a.email, s.created_at
                          from signups s join attendees a on a.id=s.attendee_id
                          where s.event_id=? order by s.created_at""", (e["id"],)).fetchall()
        people = 0
        for r in rs:
            n = party_size(r["company_title"])[0] or 1
            people += n
            rows.append([e["event_date"], e["slug"], e["name"], r["name"], r["phone"],
                         r["company_title"] or "", n, r["created_at"], r["email"] or ""])
        per[e["slug"]] = (len(rs), people)

    print("【%s】%s ～ %s" % (a.keyword, a.since, a.until))
    if not hit:
        print("資料庫裡沒有場地符合的場次。")
    for e in hit:
        n, p = per[e["slug"]]
        print("  %s %s｜%s｜報名 %d 筆、含同行 %d 人" % (e["event_date"], e["slug"], e["name"], n, p))
    if cancelled:
        print("已取消（不算）：" + "、".join("%s %s" % (e["event_date"], e["slug"]) for e in cancelled))
    if unknown:
        print("⚠️ 這幾場資料庫沒登記場地，可能也在這裡、也可能不是，回覆時照實說「場地未登記」，不要猜：")
        for e in unknown:
            print("  %s %s｜%s" % (e["event_date"], e["slug"], e["name"]))

    if rows:
        by_phone = defaultdict(set)
        for r in rows:
            by_phone[r[4]].add(r[0])
        repeat = sum(1 for v in by_phone.values() if len(v) > 1)
        print("合計 %d 筆、不重複 %d 人（看電話），參加超過一場的 %d 人" % (len(rows), len(by_phone), repeat))
        os.makedirs(OUT, exist_ok=True)
        fn = os.path.join(OUT, "場地名單_%s_%s.csv" % (a.keyword.replace("/", "_"), datetime.now().strftime("%Y%m%d%H%M%S")))
        with open(fn, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["場次日期", "場次代碼", "活動名稱", "姓名", "電話", "公司/職稱", "同行人數", "報名時間", "email"])
            w.writerows(rows)
        print("CSV（傳檔直接用這個路徑）：" + fn)


if __name__ == "__main__":
    main()
