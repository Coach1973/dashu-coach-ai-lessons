# -*- coding: utf-8 -*-
"""讀BNI Connect官方匯出的「地區會員培訓報告」(SpreadsheetML .xls)，轉成bni_region_training_raw.json。
來源檔常見於D:\\Users\\Downloads\\，檔名含日期時間戳記，內容是Excel 2003 XML格式(非二進位xls/xlsx)。
更新資料：教練有新的官方匯出，改SOURCE_XLS路徑重跑這支即可，會覆蓋bni_region_training_raw.json。
"""
import io
import json
import sys
import xml.etree.ElementTree as ET

NS = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
RAW_OUT = "bni_region_training_raw.json"


def cell_text(row):
    cells = []
    for cell in row.findall('ss:Cell', NS):
        data = cell.find('ss:Data', NS)
        cells.append(data.text if data is not None and data.text else '')
    return cells


def to_date(s):
    return s[:10] if s else ''


def main(source_xls):
    tree = ET.parse(source_xls)
    root = tree.getroot()
    ws = root.find('ss:Worksheet', NS)
    table = ws.find('ss:Table', NS)
    rows = table.findall('ss:Row', NS)

    header_idx = None
    for i, row in enumerate(rows):
        cells = cell_text(row)
        if cells[:2] == ['分會名稱', '分會類型']:
            header_idx = i
            break
    if header_idx is None:
        raise SystemExit("找不到表頭列(分會名稱/分會類型)，檔案格式可能跟預期不同")

    records = []
    for row in rows[header_idx + 1:]:
        c = cell_text(row)
        if len(c) < 11 or not c[0]:
            continue
        chapter, _ctype, surname, given, event_date, event_type, role, _joindate, phone, email, induction = c[:11]
        records.append({
            "chapter": chapter,
            "name": (surname + given).strip(),
            "event_date": to_date(event_date),
            "event_type": event_type,
            "role": role or "",
            "phone": phone or "",
            "email": email or "",
            "induction_date": to_date(induction),
        })

    with io.open(RAW_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)

    chapters = sorted(set(r["chapter"] for r in records))
    dates = sorted(r["event_date"] for r in records)
    print("%d records imported, chapters=%s, date range %s ~ %s" % (
        len(records), chapters, dates[0], dates[-1]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else r"D:\Users\Downloads\__-__-__-___17-08-2026_11-01_PM.xls")
