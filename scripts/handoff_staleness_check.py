#!/usr/bin/env python3
"""接力棒待辦表過期偵測（2026-09-11教練糾正ACER誤報後新增，根因防範）

問題：待辦表狀態🔒/🔴這類卡住項目，若在別的session/別的脈絡被順手解決，
沒人回頭改這行狀態，就會變成過期事實一路被當成真相講給教練聽
（實例：ACER「49天未開機」08-26已解決，卻放到09-11才被教練當面戳破）。

做法：不試圖自動判斷「是否真的解決了」（做不到，需要語意理解），
改成掃描待辦表裡的🔒/🔴列，抓出列裡提到的最新日期，
超過門檻天數就明確標成「過期未覆核」，逼開工時主動口頭跟教練核對
而不是把老資料原封不動讀出來當事實。
"""
import re
import sys
from datetime import date, datetime

STALE_DAYS = 14

def main():
    if len(sys.argv) < 2:
        print("usage: handoff_staleness_check.py <JUNSHI_HANDOFF_LATEST.md>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    today = date.today()
    date_re = re.compile(r"20\d{2}-\d{2}-\d{2}")
    flagged = []

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cols = [c.strip() for c in stripped.split("|")]
        # split("|") on a row starting with "|" yields a leading empty string,
        # so real columns are cols[1..]: 優先/任務/狀態/說明
        if len(cols) < 5:
            continue
        status = cols[3]
        # 只抓真正還卡著的（🔒卡住 / ⏳待動手），排除已完成✅、永久提醒⚠️（那些是刻意常駐，不是遺忘）
        if "🔒" not in status and "⏳" not in status:
            continue
        if "✅" in status:
            continue
        dates_found = date_re.findall(line)
        if not dates_found:
            continue
        try:
            parsed = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates_found]
        except ValueError:
            continue
        newest = max(parsed)
        age_days = (today - newest).days
        if age_days > STALE_DAYS:
            task_match = re.search(r"\*\*(.+?)\*\*", line)
            task_name = task_match.group(1) if task_match else cols[2][:60]
            flagged.append((age_days, newest, task_name))

    if not flagged:
        print("✅ 待辦表無超過{}天未覆核的🔒/🔴項目".format(STALE_DAYS))
        return

    flagged.sort(reverse=True)
    print("⚠️ 以下🔒/🔴待辦項目超過{}天未覆核：AI自己查證現況（git log／log檔／實際狀態），不准拿去問教練；查不出來就移到「🤫等教練自己提起」區：".format(STALE_DAYS))
    for age_days, newest, task_name in flagged:
        print(f"  - （最後提及 {newest}，{age_days} 天前）{task_name}")

if __name__ == "__main__":
    main()
