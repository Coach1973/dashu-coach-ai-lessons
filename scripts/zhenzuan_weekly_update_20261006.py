#!/usr/bin/env python3
"""真鑽分會 2026-10-06 本週會議出席報告寫入（zhenzuan-guests，Mac 本機 SQLite）

來源：教練 2026-10-13 貼的「2026/10/06 本週會議出席報告」。
範本：~/github_repos/zhenzuan-guests/import_weekly_reports_2026-10-05.py（同一套：先核對人數、對不上就中止，整週覆蓋、重跑安全）。

報告：應到 47、準時 43、遲到 1（顏淳峯）、缺席 0、病假 0、代理 3（陳坤成、楊智帆、林宜宏）；來賓 0；早鳥 24 位。
應到 47 ＝ 在籍 48 扣掉 10/01 離會的柯朝陽（見 departed.py EXPLICIT_DEPARTED）。
代理人照 9/22 的算法：準時 43 不含代理，代理人寫成「present＋proxy=1」。

用法（Mac）：
  python3 scripts/zhenzuan_weekly_update_20261006.py --dry-run
  python3 scripts/zhenzuan_weekly_update_20261006.py
"""
import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.path.expanduser("~/github_repos/zhenzuan-guests/zhenzuan_guests.db")
WEEK = "2026-10-06"
WEEK_LABEL = "10/06"
EXPECTED_ACTIVE = 47
DEPARTED = ["柯朝陽"]          # 10/01 離會，報告應到 47 已扣掉他

LATE = ["顏淳峯"]
ABSENT = []
PROXY = ["陳坤成", "楊智帆", "林宜宏"]
GUESTS = []                    # 來賓 0

EARLY_BIRD = [
    "康文彬", "楊朝欽", "郭政輝", "洪嘉鴻", "蔡丞弘", "邱南寅", "陳淑玲", "羅琳", "黃智宏", "楊仁豪",
    "莊弼翔", "許朝竣", "陳建清", "陳逸凡", "周語薇", "林宜宏", "林仁超", "傅恩平", "古禹澤", "宋映璇",
    "張敬雍", "黃一恭", "伍芬群", "王靖雯",
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
        "SELECT id, name, left_chapter FROM members ORDER BY sort_order, id").fetchall()
    active = [m for m in members if m["left_chapter"] == 0 and m["name"] not in DEPARTED]
    by_name = {m["name"]: m["id"] for m in active}

    problems = []
    if len(active) != EXPECTED_ACTIVE:
        problems.append(f"在籍（扣掉離會）{len(active)} 位，報告應到是 {EXPECTED_ACTIVE} 位")
    for n in LATE + ABSENT + PROXY + EARLY_BIRD:
        if n not in by_name:
            problems.append(f"在籍會員裡找不到「{n}」")
    on_time = len(active) - len(LATE) - len(ABSENT) - len(PROXY)
    if on_time != 43:
        problems.append(f"準時人數 {on_time} ≠ 報告的 43")
    if len(EARLY_BIRD) != 24:
        problems.append(f"早鳥 {len(EARLY_BIRD)} ≠ 報告的 24")
    if problems:
        sys.exit("中止，沒有寫入任何東西：\n- " + "\n- ".join(problems))

    print(f"應到 {len(active)}：準時 {on_time}、遲到 {LATE}、缺席 {ABSENT}、代理 {PROXY}；早鳥 {len(EARLY_BIRD)}；來賓 0")
    if args.dry_run:
        print("--dry-run：到此為止，沒有寫入。")
        return

    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M}-before-{WEEK}"
    shutil.copy2(args.db, backup)
    print(f"已備份：{backup}")

    # 柯朝陽 10/01 離會：標成離會（之後在籍統計就不再算他）
    for name in DEPARTED:
        conn.execute("UPDATE members SET left_chapter = 1 WHERE name = ?", (name,))

    max_sort = conn.execute("SELECT COALESCE(MAX(sort_order), 0) FROM weeks").fetchone()[0]
    conn.execute(
        "INSERT INTO weeks (week_date, label, is_active, sort_order) VALUES (?, ?, 1, ?) "
        "ON CONFLICT(week_date) DO UPDATE SET is_active = 1",
        (WEEK, WEEK_LABEL, max_sort + 1),
    )
    for name, mid in by_name.items():
        att = "absent" if name in ABSENT else "late" if name in LATE else "present"
        conn.execute(
            "INSERT INTO weekly_data (member_id, week_date, guests, early_bird, attendance, proxy) "
            "VALUES (?, ?, 0, ?, ?, ?) "
            "ON CONFLICT(member_id, week_date) DO UPDATE SET guests = 0, early_bird = excluded.early_bird, "
            "attendance = excluded.attendance, proxy = excluded.proxy",
            (mid, WEEK, 1 if name in EARLY_BIRD else 0, att, 1 if name in PROXY and att == "present" else 0),
        )
    conn.execute("DELETE FROM guest_list WHERE week_date = ?", (WEEK,))
    conn.commit()

    row = conn.execute(
        "SELECT SUM(attendance='present'), SUM(attendance='late'), SUM(attendance='absent'), SUM(proxy), "
        "SUM(early_bird), SUM(guests) FROM weekly_data WHERE week_date = ?", (WEEK,)).fetchone()
    print("準時、遲到、缺席、代理（含在準時內）、早鳥、來賓 ＝", tuple(row))
    ok = row[0] == 46 and row[1] == 1 and row[2] == 0 and row[3] == 3 and row[4] == 24 and row[5] == 0
    print("✅ 寫入完成，數字與報告一致（準時 43＋代理 3＝46 出現在 present）" if ok else "⚠️ 數字與預期不一致，請檢查")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
