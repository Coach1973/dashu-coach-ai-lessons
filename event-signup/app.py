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
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
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
    按下傳送才算完成binding+登記抽獎（webhook比對這句話裡的姓名寫入line_user_id）。
    2026-10-31教練：後台設定表 app_settings 有 lottery_join_url（例如「零基礎學AI」LINE群邀請連結）時，
    一律改導去那個連結（加入群組即可參加抽獎）；沒設定就維持原本官方LINE問候語。"""
    conn = db.get_conn()
    row = conn.execute("SELECT value FROM app_settings WHERE key = 'lottery_join_url'").fetchone()
    conn.close()
    if row and (row["value"] or "").startswith("https://line.me/"):
        return row["value"]
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

# 2026-10-19教練：「活動報名即時通知」群裡提到某關鍵字的報名通知，同步轉發到指定的群（原文照轉）。
# 報名通知一發出就轉（事件觸發，不輪詢、不靠小龍蝦盯）。要多轉一個群＝這裡多加一行：
#   Telegram 群寫 "telegram_chat_id"（不扣額度，建議用這個）；LINE 群寫 "group_id"（推播扣月額度，群組按人數算）。
GROUP_FORWARD_RULES = [
    {"keyword": "香檳下午茶", "group_id": "C37ef97aa4155577abfb2f6a53500d8b3", "name": "小旭老師報名通知"},
]
# LINE 官方帳號每月推播只有 200 則（教練 2026-08-24 裁示 LINE 會扣配額）；本月剩餘低於這個數就不轉、只留紀錄，
# 避免把額度用光、害別的通知送不出去（試金石案例62）。
LINE_FORWARD_MIN_QUOTA = 30


# ==== LINE_PUSH_GATE_V2（教練 2026-10-20 常設禁令：所有 LINE 小龍蝦沒有教練許可，不得使用會扣額度的推播）====
# 這裡轉 LINE 群用的是「龍蝦小助教」的金鑰，推播會扣它的月額度，所以也要過閘門。
# 許可旗標 ~/.openclaw/workspace/state/LINE_PUSH_APPROVED：內容＝許可當下的 Unix 秒數，10 分鐘有效；
# 教練口頭同意才建（scripts/line_push_approve.sh），用完 --revoke 刪檔。只看內容、不看修改時間（V2，2026-10-22）。
LINE_PUSH_STATE_DIR = os.path.expanduser("~/.openclaw/workspace/state/")  # 測試時換到暫存資料夾


def _line_push_gate(source: str, to: str, text: str) -> None:
    base = LINE_PUSH_STATE_DIR
    try:
        with open(base + "LINE_PUSH_APPROVED", encoding="utf-8") as f:
            raw = f.read().strip()
        if raw.isascii() and raw.isdigit() and 0 <= time.time() - int(raw) < 600:
            return
    except (OSError, ValueError):
        pass
    try:
        ts = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        with open(base + "line_push_blocked.log", "a", encoding="utf-8") as f:
            f.write(f"{ts}\t{source}\tpush\t{to}\t{' '.join(str(text).split())[:40]}\n")
    except Exception:
        pass
    raise RuntimeError("LINE 推播（會扣額度）已被教練常設禁令擋下，需教練同意才可送")
# ==== /LINE_PUSH_GATE_V2 ====


def _line_forward_one(token: str, group_id: str, text: str) -> None:
    """推一則文字進 LINE 群；額度不夠或 LINE 回錯都丟例外，由呼叫端寫進 notify_failures.log。"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def call(path: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(
            f"https://api.line.me/v2/bot/{path}", method="POST" if body is not None else "GET", headers=headers,
            data=json.dumps(body).encode("utf-8") if body is not None else None,
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")

    quota = call("message/quota")
    if quota.get("type") == "limited":
        used = call("message/quota/consumption").get("totalUsage", 0)
        left = quota.get("value", 0) - used
        if left < LINE_FORWARD_MIN_QUOTA:
            raise RuntimeError(f"LINE 本月額度剩 {left} 則，低於保留線 {LINE_FORWARD_MIN_QUOTA}，沒轉")
    _line_push_gate("event-signup-forward", group_id, text)
    call("message/push", {"to": group_id, "messages": [{"type": "text", "text": text[:4900]}]})


def _forward_by_keyword(text: str) -> None:
    """報名通知含關鍵字 → 同步轉發到對應的群（Telegram 群或 LINE 群）。
    失敗只留痕跡，不影響「活動報名即時通知」那則原本的通知與報名本身。"""
    rules = [r for r in GROUP_FORWARD_RULES if r["keyword"] in text]
    for r in rules:
        if r.get("telegram_chat_id"):
            # 目標不是報名群，所以不會再觸發轉發；送不出去它自己會寫進 notify_failures.log
            _notify_xiaolongxia(text, chat_id=r["telegram_chat_id"])
    line_rules = [r for r in rules if r.get("group_id")]
    if not line_rules:
        return
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            token = json.load(f)["channels"]["line"]["channelAccessToken"]
    except Exception as e:
        for r in line_rules:
            _log_notify_failure(f"line:{r['group_id']}", f"讀不到 LINE 金鑰: {e!r}", text)
        return
    for r in line_rules:
        try:
            _line_forward_one(token, r["group_id"], text)
        except Exception as e:
            _log_notify_failure(f"line:{r['group_id']}({r['name']})", repr(e), text)


def _notify_xiaolongxia(text: str, chat_id: str = TELEGRAM_NOTIFY_CHAT_ID) -> bool:
    """發Telegram訊息，預設給教練個人對話；報名通知改傳group chat_id同時通知佩佩老師。

    失敗不影響網頁本身回應，但 🔴 一定要留下痕跡——
    2026-08-17~08-23 教練整整一週收不到報名通知，就是因為舊版 LINE 通知函式
    用 `except: pass` 把 HTTP 429（月配額用完）整個吞掉，沒有任何 log、沒有任何人知道，
    教練還以為報名系統壞了（試金石案例62）。從此：靜默失敗一律不准，至少寫一行。
    """
    if chat_id == TELEGRAM_REGISTRATION_GROUP_CHAT_ID:
        # 含關鍵字就同步轉進 LINE 群；放背景執行緒，不拖慢報名頁回應，也不受 Telegram 成敗影響
        threading.Thread(target=_forward_by_keyword, args=(text,), daemon=True).start()
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


VAULT_EXTRA_PATH = Path(__file__).resolve().parent / "vault_extra.json"


def _vault_entries():
    """上面寫死的帳密表 ＋ vault_extra.json（scripts/coach888_register_admin.py 登記新後台時自動追加，
    2026-10-10：信任遊戲後台做好沒進 /vault，教練才發現）。檔案壞掉不影響原本的表。"""
    entries = list(VAULT_ENTRIES)
    try:
        for e in json.loads(VAULT_EXTRA_PATH.read_text(encoding="utf-8")):
            if e.get("url") and all(e["url"] != x["url"] for x in entries):
                entries.append({"name": e.get("name", ""), "url": e["url"], "user": e.get("user", "（不需要帳密）"),
                                "password": e.get("password", "—")})
    except (OSError, ValueError, AttributeError):
        pass
    return entries


@app.route("/vault")
def vault():
    if not session.get("vault_logged_in"):
        return redirect(url_for("vault_login", next=request.path))
    return render_template("vault.html", entries=_vault_entries())


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


# ---------- 南應大校友會台南分會：理監事團隊與顧問團隊（2026-10-14 教練交辦）：說明見 tut_team.py ----------
# 比照 BNI 分會頁自助簡介：按「我要建立檔案」→ 送出立刻上架 → 拿專屬修改連結；顧問空座位本人點名字補資料。
import tut_team as _tt

_TT_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多建立 10 份


