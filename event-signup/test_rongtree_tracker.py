#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""榮樹下 SOP「進度追蹤表」（教練 2026-10-29：網頁直接勾選、存資料庫）。
用暫時資料庫、行程表複本，不碰正式資料、不發任何通知。
執行：cd event-signup && venv/bin/python test_rongtree_tracker.py"""
import datetime as dt
import json
import os
import tempfile
from pathlib import Path

import app as appmod
import db
import rongtree_guest as rg
import rongtree_tracker as rtk

TMP = tempfile.mkdtemp(prefix="rongtree_tracker_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
appmod.app.secret_key = appmod.app.secret_key or "test-secret"
CODE = rg.list_code(appmod.app.secret_key)
today = dt.datetime.now(rtk.TZ).date()
fut, past = (today + dt.timedelta(days=5)).isoformat(), (today - dt.timedelta(days=10)).isoformat()
old = (today - dt.timedelta(days=200)).isoformat()
sched = Path(TMP) / "sched.json"
sched.write_text(json.dumps({"events": [
    {"id": "fut00001", "date": fut, "start": "19:00", "end": "20:00", "title": "榮樹下訪談（待確認）", "booking_type": "榮樹下訪談",
     "tentative": True, "booked_by": "官網預約", "note": "官網預約：私人姓名（私人資料）", "form_token": "FutToken123"},
    {"id": "gcopy001", "date": fut, "start": "19:00", "end": "20:00", "title": "榮樹下訪談", "source": "Google日曆"},
    {"id": "past0001", "date": past, "start": "20:00", "end": "21:00", "title": "榮樹下訪談：測試來賓", "guest": "測試來賓",
     "booked_by": "邱裕榮", "form_token": "PastToken12"},
    {"id": "old00001", "date": old, "start": "20:00", "end": "21:00", "title": "榮樹下訪談：很久以前"},
    {"id": "empty001", "date": fut, "start": "21:30", "end": "22:30", "title": "榮樹下訪談"},
    {"id": "other001", "date": fut, "start": "10:00", "end": "11:00", "title": "咖啡會議"},
]}, ensure_ascii=False), encoding="utf-8")
rg.SCHEDULE = sched
conn = rg._conn()
conn.execute("INSERT INTO rongtree_guest_forms (token, date, start, guest, data) VALUES (?,?,?,?,?)",
             ("PastToken12", past, "20:00", "交表來賓", json.dumps({"name": "交表來賓"}, ensure_ascii=False)))
conn.commit()
conn.close()
client = appmod.app.test_client()
fails = []


def check(label, cond, detail=""):
    print(("✅ " if cond else "❌ ") + label, "" if cond else f"→ {detail}")
    if not cond:
        fails.append(label)


def get():
    r = client.get(f"/api/rongtree/tracker/{CODE}")
    return r.status_code, r.get_json() or {}


def post(body):
    r = client.post(f"/api/rongtree/tracker/{CODE}", json=body)
    return r.status_code, r.get_json() or {}


check("1. 代碼錯 → 404", client.get("/api/rongtree/tracker/wrongcode000").status_code == 404)
st, j = get()
ids = [r["id"] for r in j.get("rows", [])]
check("2. 只列榮樹下訪談、過去 120 天～未來 60 天；Google 副本不重複；沒來賓也沒邀請人的空場不列", st == 200 and ids == ["past0001", "fut00001"], ids)
rows = {r["id"]: r for r in j.get("rows", [])}
check("3. 自動欄位：已交資料表的來賓名字、邀請人、代預約狀態、來賓卡份數",
      rows["past0001"]["guest"] == "交表來賓" and rows["past0001"]["inviter"] == "邱裕榮" and rows["past0001"]["booked"] == "✅"
      and rows["past0001"]["cards"] == 1 and rows["fut00001"]["booked"] == "待確認" and rows["fut00001"]["cards"] == 0, rows)
check("3b. 私人備註（預約人姓名、電話）不會出現在進度表", "私人姓名" not in json.dumps(j, ensure_ascii=False), j)
check("4. 手動欄位預設：勾選＝false、下拉＝空", rows["fut00001"]["group"] is False and rows["fut00001"]["warm"] == "", rows["fut00001"])
st, j2 = post({"id": "fut00001", "field": "group", "value": True})
st2, _ = post({"id": "fut00001", "field": "warm", "value": "會前會 ✅"})
st3, _ = post({"id": "past0001", "field": "shorts", "value": "暫存待剪"})
_, j = get()
rows = {r["id"]: r for r in j["rows"]}
check("5. 勾選、下拉都存進資料庫，重新讀取還在", st == st2 == st3 == 200 and rows["fut00001"]["group"] is True
      and rows["fut00001"]["warm"] == "會前會 ✅" and rows["past0001"]["shorts"] == "暫存待剪", rows)
post({"id": "fut00001", "field": "group", "value": False})
_, j = get()
check("5b. 取消勾選也存得住，其他欄不受影響", {r["id"]: r for r in j["rows"]}["fut00001"]["group"] is False
      and {r["id"]: r for r in j["rows"]}["fut00001"]["warm"] == "會前會 ✅", j)
check("6. 不在白名單的欄位 → 400", post({"id": "fut00001", "field": "guest", "value": "亂改"})[0] == 400)
check("6b. 不在選項裡的值 → 400", post({"id": "fut00001", "field": "warm", "value": "亂寫"})[0] == 400)
check("6c. 勾選欄給字串 → 400", post({"id": "fut00001", "field": "done", "value": "yes"})[0] == 400)
check("6d. 不在進度表上的行程（咖啡會議、太久以前）→ 400",
      post({"id": "other001", "field": "done", "value": True})[0] == 400 and post({"id": "old00001", "field": "done", "value": True})[0] == 400)
check("6e. POST 代碼錯 → 404", client.post("/api/rongtree/tracker/wrongcode000", json={"id": "fut00001", "field": "done", "value": True}).status_code == 404)

print("\n全部通過" if not fails else f"\n有 {len(fails)} 項失敗：{fails}")
raise SystemExit(1 if fails else 0)
