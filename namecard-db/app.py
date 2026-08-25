"""
名片搜尋網頁。跑法：python app.py（預設 port 5000，手機用同一個Cloudflare通道對外開）
"""
import json
import os
import time
import uuid
from collections import defaultdict, deque
from functools import wraps

import anthropic
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import db
from chain_matcher import match_card_to_chain
from dedup import run_dedup
from extract import MODEL, extract_card_fields

app = Flask(__name__)
app.secret_key = os.environ.get("NAMECARD_SECRET_KEY", "")
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


@app.route("/chains")
def chains_page():
    conn = db.get_conn()
    chains = db.list_chains_with_members(conn)
    conn.close()
    return render_template("chains.html", chains=chains)


def team_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("team_username"):
            return redirect(url_for("team_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/team/login", methods=["GET", "POST"])
def team_login():
    if request.method == "GET":
        return render_template("team_login.html", error=None)
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    conn = db.get_conn()
    member = db.get_team_member(conn, username)
    conn.close()
    if member and check_password_hash(member["password_hash"], password):
        session["team_username"] = username
        session["team_display_name"] = member["display_name"] or username
        session.permanent = True
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("team_login.html", error="帳號或密碼不對，請再試一次"), 401


@app.route("/team/logout")
def team_logout():
    session.pop("team_username", None)
    session.pop("team_display_name", None)
    return redirect(url_for("index"))


@app.route("/card/<int:card_id>/follow", methods=["GET"])
@team_login_required
def card_follow(card_id):
    conn = db.get_conn()
    card = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    if card is None:
        conn.close()
        return "找不到這張名片", 404
    follow_up = db.get_or_create_follow_up(conn, card_id)
    logs = db.list_follow_up_logs(conn, follow_up["id"])
    chain_context = conn.execute(
        """SELECT ic.name AS chain_name, ic.core_theme, cm.role_name
           FROM chain_members cm JOIN industry_chains ic ON ic.id = cm.chain_id
           WHERE cm.card_id = ?""",
        (card_id,),
    ).fetchall()
    conn.close()
    return render_template(
        "card_follow.html", card=card, follow_up=follow_up, logs=logs,
        chain_context=chain_context, display_name=session.get("team_display_name"),
    )


@app.route("/card/<int:card_id>/follow/update_stage", methods=["POST"])
@team_login_required
def card_follow_update_stage(card_id):
    stage = request.form.get("stage", "待邀約")
    conn = db.get_conn()
    db.update_follow_up_stage(conn, card_id, stage, session.get("team_display_name"))
    conn.close()
    return redirect(url_for("card_follow", card_id=card_id))


@app.route("/card/<int:card_id>/follow/add_log", methods=["POST"])
@team_login_required
def card_follow_add_log(card_id):
    channel = request.form.get("channel", "")
    content = (request.form.get("content") or "").strip()
    if content:
        conn = db.get_conn()
        follow_up = db.get_or_create_follow_up(conn, card_id)
        db.add_follow_up_log(conn, follow_up["id"], channel, content, session.get("team_display_name") or "")
        conn.close()
    return redirect(url_for("card_follow", card_id=card_id))


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
        card_id = db.insert_card(conn, saved_name, fields)
        if "_error" in fields:
            results.append({"filename": f.filename, "error": fields["_error"]})
        else:
            any_success = True
            try:
                match_card_to_chain(conn, client, card_id, MODEL)
            except Exception:  # noqa: BLE001 — 媒合失敗不影響名片本身已收錄
                pass
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
