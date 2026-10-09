#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coach888 排版存檔的「新作品保護」：舊頁面存排版不能把剛自動登記的大樹作品蓋掉（2026-10-10 art-lab 被蓋）。
暫時資料庫。執行：cd event-signup && ./venv/bin/python test_coach888_keep_new_works.py"""
import json
import os
import tempfile
from datetime import datetime, timedelta

import app as appmod
import db

TMP = tempfile.mkdtemp(prefix="c888_keep_test_")
db.DB_PATH = os.path.join(TMP, "event.db")
db.init_db()
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def stamp(hours_ago):
    return (datetime.now() - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M")


NEW, OLD, SHOP = "https://event.bymyway.com/curated/new-work/", "https://event.bymyway.com/curated/old-work/", "https://event.bymyway.com/curated/a-shop/"
REG = {"sites": [
    {"slug": "new-work", "title": "新作品", "event_url": NEW, "no_shop_card": True, "uploaded_at": stamp(2)},
    {"slug": "old-work", "title": "舊作品", "event_url": OLD, "no_shop_card": True, "uploaded_at": stamp(200)},
    {"slug": "a-shop", "title": "店家", "event_url": SHOP, "uploaded_at": stamp(1)},
]}
appmod._load_curated_registry = lambda: REG


def save(layout, items=None):
    body = {"coach888_layout": json.dumps(layout, ensure_ascii=False)}
    if items is not None:
        body["coach888_items"] = json.dumps(items, ensure_ascii=False)
    return client.post("/api/coach888/state", json=body)


def current():
    return json.loads(client.get("/api/coach888/state").get_json()["coach888_layout"])


# 舊頁面存的排版沒有新作品
save({"zuixinzuopin": ["https://x/1"], "baoliu": []}, {})
lay = current()
check("72 小時內的大樹作品被補回最新作品最前面", lay["zuixinzuopin"][0] == NEW)
check("超過 72 小時的不管", OLD not in json.dumps(lay))
check("店家（有商圈卡）不歸這裡管", SHOP not in json.dumps(lay))
items = json.loads(client.get("/api/coach888/state").get_json()["coach888_items"])
check("補回時一併補上名稱", items.get(NEW, {}).get("name") == "新作品")

# 教練把它移到別的分類 → 不動
save({"zuixinzuopin": ["https://x/1"], "baoliu": [NEW]}, {})
lay = current()
check("教練移到別的分類 → 尊重，不搬回", lay["baoliu"] == [NEW] and NEW not in lay["zuixinzuopin"])

# 教練刪除（落在「最近刪除」）→ 不復活
save({"zuixinzuopin": ["https://x/1"], "recentlydeleted": [NEW]}, {})
lay = current()
check("教練刪除（最近刪除）→ 不復活", lay["recentlydeleted"] == [NEW] and NEW not in lay["zuixinzuopin"])

# 不帶 layout 的存檔照常
r = client.post("/api/coach888/state", json={"coach888_titles": "{}"})
check("只存別的 key 照常成功", r.get_json()["updated"] == ["coach888_titles"])

print("\n全部通過" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
raise SystemExit(1 if fails else 0)
