"""
活動報名網頁。跑法：python app.py（預設 port 5060，比照名片系統用獨立Cloudflare通道對外開）
來賓掃QR → /e/<slug> 填表 → 感謝頁（加LINE好友）；教練看名單 → /admin（帳密登入，見/admin/login）
"""
import base64
import csv
import hashlib
import hmac
import html
import io
import json
import os
import re
import secrets
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, urlencode

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
CURATION_UPLOAD_KEY = os.environ.get("CURATION_UPLOAD_KEY", "")
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
TELEGRAM_REGISTRATION_GROUP_CHAT_ID = "-5349981085"  # 教練2026-08-24建立「活動報名即時通知」群組，教練+佩佩老師+bot三方共見


NOTIFY_FAIL_LOG = os.path.join(os.path.dirname(__file__), "notify_failures.log")


def _notify_xiaolongxia(text: str, chat_id: str = TELEGRAM_NOTIFY_CHAT_ID) -> bool:
    """發Telegram訊息，預設給教練個人對話；報名通知改傳group chat_id同時通知佩佩老師。

    失敗不影響網頁本身回應，但 🔴 一定要留下痕跡——
    2026-08-17~08-23 教練整整一週收不到報名通知，就是因為舊版 LINE 通知函式
    用 `except: pass` 把 HTTP 429（月配額用完）整個吞掉，沒有任何 log、沒有任何人知道，
    教練還以為報名系統壞了（試金石案例62）。從此：靜默失敗一律不准，至少寫一行。
    """
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        bot_token = config["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        if not result.get("ok"):
            _log_notify_failure(chat_id, f"telegram回傳ok=false: {result}", text)
            return False
        return True
    except Exception as e:
        _log_notify_failure(chat_id, repr(e), text)
        return False


def _log_notify_failure(chat_id: str, reason: str, original_text: str) -> None:
    """通知送不出去時，把「誰、什麼時候、為什麼、原本要送什麼」寫進檔案，事後查得到。"""
    try:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTIFY_FAIL_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] chat_id={chat_id} 失敗原因={reason}\n"
                    f"    原訊息：{original_text[:300].replace(chr(10), ' / ')}\n")
    except Exception:
        pass  # 連寫 log 都失敗就真的沒辦法了，但至少不能讓網頁掛掉


@app.route("/")
def root():
    return redirect("https://coach1973.github.io/ai-talk/")


QR_DIR = os.path.join(os.path.dirname(__file__), "qr")


@app.route("/qr/<path:filename>")
def qr_file(filename):
    return send_from_directory(QR_DIR, filename)


# 產業鏈圖公開網址（LINE只收公開HTTPS網址的圖），由scripts/generate_industry_chain.py --publish 寫入
CHAIN_IMG_DIR = os.path.join(os.path.dirname(__file__), "chain_images")


@app.route("/chain-img/<name>")
def chain_img(name):
    if not re.fullmatch(r"[0-9]{14}_[0-9a-f]{12}\.png", name):
        abort(404)
    return send_from_directory(CHAIN_IMG_DIR, name, mimetype="image/png")


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


def _resolve_current_slides(conn) -> list[str]:
    """回傳目前應該給出的簡報檔名清單（slides/資料夾裡的檔名），可能不只一份。
    auto模式：抓檔名開頭是今天日期(YYYY-MM-DD)的所有檔案；
    manual模式：後台指定的那幾個檔案（逗號分隔），一次可以指定多份（例如同一場有兩份簡報）。"""
    mode = db.get_slides_mode(conn)
    if mode == "manual":
        raw = db.get_manual_slide_file(conn) or ""
        names = [n.strip() for n in raw.split(",") if n.strip()]
        return [n for n in names if os.path.exists(os.path.join(SLIDES_DIR, n))]
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.isdir(SLIDES_DIR):
        return sorted(f for f in os.listdir(SLIDES_DIR) if f.startswith(today))
    return []


