#!/usr/bin/env python3
"""真誠分會 2026-10-01 例會資料寫入（sincere.bymyway.com，Mac 本機 SQLite）

來源：教練 2026-10-05 21:57 在聯想貼的「真誠例會出席報告」。
聯想連不到 Mac 的資料庫，所以寫成一支可重複執行的腳本，由 Mac 軍師在 Mac 上跑。
全部用 UPSERT／存在才跳過，重跑不會重複、不會洗掉會員自填的 121／咖啡。

用法（Mac）：
  python3 scripts/sincere_weekly_update_20261001.py --dry-run   # 先看會做什麼，不寫入
  python3 scripts/sincere_weekly_update_20261001.py             # 正式寫入（會先備份資料庫）
  python3 scripts/sincere_weekly_update_20261001.py --db /路徑/zhencheng_guests.db
"""
import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.path.expanduser("~/github_repos/zhencheng-guests/zhencheng_guests.db")
WEEK = "2026-10-01"
WEEK_LABEL = "10/01"

# 報告：應到 15、準時 15、缺席／遲到／病假／代理 0 → 目前在籍會員全部「出席」、無代理人
EXPECTED_ACTIVE = 15

# 早鳥 10 位
EARLY_BIRD = ["王彤", "李美花", "陳佩君", "鄭綉美", "張羽家", "張玉盞", "郭展鴻", "張育慈", "林佳伶", "楊在珍"]

# 來賓（姓名, 專業別, 邀約人）。報告寫邀約人「Lavi」＝林佳伶，照名單慣例寫會員中文名。
GUESTS = [
    ("林杰慷", "職涯策略顧問", "林佳伶"),
    ("江宜倫", "敏感肌保養", "陳佩君"),
    ("李晴", "音樂機構負責人", "陳佩君"),
    ("湯凡逸", "創作型小提琴家", "陳佩君"),
    ("湯琪", "編織藝品", "楊在珍"),
    ("朱振順", "國順汽車修護", "楊在珍"),
    ("呂官諭", "定昌洗染", "楊在珍"),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 主控台預設 cp950，印不出 ✅
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
    for n in EARLY_BIRD + [g[2] for g in GUESTS]:
        if n not in by_name:
            problems.append(f"在籍會員裡找不到「{n}」")
    if problems:
        sys.exit("中止，沒有寫入任何東西：\n- " + "\n- ".join(problems))

    guests_per_member = {}
    for _, _, inviter in GUESTS:
        guests_per_member[inviter] = guests_per_member.get(inviter, 0) + 1

    print(f"在籍 {len(members)} 位全部記「出席」、無代理人；早鳥 {len(EARLY_BIRD)} 位；來賓 {len(GUESTS)} 位 {guests_per_member}")
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
        conn.execute(
            "INSERT INTO weekly_data (member_id, week_date, guests, early_bird, attendance, proxy) "
            "VALUES (?, ?, ?, ?, 'present', 0) "
            "ON CONFLICT(member_id, week_date) DO UPDATE SET "
            "guests = excluded.guests, early_bird = excluded.early_bird, "
            "attendance = excluded.attendance, proxy = excluded.proxy",
            (mid, WEEK, guests_per_member.get(name, 0), 1 if name in EARLY_BIRD else 0),
        )

    added = 0
    for g_name, profession, inviter in GUESTS:
        exists = conn.execute(
            "SELECT 1 FROM guest_list WHERE week_date = ? AND name = ?", (WEEK, g_name)
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO guest_list (week_date, name, profession, inviter) VALUES (?, ?, ?, ?)",
                (WEEK, g_name, profession, inviter),
            )
            added += 1
    conn.commit()

    w = conn.execute("SELECT * FROM weeks WHERE week_date = ?", (WEEK,)).fetchone()
    n_att = conn.execute(
        "SELECT COUNT(*) FROM weekly_data WHERE week_date = ? AND attendance = 'present'", (WEEK,)
    ).fetchone()[0]
    n_eb = conn.execute(
        "SELECT COUNT(*) FROM weekly_data WHERE week_date = ? AND early_bird = 1", (WEEK,)
    ).fetchone()[0]
    n_guest = conn.execute(
        "SELECT COALESCE(SUM(guests), 0) FROM weekly_data WHERE week_date = ?", (WEEK,)
    ).fetchone()[0]
    n_list = conn.execute("SELECT COUNT(*) FROM guest_list WHERE week_date = ?", (WEEK,)).fetchone()[0]
    print(f"weeks：{dict(w)}")
    print(f"出席 {n_att}／早鳥 {n_eb}／來賓人數合計 {n_guest}／來賓名單 {n_list} 筆（本次新增 {added}）")
    ok = n_att == EXPECTED_ACTIVE and n_eb == len(EARLY_BIRD) and n_guest == len(GUESTS) and n_list == len(GUESTS)
    print("✅ 寫入完成，數字與報告一致" if ok else "⚠️ 數字與預期不一致，請檢查")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
