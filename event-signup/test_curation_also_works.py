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
files = sorted(p.name.rsplit(".", 1)[-1] for p in (TMP / "incoming").glob("*"))
check("店家沒帶 also_works → 不擋、不問，預設當作「要」（旁路檔有 .works）", r.status_code == 200 and "works" in files)
for p in (TMP / "incoming").glob("*"):
    p.unlink()
r = up("shop", "tmp-test-bb", also_works="maybe")
check("also_works 亂填 → 400，純文字原因叫AI自己改1、不准拿去問教練", r.status_code == 400 and r.mimetype == "text/plain" and "不要問教練" in r.get_data(as_text=True) and "不要拿去問教練" in r.get_data(as_text=True))
check("被擋的那次不留任何檔案", not list((TMP / "incoming").glob("*")))
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

# 2026-10-15 教練：用短網址上傳「失效」＝表單沒寫送到哪，瀏覽器把檔案 POST 回 /u/<代碼>（只准看）→ 405。
import re
html = client.get(f"/u/{code}").get_data(as_text=True)
action = re.search(r'<form[^>]*method="POST"[^>]*action="([^"]+)"', html)
check("短網址頁的上傳表單明寫送到 /curation/upload（不是送回自己）", bool(action) and action.group(1) == "/curation/upload")
hidden_key = re.search(r'name="key" value="([^"]+)"', html).group(1)
r = client.post(action.group(1), data={"key": hidden_key, "kind": "creation", "custom_slug": "tmp-test-short",
                                       "package": (io.BytesIO(b"PK"), "x.zip")}, content_type="multipart/form-data")
check("照短網址頁的表單送出（不帶 ?key=，只靠內建金鑰）→ 收件成功，不是 405／被導去登入", r.status_code == 200)
check("直接 POST 到短網址仍是 405（短網址只負責顯示）", client.post(f"/u/{code}", data={}).status_code == 405)

print("\n全部通過" if not fails else f"\n失敗 {len(fails)} 項：{fails}")
raise SystemExit(1 if fails else 0)
