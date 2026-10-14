#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""榮樹下來賓資料表＋AI 來賓卡（教練 2026-10-14）。
用暫時資料庫、行程表複本、假 AI、假通知，不碰正式資料、不真的發 Telegram、不花 MiniMax 額度。
執行：cd event-signup && python3 test_rongtree_guest.py"""
import json
import os
import tempfile
import time
from pathlib import Path

import app as appmod
import db
import rongtree_guest as rg

TMP = tempfile.mkdtemp(prefix="rongtree_guest_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
appmod.app.secret_key = appmod.app.secret_key or "test-secret"
SECRET = appmod.app.secret_key

TOKEN = "TestToken123"
sched = Path(TMP) / "sched.json"
sched.write_text(json.dumps({"events": [{"id": "abcd1234", "date": "2026-10-20", "start": "19:00", "end": "20:00",
                                         "title": "榮樹下訪談：測試來賓", "guest": "測試來賓", "form_token": TOKEN}]},
                            ensure_ascii=False), encoding="utf-8")
rg.SCHEDULE = sched
rg.UPLOAD_DIR = Path(TMP) / "uploads"
SENT, PROMPTS = [], []
rg.send_baha = lambda text: SENT.append(text) or True
rg._call_minimax = lambda prompt: PROMPTS.append(prompt) or "## 一句話介紹\n測試介紹\n## 三個核心問題\n1. 問題一\n2. **問題二**"
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def wait_card():
    for _ in range(50):
        r = rg.get_form(TOKEN)
        if r and r["card_status"] != "pending":
            return r
        time.sleep(0.1)
    return rg.get_form(TOKEN)


OK = {"name": "測試來賓", "title": "測試公司 董事長", "contact": "0912-345-678", "intro": "我是測試來賓",
      "turns": "轉折一\n轉折二\n轉折三", "story": "我的公益故事", "avoid": "家人"}
PNG = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
       "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")

r = client.get(f"/rongtree/guest/{TOKEN}")
check("填表頁打得開、預先帶入來賓名字與訪談時間", r.status_code == 200 and "測試來賓" in r.get_data(as_text=True)
      and "2026-10-20 19:00" in r.get_data(as_text=True))
check("不存在的代碼一律 404", client.get("/rongtree/guest/NoSuchToken99").status_code == 404)

r = client.post(f"/rongtree/guest/{TOKEN}", json={**OK, "story": ""})
check("必填沒填會擋下並說是哪一欄", r.status_code == 400 and "公益故事" in r.get_json()["error"])
r = client.post(f"/rongtree/guest/{TOKEN}", json={**OK, "contact": "abc"})
check("聯絡方式不對會擋下", r.status_code == 400)

r = client.post(f"/rongtree/guest/{TOKEN}", json={**OK, "photo": PNG})
check("正常送出回 ok", r.status_code == 200 and r.get_json()["ok"] is True)
row = wait_card()
check("資料存進資料庫、來賓卡做好", row and row["card_status"] == "done" and "問題一" in row["card"])
check("交給 AI 的資料不含聯絡電話（個資不外送）", PROMPTS and "0912-345-678" not in PROMPTS[0] and "我的公益故事" in PROMPTS[0])
check("巴哈群組收到通知，網址自己一行且帶簽章", len(SENT) == 1 and "\n" + rg.card_url(SECRET, TOKEN) in SENT[0])

k = rg.card_sig(SECRET, TOKEN)
r = client.get(f"/rongtree/guest/{TOKEN}/card?k={k}")
html_ = r.get_data(as_text=True)
check("來賓卡打得開，Markdown 轉成標題與清單", r.status_code == 200 and "<h2>三個核心問題</h2>" in html_ and "<b>問題二</b>" in html_)
check("來賓卡沒簽章或簽章錯一律 404", client.get(f"/rongtree/guest/{TOKEN}/card").status_code == 404
      and client.get(f"/rongtree/guest/{TOKEN}/card?k=wrong").status_code == 404)
check("照片要簽章才看得到", client.get(f"/rongtree/guest/{TOKEN}/photo.jpg?k={k}").status_code == 200
      and client.get(f"/rongtree/guest/{TOKEN}/photo.jpg").status_code == 404)

r = client.post(f"/rongtree/guest/{TOKEN}", json={**OK, "story": "改過的故事"})
row = wait_card()
check("再送一次＝更新同一筆，照片保留", row["photo_file"] and json.loads(row["data"])["story"] == "改過的故事")
check("更新也通知，寫「更新了資料」", len(SENT) == 2 and "更新了資料" in SENT[1])

rg._call_minimax = lambda prompt: (_ for _ in ()).throw(RuntimeError("額度用完"))
client.post(f"/rongtree/guest/{TOKEN}", json=OK)
row = wait_card()
check("AI 失敗時資料照存、狀態標失敗、通知附重新產生網址", row["card_status"] == "failed" and "沒做出來" in SENT[-1])

rg._call_minimax = lambda prompt: "## 一句話介紹\n重做成功"
r = client.post(f"/rongtree/guest/{TOKEN}/card/regen?k={k}")
row = wait_card()
check("按「重新產生」會重做來賓卡", r.status_code == 302 and row["card_status"] == "done" and "重做成功" in row["card"])

r = client.get(rg.list_url(SECRET).replace("https://event.bymyway.com", ""))
check("後台列表打得開、列出來賓", r.status_code == 200 and "測試來賓" in r.get_data(as_text=True))
check("後台列表沒簽章或短代碼錯 404", client.get("/rongtree/cards").status_code == 404 and client.get("/rongtree/a/wrongcode123").status_code == 404)
check("舊的長連結照樣有效", client.get(f"/rongtree/cards?k={rg.list_sig(SECRET)}").status_code == 200)

# ---- 公開名單（榮樹下網頁「訪談嘉賓前置作業」）----
rg._ensure_forms = lambda: None      # 不去改正式行程表
import datetime as _dt
fut = (_dt.date.today() + _dt.timedelta(days=3)).isoformat()
sched.write_text(json.dumps({"events": [
    {"id": "abcd1234", "date": fut, "start": "19:00", "end": "20:00", "title": "榮樹下訪談：測試來賓", "guest": "測試來賓", "form_token": TOKEN},
    {"id": "eeee5555", "date": fut, "start": "20:00", "end": "21:00", "title": "榮樹下訪談", "form_token": "OtherToken456"},
    {"id": "ffff6666", "date": fut, "start": "08:00", "end": "09:00", "title": "BNI 例會"}]}, ensure_ascii=False), encoding="utf-8")
r = client.get("/api/rongtree/prep"); j = r.get_json(); raw = r.get_data(as_text=True)
check("前置作業只列榮樹下訪談、附資料表網址、標出誰已交", r.status_code == 200 and len(j["upcoming"]) == 2
      and j["upcoming"][0]["submitted"] and not j["upcoming"][1]["submitted"] and j["upcoming"][1]["form"] == "/rongtree/guest/OtherToken456")
check("已交來賓公開姓名、職稱、一句話介紹、照片", j["guests"] and j["guests"][0]["name"] == "測試來賓"
      and j["guests"][0]["title"] == "測試公司 董事長" and j["guests"][0]["line"] == "重做成功" and j["guests"][0]["photo"])
check("公開資料不含電話、不談的話題、AI 訪綱", all(x not in raw for x in ("0912-345-678", "家人", "核心問題")))
check("公開照片不用簽章就看得到", client.get(f"/rongtree/face/{TOKEN}.jpg").status_code == 200)
client.post(f"/rongtree/guest/{TOKEN}/card/public?k={k}", data={"public": "0"})
j = client.get("/api/rongtree/prep").get_json()
check("按「從公開名單隱藏」後公開名單看不到、照片也關掉", not j["guests"] and j["upcoming"][0]["guest"] == "測試來賓"
      and client.get(f"/rongtree/face/{TOKEN}.jpg").status_code == 404)
check("隱藏開關沒簽章 404", client.post(f"/rongtree/guest/{TOKEN}/card/public", data={"public": "1"}).status_code == 404)
client.post(f"/rongtree/guest/{TOKEN}/card/public?k={k}", data={"public": "1"})
check("恢復公開", client.get("/api/rongtree/prep").get_json()["guests"][0]["name"] == "測試來賓")
check("填表頁寫明哪些資料會公開", "姓名、公司職稱、照片與一句話介紹" in client.get(f"/rongtree/guest/{TOKEN}").get_data(as_text=True))

# ---- 同一場兩位以上來賓（2026-10-14 裕榮：9–10 點有兩位來賓）----
rg._call_minimax = lambda prompt: "## 一句話介紹\n第二位介紹"
SENT.clear()
guest2 = {**OK, "name": "第二位來賓", "title": "乙公司 總經理", "contact": "second@example.com", "story": "第二位的故事"}
c2 = appmod.app.test_client()                      # 另一支手機：沒有第一位的 cookie
before = rg.get_form(TOKEN)
h2 = c2.get(f"/rongtree/guest/{TOKEN}").get_data(as_text=True)
check("另一支手機打開同網址是空白表單，看不到第一位的資料", "我的公益故事" not in h2 and "改過的故事" not in h2 and 'value="測試來賓"' not in h2)
check("已有人交過時不預填名字，避免第二位看到前一位的名字", '<input id="name" name="name" value=""' in h2)
r = c2.post(f"/rongtree/guest/{TOKEN}", json=guest2)
check("第二位送出成功", r.status_code == 200 and r.get_json()["ok"])
k2 = TOKEN + "2"
for _ in range(50):
    row2 = rg.get_form(k2)
    if row2 and row2["card_status"] == "done":
        break
    time.sleep(0.1)
check("第二位另存一筆、來賓卡也做好", row2 and row2["guest"] == "第二位來賓" and row2["card_status"] == "done")
check("第一位的資料沒被蓋掉", rg.get_form(TOKEN)["guest"] == "測試來賓" and rg.get_form(TOKEN)["data"] == before["data"])
check("第二位也通知巴哈群組、網址帶自己的簽章", any(rg.card_url(SECRET, k2) in t and "第二位來賓" in t for t in SENT))
check("第二位的來賓卡打得開、填表頁連回場次代碼", f"/rongtree/guest/{TOKEN}\"" in c2.get(f"/rongtree/guest/{k2}/card?k={rg.card_sig(SECRET, k2)}").get_data(as_text=True))
r = c2.post(f"/rongtree/guest/{TOKEN}", json={**guest2, "story": "第二位改過"})
check("第二位同一支手機再送＝修改自己那筆，不會變第三位", json.loads(rg.get_form(k2)["data"])["story"] == "第二位改過" and rg.get_form(TOKEN + "3") is None)
c3 = appmod.app.test_client()
c3.post(f"/rongtree/guest/{TOKEN}", json={**guest2, "story": "換裝置修改"})
check("換一台裝置、同名再送＝修改同一位，不重複", json.loads(rg.get_form(k2)["data"])["story"] == "換裝置修改" and rg.get_form(TOKEN + "3") is None)
c2.set_cookie("rg_" + TOKEN, "", max_age=0, path="/rongtree/guest/")   # 等於按「新增另一位來賓」
c2.post(f"/rongtree/guest/{TOKEN}", json={**OK, "name": "第三位來賓", "contact": "third@example.com"})
check("按「新增另一位來賓」後再送出＝第三位", rg.get_form(TOKEN + "3") and rg.get_form(TOKEN + "3")["guest"] == "第三位來賓")
j = client.get("/api/rongtree/prep").get_json()
check("前置作業同一場列出所有來賓名字、顯示交了幾位", j["upcoming"][0]["count"] == 3 and all(n in j["upcoming"][0]["guest"] for n in ("測試來賓", "第二位來賓", "第三位來賓")))
check("公開名單每位都有、各有自己的照片網址規則", {g["name"] for g in j["guests"]} >= {"測試來賓", "第二位來賓", "第三位來賓"})
check("後台列表三位都列出", all(n in client.get(rg.list_url(SECRET).replace("https://event.bymyway.com", "")).get_data(as_text=True) for n in ("第二位來賓", "第三位來賓")))
appmod._RG_HITS.clear()      # 測試用同一個 IP，先清掉每小時 10 次的限流
for i in range(4, 8):
    appmod.app.test_client().post(f"/rongtree/guest/{TOKEN}", json={**OK, "name": f"來賓{i}", "contact": f"g{i}@example.com"})
r = appmod.app.test_client().post(f"/rongtree/guest/{TOKEN}", json={**OK, "name": "超額來賓", "contact": "over@example.com"})
check("一場最多收 6 位，超過會明確告知", r.status_code == 400 and "已經滿了" in r.get_json()["error"])

print(f"\n{'全部通過' if not fails else f'{len(fails)} 項失敗'}")
raise SystemExit(1 if fails else 0)
