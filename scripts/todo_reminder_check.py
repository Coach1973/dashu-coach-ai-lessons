#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹教練待辦事項到期提醒（2026-09-02教練交辦，仿Microsoft To Do主動提醒）

比照 bni_credit_expiry_reminder.py 同款設計：檢查 event-signup/event.db 的
todos 表，remind_at 時間已到、尚未完成、尚未通知過的項目，組成一則訊息
透過 notify_coach.sh 送出，成功才寫回 reminder_sent，避免送達失敗卻誤記已通知。

用法：
  python3 scripts/todo_reminder_check.py           # 檢查並通知
  python3 scripts/todo_reminder_check.py --dry-run # 只印出結果，不通知不寫回

建議註冊為 OpenClaw cron，每 15 分鐘跑一次。
"""

import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = Path(__file__).resolve().parent.parent / "event-signup" / "event.db"
NOTIFY_SCRIPT = Path(__file__).resolve().parent / "notify_coach.sh"


def find_due(conn):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return conn.execute(
        """
        SELECT id, title, notes, due_date, remind_at FROM todos
        WHERE completed = 0 AND reminder_sent = 0
          AND remind_at IS NOT NULL AND remind_at != '' AND remind_at <= ?
        ORDER BY remind_at ASC
        """,
        (now,),
    ).fetchall()


def compose_message(rows):
    lines = [f"⏰ {len(rows)}件待辦事項提醒時間到了："]
    for r in rows:
        due_note = f"（到期：{r['due_date']}）" if r["due_date"] else ""
        lines.append(f"・{r['title']}{due_note}")
        if r["notes"]:
            lines.append(f"　備註：{r['notes']}")
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = find_due(conn)

    if not rows:
        print("目前沒有到時間且尚未通知過的待辦事項。")
        conn.close()
        return

    msg = compose_message(rows)
    print(msg)

    if dry_run:
        print("\n（--dry-run，未實際發送通知，也未寫回reminder_sent）")
        conn.close()
        return

    result = subprocess.run(["bash", str(NOTIFY_SCRIPT), msg], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 通知發送失敗（rc={result.returncode}），reminder_sent不寫回，下次會重試：{result.stderr}")
        conn.close()
        sys.exit(1)

    conn.executemany(
        "UPDATE todos SET reminder_sent = 1 WHERE id = ?",
        [(r["id"],) for r in rows],
    )
    conn.commit()
    conn.close()
    print(f"\n✅ 已通知教練，共{len(rows)}筆reminder_sent已寫回。")


if __name__ == "__main__":
    main()
