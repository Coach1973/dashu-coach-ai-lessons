"""
名片搜尋網頁。跑法：python app.py（預設 port 5000，手機用同一個Cloudflare通道對外開）
"""
import json
import os
import subprocess
import sys
import time
import uuid
from collections import defaultdict, deque
from functools import wraps

import anthropic
from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.security import check_password_hash

import db
from chain_matcher import match_card_to_chain
from dedup import run_dedup
from extract import MODEL, extract_card_fields

app = Flask(__name__)
app.secret_key = os.environ.get("NAMECARD_SECRET_KEY", "")
IMAGE_FOLDER = os.environ.get("NAMECARD_FOLDER", "")

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# 公開上傳辨識：任何人都能丟名片照片，存檔後立即放行，不等辨識完成——
# 教練的構想是「不追求立即出結果，後台慢慢消化」，一次丟幾百張也不卡住使用者
PUBLIC_UPLOAD_FOLDER = os.path.join(_THIS_DIR, "public_uploads")
os.makedirs(PUBLIC_UPLOAD_FOLDER, exist_ok=True)
# 團隊從Amber私有雲上傳的名片，複製一份存本機，不依賴SMB即時掛載狀態
TEAM_UPLOAD_FOLDER = os.path.join(_THIS_DIR, "team_uploads")
os.makedirs(TEAM_UPLOAD_FOLDER, exist_ok=True)
ALLOWED_UPLOAD_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 單檔15MB，防單一異常大檔案
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 單次請求總量500MB，容納大量批次上傳

# 節流只是防對外公開端點被腳本瞬間灌爆導致資料庫塞垃圾/惡意資料，
# 門檻設得夠寬鬆，不擋教練團隊一次上傳整批名片相簿的正常使用情境
_upload_log: dict[str, deque] = defaultdict(deque)
RATE_LIMIT_COUNT = 2000
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


@app.route("/image/<path:filename>")
def serve_image(filename):
    """名片原始照片，供搜尋頁核對辨識結果用。public_開頭是公開上傳的，存在
    public_uploads；其餘是團隊從Amber私有雲上傳的，已複製一份到本機team_uploads
    (不依賴SMB即時掛載，掛載斷線也看得到既有照片)。"""
    if "/" in filename or ".." in filename:
        abort(404)
    if filename.startswith("public_"):
        return send_from_directory(PUBLIC_UPLOAD_FOLDER, filename)
    if os.path.exists(os.path.join(TEAM_UPLOAD_FOLDER, filename)):
        return send_from_directory(TEAM_UPLOAD_FOLDER, filename)
    if IMAGE_FOLDER and os.path.exists(os.path.join(IMAGE_FOLDER, filename)):
        return send_from_directory(IMAGE_FOLDER, filename)
    abort(404)


