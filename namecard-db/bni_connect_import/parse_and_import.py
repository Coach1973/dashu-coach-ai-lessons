"""
BNI Connect大台南南區會員名冊匯入(2026-08-26教練交辦)
把5個分會(真富/真愛/真誠/真鑫/真鑽)的管理會員頁面爬回的原始資料，
consolidate成每人一筆，寫進namecard-db的cards表，跟名片媒合名單合併。
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402

CHAPTERS = ["真富", "真愛", "真誠", "真鑫", "真鑽"]
STATUS_RE = re.compile(r"(待定會員|待定續約|現任|暫停|逾期|過期|離開|無效)")
IMPORT_DIR = Path(__file__).resolve().parent


def parse_line(line: str, expected_chapter: str):
    line = line.strip()
    if not line:
        return None
    idx = line.find(expected_chapter)
    if idx == -1:
        raise ValueError(f"找不到分會名稱 {expected_chapter}: {line!r}")
    name = line[:idx].strip()
    rest = line[idx + len(expected_chapter):].strip()

    matches = list(STATUS_RE.finditer(rest))
    if not matches:
        raise ValueError(f"找不到狀態欄位: {line!r}")
    m = matches[-1]
    detail = rest[: m.start()].strip()
    status = m.group(1)
    date_part = rest[m.end():].strip()

    return {
        "name": name,
        "chapter": expected_chapter,
        "detail": detail,  # 公司+職業分類合併文字，不強行拆開避免拆錯
        "status": status,
        "date": date_part,
    }


def normalize_name(name: str) -> str:
    """姓名比對用：去除全部空白、統一全形/半形，作為consolidation跟既有cards比對的key"""
    n = unicodedata.normalize("NFKC", name)
    return re.sub(r"\s+", "", n)


def load_all_rows():
    rows = []
    for chapter in CHAPTERS:
        path = IMPORT_DIR / f"raw_{chapter}.txt"
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not line.strip():
                continue
            rows.append(parse_line(line, chapter))
    return rows


def consolidate(rows):
    """依姓名(正規化後)分組，決定每人現在是在籍(有任一筆現任)還是前會員"""
    people = {}
    for r in rows:
        key = normalize_name(r["name"])
        people.setdefault(key, {"display_name": r["name"], "rows": []})
        people[key]["rows"].append(r)

    consolidated = []
    for key, info in people.items():
        rows_for_person = info["rows"]
        active_rows = [r for r in rows_for_person if r["status"] == "現任"]
        chapters_seen = []
        for r in rows_for_person:
            if r["chapter"] not in chapters_seen:
                chapters_seen.append(r["chapter"])

        if active_rows:
            is_active = True
            current_chapter = active_rows[0]["chapter"]
            detail = active_rows[0]["detail"]
        else:
            is_active = False
            # 抓最後一筆非現任紀錄的分會當作「最近隸屬」
            current_chapter = rows_for_person[-1]["chapter"]
            detail = rows_for_person[-1]["detail"]

        if is_active:
            bni_note = f"{current_chapter}分會現任會員"
            if len(chapters_seen) > 1:
                others = [c for c in chapters_seen if c != current_chapter]
                bni_note += f"（曾隸屬：{'、'.join(others)}）"
        else:
            if len(chapters_seen) > 1:
                bni_note = f"前會員・曾隸屬{'、'.join(chapters_seen)}分會（最近：{current_chapter}）"
            else:
                bni_note = f"前會員・曾隸屬{current_chapter}分會"

        # detail欄位常同時含公司名稱+BNI職業分類，公司放company，全段落也存進category方便搜尋
        company = ""
        category = detail
        m = re.match(r"^(.*?)\s*([一-鿿A-Za-z&]+\s*-\s*.+)$", detail)
        if m and m.group(1).strip():
            company = m.group(1).strip()
            category = m.group(2).strip()

        consolidated.append({
            "name": info["display_name"],
            "name_key": key,
            "is_active": is_active,
            "current_chapter": current_chapter,
            "chapters_seen": chapters_seen,
            "company": company,
            "category": category,
            "bni_note": bni_note,
        })
    return consolidated


def main():
    rows = load_all_rows()
    print(f"原始資料共 {len(rows)} 筆")
    people = consolidate(rows)
    print(f"去重後共 {len(people)} 人")
    active_count = sum(1 for p in people if p["is_active"])
    former_count = len(people) - active_count
    print(f"在籍(現任): {active_count} 人")
    print(f"前會員: {former_count} 人")

    conn = db.get_conn()
    matched = 0
    inserted = 0
    for p in people:
        existing = conn.execute(
            "SELECT id, name FROM cards WHERE name IS NOT NULL AND REPLACE(name, ' ', '') = ?",
            (p["name_key"],),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE cards SET bni_status = 'bni_member', bni_note = ? WHERE id = ?",
                (p["bni_note"], existing["id"]),
            )
            matched += 1
        else:
            synthetic_filename = f"bniconnect__{p['current_chapter']}__{p['name_key']}.novalue"
            conn.execute(
                """INSERT OR IGNORE INTO cards
                   (image_filename, name, company, category, status, bni_status, bni_note)
                   VALUES (?, ?, ?, ?, 'ok', 'bni_member', ?)""",
                (synthetic_filename, p["name"], p["company"], p["category"], p["bni_note"]),
            )
            inserted += 1
    conn.commit()
    conn.close()
    print(f"比對到既有名片並更新標記: {matched} 人")
    print(f"新增進資料庫(無名片照片): {inserted} 人")


if __name__ == "__main__":
    main()
