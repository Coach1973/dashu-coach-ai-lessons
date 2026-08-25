"""
名片搜尋網頁。跑法：python app.py（預設 port 5000，手機用同一個Cloudflare通道對外開）
"""
import json
import os
import time
import uuid
from collections import defaultdict, deque

import anthropic
from flask import Flask, render_template, request

import db
from dedup import run_dedup
from extract import extract_card_fields

app = Flask(__name__)
IMAGE_FOLDER = os.environ.get("NAMECARD_FOLDER", "")

# 公開上傳辨識：任何人都能丟名片照片，AI辨識後直接收錄進同一個名片資料庫
PUBLIC_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "public_uploads")
os.makedirs(PUBLIC_UPLOAD_FOLDER, exist_ok=True)
ALLOWED_UPLOAD_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
MAX_FILES_PER_UPLOAD = 5
MAX_FILE_SIZE = 15 * 1024 * 1024  # 單檔15MB
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE * MAX_FILES_PER_UPLOAD

# 辨識本身不收費（PaddleOCR本機跑+MiniMax端點無流量限制），節流只是防對外公開端點
# 被腳本瞬間灌爆導致資料庫塞進大量垃圾/惡意資料，門檻設寬鬆不擋正常大量匯入
_upload_log: dict[str, deque] = defaultdict(deque)
RATE_LIMIT_COUNT = 200
RATE_LIMIT_WINDOW = 3600


def _rate_limited(ip: str) -> bool:
    now = time.time()
    q = _upload_log[ip]
    while q and now - q[0] > RATE_LIMIT_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT_COUNT:
        return True
    q.append(now)
    return False


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


@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html", error=None)


@app.route("/upload", methods=["POST"])
def upload_submit():
    ip = (request.headers.get("X-Forwarded-For", "") or request.remote_addr or "").split(",")[0].strip()
    if _rate_limited(ip):
        return render_template("upload.html", error="上傳太頻繁了，請稍後再試（每小時上限200張）")

    files = [f for f in request.files.getlist("photos") if f and f.filename][:MAX_FILES_PER_UPLOAD]
    if not files:
        return render_template("upload.html", error="請選擇至少一張名片照片")

    client = anthropic.Anthropic()
    conn = db.get_conn()
    results = []
    any_success = False
    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        if ext not in ALLOWED_UPLOAD_EXTS:
            results.append({"filename": f.filename, "error": "不支援的檔案格式"})
            continue
        saved_name = f"public_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
        saved_path = os.path.join(PUBLIC_UPLOAD_FOLDER, saved_name)
        f.save(saved_path)
        try:
            fields = extract_card_fields(saved_path, client)
        except Exception as e:  # noqa: BLE001 — 單張失敗不能讓整批停掉
            fields = {"_error": str(e), "_raw": ""}
        db.insert_card(conn, saved_name, fields)
        if "_error" in fields:
            results.append({"filename": f.filename, "error": fields["_error"]})
        else:
            any_success = True
            results.append({"filename": f.filename, "fields": fields})
    conn.close()

    if any_success:
        try:
            run_dedup(client)
        except Exception:  # noqa: BLE001 — 去重失敗不影響已收錄的名片
            pass

    return render_template("upload_result.html", results=results)


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("NAMECARD_PORT", 5050)))
