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
check("公開頁打得開、標題正確、用南應大紫色", r.status_code == 200 and "理監事團隊與顧問團隊" in h and "#854D92" in h)
check("顧問名單 17 位空座位已放好，各有「補上我的簡介」按鈕", h.count("補上我的簡介") == 17 and "林士民" in h and "林志和" in h)
check("顧問座位依記憶牆順序：林士民第一、林志和最後", h.index("林士民") < h.index("鄭儷絲") < h.index("林志和"))
check("理監事目前沒名單，提示本人自己建立", "理監事名單確定後" in h)
check("有「我要建立檔案」按鈕", 'href="/tut/team/join"' in h)
check("/tut/ 召集令沒被新網址吃掉", client.get("/tut/").status_code in (200, 404) and client.get("/tut/team/").status_code == 200)

h = client.get("/tut/team/join").get_data(as_text=True)
check("建立檔案頁：先列顧問名單名字可直接點", "顧問名單上已經有您的名字" in h and h.count("/tut/team/claim/") == 17)

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
check("公開頁顧問空座位少一個", h.count("補上我的簡介") == 16 and "網紅產業顧問" in h)
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
check("認領後修改頁帶入網頁整理的介紹，本人可以直接改", "藝術孵化實驗室創辦人" in h)
client.post(f"/tut/team/edit/{seat['edit_token']}", data={"team": "advisor", "role": "顧問", "name": "林丁禾",
            "company_title": "藝術商務顧問", "bio": tt.get_by_id(seat["id"])["bio"], "photo": (jpg(), "l.jpg")},
            content_type="multipart/form-data")
b = tt.get_by_id(seat["id"])["bio"]
check("本人存檔後拿掉「待本人補充」字樣、內容保留", "待本人補充" not in b and "藝術孵化實驗室創辦人" in b)

# ---- 「為你轉身」的李中閔、施正義：介紹＋照片＋網頁連結 ----
h = client.get("/tut/team").get_data(as_text=True)
for nm, key in (("李中閔", "中華媒體交流協會總幹事"), ("施正義", "Google 地圖第 10 級在地嚮導")):
    seg = h[h.index(nm):h.index("補上我的簡介", h.index(nm))]
    i = h.rfind('<div class="card seat">', 0, h.index(nm))
    check(f"{nm} 座位有為你轉身的介紹、照片、網頁連結", key in seg and "curated/turnforyou/" in seg
          and "/tut/team/photo/" in h[i:h.index(nm)])
n_before = len(list(tt.UPLOAD_DIR.glob("*.jpg")))
tt.seed_advisor_seats()
check("重複執行不會重複複製照片", len(list(tt.UPLOAD_DIR.glob("*.jpg"))) == n_before)

print(f"\n{'全部通過' if not fails else f'{len(fails)} 項失敗'}")
raise SystemExit(1 if fails else 0)