@app.route("/slides")
def slides_landing():
    """簡報最後QR掃碼進來的頁面：加LINE好友 + 下載今天的簡報，同時通知小龍蝦。
    固定網址，不用因為每次簡報不同而重印QR——後台換今天的檔案就好。
    name（選填）：從/checkin手機比對成功導過來時會帶上，顯示個人化歡迎文字；
    直接掃簡報QR進來（原本流程）不會帶這個參數，維持原本「感謝聆聽」文字。"""
    conn = db.get_conn()
    fnames = _resolve_current_slides(conn)
    event = db.get_current_event(conn)
    conn.close()

    name = (request.args.get("name") or "").strip()

    _notify_xiaolongxia(
        f"📊 有人{'簽到' if name else '掃了簡報QR碼'}\n"
        f"{f'姓名：{name}' + chr(10) if name else ''}"
        f"檔案：{'、'.join(fnames) if fnames else '（尚未設定今日簡報）'}\n時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    add_friend_url = f"https://line.me/R/ti/p/{LINE_OA_ID}"
    # 2026-07-29教練發現：現場簽到的人綁定率遠低於線上報名的人（56簽到只有12綁定），
    # 原因是這裡原本只給普通加好友連結，要來賓自己手動打「我是OOO，剛報名了XXX」才會綁定，
    # 而/e/<slug>/thanks頁面（線上報名走的那頁）早就有幫忙打好問候語的greet_url。
    # 這裡補上同一套邏輯，讓現場簽到的人也能一鍵完成綁定。
    if name and event:
        add_friend_url = _lottery_greet_url(name, event["name"])

    slides = [{"name": f, "url": url_for("slides_download", filename=f)} for f in fnames]
    return render_template(
        "slides.html", add_friend_url=add_friend_url, slides=slides, name=name,
    )


@app.route("/slides/download/<path:filename>")
def slides_download(filename):
    conn = db.get_conn()
    fnames = _resolve_current_slides(conn)
    conn.close()
    safe_name = os.path.basename(filename)
    if safe_name not in fnames:
        return "這份檔案目前沒有開放下載，請洽大樹教練", 404
    return send_from_directory(SLIDES_DIR, safe_name, as_attachment=True)


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
        fnames = [f.strip() for f in request.form.getlist("manual_file") if f.strip()]
        if fnames:
            db.set_manual_slide_file(conn, ",".join(fnames))
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
        note = (payload.get("note") or "").strip()  # 選填備註（如票種），有值才會出現在通知裡

        source = (payload.get("source") or "").strip()  # 哪個網站送來的，方便追來源

        # 🔴 2026-08-24 教練「全面檢查」時抓到的靜默漏洞：
        # 原本 slug 對不上 / 欄位缺漏就直接 return，資料沒寫進資料庫、教練也收不到任何通知，
        # 等於「有人報名了但全世界都不知道」——跟 8/17~8/23 那次 LINE 配額用完的靜默失敗同一種形狀
        # （見試金石案例62）。從現在起：只要有姓名或電話，就算寫不進資料庫也一定要吼一聲。
        if not slug or not name or not phone_raw:
            if name or phone_raw:
                _notify_xiaolongxia(
                    "⚠️【報名資料不完整，沒能存檔】\n"
                    f"來源：{source or '未標示'}\n場次代碼：{slug or '（沒帶）'}\n"
                    f"姓名：{name or '（沒填）'}\n電話：{phone_raw or '（沒填）'}\n"
                    f"公司：{company_title or '-'}\nEmail：{email or '未填'}\n"
                    "請人工確認這位有沒有真的報名成功。",
                    chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
                )
            return Response(
                json.dumps({"ok": False, "error": "missing slug/name/phone"}),
                status=200, headers={**resp_headers, "Content-Type": "application/json"},
            )

        phone = db.normalize_phone(phone_raw)
        conn = db.get_conn()
        event = db.get_event(conn, slug)
        if not event:
            conn.close()
            # 場次代碼對不上（新場次忘了建、slug 打錯、活動頁寫死舊代碼）→ 資料進不了資料庫，
            # 但人是真的報名了，通知一定要發出去，不能讓這個人憑空消失。
            _notify_xiaolongxia(
                "⚠️【報名成功但場次代碼對不上，資料沒入庫】\n"
                f"來源：{source or '未標示'}\n場次代碼：{slug}（資料庫查無此場次）\n"
                f"姓名：{name}\n電話：{phone}\n公司：{company_title or '-'}\nEmail：{email or '未填'}\n"
                "👉 請到 event.bymyway.com/admin/sessions 確認這個場次代碼是否已建立。",
                chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
            )
            return Response(
                json.dumps({"ok": False, "error": f"unknown slug: {slug}"}),
                status=200, headers={**resp_headers, "Content-Type": "application/json"},
            )

        status = db.upsert_signup(conn, event["id"], name, phone, company_title, email)
        # 2026-08-25教練回報：多場活動共用同一個活動名稱（如「AI微論壇」同時是嘉義/台中DAY1/台中DAY2），
        # 通知只印event_name完全分不出是哪一場。用events表既有的location+event_date組成明確標籤。
        event_label = event["name"]
        label_extra = []
        if event["location"]:
            label_extra.append(event["location"])
        if event["event_date"]:
            try:
                mmdd = event["event_date"][5:].replace("-", "/")
                label_extra.append(mmdd)
            except Exception:
                pass
        if label_extra:
            event_label = f'{event_label}（{"・".join(label_extra)}）'
        conn.close()
        notify_text = (
            f"【大樹小講・官網報名】\n場次：{event_label}\n姓名：{name}\n"
            f"公司：{company_title or '-'}\n電話：{phone}\nEmail：{email or '未填'}\n"
            + (f"備註：{note}\n" if note else "")
            + f"（{'新報名' if status == 'new' else '同場次重複報名'}，由bymyway.com官方發送）"
        )
        # 2026-08-24教練裁示：LINE會扣月配額，全面停用，只留Telegram
        # 「活動報名即時通知」群組(教練+佩佩老師同見，不受配額限制)。
        _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
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


# ---------- 密碼保護的憑證總覽頁(2026-09-06教練交辦，帳號密碼獨立於上面/admin) ----------
VAULT_ADMIN_USER = os.environ.get("VAULT_ADMIN_USER", "")
VAULT_ADMIN_PASSWORD_HASH = os.environ.get("VAULT_ADMIN_PASSWORD_HASH", "")

# 內容跟路徑大全_憑證層.md的「coach888 後台系統帳密」表同步維護，
# 系統有新增/密碼異動時，兩邊要一起改（AI查密碼讀.md，教練自己查看這個網頁）。
VAULT_ENTRIES = [
    {"name": "大樹小講活動後台", "url": "https://event.bymyway.com/admin", "user": "0901056777", "password": "88888"},
    {"name": "教練課程教材線上觀看後台", "url": "https://event.bymyway.com/materials/admin", "user": "（不需要帳密）", "password": "—"},
    {"name": "開發票專用後台", "url": "https://namecard.bymyway.com/invoice-admin", "user": "0901056777", "password": "88888"},
    {"name": "BNI信用証追蹤系統", "url": "https://namecard.bymyway.com/bni-credit", "user": "0901056777", "password": "88888"},
    {"name": "AI資源媒合・帳號審核", "url": "https://namecard.bymyway.com/team/login", "user": "0901056777", "password": "88888"},
    {"name": "BNI大台南南區分會後台(總管理員)", "url": "https://chapters.bymyway.com/admin", "user": "0901056777", "password": "88888"},
    {"name": "AI百人導師後台", "url": "https://mentor100.bymyway.com/admin", "user": "0901056777", "password": "88888"},
    {"name": "通用分會系統(總管理員)", "url": "https://team.bymyway.com/admin", "user": "0901056777", "password": "88888"},
    {"name": "大台南商圈整合計劃(策展店家上/下架管理)", "url": "https://event.bymyway.com/curation/admin", "user": "0901056777", "password": "88888"},
    {"name": "結繩領導學戰報系統", "url": "https://rpl-workshop.bymyway.com/admin", "user": "（不需要帳密）", "password": "—"},
    {"name": "佩佩老師活動後台(非教練個人帳號)", "url": "https://peipei-event.bymyway.com/admin", "user": "peipei", "password": "88888"},
    {"name": "「教練都在想什麼」監控後台", "url": "https://seabiscuit.bymyway.com", "user": "（無帳號欄位）", "password": "Bymyway7"},
]


@app.route("/vault/login", methods=["GET", "POST"])
def vault_login():
    if request.method == "GET":
        return render_template("vault_login.html", error=None)
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if (
        VAULT_ADMIN_USER and VAULT_ADMIN_PASSWORD_HASH
        and username == VAULT_ADMIN_USER
        and check_password_hash(VAULT_ADMIN_PASSWORD_HASH, password)
    ):
        session["vault_logged_in"] = True
        session.permanent = True
        return redirect(url_for("vault"))
    return render_template("vault_login.html", error="帳號或密碼不對，請再試一次"), 401


@app.route("/vault/logout")
def vault_logout():
    session.pop("vault_logged_in", None)
    return redirect(url_for("vault_login"))


@app.route("/vault")
def vault():
    if not session.get("vault_logged_in"):
        return redirect(url_for("vault_login", next=request.path))
    return render_template("vault.html", entries=VAULT_ENTRIES)


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


def _line_quota() -> dict | None:
    """查LINE官方帳號本月推播額度用量。查不到（沒設金鑰/網路問題）回None，不擋頁面。"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        return None
    try:
        req1 = urllib.request.Request("https://api.line.me/v2/bot/message/quota",
            headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"})
        req2 = urllib.request.Request("https://api.line.me/v2/bot/message/quota/consumption",
            headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"})
        with urllib.request.urlopen(req1, timeout=6) as r1, urllib.request.urlopen(req2, timeout=6) as r2:
            limit = json.loads(r1.read()).get("value", 0)
            used = json.loads(r2.read()).get("totalUsage", 0)
        return {"limit": limit, "used": used, "remaining": max(limit - used, 0)}
    except Exception:
        return None


def _unbound_lists(conn):
    """各場次「已報名但尚未綁定LINE」的名單，附上一鍵複製用的個人化文字。

    2026-08-23教練發現：8/21+8/22兩場合計49人參加抽獎，只有20人真的綁定LINE。
    根因是LINE官方帳號的oaMessage連結最後一步（按下傳送）無法代勞，一定要本人
    手動點——這個環節本來就無法用推播訊息催促，加上剛好這陣子推播額度也用完，
    唯一能做的是讓教練自己（用簡訊/電話/其他管道）把「一鍵開好LINE、只差按傳送」
    的連結送到這些人手上，這裡把名單跟訊息文字準備好，教練不用自己一個個組字。"""
    events = conn.execute(
        """SELECT e.slug, e.name, e.event_date,
                  COUNT(s.id) AS signup_count,
                  SUM(CASE WHEN a.line_user_id IS NOT NULL THEN 1 ELSE 0 END) AS line_bound_count
           FROM events e
           LEFT JOIN signups s ON s.event_id = e.id
           LEFT JOIN attendees a ON a.id = s.attendee_id
           GROUP BY e.id HAVING signup_count > 0 ORDER BY e.event_date DESC"""
    ).fetchall()
    result = []
    for e in events:
        unbound = conn.execute(
            """SELECT a.name, a.phone FROM attendees a
               JOIN signups s ON s.attendee_id = a.id
               JOIN events ev ON ev.id = s.event_id
               WHERE ev.slug = ? AND a.line_user_id IS NULL ORDER BY a.name""",
            (e["slug"],),
        ).fetchall()
        if not unbound:
            continue
        people = []
        for a in unbound:
            url = _lottery_greet_url(a["name"], e["name"])
            sms = f"{a['name']}您好，補登記「{e['name']}」抽獎資格請點此連結，開啟LINE後記得按「傳送」才算完成：{url}"
            people.append({"name": a["name"], "phone": a["phone"], "url": url, "sms": sms})
        result.append({"event": e, "unbound": people})
    return result


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
    unbound_lists = _unbound_lists(conn)
    conn.close()
    return render_template("notify.html", events=events, result=None, unbound_lists=unbound_lists, quota=_line_quota())


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
    unbound_lists = _unbound_lists(conn)
    conn.close()
    return render_template("notify.html", events=events, result=result, unbound_lists=unbound_lists, quota=_line_quota())


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
    current_slides = _resolve_current_slides(conn)
    manual_slides = [f.strip() for f in (db.get_manual_slide_file(conn) or "").split(",") if f.strip()]
    conn.close()
    slide_files = sorted(os.listdir(SLIDES_DIR)) if os.path.isdir(SLIDES_DIR) else []
    return render_template(
        "admin.html", events=events, attendees=attendees,
        selected=selected, current_event=current_event, routing_mode=routing_mode,
        slides_mode=slides_mode, current_slide="、".join(current_slides) if current_slides else None,
        manual_slide=manual_slides, slide_files=slide_files,
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

def _attach_deep_links(sessions):
    """幫每場活動算出分享用深連結（event.bymyway.com/bigtree/?session=日期[&slot=時段]）。
    2026-08-31教練交辦：常態需要分享/追蹤QR的網址，不用每次口頭問。
    同一天有多場、但時段標籤缺漏或彼此重複時，前端的openRegisterFromQuery()
    分不出是哪一場（見bigtree/index.html），這時不產生會誤導的連結，改標警告。"""
    out = [dict(s) for s in sessions]
    for s in out:
        same_day = [x for x in out if x["event_date"] == s["event_date"] and x["status"] != "cancelled"]
        if len(same_day) <= 1:
            s["deep_link"] = f"https://event.bymyway.com/bigtree/?session={s['event_date']}"
            s["deep_link_warning"] = None
            continue
        slot_vals = [x["slot_key"] for x in same_day]
        if s["slot_key"] and slot_vals.count(s["slot_key"]) == 1:
            s["deep_link"] = f"https://event.bymyway.com/bigtree/?session={s['event_date']}&slot={s['slot_key']}"
            s["deep_link_warning"] = None
        else:
            s["deep_link"] = None
            s["deep_link_warning"] = "同一天有多場活動，且「時段」欄位沒填或跟別場重複，目前無法產生準確的深連結——請先把上面「時段」改成不同的選項"
    return out


@app.route("/admin/sessions")
def admin_sessions():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    import bigtree_publish as bp
    conn = db.get_conn()
    sessions = _attach_deep_links(db.list_site_sessions(conn))
    summary = bp.diff_summary(conn)
    conn.close()
    return render_template(
        "sessions.html", sessions=sessions, slot_choices=bp.SLOT_CHOICES, slot_times=bp.SLOT_TIMES,
        summary=summary, live_count=len(summary["sessions"]),
        quota=bp.quota_remaining(), today=date.today().isoformat(),
        notice=request.args.get("notice", ""), error=request.args.get("error", ""),
    )


@app.route("/admin/qr/<int:event_id>.png")
def admin_session_qr(event_id):
    """場次深連結的QR code，即時產生不落地存檔（後台頻繁改期時不用擔心QR圖跟著過期）。"""
    if not _logged_in():
        abort(403)
    conn = db.get_conn()
    event = db.get_session(conn, event_id)
    conn.close()
    if not event:
        abort(404)
    url = f"https://event.bymyway.com/bigtree/?session={event['event_date']}"
    if event["slot_key"]:
        url += f"&slot={event['slot_key']}"
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return Response(buf.getvalue(), mimetype="image/png")


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


# ───────── 大樹小講／AI微論壇：bymyway 版本（2026-08-30，逐步取代 Netlify 部署次數限制）
# 教練 2026-08-30 裁示的命名邏輯：網址代表「活動格式／系列」，不代表某一次的地點——
# 跟 ai-talk-tw.netlify.app 過去台南→嘉義直接覆寫同一個網址是同一套做法：
#   /ai-forum → 兩天制場次（現在是台中9/23-24，之後10/7-8台南場一樣用這個網址，
#               台中辦完就變成歷史紀錄，不會因為換地點就換網址）
#   /ai-talk  → 半天制場次（現在是9/22台南場，之後換場地一樣沿用這個網址）
# 設計/文案本體只有一份，就是各自的 github_repos git repo，這裡在請求當下直接讀
# 原始檔案（+ 大樹小講額外疊上 event.db 即時場次資料）組合渲染，不另外複製一份，
# 教練或軍師改任一邊都立刻反映，不需要「發佈」這個動作。GitHub Pages/Netlify 兩邊
# 暫時繼續保留同步，穩定一陣子後才會退場。
BIGTREE_REPO = Path("/Users/bymyway/github_repos/bigtree")
AI_FORUM_REPO = Path("/Users/bymyway/github_repos/ai-forum-taichung")  # 目前是台中場內容，之後換場地時原地改內容，repo資料夾名稱不代表網址
AI_TALK_REPO = Path("/Users/bymyway/github_repos/ai-talk")
TAINAN_CALENDAR_REPO = Path("/Users/bymyway/github_repos/tainan-calender")  # 沿用既有repo/Netlify站台既有拼法，不擅自改成calendar
BNI_TRAFFIC_REPO = Path("/Users/bymyway/github_repos/bni-traffic")  # 紅綠燈看板，原repo已在GitHub上archived但內容仍可讀取服務
_REPO_BLOCKED_TOP_DIRS = {".git", "biz-gym"}
# 2026-09-26審查補：資料庫/紀錄檔/程式原始碼一律不對外，就算日後有人把它們放進已上架網站的資料夾也擋住。
_REPO_BLOCKED_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".env", ".log", ".sql", ".py", ".pyc", ".sh", ".bak")


def _serve_repo_file(repo: Path, filename: str):
    top = filename.split("/", 1)[0]
    if top in _REPO_BLOCKED_TOP_DIRS or filename.startswith(".") or "/." in filename \
            or filename.lower().endswith(_REPO_BLOCKED_SUFFIXES):
        abort(404)
    # 2026-09-04交辦(KR養生廚房)：多頁面靜態站的子頁面用「<slug>/index.html」資料夾結構，
    # 請求路徑本身沒有副檔名時，退而找同名資料夾底下的index.html（nginx try_files的靜態站慣例）。
    # 不影響既有單頁站(bigtree/tut/1010等)行為，那些請求的filename永遠直接對應真實檔案。
    target = repo / filename
    if not target.is_file() and "." not in filename.rsplit("/", 1)[-1]:
        index_path = filename.rstrip("/") + "/index.html"
        if (repo / index_path).is_file():
            return send_from_directory(repo, index_path)
    return send_from_directory(repo, filename)


@app.route("/bigtree/")
def bigtree_page():
    import bigtree_publish as bp
    conn = db.get_conn()
    rows = bp.read_sessions(conn)
    conn.close()
    html = (BIGTREE_REPO / "index.html").read_text(encoding="utf-8")
    block = bp.render_session_dates(rows)
    html, _n = re.subn(r"const SESSION_DATES = \[[\s\S]*?\n\];", block, html, count=1)
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/bigtree/<path:filename>")
def bigtree_assets(filename):
    if filename == "index.html":
        return bigtree_page()
    return _serve_repo_file(BIGTREE_REPO, filename)


@app.route("/ai-forum/")
def ai_forum_page():
    return _serve_repo_file(AI_FORUM_REPO, "index.html")


@app.route("/ai-forum/<path:filename>")
def ai_forum_assets(filename):
    return _serve_repo_file(AI_FORUM_REPO, filename)


@app.route("/ai-talk/")
def ai_talk_page():
    return _serve_repo_file(AI_TALK_REPO, "index.html")


@app.route("/ai-talk/<path:filename>")
def ai_talk_assets(filename):
    return _serve_repo_file(AI_TALK_REPO, filename)


@app.route("/tainan-calender/")
def tainan_calendar_page():
    return _serve_repo_file(TAINAN_CALENDAR_REPO, "index.html")


@app.route("/tainan-calender/<path:filename>")
def tainan_calendar_assets(filename):
    return _serve_repo_file(TAINAN_CALENDAR_REPO, filename)


@app.route("/bni-traffic/")
def bni_traffic_page():
    return _serve_repo_file(BNI_TRAFFIC_REPO, "index.html")


@app.route("/bni-traffic/<path:filename>")
def bni_traffic_assets(filename):
    return _serve_repo_file(BNI_TRAFFIC_REPO, filename)


TUT_ALUMNI_REPO = Path("/Users/bymyway/github_repos/tut-alumni")
PEIPEI_LINE_OA_ID = "@701ohlly"  # 佩佩老師的LINE官方帳號(讀自peipei-event/.env的EVENT_LINE_OA_ID)，
                                  # 跟本app全域LINE_OA_ID(@qaw8118h,大樹教育自己的)是不同帳號，不能共用常數


@app.route("/tut/")
def tut_alumni_page():
    return _serve_repo_file(TUT_ALUMNI_REPO, "index.html")


@app.route("/tut/<path:filename>")
def tut_alumni_assets(filename):
    return _serve_repo_file(TUT_ALUMNI_REPO, filename)


TUT_ALUMNI_CHAPTERS = {"台南", "台中", "高雄", "台北", "嘉義"}


@app.route("/api/tut/join", methods=["POST", "OPTIONS"])
def api_tut_join():
    """校友會加入表單的真正後端，取代原本純前端假成功。教練2026-09-03裁示：
    同時服務event.bymyway.com/tut跟GitHub Pages(coach1973.github.io/tut-alumni)兩個入口，
    所以CORS開放；不論資料庫寫入成功與否，都要讓前端能拿到佩佩老師LINE連結繼續往下走
    （呼應/api/register同一套原則：訪客體驗永遠不能被後端錯誤卡住，但也不能靜默吞錯誤）。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    phone = (payload.get("phone") or "").strip()
    grad_year = (payload.get("gradYear") or "").strip()
    department = (payload.get("department") or "").strip()
    chapter = (payload.get("chapter") or "").strip()
    source = (payload.get("source") or "unknown").strip()

    add_friend_url = f"https://line.me/R/ti/p/{PEIPEI_LINE_OA_ID}"
    greet_url = add_friend_url
    if name:
        greet_text = f"我是{name}，我已經送出台南應用科技大學校友會（{chapter or '尚未選擇分會'}）的資料了"
        greet_url = f"https://line.me/R/oaMessage/{PEIPEI_LINE_OA_ID}/?{quote(greet_text)}"

    if not name or not phone or chapter not in TUT_ALUMNI_CHAPTERS:
        _notify_xiaolongxia(
            "⚠️【校友會召集令・資料不完整，沒能存檔】\n"
            f"來源：{source}\n姓名：{name or '（沒填）'}\n電話：{phone or '（沒填）'}\n"
            f"分會：{chapter or '（沒選）'}\n請人工確認這位有沒有真的要加入。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": "missing name/phone/chapter",
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    try:
        conn = db.get_conn()
        conn.execute(
            "INSERT INTO tut_alumni_signups (name, phone, grad_year, department, chapter, source) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, phone, grad_year, department, chapter, source),
        )
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(
            "⚠️【校友會召集令・資料庫寫入失敗】\n"
            f"來源：{source}\n姓名：{name}\n電話：{phone}\n分會：{chapter}\n錯誤：{e}\n"
            "請人工補登這筆資料。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": str(e),
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    notify_text = (
        "【台南應用科技大學校友會・召集令報名】\n"
        f"分會：{chapter}\n姓名：{name}\n電話：{phone}\n"
        f"畢業年：{grad_year or '未填'}\n科系：{department or '未填'}\n"
        f"（來源：{'GitHub Pages' if source == 'github-pages' else 'event.bymyway.com/tut'}）"
    )
    _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return Response(
        json.dumps({"ok": True, "add_friend_url": add_friend_url, "greet_url": greet_url}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


# ---------- 校友回憶牆：留言＋照片送審，教練通過才公開（2026-10-02 教練交辦） ----------
# 原本 tut-memory 頁的照片只存在訪客自己瀏覽器，別人看不到。改成：送出→存伺服器(pending)
# →Telegram 傳照片給教練，附一個審核連結→教練按「通過」才出現在所有人的牆上。
MEMWALL_SLUGS = {"tut-memory"}
# 投稿審核通知送「活動報名即時通知」群（教練+佩佩老師+bot），佩佩老師可幫忙審核（教練2026-10-02交辦）
MEMWALL_REVIEW_CHAT_ID = TELEGRAM_REGISTRATION_GROUP_CHAT_ID
MEMWALL_DIR = Path(__file__).resolve().parent / "memwall_uploads"
MEMWALL_MAX_PHOTO = 1_600_000
MEMWALL_RECENT: dict = {}  # ip -> [時間戳]，簡單防灌爆：每個IP一小時最多10則
MEMWALL_CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def _memwall_conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS memwall_notes ("
        " id TEXT PRIMARY KEY, slug TEXT NOT NULL, name TEXT, year TEXT, color TEXT,"
        " txt TEXT NOT NULL, photo_file TEXT, status TEXT NOT NULL DEFAULT 'pending',"
        " ip TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')), reviewed_at TEXT)"
    )
    return conn


def _memwall_sig(note_id: str) -> str:
    return hmac.new(app.secret_key.encode(), f"memwall:{note_id}".encode(), hashlib.sha256).hexdigest()[:24]


def _memwall_json(obj, status=200):
    return Response(json.dumps(obj, ensure_ascii=False), status=status,
                    headers={**MEMWALL_CORS, "Content-Type": "application/json"})


def _memwall_send_photo_to_coach(photo_path: Path, caption: str, chat_id: str = None) -> bool:
    """有照片就用 sendPhoto 讓教練在 Telegram 直接看到照片；失敗退回文字通知。"""
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            bot_token = json.load(f)["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        boundary = "memwall" + secrets.token_hex(8)
        parts = []
        chat_id = chat_id or MEMWALL_REVIEW_CHAT_ID
        for k, v in (("chat_id", chat_id), ("caption", caption)):
            parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"p.jpg\"\r\n"
                     f"Content-Type: image/jpeg\r\n\r\n".encode() + photo_path.read_bytes() + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendPhoto", data=b"".join(parts), method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            if json.loads(resp.read().decode()).get("ok"):
                return True
    except Exception as e:  # noqa: BLE001
        _log_notify_failure(chat_id or MEMWALL_REVIEW_CHAT_ID, f"memwall sendPhoto失敗: {e!r}", caption)
    return _notify_xiaolongxia(caption, chat_id=chat_id or MEMWALL_REVIEW_CHAT_ID)


@app.route("/api/memwall/<slug>/notes", methods=["GET", "POST", "OPTIONS"])
def api_memwall_notes(slug):
    if request.method == "OPTIONS":
        return Response(status=204, headers=MEMWALL_CORS)
    if slug not in MEMWALL_SLUGS:
        return _memwall_json({"ok": False, "error": "unknown wall"}, 404)

    if request.method == "GET":
        conn = _memwall_conn()
        rows = conn.execute(
            "SELECT id, name, year, color, txt, photo_file, created_at FROM memwall_notes "
            "WHERE slug=? AND status='approved' ORDER BY created_at DESC LIMIT 500", (slug,)).fetchall()
        conn.close()
        notes = [{"id": r["id"], "name": r["name"], "year": r["year"], "color": r["color"], "txt": r["txt"],
                  "photo": f"/memwall/photo/{r['id']}.jpg" if r["photo_file"] else None,
                  "created_at": r["created_at"]} for r in rows]
        return _memwall_json({"ok": True, "notes": notes})

    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "?"
    now = datetime.now().timestamp()
    recent = [t for t in MEMWALL_RECENT.get(ip, []) if now - t < 3600]
    if len(recent) >= 10:
        return _memwall_json({"ok": False, "error": "too many"}, 429)

    p = request.get_json(force=True, silent=True) or {}
    txt = (p.get("txt") or "").strip()[:200]
    name = (p.get("name") or "").strip()[:30]
    year = (p.get("year") or "").strip()[:20]
    color = p.get("color") if p.get("color") in ("yellow", "pink", "mint") else "yellow"
    if not txt:
        return _memwall_json({"ok": False, "error": "empty"}, 400)

    note_id = "m" + secrets.token_hex(6)
    photo_file = None
    photo = p.get("photo") or ""
    if photo:
        m = re.match(r"^data:image/(jpeg|jpg|png|webp);base64,(.+)$", photo, re.S)
        if not m:
            return _memwall_json({"ok": False, "error": "bad photo"}, 400)
        raw = base64.b64decode(m.group(2), validate=False)
        if len(raw) > MEMWALL_MAX_PHOTO or raw[:3] not in (b"\xff\xd8\xff",) and raw[:8] != b"\x89PNG\r\n\x1a\n" and raw[8:12] != b"WEBP":
            return _memwall_json({"ok": False, "error": "bad photo"}, 400)
        MEMWALL_DIR.mkdir(exist_ok=True)
        photo_file = f"{note_id}.jpg"
        (MEMWALL_DIR / photo_file).write_bytes(raw)

    conn = _memwall_conn()
    conn.execute("INSERT INTO memwall_notes (id, slug, name, year, color, txt, photo_file, ip) VALUES (?,?,?,?,?,?,?,?)",
                 (note_id, slug, name, year, color, txt, photo_file, ip))
    conn.commit()
    conn.close()
    MEMWALL_RECENT[ip] = recent + [now]

    review_url = f"https://event.bymyway.com/memwall/review/{note_id}?t={_memwall_sig(note_id)}"
    caption = (f"📮【南應校友回憶牆・新投稿待審核】\n— {name or '匿名校友'} · {year}\n「{txt}」\n\n"
               f"審核（群裡任何人點開都可以按通過或不通過）：\n{review_url}")
    if photo_file:
        _memwall_send_photo_to_coach(MEMWALL_DIR / photo_file, caption[:1000])
    else:
        _notify_xiaolongxia(caption, chat_id=MEMWALL_REVIEW_CHAT_ID)
    return _memwall_json({"ok": True, "id": note_id, "status": "pending"})


@app.route("/memwall/photo/<note_id>.jpg")
def memwall_photo(note_id):
    if not re.fullmatch(r"m[0-9a-f]{12}", note_id):
        abort(404)
    conn = _memwall_conn()
    r = conn.execute("SELECT status, photo_file FROM memwall_notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    signed = hmac.compare_digest(request.args.get("t", ""), _memwall_sig(note_id))
    if not r or not r["photo_file"] or (r["status"] != "approved" and not signed):
        # Cloudflare 會把 .jpg 的 404 快取 4 小時，審核通過後照片還是破圖，所以 404 一律不准快取
        return Response("", status=404, headers={"Cache-Control": "no-store"})
    resp = send_from_directory(MEMWALL_DIR, r["photo_file"], mimetype="image/jpeg")
    if signed and r["status"] != "approved":
        resp.headers["Cache-Control"] = "no-store"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/memwall/review/<note_id>", methods=["GET", "POST"])
def memwall_review(note_id):
    """教練從 Telegram 連結點進來審核；連結帶簽章，不用登入。GET 只顯示，POST 才改狀態。"""
    t = request.args.get("t", "")
    if not re.fullmatch(r"m[0-9a-f]{12}", note_id) or not hmac.compare_digest(t, _memwall_sig(note_id)):
        abort(404)
    conn = _memwall_conn()
    if request.method == "POST":
        action = request.form.get("action")
        if action in ("approved", "rejected"):
            conn.execute("UPDATE memwall_notes SET status=?, reviewed_at=datetime('now','localtime') WHERE id=?",
                         (action, note_id))
            conn.commit()
    r = conn.execute("SELECT * FROM memwall_notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not r:
        abort(404)
    e = html.escape
    status_txt = {"pending": "⏳ 待審核", "approved": "✅ 已通過，所有人都看得到", "rejected": "🚫 不通過，不會公開"}[r["status"]]
    photo = f'<img src="/memwall/photo/{note_id}.jpg?t={t}" style="max-width:100%;border-radius:8px">' if r["photo_file"] else ""
    page = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>回憶牆投稿審核</title>
<style>body{{font-family:-apple-system,"PingFang TC",sans-serif;max-width:520px;margin:0 auto;padding:16px;background:#f7f3ea;color:#2b2b2b}}
.card{{background:#fff;padding:16px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
button{{font-size:18px;padding:12px 0;width:48%;border:0;border-radius:10px;color:#fff;margin-top:12px}}
.ok{{background:#2e7d4f}}.no{{background:#b23b3b}}.st{{font-size:18px;font-weight:700;margin:12px 0}}</style></head><body>
<h2>南應校友回憶牆・投稿審核</h2><div class="card">{photo}
<p style="font-size:18px">「{e(r['txt'])}」</p><p>— {e(r['name'] or '匿名校友')} · {e(r['year'] or '')}</p>
<p style="color:#888;font-size:13px">投稿時間：{e(r['created_at'])}</p></div>
<div class="st">目前狀態：{status_txt}</div>
<form method="post" style="display:flex;justify-content:space-between">
<button class="ok" name="action" value="approved">通過</button>
<button class="no" name="action" value="rejected">不通過</button></form>
<p><a href="https://event.bymyway.com/curated/{e(r['slug'])}/#wall">看回憶牆</a></p></body></html>"""
    return Response(page, mimetype="text/html")


LEADER_EVENT_NAME = "領導人溝通的藝術"


@app.route("/leader/")
def leader_page():
    return render_template("leader.html")


@app.route("/api/leader/join", methods=["POST", "OPTIONS"])
def api_leader_join():
    """「領導人溝通的藝術」9/10報名表單後端（2026-09-03交辦，design(4).html邀請函）。
    比照/api/tut/join同一套原則：報名成功同時通知教練+佩佩老師共見的Telegram群組，
    並導流佩佩老師LINE官方帳號，訪客體驗不能被後端錯誤卡住。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    phone = (payload.get("phone") or "").strip()
    source = (payload.get("source") or "event.bymyway.com/leader").strip()

    add_friend_url = f"https://line.me/R/ti/p/{PEIPEI_LINE_OA_ID}"
    greet_url = add_friend_url
    if name:
        greet_text = f"我是{name}，我已經報名了「{LEADER_EVENT_NAME}」9/10場次"
        greet_url = f"https://line.me/R/oaMessage/{PEIPEI_LINE_OA_ID}/?{quote(greet_text)}"

    if not name or not phone:
        _notify_xiaolongxia(
            "⚠️【領導人溝通的藝術・資料不完整，沒能存檔】\n"
            f"姓名：{name or '（沒填）'}\n電話：{phone or '（沒填）'}\n請人工確認這位有沒有真的要報名。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": "missing name/phone",
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    try:
        conn = db.get_conn()
        conn.execute(
            "INSERT INTO leader_workshop_signups (name, phone, source) VALUES (?, ?, ?)",
            (name, phone, source),
        )
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(
            "⚠️【領導人溝通的藝術・資料庫寫入失敗】\n"
            f"姓名：{name}\n電話：{phone}\n錯誤：{e}\n請人工補登這筆資料。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": str(e),
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    notify_text = (
        "【領導人溝通的藝術・報名通知】\n"
        f"姓名：{name}\n電話：{phone}\n"
        "日期：9/10（四）14:00-17:00\n地點：安平路176號\n"
        f"（來源：{source}）"
    )
    _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return Response(
        json.dumps({"ok": True, "add_friend_url": add_friend_url, "greet_url": greet_url}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


EVENT_1010_REPO = Path("/Users/bymyway/github_repos/1010")
EVENT_1010_NAME = "人生四席・一日共鳴（淺山綠茶席生命故事）"


@app.route("/1010/")
def event_1010_page():
    return _serve_repo_file(EVENT_1010_REPO, "index.html")


@app.route("/1010/<path:filename>")
def event_1010_assets(filename):
    if filename == "index.html":
        return event_1010_page()
    return _serve_repo_file(EVENT_1010_REPO, filename)


@app.route("/api/1010/join", methods=["POST", "OPTIONS"])
def api_event_1010_join():
    """「人生四席・一日共鳴」10/10淺山綠茶席報名（2026-09-03交辦，Designs.zip落地頁）。
    比照/api/leader/join+/api/tut/join同一套模式，LINE導流用佩佩老師官方帳號
    （教練原口頭指定大樹教育官方帳號，隨後改口「畢竟這是音樂藝術相關活動」改用佩佩老師帳號）。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    phone = (payload.get("phone") or "").strip()
    source = (payload.get("source") or "event.bymyway.com/1010").strip()

    add_friend_url = f"https://line.me/R/ti/p/{PEIPEI_LINE_OA_ID}"
    greet_url = add_friend_url
    if name:
        greet_text = f"我是{name}，我已經報名了「{EVENT_1010_NAME}」10/10場次"
        greet_url = f"https://line.me/R/oaMessage/{PEIPEI_LINE_OA_ID}/?{quote(greet_text)}"

    if not name or not phone:
        _notify_xiaolongxia(
            "⚠️【人生四席・一日共鳴・資料不完整，沒能存檔】\n"
            f"姓名：{name or '（沒填）'}\n電話：{phone or '（沒填）'}\n請人工確認這位有沒有真的要報名。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": "missing name/phone",
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    try:
        conn = db.get_conn()
        conn.execute(
            "INSERT INTO event_1010_signups (name, phone, source) VALUES (?, ?, ?)",
            (name, phone, source),
        )
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(
            "⚠️【人生四席・一日共鳴・資料庫寫入失敗】\n"
            f"姓名：{name}\n電話：{phone}\n錯誤：{e}\n請人工補登這筆資料。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": str(e),
                        "add_friend_url": add_friend_url, "greet_url": greet_url}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    notify_text = (
        "【人生四席・一日共鳴・報名通知】\n"
        f"姓名：{name}\n電話：{phone}\n"
        "日期：10/10（六）10:00～下午\n地點：淺山綠（苗栗苑裡）\n"
        f"（來源：{source}）"
    )
    _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return Response(
        json.dumps({"ok": True, "add_friend_url": add_friend_url, "greet_url": greet_url}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


TAINAN_SHANGQUAN_REPO = Path("/Users/bymyway/github_repos/tainan-shangquan")


@app.route("/tainan-shangquan/")
def tainan_shangquan_page():
    return _serve_repo_file(TAINAN_SHANGQUAN_REPO, "index.html")


@app.route("/tainan-shangquan/<path:filename>")
def tainan_shangquan_assets(filename):
    if filename == "index.html":
        return tainan_shangquan_page()
    return _serve_repo_file(TAINAN_SHANGQUAN_REPO, filename)



def _shop_slug(shop_name: str) -> str:
    """店名轉英文/拼音短碼，當作shops.bymyway.com/<slug>/的網址。
    2026-09-05教練裁示自動化流程用拼音，不用每家店手動問英文代碼；
    slug若跟既有店家撞名，外層呼叫者會自動加數字尾碼。"""
    from pypinyin import lazy_pinyin
    raw = "-".join(lazy_pinyin(shop_name))
    slug = re.sub(r"[^a-z0-9-]", "", raw.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "shop"


def _shop_placeholder_html(name, shop, category, contact, address, social, items) -> str:
    """比照迴頭快剪(huitou)手刻的暫代頁樣式，參數化成共用函式。
    所有店家提供的資料都用html.escape()處理，避免表單灌入惡意HTML/script(XSS)。"""
    e = html.escape
    items_html = e(items).replace("\n", "<br>") if items else ""
    social_row = (
        f'<div class="row"><div class="k">社群</div><div class="v">'
        f'<a href="{e(social)}" target="_blank" rel="noopener">連結</a></div></div>'
        if social else ""
    )
    items_row = (
        f'<div class="row"><div class="k">招牌商品</div><div class="v items">{items_html}</div></div>'
        if items else ""
    )
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(shop)}｜大臺南商圈整合計劃</title>
<meta name="description" content="{e(shop)}，{e(address)}。大臺南商圈整合計劃合作店家。">
<style>
  :root{{--ink:#1a1a1a;--muted:#666;--accent:#CF2030;--bg:#fafafa;--card:#fff;--line:#e5e5e5}}
  *{{box-sizing:border-box}}
  body{{margin:0;font-family:"Noto Sans TC",-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.8}}
  .wrap{{max-width:640px;margin:0 auto;padding:32px 20px 60px}}
  .badge{{display:inline-block;font-size:13px;font-weight:700;color:var(--accent);background:rgba(207,32,48,.08);border:1px solid rgba(207,32,48,.25);border-radius:999px;padding:6px 14px;margin-bottom:18px}}
  h1{{font-size:32px;margin:0 0 6px;font-weight:900}}
  .sub{{color:var(--muted);font-size:16px;margin-bottom:28px}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px;margin-bottom:20px}}
  .row{{display:flex;gap:14px;padding:12px 0;border-top:1px solid var(--line)}}
  .row:first-child{{border-top:none;padding-top:0}}
  .row .k{{flex:0 0 88px;color:var(--muted);font-size:14px;font-weight:700}}
  .row .v{{flex:1;font-size:16px}}
  .row .v a{{color:var(--accent);text-decoration:none;font-weight:600}}
  .items{{white-space:pre-line}}
  .note{{font-size:13px;color:var(--muted);text-align:center;margin-top:32px;line-height:1.9}}
  .note a{{color:var(--accent)}}
</style>
</head>
<body>
  <div class="wrap">
    <span class="badge">大臺南商圈整合計劃 · 合作店家</span>
    <h1>{e(shop)}</h1>
    <p class="sub">{e(category)}｜{e(address)}</p>

    <div class="card">
      <div class="row"><div class="k">分類</div><div class="v">{e(category)}</div></div>
      <div class="row"><div class="k">地址</div><div class="v">{e(address)}</div></div>
      <div class="row"><div class="k">聯絡方式</div><div class="v"><a href="tel:{e(contact)}">{e(contact)}</a></div></div>
      {social_row}
      {items_row}
    </div>

    <p class="note">本頁為店家資料暫代版，正式形象網站由 <a href="https://www.tava-ai.com/" target="_blank" rel="noopener">TAVA AI</a> 製作中，完成後將替換為完整版本。<br>大臺南商圈整合計劃｜<a href="https://event.bymyway.com/tainan-shangquan/" target="_blank" rel="noopener">了解更多／店家登錄</a></p>
  </div>
</body>
</html>
"""


def _shop_directory_card_html(name, shop, category, contact, address, social, items, shop_url) -> str:
    """插入tainan-shangquan首頁「店家名冊」區塊的shop-row卡片，比照迴頭快剪手刻的樣式。"""
    e = html.escape
    social_row = (
        f'<li><span class="k">社群</span><span><a href="{e(social)}" target="_blank" rel="noopener">連結</a></span></li>'
        if social else ""
    )
    items_row = (
        f'<li><span class="k">招牌商品</span><span>{e(items)}</span></li>'
        if items else ""
    )
    map_q = quote(f"{address} {shop}")
    review_q = quote(f"{shop} 台南")
    return f"""
          <!-- 計劃夥伴店家：{e(shop)}（自動建立） -->
          <article class="shop-row reveal">
            <div>
              <div class="shop-head">
                <span class="pill">計劃夥伴店家</span>
                <span class="tag">{e(category)}</span>
              </div>
              <h3>{e(shop)}</h3>
              <p class="shop-desc">位於{e(address)}，{e(category)}類合作店家。</p>
              <ul class="shop-facts">
                <li><span class="k">地址</span><span>{e(address)}</span></li>
                <li><span class="k">分類</span><span>{e(category)}</span></li>
                {items_row}
                <li><span class="k">聯絡方式</span><span><a href="tel:{e(contact)}">{e(contact)}</a></span></li>
                {social_row}
              </ul>
              <p class="slot-note"><a href="{e(shop_url)}" target="_blank" rel="noopener">查看店家專屬網站 →</a></p>

              <div class="review-block">
                <div class="review-head">
                  <span class="label">Google 評論</span>
                  <span class="star-row" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>
                  </span>
                </div>
                <div class="review-empty">
                  <p>評分與評論由 Google 商家即時提供，店家資料登錄後自動串接。</p>
                  <a href="https://www.google.com/maps/search/?api=1&amp;query={review_q}" target="_blank" rel="noopener">在 Google 地圖上查看評論 →</a>
                </div>
              </div>
            </div>

            <div class="shop-media">
              <div class="map-frame">
                <iframe
                  src="https://www.google.com/maps?q={map_q}&amp;output=embed"
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                  title="Google 地圖：{e(shop)}（{e(address)}）"></iframe>
              </div>
            </div>
          </article>
"""


def _provision_shop_placeholder(name, shop, category, contact, address, social, items):
    """新店家登錄後自動化流程（2026-09-05教練裁示；2026-09-26教練拍板改成本機處理，
    不再繞到VPS——原本用VPS是為了「24小時不間斷、隨時能接收新店家」，但event.bymyway.com
    本身就已經是本機Mac在跑（透過Cloudflare Tunnel），Mac沒開機的話上傳流程本身也一樣會停，
    VPS並沒有真的多提供獨立於Mac之外的可用性，純粹多一層SSH管理成本。
    2026-09-05~26實際只用到3個真實店家(huitou/ema/鑫瀚昌)，遷移成本很低）：
    1. 產生event.bymyway.com/curated/<slug>/暫代頁，直接寫本機`CURATED_REPOS_DIR/<slug>/`
       並登記進curated_sites_registry.json（2026-09-27全站統一event網址，不再用shops.bymyway.com）
    2. 在tainan-shangquan首頁店家名冊插入一張真實卡片
    3. git commit+push，event.bymyway.com直接讀本機repo檔案，改完立即生效不用重啟服務
    任何一步失敗都不能擋住表單本身的DB寫入/Telegram通知，所以呼叫端要包try/except。
    回傳(slug, shop_url)供通知訊息使用；失敗回傳(None, None)。"""
    slug = _shop_slug(shop)
    registry_path = TAINAN_SHANGQUAN_REPO / "_shops_slugs.json"
    reg = {}
    if registry_path.is_file():
        try:
            raw_data = json.loads(registry_path.read_text(encoding="utf-8"))
            reg = {s: s for s in raw_data} if isinstance(raw_data, list) else raw_data
        except Exception:  # noqa: BLE001
            reg = {}
    # 2026-09-26鑫瀚昌旅行社事故修復：格式改成{品牌拼音key: 目前生效slug}，
    # key在這裡（第一次登記）算出後永遠不變，就算之後curation_process.py的
    # rename_shop_slug()把value改掉，下次同一家店上傳還是查得到（見該函式註解）。
    key = slug
    base_slug = slug
    n = 2
    # 2026-09-27起暫代頁跟策展網站共用 /curated/<slug>/，slug 不能撞到任何既有網站或資料夾
    taken = set(reg.values()) | _curated_slugs()
    while slug in taken or (CURATED_REPOS_DIR / slug).exists():
        slug = f"{base_slug}-{n}"
        n += 1
    reg[key] = slug
    registry_path.write_text(json.dumps(reg, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    shop_url = f"https://event.bymyway.com/curated/{slug}/"

    # 1. 產生暫代頁，直接寫本機（2026-09-26起不再SSH到VPS）
    placeholder_html = _shop_placeholder_html(name, shop, category, contact, address, social, items)
    shop_dir = CURATED_REPOS_DIR / slug
    shop_dir.mkdir(parents=True, exist_ok=True)
    (shop_dir / "index.html").write_text(placeholder_html, encoding="utf-8")
    # 登記進正式名單，/curated/<slug>/ 才會開放（2026-09-27全站統一event網址）
    cur = _load_curated_registry()
    cur.setdefault("sites", []).append({
        "slug": slug, "title": shop, "category": category, "address": address,
        "added_by": "shop-join-form", "description": "",
    })
    CURATED_REGISTRY_PATH.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. 插入tainan-shangquan首頁店家名冊卡片
    card_html = _shop_directory_card_html(name, shop, category, contact, address, social, items, shop_url)
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    content = index_path.read_text(encoding="utf-8")
    marker = "<!-- SHOP_CARDS_INSERT_POINT：新店家自動插入這行下面，勿刪除此標記 -->"
    if marker not in content:
        raise RuntimeError("SHOP_CARDS_INSERT_POINT標記不存在，無法自動插入卡片")
    content = content.replace(marker, marker + "\n" + card_html, 1)
    index_path.write_text(content, encoding="utf-8")

    # 3. git commit+push（本機repo檔案就是event.bymyway.com直接讀取的來源，改完立即生效）
    subprocess.run(["git", "add", "index.html", "_shops_slugs.json"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=30, env=_OPENCLAW_ENV)
    subprocess.run(
        ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com",
         "commit", "-q", "-m", f"自動化：新店家「{shop}」已建立版位({slug})"],
        cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=30, env=_OPENCLAW_ENV,
    )
    subprocess.run(["git", "push"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=30, env=_OPENCLAW_ENV)

    return slug, shop_url


@app.route("/api/tainan-shangquan/join", methods=["POST", "OPTIONS"])
def api_tainan_shangquan_join():
    """大臺南商圈整合計劃店家登錄（2026-09-04交辦，大台南策展中心店家招募落地頁）。
    純資料蒐集表單，非活動報名，沒有LINE加好友流程，送出即寫DB+推播Telegram通知。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    shop = (payload.get("shop") or "").strip()
    category = (payload.get("category") or "").strip()
    contact = (payload.get("contact") or "").strip()
    address = (payload.get("address") or "").strip()
    social = (payload.get("social") or "").strip()
    items = (payload.get("items") or "").strip()
    source = (payload.get("source") or "event.bymyway.com/tainan-shangquan").strip()

    if not name or not shop or not category or not contact or not address:
        _notify_xiaolongxia(
            "⚠️【大臺南商圈整合計劃・資料不完整，沒能存檔】\n"
            f"姓名：{name or '（沒填）'}\n店名：{shop or '（沒填）'}\n"
            f"類別：{category or '（沒填）'}\n聯絡方式：{contact or '（沒填）'}\n"
            f"地址：{address or '（沒填）'}\n請人工確認這位老闆有沒有真的要登錄。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": "missing required fields"}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    try:
        conn = db.get_conn()
        conn.execute(
            "INSERT INTO tainan_shangquan_signups "
            "(name, shop, category, contact, address, social, items, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, shop, category, contact, address, social, items, source),
        )
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(
            "⚠️【大臺南商圈整合計劃・資料庫寫入失敗】\n"
            f"姓名：{name}\n店名：{shop}\n錯誤：{e}\n請人工補登這筆資料。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": str(e)}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    provision_note = ""
    try:
        slug, shop_url = _provision_shop_placeholder(name, shop, category, contact, address, social, items)
        if shop_url:
            provision_note = f"\n✅ 已自動建好版位：{shop_url}\n（等TAVA AI網頁做好，把HTML包給軍師直接置換即可）"
    except Exception as e:  # noqa: BLE001
        provision_note = f"\n⚠️ 自動建版位失敗（DB已寫入，資料沒丟）：{e}\n請軍師手動補建。"

    notify_text = (
        "【大臺南商圈整合計劃・店家登錄通知】\n"
        f"姓名：{name}\n店名：{shop}（{category}）\n"
        f"聯絡方式：{contact}\n地址：{address}\n"
        + (f"社群：{social}\n" if social else "")
        + (f"招牌商品：{items}\n" if items else "")
        + f"（來源：{source}）"
        + provision_note
    )
    _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return Response(
        json.dumps({"ok": True}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


# ── 策展SOP自動上架（2026-09-06教練交辦）──────────────────────────────
# 教練用外部AI工具(TAVA AI/Tooo.ai/Lovart.ai等)做好店家/夥伴網站zip後，
# 從這個上傳頁丟檔案，`scripts/curation_process.py`(launchd WatchPaths事件觸發，
# 非輪詢)自動解壓縮+建GitHub repo+push+開Pages+登記進下面這個白名單registry。
# 這裡的路由永遠讀registry來決定哪些slug可以被公開服務，不是任何github_repos底下
# 的資料夾都能被存取——避免意外曝光bni-chapters等含個資/密碼的內部repo。
CURATED_REPOS_DIR = Path("/Users/bymyway/github_repos")
CURATION_UPLOAD_DIR = Path(__file__).resolve().parent / "curation_uploads"
CURATION_KINDS = {"shop": "店家策展", "creation": "大樹作品"}
CURATED_REGISTRY_PATH = Path(__file__).resolve().parent / "curated_sites_registry.json"
_CURATED_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,60}$")


def _load_curated_registry() -> dict:
    if not CURATED_REGISTRY_PATH.is_file():
        return {"sites": []}
    try:
        return json.loads(CURATED_REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"sites": []}


def _curated_slugs() -> set:
    return {s["slug"] for s in _load_curated_registry().get("sites", [])}


def _curated_redirect_target(slug: str):
    """slug被人工改短過的網站，舊slug不會留在_curated_slugs()裡。
    改名當下若有登記進registry的redirects表，這裡查得到就轉址過去，
    這樣任何已經發布出去的連結(FB貼文/名片/QR code)換名字後永遠不會死。"""
    return _load_curated_registry().get("redirects", {}).get(slug)


@app.route("/curated/<slug>/")
def curated_page(slug):
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    if slug not in _curated_slugs():
        target = _curated_redirect_target(slug)
        if target:
            return redirect(f"/curated/{target}/", code=301)
        abort(404)
    return _serve_repo_file(CURATED_REPOS_DIR / slug, "index.html")


@app.route("/curated/<slug>/<path:filename>")
def curated_assets(slug, filename):
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    if slug not in _curated_slugs():
        target = _curated_redirect_target(slug)
        if target:
            return redirect(f"/curated/{target}/{filename}", code=301)
        abort(404)
    if filename == "index.html":
        return curated_page(slug)
    return _serve_repo_file(CURATED_REPOS_DIR / slug, filename)


# 2026-09-27教練拍板：全站店家網址統一用 event.bymyway.com/curated/<slug>/。
# shops.bymyway.com 只剩「舊連結永久轉址」一個用途（名片/QR code/FB貼文上印過的舊網址點了照樣打得開），
# 本身不再供應任何檔案——之前這條路曾經把整個github_repos公開(試金石案例86)，現在整段拿掉。
_SHOPS_LEGACY_TARGETS = {"kr": "https://event.bymyway.com/KR/"}


@app.route("/<slug>/")
@app.route("/<slug>/<path:filename>")
def shops_legacy_redirect(slug, filename=""):
    if request.host.split(":")[0] != "shops.bymyway.com" or not _CURATED_SLUG_RE.match(slug):
        abort(404)
    if slug in _SHOPS_LEGACY_TARGETS:
        return redirect(_SHOPS_LEGACY_TARGETS[slug] + filename, code=301)
    return redirect(f"https://event.bymyway.com/curated/{slug}/{filename}", code=301)


def _remove_tainan_shangquan_card(event_url: str) -> bool:
    """把已上架店家從教練這裡手動下架時，順手拔掉大台南策展中心首頁的店家卡片。
    卡片格式固定來自curation_process.py的insert_tainan_shangquan_card()，
    比對含這個event_url的<article>整塊(含前一行說明註解)一起移除。"""
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    if not index_path.is_file():
        return False
    content = index_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(?:[ \t]*<!--[^\n]*-->\n)?[ \t]*<article\b[^>]*>(?:(?!</article>).)*?'
        + re.escape(event_url) + r'(?:(?!</article>).)*?</article>\n?',
        re.DOTALL,
    )
    new_content, n = pattern.subn("", content)
    if n == 0:
        return False
    index_path.write_text(new_content, encoding="utf-8")
    return True


def delete_curated_site(slug: str) -> tuple[bool, str]:
    """教練2026-09-06交辦：已上架的策展店家有些「有些人不喜歡」或資料有誤，
    要能自己登入刪掉，不用每次都叫軍師動手。這裡做的是「下架」不是真的抹除
    所有痕跡——本機資料夾搬去封存區(教練一貫原則：珍貴資料只搬不刪)，
    GitHub repo受限於token沒有delete_repo權限只能改名+關Pages做到「不再對外」，
    registry移除讓網址404，策展中心卡片同步拔掉。FB貼文若有發過不會自動處理，
    量少見時軍師人工個別刪除即可。"""
    registry = _load_curated_registry()
    site = next((s for s in registry.get("sites", []) if s["slug"] == slug), None)
    if not site:
        return False, "registry裡找不到這個slug，可能已經刪過了"

    registry["sites"] = [s for s in registry["sites"] if s["slug"] != slug]
    CURATED_REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    card_note = ""
    try:
        if _remove_tainan_shangquan_card(site.get("event_url", "")):
            subprocess.run(["git", "add", "index.html"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=15, env=_OPENCLAW_ENV)
            subprocess.run(
                ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com",
                 "commit", "-q", "-m", f"策展SOP下架：移除「{site.get('title', slug)}」"],
                cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=15, env=_OPENCLAW_ENV,
            )
            subprocess.run(["git", "push", "-q"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=30, env=_OPENCLAW_ENV)
        else:
            card_note = "（大台南策展中心沒找到對應卡片，可能本來就沒插入過，不影響下架結果）"
    except Exception as e:  # noqa: BLE001
        card_note = f"（策展中心卡片移除失敗，需要軍師人工檢查：{e}）"

    repo_dir = CURATED_REPOS_DIR / slug
    if repo_dir.is_dir():
        archive_dir = CURATED_REPOS_DIR / "_archive_curation_test_folders"
        archive_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        shutil.move(str(repo_dir), str(archive_dir / f"{slug}-deleted-{ts}"))

    github_note = ""
    try:
        subprocess.run(["gh", "api", "-X", "DELETE", f"repos/Coach1973/{slug}/pages"],
                        capture_output=True, timeout=15, env=_OPENCLAW_ENV)
        subprocess.run(["gh", "repo", "rename", f"_archived_{slug}", "-R", f"Coach1973/{slug}", "--yes"],
                        capture_output=True, timeout=15, env=_OPENCLAW_ENV)
    except Exception as e:  # noqa: BLE001
        github_note = f"（GitHub repo封存失敗，不影響教練這邊已看不到：{e}）"

    return True, f"已下架「{site.get('title', slug)}」{card_note}{github_note}"


@app.route("/curation/admin")
def curation_admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    return render_template("curation_admin.html", sites=_load_curated_registry().get("sites", [])[::-1])


@app.route("/curation/admin/delete/<slug>", methods=["POST"])
def curation_admin_delete(slug):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    ok, message = delete_curated_site(slug)
    return render_template(
        "curation_admin.html",
        sites=_load_curated_registry().get("sites", [])[::-1],
        result_message=message, result_ok=ok,
    )


@app.route("/curation/upload", methods=["GET", "POST"])
def curation_upload():
    """教練交辦(2026-09-06)：策展SOP的檔案入口。教練把AI工具做好的店家網站zip丟這裡，
    存進incoming/後就完成這一步——後續解壓縮/建repo/上架/登記店家名冊全部由
    launchd WatchPaths事件觸發的背景腳本自動處理，這個路由本身不做任何耗時的事，
    只負責收檔案，教練不用等頁面轉圈圈。"""
    # 兩種身分都能用：①教練/軍師既有的admin session ②教練發給任何AI的專屬上傳金鑰
    # (CURATION_UPLOAD_KEY，跟後台主密碼分開，就算被複製到公開網頁上洩漏，頂多被拿去
    # 亂上傳測試網站，不會拿到後台主密碼的權限，可隨時單獨換掉這把鑰匙不影響教練登入)
    supplied_key = request.values.get("key") or request.form.get("key") or ""
    key_ok = bool(CURATION_UPLOAD_KEY) and supplied_key == CURATION_UPLOAD_KEY
    if not _logged_in() and not key_ok:
        return redirect(url_for("admin_login", next=request.path))

    incoming = CURATION_UPLOAD_DIR / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)

    if request.method == "POST":
        # 2026-09-24團隊體檢：類型必須明講，不再預設走店家流程——09-23~24小龍蝦/赫米斯
        # 連兩次把大樹作品當店家上架，根因就是「沒講就走最熟的那條路」。
        kind = (request.values.get("kind") or "").strip()
        if kind not in CURATION_KINDS:
            return render_template("curation_upload.html", error="請先選擇類型：店家／合作夥伴網站，還是大樹教練個人作品（API呼叫請帶 kind=shop 或 kind=creation）", key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1]), 400
        f = request.files.get("package")
        if not f or not f.filename:
            return render_template("curation_upload.html", error="請選擇一個檔案", key=supplied_key, kind=kind, sites=_load_curated_registry().get("sites", [])[::-1]), 400
        original = f.filename
        ext = "".join(Path(original).suffixes)[-20:] or ".zip"
        if not re.search(r"\.(zip|tar\.gz|tgz)$", original, re.IGNORECASE):
            return render_template("curation_upload.html", error="只接受 .zip 或 .tar.gz 檔案", key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1]), 400
        # 2026-09-06教練拍板：源頭解決網址過長問題——不再靠系統猜品牌名轉拼音，
        # 改成上傳當下強制要求輸入自訂短網址，送出前確認好，之後不用再改名。
        custom_slug = (request.form.get("custom_slug") or "").strip().lower()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", custom_slug):
            return render_template("curation_upload.html", error="網址短名稱格式不對，只能用小寫英文字母/數字/短橫線，例如 niu-shi-ting", key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1]), 400
        if custom_slug in _curated_slugs():
            return render_template("curation_upload.html", error=f"「{custom_slug}」這個短網址已經被其他店家用過，請換一個", key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1]), 400
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r"[^\w.\-一-鿿]", "_", Path(original).stem)[:80]
        dest = incoming / f"{ts}__{safe_name}{ext}"
        # .slug/.kind 旁路檔要在壓縮檔本體之前寫好：WatchPaths一看到壓縮檔就會觸發處理
        (incoming / f"{dest.name}.slug").write_text(custom_slug, encoding="utf-8")
        (incoming / f"{dest.name}.kind").write_text(kind, encoding="utf-8")
        f.save(dest)
        _notify_xiaolongxia(
            f"📦【{CURATION_KINDS[kind]}・收到新檔案】\n檔案：{original}\n系統正在背景自動處理，完成上架後會再通知一次。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return render_template("curation_upload.html", uploaded=original, kind=kind, key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1])

    return render_template("curation_upload.html", key=supplied_key, sites=_load_curated_registry().get("sites", [])[::-1])


KR_REPO = Path("/Users/bymyway/github_repos/KR")


@app.route("/KR/")
def kr_page():
    return _serve_repo_file(KR_REPO, "index.html")


@app.route("/KR/<path:filename>")
def kr_assets(filename):
    if filename == "index.html":
        return kr_page()
    return _serve_repo_file(KR_REPO, filename)


@app.route("/api/KR/contact", methods=["POST", "OPTIONS"])
def api_kr_contact():
    """KR養生廚房聯絡表單（2026-09-04交辦，教練用Tooo.ai做的示範站原封不動搬過來）。
    原站表單打的是Tooo.ai自家的api.tooo.ai/widgets/form-submit.js，搬到我們自己網域後
    改推自己的DB+Telegram，不然訊息會送去教練管不到的第三方帳號，等於做半套。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone") or "").strip()
    subject = (payload.get("subject") or "").strip()
    message = (payload.get("message") or "").strip()
    source = (payload.get("source") or "event.bymyway.com/KR/contact").strip()

    if not name or not message:
        return Response(
            json.dumps({"ok": False, "error": "missing name/message"}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    try:
        conn = db.get_conn()
        conn.execute(
            "INSERT INTO kr_contact_messages (name, email, phone, subject, message, source) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, phone, subject, message, source),
        )
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(
            f"⚠️【KR養生廚房・留言資料庫寫入失敗】\n姓名：{name}\n錯誤：{e}\n請人工補登。",
            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID,
        )
        return Response(
            json.dumps({"ok": False, "error": str(e)}),
            status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    notify_text = (
        "【KR養生廚房・線上留言通知】\n"
        f"姓名：{name}\n"
        + (f"Email：{email}\n" if email else "")
        + (f"電話：{phone}\n" if phone else "")
        + (f"主旨：{subject}\n" if subject else "")
        + f"訊息：{message}\n（來源：{source}）"
    )
    _notify_xiaolongxia(notify_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return Response(
        json.dumps({"ok": True}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


CCU_SITE_DIR = Path(__file__).parent / "ccu_site"
CCU_WALL_EVENT_DEFAULT = "ccu-club-leadership"
# 2026-09-19 22:16教練交辦：活動已結束，現場能寫的心得/提問都寫了，之後路人若誤入頁面
# 亂留言的風險大於好處，關閉觀眾寫入功能（提問/按讚/心得），只留GET讓既有內容繼續顯示。
# 課後影音(/api/ccu/media PUT)不受影響，教練接下來還要上傳影音資料。
CCU_WALL_CLOSED = True
# 2026-09-19交辦：中正大學社團幹部專場(9/19早上)互動牆。教練把教練用tava-ai.com生成的
# 整包WordPress外掛+靜態頁丟過來，裁示「走我們的策展/上架SOP，直接掛event.bymyway.com」，
# 不用另外裝WordPress管一組新帳密——後端邏輯照抄WP外掛的資料結構跟API形狀，改用
# event-signup既有的Flask+event.db實作，前端index.html只改了API_BASE這一行指到/api/ccu。


@app.route("/ccu/")
def ccu_page():
    return send_from_directory(CCU_SITE_DIR, "index.html")


@app.route("/ccu/<path:filename>")
def ccu_assets(filename):
    return send_from_directory(CCU_SITE_DIR, filename)


def _wall_clean(raw, max_len):
    s = re.sub(r"<[^>]*>", "", str(raw or ""))
    s = re.sub(r"[\u200b-\u200f\u202a-\u202e]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:max_len]


def _wall_event(source):
    return _wall_clean(source.get("event"), 64) or CCU_WALL_EVENT_DEFAULT


def _wall_ip_hash():
    ip = (request.headers.get("X-Forwarded-For", request.remote_addr) or "").split(",")[0].strip()
    return hashlib.sha256((ip + "|event-wall-salt").encode()).hexdigest()


def _wall_admin_key(event):
    conn = db.get_conn()
    setting_key = f"event_wall_key_{event}"
    row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (setting_key,)).fetchone()
    if row:
        conn.close()
        return row["value"]
    key = secrets.token_urlsafe(15)
    conn.execute("INSERT INTO app_settings (key, value) VALUES (?, ?)", (setting_key, key))
    conn.commit()
    conn.close()
    return key


def _wall_is_admin(event):
    supplied = request.headers.get("X-Tava-Key") or request.args.get("key") or ""
    return bool(supplied) and hmac.compare_digest(supplied, _wall_admin_key(event))


def _wall_question_shape(row):
    return {
        "id": row["uid"], "event": row["event"], "topic": row["topic"], "body": row["body"],
        "name": row["name"], "votes": row["votes"], "answered": bool(row["answered"]), "ts": row["ts"],
    }


@app.route("/api/ccu/questions", methods=["GET", "POST"])
def api_ccu_questions():
    if request.method == "GET":
        event = _wall_event(request.args)
        conn = db.get_conn()
        rows = conn.execute(
            "SELECT * FROM event_wall_items WHERE event = ? AND kind = 'question' ORDER BY ts ASC LIMIT 2000",
            (event,),
        ).fetchall()
        conn.close()
        return Response(json.dumps([_wall_question_shape(r) for r in rows]), mimetype="application/json")

    if CCU_WALL_CLOSED:
        return Response(json.dumps({"error": "活動已結束，提問牆已關閉留言"}), status=410, mimetype="application/json")

    payload = request.get_json(force=True, silent=True) or {}
    event = _wall_event(payload)
    body = _wall_clean(payload.get("body"), 500)
    if len(body) < 2:
        return Response(json.dumps({"error": "問題內容太短了"}), status=400, mimetype="application/json")
    uid = _wall_clean(payload.get("id"), 40) or secrets.token_hex(12)
    ts = int(payload.get("ts") or 0) or int(datetime.now().timestamp() * 1000)
    topic = _wall_clean(payload.get("topic"), 64)
    name = _wall_clean(payload.get("name"), 40)
    conn = db.get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO event_wall_items (uid,event,kind,topic,body,name,votes,answered,ts,ip_hash) "
        "VALUES (?,?,?,?,?,?,0,0,?,?)",
        (uid, event, "question", topic, body, name, ts, _wall_ip_hash()),
    )
    conn.commit()
    conn.close()
    return Response(
        json.dumps({"id": uid, "event": event, "topic": topic, "body": body,
                     "name": name, "votes": 0, "answered": False, "ts": ts}),
        mimetype="application/json",
    )


@app.route("/api/ccu/questions/<qid>", methods=["PATCH"])
def api_ccu_patch_question(qid):
    payload = request.get_json(force=True, silent=True) or {}
    event = _wall_event(payload)
    if not _wall_is_admin(event):
        return Response(json.dumps({"error": "需要講者金鑰"}), status=403, mimetype="application/json")
    if "answered" not in payload:
        return Response(json.dumps({"error": "沒有可更新的欄位"}), status=400, mimetype="application/json")
    conn = db.get_conn()
    conn.execute(
        "UPDATE event_wall_items SET answered = ? WHERE uid = ? AND kind = 'question'",
        (1 if payload.get("answered") else 0, qid),
    )
    conn.commit()
    conn.close()
    return Response(json.dumps({"ok": True}), mimetype="application/json")


@app.route("/api/ccu/questions/<qid>/vote", methods=["POST"])
def api_ccu_vote(qid):
    if CCU_WALL_CLOSED:
        return Response(json.dumps({"error": "活動已結束，提問牆已關閉留言"}), status=410, mimetype="application/json")
    payload = request.get_json(force=True, silent=True) or {}
    delta = 1 if int(payload.get("delta") or 1) >= 0 else -1
    conn = db.get_conn()
    conn.execute(
        "UPDATE event_wall_items SET votes = MAX(0, votes + ?) WHERE uid = ? AND kind = 'question'",
        (delta, qid),
    )
    conn.commit()
    row = conn.execute("SELECT votes FROM event_wall_items WHERE uid = ?", (qid,)).fetchone()
    conn.close()
    return Response(json.dumps({"ok": True, "votes": row["votes"] if row else 0}), mimetype="application/json")


@app.route("/api/ccu/echoes", methods=["GET", "POST"])
def api_ccu_echoes():
    if request.method == "GET":
        event = _wall_event(request.args)
        conn = db.get_conn()
        rows = conn.execute(
            "SELECT * FROM event_wall_items WHERE event = ? AND kind = 'echo' ORDER BY ts ASC LIMIT 2000",
            (event,),
        ).fetchall()
        conn.close()
        return Response(
            json.dumps([{"id": r["uid"], "body": r["body"], "ts": r["ts"]} for r in rows]),
            mimetype="application/json",
        )

    if CCU_WALL_CLOSED:
        return Response(json.dumps({"error": "活動已結束，心得牆已關閉留言"}), status=410, mimetype="application/json")

    payload = request.get_json(force=True, silent=True) or {}
    event = _wall_event(payload)
    body = _wall_clean(payload.get("body"), 200)
    if len(body) < 2:
        return Response(json.dumps({"error": "內容太短了"}), status=400, mimetype="application/json")
    uid = _wall_clean(payload.get("id"), 40) or secrets.token_hex(12)
    ts = int(payload.get("ts") or 0) or int(datetime.now().timestamp() * 1000)
    conn = db.get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO event_wall_items (uid,event,kind,body,ts,ip_hash) VALUES (?,?,?,?,?,?)",
        (uid, event, "echo", body, ts, _wall_ip_hash()),
    )
    conn.commit()
    conn.close()
    return Response(json.dumps({"id": uid, "body": body, "ts": ts}), mimetype="application/json")


@app.route("/api/ccu/media", methods=["GET", "PUT"])
def api_ccu_media():
    if request.method == "GET":
        event = _wall_event(request.args)
        conn = db.get_conn()
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = ?", (f"event_wall_media_{event}",)
        ).fetchone()
        conn.close()
        return Response(row["value"] if row else "[]", mimetype="application/json")

    payload = request.get_json(force=True, silent=True) or {}
    event = _wall_event(payload)
    if not _wall_is_admin(event):
        return Response(json.dumps({"error": "需要講者金鑰"}), status=403, mimetype="application/json")
    items = payload.get("items")
    clean = []
    for it in (items if isinstance(items, list) else [])[:50]:
        if not isinstance(it, dict) or not it.get("src"):
            continue
        clean.append({
            "kind": "audio" if it.get("kind") == "audio" else "video",
            "title": _wall_clean(it.get("title"), 120),
            "desc": _wall_clean(it.get("desc"), 300),
            "src": _wall_clean(it.get("src"), 500),
            "poster": _wall_clean(it.get("poster"), 500),
        })
    conn = db.get_conn()
    setting_key = f"event_wall_media_{event}"
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (setting_key, json.dumps(clean, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()
    return Response(json.dumps(clean), mimetype="application/json")


DIY_KNOT_REPO = Path("/Users/bymyway/github_repos/diy-knot-workshop")
DIY_OUTDOOR_REPO = Path("/Users/bymyway/github_repos/diy-outdoor-workshop")
DIY_STUDIO_REPO = Path("/Users/bymyway/github_repos/diy-studio-workshop")
LEADERSHIP_KNOT_REPO = Path("/Users/bymyway/github_repos/leadership-knot-workshop")
SEABISCUIT20_REPO = Path("/Users/bymyway/github_repos/seabiscuit20")
# 2026-09-03交辦：DIY.zip「結繩工作坊3小時手作體驗」預覽頁，教練要求先掛兩個網址(/DIY/、/Leadership/)
# 讓他看效果，兩份內容目前完全相同(zip來源本身就是同一頁匯出兩次)，之後教練若要區分文案各自獨立改。
# 頁面本身無報名表單(教練提供的原稿寫死「請於粉專/來訊留下姓名，無虛假表單action」)，純靜態頁不需API。


@app.route("/DIY/")
def diy_knot_page():
    return _serve_repo_file(DIY_KNOT_REPO, "index.html")


@app.route("/DIY/<path:filename>")
def diy_knot_assets(filename):
    return _serve_repo_file(DIY_KNOT_REPO, filename)


# 2026-09-03交辦：design(5).zip「傘繩DIY-2戶外工作坊」，結繩工作坊(DIY)第二種排版風格(戶外求生風)，
# 報名/日期/費用/講師資訊比照/DIY/第一版，純靜態頁不需API。


@app.route("/Outdoor/")
def diy_outdoor_page():
    return _serve_repo_file(DIY_OUTDOOR_REPO, "index.html")


@app.route("/Outdoor/<path:filename>")
def diy_outdoor_assets(filename):
    return _serve_repo_file(DIY_OUTDOOR_REPO, filename)


# 2026-09-03交辦：DIY-3「傘繩DIY-3專業研習教室」，同一套視覺(沿用DIY-2)但改室內教室/商務人士定位，
# 報名/日期/費用/講師資訊比照第一版，純靜態頁不需API。


@app.route("/DIY3/")
def diy_studio_page():
    return _serve_repo_file(DIY_STUDIO_REPO, "index.html")


@app.route("/DIY3/<path:filename>")
def diy_studio_assets(filename):
    return _serve_repo_file(DIY_STUDIO_REPO, filename)


@app.route("/Leadership/")
def leadership_knot_page():
    return _serve_repo_file(LEADERSHIP_KNOT_REPO, "index.html")


@app.route("/Leadership/<path:filename>")
def leadership_knot_assets(filename):
    return _serve_repo_file(LEADERSHIP_KNOT_REPO, filename)


# 2026-09-04交辦：海餅乾俱樂部20週年官網，教練徹夜自製6頁(含近期場次/媒體報導)，純靜態頁不需API。


@app.route("/seabiscuit20/")
def seabiscuit20_page():
    return _serve_repo_file(SEABISCUIT20_REPO, "index.html")


@app.route("/seabiscuit20/<path:filename>")
def seabiscuit20_assets(filename):
    return _serve_repo_file(SEABISCUIT20_REPO, filename)


COACH888_STATE_KEYS = {
    "coach888_layout", "coach888_titles", "coach888_badges", "coach888_names", "coach888_collapse",
    "coach888_sections", "coach888_section_order", "coach888_items",
}


@app.route("/api/coach888/state", methods=["GET", "POST", "OPTIONS"])
def api_coach888_state():
    """coach888作品一覽的排版狀態集中存放(2026-09-03交辦)：教練在Mac改完排版，
    ACER開起來還是舊版——因為原本純靠每個瀏覽器自己的localStorage，裝置之間互不同步。
    這支端點讓coach888(GitHub Pages)存/取同一份狀態，取代各自為政的localStorage。
    GET：回傳目前6組狀態(找不到的key回null)。POST：body帶哪個key就更新哪個，其餘不動。
    2026-09-19：離開頁面前(beforeunload/pagehide)前端改用sendBeacon立即補送一次最新狀態，
    避免400ms防手震debounce來不及送出就被reload取消，導致最後一兩個動作被伺服器舊值蓋回去。
    sendBeacon的請求會帶credentials:'include'，CORS規範禁止搭配萬用字元'*'，
    所以這裡跟/api/coach888/click一樣回傳實際Origin+Allow-Credentials:true。"""
    resp_headers = {
        "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    conn = db.get_conn()
    if request.method == "GET":
        rows = conn.execute("SELECT key, value FROM coach888_state").fetchall()
        conn.close()
        state = {k: None for k in COACH888_STATE_KEYS}
        for r in rows:
            if r["key"] in COACH888_STATE_KEYS:
                state[r["key"]] = r["value"]
        return Response(
            json.dumps(state), status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )

    payload = request.get_json(force=True, silent=True) or {}
    updated = []
    for key, value in payload.items():
        if key not in COACH888_STATE_KEYS or value is None:
            continue
        conn.execute(
            "INSERT INTO coach888_state (key, value, updated_at) VALUES (?, ?, datetime('now', 'localtime')) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
            (key, json.dumps(value) if not isinstance(value, str) else value),
        )
        updated.append(key)
    conn.commit()
    conn.close()
    return Response(
        json.dumps({"ok": True, "updated": updated}),
        status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


@app.route("/api/coach888/click", methods=["POST", "OPTIONS"])
def api_coach888_click():
    """coach888「熱門排行」點擊計數(2026-09-18交辦)：教練點某個項目的連結就+1，
    純累加不覆蓋，多裝置點同一個url次數會加總，前端用navigator.sendBeacon呼叫。
    注意：sendBeacon的請求會帶credentials:'include'，CORS規範禁止credentialed
    請求搭配萬用字元'*'，且必須同時明確回傳Allow-Credentials:true，否則瀏覽器
    會擋下整個請求(本場實測navigate到本機8936埠點擊連結，兩個條件各自觸發過
    一次CORS錯誤才抓全)。"""
    resp_headers = {
        "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)

    payload = request.get_json(force=True, silent=True) or {}
    url = (payload.get("url") or "").strip()
    if not url or len(url) > 500:
        return Response(
            json.dumps({"ok": False, "error": "invalid url"}),
            status=400, headers={**resp_headers, "Content-Type": "application/json"},
        )
    conn = db.get_conn()
    conn.execute(
        "INSERT INTO coach888_clicks (url, click_count, last_clicked_at) VALUES (?, 1, datetime('now', 'localtime')) "
        "ON CONFLICT(url) DO UPDATE SET click_count = click_count + 1, last_clicked_at = excluded.last_clicked_at",
        (url,),
    )
    conn.commit()
    conn.close()
    return Response(
        json.dumps({"ok": True}), status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


@app.route("/api/coach888/click-counts", methods=["GET", "DELETE", "OPTIONS"])
def api_coach888_click_counts():
    """回傳所有url的累計點擊次數({url: count})，前端自己排序取前N名顯示熱門排行。
    DELETE(2026-09-24教練交辦)：熱門排行榜原本沒有刪除機制(獨立於layout/section外運作，
    見上方loadHotRanking()註解)，教練點進去發現活動早就結束了卻退不了榜，删不掉。
    刪法：直接把該url從coach888_clicks表移除，點擊次數歸零，下次排行重算自然不會再進榜；
    若教練之後又點擊該連結，會重新累計，這是預期行為（不是永久封鎖某網址上榜）。"""
    resp_headers = {
        "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    if request.method == "OPTIONS":
        return Response(status=204, headers=resp_headers)
    if request.method == "DELETE":
        payload = request.get_json(force=True, silent=True) or {}
        url = (payload.get("url") or request.args.get("url") or "").strip()
        if not url:
            return Response(
                json.dumps({"ok": False, "error": "missing url"}),
                status=400, headers={**resp_headers, "Content-Type": "application/json"},
            )
        conn = db.get_conn()
        conn.execute("DELETE FROM coach888_clicks WHERE url = ?", (url,))
        conn.commit()
        conn.close()
        return Response(
            json.dumps({"ok": True}), status=200, headers={**resp_headers, "Content-Type": "application/json"},
        )
    conn = db.get_conn()
    rows = conn.execute("SELECT url, click_count FROM coach888_clicks").fetchall()
    conn.close()
    counts = {r["url"]: r["click_count"] for r in rows}
    return Response(
        json.dumps(counts), status=200, headers={**resp_headers, "Content-Type": "application/json"},
    )


AI_ART_REPO = Path("/Users/bymyway/github_repos/ai-art")


@app.route("/ai-art/")
def ai_art_page():
    """9/16高雄場「當古典音樂遇到AI科技」。教練明確要求即時報名人數要能自己開關（show_live_count），
    預設隱藏（怕人數少影響報名意願），教練在/admin/sessions勾選後才會顯示，比照bigtree的字串替換手法。"""
    conn = db.get_conn()
    event = db.get_event(conn, "ai-art-0916")
    widget_html = ""
    if event and event["show_live_count"]:
        count = conn.execute(
            "SELECT COUNT(*) c FROM signups WHERE event_id = ?", (event["id"],)
        ).fetchone()["c"]
        widget_html = f'<div class="live-count-badge">🔥 已有 {count} 人報名</div>'
    conn.close()
    html = (AI_ART_REPO / "index.html").read_text(encoding="utf-8")
    html = html.replace("<!-- LIVE_COUNT_WIDGET -->", widget_html)
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/ai-art/<path:filename>")
def ai_art_assets(filename):
    if filename == "index.html":
        return ai_art_page()
    return _serve_repo_file(AI_ART_REPO, filename)


TODO_REMINDER_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "todo_reminder_check.py"
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
OPENCLAW_BIN = "/opt/homebrew/bin/openclaw"  # launchd服務的PATH不含homebrew，須用絕對路徑
# openclaw本身是node script，launchd預設PATH(/usr/bin:/bin:/usr/sbin:/sbin)也找不到node，
# 需要額外把homebrew/node安裝路徑塞進subprocess的環境變數
_OPENCLAW_ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/Users/bymyway/.local/bin:{os.environ.get('PATH', '')}"}


def _schedule_todo_reminder(todo_id, remind_at):
    """待辦有填提醒時間時，註冊一個精確時間點的OpenClaw一次性cron（事件觸發，
    不是每隔幾分鐘輪詢整張表——守則#07鐵律，2026-09-02 Stop hook攔下輪詢版本後改版）。
    回傳cron job id，失敗回傳None（不擋待辦本身新增成功）。"""
    if not remind_at:
        return None
    at_iso = remind_at.replace(" ", "T") + ":00"
    try:
        result = subprocess.run(
            [
                OPENCLAW_BIN, "cron", "create",
                "--name", f"todo-reminder-{todo_id}",
                "--at", at_iso,
                "--tz", "Asia/Taipei",
                "--command", f"python3 {TODO_REMINDER_SCRIPT} --todo-id {todo_id}",
                "--command-cwd", str(WORKSPACE_ROOT),
                "--no-deliver",
            ],
            capture_output=True, text=True, timeout=15, env=_OPENCLAW_ENV,
        )
        if result.returncode != 0:
            print(f"[todo] 排程提醒失敗(todo_id={todo_id}): {result.stderr}", flush=True)
            return None
        data = json.loads(result.stdout)
        return data.get("id")
    except Exception as e:  # noqa: BLE001
        print(f"[todo] 排程提醒發生例外(todo_id={todo_id}): {e}", flush=True)
        return None


def _cancel_todo_reminder(cron_id):
    """取消尚未觸發的一次性提醒cron（待辦被完成或刪除時呼叫，避免多餘通知）。"""
    if not cron_id:
        return
    try:
        subprocess.run(
            [OPENCLAW_BIN, "cron", "delete", cron_id],
            capture_output=True, text=True, timeout=15, env=_OPENCLAW_ENV,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[todo] 取消提醒cron失敗(cron_id={cron_id}): {e}", flush=True)


def _todo_due_badge(due_date_str):
    """回傳到期日徽章的顏色分級跟文字，None代表沒設到期日。"""
    if not due_date_str:
        return None
    try:
        y, m, d = (int(x) for x in due_date_str.split("-"))
        due = date(y, m, d)
    except ValueError:
        return None
    diff = (due - date.today()).days
    if diff < 0:
        return {"cls": "overdue", "label": f"已逾期{-diff}天"}
    if diff == 0:
        return {"cls": "today", "label": "今天到期"}
    if diff <= 3:
        return {"cls": "soon", "label": f"{diff}天後到期（{due_date_str}）"}
    return {"cls": "later", "label": due_date_str}


@app.route("/todo")
def todo_page():
    conn = db.get_conn()
    pending_rows = conn.execute(
        "SELECT * FROM todos WHERE completed = 0 ORDER BY (due_date IS NULL), due_date ASC, id ASC"
    ).fetchall()
    completed_rows = conn.execute(
        "SELECT * FROM todos WHERE completed = 1 ORDER BY completed_at DESC LIMIT 50"
    ).fetchall()
    conn.close()
    pending = [dict(r, due_badge=_todo_due_badge(r["due_date"])) for r in pending_rows]
    completed = [dict(r) for r in completed_rows]
    return render_template("todo.html", pending=pending, completed=completed)


@app.route("/todo/add", methods=["POST"])
def todo_add():
    title = (request.form.get("title") or "").strip()
    if title:
        notes = (request.form.get("notes") or "").strip() or None
        due_date = (request.form.get("due_date") or "").strip() or None
        remind_at = (request.form.get("remind_at") or "").strip().replace("T", " ") or None
        conn = db.get_conn()
        cur = conn.execute(
            "INSERT INTO todos (title, notes, due_date, remind_at) VALUES (?, ?, ?, ?)",
            (title, notes, due_date, remind_at),
        )
        todo_id = cur.lastrowid
        conn.commit()
        if remind_at:
            cron_id = _schedule_todo_reminder(todo_id, remind_at)
            if cron_id:
                conn.execute("UPDATE todos SET reminder_cron_id = ? WHERE id = ?", (cron_id, todo_id))
                conn.commit()
        conn.close()
    return redirect(url_for("todo_page"))


@app.route("/todo/<int:todo_id>/toggle", methods=["POST"])
def todo_toggle(todo_id):
    conn = db.get_conn()
    row = conn.execute("SELECT completed, reminder_cron_id FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row:
        new_val = 0 if row["completed"] else 1
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_val else None
        conn.execute(
            "UPDATE todos SET completed = ?, completed_at = ? WHERE id = ?",
            (new_val, completed_at, todo_id),
        )
        conn.commit()
        if new_val and row["reminder_cron_id"]:
            # 完成待辦時，尚未觸發的提醒沒有意義了，取消掉避免多餘通知
            _cancel_todo_reminder(row["reminder_cron_id"])
    conn.close()
    return redirect(url_for("todo_page"))


@app.route("/todo/<int:todo_id>/delete", methods=["POST"])
def todo_delete(todo_id):
    conn = db.get_conn()
    row = conn.execute("SELECT reminder_cron_id FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row and row["reminder_cron_id"]:
        _cancel_todo_reminder(row["reminder_cron_id"])
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("todo_page"))


# 2026-09-04交辦：Google Drive OAuth整合，讓/materials/新增資料夾時能自動用API列出裡面每個
# 檔案各自建卡片(而不是只能整個資料夾嵌入瀏覽器)。教練用seabiscuitclub@gmail.com帳號一次性
# 授權(drive.readonly唯讀範圍)，refresh_token永久存在credentials/google_drive_oauth.json
# (workspace .gitignore已排除該目錄，不會進git)。沒授權或API呼叫失敗時，自動退回舊版
# embeddedfolderview整個資料夾嵌入模式，不擋教練原本已經在用的流程。
GOOGLE_OAUTH_CREDS_PATH = WORKSPACE_ROOT / "credentials" / "google_drive_oauth.json"
GOOGLE_OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_DRIVE_MIME_MAP = {
    "presentation": "ppt",
    "pdf": "pdf",
    "image/": "image",
}


def _load_google_drive_creds():
    if not GOOGLE_OAUTH_CREDS_PATH.exists():
        return {}
    try:
        return json.loads(GOOGLE_OAUTH_CREDS_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def _save_google_drive_creds(data):
    GOOGLE_OAUTH_CREDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    GOOGLE_OAUTH_CREDS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _google_drive_access_token():
    """用refresh_token換一個新的access_token；沒授權過或換失敗回傳None。"""
    creds = _load_google_drive_creds()
    if not creds.get("refresh_token"):
        return None
    data = urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    try:
        req = urllib.request.Request(GOOGLE_TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get("access_token")
    except Exception as e:  # noqa: BLE001
        print(f"[materials] 換取access_token失敗: {e}", flush=True)
        return None


def _google_drive_mime_to_type(mime):
    for key, label in GOOGLE_DRIVE_MIME_MAP.items():
        if key in (mime or ""):
            return label
    return None


def _google_drive_list_folder(folder_id):
    """列出資料夾內所有檔案(不含子資料夾遞迴)，回傳[{id,name,mimeType}]；沒授權或失敗回傳None。"""
    token = _google_drive_access_token()
    if not token:
        return None
    q = f"'{folder_id}' in parents and trashed = false"
    url = "https://www.googleapis.com/drive/v3/files?" + urlencode({
        "q": q,
        "fields": "files(id,name,mimeType)",
        "pageSize": 200,
    })
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get("files", [])
    except Exception as e:  # noqa: BLE001
        print(f"[materials] 列出資料夾失敗(folder_id={folder_id}): {e}", flush=True)
        return None


@app.route("/materials/oauth/start")
def materials_oauth_start():
    creds = _load_google_drive_creds()
    if not creds.get("client_id"):
        return "尚未設定Google Drive憑證，請先完成credentials/google_drive_oauth.json設定。", 400
    params = {
        "client_id": creds["client_id"],
        "redirect_uri": creds.get("redirect_uri", "https://event.bymyway.com/materials/oauth/callback"),
        "response_type": "code",
        "scope": GOOGLE_OAUTH_SCOPE,
        "access_type": "offline",
        "prompt": "consent",  # 強制每次都核發refresh_token，避免舊授權沒有refresh_token
    }
    return redirect(GOOGLE_AUTH_URL + "?" + urlencode(params))


@app.route("/materials/oauth/callback")
def materials_oauth_callback():
    error = request.args.get("error")
    if error:
        return f"Google授權失敗：{error}", 400
    code = request.args.get("code")
    if not code:
        return "缺少授權碼，請重新從 /materials/oauth/start 開始。", 400
    creds = _load_google_drive_creds()
    data = urlencode({
        "code": code,
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "redirect_uri": creds.get("redirect_uri", "https://event.bymyway.com/materials/oauth/callback"),
        "grant_type": "authorization_code",
    }).encode()
    try:
        req = urllib.request.Request(GOOGLE_TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            token_data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return f"換取token失敗：{e.read().decode(errors='replace')}", 400
    refresh_token = token_data.get("refresh_token")
    if refresh_token:
        creds["refresh_token"] = refresh_token
        _save_google_drive_creds(creds)
    return redirect(url_for("materials_admin", authorized="1" if refresh_token else "0"))


# 2026-09-04交辦：教練課程教材線上觀看區。教練把PPT/PDF上傳自己的Google雲端硬碟(設定「知道連結
# 的人可檢視」)，這裡只存Drive檔案ID，實際畫面用Google Drive自己的embed viewer(iframe /preview)
# 渲染——不用自建PPT/PDF轉檔管線，學員在教練自己的網址看，但畫面渲染仍是Google Drive在做。
_DRIVE_FOLDER_PATTERN = re.compile(r"/folders/([a-zA-Z0-9_-]{10,})")
_DRIVE_ID_PATTERNS = [
    re.compile(r"/file/d/([a-zA-Z0-9_-]{10,})"),
    re.compile(r"[?&]id=([a-zA-Z0-9_-]{10,})"),
    re.compile(r"/d/([a-zA-Z0-9_-]{10,})"),
]


def _extract_drive_link(text):
    """接受完整Google Drive分享連結(單檔或資料夾)或純ID，回傳(link_type, drive_id)；
    格式不對回傳(None, None)。資料夾連結長這樣：drive.google.com/drive/folders/FOLDER_ID"""
    text = (text or "").strip()
    if not text:
        return None, None
    m = _DRIVE_FOLDER_PATTERN.search(text)
    if m:
        return "folder", m.group(1)
    if "/" not in text and "?" not in text:
        return "file", text  # 教練直接貼ID
    for pat in _DRIVE_ID_PATTERNS:
        m = pat.search(text)
        if m:
            return "file", m.group(1)
    return None, None


@app.route("/materials/")
def materials_page():
    """學員看的乾淨頁面，只顯示教練勾選公開的教材，沒有任何管理控制項。"""
    conn = db.get_conn()
    rows = conn.execute("SELECT * FROM materials WHERE visible = 1 ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("materials.html", items=[dict(r) for r in rows], is_admin=False)


@app.route("/materials/admin")
def materials_admin():
    """教練自己的後台：新增教材、勾選要公開哪些、刪除/展開資料夾。"""
    conn = db.get_conn()
    rows = conn.execute("SELECT * FROM materials ORDER BY id DESC").fetchall()
    conn.close()
    drive_authorized = bool(_load_google_drive_creds().get("refresh_token"))
    all_items = [dict(r) for r in rows]
    return render_template(
        "materials.html",
        items=[m for m in all_items if m["visible"]],
        all_items=sorted(all_items, key=lambda m: m["title"]),
        drive_authorized=drive_authorized,
        just_authorized=request.args.get("authorized"),
        is_admin=True,
    )


@app.route("/materials/add", methods=["POST"])
def materials_add():
    title = (request.form.get("title") or "").strip()
    link = (request.form.get("drive_link") or "").strip()
    link_type, drive_id = _extract_drive_link(link)
    if title and drive_id:
        description = (request.form.get("description") or "").strip() or None
        file_type = (request.form.get("file_type") or "").strip() or None
        conn = db.get_conn()
        if link_type == "folder":
            # 有授權過就用Drive API把資料夾展開成一筆一筆個別檔案卡片；
            # 沒授權或API失敗就退回舊版整個資料夾embeddedfolderview嵌入(不擋教練原有流程)。
            # 資料夾整批匯入的檔案預設不公開(visible=0)——教練上傳資料夾常常沒特別篩選過，
            # 要先讓他勾選想公開的，不能整批直接show給學員看。
            files = _google_drive_list_folder(drive_id)
            if files is not None:
                for f in files:
                    f_title = f.get("name") or title
                    f_type = _google_drive_mime_to_type(f.get("mimeType"))
                    conn.execute(
                        "INSERT INTO materials (title, description, drive_file_id, file_type, link_type, visible) VALUES (?, ?, ?, ?, 'file', 0)",
                        (f_title, description, f.get("id"), f_type),
                    )
            else:
                conn.execute(
                    "INSERT INTO materials (title, description, drive_file_id, file_type, link_type, visible) VALUES (?, ?, ?, ?, 'folder', 1)",
                    (title, description, drive_id, file_type),
                )
        else:
            # 教練貼單一檔案連結是明確指定要公開這一份，直接visible=1
            conn.execute(
                "INSERT INTO materials (title, description, drive_file_id, file_type, link_type, visible) VALUES (?, ?, ?, ?, 'file', 1)",
                (title, description, drive_id, file_type),
            )
        conn.commit()
        conn.close()
    else:
        all_items = [dict(r) for r in db.get_conn().execute("SELECT * FROM materials ORDER BY id DESC").fetchall()]
        return render_template(
            "materials.html",
            items=[m for m in all_items if m["visible"]],
            all_items=sorted(all_items, key=lambda m: m["title"]),
            drive_authorized=bool(_load_google_drive_creds().get("refresh_token")),
            error="標題或Google雲端硬碟連結格式看起來不對，請確認後再送出一次（單一檔案連結要包含 drive.google.com/file/d/，資料夾連結要包含 drive.google.com/drive/folders/，或直接貼ID）。",
            is_admin=True,
        )
    return redirect(url_for("materials_admin"))


@app.route("/materials/<int:material_id>/delete", methods=["POST"])
def materials_delete(material_id):
    conn = db.get_conn()
    conn.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("materials_admin"))


@app.route("/materials/<int:material_id>/expand", methods=["POST"])
def materials_expand(material_id):
    """把一筆整個資料夾嵌入的舊卡片，展開成一筆一筆個別檔案卡片(授權完成後才會有這顆按鈕)。
    展開出來的每一筆預設不公開(visible=0)，教練勾選過才會顯示給學員。"""
    conn = db.get_conn()
    row = conn.execute("SELECT * FROM materials WHERE id = ? AND link_type = 'folder'", (material_id,)).fetchone()
    if row:
        files = _google_drive_list_folder(row["drive_file_id"])
        if files:
            for f in files:
                conn.execute(
                    "INSERT INTO materials (title, description, drive_file_id, file_type, link_type, visible) VALUES (?, ?, ?, ?, 'file', 0)",
                    (f.get("name") or row["title"], row["description"], f.get("id"), _google_drive_mime_to_type(f.get("mimeType"))),
                )
            conn.execute("DELETE FROM materials WHERE id = ?", (material_id,))
            conn.commit()
    conn.close()
    return redirect(url_for("materials_admin"))


@app.route("/materials/visibility", methods=["POST"])
def materials_visibility():
    """教練在勾選清單裡選好要公開哪些教材後送出，這裡整批更新visible狀態
    (被勾選的checkbox才會出現在request.form，沒勾的完全不會送出，所以先全部設0再把勾選的設1)。"""
    checked_ids = {int(x) for x in request.form.getlist("visible_ids") if x.isdigit()}
    conn = db.get_conn()
    all_ids = [r["id"] for r in conn.execute("SELECT id FROM materials").fetchall()]
    for mid in all_ids:
        conn.execute("UPDATE materials SET visible = ? WHERE id = ?", (1 if mid in checked_ids else 0, mid))
    conn.commit()
    conn.close()
    return redirect(url_for("materials_admin"))


CICA_REPO = Path("/Users/bymyway/github_repos/cica")


@app.route("/cica/")
def cica_page():
    return _serve_repo_file(CICA_REPO, "index.html")


@app.route("/cica/<path:filename>")
def cica_assets(filename):
    return _serve_repo_file(CICA_REPO, filename)


LIN_BEIYI_REPO = Path("/Users/bymyway/github_repos/lin-beiyi")


@app.route("/lin-beiyi/")
def lin_beiyi_page():
    return _serve_repo_file(LIN_BEIYI_REPO, "index.html")


@app.route("/lin-beiyi/<path:filename>")
def lin_beiyi_assets(filename):
    if filename == "index.html":
        return lin_beiyi_page()
    return _serve_repo_file(LIN_BEIYI_REPO, filename)


HARBOUR66_REPO = Path("/Users/bymyway/github_repos/66-harbour")


@app.route("/66-harbour/")
def harbour66_page():
    return _serve_repo_file(HARBOUR66_REPO, "index.html")


@app.route("/66-harbour/<path:filename>")
def harbour66_assets(filename):
    if filename == "index.html":
        return harbour66_page()
    return _serve_repo_file(HARBOUR66_REPO, filename)


TPAR_REPO = Path("/Users/bymyway/github_repos/tainan-pickleball-art-rotary")


@app.route("/tainan-pickleball-art-rotary/")
def tpar_page():
    return _serve_repo_file(TPAR_REPO, "index.html")


@app.route("/tainan-pickleball-art-rotary/<path:filename>")
def tpar_assets(filename):
    if filename == "index.html":
        return tpar_page()
    return _serve_repo_file(TPAR_REPO, filename)


KINGMAUII_REPO = Path("/Users/bymyway/github_repos/kingmauii-brand-site-github")


@app.route("/kingmauii-brand-site-github/")
def kingmauii_page():
    return _serve_repo_file(KINGMAUII_REPO, "index.html")


@app.route("/kingmauii-brand-site-github/<path:filename>")
def kingmauii_assets(filename):
    if filename == "index.html":
        return kingmauii_page()
    return _serve_repo_file(KINGMAUII_REPO, filename)


QIKOUZAO_REPO = Path("/Users/bymyway/github_repos/qikouzao")


@app.route("/qikouzao/")
def qikouzao_page():
    return _serve_repo_file(QIKOUZAO_REPO, "index.html")


@app.route("/qikouzao/<path:filename>")
def qikouzao_assets(filename):
    if filename == "index.html":
        return qikouzao_page()
    return _serve_repo_file(QIKOUZAO_REPO, filename)


# ── 一鍵發布：教練貼網址說「請更新/請發布」，小龍蝦/Hermes呼叫這支API即可完成 ──
# 2026-09-11教練交辦：ai-forum-taichung這類讀活repo的網站，內容改在GitHub（Lenovo/
# ACER任一台推送都行），但這台Mac讀的是本機github_repos/下的clone，沒人在Mac執行
# git pull就不會反映最新內容。跟tainan-shangquan（內容寫進資料庫，POST當下就生效，
# 完全不需要git pull這一步）不是同一種架構，所以少了「不用經過Mac」這個特性。
# 補一支通用端點：把「git pull」這個唯一缺的動作也變成一次HTTP呼叫，
# 小龍蝦/Hermes只要會打curl就能觸發，不用開Mac的Claude Code對話框。
SITE_SYNC_KEY = os.environ.get("SITE_SYNC_KEY", "")
SITE_SYNC_REPOS = {
    "bigtree": BIGTREE_REPO,
    "ai-forum": AI_FORUM_REPO,
    "ai-talk": AI_TALK_REPO,
    "tainan-calender": TAINAN_CALENDAR_REPO,
    "bni-traffic": BNI_TRAFFIC_REPO,
    "tainan-shangquan": TAINAN_SHANGQUAN_REPO,
    "tut-alumni": TUT_ALUMNI_REPO,
    "1010": EVENT_1010_REPO,
    "KR": KR_REPO,
    "diy-knot-workshop": DIY_KNOT_REPO,
    "diy-outdoor-workshop": DIY_OUTDOOR_REPO,
    "diy-studio-workshop": DIY_STUDIO_REPO,
    "leadership-knot-workshop": LEADERSHIP_KNOT_REPO,
    "seabiscuit20": SEABISCUIT20_REPO,
    "ai-art": AI_ART_REPO,
    "cica": CICA_REPO,
    "lin-beiyi": LIN_BEIYI_REPO,
    "66-harbour": HARBOUR66_REPO,
    "tainan-pickleball-art-rotary": TPAR_REPO,
    "kingmauii-brand-site-github": KINGMAUII_REPO,
    "qikouzao": QIKOUZAO_REPO,
}


@app.route("/api/site-update/<repo_name>", methods=["POST", "GET"])
def api_site_update(repo_name):
    supplied_key = request.values.get("key") or ""
    if not SITE_SYNC_KEY or supplied_key != SITE_SYNC_KEY:
        return Response(json.dumps({"ok": False, "error": "invalid key"}), status=403,
                         headers={"Content-Type": "application/json"})
    repo_path = SITE_SYNC_REPOS.get(repo_name)
    if repo_path is None:
        return Response(
            json.dumps({"ok": False, "error": f"unknown repo: {repo_name}",
                        "known_repos": sorted(SITE_SYNC_REPOS.keys())}, ensure_ascii=False),
            status=404, headers={"Content-Type": "application/json"},
        )
    if not repo_path.exists():
        return Response(json.dumps({"ok": False, "error": f"repo path missing on disk: {repo_path}"}),
                         status=404, headers={"Content-Type": "application/json"})
    try:
        pull = subprocess.run(["git", "-C", str(repo_path), "pull", "--ff-only"],
                               capture_output=True, text=True, timeout=30)
        commit = subprocess.run(["git", "-C", str(repo_path), "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, timeout=10).stdout.strip()
        return Response(
            json.dumps({"ok": pull.returncode == 0, "repo": repo_name, "commit": commit,
                        "output": (pull.stdout + pull.stderr).strip()}, ensure_ascii=False),
            status=200 if pull.returncode == 0 else 500,
            headers={"Content-Type": "application/json"},
        )
    except Exception as exc:
        return Response(json.dumps({"ok": False, "error": str(exc)}), status=500,
                         headers={"Content-Type": "application/json"})


# ── 隱私政策頁：Meta App Review「隱私政策網址」欄位要求 (2026-09-11) ──
_PRIVACY_POLICY_HTML = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>隱私政策｜大樹教練粉專發文小幫手</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC",sans-serif;max-width:720px;margin:40px auto;padding:0 20px;line-height:1.8;color:#222}
h1{font-size:1.6rem;border-bottom:3px solid #CF2030;padding-bottom:10px}
h2{font-size:1.2rem;margin-top:2em;color:#CF2030}
footer{margin-top:3em;color:#888;font-size:0.85rem}
</style>
</head>
<body>
<h1>隱私政策</h1>
<p>本頁說明「大樹教練粉專發文小幫手」（下稱本應用程式）如何處理資料。</p>

<h2>應用程式用途</h2>
<p>本應用程式僅供應用程式擁有者（大樹教練／吳大樹）本人使用，用於管理自己名下管理的 Facebook 粉絲專頁，
包括發佈貼文、讀取貼文內容與粉絲專頁基本互動資料。本應用程式不對外開放第三方使用者登入或授權，
也不會為其他企業或個人管理其 Facebook 資產。</p>

<h2>資料蒐集與使用</h2>
<p>本應用程式透過 Facebook Graph API 存取以下資料：</p>
<ul>
<li>應用程式擁有者本人管理的粉絲專頁清單（<code>pages_show_list</code>）</li>
<li>發佈、編輯粉絲專頁貼文（<code>pages_manage_posts</code>）</li>
<li>讀取粉絲專頁貼文與互動洞察報告（<code>pages_read_engagement</code>）</li>
</ul>
<p>上述資料僅用於應用程式擁有者本人管理自己粉絲專頁內容之用途，不會蒐集一般訪客或粉絲專頁追蹤者的個人資料，
不會將任何資料出售、出租或提供予第三方，也不會用於廣告投放以外的商業用途。</p>

<h2>資料保存與刪除</h2>
<p>本應用程式不另行儲存 Facebook 提供的資料副本；所有資料皆即時透過 Facebook Graph API 存取，
不留存於應用程式自有的資料庫。如需刪除授權，應用程式擁有者可隨時於
<a href="https://www.facebook.com/settings?tab=business_tools" target="_blank" rel="noopener">Facebook 設定頁面</a>
移除本應用程式的存取權限。</p>

<h2>聯絡方式</h2>
<p>如對本隱私政策有任何疑問，請透過 <a href="mailto:seabiscuitclub@gmail.com">seabiscuitclub@gmail.com</a> 聯絡。</p>

<footer>最後更新：2026-09-11</footer>
</body>
</html>"""


@app.route("/privacy-policy/fb-poster-app")
def privacy_policy_fb_poster_app():
    return Response(_PRIVACY_POLICY_HTML, headers={"Content-Type": "text/html; charset=utf-8"})


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("EVENT_PORT", 5060)))
