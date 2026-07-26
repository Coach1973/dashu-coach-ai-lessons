"""
結繩領導學工作坊（台南／台中／台北）即時戰報。跑法：python app.py（預設 port 5061）
純工作人員內部工具，不對外公開報名——資料全靠工作人員手動輸入，帳密登入才看得到。
"""
import os
from datetime import date, datetime

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import db

app = Flask(__name__)
app.secret_key = os.environ.get("JIESHENG_SECRET_KEY", "")
ADMIN_USER = os.environ.get("JIESHENG_ADMIN_USER", "")
ADMIN_PASSWORD_HASH = os.environ.get("JIESHENG_ADMIN_PASSWORD_HASH", "")

WORKSHOP_DATES = {"台南": "2026-08-19", "台中": "2026-09-23", "台北": "2026-11-25"}
WORKSHOP_TARGETS = {"台南": 25, "台中": 20, "台北": 50}


def _countdown_days(date_str: str) -> int:
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (target - date.today()).days


def _logged_in() -> bool:
    return bool(session.get("logged_in"))


@app.route("/")
def root():
    return redirect(url_for("admin"))


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


@app.route("/admin")
def admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    workshop = request.args.get("workshop", db.WORKSHOPS[0])
    if workshop not in db.WORKSHOPS:
        workshop = db.WORKSHOPS[0]

    conn = db.get_conn()
    registrants = db.list_registrants(conn, workshop)
    stats = db.get_stats(conn)
    conn.close()

    countdown_days = {w: _countdown_days(WORKSHOP_DATES[w]) for w in db.WORKSHOPS}
    percent = {
        w: round(stats[w]["total"] / WORKSHOP_TARGETS[w] * 100) if WORKSHOP_TARGETS[w] else 0
        for w in db.WORKSHOPS
    }

    return render_template(
        "admin.html",
        workshops=db.WORKSHOPS,
        workshop_dates=WORKSHOP_DATES,
        workshop_targets=WORKSHOP_TARGETS,
        countdown_days=countdown_days,
        percent=percent,
        paid_methods=db.PAID_METHODS,
        referrers=db.REFERRERS,
        selected=workshop,
        registrants=registrants,
        stats=stats,
        today=date.today().isoformat(),
    )


@app.route("/admin/add", methods=["POST"])
def add():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    workshop = request.form.get("workshop", db.WORKSHOPS[0])
    if workshop not in db.WORKSHOPS:
        workshop = db.WORKSHOPS[0]
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    register_date = (request.form.get("register_date") or date.today().isoformat()).strip()
    note = (request.form.get("note") or "").strip()
    referrer = (request.form.get("referrer") or "").strip()
    if referrer not in db.REFERRERS:
        referrer = ""

    if name:
        conn = db.get_conn()
        db.add_registrant(conn, workshop, name, phone, register_date, note, referrer)
        conn.close()
    return redirect(url_for("admin", workshop=workshop))


@app.route("/admin/update/<int:reg_id>", methods=["POST"])
def update(reg_id):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    reg = db.get_registrant(conn, reg_id)
    if reg is None:
        conn.close()
        return redirect(url_for("admin"))

    name = (request.form.get("name") or reg["name"]).strip()
    phone = (request.form.get("phone") or "").strip()
    register_date = (request.form.get("register_date") or reg["register_date"]).strip()
    note = (request.form.get("note") or "").strip()
    paid_method = (request.form.get("paid_method") or "").strip()
    amount_raw = (request.form.get("amount") or "").strip()
    amount = int(amount_raw) if amount_raw.isdigit() else None
    paid = request.form.get("paid") == "on"
    referrer = (request.form.get("referrer") or "").strip()
    if referrer not in db.REFERRERS:
        referrer = ""

    db.update_registrant(conn, reg_id, name, phone, register_date, note, paid_method, amount, referrer)
    db.set_paid(conn, reg_id, paid, paid_method, amount)
    conn.close()
    return redirect(url_for("admin", workshop=reg["workshop"]))


@app.route("/admin/delete/<int:reg_id>", methods=["POST"])
def delete(reg_id):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    reg = db.get_registrant(conn, reg_id)
    workshop = reg["workshop"] if reg else db.WORKSHOPS[0]
    db.delete_registrant(conn, reg_id)
    conn.close()
    return redirect(url_for("admin", workshop=workshop))


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("JIESHENG_PORT", 5061)))
