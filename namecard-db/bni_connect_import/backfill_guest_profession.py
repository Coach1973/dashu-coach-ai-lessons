"""
教練糾正：guests表原本只抓姓名/電話/email三欄，漏了「地區-查看來賓」報告
本來就有的公司/職業欄位——BNI Connect來賓報名時必填職業，不可能沒有。
這支腳本讀教練匯出的完整報表(.xls，實為SpreadsheetML)，把公司/職業/分會
補進既有guests表，用電話比對回填，同一人多筆訪問取「最新一次」的職業為準
(同一人不同次訪問填的職業常不一致，是BNI Connect本身的自由填寫欄位)。
"""
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402

NS = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
IDX_ATTR = "{urn:schemas-microsoft-com:office:spreadsheet}Index"

XLS_PATH = Path("/Users/bymyway/Downloads/__-__-__-___26-08-2026_3-26_AM.xls")


def row_to_dict(row) -> dict:
    d = {}
    idx = 0
    for c in row.findall("ss:Cell", NS):
        ss_index = c.get(IDX_ATTR)
        idx = int(ss_index) if ss_index else idx + 1
        data = c.find("ss:Data", NS)
        d[idx] = data.text if data is not None else None
    return d


def parse_rows() -> list[dict]:
    tree = ET.parse(XLS_PATH)
    root = tree.getroot()
    table = root.find("ss:Worksheet", NS).find("ss:Table", NS)
    rows = table.findall("ss:Row", NS)

    header_row_idx = next(
        i for i, r in enumerate(rows) if row_to_dict(r).get(1) == "姓氏"
    )
    header = row_to_dict(rows[header_row_idx])
    col = {v: k for k, v in header.items()}  # 欄位名 -> index

    records = []
    for r in rows[header_row_idx + 1 :]:
        d = row_to_dict(r)
        phone = (d.get(col["電話"]) or "").strip()
        if not phone:
            continue
        records.append(
            {
                "name": f"{(d.get(col['姓氏']) or '').strip()} {(d.get(col['名字']) or '').strip()}".strip(),
                "phone": phone,
                "company": (d.get(col["公司"]) or "").strip() or None,
                "profession": (d.get(col["職業"]) or "").strip() or None,
                "chapter": (d.get(col["分會"]) or "").strip() or None,
                "visit_date": d.get(col["訪問日期"]) or "",
            }
        )
    return records


def main() -> None:
    records = parse_rows()
    print(f"報表總筆數: {len(records)}")

    latest_by_phone: dict[str, dict] = {}
    for rec in records:
        existing = latest_by_phone.get(rec["phone"])
        if existing is None or rec["visit_date"] > existing["visit_date"]:
            latest_by_phone[rec["phone"]] = rec
    print(f"依電話去重後: {len(latest_by_phone)} 人")

    conn = db.get_conn()
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(guests)").fetchall()}
    for col_name in ("company", "profession", "chapter"):
        if col_name not in cols:
            conn.execute(f"ALTER TABLE guests ADD COLUMN {col_name} TEXT")
    conn.commit()

    existing_phones = {
        r["mobile"] for r in conn.execute("SELECT mobile FROM guests").fetchall()
    }

    updated = 0
    not_found = 0
    for phone, rec in latest_by_phone.items():
        if phone not in existing_phones:
            not_found += 1
            continue
        conn.execute(
            "UPDATE guests SET company = ?, profession = ?, chapter = ? WHERE mobile = ?",
            (rec["company"], rec["profession"], rec["chapter"], phone),
        )
        updated += 1
    conn.commit()

    total_guests = conn.execute("SELECT COUNT(*) FROM guests").fetchone()[0]
    has_profession = conn.execute(
        "SELECT COUNT(*) FROM guests WHERE profession IS NOT NULL AND profession != ''"
    ).fetchone()[0]
    conn.close()

    print(f"回填成功: {updated} 人")
    print(f"報表裡有但guests表查無此電話: {not_found} 人")
    print(f"guests表總人數: {total_guests}，已有職業: {has_profession} ({has_profession/total_guests:.1%})")


if __name__ == "__main__":
    main()
