#!/usr/bin/env python3
"""真誠分會 2026-10-08 例會資料寫入（sincere.bymyway.com，Mac 本機 SQLite）

來源：教練 2026-10-13 貼的「2026/10/08-補紀錄 真誠例會出席報告」。
範本：sincere_weekly_update_20261001.py（同一套：先核對人數、對不上就中止，重跑不重複、不洗掉會員自填的 121／咖啡）。

報告：應到 15、準時 14、遲到 1（黃秀麗）、缺席 0、病假 0、代理 0；來賓 5 位，邀約人都是陳佩君。
早鳥：報告寫「［禮昂未截圖］」且沒有名單，所以早鳥欄位不寫（留 NULL），不猜。

用法（Mac）：
  python3 scripts/sincere_weekly_update_20261008.py --dry-run   # 先看會做什麼，不寫入
  python3 scripts/sincere_weekly_update_20261008.py             # 正式寫入（會先備份資料庫）
"""
import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.path.expanduser("~/github_repos/zhencheng-guests/zhencheng_guests.db")
WEEK = "2026-10-08"
WEEK_LABEL = "10/08"

EXPECTED_ACTIVE = 15          # 應到 15（在籍 15 位，全部納入）
LATE = ["黃秀麗"]              # 遲到 1
ABSENT = []                    # 缺席 0
PROXY = []                     # 代理 0

# 來賓（姓名, 專業別, 邀約人）
GUESTS = [
    ("許晏寧", "頭皮紋髮教學", "陳佩君"),
    ("孫林宏証", "教育諮詢顧問", "陳佩君"),
    ("張麗雲", "作曲編曲愛好者", "陳佩君"),
    ("宋美齡", "旅遊團購", "陳佩君"),
    ("王奎嵐", "AI導入顧問", "陳佩君"),
]


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
    members = conn.execute(
        "SELECT id, name FROM members WHERE left_chapter = 0 ORDER BY sort_order, id"
    ).fetchall()
    by_name = {m["name"]: m["id"] for m in members}

    problems = []
    if len(members) != EXPECTED_ACTIVE:
        problems.append(f"在籍會員 {len(members)} 位，報告應到是 {EXPECTED_ACTIVE} 位")
    for n in LATE + ABSENT + PROXY + [g[2] for g in GUESTS]:
        if n not in by_name:
            problems.append(f"在籍會員裡找不到「{n}」")
    on_time = len(members) - len(LATE) - len(ABSENT) - len(PROXY)
    if on_time != 14:   # 報告：準時 14、遲到 1、缺席 0、代理 0，合計應到 15
        problems.append(f"準時人數 {on_time} ≠ 報告的 14")
    if problems:
        sys.exit("中止，沒有寫入任何東西：\n- " + "\n- ".join(problems))

    guests_per_member = {}
    for _, _, inviter in GUESTS:
        guests_per_member[inviter] = guests_per_member.get(inviter, 0) + 1

    print(f"在籍 {len(members)} 位：準時 {len(members) - len(LATE) - len(ABSENT) - len(PROXY)}、遲到 {LATE}、缺席 {ABSENT}、代理 {PROXY}；"
          f"早鳥：不寫（報告未提供）；來賓 {len(GUESTS)} 位 {guests_per_member}")
    if args.dry_run:
        print("--dry-run：到此為止，沒有寫入。")
        return

    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M}-before-{WEEK}"
    shutil.copy2(args.db, backup)
    print(f"已備份：{backup}")

    max_sort = conn.execute("SELECT COALESCE(MAX(sort_order), 0) FROM weeks").fetchone()[0]
    conn.execute(
        "INSERT OR IGNORE INTO weeks (week_date, label, is_active, note, sort_order) VALUES (?, ?, 1, NULL, ?)",
        (WEEK, WEEK_LABEL, max_sort + 1),
    )

    for m in members:
        name, mid = m["name"], m["id"]
        att = "absent" if name in ABSENT else "late" if name in LATE else "present"
        conn.execute(
            "INSERT INTO weekly_data (member_id, week_date, guests, early_bird, attendance, proxy) "
            "VALUES (?, ?, ?, NULL, ?, 0) "
            "ON CONFLICT(member_id, week_date) DO UPDATE SET "
            "guests = excluded.guests, attendance = excluded.attendance, proxy = excluded.proxy",
            (mid, WEEK, guests_per_member.get(name, 0), att),
        )

    conn.execute("DELETE FROM guest_list WHERE week_date = ?", (WEEK,))
    for g_name, profession, inviter in GUESTS:
        conn.execute(
            "INSERT INTO guest_list (week_date, name, profession, inviter) VALUES (?, ?, ?, ?)",
            (WEEK, g_name, profession, inviter),
        )
    conn.commit()

    n_present = conn.execute(
        "SELECT COUNT(*) FROM weekly_data WHERE week_date = ? AND attendance = 'present'", (WEEK,)).fetchone()[0]
    n_late = conn.execute(
        "SELECT COUNT(*) FROM weekly_data WHERE week_date = ? AND attendance = 'late'", (WEEK,)).fetchone()[0]
    n_guest = conn.execute(
        "SELECT COALESCE(SUM(guests), 0) FROM weekly_data WHERE week_date = ?", (WEEK,)).fetchone()[0]
    n_list = conn.execute("SELECT COUNT(*) FROM guest_list WHERE week_date = ?", (WEEK,)).fetchone()[0]
    print(f"準時 {n_present}／遲到 {n_late}／來賓人數合計 {n_guest}／來賓名單 {n_list} 筆")
    ok = n_present == 14 and n_late == 1 and n_guest == len(GUESTS) and n_list == len(GUESTS)
    print("✅ 寫入完成，數字與報告一致" if ok else "⚠️ 數字與預期不一致，請檢查")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
