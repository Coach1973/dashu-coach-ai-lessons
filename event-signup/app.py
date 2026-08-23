"""
活動報名網頁。跑法：python app.py（預設 port 5060，比照名片系統用獨立Cloudflare通道對外開）
來賓掃QR → /e/<slug> 填表 → 感謝頁（加LINE好友）；教練看名單 → /admin（帳密登入，見/admin/login）
"""
import base64
import csv
import hashlib
import hmac
import io
import json
import os
import re
import urllib.error
import urllib.request
from datetime import date, datetime
from urllib.parse import quote

from flask import Flask, Response, abort, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.security import check_password_hash

import db


def _sanitize_filename(raw: str) -> str:
    """保留中文檔名（簡報標題常是中文），只擋掉路徑穿越與危險字元。
    不能直接用werkzeug的secure_filename——它會把中文整段砍掉，
    「2026-07-16-AI微型論壇.pdf」會變成「2026-07-16-AI.pdf」，日期後的說明文字全部消失。"""
    name = os.path.basename(raw).replace("\x00", "")
    name = re.sub(r'[/\\:*?"<>|]', "", name)
    return name.strip() or "file"

app = Flask(__name__)
app.secret_key = os.environ.get("EVENT_SECRET_KEY", "")
ADMIN_USER = os.environ.get("EVENT_ADMIN_USER", "")
ADMIN_PASSWORD_HASH = os.environ.get("EVENT_ADMIN_PASSWORD_HASH", "")
LINE_OA_ID = os.environ.get("EVENT_LINE_OA_ID", "@qaw8118h")
LINE_CHANNEL_SECRET = os.environ.get("EVENT_LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("EVENT_LINE_CHANNEL_ACCESS_TOKEN", "")


def _lottery_greet_url(name: str, event_name: str) -> str:
    """組出「加好友同時帶問候語」的LINE連結：對方點開LINE就看到預填好的訊息，
    按下傳送才算完成binding+登記抽獎（webhook比對這句話裡的姓名寫入line_user_id）。"""
    greet_text = (
        f"我是{name}，剛報名了{event_name}。"
        f"我要現場立即參加抽獎（送出才算登記成功）"
    )
    return f"https://line.me/R/oaMessage/{LINE_OA_ID}/?{quote(greet_text)}"

GREET_PATTERN = re.compile(r"^我是(.+?)，剛報名了")

SLIDES_DIR = os.path.join(os.path.dirname(__file__), "slides")
OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
TELEGRAM_NOTIFY_CHAT_ID = "6124913915"  # 教練跟小龍蝦的對話，路徑大全.md已記錄
COACH_LINE_USER_ID = "U895a0ad8e49d75f8303dc3d067282dc0"  # 教練本人LINE ID，workspace/memory/people.md已記錄


def _notify_coach_line(text: str) -> bool:
    """用龍蝦小助教（@268dptjc，OpenClaw預設LINE帳號）推播訊息給教練本人LINE。
    2026-08-14教練要求：長期要把報名通知改由bymyway.com自己發，不能只靠外部Netlify黑箱
    (sme-register-fn)。跟_notify_xiaolongxia()是同一等級的通知，只是換LINE通道，
    token直接讀openclaw.json（跟default帳號共用同一份，不新增憑證檔）。"""
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        token = config["channels"]["line"]["channelAccessToken"]
        body = json.dumps({
            "to": COACH_LINE_USER_ID,
            "messages": [{"type": "text", "text": text}],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.line.me/v2/bot/message/push", data=body, method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False  # 通知失敗不該擋住報名資料落地，呼叫端不拋錯


def _notify_xiaolongxia(text: str) -> None:
    """發Telegram訊息給小龍蝦（教練本人的對話），失敗不影響網頁本身回應。"""
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        bot_token = config["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": TELEGRAM_NOTIFY_CHAT_ID, "text": text}).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass  # 通知失敗不該擋住聽眾拿到簡報


@app.route("/")
def root():
    return redirect("https://coach1973.github.io/ai-talk/")


QR_DIR = os.path.join(os.path.dirname(__file__), "qr")


@app.route("/qr/<path:filename>")
def qr_file(filename):
    return send_from_directory(QR_DIR, filename)


@app.route("/checkin", methods=["GET"])
def checkin():
    """固定不變的報到入口，QR立牌永久印這個網址。後台切哪場是「目前活動」，
    這裡就自動導去那場的簽到頁，不用重印立牌。
    2026-07-28教練指出來賓線上報名時已留過姓名/電話，現場只需要再輸入手機號碼比對身份即可，
    不用整份表單重填一次——比對成功才算「簽到」，一樣會記進signups表供集點使用。"""
    conn = db.get_conn()
    event = db.get_current_event(conn)
    conn.close()
    if not event:
        return "目前沒有進行中的活動，請稍後再試", 404
    return render_template("checkin.html", event=event, error=None, phone="")


@app.route("/checkin", methods=["POST"])
def checkin_submit():
    conn = db.get_conn()
    event = db.get_current_event(conn)
    if not event:
        conn.close()
        return "目前沒有進行中的活動，請稍後再試", 404

    phone_raw = (request.form.get("phone") or "").strip()
    phone = db.normalize_phone(phone_raw)

    if not (phone.startswith("09") and len(phone) == 10):
        conn.close()
        return render_template(
            "checkin.html", event=event, phone=phone_raw,
            error="手機號碼格式不對，請確認是 09 開頭的 10 碼",
        ), 400

    row = conn.execute(
        "SELECT id, name, company_title FROM attendees WHERE phone = ?", (phone,)
    ).fetchone()
    if not row:
        conn.close()
        # 查無報名資料（現場臨時來、沒事先線上報名的人）：導去完整報名表單，手機號碼先幫他帶進去
        return redirect(url_for("signup_form", slug=event["slug"], phone=phone))

    db.upsert_signup(conn, event["id"], row["name"], phone, row["company_title"] or "")
    conn.close()
    # 2026-08-10教練指示：不要停在「簽到成功」中繼畫面等他再按一次加好友，
    # 填手機送出的同一步直接跳進LINE把問候語準備好，按傳送就同時完成binding+登記抽獎。
    return redirect(_lottery_greet_url(row["name"], event["name"]))


def _resolve_current_slide(conn) -> str | None:
    """回傳目前應該給出的簡報檔名（slides/資料夾裡的檔名），找不到回傳None。
    auto模式：抓檔名開頭是今天日期(YYYY-MM-DD)的檔案；manual模式：後台指定的那個檔案。"""
    mode = db.get_slides_mode(conn)
    if mode == "manual":
        fname = db.get_manual_slide_file(conn)
        if fname and os.path.exists(os.path.join(SLIDES_DIR, fname)):
            return fname
        return None
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.isdir(SLIDES_DIR):
        for fname in sorted(os.listdir(SLIDES_DIR)):
            if fname.startswith(today):
                return fname
    return None


@app.route("/slides")
def slides_landing():
    """簡報最後QR掃碼進來的頁面：加LINE好友 + 下載今天的簡報，同時通知小龍蝦。
    固定網址，不用因為每次簡報不同而重印QR——後台換今天的檔案就好。
    name（選填）：從/checkin手機比對成功導過來時會帶上，顯示個人化歡迎文字；
    直接掃簡報QR進來（原本流程）不會帶這個參數，維持原本「感謝聆聽」文字。"""
    conn = db.get_conn()
    fname = _resolve_current_slide(conn)
    event = db.get_current_event(conn)
    conn.close()

    name = (request.args.get("name") or "").strip()

    _notify_xiaolongxia(
        f"📊 有人{'簽到' if name else '掃了簡報QR碼'}\n"
        f"{f'姓名：{name}' + chr(10) if name else ''}"
        f"檔案：{fname or '（尚未設定今日簡報）'}\n時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    add_friend_url = f"https://line.me/R/ti/p/{LINE_OA_ID}"
    # 2026-07-29教練發現：現場簽到的人綁定率遠低於線上報名的人（56簽到只有12綁定），
    # 原因是這裡原本只給普通加好友連結，要來賓自己手動打「我是OOO，剛報名了XXX」才會綁定，
    # 而/e/<slug>/thanks頁面（線上報名走的那頁）早就有幫忙打好問候語的greet_url。
    # 這裡補上同一套邏輯，讓現場簽到的人也能一鍵完成綁定。
    if name and event:
        add_friend_url = _lottery_greet_url(name, event["name"])

    return render_template(
        "slides.html", add_friend_url=add_friend_url, has_slide=bool(fname), name=name,
        download_url=url_for("slides_download") if fname else None,
    )


@app.route("/slides/download")
def slides_download():
    conn = db.get_conn()
    fname = _resolve_current_slide(conn)
    conn.close()
    if not fname:
        return "今天還沒有設定簡報檔，請洽大樹教練", 404
    return send_from_directory(SLIDES_DIR, fname, as_attachment=True)


@app.route("/admin/slides-upload", methods=["POST"])
def slides_upload():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    file = request.files.get("slide_file")
    if file and file.filename:
        os.makedirs(SLIDES_DIR, exist_ok=True)
        safe_name = _sanitize_filename(file.filename)
        file.save(os.path.join(SLIDES_DIR, safe_name))
    return redirect(url_for("admin"))


@app.route("/admin/slides-set-mode", methods=["POST"])
def slides_set_mode():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    mode = (request.form.get("mode") or "auto").strip()
    conn = db.get_conn()
    if mode == "manual":
        fname = (request.form.get("manual_file") or "").strip()
        if fname:
            db.set_manual_slide_file(conn, fname)
        db.set_slides_mode(conn, "manual")
    else:
        db.set_slides_mode(conn, "auto")
    conn.close()
    return redirect(url_for("admin"))


@app.route("/e/<slug>", methods=["GET"])
def signup_form(slug):
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    conn.close()
    if not event:
        abort(404)
    # phone（選填）：從/checkin查無資料時會帶上，先幫現場臨時報名的人把手機號碼帶進表單，
    # 不用手機、姓名兩個都重打一次
    prefill_phone = (request.args.get("phone") or "").strip()
    return render_template("form.html", event=event, error=None, form={"phone": prefill_phone})


@app.route("/e/<slug>", methods=["POST"])
def signup_submit(slug):
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    if not event:
        conn.close()
        abort(404)

    name = (request.form.get("name") or "").strip()
    phone_raw = (request.form.get("phone") or "").strip()
    company_title = (request.form.get("company_title") or "").strip()
    phone = db.normalize_phone(phone_raw)

    error = None
    if not name:
        error = "請填寫姓名"
    elif not (phone.startswith("09") and len(phone) == 10):
        error = "手機號碼格式不對，請確認是 09 開頭的 10 碼"

    if error:
        conn.close()
        return render_template(
            "form.html", event=event, error=error,
            form={"name": name, "phone": phone_raw, "company_title": company_title},
        ), 400

    status = db.upsert_signup(conn, event["id"], name, phone, company_title)
    conn.close()
    return redirect(url_for("thanks", slug=slug, s=status, n=name))


@app.route("/api/register", methods=["POST", "OPTIONS"])
def api_register():
    """給外部網站（大樹小講等）跨網域直接寫入報名資料用的輕量JSON端點。
    2026-08-14教練裁示：報名資料要落地在bymyway.com自己的資料庫，不能只活在LINE/Telegram通知訊息裡。
    跟原本/e/<slug>的HTML表單流程共用db.upsert_signup()同一套邏輯，但走JSON+CORS，給fetch()呼叫用。
    設計成雙寫並存期的其中一路：外部網站原本呼叫的Netlify通知(sme-register-fn/xiaolongxia-notify)
    完全不動，這支只是「多一路」，任何失敗都不能影響訪客報名體驗——所以永遠回200，錯誤只記log不拋出。
    """
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    try:
        payload = request.get_json(force=True, silent=True) or {}
        slug = (payload.get("slug") or "").strip()
        name = (payload.get("name") or "").strip()
        phone_raw = (payload.get("phone") or "").strip()
        company_title = (payload.get("company") or "").strip()
        email = (payload.get("email") or "").strip()

        if not slug or not name or not phone_raw:
            return Response(
                json.dumps({"ok": False, "error": "missing slug/name/phone"}),
                status=200, headers={**resp_headers, "Content-Type": "application/json"},
            )

        phone = db.normalize_phone(phone_raw)
        conn = db.get_conn()
        event = db.get_event(conn, slug)
        if not event:
            conn.close()
            return Response(
                json.dumps({"ok": False, "error": f"unknown slug: {slug}"}),
                status=200, headers={**resp_headers, "Content-Type": "application/json"},
            )

        status = db.upsert_signup(conn, event["id"], name, phone, company_title, email)
        event_name = event["name"]
        conn.close()
        _notify_coach_line(
            f"【大樹小講・官網報名】\n場次：{event_name}\n姓名：{name}\n"
            f"公司：{company_title or '-'}\n電話：{phone}\nEmail：{email or '未填'}\n"
            f"（{'新報名' if status == 'new' else '同場次重複報名'}，由bymyway.com官方發送）"
        )
        return Response(
            json.dumps({"ok": True, "status": status}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )
    except Exception as e:
        # 任何未預期錯誤都不能讓訪客報名體驗中斷（這支是雙寫的其中一路，不是唯一路徑）
        return Response(
            json.dumps({"ok": False, "error": str(e)}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )


@app.route("/e/<slug>/thanks")
def thanks(slug):
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    conn.close()
    if not event:
        abort(404)
    repeat = request.args.get("s") == "repeat"
    name = (request.args.get("n") or "").strip()

    add_friend_url = f"https://line.me/R/ti/p/{LINE_OA_ID}"
    greet_url = add_friend_url
    if name:
        greet_text = f"我是{name}，剛報名了{event['name']}"
        greet_url = f"https://line.me/R/oaMessage/{LINE_OA_ID}/?{quote(greet_text)}"

    return render_template(
        "thanks.html", event=event, repeat=repeat,
        add_friend_url=add_friend_url, greet_url=greet_url,
    )


def _verify_line_signature(body: bytes, signature: str) -> bool:
    if not LINE_CHANNEL_SECRET or not signature:
        return False
    expected = base64.b64encode(
        hmac.new(LINE_CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256).digest()
    ).decode("utf-8")
    return hmac.compare_digest(expected, signature)


@app.route("/line/webhook", methods=["POST"])
def line_webhook():
    body = request.get_data()
    signature = request.headers.get("X-Line-Signature", "")
    if not _verify_line_signature(body, signature):
        abort(403)

    payload = json.loads(body)
    conn = db.get_conn()
    for event in payload.get("events", []):
        if event.get("type") != "message":
            continue
        message = event.get("message", {})
        if message.get("type") != "text":
            continue
        text = (message.get("text") or "").strip()
        line_user_id = event.get("source", {}).get("userId")
        if not line_user_id:
            continue
        m = GREET_PATTERN.match(text)
        if m:
            db.match_line_identity(conn, m.group(1).strip(), line_user_id)
    conn.close()
    return "", 200


def _logged_in() -> bool:
    return bool(session.get("logged_in"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if (
        ADMIN_USER and ADMIN_PASSWORD_HASH
        and username == ADMIN_USER
        and check_password_hash(ADMIN_PASSWORD_HASH, password)
    ):
        session["logged_in"] = True
        session.permanent = True
        return redirect(request.args.get("next") or url_for("admin"))
    return render_template("login.html", error="帳號或密碼不對，請再試一次"), 401


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


def _line_push(line_user_id: str, text: str) -> bool:
    body = json.dumps({"to": line_user_id, "messages": [{"type": "text", "text": text}]}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push", data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.HTTPError:
        return False


@app.route("/admin/notify", methods=["GET"])
def notify_form():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    events = conn.execute(
        """SELECT e.*, COUNT(s.id) AS signup_count,
                  SUM(CASE WHEN a.line_user_id IS NOT NULL THEN 1 ELSE 0 END) AS line_bound_count
           FROM events e
           LEFT JOIN signups s ON s.event_id = e.id
           LEFT JOIN attendees a ON a.id = s.attendee_id
           GROUP BY e.id ORDER BY e.event_date DESC"""
    ).fetchall()
    conn.close()
    return render_template("notify.html", events=events, result=None)


@app.route("/admin/notify", methods=["POST"])
def notify_send():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    if not LINE_CHANNEL_ACCESS_TOKEN:
        abort(500)

    slug = (request.form.get("event") or "").strip()
    message = (request.form.get("message") or "").strip()

    conn = db.get_conn()
    events = conn.execute(
        """SELECT e.*, COUNT(s.id) AS signup_count,
                  SUM(CASE WHEN a.line_user_id IS NOT NULL THEN 1 ELSE 0 END) AS line_bound_count
           FROM events e
           LEFT JOIN signups s ON s.event_id = e.id
           LEFT JOIN attendees a ON a.id = s.attendee_id
           GROUP BY e.id ORDER BY e.event_date DESC"""
    ).fetchall()

    result = None
    if slug and message:
        recipients = conn.execute(
            """SELECT a.line_user_id FROM attendees a
               JOIN signups s ON s.attendee_id = a.id
               JOIN events e ON e.id = s.event_id
               WHERE e.slug = ? AND a.line_user_id IS NOT NULL""",
            (slug,),
        ).fetchall()
        sent, failed = 0, 0
        for r in recipients:
            if _line_push(r["line_user_id"], message):
                sent += 1
            else:
                failed += 1
        result = {"sent": sent, "failed": failed, "total": len(recipients)}
    conn.close()
    return render_template("notify.html", events=events, result=result)


@app.route("/admin/set-current", methods=["POST"])
def set_current():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    slug = (request.form.get("event") or "").strip()
    conn = db.get_conn()
    db.set_current_event(conn, slug)
    conn.close()
    return redirect(url_for("admin"))


@app.route("/admin/set-auto", methods=["POST"])
def set_auto():
    """恢復自動切換：/checkin 改回自動抓日期最接近的那場，不用每次手動點。"""
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    db.set_routing_mode(conn, "auto")
    conn.close()
    return redirect(url_for("admin"))


@app.route("/wheel")
def wheel():
    """抽獎轉盤：教練上台操作用，名單直接來自「目前活動」已簽到的人，不用手動輸入。
    跟/admin共用同一組登入session，登入過/admin這裡就不用再登一次。"""
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    event = db.get_current_event(conn)
    conn.close()
    if not event:
        return "目前沒有進行中的活動，請先到 /admin 設定", 404
    return render_template("wheel.html", event=event)


@app.route("/wheel/data")
def wheel_data():
    if not _logged_in():
        abort(401)
    conn = db.get_conn()
    event = db.get_current_event(conn)
    if not event:
        conn.close()
        return {"error": "目前沒有進行中的活動"}, 404
    roster = db.get_wheel_roster(conn, event["id"])
    winners = db.get_wheel_winners(conn, event["id"])
    prizes = db.get_wheel_prizes(conn, event["id"])
    conn.close()
    return {
        "event_name": event["name"],
        "roster": [{"id": r["id"], "name": r["name"]} for r in roster],
        "winners": [{"name": w["name"], "prize": w["prize"] or ""} for w in winners],
        "prizes": [
            {"id": p["id"], "name": p["name"], "remaining": p["remaining_qty"], "total": p["total_qty"]}
            for p in prizes
        ],
    }


@app.route("/wheel/winner", methods=["POST"])
def wheel_winner():
    if not _logged_in():
        abort(401)
    data = request.get_json(silent=True) or {}
    attendee_id = data.get("attendee_id")
    prize_id = data.get("prize_id")
    prize_text = (data.get("prize") or "").strip()
    if not attendee_id:
        return {"ok": False, "error": "缺少attendee_id"}, 400
    conn = db.get_conn()
    event = db.get_current_event(conn)
    if not event:
        conn.close()
        return {"ok": False, "error": "目前沒有進行中的活動"}, 404

    prize_name = prize_text
    if prize_id:
        prize_name = db.decrement_wheel_prize(conn, prize_id)
        if prize_name is None:
            conn.close()
            return {"ok": False, "error": "這個獎項已經發完了，請重新整理頁面選別的獎項"}, 409

    ok = db.add_wheel_winner(conn, event["id"], attendee_id, prize_name)
    conn.close()
    return {"ok": ok}


@app.route("/wheel/prizes/set", methods=["POST"])
def wheel_prizes_set():
    """整批設定目前活動的獎品清單，格式：每行「獎品名稱 數量」，例如「雲朵包 1」。"""
    if not _logged_in():
        abort(401)
    conn = db.get_conn()
    event = db.get_current_event(conn)
    if not event:
        conn.close()
        return {"ok": False, "error": "目前沒有進行中的活動"}, 404

    raw = (request.get_json(silent=True) or {}).get("text", "")
    prizes = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            prizes.append((parts[0].strip(), int(parts[1])))
        else:
            prizes.append((line, 1))

    db.set_wheel_prizes(conn, event["id"], prizes)
    conn.close()
    return {"ok": True, "count": len(prizes)}


@app.route("/wheel/reset", methods=["POST"])
def wheel_reset():
    if not _logged_in():
        abort(401)
    conn = db.get_conn()
    event = db.get_current_event(conn)
    if not event:
        conn.close()
        return {"ok": False, "error": "目前沒有進行中的活動"}, 404
    db.clear_wheel_winners(conn, event["id"])
    conn.close()
    return {"ok": True}


@app.route("/admin")
def admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    events = conn.execute(
        """SELECT e.*, COUNT(s.id) AS signup_count
           FROM events e LEFT JOIN signups s ON s.event_id = e.id
           GROUP BY e.id ORDER BY e.event_date DESC"""
    ).fetchall()

    selected = request.args.get("event", "").strip()
    sql = """SELECT a.name, a.phone, a.company_title, a.created_at,
                    a.line_user_id IS NOT NULL AS line_bound,
                    GROUP_CONCAT(e.name, '、') AS attended_events,
                    COUNT(DISTINCT s.event_id) AS event_count
             FROM attendees a
             JOIN signups s ON s.attendee_id = a.id
             JOIN events e ON e.id = s.event_id"""
    params = []
    if selected:
        sql += """ WHERE a.id IN (SELECT s2.attendee_id FROM signups s2
                   JOIN events e2 ON e2.id = s2.event_id WHERE e2.slug = ?)"""
        params.append(selected)
    sql += " GROUP BY a.id ORDER BY a.created_at DESC"
    attendees = conn.execute(sql, params).fetchall()
    current_event = db.get_current_event(conn)
    routing_mode = db.get_routing_mode(conn)
    slides_mode = db.get_slides_mode(conn)
    current_slide = _resolve_current_slide(conn)
    manual_slide = db.get_manual_slide_file(conn)
    conn.close()
    slide_files = sorted(os.listdir(SLIDES_DIR)) if os.path.isdir(SLIDES_DIR) else []
    return render_template(
        "admin.html", events=events, attendees=attendees,
        selected=selected, current_event=current_event, routing_mode=routing_mode,
        slides_mode=slides_mode, current_slide=current_slide,
        manual_slide=manual_slide, slide_files=slide_files,
    )


@app.route("/admin/export.csv")
def export_csv():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    rows = conn.execute(
        """SELECT a.name, a.phone, a.company_title, a.line_user_id IS NOT NULL AS line_bound,
                  GROUP_CONCAT(e.name, '、') AS attended_events, a.created_at
           FROM attendees a
           JOIN signups s ON s.attendee_id = a.id
           JOIN events e ON e.id = s.event_id
           GROUP BY a.id ORDER BY a.created_at"""
    ).fetchall()
    conn.close()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["姓名", "手機", "公司／職稱", "參加過的活動", "首次留資料時間", "LINE可通知"])
    for r in rows:
        writer.writerow([r["name"], r["phone"], r["company_title"] or "", r["attended_events"], r["created_at"],
                         "是" if r["line_bound"] else "否"])
    out = "﻿" + buf.getvalue()  # BOM讓Excel直接開不亂碼
    return Response(out, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=attendees.csv"})


# ---- 大樹小講場次管理（2026-08-23 教練交辦：以前改場次都要透過AI改網頁原始碼，
#      資料庫與網頁兩份各自維護必定會漏。改成資料庫當唯一真相源＋後台一鍵發佈） ----

@app.route("/admin/sessions")
def admin_sessions():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    import bigtree_publish as bp
    conn = db.get_conn()
    sessions = db.list_site_sessions(conn)
    summary = bp.diff_summary(conn)
    conn.close()
    return render_template(
        "sessions.html", sessions=sessions, slot_choices=bp.SLOT_CHOICES,
        summary=summary, live_count=len(summary["sessions"]),
        quota=bp.quota_remaining(), today=date.today().isoformat(),
        notice=request.args.get("notice", ""), error=request.args.get("error", ""),
    )


@app.route("/admin/sessions/save", methods=["POST"])
def admin_sessions_save():
    if not _logged_in():
        return redirect(url_for("admin_login"))
    raw_id = request.form.get("event_id", "").strip()
    conn = db.get_conn()
    ok, msg = db.save_session(conn, request.form.to_dict(), int(raw_id) if raw_id else None)
    conn.close()
    return redirect(url_for("admin_sessions", **({"notice": msg} if ok else {"error": msg})))


@app.route("/admin/sessions/status", methods=["POST"])
def admin_sessions_status():
    if not _logged_in():
        return redirect(url_for("admin_login"))
    conn = db.get_conn()
    db.set_session_status(conn, int(request.form["event_id"]), request.form.get("status", "active"))
    conn.close()
    return redirect(url_for("admin_sessions", notice="已更新狀態。記得按「發佈到官網」才會對外生效。"))


@app.route("/admin/sessions/delete", methods=["POST"])
def admin_sessions_delete():
    if not _logged_in():
        return redirect(url_for("admin_login"))
    conn = db.get_conn()
    ok, msg = db.delete_session(conn, int(request.form["event_id"]))
    conn.close()
    return redirect(url_for("admin_sessions", **({"notice": msg} if ok else {"error": msg})))


@app.route("/admin/sessions/publish", methods=["POST"])
def admin_sessions_publish():
    """教練本人按下按鈕＝本人授權，不需要再經過任何確認流程。"""
    if not _logged_in():
        return redirect(url_for("admin_login"))
    import bigtree_publish as bp
    conn = db.get_conn()
    result = bp.publish(conn, request.form.get("message", ""))
    conn.close()
    if result["ok"]:
        left = f"，剩餘額度約 {result['remaining']} 次" if result.get("remaining") is not None else ""
        return redirect(url_for("admin_sessions",
                                notice=f"✅ {result['message']}官網已更新{left}。"))
    return redirect(url_for("admin_sessions",
                            error=f"（{result['step']}）{result['message']}"))


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("EVENT_PORT", 5060)))
