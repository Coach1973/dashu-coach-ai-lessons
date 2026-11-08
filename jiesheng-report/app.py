"""
結繩領導學工作坊（台南／台中／台北）即時戰報。跑法：python app.py（預設 port 5061）
純工作人員內部工具，不對外公開報名——資料全靠工作人員手動輸入。
2026-08-27 教練要求改免登錄：「除了我們，不會有其他人看」，_logged_in() 已改成
永遠回傳 True。登入頁/帳密機制程式碼保留不刪，若日後要重新上鎖，改回
`return bool(session.get("logged_in"))` 即可。
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

WORKSHOP_DATES = {"台南": "2026-08-19", "台北": "2026-11-25"}
WORKSHOP_TARGETS = {"台南": 20, "台北": 50}
WORKSHOP_BREAKEVEN = {"台南": 13, "台北": 11}

# 即時戰報只顯示現役場次；已結束的場次資料保留、改列「歷史記錄」連結，不刪除
ACTIVE_WORKSHOPS = ["台北"]
HISTORY_WORKSHOPS = [w for w in db.WORKSHOPS if w not in ACTIVE_WORKSHOPS]


def _countdown_days(date_str: str) -> int:
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (target - date.today()).days


def _logged_in() -> bool:
    # 2026-08-27 教練要求改免登錄（見檔頭說明），永遠放行。
    return True


@app.route("/")
def root():
    return redirect(url_for("admin"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method in ("GET", "HEAD"):
        # 2026-10-11 教練再次確認免登入（工作人員三人專用、不對外）：舊登入頁不再顯示，直接進戰報。
        return redirect(url_for("admin"))

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
    return redirect(url_for("admin"))


@app.route("/admin")
def admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    workshop = request.args.get("workshop", ACTIVE_WORKSHOPS[0])
    if workshop not in db.WORKSHOPS:
        workshop = ACTIVE_WORKSHOPS[0]

    conn = db.get_conn()
    registrants = db.list_registrants(conn, workshop)
    stats = db.get_stats(conn)
    conn.close()

    countdown_days = {w: _countdown_days(WORKSHOP_DATES[w]) for w in ACTIVE_WORKSHOPS}
    # 目標達成率以「已繳費」人數計算（2026-11-09 教練要求，不再以報名人數計）
    percent = {
        w: round(stats[w]["paid"] / WORKSHOP_TARGETS[w] * 100) if WORKSHOP_TARGETS[w] else 0
        for w in ACTIVE_WORKSHOPS
    }
    # 損益平衡以「已繳費」人數判斷（2026-11-09 教練要求，與目標達成率一致）
    breakeven_reached = {w: stats[w]["paid"] >= WORKSHOP_BREAKEVEN[w] for w in ACTIVE_WORKSHOPS}

    return render_template(
        "admin.html",
        workshops=ACTIVE_WORKSHOPS,
        history_workshops=HISTORY_WORKSHOPS,
        workshop_dates=WORKSHOP_DATES,
        workshop_targets=WORKSHOP_TARGETS,
        workshop_breakeven=WORKSHOP_BREAKEVEN,
        breakeven_reached=breakeven_reached,
        countdown_days=countdown_days,
        percent=percent,
        paid_methods=db.PAID_METHODS,
        referrers=db.REFERRERS,
        submitters=db.REFERRERS,
        selected=workshop,
        registrants=registrants,
        stats=stats,
        today=date.today().isoformat(),
    )


@app.route("/admin/add", methods=["POST"])
def add():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    workshop = request.form.get("workshop", ACTIVE_WORKSHOPS[0])
    if workshop not in db.WORKSHOPS:
        workshop = ACTIVE_WORKSHOPS[0]
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    register_date = (request.form.get("register_date") or date.today().isoformat()).strip()
    note = (request.form.get("note") or "").strip()
    referrer = (request.form.get("referrer") or "").strip()
    if referrer not in db.REFERRERS:
        referrer = ""
    submitter = (request.form.get("submitter") or "").strip()
    if submitter not in db.REFERRERS:
        submitter = ""
    paid_method = (request.form.get("paid_method") or "").strip()
    amount_raw = (request.form.get("amount") or "").strip()
    amount = int(amount_raw) if amount_raw.isdigit() else None
    paid = request.form.get("paid") == "on"

    if name:
        conn = db.get_conn()
        db.add_registrant(conn, workshop, name, phone, register_date, note, referrer,
                           paid, paid_method, amount, submitter)
        conn.close()
    return redirect(url_for("admin", workshop=workshop))


@app.route("/admin/save_all", methods=["POST"])
def save_all():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    workshop = request.form.get("workshop", ACTIVE_WORKSHOPS[0])
    if workshop not in db.WORKSHOPS:
        workshop = ACTIVE_WORKSHOPS[0]

    conn = db.get_conn()
    for reg_id in request.form.getlist("ids"):
        reg = db.get_registrant(conn, reg_id)
        if reg is None:
            continue
        name = (request.form.get(f"name_{reg_id}") or reg["name"]).strip()
        phone = (request.form.get(f"phone_{reg_id}") or "").strip()
        register_date = (request.form.get(f"register_date_{reg_id}") or reg["register_date"]).strip()
        note = (request.form.get(f"note_{reg_id}") or "").strip()
        paid_method = (request.form.get(f"paid_method_{reg_id}") or "").strip()
        amount_raw = (request.form.get(f"amount_{reg_id}") or "").strip()
        amount = int(amount_raw) if amount_raw.isdigit() else None
        paid = request.form.get(f"paid_{reg_id}") == "on"
        referrer = (request.form.get(f"referrer_{reg_id}") or "").strip()
        if referrer not in db.REFERRERS:
            referrer = ""
        submitter = (request.form.get(f"submitter_{reg_id}") or "").strip()
        if submitter not in db.REFERRERS:
            submitter = ""

        db.update_registrant(conn, reg_id, name, phone, register_date, note, paid_method, amount,
                              referrer, submitter)
        db.set_paid(conn, reg_id, paid, paid_method, amount)
    conn.close()
    return redirect(url_for("admin", workshop=workshop))


@app.route("/admin/delete/<int:reg_id>", methods=["POST"])
def delete(reg_id):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    conn = db.get_conn()
    reg = db.get_registrant(conn, reg_id)
    workshop = reg["workshop"] if reg else ACTIVE_WORKSHOPS[0]
    db.delete_registrant(conn, reg_id)
    conn.close()
    return redirect(url_for("admin", workshop=workshop))


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("JIESHENG_PORT", 5061)))
