#!/usr/bin/env python3
"""解析真鑽分會PALMS摘要報告(SpreadsheetML .xls)，彙整每期總來賓/總引薦/總TYFCB。"""
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
DATA_DIR = Path(__file__).resolve().parent.parent / "claude-brain" / "data" / "zhenzuan_palms_quarterly"


def cellvals(row):
    return [
        (c.find('ss:Data', NS).text if c.find('ss:Data', NS) is not None else "")
        for c in row.findall('ss:Cell', NS)
    ]


def parse_file(path):
    tree = ET.parse(path)
    ws = tree.getroot().find('ss:Worksheet', NS)
    rows = ws.find('ss:Table', NS).findall('ss:Row', NS)
    from_date = cellvals(rows[5])[1][:10]
    to_date = cellvals(rows[6])[1][:10]
    header = cellvals(rows[7])
    idx = {name: i for i, name in enumerate(header)}
    member_count = 0
    total_row = None
    for r in rows[8:]:
        vals = cellvals(r)
        if len(vals) < len(header):
            continue
        if vals[0] == "總數":
            # PALMS報表最後一列是官方認證的總計，不能跟個別會員列相加，
            # 否則會把總數再疊加一次造成重複計算(試金石教訓)。
            total_row = vals
            continue
        member_count += 1
    if total_row is None:
        raise ValueError(f"{path} 找不到官方「總數」列")
    total_guest = int(float(total_row[idx['來賓']] or 0))
    total_int_given = int(float(total_row[idx['提供內部引薦']] or 0))
    total_ext_given = int(float(total_row[idx['提供外部引薦']] or 0))
    total_tyfcb = float(total_row[idx['交易價值']] or 0)
    return {
        "from": from_date,
        "to": to_date,
        "members_in_report": member_count,
        "guests": total_guest,
        "referrals": total_int_given + total_ext_given,
        "referrals_internal": total_int_given,
        "referrals_external": total_ext_given,
        "tyfcb": total_tyfcb,
    }


def main():
    import json
    results = []
    for f in sorted(DATA_DIR.glob("*.xls")):
        results.append(parse_file(f))
    results.sort(key=lambda r: r["from"])
    print(f"{'從':<12}{'至':<12}{'會員數':>6}{'來賓':>6}{'引薦':>6}{'TYFCB':>14}")
    for r in results:
        print(f"{r['from']:<12}{r['to']:<12}{r['members_in_report']:>6}{r['guests']:>6}{r['referrals']:>6}{r['tyfcb']:>14,.0f}")
    out_path = DATA_DIR.parent / "zhenzuan_palms_quarterly_summary.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n已存 {out_path}")
    return results


if __name__ == "__main__":
    main()
