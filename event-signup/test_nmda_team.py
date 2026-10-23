#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NMDA 理監事團隊（教練 2026-10-23）。用暫時資料庫、暫時照片資料夾、假通知，不碰正式資料、不真的發 Telegram。
執行：cd event-signup && venv/bin/python test_nmda_team.py"""
import io
import os
import tempfile
import time
from pathlib import Path

from PIL import Image

import app as appmod
import db
import nmda_team as nt

TMP = tempfile.mkdtemp(prefix="nmda_team_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
nt.UPLOAD_DIR = Path(TMP) / "uploads"
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


code = nt.admin_code(appmod.app.secret_key)

# 1. 公開資料：先放陳佩君、吳大樹兩個空座位
r = client.get("/api/nmda/team/board")
data = r.get_json()
check("API 打得開、no-store、允許跨站讀", r.status_code == 200 and r.headers["Cache-Control"] == "no-store" and r.headers["Access-Control-Allow-Origin"] == "*")
check("先放陳佩君、吳大樹兩位，都是空座位、沒有修改連結", [p["name"] for p in data] == ["陳佩君", "吳大樹"] and not any(p["filled"] for p in data) and not any("edit" in p for p in data))
check("再讀一次不會重複放座位", len(client.get("/api/nmda/team/board").get_json()) == 2)

# 2. 建置模式：簽章對才多給編輯網址
data_b = client.get(f"/api/nmda/team/board?build={code}").get_json()
check("簽章對：每位多一條編輯網址（帶 build）", all(p.get("edit", "").endswith(f"?build={code}") for p in data_b))
check("簽章錯：照一般訪客處理", not any("edit" in p for p in client.get("/api/nmda/team/board?build=wrong").get_json()))
r = client.get(f"/nmda/b/{code}")
check("建置短網址轉到 NMDA 團隊頁建置模式", r.status_code == 302 and r.headers["Location"] == f"/curated/nmda/team.html?build={code}")
check("短網址簽章錯回 404", client.get("/nmda/b/wrongcode").status_code == 404)

# 3. 本人認領空座位 → 補資料 → 上架
mid = data[0]["id"]
r = client.post(f"/nmda/team/claim/{mid}")
check("點名字進到自己的修改頁", r.status_code == 302 and "/nmda/team/edit/" in r.headers["Location"])
edit_url = r.headers["Location"]
token = edit_url.rsplit("/", 1)[1]
h = client.get(edit_url).get_data(as_text=True)
check("修改頁顯示「陳佩君 的檔案」、NMDA 紅色、字級沒有小於 20px", "陳佩君 的檔案" in h and "#b3221d" in h and "font-size:1" not in h.replace("font-size:1.", ""))
r = client.post(edit_url, data={"name": "陳佩君", "role": "常務理事", "company_title": "", "bio": ""}, content_type="multipart/form-data")
check("沒填職稱簡介照片，一般模式擋下（400）", r.status_code == 400)
r = client.post(edit_url, data={"name": "陳佩君", "role": "常務理事", "company_title": "嗨餅乾 藝術策展人", "bio": "我是陳佩君。",
                                "link_web": "example.com", "photo": (jpg(), "me.jpg")}, content_type="multipart/form-data")
check("補完上架：轉到 ?new=1", r.status_code == 302 and r.headers["Location"].endswith("?new=1"))
wait_sent(1)
check("有發一則通知進活動報名群，含公開頁與後台網址", len(SENT) == 1 and "理監事團隊" in SENT[0][1] and nt.PAGE_URL in SENT[0][1] and code in SENT[0][1])
data2 = client.get("/api/nmda/team/board").get_json()
me = next(p for p in data2 if p["name"] == "陳佩君")
check("API 變成已上架、有職稱簡介照片連結", me["filled"] and me["role"] == "常務理事" and me["bio"] == "我是陳佩君。" and me["photo"].endswith(".jpg") and me["links"][0]["url"] == "https://example.com")
check("常務理事排在空座位前面", [p["name"] for p in data2][0] == "陳佩君")
check("照片打得開", client.get(me["photo"].replace(nt.SITE, "")).status_code == 200)
check("已補完的座位不能再被別人認領", client.post(f"/nmda/team/claim/{mid}").headers["Location"] == "/nmda/team/join")

# 4. 建置模式：只補照片，不發通知
mid2 = next(p["id"] for p in data2 if p["name"] == "吳大樹")
tok2 = client.post(f"/nmda/team/claim/{mid2}").headers["Location"].rsplit("/", 1)[1]
n0 = len(SENT)
r = client.post(f"/nmda/team/edit/{tok2}?build={code}", data={"name": "吳大樹", "photo": (jpg(), "t.jpg")}, content_type="multipart/form-data")
check("建置模式可只補照片、轉回儲存成功頁", r.status_code == 302 and "saved=1" in r.headers["Location"] and f"build={code}" in r.headers["Location"])
time.sleep(0.2)
check("建置模式不發通知", len(SENT) == n0)
check("吳大樹有照片了", next(p for p in client.get("/api/nmda/team/board").get_json() if p["name"] == "吳大樹")["photo"].endswith(".jpg"))

# 5. 自助建立新檔案、防機器人、後台
r = client.post("/nmda/team/join", data={"name": "王小明", "company_title": "明光企業", "bio": "樂於服務。", "photo": (jpg(), "w.jpg")}, content_type="multipart/form-data")
check("自己建立新檔案送出即上架", r.status_code == 302 and "?new=1" in r.headers["Location"])
r = client.post("/nmda/team/join", data={"website": "bot", "name": "機器人"}, content_type="multipart/form-data")
check("機器人隱藏欄位：假裝成功、不建立", r.status_code == 302 and "機器人" not in str(client.get("/api/nmda/team/board").get_json()))
h = client.get(f"/nmda/team/a/{code}").get_data(as_text=True)
check("後台打得開、列出所有人", "王小明" in h and "陳佩君" in h and "吳大樹" in h)
check("後台簽章錯 404", client.get("/nmda/team/a/wrongcode").status_code == 404)
client.post(f"/nmda/team/a/{code}/seat", data={"name": "林新人", "role": "理事"})
check("後台新增空座位", "林新人" in str(client.get("/api/nmda/team/board").get_json()))
wid = next(p["id"] for p in client.get("/api/nmda/team/board").get_json() if p["name"] == "王小明")
client.post(f"/nmda/team/a/{code}/hide/{wid}", data={"hidden": "1"})
check("隱藏後公開 API 看不到", "王小明" not in str(client.get("/api/nmda/team/board").get_json()))
client.post(f"/nmda/team/a/{code}/delete/{wid}")
check("刪除後後台也看不到", "王小明" not in client.get(f"/nmda/team/a/{code}").get_data(as_text=True))

# 6. 本人刪除、HTML 跳脫
tok_me = token
photo_me = me["photo"].rsplit("/", 1)[1]
r = client.post(f"/nmda/team/edit/{tok_me}/delete")
check("本人刪除自己的檔案、照片檔一起清掉", r.status_code == 302 and not (nt.UPLOAD_DIR / photo_me).exists() and "陳佩君" not in str(client.get("/api/nmda/team/board").get_json()))
client.post(f"/nmda/team/a/{code}/seat", data={"name": "<script>alert(1)</script>"})
check("後台輸出會跳脫 HTML", "<script>alert(1)</script>" not in client.get(f"/nmda/team/a/{code}").get_data(as_text=True))

print("\n全部通過 ✅" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
raise SystemExit(1 if fails else 0)
