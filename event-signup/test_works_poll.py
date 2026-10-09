#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹作品票選＋收集建議 /api/works/poll/<site>（2026-10-10，南應大記憶牆）。
暫時資料庫＋假通知。執行：cd event-signup && ./venv/bin/python test_works_poll.py"""
import os
import tempfile

import app as appmod
import db

TMP = tempfile.mkdtemp(prefix="works_poll_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
SENT = []
appmod._notify_xiaolongxia = lambda text, chat_id=appmod.TELEGRAM_NOTIFY_CHAT_ID: SENT.append((chat_id, text)) or True
client = appmod.app.test_client()
fails = []
V1, V2 = "voter-aaaaaaaa", "voter-bbbbbbbb"


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def vote(opt, voter, site="tut-memory"):
    return client.post(f"/api/works/poll/{site}/vote", json={"option": opt, "voter": voter})


r = client.get("/api/works/poll/tut-memory")
check("一開始四個選項都是 0 票", r.get_json()["counts"] == {"t1": 0, "t2": 0, "t3": 0, "t4": 0})
check("投 t2 → 1 票", vote("t2", V1).get_json()["counts"]["t2"] == 1)
check("同一個人重複投 t2 → 還是 1 票", vote("t2", V1).get_json()["counts"]["t2"] == 1)
check("另一個人投 t2 → 2 票", vote("t2", V2).get_json()["counts"]["t2"] == 2)
check("同一個人可以投不同主題", vote("t3", V1).get_json()["counts"]["t3"] == 1)
check("不存在的選項 → 400", vote("t9", V1).status_code == 400)
check("怪的 voter 代號 → 400", vote("t1", "../x").status_code == 400)
check("沒登記的作品 → 404", vote("t1", V1, site="hnv-cc").status_code == 404 and client.get("/api/works/poll/hnv-cc").status_code == 404)
check("重新讀取票數仍是 t2=2", client.get("/api/works/poll/tut-memory").get_json()["counts"]["t2"] == 2)

SENT.clear()
r = client.post("/api/works/poll/tut-memory/suggest", json={"suggestion": "想聽家專時期的故事", "name": "小美"})
check("送出建議 → ok 並通知活動報名群", r.get_json()["ok"] and len(SENT) == 1 and SENT[0][0] == appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID and "家專" in SENT[0][1])
conn = db.get_conn()
check("建議存進資料庫", conn.execute("SELECT COUNT(*) FROM works_poll_suggestions").fetchone()[0] == 1)
conn.close()
SENT.clear()
check("建議太短 → 400", client.post("/api/works/poll/tut-memory/suggest", json={"suggestion": "a"}).status_code == 400)
check("機器人隱藏欄位有填 → 假裝成功、不存不通知",
      client.post("/api/works/poll/tut-memory/suggest", json={"suggestion": "廣告廣告", "website": "x"}).get_json()["ok"] and not SENT)
appmod._WORKS_POLL_HITS.clear()
codes = [client.post("/api/works/poll/tut-memory/suggest", json={"suggestion": f"第{i}個主題想聽"}).status_code for i in range(7)]
check("同一 IP 一小時最多 5 則建議（第 6 則起 429）", codes[:5] == [200] * 5 and codes[5] == 429)
r = client.get("/api/works/counter/tut-memory/support-peijun")
check("按讚一開始是 0", r.get_json() == {"ok": True, "n": 0})
for _ in range(5):
    last = client.post("/api/works/counter/tut-memory/support-peijun").get_json()
check("同一個人連按 5 下 → 5 個讚（不限次數）", last["n"] == 5)
check("重新讀取還是 5", client.get("/api/works/counter/tut-memory/support-peijun").get_json()["n"] == 5)
check("沒登記的計數 → 404", client.post("/api/works/counter/tut-memory/other").status_code == 404 and client.post("/api/works/counter/hnv-cc/support-peijun").status_code == 404)
conn = db.get_conn()
check("資料表只有總數、沒有 IP 欄位", [c["name"] for c in conn.execute("PRAGMA table_info(works_counters)")] == ["site", "counter_key", "n"])
conn.close()
print(f"\n{'全部通過' if not fails else '失敗 ' + str(len(fails)) + ' 項'}")
raise SystemExit(1 if fails else 0)
