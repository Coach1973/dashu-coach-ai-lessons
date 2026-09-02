#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹教練待辦事項到期提醒（2026-09-02教練交辦，仿Microsoft To Do主動提醒）

事件觸發設計（2026-09-02守則#07 Stop hook攔下輪詢版本後改版）：新增待辦時
若填了remind_at，app.py會當場註冊一個「精確時間點」的OpenClaw一次性cron
（`openclaw cron create --at <remind_at>`），時間一到才觸發本腳本檢查
「這一筆」待辦事項，不是每隔幾分鐘重複掃描整張表。完成或刪除待辦時
app.py會同步取消尚未觸發的cron，避免多餘通知。

用法：
  python3 scripts/todo_reminder_check.py --todo-id 5   # 一次性cron觸發時用，只查這一筆
  python3 scripts/todo_reminder_check.py --sweep [--dry-run]  # 手動補漏用，掃全表到期未通知項目
"""

import argparse
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = Path(__file__).resolve().parent.parent / "event-signup" / "event.db"
NOTIFY_SCRIPT = Path(__file__).resolve().parent / "notify_coach.sh"


def find_one(conn, todo_id):
    return conn.execute(
        "SELECT id, title, notes, due_date, remind_at FROM todos "
        "WHERE id = ? AND completed = 0 AND reminder_sent = 0",
        (todo_id,),
    ).fetchone()


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


def notify_and_mark(conn, rows, dry_run):
    if not rows:
        print("這筆待辦已不存在、已完成，或已經通知過，跳過。")
        return

    msg = compose_message(rows)
    print(msg)

    if dry_run:
        print("\n（--dry-run，未實際發送通知，也未寫回reminder_sent）")
        return

    result = subprocess.run(["bash", str(NOTIFY_SCRIPT), msg], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 通知發送失敗（rc={result.returncode}），reminder_sent不寫回：{result.stderr}")
        sys.exit(1)

    conn.executemany(
        "UPDATE todos SET reminder_sent = 1 WHERE id = ?",
        [(r["id"],) for r in rows],
    )
    conn.commit()
    print(f"\n✅ 已通知教練，共{len(rows)}筆reminder_sent已寫回。")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--todo-id", type=int, help="只檢查/通知這一筆待辦（一次性cron觸發時用）")
    parser.add_argument("--sweep", action="store_true", help="手動補漏：掃全表到期未通知項目")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if args.todo_id is not None:
        row = find_one(conn, args.todo_id)
        rows = [row] if row else []
    elif args.sweep:
        rows = find_due(conn)
    else:
        parser.error("需要指定 --todo-id N 或 --sweep 其中之一")
        return

    notify_and_mark(conn, rows, args.dry_run)
    conn.close()


if __name__ == "__main__":
    main()
