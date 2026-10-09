#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹作品通用留資料表單 /api/works/contact（教練 2026-10-10 裁示）。
用暫時資料庫＋假通知，不碰正式 event.db、不真的發 Telegram。執行：cd event-signup && python3 test_works_contact.py"""
import os
import sys
import tempfile

import app as appmod
import db

TMP = tempfile.mkdtemp(prefix="works_contact_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()

SENT = []
appmod._notify_xiaolongxia = lambda text, chat_id=appmod.TELEGRAM_NOTIFY_CHAT_ID: SENT.append({"chat_id": chat_id, "text": text}) or True
GROUP = appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID
client = appmod.app.test_client()
OK = {"site": "hnv-cc", "name": "測試勿理", "phone": "0912-345-678", "item": "洽詢代工", "message": "想了解"}
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def post(**over):
    data = dict(OK); data.update(over)
    return client.post("/api/works/contact", json=data)


r = post()
check("正常送出回 ok", r.status_code == 200 and r.get_json()["ok"] is True)
check("通知只發到「活動報名即時通知」群", len(SENT) == 1 and SENT[0]["chat_id"] == GROUP)
check("通知含作品名、姓名、電話、項目", all(k in SENT[0]["text"] for k in ("楊博士", "測試勿理", "0912-345-678", "洽詢代工")))
conn = db.get_conn(); row = conn.execute("SELECT * FROM works_contact_leads").fetchone()
check("資料有存進資料庫", row and row["site"] == "hnv-cc" and row["name"] == "測試勿理" and row["item"] == "洽詢代工")

n = len(SENT)
check("沒填姓名被擋", post(name=" ").status_code == 400)
check("電話太短被擋", post(phone="123").status_code == 400)
check("不存在的作品頁被擋", post(site="no-such-site").status_code == 404)
check("亂填 site 格式被擋", post(site="../etc").status_code == 404)
check("以上被擋的都沒有通知", len(SENT) == n)
r = post(website="http://spam")
check("機器人隱藏欄位：假裝成功但不通知不存檔", r.get_json()["ok"] is True and len(SENT) == n
      and conn.execute("SELECT COUNT(*) FROM works_contact_leads").fetchone()[0] == 1)
check("超長輸入被截斷", (post(name="字" * 200) and conn.execute("SELECT length(name) FROM works_contact_leads ORDER BY id DESC LIMIT 1").fetchone()[0] == 30))
appmod._WORKS_CONTACT_HITS.clear()
for _ in range(10):
    post()
check("同一 IP 每小時超過 10 次被擋", post().status_code == 429)
print("\n全部通過" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
sys.exit(1 if fails else 0)
