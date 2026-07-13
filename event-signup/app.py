"""
活動報名網頁。跑法：python app.py（預設 port 5060，比照名片系統用獨立Cloudflare通道對外開）
來賓掃QR → /e/<slug> 填表 → 感謝頁（加LINE好友）；教練看名單 → /admin?key=<ADMIN_KEY>
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
from urllib.parse import quote

from flask import Flask, Response, abort, redirect, render_template, request, send_from_directory, url_for

import db

app = Flask(__name__)
ADMIN_KEY = os.environ.get("EVENT_ADMIN_KEY", "")
LINE_OA_ID = os.environ.get("EVENT_LINE_OA_ID", "@qaw8118h")
LINE_CHANNEL_SECRET = os.environ.get("EVENT_LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("EVENT_LINE_CHANNEL_ACCESS_TOKEN", "")

GREET_PATTERN = re.compile(r"^我是(.+?)，剛報名了")


@app.route("/")
def root():
    return redirect("https://coach1973.github.io/ai-talk/")


QR_DIR = os.path.join(os.path.dirname(__file__), "qr")


@app.route("/qr/<path:filename>")
def qr_file(filename):
    return send_from_directory(QR_DIR, filename)


@app.route("/checkin")
def checkin():
    """固定不變的報到入口，QR立牌永久印這個網址。後台切哪場是「目前活動」，
    這裡就自動導去那場的報名頁，不用重印立牌。"""
    conn = db.get_conn()
    event = db.get_current_event(conn)
    conn.close()
    if not event:
        return "目前沒有進行中的活動，請稍後再試", 404
    return redirect(url_for("signup_form", slug=event["slug"]))


@app.route("/e/<slug>", methods=["GET"])
def signup_form(slug):
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    conn.close()
    if not event:
        abort(404)
    return render_template("form.html", event=event, error=None, form={})


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


def _require_key():
    if not ADMIN_KEY or request.args.get("key") != ADMIN_KEY:
        abort(403)


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
    _require_key()
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
    return render_template("notify.html", events=events, admin_key=ADMIN_KEY, result=None)


@app.route("/admin/notify", methods=["POST"])
def notify_send():
    _require_key()
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
    return render_template("notify.html", events=events, admin_key=ADMIN_KEY, result=result)


@app.route("/admin/set-current", methods=["POST"])
def set_current():
    _require_key()
    slug = (request.form.get("event") or "").strip()
    conn = db.get_conn()
    db.set_current_event(conn, slug)
    conn.close()
    return redirect(url_for("admin", key=ADMIN_KEY))


@app.route("/admin")
def admin():
    _require_key()
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
    conn.close()
    return render_template(
        "admin.html", events=events, attendees=attendees,
        selected=selected, admin_key=ADMIN_KEY, current_event=current_event,
    )


@app.route("/admin/export.csv")
def export_csv():
    _require_key()
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


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("EVENT_PORT", 5060)))
