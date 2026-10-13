#!/usr/bin/env python3
"""真鑫分會 2026-10-01、2026-10-08 本週會議出席報告寫入（zhenxin-guests，Mac 本機 SQLite）

來源：教練 2026-10-13 貼的兩份「本週會議出席報告」（10/01、10/08）。
範本：zhenzuan_weekly_update_20261006.py（先核對人數、對不上就中止，整週覆蓋，重跑安全）。

人數規則（教練 2026-10-13 確認）：
- 張晴晴：9 月底離會，兩週都不在應到名單 → 標離會、不寫。
- 楊凱為：兩週都不在應到名單 → 不寫（在籍標記先不動，等教練回覆他是否離會）。
- 范郁琪、薛如媛：10/01 報告還列為缺席（那週仍是會員），10/08 已離會 → 只寫 10/01。
- 徐偉倫、黃鑫豊、買竣淯：兩週都有缺席記錄，照寫。

報告數字：
- 10/01：應到 17、準時 11、遲到 1（莊政川）、缺席 5（黃鑫豊、徐偉倫、買竣淯、范郁琪、薛如媛）、代理 0、來賓 0、早鳥 9
- 10/08：應到 15、準時 12、遲到 1（吳志煒）、缺席 2（黃鑫豊、徐偉倫）、代理 0、來賓 5、早鳥 7

用法（Mac）：
  python3 scripts/zhenxin_weekly_update_20261001_20261008.py --dry-run
  python3 scripts/zhenxin_weekly_update_20261001_20261008.py
"""
import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.path.expanduser("~/github_repos/zhenxin-guests/zhenxin_guests.db")

LEFT_BEFORE = ["張晴晴"]          # 9 月底離會：標離會
NOT_COUNTED = ["楊凱為"]           # 兩週都不在應到名單：不寫，在籍標記不動
EXTRA_TEN_01 = ["范郁琪", "薛如媛"]  # 10/01 仍在應到名單（報告列為缺席），現已標離會，只在 10/01 寫入

WEEKS = {
    "2026-10-01": dict(
        label="10/01", sort=26, expected=17,
        absent=["黃鑫豊", "徐偉倫", "買竣淯", "范郁琪", "薛如媛"], late=["莊政川"], proxy=[],
        guests=[], early=["吳志煒", "林尹渰", "王聖凱", "買駿航", "連皓宇", "吳亞平", "蔡姵彤", "買竣淯", "吳玫萱"],
        on_time=11, extra=EXTRA_TEN_01,
    ),
    "2026-10-08": dict(
        label="10/08", sort=27, expected=15,
        absent=["黃鑫豊", "徐偉倫"], late=["吳志煒"], proxy=[],
        guests=[("楊惠名", "吳亞平"), ("呂承璁", "吳亞平"), ("陳映妤", "吳亞平"),
                ("游雲喬", "林佳慧"), ("張伊婷", "吳玫萱")],
        early=["林尹渰", "王聖凱", "買駿航", "連皓宇", "蔡姵彤", "買竣淯", "吳玫萱"],
        on_time=12, extra=[],
    ),
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not os.path.exists(args.db):
        sys.exit(f"找不到資料庫：{args.db}")

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, name, left_chapter FROM members").fetchall()
    by_name = {r["name"]: r["id"] for r in rows}
    active = [r for r in rows if r["left_chapter"] == 0 and r["name"] not in LEFT_BEFORE + NOT_COUNTED]

    problems = []
    for n in LEFT_BEFORE + NOT_COUNTED + EXTRA_TEN_01:
        if n not in by_name:
            problems.append(f"資料庫找不到「{n}」")
    for week, w in WEEKS.items():
        names = w["absent"] + w["late"] + w["proxy"] + w["early"] + [i for _, i in w["guests"]]
        for n in names:
            if n not in by_name:
                problems.append(f"{week}：「{n}」不在資料庫")
        in_week = {r["name"] for r in active} | set(w["extra"])
        for n in w["absent"] + w["late"] + w["proxy"]:
            if n not in in_week:
                problems.append(f"{week}：「{n}」不在當週應到名單")
        total = len(active) + len(w["extra"])
        if total != w["expected"]:
            problems.append(f"{week}：應到 {total} ≠ 報告 {w['expected']}")
        on_time = total - len(w["absent"]) - len(w["late"]) - len(w["proxy"])
        if on_time != w["on_time"]:
            problems.append(f"{week}：準時 {on_time} ≠ 報告 {w['on_time']}")
        if len(w["early"]) != {"2026-10-01": 9, "2026-10-08": 7}[week]:
            problems.append(f"{week}：早鳥人數不符")
    if problems:
        sys.exit("中止，沒有寫入任何東西：\n- " + "\n- ".join(problems))

    for week, w in WEEKS.items():
        print(f"{week}：應到 {w['expected']}（在籍 {len(active)}" + (f"＋{len(w['extra'])} 位已離會" if w["extra"] else "") +
              f"）；準時 {w['on_time']}、遲到 {w['late']}、缺席 {w['absent']}；早鳥 {len(w['early'])}；來賓 {len(w['guests'])}")
    if args.dry_run:
        print("--dry-run：到此為止，沒有寫入。")
        return

    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M}-before-2026-10-01-08"
    shutil.copy2(args.db, backup)
    print(f"已備份：{backup}")

    for n in LEFT_BEFORE:
        conn.execute("UPDATE members SET left_chapter = 1 WHERE name = ?", (n,))

    for week, w in WEEKS.items():
        conn.execute(
            "INSERT INTO weeks (week_date, label, is_active, sort_order) VALUES (?, ?, 1, ?) "
            "ON CONFLICT(week_date) DO UPDATE SET is_active = 1, label = excluded.label",
            (week, w["label"], w["sort"]),
        )
        conn.execute("DELETE FROM weekly_data WHERE week_date = ?", (week,))
        conn.execute("DELETE FROM guest_list WHERE week_date = ?", (week,))
        guests_per = {}
        for _, inviter in w["guests"]:
            guests_per[inviter] = guests_per.get(inviter, 0) + 1
        week_members = active + [r for r in rows if r["name"] in w["extra"]]
        for r in week_members:
            name = r["name"]
            att = "absent" if name in w["absent"] else "late" if name in w["late"] else "present"
            conn.execute(
                "INSERT INTO weekly_data (member_id, week_date, guests, early_bird, attendance, proxy) "
                "VALUES (?, ?, ?, ?, ?, 0)",
                (r["id"], week, guests_per.get(name, 0), 1 if name in w["early"] else 0, att),
            )
        for name, inviter in w["guests"]:
            conn.execute("INSERT INTO guest_list (week_date, name, profession, inviter) VALUES (?, ?, NULL, ?)",
                         (week, name, inviter))
    conn.commit()

    for week, w in WEEKS.items():
        row = conn.execute(
            "SELECT SUM(attendance='present'), SUM(attendance='late'), SUM(attendance='absent'), "
            "SUM(early_bird), SUM(guests) FROM weekly_data WHERE week_date = ?", (week,)).fetchone()
        print(week, "準時／遲到／缺席／早鳥／來賓 ＝", tuple(row))
        exp = (w["on_time"], len(w["late"]), len(w["absent"]), len(w["early"]), len(w["guests"]))
        got = (row[0], row[1], row[2], row[3], row[4])
        if got != exp:
            print("⚠️ 與報告不一致：預期", exp, "實際", got)
            sys.exit(1)
    print("✅ 兩週寫入完成，數字與報告一致")


if __name__ == "__main__":
    main()
