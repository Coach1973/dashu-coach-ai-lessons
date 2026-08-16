#!/usr/bin/env python3
"""todo_staleness_check.py — 賈維斯計畫 Phase 3 的解析邏輯
被 todo_staleness_check.sh 呼叫，不單獨執行。
用途：解析待辦表格列，找出「卡住超過7天」與「3天內到期」的項目。
"""
import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta

DONE_MARKS = ("✅", "🟢")
STUCK_MARKS = ("🔒", "⏳", "⚠️")


def parse_row(line: str):
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) < 3:
        return None
    priority, task, status = parts[0], parts[1], parts[2]
    return priority, task, status


def is_stuck(status: str) -> bool:
    if any(m in status for m in DONE_MARKS):
        return False
    return any(m in status for m in STUCK_MARKS)


def find_upcoming_dates(text: str, today: date, window_days: int = 3):
    """抓文字裡的 M/D 或 MM/DD 格式日期，判斷是否落在今天起 window_days 天內"""
    hits = []
    for m in re.finditer(r"(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)", text):
        month, day = int(m.group(1)), int(m.group(2))
        if not (1 <= month <= 12 and 1 <= day <= 31):
            continue
        for year in (today.year, today.year + 1):
            try:
                candidate = date(year, month, day)
            except ValueError:
                continue
            delta = (candidate - today).days
            if 0 <= delta <= window_days:
                hits.append((m.group(0), candidate))
                break
    return hits


def main():
    rows_file, state_file = sys.argv[1], sys.argv[2]
    with open(rows_file, encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]

    with open(state_file, encoding="utf-8") as f:
        state = json.load(f)

    today = date.today()
    seen_hashes = set()
    stale_items = []
    upcoming_items = []

    for line in lines:
        parsed = parse_row(line)
        if not parsed:
            continue
        priority, task, status = parsed
        if not is_stuck(status):
            continue

        task_hash = hashlib.md5(task.encode("utf-8")).hexdigest()[:12]
        seen_hashes.add(task_hash)

        if task_hash not in state:
            state[task_hash] = {"first_seen": today.isoformat(), "label": task[:40]}
        else:
            first_seen = datetime.fromisoformat(state[task_hash]["first_seen"]).date()
            if (today - first_seen).days >= 7:
                stale_items.append((task[:60], (today - first_seen).days))

        for date_str, candidate in find_upcoming_dates(task, today):
            upcoming_items.append((task[:60], date_str, candidate.isoformat()))

    # 清掉表格裡已經不存在的舊hash（已解決/已改狀態），state只保留還活著的
    state = {h: v for h, v in state.items() if h in seen_hashes}
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    if not stale_items and not upcoming_items:
        return  # 安靜，不輸出

    out = []
    if stale_items:
        out.append(f"⏰ 卡住超過7天（{len(stale_items)}項）：")
        for task, days in stale_items:
            out.append(f"  • {task}（卡了{days}天）")
    if upcoming_items:
        out.append(f"📅 3天內有日期到（{len(upcoming_items)}項）：")
        seen_pairs = set()
        for task, date_str, iso in upcoming_items:
            key = (task, date_str)
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            out.append(f"  • {task}（{date_str}）")

    print("\n".join(out))


if __name__ == "__main__":
    main()
