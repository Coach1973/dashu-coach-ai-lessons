"""
教練指出：guests表只存「最新一次」訪問的分會，看不到來賓是哪個分會、
什麼時候來過——同一人常有多筆不同分會/不同日期的訪問紀錄。
這支腳本讀「地區-查看來賓」完整歷史報表(.xls，實為SpreadsheetML，涵蓋
2018-08-08~2026-09-01全部訪問紀錄)，把每一筆訪問明細寫進guest_visits表
(guests表本身不動，仍是每人一筆摘要)，用電話比對guest_id。
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402

NS = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
IDX_ATTR = "{urn:schemas-microsoft-com:office:spreadsheet}Index"

XLS_PATH = Path("/Users/bymyway/Downloads/__-__-__-___31-08-2026_3-04_PM.xls")


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
    col = {v: k for k, v in header.items()}

    records = []
    for r in rows[header_row_idx + 1:]:
        d = row_to_dict(r)
        phone = (d.get(col["電話"]) or "").strip()
        if not phone:
            continue
        visit_date = (d.get(col["訪問日期"]) or "").strip()
        records.append({
            "name": f"{(d.get(col['姓氏']) or '').strip()} {(d.get(col['名字']) or '').strip()}".strip(),
            "phone": phone,
            "email": (d.get(col["電子郵箱"]) or "").strip() or None,
            "company": (d.get(col["公司"]) or "").strip() or None,
            "profession": (d.get(col["職業"]) or "").strip() or None,
            "chapter": (d.get(col["分會"]) or "").strip() or None,
            "visit_date": visit_date.split("T")[0] if visit_date else None,
            "invited_by": (d.get(col["Invited By"]) or "").strip() or None,
            "visit_type": (d.get(col["Type"]) or "").strip() or None,
        })
    return records


def main() -> None:
    db.init_db()  # 確保guest_visits表已建立
    records = parse_rows()
    print(f"報表總筆數(有電話): {len(records)}")

    conn = db.get_conn()
    guest_id_by_phone = {
        r["mobile"]: r["id"]
        for r in conn.execute("SELECT id, mobile FROM guests WHERE mobile IS NOT NULL AND mobile != ''")
    }

    new_guests = 0
    visits_inserted = 0
    visits_duplicate = 0

    for rec in records:
        guest_id = guest_id_by_phone.get(rec["phone"])
        if guest_id is None:
            # 報表裡有、guests表沒有的新來賓(教練原設計就是要涵蓋所有分會約過的來賓)
            cur = conn.execute(
                """INSERT INTO guests (name, mobile, email, company, profession, chapter)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (rec["name"], rec["phone"], rec["email"], rec["company"], rec["profession"], rec["chapter"]),
            )
            guest_id = cur.lastrowid
            guest_id_by_phone[rec["phone"]] = guest_id
            new_guests += 1

        cur = conn.execute(
            """INSERT OR IGNORE INTO guest_visits
               (guest_id, chapter, visit_date, company, profession, invited_by, visit_type)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (guest_id, rec["chapter"], rec["visit_date"], rec["company"],
             rec["profession"], rec["invited_by"], rec["visit_type"]),
        )
        if cur.rowcount == 1:
            visits_inserted += 1
        else:
            visits_duplicate += 1

    conn.commit()
    total_visits = conn.execute("SELECT COUNT(*) FROM guest_visits").fetchone()[0]
    multi_visit_guests = conn.execute(
        "SELECT COUNT(*) FROM (SELECT guest_id FROM guest_visits GROUP BY guest_id HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    conn.close()

    print(f"新增來賓(報表有、guests表原本沒有): {new_guests} 人")
    print(f"新增訪問紀錄: {visits_inserted} 筆")
    print(f"重複跳過(同人同分會同日期): {visits_duplicate} 筆")
    print(f"guest_visits表總筆數: {total_visits}")
    print(f"有多筆訪問紀錄的來賓: {multi_visit_guests} 人")


if __name__ == "__main__":
    main()
