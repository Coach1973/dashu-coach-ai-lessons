#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BNI信用証到期提醒（教練 2026-08-28 交辦）

教練原話：「如果有會員即將在一個月內到期，你要透過電報給我發通知。」

只認 usage_status='active'（有效未使用）且到期日在未來30天內（含當天，
不含已逾期）的記錄。每筆只通知一次——寫回 reminder_sent_at 後，之後重跑
不會重複發送同一筆，避免教練每天被同一批人洗版。

用法：
  python3 scripts/bni_credit_expiry_reminder.py         # 檢查並通知
  python3 scripts/bni_credit_expiry_reminder.py --dry-run  # 只印出結果，不通知不寫回
"""

import sqlite3
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "namecard-db" / "namecards.db"
NOTIFY_SCRIPT = Path(__file__).resolve().parent / "notify_coach.sh"
WINDOW_DAYS = 30


def find_due_soon(conn):
    rows = conn.execute(
        """
        SELECT id, bni_member_id, name, chapter, company, expiry_date
        FROM bni_credit_certificates
        WHERE cert_status = 'issued' AND usage_status = 'active'
          AND expiry_date IS NOT NULL AND expiry_date != ''
          AND reminder_sent_at IS NULL
        """
    ).fetchall()

    today = date.today()
    due = []
    for r in rows:
        try:
            y, m, d = (int(x) for x in r["expiry_date"].split("-"))
        except ValueError:
            continue
        remaining_days = (date(y, m, d) - today).days
        if 0 <= remaining_days <= WINDOW_DAYS:
            due.append({**dict(r), "remaining_days": remaining_days})
    due.sort(key=lambda x: x["remaining_days"])
    return due


def compose_message(due):
    lines = [f"🔔 {len(due)}位BNI會員的信用証將在{WINDOW_DAYS}天內到期："]
    for r in due:
        company = f"（{r['company']}）" if r["company"] else ""
        lines.append(
            f"・{r['chapter']} {r['name']}{company} — 剩{r['remaining_days']}天，到期日{r['expiry_date']}"
        )
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    due = find_due_soon(conn)

    if not due:
        print("目前沒有30天內到期且尚未通知過的信用証。")
        conn.close()
        return

    msg = compose_message(due)
    print(msg)

    if dry_run:
        print("\n（--dry-run，未實際發送通知，也未寫回reminder_sent_at）")
        conn.close()
        return

    result = subprocess.run(["bash", str(NOTIFY_SCRIPT), msg], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 通知發送失敗（rc={result.returncode}），reminder_sent_at不寫回，下次會重試：{result.stderr}")
        conn.close()
        sys.exit(1)

    now = datetime.now().isoformat(timespec="seconds")
    ids = [r["id"] for r in due]
    conn.executemany(
        "UPDATE bni_credit_certificates SET reminder_sent_at = ? WHERE id = ?",
        [(now, i) for i in ids],
    )
    conn.commit()
    conn.close()
    print(f"\n✅ 已通知教練，{len(due)}筆記錄reminder_sent_at已寫回。")


if __name__ == "__main__":
    main()
