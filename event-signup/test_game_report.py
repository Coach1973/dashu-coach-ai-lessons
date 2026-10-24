#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""互動教材學習報告（教練 2026-10-25）。用暫時資料庫、假通知，不碰正式資料、不真的發 Telegram。
執行：cd event-signup && venv/bin/python test_game_report.py"""
import os
import tempfile

import app as appmod
import db
import game_report as gr

TMP = tempfile.mkdtemp(prefix="game_report_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
appmod.app.secret_key = appmod.app.secret_key or "test-secret"
SENT = []
appmod._notify_xiaolongxia = lambda text, chat_id=None: SENT.append((chat_id, text)) or True
appmod._curated_slugs = lambda: {"bni-gusest"}
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def post(**kw):
    body = {"site": "bni-gusest", "name": "王小明", "chapter": "真誠", "game": "你的假設對了嗎？",
            "sections": [{"title": "練習一", "items": [{"label": "當時我的假設", "value": "他不需要\n第二行"},
                                                       {"label": "結果如何", "value": ""}]}],
            "scores": [{"label": "小測驗", "got": 3, "total": 4}, {"label": "接待演練", "got": 4, "total": 4}],
            "feedback": ["很好"], "takeaway": "先問清楚，再明確邀請"}
    body.update(kw)
    return client.post("/api/game/report", json=body)


r = post(name="")
check("沒填姓名 → 400", r.status_code == 400 and "姓名" in r.get_json()["error"])
r = post(site="no-such-site")
check("不存在的教材 → 404", r.status_code == 404)
r = post(website="bot")
check("機器人欄位 → 假裝成功、不存", r.get_json()["ok"] and not gr.list_reports())

import time as _t
SENT.clear()
r = post()
j = r.get_json()
check("正常送出 → ok 且回報告網址", j["ok"] and j["url"].startswith("https://event.bymyway.com/game-report/"))
_t.sleep(0.3)
check("正常送出 → 通知活動報名群一次", len(SENT) == 1 and SENT[0][0] == appmod.TELEGRAM_REGISTRATION_GROUP_CHAT_ID
      and "王小明（真誠）" in SENT[0][1] and "小測驗 3/4" in SENT[0][1])
token = j["url"].rsplit("/", 1)[1]
page = client.get(f"/game-report/{token}").get_data(as_text=True)
check("報告頁有姓名、分數、答案、空白題標示", all(x in page for x in ("王小明", "3<small> / 4", "他不需要\n第二行", "（沒有填寫）", "先問清楚")))
check("報告頁 noindex", "noindex" in page)
check("錯的報告代碼 → 404", client.get("/game-report/xxxx").status_code == 404)

SENT.clear()
r = post(name="【測試】軍師")
_t.sleep(0.3)
check("名字開頭【測試】→ 有存但不通知", r.get_json()["ok"] and not SENT)

r = post(name="<script>alert(1)</script>", sections=[{"title": "<b>x</b>", "items": [{"label": "<img src=x>", "value": "<i>y</i>"}]}])
t2 = r.get_json()["url"].rsplit("/", 1)[1]
p2 = client.get(f"/game-report/{t2}").get_data(as_text=True)
check("輸入的 HTML 一律跳脫", "<script>alert" not in p2 and "&lt;img src=x&gt;" in p2 and "&lt;i&gt;y&lt;/i&gt;" in p2)

r = post(scores=[{"label": "亂", "got": 9, "total": 4}, {"label": "ok", "got": 1, "total": 2}])
d = gr.get(r.get_json()["url"].rsplit("/", 1)[1])
import json as _j
check("不合理的分數會被丟掉", [s["label"] for s in _j.loads(d["data"])["scores"]] == ["ok"])

code = gr.admin_code(appmod.app.secret_key)
check("後台錯的碼 → 404", client.get("/game-report/a/wrong").status_code == 404)
a = client.get(f"/game-report/a/{code}?site=bni-gusest").get_data(as_text=True)
check("後台列出所有報告與連結", "王小明" in a and f"/game-report/{token}" in a and "共 " in a)
check("後台短網址 /gr/<碼> 也能開", "王小明" in client.get(f"/gr/{code}").get_data(as_text=True) and gr.admin_url(appmod.app.secret_key).endswith(f"/gr/{code}"))

print("\n" + ("全部通過" if not fails else f"失敗 {len(fails)} 項：{fails}"))
raise SystemExit(1 if fails else 0)
