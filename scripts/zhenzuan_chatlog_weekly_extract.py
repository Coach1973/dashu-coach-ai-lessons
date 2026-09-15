#!/usr/bin/env python3
"""從真鑽唯讀群LINE聊天記錄逐週出席報告，抽取「人數」與「來賓」時間序列。"""
import re
import json
from pathlib import Path

SRC = Path.home() / "Downloads" / "[LINE] ※真鑽唯讀群的聊天.txt"
OUT = Path(__file__).resolve().parent.parent / "claude-brain" / "data" / "zhenzuan_weekly_from_chatlog.json"

date_re = re.compile(r"^(\d{4})/(\d{2})/(\d{2})（")
member_patterns = [
    re.compile(r"應到會員[：:]\s*(\d+)位"),
    re.compile(r"❇️?人數\s*[：:]\s*(\d+)位"),
    re.compile(r"人數\s+(\d+)位"),
]
guest_patterns = [re.compile(r"來賓[：:]\s*(\d+)\s*位")]


def main():
    lines = SRC.read_text(encoding="utf-8", errors="replace").split("\n")
    current_date = None
    results = []
    for i, line in enumerate(lines):
        m = date_re.match(line)
        if m:
            current_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            continue
        for pat in member_patterns:
            mm = pat.search(line)
            if mm:
                guest_val = None
                for j in range(i, min(i + 40, len(lines))):
                    for gp in guest_patterns:
                        gm = gp.search(lines[j])
                        if gm:
                            guest_val = int(gm.group(1))
                            break
                    if guest_val is not None:
                        break
                results.append({"date": current_date, "members": int(mm.group(1)), "guests": guest_val})
                break
    results.sort(key=lambda r: r["date"] or "")
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"共擷取 {len(results)} 筆週報，已存 {OUT}")
    print("date range:", results[0]["date"], "~", results[-1]["date"])


if __name__ == "__main__":
    main()
