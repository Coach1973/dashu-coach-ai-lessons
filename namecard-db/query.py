"""
查詢名片資料庫，給 LINE/Telegram 對話用。

用法：
    python query.py <關鍵字>

比對欄位：name / company / title / mobile / email / line_id
"""
import sys

import db


def search(keyword: str) -> list[dict]:
    conn = db.get_conn()
    like = f"%{keyword}%"
    rows = conn.execute(
        """SELECT name, title, company, mobile, landline, email, line_id, website, status
           FROM cards
           WHERE status != 'failed'
             AND (name LIKE ? OR company LIKE ? OR title LIKE ?
                  OR mobile LIKE ? OR email LIKE ? OR line_id LIKE ?)
           ORDER BY name""",
        (like, like, like, like, like, like),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def format_result(rows: list[dict]) -> str:
    if not rows:
        return "查無符合的名片資料。"
    blocks = []
    for r in rows:
        lines = [f"👤 {r['name'] or '（無姓名）'}"]
        if r["title"] or r["company"]:
            lines.append(f"　{r['title'] or ''} {r['company'] or ''}".rstrip())
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
