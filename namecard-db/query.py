"""
查詢名片資料庫，給 LINE/Telegram 對話用。教練要找人組產業服務鏈或組團隊，
搜尋範圍涵蓋 cards(真實名片+BNI會員) 跟 guests(BNI Connect來賓)兩張表。

用法：
    python query.py <關鍵字>

比對欄位：name / company / title / profession / mobile / email / line_id
"""
import sys

import db


def search(keyword: str) -> list[dict]:
    conn = db.get_conn()
    like = f"%{keyword}%"
    card_rows = conn.execute(
        """SELECT 'card' AS source, name, title, company, mobile, landline, email,
                  line_id, website, status, bni_note
           FROM cards
           WHERE status != 'failed' AND status != 'roster'
             AND (name LIKE ? OR company LIKE ? OR title LIKE ?
                  OR mobile LIKE ? OR email LIKE ? OR line_id LIKE ?)
           ORDER BY name""",
        (like, like, like, like, like, like),
    ).fetchall()
    guest_rows = conn.execute(
        """SELECT 'guest' AS source, name, profession AS title, company, mobile,
                  NULL AS landline, email, NULL AS line_id, NULL AS website,
                  NULL AS status, chapter AS bni_note
           FROM guests
           WHERE name LIKE ? OR company LIKE ? OR profession LIKE ?
                 OR mobile LIKE ? OR email LIKE ?
           ORDER BY name""",
        (like, like, like, like, like),
    ).fetchall()
    # 2026-09-07新增：通訊錄/會員名冊聯絡人(獅子會/扶輪社等)，跟名片是分開的表
    directory_rows = conn.execute(
        """SELECT 'directory' AS source, name, profession AS title, org_name AS company,
                  phone AS mobile, NULL AS landline, NULL AS email, NULL AS line_id,
                  NULL AS website, NULL AS status, org_name AS bni_note
           FROM directory_contacts
           WHERE name LIKE ? OR org_name LIKE ? OR profession LIKE ? OR phone LIKE ?
           ORDER BY name""",
        (like, like, like, like),
    ).fetchall()
    conn.close()
    return [dict(r) for r in card_rows] + [dict(r) for r in guest_rows] + [dict(r) for r in directory_rows]


def format_result(rows: list[dict]) -> str:
    if not rows:
        return "查無符合的名片資料。"
    blocks = []
    for r in rows:
        tag = {"card": "👤", "guest": "🧑‍🤝‍🧑 [來賓]", "directory": "📒 [通訊錄]"}.get(r["source"], "👤")
        lines = [f"{tag} {r['name'] or '（無姓名）'}"]
        if r["title"] or r["company"]:
            lines.append(f"　{r['title'] or ''} {r['company'] or ''}".rstrip())
        if r["bni_note"]:
            lines.append(f"🏷️ {r['bni_note']}")
        if r["mobile"]:
            lines.append(f"📱 {r['mobile']}")
        if r["landline"]:
            lines.append(f"☎️ {r['landline']}")
        if r["email"]:
            lines.append(f"✉️ {r['email']}")
        if r["line_id"]:
            lines.append(f"💬 LINE：{r['line_id']}")
        if r["website"]:
            lines.append(f"🌐 {r['website']}")
        if r["status"] == "needs_review":
            lines.append("⚠️ 這筆資料AI信心較低，建議人工核對")
        blocks.append("\n".join(lines))
    return f"共找到 {len(rows)} 筆：\n\n" + "\n\n".join(blocks)


def main() -> None:
    if len(sys.argv) < 2:
        print("用法：python query.py <關鍵字>")
        raise SystemExit(1)
    keyword = " ".join(sys.argv[1:])
    rows = search(keyword)
    print(format_result(rows))


if __name__ == "__main__":
    main()
