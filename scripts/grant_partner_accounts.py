#!/usr/bin/env python3
"""一次開好夥伴的兩組後台帳號（2026-09-30 教練交辦：怡靜）。

1. team.bymyway.com 總管理後台（/admin，可管第一～第五分會）
2. namecard.bymyway.com 名片系統團隊帳號（等同走 /apply 申請，教練直接批准）

帳號都是手機號碼，密碼都是 88888（兩套系統原本的預設密碼）。
用法：python3 grant_partner_accounts.py --phone 0912345678 --name 陳怡靜
測試：加 --team-db / --namecard-db 指向複本，不動正式資料庫。
"""
import argparse
import re
import sqlite3
import sys
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

PASSWORD = "88888"
TEAM_DB = Path.home() / "github_repos" / "team-bymyway" / "team.db"
NAMECARD_DB = Path.home() / ".openclaw" / "workspace" / "namecard-db" / "namecards.db"


def grant_team_super_admin(db_path, phone):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT id FROM admins WHERE username = ? AND chapter_id IS NULL", (phone,)
    ).fetchone()
    pw_hash = generate_password_hash(PASSWORD)
    if row:
        conn.execute("UPDATE admins SET password_hash = ? WHERE id = ?", (pw_hash, row[0]))
    else:
        conn.execute(
            "INSERT INTO admins (username, password_hash, chapter_id) VALUES (?, ?, NULL)",
            (phone, pw_hash),
        )
    conn.commit()
    check = conn.execute(
        "SELECT password_hash FROM admins WHERE username = ? AND chapter_id IS NULL", (phone,)
    ).fetchone()
    conn.close()
    return check is not None and check_password_hash(check[0], PASSWORD)


def grant_namecard_member(db_path, phone, name):
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT id FROM team_members WHERE username = ?", (phone,)).fetchone()
    pw_hash = generate_password_hash(PASSWORD)
    if row:
        conn.execute(
            "UPDATE team_members SET password_hash = ?, display_name = ?, status = 'approved' WHERE id = ?",
            (pw_hash, name, row[0]),
        )
    else:
        conn.execute(
            "INSERT INTO team_members (username, password_hash, display_name, status, applied_at)"
            " VALUES (?, ?, ?, 'approved', datetime('now','localtime'))",
            (phone, pw_hash, name),
        )
    conn.commit()
    check = conn.execute(
        "SELECT password_hash, status FROM team_members WHERE username = ?", (phone,)
    ).fetchone()
    conn.close()
    return check is not None and check[1] == "approved" and check_password_hash(check[0], PASSWORD)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phone", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--team-db", default=str(TEAM_DB))
    ap.add_argument("--namecard-db", default=str(NAMECARD_DB))
    args = ap.parse_args()

    phone = re.sub(r"\D", "", args.phone)
    if not re.fullmatch(r"09\d{8}", phone):
        sys.exit(f"手機號碼格式不對：{args.phone}（要 09 開頭 10 碼）")

    ok_team = grant_team_super_admin(args.team_db, phone)
    ok_card = grant_namecard_member(args.namecard_db, phone, args.name)
    print(f"team.bymyway.com/admin 總管理（第一～第五分會）：{'✅' if ok_team else '❌'} 帳號 {phone}")
    print(f"namecard.bymyway.com 名片系統（已批准）：{'✅' if ok_card else '❌'} 帳號 {phone}")
    print(f"密碼都是 {PASSWORD}")
    sys.exit(0 if ok_team and ok_card else 1)


if __name__ == "__main__":
    main()
