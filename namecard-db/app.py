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
from urllib.parse import urlencode

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

    sql = "SELECT * FROM cards WHERE status != 'split'"
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
        "index.html", cards=cards, categories=categories, query=query, selected_category=category,
        logged_in=bool(session.get("team_username")),
    )


HEIC_CACHE_FOLDER = os.path.join(_THIS_DIR, "heic_cache")
os.makedirs(HEIC_CACHE_FOLDER, exist_ok=True)


@app.route("/image/<path:filename>")
def serve_image(filename):
    """名片原始照片，供搜尋頁核對辨識結果用。public_開頭是公開上傳的，存在
    public_uploads；其餘是團隊從Amber私有雲上傳的，已複製一份到本機team_uploads
    (不依賴SMB即時掛載，掛載斷線也看得到既有照片)。iPhone拍的HEIC瀏覽器無法
    原生顯示，即時轉JPEG並快取，避免每次重轉。"""
    if "/" in filename or ".." in filename:
        abort(404)
    if filename.startswith("public_"):
        base_folder = PUBLIC_UPLOAD_FOLDER
    elif os.path.exists(os.path.join(TEAM_UPLOAD_FOLDER, filename)):
        base_folder = TEAM_UPLOAD_FOLDER
    elif IMAGE_FOLDER and os.path.exists(os.path.join(IMAGE_FOLDER, filename)):
        base_folder = IMAGE_FOLDER
    else:
        abort(404)

    ext = os.path.splitext(filename)[1].lower()
    if ext not in (".heic", ".heif"):
        return send_from_directory(base_folder, filename)

    cache_name = filename + ".jpg"
    cache_path = os.path.join(HEIC_CACHE_FOLDER, cache_name)
    if not os.path.exists(cache_path):
        import pillow_heif
        from PIL import Image

        pillow_heif.register_heif_opener()
        img = Image.open(os.path.join(base_folder, filename)).convert("RGB")
        img.thumbnail((900, 900))
        img.save(cache_path, format="JPEG", quality=88)
    return send_from_directory(HEIC_CACHE_FOLDER, cache_name, mimetype="image/jpeg")


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
            """SELECT cm.id AS member_id, cm.card_id, cm.role_name, cm.is_gap,
                      c.name AS card_name, c.company AS card_company,
                      c.bni_status AS card_bni_status, c.bni_note AS card_bni_note
               FROM chain_members cm LEFT JOIN cards c ON c.id = cm.card_id
               WHERE cm.chain_id = ? AND cm.card_id IS NOT ? """,
            (row["chain_id"], card_id),
        ).fetchall()
        chains_detail.append({"chain": row, "other_members": members})

    conn.close()
    return render_template(
        "card_match.html", card=card, chains_detail=chains_detail, match_error=match_error,
        analyzed=bool(existing) or card["status"] not in ("ok", "needs_review"),
        logged_in=bool(session.get("team_username")),
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
    return render_template("chains.html", chains=chains, logged_in=bool(session.get("team_username")))


@app.route("/find")
def find_page():
    """簡約搜尋頁：教練打一個關鍵字，同時查cards(名片/BNI會員)+guests(來賓)，
    每筆結果都有「媒合」按鈕——按下去才呼叫AI，平常瀏覽/搜尋完全不耗MiniMax額度。"""
    query = request.args.get("q", "").strip()
    results = []
    if query:
        conn = db.get_conn()
        like = f"%{query}%"
        card_rows = conn.execute(
            """SELECT id, name, title, company, mobile, email, bni_status, bni_note
               FROM cards
               WHERE status != 'failed'
                 AND (name LIKE ? OR company LIKE ? OR title LIKE ?
                      OR standard_category LIKE ? OR category LIKE ?
                      OR mobile LIKE ? OR email LIKE ?)
               ORDER BY name""",
            (like, like, like, like, like, like, like),
        ).fetchall()
        guest_rows = conn.execute(
            """SELECT id, name, profession, company, mobile, email, chapter
               FROM guests
               WHERE name LIKE ? OR company LIKE ? OR profession LIKE ?
                     OR mobile LIKE ? OR email LIKE ?
               ORDER BY name""",
            (like, like, like, like, like),
        ).fetchall()
        conn.close()
        for r in card_rows:
            results.append({"source": "card", **dict(r)})
        for r in guest_rows:
            d = dict(r)
            results.append({
                "source": "guest", "id": d["id"], "name": d["name"],
                "title": d["profession"], "company": d["company"],
                "mobile": d["mobile"], "email": d["email"], "bni_note": d["chapter"],
            })
    return render_template("find.html", query=query, results=results)


@app.route("/guest/<int:guest_id>/match")
def guest_match(guest_id):
    """來賓版「媒合」入口：第一次點擊才把這位來賓轉成一筆card(用source_guest_id
    記住避免重複轉入)，接著直接沿用既有card媒合流程，不重造一套邏輯。"""
    conn = db.get_conn()
    guest = conn.execute("SELECT * FROM guests WHERE id = ?", (guest_id,)).fetchone()
    if guest is None:
        conn.close()
        return "找不到這位來賓", 404

    existing_card = conn.execute(
        "SELECT id FROM cards WHERE source_guest_id = ?", (guest_id,)
    ).fetchone()
    if existing_card:
        card_id = existing_card["id"]
    else:
        bni_note = f"BNI來賓・{guest['chapter']}分會" if guest["chapter"] else "BNI來賓"
        cur = conn.execute(
            """INSERT INTO cards
               (image_filename, name, company, category, standard_category,
                mobile, email, bni_status, bni_note, status, source_guest_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'unknown', ?, 'ok', ?)""",
            (
                f"guest__{guest_id}", guest["name"], guest["company"],
                guest["profession"], guest["profession"],
                guest["mobile"], guest["email"], bni_note, guest_id,
            ),
        )
        conn.commit()
        card_id = cur.lastrowid
    conn.close()
    return redirect(url_for("card_match", card_id=card_id))


def team_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("team_username"):
            return redirect(url_for("team_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


# 教練專屬頁面（如BNI信用証追蹤）：夥伴帳號(如佩君老師)登入team系統後不能看，
# 只有教練本人的帳號能進，跟「名片系統」開放給夥伴的權限刻意分開
OWNER_USERNAME = "bymyway"


def owner_only_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("team_username"):
            return redirect(url_for("team_login", next=request.path))
        if session.get("team_username") != OWNER_USERNAME:
            return "此頁面僅限教練本人查看", 403
        return view(*args, **kwargs)
    return wrapped


@app.route("/card/<int:card_id>/bni_status", methods=["POST"])
@team_login_required
def card_bni_status(card_id):
    """標記這張名片(已有真實聯絡資料的人)是否為BNI會員。只套用在真實名片上，
    不套用在AI建議的抽象待招募角色——沒聯絡方式標了也聯絡不到，沒有意義(教練親定)。"""
    bni_status = request.form.get("bni_status", "unknown")
    bni_note = (request.form.get("bni_note") or "").strip()
    if bni_status not in ("unknown", "bni_member", "not_bni"):
        bni_status = "unknown"
    conn = db.get_conn()
    db.update_card_bni_status(conn, card_id, bni_status, bni_note)
    conn.close()
    return redirect(request.referrer or url_for("index"))


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


# BNI信用証追蹤：cert_status/usage_status兩個資料庫欄位合併成單一「狀態」給教練操作，
# 內部拆解成兩欄寫回；教練切換狀態不清空cert_id/issue_date等既有查證資料，切回去時仍看得到原始紀錄。
BNI_CREDIT_STATUS_MAP = {
    "not_issued": {"cert_status": "not_issued", "usage_status": None},
    "ineligible": {"cert_status": "ineligible", "usage_status": None},
    "active": {"cert_status": "issued", "usage_status": "active"},
    "expired": {"cert_status": "issued", "usage_status": "expired"},
    "redeemed": {"cert_status": "issued", "usage_status": "redeemed"},
    "transferred": {"cert_status": "issued", "usage_status": "transferred"},
}
BNI_CREDIT_STATUS_LABELS = {
    "active": "✅ 有效",
    "expired": "⏰ 已過期",
    "not_issued": "⬜ 未開立",
    "redeemed": "💰 已贖回",
    "transferred": "↪️ 已轉移",
    "ineligible": "🈳 沒有額度",
}
BNI_CREDIT_STATUS_ORDER = ["active", "expired", "not_issued", "redeemed", "transferred", "ineligible"]
# 表頭可點擊排序的欄位，key跟前端<a href>帶的sort參數一致；expiry_date/status_key
# 排序時特別取代成實際比較用的值(見bni_credit_list()裡的_sort_value)
BNI_CREDIT_SORTABLE_FIELDS = {
    "chapter", "name", "company", "credit_months", "issue_date", "expiry_date", "status_key",
}


def _bni_credit_status_key(cert_status, usage_status):
    if cert_status == "issued":
        return usage_status or "active"
    return cert_status


@app.route("/bni-credit")
@owner_only_required
def bni_credit_list():
    from datetime import date

    selected_statuses = request.args.getlist("status") or ["active", "expired", "not_issued"]
    selected_chapters = request.args.getlist("chapter")
    query = (request.args.get("q") or "").strip()

    conn = db.get_conn()
    chapters = [
        r["chapter"]
        for r in conn.execute("SELECT DISTINCT chapter FROM bni_credit_certificates ORDER BY chapter").fetchall()
    ]
    rows = conn.execute("SELECT * FROM bni_credit_certificates").fetchall()
    conn.close()

    today = date.today()
    records = []
    for r in rows:
        status_key = _bni_credit_status_key(r["cert_status"], r["usage_status"])
        if status_key not in selected_statuses:
            continue
        if selected_chapters and r["chapter"] not in selected_chapters:
            continue
        if query and query not in (r["name"] or "") and query not in (r["company"] or ""):
            continue

        remaining_days = None
        remaining_months = None
        urgency = 9
        if status_key == "active" and r["expiry_date"]:
            try:
                y, m, d = (int(x) for x in r["expiry_date"].split("-"))
                remaining_days = (date(y, m, d) - today).days
                remaining_months = round(remaining_days / 30.44, 1)
            except ValueError:
                remaining_days = None
        remain_tier = None
        if status_key == "active":
            if remaining_days is None:
                urgency = 1
                remain_tier = "urgent"
            elif remaining_days < 0:
                urgency = 0
                remain_tier = "overdue"
            elif remaining_days < 91:
                urgency = 1
                remain_tier = "urgent"
            elif remaining_days < 183:
                urgency = 2
                remain_tier = "hot"
            elif remaining_days < 365:
                urgency = 3
                remain_tier = "warn"
            else:
                urgency = 4
                remain_tier = "ok"
        else:
            urgency = {
                "expired": 5, "not_issued": 6, "transferred": 7, "redeemed": 8, "ineligible": 9,
            }.get(status_key, 10)

        record = dict(r)
        record["status_key"] = status_key
        record["status_label"] = BNI_CREDIT_STATUS_LABELS.get(status_key, status_key)
        record["remaining_days"] = remaining_days
        record["remaining_months"] = remaining_months
        record["remain_tier"] = remain_tier
        record["urgency"] = urgency
        records.append(record)

    sort_key = request.args.get("sort") or ""
    sort_dir = request.args.get("dir") or "asc"
    if sort_key in BNI_CREDIT_SORTABLE_FIELDS:
        def _sort_value(r):
            if sort_key == "expiry_date":
                return r.get("expiry_date") or r.get("scheduled_end_date")
            if sort_key == "status_key":
                return r.get("status_label")
            return r.get(sort_key)

        with_value = [r for r in records if _sort_value(r) not in (None, "")]
        without_value = [r for r in records if _sort_value(r) in (None, "")]
        with_value.sort(key=_sort_value, reverse=(sort_dir == "desc"))
        records = with_value + without_value
    else:
        sort_key = ""
        records.sort(key=lambda r: (r["urgency"], r["remaining_days"] if r["remaining_days"] is not None else 99999, r["name"]))

    counts_conn = db.get_conn()
    all_rows = counts_conn.execute("SELECT cert_status, usage_status FROM bni_credit_certificates").fetchall()
    counts_conn.close()
    status_counts = {k: 0 for k in BNI_CREDIT_STATUS_ORDER}
    for r in all_rows:
        k = _bni_credit_status_key(r["cert_status"], r["usage_status"])
        status_counts[k] = status_counts.get(k, 0) + 1

    def sort_url(field):
        params = []
        for s in selected_statuses:
            params.append(("status", s))
        for c in selected_chapters:
            params.append(("chapter", c))
        if query:
            params.append(("q", query))
        next_dir = "desc" if (sort_key == field and sort_dir == "asc") else "asc"
        params.append(("sort", field))
        params.append(("dir", next_dir))
        return "?" + urlencode(params)

    return render_template(
        "bni_credit.html",
        records=records,
        chapters=chapters,
        selected_statuses=selected_statuses,
        selected_chapters=selected_chapters,
        query=query,
        status_labels=BNI_CREDIT_STATUS_LABELS,
        status_order=BNI_CREDIT_STATUS_ORDER,
        status_counts=status_counts,
        sort_key=sort_key,
        sort_dir=sort_dir,
        sort_url=sort_url,
        display_name=session.get("team_display_name"),
    )


@app.route("/bni-credit/<int:record_id>/status", methods=["POST"])
@owner_only_required
def bni_credit_update_status(record_id):
    new_status = request.form.get("status_key")
    mapping = BNI_CREDIT_STATUS_MAP.get(new_status)
    if mapping is None:
        return redirect(request.referrer or url_for("bni_credit_list"))
    conn = db.get_conn()
    conn.execute(
        "UPDATE bni_credit_certificates SET cert_status = ?, usage_status = ? WHERE id = ?",
        (mapping["cert_status"], mapping["usage_status"], record_id),
    )
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("bni_credit_list"))


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
