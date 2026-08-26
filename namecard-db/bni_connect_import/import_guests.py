"""
匯入BNI Connect大台南南區「來賓」名單到guests表。
來源: guest_scrape/all_guests_final.tsv (name\tmobile\temail)
同一人常有多筆訪問紀錄，依「姓名正規化+電話」去重，每人只留一筆
(電話為主要去重鍵，因姓名可能有全形/半形或姓在前後的差異)。
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402

IMPORT_DIR = Path(__file__).resolve().parent
TSV_PATH = IMPORT_DIR / "guest_scrape" / "all_guests_final.tsv"


def normalize_name(name: str) -> str:
    n = unicodedata.normalize("NFKC", name)
    return re.sub(r"\s+", "", n)


def main():
    conn = db.get_conn()
    seen_keys = set()
    inserted = 0
    skipped_dup = 0
    skipped_no_contact = 0

    with TSV_PATH.open(encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            name, mobile, email = parts
            name = name.strip()
            mobile = mobile.strip()
            email = email.strip()
            if not mobile and not email:
                skipped_no_contact += 1
                continue

            key = mobile if mobile else (normalize_name(name), email)
            if key in seen_keys:
                skipped_dup += 1
                continue
            seen_keys.add(key)

            conn.execute(
                "INSERT INTO guests (name, mobile, email) VALUES (?, ?, ?)",
                (name, mobile, email),
            )
            inserted += 1

    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM guests").fetchone()[0]
    conn.close()

    print(f"新增: {inserted} 筆")
    print(f"重複跳過(同電話): {skipped_dup} 筆")
    print(f"無聯絡方式跳過: {skipped_no_contact} 筆")
    print(f"guests表目前總筆數: {total}")


if __name__ == "__main__":
    main()
