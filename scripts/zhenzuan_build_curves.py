#!/usr/bin/env python3
"""合併PALMS季度彙整(來賓/引薦/TYFCB)+聊天記錄週報(人數)，產出4條36個月曲線的統一資料集。"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "claude-brain" / "data"
PALMS_JSON = BASE / "zhenzuan_palms_quarterly_summary.json"
CHATLOG_JSON = BASE / "zhenzuan_weekly_from_chatlog.json"
OUT_JSON = BASE / "zhenzuan_36month_curves.json"


def main():
    palms = json.loads(PALMS_JSON.read_text(encoding="utf-8"))
    weekly = json.loads(CHATLOG_JSON.read_text(encoding="utf-8"))
    weekly = [w for w in weekly if w["date"]]

    curves = []
    for period in palms:
        lo, hi = period["from"], period["to"]
        in_range = [w["members"] for w in weekly if lo <= w["date"] <= hi]
        avg_members = round(sum(in_range) / len(in_range), 1) if in_range else None
        curves.append({
            "label": f"{period['from'][:7]}~{period['to'][:7]}",
            "from": period["from"],
            "to": period["to"],
            "members_avg": avg_members,
            "members_sample_weeks": len(in_range),
            "guests": period["guests"],
            "referrals": period["referrals"],
            "referrals_internal": period["referrals_internal"],
            "referrals_external": period["referrals_external"],
            "tyfcb": period["tyfcb"],
        })
    OUT_JSON.write_text(json.dumps(curves, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{'期間':<20}{'人數(週報均值)':>14}{'樣本週數':>8}{'來賓':>8}{'引薦':>8}{'TYFCB':>14}")
    for c in curves:
        print(f"{c['label']:<20}{str(c['members_avg']):>14}{c['members_sample_weeks']:>8}{c['guests']:>8}{c['referrals']:>8}{c['tyfcb']:>14,.0f}")
    print(f"\n已存 {OUT_JSON}")


if __name__ == "__main__":
    main()
