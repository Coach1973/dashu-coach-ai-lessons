#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""報名通知空窗期稽核（2026-08-26 教練當場糾正後建置）

起因：教練問「金門場報名資料跟我們得知的有落差」，一路追問三次才查出：
8/17~8/24 03:11（Telegram通知群組上線前）這段時間LINE額度早已用完靜默
失敗，這段期間報名的人幾乎沒收到即時通知。教練從金門回來後才被告知
完整名單，痛批「這是很嚴重的失職——早知道還可以打電話問他們到底有
沒有來，現在資料再給也沒用了」。

這支腳本要做的事：以後不會再有人需要「追問三次」才問到完整答案——
只要某場活動還沒開始（event_date >= 今天），就自動列出裡面有沒有
「NOTIFY_CUTOFF之前報名、當下極可能沒收到即時通知」的人，讓教練在
活動開始前就知道，而不是活動結束、人都回來了才知道。

用法：
  python3 scripts/registration_notify_gap_check.py           # 列出所有尚未開始場次的空窗期報名
  python3 scripts/registration_notify_gap_check.py --notify  # 有發現才發Telegram（節流24小時）
"""

import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
EVENT_DB = os.path.join(WORKSPACE, "event-signup", "event.db")
NOTIFY_SCRIPT = os.path.join(WORKSPACE, "scripts", "notify_coach.sh")
TPE = timezone(timedelta(hours=8))

# 2026-08-24 03:11:39：commit c5871e7dc「報名通知改推Telegram群組」上線的確切時刻。
# 在這之前，唯一通知管道是LINE，而LINE當時額度已用完、靜默失敗（無報錯）。
# 這個時間點寫死在這裡，是「已知修復過的那一次」空窗期；未來若再發生新的
# 通知管道故障，需要另外查證那次故障的起訖時間，不能假設全部都套用這個值。
NOTIFY_CUTOFF = datetime(2026, 8, 24, 3, 11, 39, tzinfo=TPE)


def conn():
    c = sqlite3.connect(EVENT_DB)
    c.row_factory = sqlite3.Row
    return c


def today_str():
    return datetime.now(TPE).strftime("%Y-%m-%d")


def find_gaps(c):
    events = c.execute(
        "SELECT id, name, event_date, start_time, location FROM events "
        "WHERE event_date >= ? AND status = 'active' ORDER BY event_date, start_time",
        (today_str(),),
    ).fetchall()

    results = []
    for e in events:
        rows = c.execute(
            """
            SELECT a.name, a.phone, s.created_at
            FROM signups s JOIN attendees a ON a.id = s.attendee_id
            WHERE s.event_id = ?
            ORDER BY s.created_at
            """,
            (e["id"],),
        ).fetchall()
        gap_people = []
        for r in rows:
            created = datetime.fromisoformat(r["created_at"]).replace(tzinfo=TPE)
            if created < NOTIFY_CUTOFF:
                gap_people.append((r["name"], r["phone"], r["created_at"]))
        if gap_people:
            results.append((e, gap_people))
    return results


def format_report(results):
    if not results:
        return "查了所有尚未開始的場次，沒有發現任何『報名時通知管道已知故障』的空窗期報名。"
    lines = ["🔴 以下尚未開始的場次，有報名者落在已知的Telegram通知空窗期（8/17~8/24 03:11，當時LINE額度用完靜默失敗），極可能從未收到即時通知："]
    for e, people in results:
        lines.append(f"\n【{e['name']}】{e['event_date']} {e['start_time']} {e['location']}（共{len(people)}位落在空窗期）")
        for name, phone, created in people:
            lines.append(f"  - {name} / {phone}（{created}報名）")
    return "\n".join(lines)


def main():
    c = conn()
    results = find_gaps(c)
    report = format_report(results)
    print(report)

    if "--notify" in sys.argv and results:
        subprocess.run(
            [NOTIFY_SCRIPT, report, "86400", "registration_notify_gap_check"],
            check=False,
        )


if __name__ == "__main__":
    main()