@app.route("/card/<int:card_id>/match", methods=["GET", "POST"])
def card_match(card_id):
    """點一下「媒合」：如果這張名片還沒分析過，當場呼叫AI判斷一次並存起來；
    已經分析過的直接顯示既有結果，不重複觸發(避免公開端點被重複濫用)。"""
    conn = db.get_conn()
    card = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    if card is None:
        conn.close()
        return "找不到這張名片", 404

    existing = conn.execute(
        """SELECT cm.role_name, ic.id AS chain_id, ic.name AS chain_name, ic.core_theme
           FROM chain_members cm JOIN industry_chains ic ON ic.id = cm.chain_id
           WHERE cm.card_id = ?""",
        (card_id,),
    ).fetchall()

    match_error = None
    if not existing and card["status"] in ("ok", "needs_review"):
        try:
            client = anthropic.Anthropic()
            match_card_to_chain(conn, client, card_id, MODEL)
            existing = conn.execute(
                """SELECT cm.role_name, ic.id AS chain_id, ic.name AS chain_name, ic.core_theme
                   FROM chain_members cm JOIN industry_chains ic ON ic.id = cm.chain_id
                   WHERE cm.card_id = ?""",
                (card_id,),
            ).fetchall()
        except Exception as e:  # noqa: BLE001
            match_error = str(e)

    # 同一條產業鏈裡，這張名片以外的其他角色位置(已補位或待招募)，方便看出可以合作誰
    chains_detail = []
    for row in existing:
        members = conn.execute(
            """SELECT cm.role_name, cm.is_gap, c.name AS card_name, c.company AS card_company
               FROM chain_members cm LEFT JOIN cards c ON c.id = cm.card_id
               WHERE cm.chain_id = ? AND cm.card_id IS NOT ? """,
            (row["chain_id"], card_id),
        ).fetchall()
        chains_detail.append({"chain": row, "other_members": members})

    conn.close()
    return render_template(
        "card_match.html", card=card, chains_detail=chains_detail, match_error=match_error,
        analyzed=bool(existing) or card["status"] not in ("ok", "needs_review"),
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


@app.route("/card/<int:card_id>/delete", methods=["POST"])
@team_login_required
def card_delete(card_id):
    conn = db.get_conn()
    db.delete_card(conn, card_id)
    conn.close()
    return redirect(url_for("index"))


@app.route("/card/<int:card_id>/edit", methods=["GET", "POST"])
@team_login_required
def card_edit(card_id):
    conn = db.get_conn()
    if request.method == "POST":
        keywords_raw = (request.form.get("keywords") or "").strip()
        fields = {
            "name": (request.form.get("name") or "").strip() or None,
            "title": (request.form.get("title") or "").strip() or None,
            "company": (request.form.get("company") or "").strip() or None,
            "mobile": (request.form.get("mobile") or "").strip() or None,
            "landline": (request.form.get("landline") or "").strip() or None,
            "email": (request.form.get("email") or "").strip() or None,
            "line_id": (request.form.get("line_id") or "").strip() or None,
            "website": (request.form.get("website") or "").strip() or None,
            "address": (request.form.get("address") or "").strip() or None,
            "tagline": (request.form.get("tagline") or "").strip() or None,
            "category": (request.form.get("category") or "").strip() or None,
            "standard_category": (request.form.get("standard_category") or "").strip() or None,
            "keywords": [k.strip() for k in keywords_raw.split("、") if k.strip()],
        }
        db.update_card_manual(conn, card_id, fields)
        conn.close()
        return redirect(url_for("index"))

    card = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    conn.close()
    if card is None:
        return "找不到這張名片", 404
    keywords = []
    try:
        keywords = json.loads(card["keywords"] or "[]")
    except json.JSONDecodeError:
        pass
    return render_template("card_edit.html", card=card, keywords_text="、".join(keywords))


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
        return render_template("upload.html", error="上傳太頻繁了，請稍後再試")

    files = [f for f in request.files.getlist("photos") if f and f.filename]
    if not files:
        return render_template("upload.html", error="請選擇至少一張名片照片")

    conn = db.get_conn()
    saved_count = 0
    skipped = []
    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        if ext not in ALLOWED_UPLOAD_EXTS:
            skipped.append(f.filename)
            continue
        saved_name = f"public_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
        saved_path = os.path.join(PUBLIC_UPLOAD_FOLDER, saved_name)
        f.save(saved_path)
        db.insert_card_pending(conn, saved_name)
        saved_count += 1
    conn.close()

    if saved_count > 0:
        # 非阻塞觸發背景worker，不等它處理完就直接回應——上傳這個動作本身就是
        # 事件觸發點，不是定時輪詢；子行程繼承父行程環境變數(含.env裡的API金鑰)
        subprocess.Popen(
            [sys.executable, os.path.join(_THIS_DIR, "process_pending.py"), "--limit", str(saved_count)],
            cwd=_THIS_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return render_template("upload_result.html", saved_count=saved_count, skipped=skipped)


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("NAMECARD_PORT", 5050)))
