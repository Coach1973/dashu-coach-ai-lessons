#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹常用查詢網站排版存檔 /api/mytools/state：Origin 檢查、格式檢查、歷史保留。
執行：cd event-signup && python test_mytools_state.py"""
import json
import os
import tempfile

try:  # Windows 沒有 fcntl（只影響行程表檢視），測試用空殼
    import fcntl  # noqa: F401
except ImportError:
    import sys
    import types
    sys.modules["fcntl"] = types.ModuleType("fcntl")

import app as appmod
import db

TMP = tempfile.mkdtemp(prefix="mytools_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
c = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


OK = {"Origin": "https://coach1973.github.io"}
good = {"sections": [{"id": "a", "icon": "🤖", "title": "AI", "items": [{"name": "X", "url": "https://x.com/", "desc": "d", "tag": "t"}]}], "removed": ["https://old.com/"]}

check("沒存過 GET 回 data=null", c.get("/api/mytools/state").get_json()["data"] is None)
check("沒帶 Origin 的 POST 被擋 403", c.post("/api/mytools/state", json={"data": good}).status_code == 403)
check("別的網站 Origin 被擋 403", c.post("/api/mytools/state", json={"data": good}, headers={"Origin": "https://evil.com"}).status_code == 403)
check("正確 Origin 存檔 200", c.post("/api/mytools/state", json={"data": good}, headers=OK).status_code == 200)
got = c.get("/api/mytools/state").get_json()["data"]
check("讀回內容相同", got["sections"][0]["items"][0]["url"] == "https://x.com/" and got["removed"] == ["https://old.com/"])
bad = json.loads(json.dumps(good)); bad["sections"][0]["items"][0]["url"] = "javascript:alert(1)"
check("非 http(s) 網址 400", c.post("/api/mytools/state", json={"data": bad}, headers=OK).status_code == 400)
check("sections 不是 list 400", c.post("/api/mytools/state", json={"data": {"sections": "x"}}, headers=OK).status_code == 400)
check("空分類清單 400", c.post("/api/mytools/state", json={"data": {"sections": []}}, headers=OK).status_code == 400)
check("壞資料沒有蓋掉好資料", c.get("/api/mytools/state").get_json()["data"]["sections"][0]["title"] == "AI")
extra = json.loads(json.dumps(good)); extra["sections"][0]["items"][0]["evil"] = "<script>"; extra["sections"][0]["title"] = "  新名字  "
c.post("/api/mytools/state", json={"data": extra}, headers=OK)
got = c.get("/api/mytools/state").get_json()["data"]
check("多餘欄位被丟掉、標題去空白", "evil" not in got["sections"][0]["items"][0] and got["sections"][0]["title"] == "新名字")
for i in range(65):
    c.post("/api/mytools/state", json={"data": good}, headers=OK)
conn = db.get_conn(); n = conn.execute("SELECT COUNT(*) FROM mytools_history").fetchone()[0]; conn.close()
check("歷史只留最近 60 份", n == 60)
check("OPTIONS 預檢 204", c.options("/api/mytools/state", headers=OK).status_code == 204)
check("coach888 狀態端點看不到 mytools_data", "mytools_data" not in c.get("/api/coach888/state").get_json())
tc = json.loads(json.dumps(good)); tc["trashCollapsed"] = True
c.post("/api/mytools/state", json={"data": tc}, headers=OK)
check("最近刪除收合狀態存得住", c.get("/api/mytools/state").get_json()["data"]["trashCollapsed"] is True)
c.post("/api/coach888/click", json={"url": "https://a.com/"})
c.post("/api/coach888/click", json={"url": "mytools::https://b.com/"})
check("作品一覽熱門排行看不到 mytools:: 點擊", c.get("/api/coach888/click-counts").get_json() == {"https://a.com/": 1})
check("常用查詢熱門排行只拿 mytools:: 點擊", c.get("/api/coach888/click-counts?prefix=mytools::").get_json() == {"mytools::https://b.com/": 1})
print("全過" if not fails else f"失敗 {len(fails)} 項")
raise SystemExit(1 if fails else 0)
