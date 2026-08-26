"""
把contact_scrape/batch_*.json (格式: [姓名, memberId, 電話, 手機, Email]) 寫回cards表的
mobile/email欄位。姓名比對用REPLACE(name,' ','')，跟parse_and_import.py同一套key。
電話優先用「手機」欄位，沒有才退回用「電話」欄位。只補空值，不覆蓋既有非空資料。
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402

IMPORT_DIR = Path(__file__).resolve().parent
SCRAPE_DIR = IMPORT_DIR / "contact_scrape"


def normalize_name(name: str) -> str:
    n = unicodedata.normalize("NFKC", name)
    return re.sub(r"\s+", "", n)


def main():
    conn = db.get_conn()
    updated = 0
    skipped_no_match = 0
    skipped_already_filled = 0
    no_match_names = []

    for path in sorted(SCRAPE_DIR.glob("batch_*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        for name, member_id, phone, mobile, email in rows:
            key = normalize_name(name)
            best_phone = mobile.strip() if mobile and mobile.strip() else phone.strip()
            email = (email or "").strip()
            if not best_phone and not email:
                continue

            existing = conn.execute(
                "SELECT id, mobile, email FROM cards WHERE name IS NOT NULL AND REPLACE(name, ' ', '') = ?",
                (key,),
            ).fetchone()
            if not existing:
                skipped_no_match += 1
                no_match_names.append(f"{name}({member_id})")
                continue

            new_mobile = existing["mobile"] if existing["mobile"] else best_phone
            new_email = existing["email"] if existing["email"] else email
            if new_mobile == existing["mobile"] and new_email == existing["email"]:
                skipped_already_filled += 1
                continue

            conn.execute(
                "UPDATE cards SET mobile = ?, email = ? WHERE id = ?",
                (new_mobile, new_email, existing["id"]),
            )
            updated += 1

    conn.commit()
    conn.close()

    print(f"更新: {updated} 筆")
    print(f"已有資料跳過: {skipped_already_filled} 筆")
    print(f"查無對應姓名: {skipped_no_match} 筆")
    if no_match_names:
        print("查無對應姓名清單:")
        for n in no_match_names:
            print(f"  {n}")


if __name__ == "__main__":
    main()
