#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""活動前一天提醒教練名單（2026-08-27教練交辦）

背景：學員反映報名後想在活動前收到提醒，但LINE官方帳號後台主動推播
（Push API）每月只有200則免費額度，超過要收費。教練的解法：不由AI/系統
自動群發，改成——活動前一天，AI把「誰報名了」的名單告訴教練，教練自己
到LINE@後台用「回覆訊息」逐一私訊提醒（LINE官方帳號對談框裡的1對1回覆
不算進推播額度，跟Push API是兩種不同計費）。

這支腳本負責的就是「AI告訴教練名單」這一步，教練後續怎麼在LINE@後台
發送不歸這支腳本管。

刻意重用 registration_report.py 既有的 roster()/_legacy_rows()/notify()，
不重新發明一套比對邏輯——那支腳本的同日多場次比對、MM/DD vs 0M/0D格式
不一致等坑都已經踩過修好，這裡直接借用才不會重蹈覆轍。

用法：
  python3 scripts/event_reminder_day_before.py           # 檢查明天有沒有場次，有就發Telegram名單
  python3 scripts/event_reminder_day_before.py --dry-run # 只印出來，不發Telegram(除錯用)

建議排程：每天早上一個固定時間跑一次（例如09:00），檢查「明天」有沒有場次。
一天只需要問一次「明天有沒有活動」，不是輪詢盯著看狀態變化。
"""
import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))
import registration_report as rr  # noqa: E402

TPE = timezone(timedelta(hours=8))


def tomorrow_str() -> str:
    return (datetime.now(TPE) + timedelta(days=1)).strftime("%Y-%m-%d")


def fetch_tomorrow_events(c):
    d = tomorrow_str()
    # 2026-10-07教練抓到：10/7、10/8已取消（status=cancelled）卻照樣每天提醒，取消的場次不提醒
    return [e for e in rr.fetch_events(c, include_past=True)
            if e["event_date"] == d and e.get("status") != "cancelled"]


def build_message(c, events) -> str:
    all_events = rr.fetch_events(c, include_past=True)
    legacy_all = rr._legacy_rows(c)
    by_date = {}
    for e in all_events:
        by_date.setdefault(e["event_date"], []).append(e)

    lines = ["📋 明天有活動，這是目前的報名名單（請到LINE@後台逐一私訊提醒，回覆訊息不會扣推播額度）：\n"]
    for ev in events:
        live, legacy, unassigned = rr.roster(c, ev, legacy_all, by_date.get(ev["event_date"], []))
        where = ev.get("venue") or ev.get("location") or ""
        lines.append(f"【{ev['name']}】{ev['event_date']} {ev['start_time'] or ''}｜{where}")
        combined = live + legacy
        if not combined:
            lines.append("　（目前尚無人報名）")
        else:
            for i, r in enumerate(combined, 1):
                lines.append(f"　{i}. {r['name']}｜{r['phone'] or '無電話'}")
        if unassigned:
            lines.append(f"　⚠️另有 {len(unassigned)} 筆同日報名資料分不出確切場次，請人工核對")
        lines.append("")
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    c = rr.conn()
    events = fetch_tomorrow_events(c)
    if not events:
        print(f"明天（{tomorrow_str()}）沒有場次，不用提醒")
        return

    msg = build_message(c, events)
    print(msg)

    if args.dry_run:
        print("\n[--dry-run，不會真的發送]")
        return

    if not rr.notify(msg):
        print("Telegram直送失敗，改用notify_coach.sh", file=sys.stderr)
        import subprocess
        subprocess.run(
            ["bash", os.path.join(os.path.dirname(__file__), "notify_coach.sh"), msg],
            timeout=15, check=False,
        )


if __name__ == "__main__":
    main()