def _tt_html(body, status=200):
    return Response(body, status=status, content_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store"})


def _tt_rate_ok(ip):
    now = time.time()
    hits = [t for t in _TT_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 10:
        return False
    _TT_HITS[ip] = hits + [now]
    return True


def _tt_notify(token):
    """有人新上架（含認領顧問座位第一次補完）→ 活動報名即時通知群（教練＋佩佩老師），附後台網址方便處理亂填。"""
    r = _tt.get_by_token(token)
    if not r:
        return
    role = f"／{r['role']}" if r["role"] else ""
    text = (f"🎓【南應大校友會・理監事與顧問】{r['name']} 建立了檔案（{_tt.TEAMS.get(r['team'], '')}{role}）\n"
            f"{r['company_title']}\n公開頁：\nhttps://event.bymyway.com/tut/team\n"
            f"管理後台（有人亂填可隱藏或刪除）：\n{_tt.admin_url(app.secret_key)}")
    threading.Thread(target=_notify_xiaolongxia, args=(text,),
                     kwargs={"chat_id": TELEGRAM_REGISTRATION_GROUP_CHAT_ID}, daemon=True).start()


def _tt_photo(form_file, err):
    """有選照片就存；回傳 (檔名或 None, 錯誤訊息)。"""
    if err or not (form_file and form_file.filename):
        return None, err
    name = _tt.save_photo(form_file)
    return name, ("" if name else "這張照片打不開，麻煩改存成 jpg 或 png 再上傳一次")


def _tt_build_ok():
    """教練的「建置模式」專屬連結（?build=簽章短碼，同後台簽章）：對才回短碼，沒帶或錯回空字串。"""
    code = request.args.get("build", "")
    return code if code and hmac.compare_digest(code.encode(), _tt.admin_code(app.secret_key).encode()) else ""


@app.route("/tut/team")
@app.route("/tut/team/")
def tut_team_index():
    return _tt_html(_tt.render_index(_tt_build_ok()))


@app.route("/api/tut/team/board")
def tut_team_board_api():
    """記憶牆（/curated/tut-memory/）的「理監事校友名單」讀這裡，跟 /tut/team 是同一份資料（2026-10-23 教練）。"""
    return Response(json.dumps(_tt.board_public(_tt_build_ok()), ensure_ascii=False), content_type="application/json; charset=utf-8",
                    headers={"Cache-Control": "no-store", "Access-Control-Allow-Origin": "*"})


@app.route("/tut/b/<code>")
def tut_team_build_short(code):
    """教練的建置模式短網址（簽章短碼，同後台）→ 團隊頁建置模式。"""
    _tt_admin(code)
    return redirect(f"/tut/team?build={code}")


@app.route("/tut/m/<code>")
def tut_memory_build_short(code):
    """同上，但回到記憶牆「加入校友會」的理監事校友名單（建置模式）。"""
    _tt_admin(code)
    return redirect(f"/curated/tut-memory/?build={code}#join")


@app.route("/tut/team/join", methods=["GET", "POST"])
def tut_team_join():
    if request.method == "GET":
        return _tt_html(_tt.render_join())
    if (request.form.get("website") or "").strip():   # honeypot：機器人才會填
        return redirect("/tut/team")
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _tt_rate_ok(ip):
        return _tt_html(_tt.render_join(request.form, "這個小時送出次數太多了，請稍後再試一次"), 429)
    photo = request.files.get("photo")
    d, err = _tt.clean_form(request.form, need_photo=not (photo and photo.filename))
    fname, err = _tt_photo(photo, err)
    if err:
        return _tt_html(_tt.render_join(d, err), 400)
    token = _tt.insert(d, fname, ip)
    _tt_notify(token)
    return redirect(f"/tut/team/edit/{token}?new=1")


@app.route("/tut/team/claim/<int:mid>", methods=["POST"])
def tut_team_claim(mid):
    """顧問空座位：本人點自己的名字就進到修改頁（誠信原則，比照 BNI 認座位）；已補完的不能再認領。"""
    r = _tt.get_by_id(mid)
    if not r or r["filled"] or r["hidden"]:
        return redirect("/tut/team/join")
    return redirect(f"/tut/team/edit/{r['edit_token']}")


@app.route("/tut/team/edit/<token>", methods=["GET", "POST"])
def tut_team_edit(token):
    r = _tt.get_by_token(token)
    if not r:
        abort(404)
    build = _tt_build_ok()   # 教練的建置模式：可只補一部分、不發通知
    if request.method == "GET":
        return _tt_html(_tt.render_edit(r, first=request.args.get("new") == "1", saved=request.args.get("saved") == "1", build=build))
    photo = request.files.get("photo")
    d, err = _tt.clean_form(request.form, need_photo=not r["photo_file"] and not (photo and photo.filename), partial=bool(build))
    fname, err = _tt_photo(photo, err)
    if err:
        return _tt_html(_tt.render_edit(r, d, err, build=build), 400)
    _tt.update(r["id"], d, fname)
    if fname and r["photo_file"] and _tt.PHOTO_RE.match(r["photo_file"]):
        (_tt.UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)   # 換照片就把舊的刪掉
    if not r["filled"] and not build:   # 認領的顧問座位第一次補完＝上架
        _tt_notify(token)
        return redirect(f"/tut/team/edit/{token}?new=1")
    return redirect(f"/tut/team/edit/{token}?saved=1" + (f"&build={build}" if build else ""))


@app.route("/tut/team/edit/<token>/delete", methods=["POST"])
def tut_team_delete(token):
    r = _tt.get_by_token(token)
    if not r:
        abort(404)
    _tt.delete(r["id"])
    return redirect("/tut/team")


@app.route("/tut/team/photo/<name>")
def tut_team_photo(name):
    if not _tt.PHOTO_RE.match(name) or not (_tt.UPLOAD_DIR / name).exists():
        abort(404)
    resp = send_from_directory(_tt.UPLOAD_DIR, name, mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "public, max-age=86400"   # 換照片會換檔名，可以放心快取
    return resp


def _tt_admin(code):
    if not hmac.compare_digest(code, _tt.admin_code(app.secret_key)):
        abort(404)


@app.route("/tut/team/a/<code>")
def tut_team_admin(code):
    _tt_admin(code)
    return _tt_html(_tt.render_admin(app.secret_key, request.args.get("msg", "")[:60]))


@app.route("/tut/team/a/<code>/hide/<int:mid>", methods=["POST"])
def tut_team_admin_hide(code, mid):
    _tt_admin(code)
    _tt.set_hidden(mid, request.form.get("hidden") == "1")
    return redirect(f"/tut/team/a/{code}")


@app.route("/tut/team/a/<code>/delete/<int:mid>", methods=["POST"])
def tut_team_admin_delete(code, mid):
    _tt_admin(code)
    _tt.delete(mid)
    return redirect(f"/tut/team/a/{code}?msg=已刪除")


@app.route("/tut/team/a/<code>/seat", methods=["POST"])
def tut_team_admin_seat(code):
    _tt_admin(code)
    name = (request.form.get("name") or "").strip()
    team = request.form.get("team") or "board"
    if name and team in _tt.TEAMS:
        _tt.add_seat(team, (request.form.get("role") or "").strip(), name, (request.form.get("company_title") or "").strip())
    return redirect(f"/tut/team/a/{code}?msg=已新增座位：{name}" if name else f"/tut/team/a/{code}")


# ---------- 互動教材學習報告（2026-10-25 教練交辦：bni-gusest 來賓接待工作坊）：說明見 game_report.py ----------
import game_report as _gr

_GR_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多送 20 份


@app.route("/api/game/report", methods=["POST"])
def game_report_submit():
    def reply(body, status=200):
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json")

    payload = request.get_json(force=True, silent=True) or {}
    if (payload.get("website") or "").strip():          # 防機器人的隱藏欄位：假裝成功
        return reply({"ok": True, "url": ""})
    site = (payload.get("site") or "").strip()
    if not _CURATED_SLUG_RE.match(site) or site not in _curated_slugs():
        return reply({"ok": False, "error": "找不到這個互動教材"}, 404)
    d, err = _gr.clean(payload)
    if err:
        return reply({"ok": False, "error": err}, 400)
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _GR_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 20:
        return reply({"ok": False, "error": "送出次數太多，請稍後再試"}, 429)
    _GR_HITS[ip] = hits + [now]
    title = next((s.get("title") for s in _load_curated_registry().get("sites", []) if s["slug"] == site), site) or site
    token = _gr.save(site, title, d, ip)
    if not d["name"].startswith(_gr.TEST_PREFIX):
        who = d["name"] + (f"（{d['chapter']}）" if d["chapter"] else "")
        text = (f"📝【{d['game'] or title}】{who} 完成學習報告\n{_gr.summary_line(d)}\n"
                f"看報告：\n{_gr.report_url(token)}\n全部報告（講師後台）：\n{_gr.admin_url(app.secret_key, site)}")
        threading.Thread(target=_notify_xiaolongxia, args=(text,),
                         kwargs={"chat_id": TELEGRAM_REGISTRATION_GROUP_CHAT_ID}, daemon=True).start()
    return reply({"ok": True, "url": _gr.report_url(token)})


@app.route("/game-report/<token>")
def game_report_view(token):
    r = _gr.get(token)
    if not r:
        abort(404)
    return Response(_gr.render_report(r), content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


@app.route("/gr/<code>")
@app.route("/game-report/a/<code>")
def game_report_admin(code):
    if not hmac.compare_digest(code, _gr.admin_code(app.secret_key)):
        abort(404)
    site = request.args.get("site", "").strip()
    return Response(_gr.render_admin(_gr.list_reports(site), site), content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


# ---------- 顧問師天團人氣排序＋到訪次數（2026-10-25 教練交辦，比照 mentor100）：說明見 skyteam_stats.py ----------
import skyteam_stats as _sts


def _sts_json(obj, status=200):
    return Response(json.dumps(obj, ensure_ascii=False), status=status,
                    headers={"Content-Type": "application/json", "Cache-Control": "no-store"})


@app.route("/api/skyteam/visit", methods=["POST"])
def skyteam_visit():
    """頁面載入時呼叫一次：記一筆到訪（含重複造訪），回傳目前的到訪數與各人點擊數。"""
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _sts.is_bot(request.headers.get("User-Agent", "")) and _sts.allowed(ip):
        _sts.log_visit(ip)
    return _sts_json(_sts.stats())


@app.route("/api/skyteam/ranking", methods=["GET"])
def skyteam_ranking():
    """只讀各人點擊數（不記到訪）：邀請函頁用它跟首頁排名同步。"""
    return _sts_json({"clicks": _sts.stats().get("clicks", {})})


@app.route("/api/skyteam/click", methods=["POST"])
def skyteam_click():
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if _sts.is_bot(request.headers.get("User-Agent", "")) or not _sts.allowed(ip):
        return ("", 204)
    payload = request.get_json(force=True, silent=True) or {}
    return ("", 204) if _sts.log_click(payload.get("name")) else ("", 400)


# ---------- 「零基礎學 AI」現場互動頁後端（2026-10-31）：說明見 nmda_ai.py ----------
import nmda_ai as _nai
app.register_blueprint(_nai.bp)


# ---------- 中華新媒體影音發展協會（NMDA）理監事團隊（2026-10-23 教練交辦）：說明見 nmda_team.py ----------
# 照南應大 /tut/team 同一套：名單先放空座位，本人點自己的名字補照片簡介；公開頁是 nmda 網站自己的 team.html，讀 /api/nmda/team/board。
import nmda_team as _nt

_NT_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多建立 10 份


def _nt_html(body, status=200):
    return Response(body, status=status, content_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store"})


def _nt_rate_ok(ip):
    now = time.time()
    hits = [t for t in _NT_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 10:
        return False
    _NT_HITS[ip] = hits + [now]
    return True


def _nt_notify(token):
    """有人新上架（含認領空座位第一次補完）→ 活動報名即時通知群，附後台網址方便處理亂填。"""
    r = _nt.get_by_token(token)
    if not r:
        return
    role = f"（{r['role']}）" if r["role"] else ""
    text = (f"🎬【中華新媒體影音發展協會・理監事團隊】{r['name']}{role} 建立了檔案\n"
            f"{r['company_title']}\n公開頁：\n{_nt.PAGE_URL}\n"
            f"管理後台（有人亂填可隱藏或刪除）：\n{_nt.admin_url(app.secret_key)}")
    threading.Thread(target=_notify_xiaolongxia, args=(text,),
                     kwargs={"chat_id": TELEGRAM_REGISTRATION_GROUP_CHAT_ID}, daemon=True).start()


def _nt_photo(form_file, err):
    """有選照片就存；回傳 (檔名或 None, 錯誤訊息)。"""
    if err or not (form_file and form_file.filename):
        return None, err
    name = _nt.save_photo(form_file)
    return name, ("" if name else "這張照片打不開，麻煩改存成 jpg 或 png 再上傳一次")


def _nt_build_ok():
    """教練的「建置模式」專屬連結（?build=簽章短碼，同後台簽章）：對才回短碼，沒帶或錯回空字串。"""
    code = request.args.get("build", "")
    return code if code and hmac.compare_digest(code.encode(), _nt.admin_code(app.secret_key).encode()) else ""


def _nt_admin(code):
    if not hmac.compare_digest(code, _nt.admin_code(app.secret_key)):
        abort(404)


@app.route("/api/nmda/team/board")
def nmda_team_board_api():
    """NMDA 網站 team.html 讀這裡（跟本檔所有編輯頁是同一份資料）。"""
    return Response(json.dumps(_nt.board_public(_nt_build_ok()), ensure_ascii=False), content_type="application/json; charset=utf-8",
                    headers={"Cache-Control": "no-store", "Access-Control-Allow-Origin": "*"})


@app.route("/nmda/b/<code>")
def nmda_team_build_short(code):
    """教練的建置模式短網址（簽章短碼，同後台）→ NMDA 理監事團隊頁建置模式。"""
    _nt_admin(code)
    return redirect(f"/curated/nmda/team.html?build={code}")


@app.route("/nmda/team/join", methods=["GET", "POST"])
def nmda_team_join():
    if request.method == "GET":
        return _nt_html(_nt.render_join())
    if (request.form.get("website") or "").strip():   # honeypot：機器人才會填
        return redirect("/curated/nmda/team.html")
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _nt_rate_ok(ip):
        return _nt_html(_nt.render_join(request.form, "這個小時送出次數太多了，請稍後再試一次"), 429)
    photo = request.files.get("photo")
    d, err = _nt.clean_form(request.form, need_photo=not (photo and photo.filename))
    fname, err = _nt_photo(photo, err)
    if err:
        return _nt_html(_nt.render_join(d, err), 400)
    token = _nt.insert(d, fname, ip)
    _nt_notify(token)
    return redirect(f"/nmda/team/edit/{token}?new=1")


@app.route("/nmda/team/claim/<int:mid>", methods=["POST"])
def nmda_team_claim(mid):
    """空座位：本人點自己的名字就進到修改頁（誠信原則，比照 BNI 認座位）；已補完的不能再認領。"""
    r = _nt.get_by_id(mid)
    if not r or r["filled"] or r["hidden"]:
        return redirect("/nmda/team/join")
    return redirect(f"/nmda/team/edit/{r['edit_token']}")


@app.route("/nmda/team/edit/<token>", methods=["GET", "POST"])
def nmda_team_edit(token):
    r = _nt.get_by_token(token)
    if not r:
        abort(404)
    build = _nt_build_ok()   # 教練的建置模式：可只補一部分、不發通知
    if request.method == "GET":
        return _nt_html(_nt.render_edit(r, first=request.args.get("new") == "1", saved=request.args.get("saved") == "1", build=build))
    photo = request.files.get("photo")
    d, err = _nt.clean_form(request.form, need_photo=not r["photo_file"] and not (photo and photo.filename), partial=bool(build))
    fname, err = _nt_photo(photo, err)
    if err:
        return _nt_html(_nt.render_edit(r, d, err, build=build), 400)
    _nt.update(r["id"], d, fname)
    if fname and r["photo_file"] and _nt.PHOTO_RE.match(r["photo_file"]):
        (_nt.UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)   # 換照片就把舊的刪掉
    if not r["filled"] and not build:   # 認領的空座位第一次補完＝上架
        _nt_notify(token)
        return redirect(f"/nmda/team/edit/{token}?new=1")
    return redirect(f"/nmda/team/edit/{token}?saved=1" + (f"&build={build}" if build else ""))


@app.route("/nmda/team/edit/<token>/delete", methods=["POST"])
def nmda_team_delete(token):
    r = _nt.get_by_token(token)
    if not r:
        abort(404)
    _nt.delete(r["id"])
    return redirect("/curated/nmda/team.html")


@app.route("/nmda/team/photo/<name>")
def nmda_team_photo(name):
    if not _nt.PHOTO_RE.match(name) or not (_nt.UPLOAD_DIR / name).exists():
        abort(404)
    resp = send_from_directory(_nt.UPLOAD_DIR, name, mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "public, max-age=86400"   # 換照片會換檔名，可以放心快取
    return resp


@app.route("/nmda/team/a/<code>")
def nmda_team_admin(code):
    _nt_admin(code)
    return _nt_html(_nt.render_admin(app.secret_key, request.args.get("msg", "")[:60]))


@app.route("/nmda/team/a/<code>/hide/<int:mid>", methods=["POST"])
def nmda_team_admin_hide(code, mid):
    _nt_admin(code)
    _nt.set_hidden(mid, request.form.get("hidden") == "1")
    return redirect(f"/nmda/team/a/{code}")


@app.route("/nmda/team/a/<code>/delete/<int:mid>", methods=["POST"])
def nmda_team_admin_delete(code, mid):
    _nt_admin(code)
    _nt.delete(mid)
    return redirect(f"/nmda/team/a/{code}?msg=已刪除")


@app.route("/nmda/team/a/<code>/seat", methods=["POST"])
def nmda_team_admin_seat(code):
    _nt_admin(code)
    name = (request.form.get("name") or "").strip()
    if name:
        _nt.add_seat((request.form.get("role") or "").strip(), name, (request.form.get("company_title") or "").strip())
    return redirect(f"/nmda/team/a/{code}?msg=已新增座位：{name}" if name else f"/nmda/team/a/{code}")


# ---------- 中華新媒體影音發展協會（NMDA）會員資料（2026-10-30 教練交辦）：說明見 nmda_members.py ----------
# 照上面的理監事團隊同一套：會員自己建立檔案、送出即上架；公開頁是 nmda 網站自己的 members.html，讀 /api/nmda/members/board。
import nmda_members as _nm

_NM_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多建立 10 份


def _nm_rate_ok(ip):
    now = time.time()
    hits = [t for t in _NM_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 10:
        return False
    _NM_HITS[ip] = hits + [now]
    return True


def _nm_notify(token):
    """有人新建立檔案 → 活動報名即時通知群，附後台網址方便處理亂填。"""
    r = _nm.get_by_token(token)
    if not r:
        return
    text = (f"🎬【中華新媒體影音發展協會・會員資料】{r['name']} 建立了檔案\n"
            f"{r['company_title']}\n公開頁：\n{_nm.PAGE_URL}\n"
            f"管理後台（有人亂填可隱藏或刪除）：\n{_nm.admin_url(app.secret_key)}")
    threading.Thread(target=_notify_xiaolongxia, args=(text,),
                     kwargs={"chat_id": TELEGRAM_REGISTRATION_GROUP_CHAT_ID}, daemon=True).start()


def _nm_photo(form_file, err):
    """有選照片就存；回傳 (檔名或 None, 錯誤訊息)。"""
    if err or not (form_file and form_file.filename):
        return None, err
    name = _nm.save_photo(form_file)
    return name, ("" if name else "這張照片打不開，麻煩改存成 jpg 或 png 再上傳一次")


def _nm_admin(code):
    if not hmac.compare_digest(code, _nm.admin_code(app.secret_key)):
        abort(404)


@app.route("/api/nmda/members/board")
def nmda_members_board_api():
    """NMDA 網站 members.html 讀這裡（跟本段所有編輯頁是同一份資料）。"""
    return Response(json.dumps(_nm.board_public(), ensure_ascii=False), content_type="application/json; charset=utf-8",
                    headers={"Cache-Control": "no-store", "Access-Control-Allow-Origin": "*"})


@app.route("/nmda/members/join", methods=["GET", "POST"])
def nmda_members_join():
    if request.method == "GET":
        return _nt_html(_nm.render_join())
    if (request.form.get("website") or "").strip():   # honeypot：機器人才會填
        return redirect("/curated/nmda/members.html")
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _nm_rate_ok(ip):
        return _nt_html(_nm.render_join(request.form, "這個小時送出次數太多了，請稍後再試一次"), 429)
    photo = request.files.get("photo")
    d, err = _nm.clean_form(request.form, need_photo=not (photo and photo.filename))
    fname, err = _nm_photo(photo, err)
    if err:
        return _nt_html(_nm.render_join(d, err), 400)
    token = _nm.insert(d, fname, ip)
    _nm_notify(token)
    return redirect(f"/nmda/members/edit/{token}?new=1")


@app.route("/nmda/members/edit/<token>", methods=["GET", "POST"])
def nmda_members_edit(token):
    r = _nm.get_by_token(token)
    if not r:
        abort(404)
    if request.method == "GET":
        return _nt_html(_nm.render_edit(r, first=request.args.get("new") == "1", saved=request.args.get("saved") == "1"))
    photo = request.files.get("photo")
    d, err = _nm.clean_form(request.form, need_photo=not r["photo_file"] and not (photo and photo.filename))
    fname, err = _nm_photo(photo, err)
    if err:
        return _nt_html(_nm.render_edit(r, d, err), 400)
    _nm.update(r["id"], d, fname)
    if fname and r["photo_file"] and _nm.PHOTO_RE.match(r["photo_file"]):
        (_nm.UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)   # 換照片就把舊的刪掉
    return redirect(f"/nmda/members/edit/{token}?saved=1")


@app.route("/nmda/members/edit/<token>/delete", methods=["POST"])
def nmda_members_delete(token):
    r = _nm.get_by_token(token)
    if not r:
        abort(404)
    _nm.delete(r["id"])
    return redirect("/curated/nmda/members.html")


@app.route("/nmda/members/photo/<name>")
def nmda_members_photo(name):
    if not _nm.PHOTO_RE.match(name) or not (_nm.UPLOAD_DIR / name).exists():
        abort(404)
    resp = send_from_directory(_nm.UPLOAD_DIR, name, mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "public, max-age=86400"   # 換照片會換檔名，可以放心快取
    return resp


_NM_LOGIN_FAILS = {}   # ip -> [失敗時間戳]；10 分鐘內失敗 5 次就先鎖住，擋猜密碼


def _nm_staff():
    return bool(session.get("nmda_members_admin"))


@app.route("/nmda/members/login", methods=["GET", "POST"])
def nmda_members_login():
    """協會工作人員的後台登入（帳號 admin；密碼只存雜湊）。登入成功只開 NMDA 會員資料後台，不影響大樹的其他後台。"""
    if request.method == "GET":
        return _nt_html(_nm.render_login())
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    fails = [t for t in _NM_LOGIN_FAILS.get(ip, []) if now - t < 600]
    if len(fails) >= 5:
        return _nt_html(_nm.render_login("嘗試次數太多，請 10 分鐘後再試"), 429)
    user = (request.form.get("username") or "").strip()
    ok = hmac.compare_digest(user.encode(), _nm.ADMIN_USER.encode()) & check_password_hash(_nm.ADMIN_PASS_HASH, request.form.get("password") or "")
    if not ok:
        _NM_LOGIN_FAILS[ip] = fails + [now]
        return _nt_html(_nm.render_login("帳號或密碼不對"), 401)
    _NM_LOGIN_FAILS.pop(ip, None)
    session["nmda_members_admin"] = True
    session.permanent = True
    return redirect("/nmda/members/admin")


@app.route("/nmda/members/logout", methods=["POST"])
def nmda_members_logout():
    session.pop("nmda_members_admin", None)
    return redirect("/nmda/members/login")


@app.route("/nmda/members/admin")
def nmda_members_staff_admin():
    if not _nm_staff():
        return redirect("/nmda/members/login")
    return _nt_html(_nm.render_admin(app.secret_key, request.args.get("msg", "")[:60], staff=True))


@app.route("/nmda/members/admin/hide/<int:mid>", methods=["POST"])
def nmda_members_staff_hide(mid):
    if not _nm_staff():
        return redirect("/nmda/members/login")
    _nm.set_hidden(mid, request.form.get("hidden") == "1")
    return redirect("/nmda/members/admin")


@app.route("/nmda/members/admin/delete/<int:mid>", methods=["POST"])
def nmda_members_staff_delete(mid):
    if not _nm_staff():
        return redirect("/nmda/members/login")
    _nm.delete(mid)
    return redirect("/nmda/members/admin?msg=已刪除")


@app.route("/nmda/members/a/<code>")
def nmda_members_admin(code):
    _nm_admin(code)
    return _nt_html(_nm.render_admin(app.secret_key, request.args.get("msg", "")[:60]))


@app.route("/nmda/members/a/<code>/hide/<int:mid>", methods=["POST"])
def nmda_members_admin_hide(code, mid):
    _nm_admin(code)
    _nm.set_hidden(mid, request.form.get("hidden") == "1")
    return redirect(f"/nmda/members/a/{code}")


@app.route("/nmda/members/a/<code>/delete/<int:mid>", methods=["POST"])
def nmda_members_admin_delete(code, mid):
    _nm_admin(code)
    _nm.delete(mid)
    return redirect(f"/nmda/members/a/{code}?msg=已刪除")


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
_CURATED_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,60}$")


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


def _shangquan_card_pattern(event_url):
    """含這個網址的店家卡片整塊(含前一行說明註解)。刪除、下架、重新上架共用同一個比對規則。
    event_url 可以是一個字串，或一串網址（任何一個出現在卡片裡都算）。"""
    urls = [event_url] if isinstance(event_url, str) else list(event_url)
    return re.compile(
        r'(?:[ \t]*<!--[^\n]*-->\n)?[ \t]*<article\b[^>]*>(?:(?!</article>).)*?'
        + "(?:" + "|".join(re.escape(u) for u in urls) + ")" + r'(?:(?!</article>).)*?</article>\n?',
        re.DOTALL,
    )


def _site_card_urls(site: dict) -> list:
    """這個網站的卡片可能出現的網址寫法：正式網址、GitHub Pages 網址、/<slug>/。
    早期上架的卡片用的是舊網址格式，只認 event_url 會漏掉它們（鑫瀚昌、迴頭快剪等）。"""
    urls = [site.get("event_url") or "", site.get("github_pages_url") or "", f"/{site['slug']}/"]
    return [u for u in urls if u]


def _remove_tainan_shangquan_card(event_url: str) -> bool:
    """把已上架店家從教練這裡手動下架時，順手拔掉大台南策展中心首頁的店家卡片。
    卡片格式固定來自curation_process.py的insert_tainan_shangquan_card()，
    比對含這個event_url的<article>整塊(含前一行說明註解)一起移除。"""
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    if not index_path.is_file():
        return False
    content = index_path.read_text(encoding="utf-8")
    new_content, n = _shangquan_card_pattern(event_url).subn("", content)
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


def _publish_shangquan_index(message: str) -> None:
    """把大台南策展中心首頁(index.html)的改動 commit + push（失敗會丟例外，由呼叫端決定怎麼說）。"""
    subprocess.run(["git", "add", "index.html"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=15, env=_OPENCLAW_ENV)
    subprocess.run(
        ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com", "commit", "-q", "-m", message],
        cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=15, env=_OPENCLAW_ENV,
    )
    subprocess.run(["git", "push", "-q"], cwd=TAINAN_SHANGQUAN_REPO, check=True, timeout=30, env=_OPENCLAW_ENV)


def _fire_all_works_refresh(reason: str) -> None:
    """「完整作品一覽」(Coach1973/all-works) 資料更新：下架／重新上架／刪除按下去的那一刻背景跑一次（事件觸發，不輪詢）。
    不等結果、不擋後台操作；測試用的假名冊不觸發。"""
    if CURATED_REGISTRY_PATH != Path(__file__).resolve().parent / "curated_sites_registry.json":
        return
    try:
        script = Path(__file__).resolve().parent.parent / "scripts" / "all_works_refresh.py"
        log_file = open(script.parent.parent / "state" / "all_works_refresh.log", "a", encoding="utf-8")
        subprocess.Popen([sys.executable, str(script), "--reason", reason],
                         stdout=log_file, stderr=subprocess.STDOUT, start_new_session=True, env=_OPENCLAW_ENV)
    except Exception:  # noqa: BLE001  更新一覽失敗不能影響後台本身
        pass


def _save_curated_registry(registry: dict) -> None:
    CURATED_REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def unlist_curated_site(slug: str) -> tuple[bool, str]:
    """教練2026-10-07交辦：「下架」只能讓網站不出現在大台南策展中心，不能讓網站不見。
    這裡只做一件事：把策展中心首頁的卡片收起來，卡片原文存進名冊（重新上架時原樣放回）。
    網址、本機資料夾、GitHub repo、名冊條目全部不動，所以教練點進去還看得到、後台清單也還在。
    真的要讓網站消失（重複、上錯）才用 delete_curated_site()。"""
    registry = _load_curated_registry()
    site = next((s for s in registry.get("sites", []) if s["slug"] == slug), None)
    if not site:
        return False, "名冊裡找不到這個網站"
    title = site.get("title", slug)
    if site.get("listed") is False:
        return False, f"「{title}」已經是下架狀態，網站本身一直都在"
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    content = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    m = None if site.get("no_shop_card") else _shangquan_card_pattern(_site_card_urls(site)).search(content)
    if not m:
        return False, f"「{title}」本來就沒有展示在大台南策展中心，不需要下架，網站照常保留"
    site["listed"] = False
    site["card_html"] = m.group(0)
    site["unlisted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    _save_curated_registry(registry)  # 先把卡片原文存進名冊，再動首頁：中途出事也不會弄丟卡片
    index_path.write_text(content[:m.start()] + content[m.end():], encoding="utf-8")
    note = ""
    try:
        _publish_shangquan_index(f"策展SOP下架（只收起卡片，網站保留）：「{title}」")
    except Exception as e:  # noqa: BLE001
        note = f"（卡片已收起，但同步到 GitHub 失敗，需要軍師檢查：{e}）"
    return True, f"已下架「{title}」：不再出現在大台南策展中心，網站和資料都還在，隨時可以重新上架{note}"


def relist_curated_site(slug: str) -> tuple[bool, str]:
    """把下架的網站卡片原樣放回大台南策展中心首頁（插入點：SHOP_CARDS_INSERT_POINT 那行下面）。"""
    registry = _load_curated_registry()
    site = next((s for s in registry.get("sites", []) if s["slug"] == slug), None)
    if not site:
        return False, "名冊裡找不到這個網站"
    title = site.get("title", slug)
    if site.get("listed") is not False:
        return False, f"「{title}」現在就是展示狀態"
    card = site.get("card_html") or ""
    if not card:
        return False, f"名冊裡沒有保存「{title}」的卡片內容，需要軍師補卡片（網站本身沒問題）"
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    content = index_path.read_text(encoding="utf-8")
    if _shangquan_card_pattern(_site_card_urls(site)).search(content):
        pass  # 卡片已經在首頁了，只需要把狀態改回來
    else:
        marker = content.find("SHOP_CARDS_INSERT_POINT")
        if marker < 0:
            return False, "找不到策展中心首頁的卡片插入點，需要軍師檢查"
        insert_at = content.index("\n", marker) + 1
        if content[insert_at:insert_at + 1] == "\n":
            insert_at += 1  # 插入點後面本來就有一個空行，卡片放在空行後面，跟原本一模一樣
        if not card.endswith("\n"):
            card += "\n"
        index_path.write_text(content[:insert_at] + card + content[insert_at:], encoding="utf-8")
    for k in ("listed", "card_html", "unlisted_at"):
        site.pop(k, None)
    _save_curated_registry(registry)
    note = ""
    try:
        _publish_shangquan_index(f"策展SOP重新上架：「{title}」")
    except Exception as e:  # noqa: BLE001
        note = f"（卡片已放回，但同步到 GitHub 失敗，需要軍師檢查：{e}）"
    return True, f"已重新上架「{title}」，大台南策展中心首頁又看得到了{note}"


def _curation_admin_context() -> dict:
    """後台清單要的資料：全部網站（新的在前）＋目前真的有卡片展示在策展中心首頁的 slug。"""
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    content = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    sites = _load_curated_registry().get("sites", [])[::-1]
    carded = {s["slug"] for s in sites
              if s.get("listed") is not False and not s.get("no_shop_card")
              and _shangquan_card_pattern(_site_card_urls(s)).search(content)}
    return {"sites": sites, "carded": carded}


@app.route("/curation/admin")
def curation_admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    return render_template("curation_admin.html", **_curation_admin_context())


@app.route("/curation/admin/unlist/<slug>", methods=["POST"])
def curation_admin_unlist(slug):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    ok, message = unlist_curated_site(slug)
    if ok:
        _fire_all_works_refresh(f"策展下架 {slug}")
    return render_template("curation_admin.html", **_curation_admin_context(), result_message=message, result_ok=ok)


@app.route("/curation/admin/relist/<slug>", methods=["POST"])
def curation_admin_relist(slug):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    ok, message = relist_curated_site(slug)
    if ok:
        _fire_all_works_refresh(f"策展重新上架 {slug}")
    return render_template("curation_admin.html", **_curation_admin_context(), result_message=message, result_ok=ok)


@app.route("/curation/admin/delete/<slug>", methods=["POST"])
def curation_admin_delete(slug):
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    if not _CURATED_SLUG_RE.match(slug):
        abort(404)
    ok, message = delete_curated_site(slug)
    if ok:
        _fire_all_works_refresh(f"策展刪除 {slug}")
    return render_template("curation_admin.html", **_curation_admin_context(), result_message=message, result_ok=ok)


def curation_upload_short_code() -> str:
    """策展上傳網址的短代碼（教練 2026-10-10 嫌帶 key 的網址太長）：用上傳金鑰算出來的固定 10 個字，換金鑰就跟著失效。"""
    import base64
    import hashlib
    import hmac
    digest = hmac.new(CURATION_UPLOAD_KEY.encode("utf-8"), b"curation-upload-short", hashlib.sha256).digest()
    return base64.b32encode(digest).decode("ascii").lower().rstrip("=")[:10]


@app.route("/u/<code>")
def curation_upload_short(code):
    """短網址：打開就是上傳頁（金鑰已內建在頁面裡，跟原本帶 ?key= 的效果一樣）。代碼不對一律 404。"""
    import hmac
    if not CURATION_UPLOAD_KEY or not hmac.compare_digest(code, curation_upload_short_code()):
        abort(404)
    return render_template("curation_upload.html", key=CURATION_UPLOAD_KEY,
                           sites=_load_curated_registry().get("sites", [])[::-1])


# ---- 未上架的人才軍火庫（教練 2026-11-02）：做好的人一律先進「未上架」，教練勾選才上架、也能勾選下架；比照上面的策展上架／下架後台 ----
import skyteam_pool as _stp


def _skyteam_admin_page(message=None, ok=None):
    _, experts, front = _stp.read_roster()
    return render_template("skyteam_admin.html", pool=_stp.load_pool()["pool"][::-1], experts=experts, front=front,
                           topics=_stp.TOPICS, result_message=message, result_ok=ok)


@app.route("/skyteam/admin")
def skyteam_admin():
    if not _logged_in():
        return redirect(url_for("admin_login", next=request.path))
    return _skyteam_admin_page()


@app.route("/skyteam/admin/<action>", methods=["POST"])
def skyteam_admin_action(action):
    if not _logged_in():
        return redirect(url_for("admin_login", next="/skyteam/admin"))
    if action == "publish":
        ok, message = _stp.publish(request.form.getlist("slug"), request.form.get("to", ""), request.form.get("topic") or None)
    elif action == "unpublish":
        ok, message = _stp.unpublish(request.form.getlist("name"))
    elif action == "dismiss":
        ok, message = _stp.dismiss(request.form.getlist("slug"))
    else:
        abort(404)
    return _skyteam_admin_page(message, ok)


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

    def _fail(msg: str, **ctx):
        # 2026-10-12 赫米斯用 curl 上傳只看到「HTTP 400」，原因藏在整頁 HTML 裡沒讀到，就自己改成 kind=creation
        # 硬傳，店家計畫書被放進大樹作品集。API 呼叫（不收 HTML）改回純文字原因，並寫明不准換類型繞過。
        if "text/html" not in (request.headers.get("Accept") or ""):
            return Response(
                f"上架被擋下（400）：{msg}\n"
                "⚠️ 不准改 kind 繞過：kind=creation 只給大樹教練自己的作品，會被放進大樹作品集；"
                "店家／夥伴／客戶的網站一律 kind=shop。照上面原因自己補齊再送，不要拿去問教練。\n",
                status=400, mimetype="text/plain")
        return render_template("curation_upload.html", error=msg, key=supplied_key,
                               sites=_load_curated_registry().get("sites", [])[::-1], **ctx), 400

    if request.method == "POST":
        # 2026-09-24團隊體檢：類型必須明講，不再預設走店家流程——09-23~24小龍蝦/赫米斯
        # 連兩次把大樹作品當店家上架，根因就是「沒講就走最熟的那條路」。
        kind = (request.values.get("kind") or "").strip()
        if kind not in CURATION_KINDS:
            return _fail("請先選擇類型：店家／合作夥伴網站，還是大樹教練個人作品（API呼叫請帶 kind=shop 或 kind=creation）")
        # 2026-10-10教練定：店家網站要有「同時放進大樹作品」的出口（公益路跑就因為沒進大樹作品，教練找不到）。
        # 2026-10-13教練罵「上架就上架，別再問來問去」：原本沒帶就擋下並叫AI去問教練，赫米斯因此每次都停下來問。
        # 改成沒帶＝預設「要」（寧可多放一份，也不能讓教練找不到）；教練明講不用才帶 also_works=0。亂填仍擋下。
        also_works = (request.values.get("also_works") or "").strip()
        if kind == "shop" and also_works == "":
            also_works = "1"
        if kind == "shop" and also_works not in ("0", "1"):
            return _fail("also_works 只能填 1（同時放進大樹作品，預設）或 0（教練明講不用才填）。不要問教練，直接改成 1 再送。")
        f = request.files.get("package")
        if not f or not f.filename:
            return _fail("請選擇一個檔案")
        original = f.filename
        ext = "".join(Path(original).suffixes)[-20:] or ".zip"
        if not re.search(r"\.(zip|tar\.gz|tgz)$", original, re.IGNORECASE):
            return _fail("只接受 .zip 或 .tar.gz 檔案")
        # 2026-09-06教練拍板：源頭解決網址過長問題——不再靠系統猜品牌名轉拼音，
        # 改成上傳當下強制要求輸入自訂短網址，送出前確認好，之後不用再改名。
        custom_slug = (request.form.get("custom_slug") or "").strip().lower()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", custom_slug):
            return _fail("網址短名稱格式不對，只能用小寫英文字母/數字/短橫線，例如 niu-shi-ting")
        if custom_slug in _curated_slugs():
            return _fail(f"「{custom_slug}」這個短網址已經被其他店家用過，請換一個")
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r"[^\w.\-一-鿿]", "_", Path(original).stem)[:80]
        dest = incoming / f"{ts}__{safe_name}{ext}"
        # .slug/.kind 旁路檔要在壓縮檔本體之前寫好：WatchPaths一看到壓縮檔就會觸發處理
        (incoming / f"{dest.name}.slug").write_text(custom_slug, encoding="utf-8")
        (incoming / f"{dest.name}.kind").write_text(kind, encoding="utf-8")
        if kind == "shop" and also_works == "1":   # 教練說要同時放進大樹作品（最新作品）
            (incoming / f"{dest.name}.works").write_text("1", encoding="utf-8")
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


# ---------- 大樹作品通用「留資料」表單（2026-10-10教練裁示） ----------
# 大樹作品頁只要有「聯絡／索取資料／送出」的介面，一律打這支，資料存 works_contact_leads，
# 同時通知「活動報名即時通知」群（TELEGRAM_REGISTRATION_GROUP_CHAT_ID）。不要為單一作品另開通知管道。
_WORKS_CONTACT_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多 10 次，防機器人


def _works_contact_rate_ok(ip: str, limit: int = 10) -> bool:
    import time
    now = time.time()
    hits = [t for t in _WORKS_CONTACT_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= limit:
        _WORKS_CONTACT_HITS[ip] = hits
        return False
    hits.append(now)
    _WORKS_CONTACT_HITS[ip] = hits
    return True


@app.route("/api/works/contact", methods=["POST"])
def api_works_contact():
    def reply(ok, error=None, status=200):
        body = {"ok": ok}
        if error:
            body["error"] = error
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json")

    payload = request.get_json(force=True, silent=True) or {}
    if (payload.get("website") or "").strip():          # 防機器人的隱藏欄位：假裝成功、不通知
        return reply(True)
    site = (payload.get("site") or "").strip()
    if not _CURATED_SLUG_RE.match(site) or site not in _curated_slugs():
        return reply(False, "找不到這個作品頁", 404)
    clean = lambda k, n: re.sub(r"\s+", " ", (payload.get(k) or "").strip())[:n]
    name, phone = clean("name", 30), clean("phone", 30)
    item, email, message = clean("item", 40), clean("email", 80), (payload.get("message") or "").strip()[:500]
    if not name:
        return reply(False, "請填寫姓名", 400)
    # 2026-10-13 榮樹下（rongtree）表單是「電話或 Email」擇一，只留 Email 也收
    if len(re.sub(r"\D", "", phone)) < 8 and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return reply(False, "請填寫正確的電話或 Email", 400)
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _works_contact_rate_ok(ip):
        return reply(False, "送出次數太多，請稍後再試", 429)
    title = next((s.get("title") for s in _load_curated_registry().get("sites", []) if s["slug"] == site), site) or site
    try:
        conn = db.get_conn()
        conn.execute("INSERT INTO works_contact_leads (site, site_title, name, phone, item, email, message, ip) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (site, title, name, phone, item, email, message, ip))
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001  資料庫寫入失敗也一定要通知，人工補登
        fail_text = f"⚠️【{title}・留資料寫入失敗】\n姓名：{name}\n電話：{phone}\n項目：{item or '未選'}\n錯誤：{e}\n請人工補登。"
        _notify_xiaolongxia(fail_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
        _notify_xiaolongxia(f"📩（同步給教練）{fail_text}", chat_id=TELEGRAM_NOTIFY_CHAT_ID)
        return reply(False, "系統忙碌，請稍後再試", 500)
    lead_text = (
        f"📩【{title}】有人留資料\n姓名：{name}\n電話：{phone or '（沒留，請看 Email）'}\n想了解：{item or '未選'}\n"
        + (f"Email：{email}\n" if email else "") + (f"留言：{message}\n" if message else "")
        + f"（來源：event.bymyway.com/curated/{site}/）")
    _notify_xiaolongxia(lead_text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    _notify_xiaolongxia(lead_text.replace("有人留資料", "有人留資料（同步給教練）", 1),
                        chat_id=TELEGRAM_NOTIFY_CHAT_ID)
    return reply(True)



# ---------- 點子樹（2026-10-30 教練：「我丟了一個點子，樹上還是四個，圖文不符」）----------
# idea-center 原本只畫範例點子＋這台瀏覽器自己存的，伺服器收到的點子不會回到樹上；上架時又被自動接成
# 留資料表單（要姓名電話），匿名的人送不出去、果實也不會長。改成：點子存 curated_ideas，所有人看到同一棵樹，
# 同時照舊寫進 works_contact_leads（各頁後台看得到）並通知「活動報名即時通知」群。
_IDEA_TREE_SITES = {"idea-center"}
_IDEA_CATS = {"run", "community", "share", "npo", "other"}


def _idea_row(r) -> dict:
    return {"id": r["id"], "text": r["text"], "cat": r["cat"], "ripe": r["ripe"], "path": r["path"],
            "who": r["who"], "t": r["created_at"]}


@app.route("/api/curated/<site>/ideas", methods=["GET", "POST"])
def api_curated_ideas(site):
    def reply(body, status=200):
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json",
                        headers={"Cache-Control": "no-store"})

    if site not in _IDEA_TREE_SITES or site not in _curated_slugs():
        return reply({"ok": False, "error": "找不到這個作品頁"}, 404)
    if request.method == "GET":
        conn = db.get_conn()
        rows = conn.execute("SELECT * FROM curated_ideas WHERE site=? AND hidden=0 ORDER BY id LIMIT 500",
                            (site,)).fetchall()
        conn.close()
        return reply({"ok": True, "ideas": [_idea_row(r) for r in rows]})

    payload = request.get_json(force=True, silent=True) or {}
    if (payload.get("website") or "").strip():          # 防機器人的隱藏欄位
        return reply({"ok": True, "idea": None})
    clean = lambda k, n: re.sub(r"\s+", " ", str(payload.get(k) or "").strip())[:n]
    text = clean("text", 500)
    if not text:
        return reply({"ok": False, "error": "先寫下一句話就好，不用完美。"}, 400)
    cat = clean("cat", 20)
    cat = cat if cat in _IDEA_CATS else "other"
    ripe = clean("ripe", 10) if clean("ripe", 10) in {"種子", "發芽", "長葉", "結果"} else "種子"
    path = clean("path", 2) if clean("path", 2) in {"A", "B", "C", "?"} else "?"
    name, org, email = clean("name", 30), clean("org", 40), clean("email", 80)
    anon = bool(payload.get("anon"))
    who = "匿名的好心人" if anon else ("・".join(filter(None, [name, org])) or "一位好心人")
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _works_contact_rate_ok(ip):
        return reply({"ok": False, "error": "送出次數太多，請稍後再試"}, 429)
    title = next((s.get("title") for s in _load_curated_registry().get("sites", []) if s["slug"] == site), site) or site
    conn = db.get_conn()
    cur = conn.execute("INSERT INTO curated_ideas (site, text, cat, ripe, path, who, email, ip) VALUES (?,?,?,?,?,?,?,?)",
                       (site, text, cat, ripe, path, who, email, ip))
    row = conn.execute("SELECT * FROM curated_ideas WHERE id=?", (cur.lastrowid,)).fetchone()
    msg = f"點子：{text}\n分類：{cat}｜熟度：{ripe}｜落地方式：{path}" + (f"\n單位：{org}" if org and not anon else "")
    try:
        conn.execute("INSERT INTO works_contact_leads (site, site_title, name, phone, item, email, message, ip) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (site, title, who, "", "點子", email, msg, ip))
    except Exception:  # noqa: BLE001  後台副本寫不進去不影響點子長在樹上
        pass
    conn.commit()
    conn.close()
    note = (f"🌱【{title}】有人種了一個點子\n署名：{who}\n" + (f"Email：{email}\n" if email else "")
            + msg + f"\n（來源：event.bymyway.com/curated/{site}/）")
    _notify_xiaolongxia(note, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    _notify_xiaolongxia(note.replace("有人種了一個點子", "有人種了一個點子（同步給教練）", 1), chat_id=TELEGRAM_NOTIFY_CHAT_ID)
    return reply({"ok": True, "idea": _idea_row(row)})

# ---------- 留資料後台（教練 2026-10-27：「寫好的資料在哪裡，我看不到，給我網址」）
# works_contact_leads 原本只有寫入、沒有任何一處讀取或後台頁 → 教練在網站上完全看不到自己收的資料。
# 短網址即通行證（沿用 rongtree_guest.py 的慣例），簽章用 app.secret_key，無簽章一律 404。
import works_leads as _wl


@app.route("/leads")
@app.route("/leads/a/<code>")
def works_leads_list(code=""):
    ok = (hmac.compare_digest(code, _wl.list_code(app.secret_key)) if code
          else hmac.compare_digest(request.args.get("k", ""), _wl.list_sig(app.secret_key)))
    if not ok:
        abort(404)
    return Response(_wl.render_list(app.secret_key, (request.args.get("site") or "").strip() or None),
                    content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


# ---------- 每個策展頁各有各的後台（2026-10-30 教練裁示） ----------
# 原本所有頁面留言混在同一個簽章池 → 教練要各頁獨立，讓每頁負責人只看得到自己頁面的客戶。
# 簽章綁 site：別頁的簽章打不開這頁；這頁也不會出現總覽簽章碼，拿到的人跳不出去。
@app.route("/leads/s/<site>/<code>")
def works_leads_site(site, code):
    if not _CURATED_SLUG_RE.match(site):
        abort(404)
    if not hmac.compare_digest(code, _wl.site_code(app.secret_key, site)):
        abort(404)
    return Response(_wl.render_site_only(app.secret_key, site),
                    content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


# ---------- 教練行程預約頁（2026-10-12）：只有拿到含隨機代碼的網址才進得來 ----------
# 資料＝workspace/knowledges/教練行程總表.json（scripts/coach_schedule.py）。預約會先寫成「待確認」占位，
# 並通知「活動報名即時通知」群；教練確認：coach_schedule.py confirm --id，不要：remove --id。
import coach_schedule_view as _csv

_SCHEDULE_BOOK_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多 6 次


@app.route("/schedule/<token>/")
def coach_schedule_page(token):
    if not _csv.token_ok(token):
        abort(404)
    return Response(_csv.render(token), content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


@app.route("/schedule/<token>/book", methods=["POST"])
def coach_schedule_book(token):
    def reply(ok, error=None, status=200, **extra):
        body = {"ok": ok, **extra}
        if error:
            body["error"] = error
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json",
                        headers={"Cache-Control": "no-store"})

    if not _csv.token_ok(token):
        abort(404)
    p = request.get_json(force=True, silent=True) or {}
    if (p.get("website") or "").strip():          # 防機器人隱藏欄位：假裝成功
        return reply(True, label="")
    import time
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _SCHEDULE_BOOK_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 6:
        return reply(False, "送出次數太多，請稍後再試", 429)
    hits.append(now)
    _SCHEDULE_BOOK_HITS[ip] = hits
    ok, res = _csv.book(p.get("date"), p.get("start"), p.get("type"))
    if not ok:
        return reply(False, res, 400)
    d = datetime.strptime(res["date"], "%Y-%m-%d")
    label = f"{d.month}/{d.day}（{'一二三四五六日'[d.weekday()]}）{res['start']}–{res['end']}"
    # 2026-10-13 教練：行程都在「佩佩老師的巴哈助理」群組處理（佩佩老師手寫筆記本數位化），預約通知改送那裡；送不出去才退回活動報名群
    text = (f"📅【{res['booking_type']}・待教練確認】\n時間：{label}\n預約人：{res['booked_by']}（預約頁點選）\n"
            f"（已先占位，其他人不能再約這個時段）\n確認：跟巴哈助理說「確認預約 {res['id']}」；取消：「取消預約 {res['id']}」")

    def _send_baha(t=text):
        import subprocess
        try:
            r = subprocess.run(["/Users/bymyway/.nvm/versions/node/v24.21.0/bin/node",  # 網站服務的 PATH 沒有 node，直接指定
                                "/Users/bymyway/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/openclaw.mjs", "message", "send", "--channel", "telegram",
                                "--account", "bot_peipei", "--target", "-5115910257", "-m", t],
                               capture_output=True, text=True, timeout=90)
            ok = r.returncode == 0
        except Exception:  # noqa: BLE001
            ok = False
        if not ok:
            _notify_xiaolongxia(t, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    threading.Thread(target=_send_baha, daemon=True).start()

    def _push_google():  # 預約一成功就寫進教練 Google 日曆；失敗沒關係，每 15 分鐘的同步會補
        import subprocess
        try:
            subprocess.run(["/usr/bin/python3", "-I", str(_csv.WS / "scripts" / "coach_schedule.py"), "push-google"],
                           capture_output=True, text=True, timeout=120)
        except Exception:  # noqa: BLE001
            pass
    threading.Thread(target=_push_google, daemon=True).start()
    return reply(True, label=label, type=res["booking_type"])


# ---------- 榮樹下網頁「我要預約」自動占位（教練 2026-10-23：要） ----------
_RONGTREE_HOLD_HITS = {}          # ip -> [時間戳]；每個 IP 每小時最多 4 次
_RONGTREE_HOLD_MAX_OPEN = 6       # 官網預約「還沒填來賓資料表」的同時最多 6 筆（2026-10-30 起不再有待確認，改看資料表）；超過就不再自動排入（防有人亂點占光空檔），前端改走一般留資料


def _rongtree_hold_notify(text):
    """通知進「佩佩老師的巴哈助理」群（跟預約頁同一條路）；送不出去退回活動報名群。"""
    import subprocess
    try:
        r = subprocess.run(["/Users/bymyway/.nvm/versions/node/v24.21.0/bin/node",  # 網站服務的 PATH 沒有 node，直接指定
                            "/Users/bymyway/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/openclaw.mjs", "message", "send", "--channel", "telegram",
                            "--account", "bot_peipei", "--target", "-5115910257", "-m", text],
                           capture_output=True, text=True, timeout=90)
        ok = r.returncode == 0
    except Exception:  # noqa: BLE001
        ok = False
    if not ok:
        _notify_xiaolongxia(text, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)


def _rongtree_hold_record_lead(name, contact, org, msg, label, ip):
    """留資料紀錄（跟 /api/works/contact 同一張表）；寫入失敗不影響占位。"""
    title = next((s.get("title") for s in _load_curated_registry().get("sites", []) if s["slug"] == "rongtree"), "榮樹下") or "榮樹下"
    is_mail = "@" in contact
    try:
        conn = db.get_conn()
        conn.execute("INSERT INTO works_contact_leads (site, site_title, name, phone, item, email, message, ip) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     ("rongtree", title, name, "" if is_mail else contact, "節目專訪", contact if is_mail else "",
                      f"企業／單位：{org}\n想預約的時間：{label}" + (f"\n想說的話：{msg}" if msg else ""), ip))
        conn.commit()
        conn.close()
    except Exception:  # noqa: BLE001
        pass


def _rongtree_hold_confirm(bid):
    """官網預約一成功就自動確認：改行程、排開始前 1 小時提醒、寫進教練 Google 日曆（跟對巴哈說「確認預約」同一支 confirm）。
    失敗沒關係：來賓卡後台有「確認這個時段」鈕，Google 也有每 15 分鐘的同步會補。"""
    import subprocess
    try:
        subprocess.run(["/usr/bin/python3", "-I", str(_csv.WS / "scripts" / "coach_schedule.py"), "confirm", "--id", bid],
                       capture_output=True, text=True, timeout=120)
    except Exception:  # noqa: BLE001
        pass


@app.route("/api/rongtree/hold", methods=["POST"])
def api_rongtree_hold():
    """榮樹下網頁「我要預約」：節目專訪選好那一小時、送出 → 那一小時直接排進行程（背景自動確認；2026-10-30 教練：對方自選的時間不用再確認），空檔清單就不再出現它。
    要取消：「取消預約 <id>」（取消後空檔自動恢復）。
    姓名寫進 guest，前置作業與來賓卡後台看得到是誰預約（2026-10-30 教練）；單位、聯絡方式只放私人備註與巴哈群通知。
    回應附來賓資料表網址，成功畫面直接帶預約人去填。
    搶不到（剛被約走／離前後訪談太近）回 409 code=taken；官網待確認已達上限回 409 code=full，前端改走一般留資料。"""
    def reply(ok, error=None, status=200, **extra):
        body = {"ok": ok, **extra}
        if error:
            body["error"] = error
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json",
                        headers={"Cache-Control": "no-store"})

    p = request.get_json(force=True, silent=True) or {}
    if (p.get("website") or "").strip():          # 防機器人隱藏欄位：假裝成功、不占位、不通知
        return reply(True, held=False)
    clean = lambda k, n: re.sub(r"\s+", " ", (p.get(k) or "").strip())[:n]
    name, org, contact, msg = clean("name", 30), clean("org", 40), clean("contact", 80), (p.get("msg") or "").strip()[:300]
    if not name or not org:
        return reply(False, "請填寫姓名與單位", 400)
    if len(re.sub(r"\D", "", contact)) < 8 and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", contact):
        return reply(False, "請填寫正確的電話或 Email", 400)
    import time
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _RONGTREE_HOLD_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 4:
        return reply(False, "送出次數太多，請稍後再試", 429)
    hits.append(now)
    _RONGTREE_HOLD_HITS[ip] = hits
    try:
        evs = json.loads(_csv.DATA.read_text(encoding="utf-8")).get("events", [])
    except Exception:  # noqa: BLE001
        evs = []
    today_s = datetime.now(_csv.TZ).date().isoformat()
    forms = _rg.all_forms()
    filled = lambda e: bool(e.get("form_token")) and any(_rg._slot_has(r["token"], e["form_token"]) for r in forms)
    if sum(1 for e in evs if e.get("booked_by") == "官網預約" and e.get("date", "") >= today_s and not filled(e)) >= _RONGTREE_HOLD_MAX_OPEN:
        return reply(False, "目前待確認的預約已滿", 409, code="full")
    ok, res = _csv.book(p.get("date"), p.get("start"), "榮樹下訪談", who="官網預約", guest=name,
                        guest_data={"name": name, "org": org, "contact": contact, "msg": msg},
                        note=f"官網預約：{name}（{org}）｜聯絡：{contact}" + (f"｜留言：{msg}" if msg else "") + "（單位與聯絡方式為私人資料，網頁不公開）")
    if not ok:
        return reply(False, res, 409, code="taken")
    d = datetime.strptime(res["date"], "%Y-%m-%d")
    label = f"{d.month}/{d.day}（{'一二三四五六日'[d.weekday()]}）{res['start']}–{res['end']}"
    form = f"/rongtree/guest/{res['form_token']}" if res.get("form_token") else ""
    text = (f"📅【榮樹下訪談・官網預約】\n時間：{label}\n預約人：{name}（{org}）\n聯絡：{contact}\n"
            + (f"留言：{msg}\n" if msg else "")
            + (f"來賓資料表（預約人送出後已在畫面上看到這個按鈕）：https://event.bymyway.com{form}\n" if form else "")
            + f"（時段已直接排入教練行程，其他人不能再約；對方還沒填來賓資料表的話，榮樹下前置作業會標示）\n要取消：跟巴哈助理說「取消預約 {res['id']}」（取消後空檔自動恢復）")
    _rongtree_hold_record_lead(name, contact, org, msg, label, ip)
    threading.Thread(target=_rongtree_hold_notify, args=(text,), daemon=True).start()
    threading.Thread(target=_rongtree_hold_confirm, args=(res["id"],), daemon=True).start()
    return reply(True, held=True, label=label, form=form)


@app.route("/schedule/<token>/cancel", methods=["POST"])
def coach_schedule_cancel(token):
    """預約頁的「取消」鈕（教練 2026-10-13）：拿到網址的人可取消總表自己的行程（預約頁／巴哈／榮樹下訪談／每週固定的單一天）；
    Google 日曆或官方來源的不給取消。取消後通知巴哈群組，讓大家看得到誰的行程被取消了。"""
    def reply(ok, error=None, status=200, **extra):
        body = {"ok": ok, **extra}
        if error:
            body["error"] = error
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json",
                        headers={"Cache-Control": "no-store"})

    if not _csv.token_ok(token):
        abort(404)
    import time
    p = request.get_json(force=True, silent=True) or {}
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _SCHEDULE_BOOK_HITS.get("cx:" + ip, []) if now - t < 3600]
    if len(hits) >= 20:
        return reply(False, "操作太頻繁，請稍後再試", 429)
    hits.append(now)
    _SCHEDULE_BOOK_HITS["cx:" + ip] = hits
    ok, res = _csv.cancel(str(p.get("id") or ""), str(p.get("date") or ""))
    if not ok:
        return reply(False, res, 400)

    def _send_baha(t=f"🗑【行程已取消】{res}\n（預約頁按「取消」；教練 Google 日曆若有同一筆，已一起刪除）"):
        import subprocess
        try:
            r = subprocess.run(["/Users/bymyway/.nvm/versions/node/v24.21.0/bin/node",
                                "/Users/bymyway/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/openclaw.mjs", "message", "send", "--channel", "telegram",
                                "--account", "bot_peipei", "--target", "-5115910257", "-m", t],
                               capture_output=True, text=True, timeout=90)
            ok2 = r.returncode == 0
        except Exception:  # noqa: BLE001
            ok2 = False
        if not ok2:
            _notify_xiaolongxia(t, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    threading.Thread(target=_send_baha, daemon=True).start()
    return reply(True, label=res)


# ---------- 大樹作品通用「票選＋收集建議」（2026-10-10：南應大記憶牆講座主題票選） ----------
# 票數所有人共用；選項只認這份名單（網站代號 → 選項代號），不在名單裡的一律擋下。
WORKS_POLL_OPTIONS = {"tut-memory": {"t1", "t2", "t3", "t4"}}
_WORKS_POLL_HITS = {}   # (用途, ip) -> [時間戳]


def _works_poll_rate_ok(kind: str, ip: str, limit: int) -> bool:
    import time
    now = time.time()
    hits = [t for t in _WORKS_POLL_HITS.get((kind, ip), []) if now - t < 3600]
    ok = len(hits) < limit
    if ok:
        hits.append(now)
    _WORKS_POLL_HITS[(kind, ip)] = hits
    return ok


def _works_poll_json(obj, status=200):
    return Response(json.dumps(obj, ensure_ascii=False), status=status, content_type="application/json",
                    headers={"Cache-Control": "no-store"})


def _works_poll_counts(site: str) -> dict:
    conn = db.get_conn()
    rows = conn.execute("SELECT option_id, COUNT(*) AS n FROM works_poll_votes WHERE site=? GROUP BY option_id", (site,)).fetchall()
    conn.close()
    counts = {o: 0 for o in WORKS_POLL_OPTIONS[site]}
    counts.update({r["option_id"]: r["n"] for r in rows if r["option_id"] in counts})
    return counts


# ---- 榮樹下節目單：SoundOn 上架新集數，網頁開啟時自己讀 RSS 補上（教練 2026-10-13，不用手動補）----
ROUNG_FEED = "https://feeds.soundon.fm/podcasts/01bac58b-741f-4cbc-8fa6-58dd45f24923.xml"
_rong_cache = {"at": 0.0, "items": []}


def _rong_parse_feed(xml_text: str) -> list:
    import xml.etree.ElementTree as ET
    ns = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
    out = []
    for it in ET.fromstring(xml_text).iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        guid = (it.findtext("guid") or "").strip()
        if not title or not guid:
            continue
        ver = "live" if "實況" in title else "highlight"
        guest = re.sub(r"^【[^】]*】\s*", "", title)
        mno = re.match(r"^第\s*(\d+)\s*集\s*[:：]\s*", guest)
        no = int(mno.group(1)) if mno else 0   # Podcast 標題上的真集數（2026-10-28 教練：頁面不要自己照發布順序編號）
        guest = re.sub(r"^第\s*\d+\s*集\s*[:：]\s*", "", guest)
        guest = re.sub(r"\s*[\(（][^\)）]*版[\)）]\s*$", "", guest).strip()
        desc = re.sub(r"\s+", " ", (it.findtext("description") or "")).strip()
        try:
            sec = int(it.findtext("itunes:duration", default="0", namespaces=ns))
        except ValueError:
            sec = 0
        dur = f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"
        try:
            from email.utils import parsedate_to_datetime
            day = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone(timedelta(hours=8))).strftime("%Y.%m.%d")
        except Exception:
            day = ""
        out.append({"id": guid, "url": link, "title": guest, "version": ver, "desc": desc[:140], "dur": dur, "date": day, "no": no})
    return out[::-1]  # 舊→新


# 每集彈窗的「認識來賓」專屬網頁（教練 2026-10-28）：照節目標題裡的名字，自動對到策展名冊裡已上架的個人頁；
# 網頁標題不是以本人名字開頭的（暱稱、專題頁），寫在 _RONG_ALIAS。新集數只要來賓有上架網頁就會自己出現。
_RONG_ALIAS = {"周總": ["zhou-ruiqi"], "天使姐姐": ["angel-sister"], "陳智博": ["big-plan"],
               "黃國彰": ["inventor"], "楊境界": ["hnv-cc"]}
_RONG_PAGE_SKIP = {"skyteam", "all-works", "rongtree", "coach888", "coachwu"}


def _rong_guest_pages(title: str, sites: list) -> list:
    hits = []
    for kw, slugs in _RONG_ALIAS.items():
        if kw in title:
            hits += slugs
    for s in sites:
        if s["slug"] in _RONG_PAGE_SKIP:
            continue
        nm = re.split(r"[｜|]", s["title"])[0].strip().split(" ")[0]
        nm = re.sub(r"(博士|董事長|總經理|老師|牧師)$", "", nm)
        if re.fullmatch(r"[\u4e00-\u9fff]{2,4}", nm) and nm in title:
            hits.append(s["slug"])
    by = {s["slug"]: s for s in sites}
    out, seen = [], set()
    for slug in hits:
        s = by.get(slug)
        if not s or slug in seen:
            continue
        seen.add(slug)
        parts = re.split(r"[｜|]", s["title"], 1)
        label = parts[0].strip() + (" ‧ " + parts[1].strip()[:24] if len(parts) > 1 else "")
        out.append([label, s["event_url"]])
    return out[:4]


@app.route("/api/rongtree/episodes", methods=["GET"])
def api_rongtree_episodes():
    """同源給 /curated/rongtree/ 的 JS 用；5 分鐘快取，SoundOn 暫時連不上就給上一份（網頁還是有靜態名單當底）"""
    now = time.time()
    if now - _rong_cache["at"] > 300:
        try:
            req = urllib.request.Request(ROUNG_FEED, headers={"User-Agent": "rongtree-site/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                items = _rong_parse_feed(r.read().decode("utf-8", "replace"))
            if items:
                _rong_cache.update(at=now, items=items)
        except Exception as exc:
            print(f"[rongtree-episodes] 讀 SoundOn 失敗，沿用上一份：{exc}", flush=True)
            _rong_cache["at"] = now - 240  # 1 分鐘後再試，不要每個訪客都重打
    try:
        _sites = [x for x in json.loads(CURATED_REGISTRY_PATH.read_text(encoding="utf-8"))["sites"] if x.get("status") == "live"]
    except Exception:
        _sites = []
    _eps = [dict(e, pages=_rong_guest_pages(e["title"], _sites)) for e in _rong_cache["items"]]
    resp = Response(json.dumps({"ok": True, "episodes": _eps}, ensure_ascii=False), mimetype="application/json")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Cache-Control"] = "public, max-age=120"
    return resp


# ---- 榮樹下來賓資料表＋AI 來賓卡（教練 2026-10-14）：說明見 rongtree_guest.py ----
import rongtree_guest as _rg

_RG_HITS = {}   # ip -> [時間戳]；每個 IP 每小時最多送出 10 次


def _rg_json(obj, status=200):
    return Response(json.dumps(obj, ensure_ascii=False), status=status, content_type="application/json",
                    headers={"Cache-Control": "no-store"})


def _rg_card_ok(token):
    return hmac.compare_digest(request.args.get("k", ""), _rg.card_sig(app.secret_key, token))


@app.route("/rongtree/guest/<token>", methods=["GET", "POST"])
def rongtree_guest_form(token):
    ev = _rg.find_event(token)
    if not ev:
        abort(404)
    token = ev["form_token"]          # 一律用「場次代碼」；同一場可有好幾位來賓，各存一筆
    cookie_name = f"rg_{token}"
    mine = request.cookies.get(cookie_name, "")
    if request.method == "GET":
        mine_row = _rg.get_form(mine) if _rg.TOKEN_RE.match(mine) and _rg._slot_has(mine, token) else None
        return Response(_rg.render_form(token, ev, mine_row, _rg.count_in_slot(token)), content_type="text/html; charset=utf-8",
                        headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _RG_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 10:
        return _rg_json({"ok": False, "error": "送出次數太多，請稍後再試"}, 429)
    _RG_HITS[ip] = hits + [now]
    ok, err, first, key = _rg.save(token, ev, request.get_json(force=True, silent=True) or {}, ip, mine)
    if not ok:
        return _rg_json({"ok": False, "error": err}, 400)
    _rg.start_card(key, app.secret_key,
                   lambda t: _notify_xiaolongxia(t, chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID), first,
                   coach_notify=_notify_xiaolongxia)   # 預設＝教練私人電報（10/14 教練要求）
    resp = _rg_json({"ok": True})
    # 這個瀏覽器記得自己填的是哪一筆：再打開網址是修改自己的；按「新增另一位來賓」才清掉
    resp.set_cookie(cookie_name, key, max_age=30 * 86400, path="/rongtree/guest/", samesite="Lax")
    return resp


@app.route("/rongtree/guest/<token>/card")
def rongtree_guest_card(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not _rg_card_ok(token):
        abort(404)
    return Response(_rg.render_card(token, r, app.secret_key), content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


@app.route("/rongtree/guest/<token>/card/regen", methods=["POST"])
def rongtree_guest_card_regen(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not _rg_card_ok(token):
        abort(404)
    if r["card_status"] != "pending":
        conn = _rg._conn()
        conn.execute("UPDATE rongtree_guest_forms SET card_status='pending' WHERE token=?", (token,))
        conn.commit()
        conn.close()
        threading.Thread(target=_rg.build_card, args=(token,), daemon=True).start()
    return redirect(f"/rongtree/guest/{token}/card?k={request.args.get('k', '')}")


@app.route("/rongtree/guest/<token>/card/delete", methods=["POST"])
def rongtree_guest_card_delete(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not _rg_card_ok(token):
        abort(404)
    _rg.delete_form(token)
    return redirect(f"/rongtree/a/{_rg.list_code(app.secret_key)}")


@app.route("/rongtree/guest/<token>/card/restore", methods=["POST"])
def rongtree_guest_card_restore(token):
    r = _rg.get_form(token, include_deleted=True) if _rg.TOKEN_RE.match(token) else None
    if not r or not _rg_card_ok(token):
        abort(404)
    _rg.restore_form(token)
    return redirect(f"/rongtree/a/{_rg.list_code(app.secret_key)}")


@app.route("/rongtree/guest/<token>/photo.jpg")
def rongtree_guest_photo(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not r["photo_file"] or not _rg_card_ok(token):
        return Response("", status=404, headers={"Cache-Control": "no-store"})
    resp = send_from_directory(_rg.UPLOAD_DIR, r["photo_file"], mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/rongtree/guest/<token>/card/public", methods=["POST"])
def rongtree_guest_card_public(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not _rg_card_ok(token):
        abort(404)
    _rg.set_public(token, request.form.get("public") == "1")
    return redirect(f"/rongtree/guest/{token}/card?k={request.args.get('k', '')}")


@app.route("/api/rongtree/prep")
def api_rongtree_prep():
    """榮樹下網頁「訪談嘉賓前置作業」區：接下來的訪談（含資料表網址）＋已交資料的來賓（只給公開欄位）"""
    resp = _rg_json(_rg.public_prep())
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


# ---------- 主持人專區（2026-11-02 教練：在榮樹下頁面直接點「我是主持人」，輸入手機＋密碼就看得到來賓填的資料，不用另外記網址）----------
_RG_HOST_PHONES = {"0901056777": "吳大樹"}   # 主持人手機白名單；要加人（邱裕榮等）就加在這裡
_RG_HOST_PASSWORD = "88888"                    # 教練指定，跟大樹各後台同一組
_RG_HOST_HITS = {}                             # ip -> [時間戳]；每個 IP 10 分鐘最多試 8 次


def _rg_is_host():
    return bool(session.get("rongtree_host"))


@app.route("/api/rongtree/host/login", methods=["POST"])
def api_rongtree_host_login():
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _RG_HOST_HITS.get(ip, []) if now - t < 600]
    if len(hits) >= 8:
        return _rg_json({"ok": False, "error": "試太多次了，請 10 分鐘後再試"}, 429)
    _RG_HOST_HITS[ip] = hits + [now]
    p = request.get_json(force=True, silent=True) or {}
    phone = re.sub(r"\D", "", str(p.get("phone") or ""))
    pw = str(p.get("password") or "")
    ok_phone = any(hmac.compare_digest(phone, h) for h in _RG_HOST_PHONES)
    ok_pw = hmac.compare_digest(pw.encode(), _RG_HOST_PASSWORD.encode())
    if not (ok_phone and ok_pw):
        return _rg_json({"ok": False, "error": "手機號碼或密碼不對"}, 401)
    session["rongtree_host"] = True
    session.permanent = True
    return _rg_json({"ok": True, "name": _RG_HOST_PHONES.get(phone, "")})


@app.route("/api/rongtree/host/logout", methods=["POST"])
def api_rongtree_host_logout():
    session.pop("rongtree_host", None)
    return _rg_json({"ok": True})


@app.route("/api/rongtree/host/cards")
def api_rongtree_host_cards():
    """主持人登入後：每一場訪談對應的來賓卡網址（帶簽章），加上全部來賓卡總覽網址"""
    if not _rg_is_host():
        return _rg_json({"ok": False, "error": "請先登入主持人專區"}, 401)
    by_slot = {}
    for e in _rg._upcoming():
        tok = e.get("form_token")
        if not tok:
            continue
        by_slot[tok] = [{"guest": r["guest"] or "", "status": r["card_status"],
                         "url": f"/rongtree/guest/{r['token']}/card?k={_rg.card_sig(app.secret_key, r['token'])}"}
                        for r in _rg.all_forms() if _rg._slot_has(r["token"], tok)]
    return _rg_json({"ok": True, "list_url": f"/rongtree/a/{_rg.list_code(app.secret_key)}", "by_slot": by_slot})


@app.route("/rongtree/face/<token>.jpg")
def rongtree_guest_face(token):
    r = _rg.get_form(token) if _rg.TOKEN_RE.match(token) else None
    if not r or not r["photo_file"] or not r["public"]:
        return Response("", status=404, headers={"Cache-Control": "no-store"})
    resp = send_from_directory(_rg.UPLOAD_DIR, r["photo_file"], mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "no-store"   # 來賓換照片或被隱藏要立刻生效
    return resp


@app.route("/rongtree/a/<code>/confirm/<bid>", methods=["POST"])
def rongtree_confirm_booking(code, bid):
    """來賓卡後台「確認這個時段」鈕（2026-10-30 教練）：等於對巴哈說「確認預約 <id>」，走同一支 coach_schedule.py confirm（改行程、排提醒、寫 Google 日曆）。"""
    if not hmac.compare_digest(code, _rg.list_code(app.secret_key)) or not re.fullmatch(r"[0-9a-f]{8}", bid):
        abort(404)
    import subprocess
    subprocess.run(["/usr/bin/python3", "-I", str(_csv.WS / "scripts" / "coach_schedule.py"), "confirm", "--id", bid],
                   capture_output=True, text=True, timeout=120)
    return redirect(f"/rongtree/a/{code}")


@app.route("/rongtree/cards")
@app.route("/rongtree/a/<code>")
def rongtree_guest_cards(code=""):
    ok = (hmac.compare_digest(code, _rg.list_code(app.secret_key)) if code
          else hmac.compare_digest(request.args.get("k", ""), _rg.list_sig(app.secret_key)))
    if not ok:
        abort(404)
    return Response(_rg.render_list(app.secret_key), content_type="text/html; charset=utf-8",
                    headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})


import rongtree_tracker as _rtk  # noqa: E402
_RONGTREE_TRACKER_HITS = {}   # ip -> [時間戳]


@app.route("/api/rongtree/tracker/<code>", methods=["GET", "POST"])
def api_rongtree_tracker(code):
    """榮樹下 SOP 網頁「進度追蹤表」（2026-10-29 教練：不用另開 Google 試算表，網頁直接勾選、存資料庫）。
    代碼同來賓卡後台 /rongtree/a/<代碼>；GET 讀全部，POST {id, field, value} 改一格。"""
    if not hmac.compare_digest(code, _rg.list_code(app.secret_key)):
        abort(404)

    def reply(body, status=200):
        return Response(json.dumps(body, ensure_ascii=False), status=status, content_type="application/json",
                        headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"})

    if request.method == "GET":
        return reply({"ok": True, "rows": _rtk.rows(),
                      "fields": {k: ("check" if v is True else v) for k, v in _rtk.FIELDS.items()}})
    import time
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    hits = [t for t in _RONGTREE_TRACKER_HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 300:
        return reply({"ok": False, "error": "操作太頻繁，請稍後再試"}, 429)
    hits.append(now)
    _RONGTREE_TRACKER_HITS[ip] = hits
    p = request.get_json(force=True, silent=True) or {}
    ok, err = _rtk.set_field(str(p.get("id") or ""), str(p.get("field") or ""), p.get("value"))
    return reply({"ok": True} if ok else {"ok": False, "error": err}, 200 if ok else 400)


@app.route("/api/works/poll/<site>", methods=["GET"])
def api_works_poll_counts(site):
    if site not in WORKS_POLL_OPTIONS:
        return _works_poll_json({"ok": False, "error": "找不到這個票選"}, 404)
    return _works_poll_json({"ok": True, "counts": _works_poll_counts(site)})


@app.route("/api/works/poll/<site>/vote", methods=["POST"])
def api_works_poll_vote(site):
    if site not in WORKS_POLL_OPTIONS:
        return _works_poll_json({"ok": False, "error": "找不到這個票選"}, 404)
    payload = request.get_json(force=True, silent=True) or {}
    option = str(payload.get("option") or "")
    voter = str(payload.get("voter") or "")
    if option not in WORKS_POLL_OPTIONS[site] or not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", voter):
        return _works_poll_json({"ok": False, "error": "票選資料不正確"}, 400)
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _works_poll_rate_ok("vote", ip, 30):
        return _works_poll_json({"ok": False, "error": "投票次數太多，請稍後再試"}, 429)
    conn = db.get_conn()
    conn.execute("INSERT OR IGNORE INTO works_poll_votes (site, option_id, voter, ip) VALUES (?, ?, ?, ?)", (site, option, voter, ip))
    conn.commit()
    conn.close()
    return _works_poll_json({"ok": True, "counts": _works_poll_counts(site)})


@app.route("/api/works/poll/<site>/suggest", methods=["POST"])
def api_works_poll_suggest(site):
    if site not in WORKS_POLL_OPTIONS:
        return _works_poll_json({"ok": False, "error": "找不到這個票選"}, 404)
    payload = request.get_json(force=True, silent=True) or {}
    if (payload.get("website") or "").strip():          # 防機器人隱藏欄位：假裝成功、不通知
        return _works_poll_json({"ok": True})
    clean = lambda k, n: re.sub(r"\s+", " ", (payload.get(k) or "").strip())[:n]
    name, text = clean("name", 30), clean("suggestion", 200)
    if len(text) < 2:
        return _works_poll_json({"ok": False, "error": "請寫下您想聽的主題"}, 400)
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    if not _works_poll_rate_ok("suggest", ip, 5):
        return _works_poll_json({"ok": False, "error": "送出次數太多，請稍後再試"}, 429)
    title = next((s.get("title") for s in _load_curated_registry().get("sites", []) if s["slug"] == site), site) or site
    try:
        conn = db.get_conn()
        conn.execute("INSERT INTO works_poll_suggestions (site, name, suggestion, ip) VALUES (?, ?, ?, ?)", (site, name, text, ip))
        conn.commit()
        conn.close()
    except Exception as e:  # noqa: BLE001
        _notify_xiaolongxia(f"⚠️【{title}・講座建議寫入失敗】\n建議：{text}\n暱稱：{name or '未填'}\n錯誤：{e}\n請人工補登。",
                            chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
        return _works_poll_json({"ok": False, "error": "系統忙碌，請稍後再試"}, 500)
    _notify_xiaolongxia(f"💡【{title}】有人建議想聽的講座\n建議：{text}\n暱稱：{name or '未填'}\n（來源：event.bymyway.com/curated/{site}/）",
                        chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)
    return _works_poll_json({"ok": True})


# ---------- 大樹作品通用「按讚計數」（2026-10-10：南應大記憶牆「支持陳佩君」） ----------
# 教練裁示：不記 IP、不限次數，按一下加一，營造支持的氛圍。只存總數；計數器要先登記在這裡。
WORKS_COUNTERS = {"tut-memory": {"support-peijun"}}


def _works_counter_value(site: str, key: str) -> int:
    conn = db.get_conn()
    row = conn.execute("SELECT n FROM works_counters WHERE site=? AND counter_key=?", (site, key)).fetchone()
    conn.close()
    return row["n"] if row else 0


@app.route("/api/works/counter/<site>/<key>", methods=["GET", "POST"])
def api_works_counter(site, key):
    if key not in WORKS_COUNTERS.get(site, set()):
        return _works_poll_json({"ok": False, "error": "找不到這個計數"}, 404)
    if request.method == "POST":
        conn = db.get_conn()
        conn.execute("INSERT INTO works_counters (site, counter_key, n) VALUES (?, ?, 1) "
                     "ON CONFLICT(site, counter_key) DO UPDATE SET n = n + 1", (site, key))
        conn.commit()
        conn.close()
    return _works_poll_json({"ok": True, "n": _works_counter_value(site, key)})


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


def _coach888_keep_new_works(conn, payload):
    """2026-10-10：開著舊版 coach888 頁面的瀏覽器一存排版，會把整份 layout 蓋回舊的，剛自動登記的新作品就不見了
    （art-lab 04:59 登記、05:01 被蓋掉；big-plan 同樣）。保護：近 72 小時上架的「大樹作品」(no_shop_card，
    或店家上架時教練要求同時放進大樹作品的 in_works)，
    如果新的 layout 在所有分類（含「最近刪除」）都找不到它，就把它補回「最新作品」最前面。
    教練真的刪除作品會落在「最近刪除」，所以不會被擋；超過 72 小時的不管。"""
    raw = payload.get("coach888_layout")
    if raw is None:
        return
    layout = json.loads(raw) if isinstance(raw, str) else raw
    if not isinstance(layout, dict):
        return
    present = {u for urls in layout.values() if isinstance(urls, list) for u in urls}
    cutoff = datetime.now() - timedelta(hours=72)
    missing = []
    for site in _load_curated_registry().get("sites", []):
        if not (site.get("no_shop_card") or site.get("in_works")) or site.get("event_url") in present:
            continue
        try:
            if datetime.strptime(site["uploaded_at"], "%Y-%m-%d %H:%M") < cutoff:
                continue
        except (KeyError, ValueError):
            continue
        missing.append(site)
    if not missing:
        return
    row = conn.execute("SELECT value FROM coach888_state WHERE key = 'coach888_items'").fetchone()
    server_items = json.loads(row["value"]) if row and row["value"] else {}
    new_items = payload.get("coach888_items")
    new_items = json.loads(new_items) if isinstance(new_items, str) else (new_items if isinstance(new_items, dict) else None)
    for site in sorted(missing, key=lambda x: x["uploaded_at"]):   # 舊的先補，新的排最前
        url = site["event_url"]
        layout.setdefault("zuixinzuopin", []).insert(0, url)
        if new_items is not None and url not in new_items:
            new_items[url] = server_items.get(url) or {"name": site["title"], "badge": "公開"}
        app.logger.warning("coach888 保護：補回被舊頁面蓋掉的新作品 %s", url)
    payload["coach888_layout"] = json.dumps(layout, ensure_ascii=False)
    if new_items is not None:
        payload["coach888_items"] = json.dumps(new_items, ensure_ascii=False)


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
    try:
        _coach888_keep_new_works(conn, payload)
    except Exception as e:  # noqa: BLE001  保護失敗不能擋住教練存排版
        app.logger.warning("coach888 新作品保護失敗: %r", e)
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


MYTOOLS_ORIGINS = {"https://coach1973.github.io", "http://localhost:8765", "http://127.0.0.1:8765"}
MYTOOLS_KEY = "mytools_data"


def _mytools_clean(data):
    """「大樹的常用查詢網站」排版存檔的格式檢查：只收 sections(分類)/items(項目)/removed(已刪除網址)/
    trash(最近刪除，可復原；2026-10-20 補，比照大樹作品一覽)/trashCollapsed(最近刪除收合，2026-10-21 補)，其他欄位丟掉、字串截長度，網址只收 http(s)。不合格式回 None。"""
    if not isinstance(data, dict) or not isinstance(data.get("sections"), list):
        return None
    if not 1 <= len(data["sections"]) <= 40:
        return None

    def txt(v, n):
        return v.strip()[:n] if isinstance(v, str) else ""

    sections = []
    for sec in data["sections"]:
        if not isinstance(sec, dict) or not isinstance(sec.get("items"), list) or len(sec["items"]) > 300:
            return None
        items = []
        for it in sec["items"]:
            if not isinstance(it, dict):
                return None
            url = txt(it.get("url"), 1000)
            if not re.match(r"^https?://", url):
                return None
            items.append({"name": txt(it.get("name"), 120) or url, "url": url,
                          "desc": txt(it.get("desc"), 300), "tag": txt(it.get("tag"), 20)})
        sections.append({"id": txt(sec.get("id"), 40) or "s" + secrets.token_hex(4),
                         "icon": txt(sec.get("icon"), 8), "title": txt(sec.get("title"), 60) or "未命名",
                         "collapsed": bool(sec.get("collapsed")), "items": items})
    removed = [u for u in data.get("removed", []) if isinstance(u, str)][:500] if isinstance(data.get("removed", []), list) else []
    trash = []
    for it in data.get("trash", []) if isinstance(data.get("trash", []), list) else []:
        url = txt(it.get("url"), 1000) if isinstance(it, dict) else ""
        if re.match(r"^https?://", url) and len(trash) < 500:
            trash.append({"name": txt(it.get("name"), 120) or url, "url": url, "desc": txt(it.get("desc"), 300),
                          "tag": txt(it.get("tag"), 20), "from": txt(it.get("from"), 40) or None})
    return {"sections": sections, "removed": removed, "trash": trash, "trashCollapsed": bool(data.get("trashCollapsed"))}


@app.route("/api/mytools/state", methods=["GET", "POST", "OPTIONS"])
def api_mytools_state():
    """大樹的常用查詢網站(coach1973.github.io/my-tools)的排版狀態(2026-10-15教練交辦：像作品一覽一樣自己排分組、搬項目)。
    GET：回傳 {data, updated_at}（沒存過 data 是 null，頁面用內建預設）。
    POST：body {data:{sections,removed}}，只收來自 coach1973.github.io 的瀏覽器(Origin 檢查)，格式不合回 400。
    每次存檔都留一份歷史(最近 60 份)，被亂改可以還原：mytools_history 表。"""
    origin = request.headers.get("Origin", "")
    headers = {"Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type",
               "Content-Type": "application/json"}
    if origin in MYTOOLS_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
    if request.method == "OPTIONS":
        return Response(status=204, headers=headers)
    conn = db.get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS mytools_history (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT, saved_at TEXT)")
    if request.method == "GET":
        row = conn.execute("SELECT value, updated_at FROM coach888_state WHERE key = ?", (MYTOOLS_KEY,)).fetchone()
        conn.close()
        body = {"data": json.loads(row["value"]) if row and row["value"] else None,
                "updated_at": row["updated_at"] if row else None}
        return Response(json.dumps(body, ensure_ascii=False), status=200, headers={**headers, "Access-Control-Allow-Origin": "*"} if "Access-Control-Allow-Origin" not in headers else headers)
    if origin not in MYTOOLS_ORIGINS:
        conn.close()
        return Response(json.dumps({"ok": False, "error": "origin not allowed"}), status=403, headers=headers)
    payload = request.get_json(force=True, silent=True) or {}
    clean = _mytools_clean(payload.get("data"))
    if clean is None:
        conn.close()
        return Response(json.dumps({"ok": False, "error": "bad data"}), status=400, headers=headers)
    value = json.dumps(clean, ensure_ascii=False)
    if len(value) > 400_000:
        conn.close()
        return Response(json.dumps({"ok": False, "error": "too large"}), status=413, headers=headers)
    conn.execute(
        "INSERT INTO coach888_state (key, value, updated_at) VALUES (?, ?, datetime('now', 'localtime')) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at", (MYTOOLS_KEY, value))
    conn.execute("INSERT INTO mytools_history (value, saved_at) VALUES (?, datetime('now', 'localtime'))", (value,))
    conn.execute("DELETE FROM mytools_history WHERE id NOT IN (SELECT id FROM mytools_history ORDER BY id DESC LIMIT 60)")
    conn.commit()
    conn.close()
    return Response(json.dumps({"ok": True}), status=200, headers=headers)


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
    # 2026-10-21：常用查詢網站(my-tools)照抄熱門排行，網址前加「mytools::」記在同一張表；
    # 帶 ?prefix=mytools:: 只回那一份，不帶就排除，兩邊的前 10 名不會互相擠掉
    prefix = request.args.get("prefix", "")
    counts = {r["url"]: r["click_count"] for r in rows
              if (r["url"].startswith(prefix) if prefix else not r["url"].startswith("mytools::"))}
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


# ── GitHub 推送自動換新（2026-10-10 教練交辦，原 09-30 命令）──
# 教練要：event.bymyway.com 的靜態網站背後都有 GitHub，他在聯想／宏碁／小龍蝦改 GitHub，
# 網站就跟著換新，不用回 Mac。每個 repo 掛一個 GitHub webhook 打到這裡（push 事件），
# 用 HMAC 驗證是 GitHub 送來的，只認得登記過的網站，然後在背景把最新版拉回本機。
# 只服務策展名單（大樹作品＋策展SOP）的網站，走 curated_git.py sync（會先存 Mac 本機修改再合併）。
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
CURATED_GIT_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "curated_git.py"
_GH_REPO_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def _github_signature_ok(body: bytes, signature: str) -> bool:
    if not GITHUB_WEBHOOK_SECRET or not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(GITHUB_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def _origin_repo_name(path: Path) -> str:
    r = subprocess.run(["git", "-C", str(path), "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10)
    return r.stdout.strip().rstrip("/").split("/")[-1].removesuffix(".git") if r.returncode == 0 else ""


def _resolve_github_repo(repo_name: str):
    """GitHub repo 名稱 → 策展名單（大樹作品＋策展SOP）裡的網站代號。只服務這份名單，
    其他舊站（SITE_SYNC_REPOS）教練沒要求，不碰（2026-10-10 教練糾正）。"""
    for s in _load_curated_registry().get("sites", []):
        if (s.get("repo") or f"Coach1973/{s['slug']}").split("/")[-1] == repo_name:
            return "curated", s["slug"]
    return None, None


def _github_sync_worker(kind: str, key: str, pushed_sha: str) -> None:
    try:
        r = subprocess.run([sys.executable, str(CURATED_GIT_SCRIPT), "sync", key], capture_output=True, text=True,
                           timeout=300, env=_OPENCLAW_ENV)
        app.logger.info("github-sync %s %s %s rc=%s %s", kind, key, pushed_sha[:7], r.returncode, (r.stdout + r.stderr)[-300:])
        if r.returncode != 0:
            _notify_xiaolongxia(f"⚠️ GitHub 有新版本，但網站沒能自動換新：{key}\n"
                                f"原因：{(r.stdout + r.stderr).strip()[-200:]}\n需要 Mac 軍師處理")
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("github-sync %s %s failed", kind, key)
        _notify_xiaolongxia(f"⚠️ GitHub 有新版本，但網站沒能自動換新：{key}\n原因：{exc}")


_CLOUD_PUSH_LAST = {}
CLOUD_PENDING_DIR = WORKSPACE_ROOT / "state" / "cloud_branch_pending"   # 雲端交件待接手清單（開工注入、cloud_branch_pickup.sh 讀）
CLOUD_REPOS_CONF = WORKSPACE_ROOT / "scripts" / "cloud" / "cloud_repos.json"


def _record_cloud_branch_pending(repo_name: str, branch: str, payload: dict) -> bool:
    """雲端分支每推一次就更新一筆「待接手」紀錄（事件觸發）。回傳這個倉庫有沒有規則包（沒有的話通知會提醒補上）。"""
    commits = payload.get("commits") or []
    last = (commits[-1].get("message", "") if commits else "").splitlines()[0][:120]
    try:
        known = repo_name in json.loads(CLOUD_REPOS_CONF.read_text(encoding="utf-8")).get("repos", [])
    except Exception:
        known = True
    try:
        CLOUD_PENDING_DIR.mkdir(parents=True, exist_ok=True)
        f = CLOUD_PENDING_DIR / (repo_name + "__" + branch.replace("/", "__") + ".json")
        old = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        if old.get("status") == "done" and old.get("head") == str(payload.get("after", "")):
            return known
        f.write_text(json.dumps({
            "repo": repo_name, "branch": branch, "head": str(payload.get("after", "")), "last_message": last,
            "first_seen": old.get("first_seen") or datetime.now().isoformat(timespec="seconds"),
            "pushed_at": datetime.now().isoformat(timespec="seconds"), "status": "pending", "has_rules_pack": known,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        app.logger.exception("cloud pending record failed")
    return known


def _notify_cloud_branch_push(repo_name: str, branch: str, payload: dict) -> None:
    """雲端 Claude 對話把成果推到 claude/* 分支時：①寫一筆「待接手」紀錄（下次開工第一件事，驗證後直接合併上線，不問教練同不同意）
    ②電報通知教練（2026-10-15 教練：「我要等到什麼時候才知道他們交回來？」）。
    每個分支 10 分鐘內只通知一次，避免雲端連推好幾次洗版；通知失敗不影響 webhook 回應。"""
    known = _record_cloud_branch_pending(repo_name, branch, payload)
    now = time.time()
    key = repo_name + "/" + branch
    if now - _CLOUD_PUSH_LAST.get(key, 0) < 600:
        return
    _CLOUD_PUSH_LAST[key] = now
    commits = payload.get("commits") or []
    last = (commits[-1].get("message", "") if commits else "").splitlines()[0][:80]
    msg = (f"☁️ 雲端對話有交件：{repo_name} 的分支 {branch}\n"
           f"最新一筆：{last or '（無說明）'}\n"
           f"已排進軍師的待接手清單：軍師下次被叫到，第一件事就是驗證、用正式程式再測、合併上線，不會停在等您同意。")
    if not known:
        msg += f"\n⚠️ {repo_name} 還沒有雲端規則包（亮燈／交件流程），軍師會補上。"
    try:
        _notify_xiaolongxia(msg)
    except Exception:
        pass


@app.route("/hooks/github-site", methods=["POST"])
def github_site_webhook():
    body = request.get_data()
    if not _github_signature_ok(body, request.headers.get("X-Hub-Signature-256", "")):
        abort(403)
    event = request.headers.get("X-GitHub-Event", "")
    if event == "ping":
        return {"ok": True, "pong": True}
    if event != "push":
        return {"ok": True, "ignored": event}
    payload = request.get_json(silent=True) or {}
    repo = payload.get("repository") or {}
    repo_name = str(repo.get("name", ""))
    default_ref = f"refs/heads/{repo.get('default_branch') or 'main'}"
    if not _GH_REPO_NAME_RE.fullmatch(repo_name):
        abort(400)
    ref = str(payload.get("ref", ""))
    if ref.startswith("refs/heads/claude/") and payload.get("deleted") is not True:
        _notify_cloud_branch_push(repo_name, ref[len("refs/heads/"):], payload)   # 雲端對話交件：電報通知教練（事件觸發，不輪詢）
    if payload.get("ref") != default_ref:
        return {"ok": True, "ignored": "not default branch"}
    kind, key = _resolve_github_repo(repo_name)
    if kind is None:
        return {"ok": False, "error": "unknown repo"}, 404
    sha = str(payload.get("after", ""))
    threading.Thread(target=_github_sync_worker, args=(kind, key, sha), daemon=True).start()
    return {"ok": True, "kind": kind, "site": key, "commit": sha[:7]}, 202


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
