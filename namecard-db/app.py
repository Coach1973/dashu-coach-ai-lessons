"""
名片搜尋網頁。跑法：python app.py（預設 port 5000，手機用同一個Cloudflare通道對外開）
"""
import json
import os

from flask import Flask, render_template, request

import db

app = Flask(__name__)
IMAGE_FOLDER = os.environ.get("NAMECARD_FOLDER", "")


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    conn = db.get_conn()
    categories = [
        r["category"]
        for r in conn.execute(
            "SELECT DISTINCT category FROM cards WHERE category IS NOT NULL ORDER BY category"
        ).fetchall()
    ]

    sql = "SELECT * FROM cards WHERE 1=1"
    params: list[str] = []
    if query:
        sql += """ AND (name LIKE ? OR company LIKE ? OR address LIKE ?
                        OR tagline LIKE ? OR keywords LIKE ? OR category LIKE ?)"""
        like = f"%{query}%"
        params += [like] * 6
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY created_at DESC LIMIT 200"

    rows = conn.execute(sql, params).fetchall()
    cards = []
    for r in rows:
        card = dict(r)
        try:
            card["keywords"] = json.loads(card["keywords"] or "[]")
        except json.JSONDecodeError:
            card["keywords"] = []
        cards.append(card)
    conn.close()

    return render_template(
        "index.html", cards=cards, categories=categories, query=query, selected_category=category
    )


@app.route("/matches")
def matches():
    conn = db.get_conn()
    rows = conn.execute(
        """SELECT m.relation_reason, a.name AS name_a, a.company AS company_a,
                  b.name AS name_b, b.company AS company_b
           FROM matches m
           JOIN cards a ON a.id = m.card_id_a
           JOIN cards b ON b.id = m.card_id_b
           ORDER BY m.created_at DESC"""
    ).fetchall()
    conn.close()
    return render_template("matches.html", pairs=rows)


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("NAMECARD_PORT", 5050)))
