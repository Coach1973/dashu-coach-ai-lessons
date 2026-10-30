#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NMDA 會員資料（教練 2026-10-30）。用暫時資料庫、暫時照片資料夾、假通知，不碰正式資料、不真的發 Telegram。
執行：cd event-signup && venv/bin/python test_nmda_members.py"""
import io
import os
import tempfile
import time
from pathlib import Path

from PIL import Image

import app as appmod
import db
import nmda_members as nm

TMP = tempfile.mkdtemp(prefix="nmda_members_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
nm.UPLOAD_DIR = Path(TMP) / "uploads"
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
    Image.new("RGB", (1600, 1200), (179, 34, 29)).save(b, "JPEG")
    b.seek(0)
    return b


def wait_sent(n):
    for _ in range(30):
        if len(SENT) >= n:
            return
        time.sleep(0.05)


code = nm.admin_code(appmod.app.secret_key)
ALL_LINKS = {"link_web": "example.com", "link_fb": "https://facebook.com/x", "link_ig": "https://instagram.com/x",
             "link_threads": "https://threads.net/@x", "link_youtube": "https://youtube.com/@x",
             "link_linkedin": "https://linkedin.com/in/x", "link_podcast": "https://podcast.example/x",
             "link_blog": "https://blog.example/x", "link_gjw": "https://www.ganjing.world/x", "link_line": "@abc123"}

# 1. 一開始是空的
r = client.get("/api/nmda/members/board")
check("API 打得開、no-store、允許跨站讀、一開始是空名單", r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
      and r.headers["Access-Control-Allow-Origin"] == "*" and r.get_json() == [])

# 2. 建立檔案頁
h = client.get("/nmda/members/join").get_data(as_text=True)
check("建立頁有姓名、公司職稱、簡介、照片", all(x in h for x in ('name="name"', 'name="company_title"', 'name="bio"', 'name="photo"')))
check("建立頁有 12 種連結欄位（含抖音、其他連結、Threads、YouTube、LinkedIn、Podcast、部落格）", all(f'name="{k}"' in h for k in nm.LINK_KEYS) and len(nm.LINK_KEYS) == 12)
check("連結欄位選填、姓名公司簡介照片必填", h.count(">選填<") >= 10 and h.count("required") >= 4)

# 3. 缺欄位擋下
r = client.post("/nmda/members/join", data={"name": "王小明"}, content_type="multipart/form-data")
check("沒填公司職稱簡介照片擋下（400）", r.status_code == 400)
r = client.post("/nmda/members/join", data={"name": "王小明", "company_title": "明光企業", "bio": "樂於服務。"}, content_type="multipart/form-data")
check("沒上傳照片擋下（400）", r.status_code == 400 and "照片" in r.get_data(as_text=True))
r = client.post("/nmda/members/join", data={"name": "王小明", "company_title": "明光企業", "bio": "樂於服務。", "photo": (io.BytesIO(b"not an image"), "x.jpg")},
                content_type="multipart/form-data")
check("假圖片檔擋下（400）", r.status_code == 400)

# 4. 送出即上架
r = client.post("/nmda/members/join", data={"name": "王小明", "company_title": "明光企業 總經理", "bio": "樂於服務。", **ALL_LINKS, "photo": (jpg(), "w.jpg")},
                content_type="multipart/form-data")
check("送出轉到 ?new=1", r.status_code == 302 and r.headers["Location"].endswith("?new=1"))
edit_url = r.headers["Location"].split("?")[0]
token = edit_url.rsplit("/", 1)[1]
wait_sent(1)
check("通知進活動報名群，含公開頁與後台網址", len(SENT) == 1 and "會員資料" in SENT[0][1] and nm.PAGE_URL in SENT[0][1] and code in SENT[0][1])
data = client.get("/api/nmda/members/board").get_json()
me = data[0]
check("API 有一位、欄位正確、不含修改連結", len(data) == 1 and me["name"] == "王小明" and me["title"] == "明光企業 總經理" and "edit" not in me and "edit_token" not in str(me))
check("10 個連結都在、網址補成 https、LINE ID 轉成加好友網址", len(me["links"]) == 10 and me["links"][0]["url"] == "https://example.com"
      and me["links"][-1]["url"] == "https://line.me/ti/p/~abc123" and [l["label"] for l in me["links"]][:5] == ["官網", "Facebook", "Instagram", "Threads", "YouTube"])
check("照片打得開、縮在 900px 內", client.get(me["photo"].replace(nm.SITE, "")).status_code == 200 and max(Image.open(nm.UPLOAD_DIR / me["photo"].rsplit("/", 1)[1]).size) <= 900)

# 5. 本人修改、只留部分連結、新的排最前面
h = client.get(edit_url + "?new=1").get_data(as_text=True)
check("修改頁顯示專屬連結與「王小明 的檔案」", "王小明 的檔案" in h and edit_url in h)
r = client.post(edit_url, data={"name": "王小明", "company_title": "明光企業 董事長", "bio": "改過了。", "link_web": "mingguang.tw"}, content_type="multipart/form-data")
me = client.get("/api/nmda/members/board").get_json()[0]
check("修改成功（不換照片保留原照片、連結清掉沒填的）", r.status_code == 302 and me["title"] == "明光企業 董事長" and me["photo"] and [l["label"] for l in me["links"]] == ["官網"])
client.post("/nmda/members/join", data={"name": "李美麗", "company_title": "美麗工作室", "bio": "第二位。", "photo": (jpg(), "l.jpg")}, content_type="multipart/form-data")
check("後來建立的排前面", [p["name"] for p in client.get("/api/nmda/members/board").get_json()] == ["李美麗", "王小明"])

# 6. 機器人、後台
r = client.post("/nmda/members/join", data={"website": "bot", "name": "機器人"}, content_type="multipart/form-data")
check("機器人隱藏欄位：假裝成功、不建立", r.status_code == 302 and "機器人" not in str(client.get("/api/nmda/members/board").get_json()))
h = client.get(f"/nmda/members/a/{code}").get_data(as_text=True)
check("後台打得開、列出所有人", "王小明" in h and "李美麗" in h)
check("後台簽章錯 404", client.get("/nmda/members/a/wrongcode").status_code == 404)
wid = next(p["id"] for p in client.get("/api/nmda/members/board").get_json() if p["name"] == "王小明")
client.post(f"/nmda/members/a/{code}/hide/{wid}", data={"hidden": "1"})
check("隱藏後公開 API 看不到、後台還看得到", "王小明" not in str(client.get("/api/nmda/members/board").get_json()) and "王小明" in client.get(f"/nmda/members/a/{code}").get_data(as_text=True))
client.post(f"/nmda/members/a/{code}/delete/{wid}")
check("刪除後後台也看不到", "王小明" not in client.get(f"/nmda/members/a/{code}").get_data(as_text=True))

# 7. 本人刪除、HTML 跳脫、不影響理監事團隊
li = next(p for p in client.get("/api/nmda/members/board").get_json() if p["name"] == "李美麗")
tok_li = db.get_conn().execute("SELECT edit_token FROM nmda_members WHERE id=?", (li["id"],)).fetchone()[0]
photo_li = li["photo"].rsplit("/", 1)[1]
r = client.post(f"/nmda/members/edit/{tok_li}/delete")
check("本人刪除、照片檔一起清掉", r.status_code == 302 and not (nm.UPLOAD_DIR / photo_li).exists() and client.get("/api/nmda/members/board").get_json() == [])
client.post("/nmda/members/join", data={"name": "<script>alert(1)</script>", "company_title": "<b>x</b>", "bio": "y", "photo": (jpg(), "z.jpg")}, content_type="multipart/form-data")
check("後台輸出會跳脫 HTML", "<script>alert(1)</script>" not in client.get(f"/nmda/members/a/{code}").get_data(as_text=True))
check("理監事團隊 API 仍正常", client.get("/api/nmda/team/board").status_code == 200)

# 8. 工作人員帳密登入後台（教練 2026-10-30：帳號 admin、專用登入網址）
client2 = appmod.app.test_client()
client2.post("/nmda/members/join", data={"name": "後台測試", "company_title": "測試公司", "bio": "x", "photo": (jpg(), "a.jpg")}, content_type="multipart/form-data")
h = client2.get("/nmda/members/login").get_data(as_text=True)
check("登入頁有帳號、密碼欄位", 'name="username"' in h and 'name="password"' in h and 'type="password"' in h)
r = client2.get("/nmda/members/admin")
check("沒登入打後台 → 轉去登入頁", r.status_code == 302 and r.headers["Location"] == "/nmda/members/login")
check("沒登入打隱藏／刪除 → 轉去登入頁、不會動資料", client2.post("/nmda/members/admin/delete/1").headers["Location"] == "/nmda/members/login")
r = client2.post("/nmda/members/login", data={"username": "admin", "password": "wrong"})
check("密碼錯 → 401、不給進後台", r.status_code == 401 and client2.get("/nmda/members/admin").status_code == 302)
r = client2.post("/nmda/members/login", data={"username": "other", "password": "88888"})
check("帳號錯 → 401", r.status_code == 401)
r = client2.post("/nmda/members/login", data={"username": "admin", "password": "88888"})
check("帳密對 → 轉到後台", r.status_code == 302 and r.headers["Location"] == "/nmda/members/admin")
h = client2.get("/nmda/members/admin").get_data(as_text=True)
check("後台看得到會員、有登出鈕、操作走 /nmda/members/admin/", "後台測試" in h and "/nmda/members/logout" in h and "/nmda/members/admin/hide/" in h)
check("工作人員 session 進不了教練的主後台 /admin", client2.get("/admin").status_code in (302, 401, 403))
sid = next(p["id"] for p in client2.get("/api/nmda/members/board").get_json() if p["name"] == "後台測試")
client2.post(f"/nmda/members/admin/hide/{sid}", data={"hidden": "1"})
check("工作人員可隱藏", "後台測試" not in str(client2.get("/api/nmda/members/board").get_json()))
client2.post(f"/nmda/members/admin/delete/{sid}")
check("工作人員可刪除", "後台測試" not in client2.get("/nmda/members/admin").get_data(as_text=True))
client2.post("/nmda/members/logout")
check("登出後進不了後台", client2.get("/nmda/members/admin").status_code == 302)
client3 = appmod.app.test_client()
for _ in range(5):
    client3.post("/nmda/members/login", data={"username": "admin", "password": "bad"})
r = client3.post("/nmda/members/login", data={"username": "admin", "password": "88888"})
check("連錯 5 次後鎖 10 分鐘（連對的密碼也擋）", r.status_code == 429)
appmod._NM_LOGIN_FAILS.clear()
check("原本教練的簽章短址後台仍可用", client.get(f"/nmda/members/a/{code}").status_code == 200)

print("\n全部通過 ✅" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
raise SystemExit(1 if fails else 0)
