#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""南應大校友會台南分會：理監事團隊與顧問團隊（教練 2026-10-14）。
用暫時資料庫、暫時照片資料夾、假通知，不碰正式資料、不真的發 Telegram。
執行：cd event-signup && venv/bin/python test_tut_team.py"""
import io
import os
import re
import tempfile
import time
from pathlib import Path

from PIL import Image

import app as appmod
import db
import tut_team as tt

TMP = tempfile.mkdtemp(prefix="tut_team_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
tt.UPLOAD_DIR = Path(TMP) / "uploads"
appmod.app.secret_key = appmod.app.secret_key or "test-secret"
SENT = []
appmod._notify_xiaolongxia = lambda text, chat_id=None: SENT.append((chat_id, text)) or True
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def jpg():
    b = io.BytesIO()
    Image.new("RGB", (1600, 1200), (133, 77, 146)).save(b, "JPEG")
    b.seek(0)
    return b


def wait_sent(n):
    for _ in range(30):
        if len(SENT) >= n:
            return
        time.sleep(0.05)


FORM = {"team": "board", "role": "理事長", "name": "王小明", "company_title": "明光企業 董事長",
        "dept_year": "企管系 1998 年畢業", "bio": "我是王小明，" + "樂於服務校友。" * 40,
        "link_web": "example.com", "link_line": "@wang"}

r = client.get("/tut/team")
h = r.get_data(as_text=True)
check("公開頁打得開、標題正確、用南應大紫色", r.status_code == 200 and "理監事候選人團隊與顧問團隊" in h and "#854D92" in h)
check("顧問 17 位＋理監事 23 位空座位已放好，各有「補上我的簡介」按鈕", h.count("補上我的簡介") == 40 and "林士民" in h and "林志和" in h)
check("顧問座位依記憶牆順序：林士民第一、林志和最後", h.index("林士民") < h.index("鄭儷絲") < h.index("林志和"))
check("理監事 23 位照教練貼的順序放好，在顧問區前面",
      h.index("王佩茹") < h.index("陳佩君") < h.index("孫熙閑") < h.index('id="advisor"') and "許山本美道子" in h)
check("有「我要建立檔案」按鈕", 'href="/tut/team/join"' in h)
check("/tut/ 召集令沒被新網址吃掉", client.get("/tut/").status_code in (200, 404) and client.get("/tut/team/").status_code == 200)

h = client.get("/tut/team/join").get_data(as_text=True)
check("建立檔案頁：先列兩個團隊的名單名字可直接點", "名單上已經有您的名字" in h and h.count("/tut/team/claim/") == 40
      and "理監事團隊" in h and "王佩茹" in h)

r = client.post("/tut/team/join", data={**FORM, "bio": ""}, content_type="multipart/form-data")
check("簡介沒填會擋下並說是哪一欄、資料保留", r.status_code == 400 and "個人簡介" in r.get_data(as_text=True) and "王小明" in r.get_data(as_text=True))
r = client.post("/tut/team/join", data={**FORM, "team": ""}, content_type="multipart/form-data")
check("沒選團隊會擋下", r.status_code == 400 and "理監事團隊" in r.get_data(as_text=True))
r = client.post("/tut/team/join", data=FORM, content_type="multipart/form-data")
check("新建一定要照片", r.status_code == 400 and "請上傳一張照片" in r.get_data(as_text=True))
r = client.post("/tut/team/join", data={**FORM, "photo": (io.BytesIO(b"not an image"), "x.jpg")}, content_type="multipart/form-data")
check("假圖片會擋下", r.status_code == 400 and "照片打不開" in r.get_data(as_text=True))

r = client.post("/tut/team/join", data={**FORM, "photo": (jpg(), "me.jpg")}, content_type="multipart/form-data")
loc = r.headers.get("Location", "")
check("送出成功 → 轉到自己的專屬修改頁", r.status_code == 302 and "/tut/team/edit/" in loc and "new=1" in loc)
token = re.search(r"/tut/team/edit/([^?]+)", loc).group(1)
h = client.get(loc).get_data(as_text=True)
check("修改頁顯示「已上架」與可複製的專屬連結", "已上架" in h and f"https://event.bymyway.com/tut/team/edit/{token}" in h)
wait_sent(1)
check("通知送進活動報名即時通知群，附公開頁與後台網址各自一行",
      SENT and SENT[0][0] == appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID and "王小明" in SENT[0][1]
      and "\n" + tt.admin_url(appmod.app.secret_key) in SENT[0][1])

h = client.get("/tut/team").get_data(as_text=True)
check("立刻出現在公開頁的理監事團隊", "王小明" in h and "明光企業 董事長" in h and "企管系 1998 年畢業" in h and h.index("王小明") < h.index('id="advisor"'))
check("長簡介收進「看完整介紹」", "看完整介紹" in h)
check("連結自動補上 https、LINE ID 轉成加好友網址", "https://example.com" in h and "https://line.me/ti/p/~wang" in h)
m = re.search(r'/tut/team/photo/([0-9a-f]{16}\.jpg)', h)
check("照片縮圖後公開可看", m and client.get(f"/tut/team/photo/{m.group(1)}").status_code == 200
      and max(Image.open(tt.UPLOAD_DIR / m.group(1)).size) <= tt.MAX_EDGE)
check("照片網址不能亂猜路徑", client.get("/tut/team/photo/..%2Fevent.db").status_code == 404)

old_photo = m.group(1)
r = client.post(f"/tut/team/edit/{token}", data={**FORM, "company_title": "明光企業 總經理"}, content_type="multipart/form-data")
check("修改不用重傳照片，照片保留", r.status_code == 302 and "saved=1" in r.headers["Location"]
      and tt.get_by_token(token)["photo_file"] == old_photo and "明光企業 總經理" in client.get("/tut/team").get_data(as_text=True))
client.post(f"/tut/team/edit/{token}", data={**FORM, "photo": (jpg(), "new.jpg")}, content_type="multipart/form-data")
check("換照片會刪掉舊檔", tt.get_by_token(token)["photo_file"] != old_photo and not (tt.UPLOAD_DIR / old_photo).exists())
check("修改不再發通知（只有新上架才通知）", len(SENT) == 1)
check("亂猜修改連結 404", client.get("/tut/team/edit/wrong-token").status_code == 404)

# ---- 顧問認座位 ----
seat = next(s for s in tt.open_seats() if s["name"] == "鄭儷絲")
r = client.post(f"/tut/team/claim/{seat['id']}")
check("點自己的名字 → 進到這個座位的修改頁", r.status_code == 302 and seat["edit_token"] in r.headers["Location"])
h = client.get(r.headers["Location"]).get_data(as_text=True)
check("座位修改頁已帶好名字、職稱、原本的網站連結，並提示補資料就上架",
      'value="鄭儷絲"' in h and "中華網紅協會理事長" in h and "https://event.bymyway.com/cica/" in h and "補上照片與簡介" in h)
r = client.post(f"/tut/team/edit/{seat['edit_token']}", data={"team": "advisor", "role": "顧問", "name": "鄭儷絲",
                "company_title": "中華網紅協會理事長", "bio": "網紅產業顧問", "photo": (jpg(), "z.jpg")}, content_type="multipart/form-data")
check("補完照片與簡介 → 上架（顯示專屬連結）", "new=1" in r.headers.get("Location", ""))
wait_sent(2)
check("顧問補完也通知一次", len(SENT) == 2 and "鄭儷絲" in SENT[1][1])
h = client.get("/tut/team").get_data(as_text=True)
check("公開頁顧問空座位少一個", h.count("補上我的簡介") == 39 and "網紅產業顧問" in h)
r = client.post(f"/tut/team/claim/{seat['id']}")
check("已補完的座位不能再被別人認領", "/tut/team/join" in r.headers.get("Location", ""))

# ---- 管理後台 ----
code = tt.admin_code(appmod.app.secret_key)
check("後台要簽章短碼，錯的 404", client.get("/tut/team/a/wrongcode123").status_code == 404
      and client.get(f"/tut/team/a/{code}").status_code == 200)
me = tt.get_by_token(token)
client.post(f"/tut/team/a/{code}/hide/{me['id']}", data={"hidden": "1"})
check("後台隱藏 → 公開頁看不到、資料保留", "王小明" not in client.get("/tut/team").get_data(as_text=True) and tt.get_by_token(token))
client.post(f"/tut/team/a/{code}/hide/{me['id']}", data={"hidden": "0"})
check("恢復顯示", "王小明" in client.get("/tut/team").get_data(as_text=True))
client.post(f"/tut/team/a/{code}/seat", data={"team": "board", "role": "常務理事", "name": "李監事", "company_title": "某公司"})
h = client.get("/tut/team").get_data(as_text=True)
check("後台新增理監事空座位 → 公開頁出現、可認領", "李監事" in h and "我是李監事，補上我的簡介" in h)
check("理監事依職務排序：理事長在常務理事前面", h.index("王小明") < h.index("李監事"))
check("後台操作沒簽章一律 404", client.post(f"/tut/team/a/wrong/delete/{me['id']}").status_code == 404)

client.post(f"/tut/team/edit/{token}/delete")
check("本人刪除自己的檔案 → 公開頁消失、照片檔刪掉", "王小明" not in client.get("/tut/team").get_data(as_text=True)
      and tt.get_by_token(token) is None)
check("重開網站不會重複放顧問座位", (tt.seed_advisor_seats() or True) and len([r for r in tt.list_members() if r["team"] == "advisor"]) == 17)
check("重開網站不會重複放理監事座位", len([r for r in tt.list_members() if r["name"] in tt.BOARD_SEATS]) == 23)

r = client.post("/tut/team/join", data={**FORM, "website": "spam"}, content_type="multipart/form-data")
check("機器人（填了隱藏欄位）不會建立資料", r.status_code == 302 and "王小明" not in client.get("/tut/team").get_data(as_text=True))

h = client.get("/tut/team").get_data(as_text=True)
check("公開頁不含修改連結、後台網址", "/tut/team/edit/" not in h and "/tut/team/a/" not in h)

# ---- 有網頁連結的顧問：先放網頁整理的介紹（2026-10-14 教練）----
h = client.get("/tut/team").get_data(as_text=True)
for nm in ("陳彥玲", "謝志賓", "林丁禾"):
    seg = h[h.index(nm):h.index("補上我的簡介", h.index(nm))]
    check(f"{nm} 座位已有網頁整理的介紹、標註待本人補充、附網頁連結", "整理自公開網頁" in seg and "看網頁介紹" in seg)
check("陳彥玲介紹寫對網頁上的頭銜", "紐約北方醫學中心國際合作處處長" in h)
check("謝志賓只介紹協會，不替本人編頭銜", "協會介紹：中華新媒體影音發展協會" in h)
seg = h[h.index("林家旭"):h.index("補上我的簡介", h.index("林家旭"))]
check("沒有網頁的顧問維持「簡介準備中」", "簡介準備中" in seg and "整理自公開網頁" not in seg)
seat = next(s for s in tt.open_seats() if s["name"] == "林丁禾")
h = client.get(f"/tut/team/edit/{seat['edit_token']}").get_data(as_text=True)
check("認領後修改頁帶入網頁整理的介紹，本人可以直接改", "藝術孵化實驗室" in h and "社會雕塑" in h)
client.post(f"/tut/team/edit/{seat['edit_token']}", data={"team": "advisor", "role": "顧問", "name": "林丁禾",
            "company_title": "藝術商務顧問", "bio": tt.get_by_id(seat["id"])["bio"], "photo": (jpg(), "l.jpg")},
            content_type="multipart/form-data")
b = tt.get_by_id(seat["id"])["bio"]
check("本人存檔後拿掉「待本人補充」字樣、內容保留", "待本人補充" not in b and "社會雕塑" in b)

# ---- 「為你轉身」的李中閔、施正益：介紹＋照片＋網頁連結 ----
h = client.get("/tut/team").get_data(as_text=True)
for nm, key in (("李中閔", "中華媒體交流協會總幹事"), ("施正益", "Google 地圖第 10 級在地嚮導")):
    seg = h[h.index(nm):h.index("補上我的簡介", h.index(nm))]
    i = h.rfind('<div class="card seat">', 0, h.index(nm))
    check(f"{nm} 座位有為你轉身的介紹、照片、網頁連結", key in seg and "curated/turnforyou/" in seg
          and "/tut/team/photo/" in h[i:h.index(nm)])
check("記憶牆舊寫法「施正義」已改成正確的「施正益」", "施正義" not in h and "施正益" in h)
n_before = len(list(tt.UPLOAD_DIR.glob("*.jpg")))
tt.seed_advisor_seats()
check("重複執行不會重複複製照片", len(list(tt.UPLOAD_DIR.glob("*.jpg"))) == n_before)

# ---- 百人導師的林丁禾、江睿翔、林士民：照片（＋簡介、社群）----
h = client.get("/tut/team").get_data(as_text=True)
def seat_seg(nm):
    i = h.index(nm)
    return h[h.rfind('<div class="card seat">', 0, i):h.index("補上我的簡介", i)]
seg = seat_seg("江睿翔")
check("江睿翔：百人導師照片、簡介、Facebook", "/tut/team/photo/" in seg and "ESG 永續經營" in seg and "facebook.com/mickjay1201" in seg)
seg = seat_seg("林士民")
check("林士民：只有照片，簡介仍準備中", "/tut/team/photo/" in seg and "簡介準備中" in seg)
check("林丁禾在測試裡已被認領，本人上傳的照片不會被百人導師照片蓋掉",
      tt.get_by_id(next(r["id"] for r in tt.list_members() if r["name"] == "林丁禾"))["filled"] == 1)

# ---- 後台一鍵複製專屬連結（2026-10-14 教練）----
h = client.get(f"/tut/team/a/{code}").get_data(as_text=True)
rows_n = len(tt.list_members(include_hidden=True))
check("後台每位都有「複製專屬連結」，連結是 https 完整網址", h.count("複製專屬連結</button>") == rows_n
      and len(re.findall(r"data-url='https://event.bymyway.com/tut/team/edit/[\w-]+'", h)) == rows_n)
check("後台說明哪條可傳給本人、哪條不能", "不要傳給別人" in h)
check("複製的連結真的打得開本人修改頁（不用登入）", client.get(re.search(r"data-url='https://event.bymyway.com(/tut/team/edit/[\w-]+)'", h).group(1)).status_code == 200)

# ---- 記憶牆「理監事校友名單」共用同一份資料（2026-10-23 教練）----
r = client.get("/api/tut/team/board")
raw = r.get_data(as_text=True)
data = r.get_json(force=True)
check("API：回 JSON、可跨站讀、不快取", r.status_code == 200 and r.headers.get("Access-Control-Allow-Origin") == "*"
      and "no-store" in r.headers.get("Cache-Control", "") and "json" in r.headers.get("Content-Type", ""))
check("API：23 位照貼的順序，顧問不混進來", [x["name"] for x in data if x["name"] in tt.BOARD_SEATS] == tt.BOARD_SEATS
      and not any(x["name"] in ("林士民", "林志和") for x in data))
check("API：不外洩修改連結與 IP", "edit_token" not in raw and "/tut/team/edit/" not in raw and '"ip"' not in raw)
seat = next(s for s in tt.open_seats() if s["name"] == "陳佩君")
client.post(f"/tut/team/edit/{seat['edit_token']}", data={"team": "board", "role": "常務理事", "name": "陳佩君",
            "company_title": "大樹教育 創辦人", "dept_year": "企管系 1998 年畢業", "bio": "簡介一\n\n簡介二",
            "link_web": "example.org", "photo": (jpg(), "p.jpg")}, content_type="multipart/form-data")
one = next(x for x in client.get("/api/tut/team/board").get_json(force=True) if x["name"] == "陳佩君")
check("API：補完資料後兩邊同步（職務｜公司、系級、簡介、照片、連結）",
      one["title"] == "常務理事 ｜ 大樹教育 創辦人" and one["bio"].startswith("🎓 企管系 1998 年畢業") and "簡介二" in one["bio"]
      and one["photo"].startswith("https://event.bymyway.com/tut/team/photo/") and one["links"] == [{"label": "網站", "url": "https://example.org"}])
check("API：照片網址真的打得開", client.get(one["photo"].replace("https://event.bymyway.com", "")).status_code == 200)
mid = tt.get_by_id(seat["id"])["id"]
client.post(f"/tut/team/a/{code}/hide/{mid}", data={"hidden": "1"})
check("API：後台隱藏的人兩邊都不顯示", "陳佩君" not in [x["name"] for x in client.get("/api/tut/team/board").get_json(force=True)]
      and "陳佩君" not in client.get("/tut/team").get_data(as_text=True))

# ---- 建置模式（教練 2026-10-23：直接在頁面上點就能補照片、簡介，不用先認領）----
bq = tt.admin_code(appmod.app.secret_key)
h = client.get("/tut/team").get_data(as_text=True)
check("一般訪客看不到編輯按鈕、也沒有建置碼", "✏️ 編輯" not in h and "build=" not in h)
h = client.get(f"/tut/team?build={bq}").get_data(as_text=True)
check("建置模式：每張卡都有編輯按鈕，有提示", h.count("✏️ 編輯（上傳照片／簡介）") == len(tt.list_members()) and "建置模式" in h)
check("建置碼錯（含中文）＝跟一般訪客一樣、不報錯",
      client.get("/tut/team?build=wrongwrong").status_code == 200 and "✏️ 編輯" not in client.get("/tut/team?build=wrongwrong").get_data(as_text=True)
      and client.get("/tut/team?build=%E4%B8%AD").status_code == 200)
seat = next(s for s in tt.open_seats() if s["name"] == "王佩茹")
n_sent = len(SENT)
r = client.post(f"/tut/team/edit/{seat['edit_token']}?build={bq}", data={"team": "board", "name": "王佩茹", "photo": (jpg(), "a.jpg")},
                content_type="multipart/form-data")
check("建置模式：只補照片就能存，轉回編輯頁並帶著建置碼", r.status_code == 302 and "saved=1" in r.headers["Location"] and f"build={bq}" in r.headers["Location"])
row = tt.get_by_id(seat["id"])
check("照片存好、算已上架、不發通知（不吵通知群）", row["photo_file"] and row["filled"] == 1 and len(SENT) == n_sent)
r = client.post(f"/tut/team/edit/{seat['edit_token']}?build={bq}", data={"team": "board", "name": "王佩茹",
                "company_title": "測試公司 董事長", "bio": "第一次補簡介"}, content_type="multipart/form-data")
row2 = tt.get_by_id(seat["id"])
check("建置模式：再補職稱簡介，照片保留", row2["company_title"] == "測試公司 董事長" and row2["bio"] == "第一次補簡介" and row2["photo_file"] == row["photo_file"])
h = client.get(f"/tut/team/edit/{seat['edit_token']}?build={bq}").get_data(as_text=True)
check("建置模式編輯頁：職稱簡介照片都不必填，回團隊頁帶建置碼",
      "required" not in re.search(r'<input[^>]*id="company_title"[^>]*>', h).group(0) and "required" not in re.search(r'<textarea[^>]*id="bio"[^>]*>', h).group(0)
      and "建置模式" in h and f"/tut/team/edit/{seat['edit_token']}?build={bq}" in h)
seat2 = next(s for s in tt.open_seats() if s["name"] == "楊孟薰")
r = client.post(f"/tut/team/edit/{seat2['edit_token']}", data={"team": "board", "name": "楊孟薰"}, content_type="multipart/form-data")
check("沒有建置碼的一般修改，簡介照片照樣必填", r.status_code == 400 and "個人簡介" in r.get_data(as_text=True))
r = client.post(f"/tut/team/edit/{seat2['edit_token']}?build=wrongwrong", data={"team": "board", "name": "楊孟薰"}, content_type="multipart/form-data")
check("建置碼錯的人不能借用寬鬆規則", r.status_code == 400)
api = client.get("/api/tut/team/board").get_json(force=True)
check("API 一般訪客：有 id 與 filled，沒有編輯網址", all("id" in x and "filled" in x and "edit" not in x for x in api))
api = client.get(f"/api/tut/team/board?build={bq}").get_json(force=True)
check("API 建置模式：每人多一個編輯網址", all(x["edit"].startswith("https://event.bymyway.com/tut/team/edit/") and f"build={bq}" in x["edit"] for x in api))
check("API 建置碼錯＝沒有編輯網址", all("edit" not in x for x in client.get("/api/tut/team/board?build=nope").get_json(force=True)))

r = client.get(f"/tut/b/{bq}")
check("短網址 /tut/b/<碼> → 團隊頁建置模式", r.status_code == 302 and r.headers["Location"] == f"/tut/team?build={bq}")
r = client.get(f"/tut/m/{bq}")
check("短網址 /tut/m/<碼> → 記憶牆理監事名單建置模式", r.status_code == 302 and r.headers["Location"] == f"/curated/tut-memory/?build={bq}#join")
check("短網址碼錯一律 404", client.get("/tut/b/wrongcode123").status_code == 404 and client.get("/tut/m/wrongcode123").status_code == 404)

print(f"\n{'全部通過' if not fails else f'{len(fails)} 項失敗'}")
raise SystemExit(1 if fails else 0)
