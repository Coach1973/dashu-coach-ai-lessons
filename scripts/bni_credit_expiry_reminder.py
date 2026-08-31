#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BNI信用証到期提醒（教練 2026-08-28 交辦；2026-09-01 教練追加「2個月及1個月都要通知」擴充為兩段式）

教練原話（2026-08-28）：「如果有會員即將在一個月內到期，你要透過電報給我發通知。」
教練原話（2026-09-01）：「信用証，當會員只剩2個月及1個月到期時，要記得通知我。」

只認 usage_status='active'（有效未使用）且到期日在未來的記錄，分兩段各通知一次：
- 剩餘 31~60 天（約2個月內）→ 寫回 reminder_60d_sent_at，之後不會為同一個里程碑重複通知
- 剩餘 0~30 天（約1個月內）→ 寫回 reminder_sent_at（沿用舊欄位，語意等同「30天提醒已發」）
同一筆證書會各收到一次「2個月」跟一次「1個月」通知，兩者互不影響、不會重複洗版同一個里程碑。

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
WINDOW_1M_DAYS = 30
WINDOW_2M_DAYS = 60


def _fetch_candidates(conn, sent_column):
    return conn.execute(
        f"""
        SELECT id, bni_member_id, name, chapter, company, expiry_date
        FROM bni_credit_certificates
        WHERE cert_status = 'issued' AND usage_status = 'active'
          AND expiry_date IS NOT NULL AND expiry_date != ''
          AND {sent_column} IS NULL
        """
    ).fetchall()


def _with_remaining_days(rows):
    today = date.today()
    out = []
    for r in rows:
        try:
            y, m, d = (int(x) for x in r["expiry_date"].split("-"))
        except ValueError:
            continue
        out.append({**dict(r), "remaining_days": (date(y, m, d) - today).days})
    return out


def find_due_soon(conn):
    """回傳 (due_1m, due_2m)：due_1m=剩0~30天且尚未發過1個月提醒；due_2m=剩31~60天且尚未發過2個月提醒。"""
    due_1m = [
        r for r in _with_remaining_days(_fetch_candidates(conn, "reminder_sent_at"))
        if 0 <= r["remaining_days"] <= WINDOW_1M_DAYS
    ]
    due_2m = [
        r for r in _with_remaining_days(_fetch_candidates(conn, "reminder_60d_sent_at"))
        if WINDOW_1M_DAYS < r["remaining_days"] <= WINDOW_2M_DAYS
    ]
    due_1m.sort(key=lambda x: x["remaining_days"])
    due_2m.sort(key=lambda x: x["remaining_days"])
    return due_1m, due_2m


def compose_message(due_1m, due_2m):
    lines = []
    if due_2m:
        lines.append(f"🔔 {len(due_2m)}位BNI會員的信用証將在2個月內到期：")
        for r in due_2m:
            company = f"（{r['company']}）" if r["company"] else ""
            lines.append(
                f"・{r['chapter']} {r['name']}{company} — 剩{r['remaining_days']}天，到期日{r['expiry_date']}"
            )
    if due_1m:
        if lines:
            lines.append("")
        lines.append(f"🔴 {len(due_1m)}位BNI會員的信用証將在1個月內到期：")
        for r in due_1m:
            company = f"（{r['company']}）" if r["company"] else ""
            lines.append(
                f"・{r['chapter']} {r['name']}{company} — 剩{r['remaining_days']}天，到期日{r['expiry_date']}"
            )
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    due_1m, due_2m = find_due_soon(conn)

    if not due_1m and not due_2m:
        print("目前沒有2個月或1個月內到期且尚未通知過該里程碑的信用証。")
        conn.close()
        return

    msg = compose_message(due_1m, due_2m)
    print(msg)

    if dry_run:
        print("\n（--dry-run，未實際發送通知，也未寫回reminder欄位）")
        conn.close()
        return

    result = subprocess.run(["bash", str(NOTIFY_SCRIPT), msg], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 通知發送失敗（rc={result.returncode}），reminder欄位不寫回，下次會重試：{result.stderr}")
        conn.close()
        sys.exit(1)

    now = datetime.now().isoformat(timespec="seconds")
    if due_1m:
        conn.executemany(
            "UPDATE bni_credit_certificates SET reminder_sent_at = ? WHERE id = ?",
            [(now, r["id"]) for r in due_1m],
        )
    if due_2m:
        conn.executemany(
            "UPDATE bni_credit_certificates SET reminder_60d_sent_at = ? WHERE id = ?",
            [(now, r["id"]) for r in due_2m],
        )
    conn.commit()
    conn.close()
    print(f"\n✅ 已通知教練，2個月提醒{len(due_2m)}筆、1個月提醒{len(due_1m)}筆reminder欄位已寫回。")


if __name__ == "__main__":
    main()
