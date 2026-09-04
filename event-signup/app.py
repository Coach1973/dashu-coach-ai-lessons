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


def _serve_repo_file(repo: Path, filename: str):
    top = filename.split("/", 1)[0]
    if top in _REPO_BLOCKED_TOP_DIRS or filename.startswith("."):
        abort(404)
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
    "coach888_sections", "coach888_section_order",
}


@app.route("/api/coach888/state", methods=["GET", "POST", "OPTIONS"])
def api_coach888_state():
    """coach888作品一覽的排版狀態集中存放(2026-09-03交辦)：教練在Mac改完排版，
    ACER開起來還是舊版——因為原本純靠每個瀏覽器自己的localStorage，裝置之間互不同步。
    這支端點讓coach888(GitHub Pages)存/取同一份狀態，取代各自為政的localStorage。
    GET：回傳目前6組狀態(找不到的key回null)。POST：body帶哪個key就更新哪個，其餘不動。"""
    resp_headers = {
        "Access-Control-Allow-Origin": "*",
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


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("EVENT_PORT", 5060)))
