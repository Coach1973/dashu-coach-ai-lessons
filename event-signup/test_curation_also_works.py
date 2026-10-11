#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""策展上傳「要不要同時放大樹作品」必填（2026-10-10 公益路跑沒進大樹作品的源頭修法）。
暫時資料夾＋假通知。執行：cd event-signup && ./venv/bin/python test_curation_also_works.py"""
import io
import os
import tempfile
from pathlib import Path

import app as appmod

TMP = Path(tempfile.mkdtemp(prefix="curation_works_test_"))
appmod.CURATION_UPLOAD_DIR = TMP
appmod._notify_xiaolongxia = lambda *a, **k: True
appmod.CURATION_UPLOAD_KEY = KEY = "test-key-only"
client = appmod.app.test_client()
fails = []


def check(label, cond):
    print(("✅" if cond else "❌"), label)
    if not cond:
        fails.append(label)


def up(kind, slug, **extra):
    data = {"kind": kind, "custom_slug": slug, "package": (io.BytesIO(b"PK"), "x.zip"), **extra}
    return client.post(f"/curation/upload?key={KEY}", data=data, content_type="multipart/form-data")


r = up("shop", "tmp-test-aa")
check("店家沒帶 also_works → 400，並教 AI 去問教練", r.status_code == 400 and "要不要同時放進大樹作品" in r.get_data(as_text=True))
check("API 呼叫（curl）被擋時回純文字原因＋不准換 kind 繞過", r.mimetype == "text/plain" and "不准改 kind 繞過" in r.get_data(as_text=True))
r = client.post(f"/curation/upload?key={KEY}", data={"kind": "shop", "custom_slug": "tmp-test-ab", "package": (io.BytesIO(b"PK"), "x.zip")},
                content_type="multipart/form-data", headers={"Accept": "text/html"})
check("瀏覽器被擋時照舊顯示上傳頁＋原因", r.status_code == 400 and r.mimetype == "text/html" and "要不要同時放進大樹作品" in r.get_data(as_text=True))
check("被擋的那次不留任何檔案", not list((TMP / "incoming").glob("*")))
r = up("shop", "tmp-test-bb", also_works="maybe")
check("also_works 亂填 → 400", r.status_code == 400)
r = up("shop", "tmp-test-cc", also_works="1")
files = sorted(p.name.rsplit(".", 1)[-1] for p in (TMP / "incoming").glob("*"))
check("店家 also_works=1 → 收件，旁路檔有 .works", r.status_code == 200 and "works" in files)
for p in (TMP / "incoming").glob("*"):
    p.unlink()
r = up("shop", "tmp-test-dd", also_works="0")
files = sorted(p.name.rsplit(".", 1)[-1] for p in (TMP / "incoming").glob("*"))
check("店家 also_works=0 → 收件，沒有 .works", r.status_code == 200 and "works" not in files)
for p in (TMP / "incoming").glob("*"):
    p.unlink()
r = up("creation", "tmp-test-ee")
check("大樹作品不需要問（本來就進大樹作品）", r.status_code == 200)
page = client.get(f"/curation/upload?key={KEY}").get_data(as_text=True)
check("上傳頁有「要不要同時放進大樹作品」選項", 'name="also_works"' in page)

code = appmod.curation_upload_short_code()
r = client.get(f"/u/{code}")
check("短網址 /u/<10字> 打開就是上傳頁，帶著金鑰", r.status_code == 200 and KEY in r.get_data(as_text=True) and len(code) == 10)
check("短代碼不對 → 404", client.get("/u/aaaaaaaaaa").status_code == 404)

print("\n全部通過" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
raise SystemExit(1 if fails else 0)
