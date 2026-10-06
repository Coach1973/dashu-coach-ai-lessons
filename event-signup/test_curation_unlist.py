#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""策展後台「下架／重新上架」驗證（教練 2026-10-07 交辦：下架只能收起卡片，不能讓網站不見）

全部用臨時資料夾裡的假策展中心首頁、假名冊、假網站資料夾，不碰正式資料、不碰 GitHub
（假的遠端也是臨時資料夾裡的 bare repo）。驗證重點：
  1. 下架：卡片從首頁消失，但網站網址、資料夾、名冊條目都還在，後台清單還看得到
  2. 重新上架：卡片原樣放回（卡片內容逐字相同）
  3. 舊格式卡片（網址不是 event_url）也認得出來
  4. 大樹作品（no_shop_card）沒有卡片，不需要下架
  5. 沒登入不能操作

執行：cd event-signup && venv/bin/python3 test_curation_unlist.py
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import app as appmod

T = Path(tempfile.mkdtemp(prefix="unlist_test_"))
MARKER = "<!-- SHOP_CARDS_INSERT_POINT：新店家自動插入這行下面，勿刪除此標記 -->"


def card(title, url):
    return (f"          <!-- 計劃夥伴店家：{title}（策展SOP自動上架） -->\n"
            f'          <article class="shop-row"><h3>{title}</h3><a href="{url}">查看店家專屬網站</a></article>\n')


NEW = card("新店甲", "https://event.bymyway.com/curated/shop-a/")
OLD = card("舊店乙", "https://shops.bymyway.com/shop-b/")  # 早期卡片的網址格式
INDEX = f"<html><body>\n          {MARKER}\n\n{NEW}{OLD}</body></html>\n"


def git(*a, cwd):
    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True)


# 假遠端 + 假策展中心首頁
remote = T / "remote.git"
git("init", "-q", "--bare", "-b", "main", str(remote), cwd=T)
work = T / "shangquan"
work.mkdir()
git("init", "-q", "-b", "main", cwd=work)
(work / "index.html").write_text(INDEX, encoding="utf-8")
git("add", "index.html", cwd=work)
git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init", cwd=work)
git("remote", "add", "origin", str(remote), cwd=work)
git("push", "-q", "-u", "origin", "main", cwd=work)

# 假網站資料夾 + 假名冊
repos = T / "repos"
for slug in ("shop-a", "shop-b", "work-c"):
    (repos / slug).mkdir(parents=True)
    (repos / slug / "index.html").write_text(f"<html>{slug}</html>", encoding="utf-8")
registry = {"sites": [
    {"slug": "shop-a", "title": "新店甲", "event_url": "https://event.bymyway.com/curated/shop-a/", "status": "live"},
    {"slug": "shop-b", "title": "舊店乙", "event_url": "https://event.bymyway.com/curated/shop-b/", "status": "live"},
    {"slug": "work-c", "title": "作品丙", "event_url": "https://event.bymyway.com/curated/work-c/", "status": "live",
     "no_shop_card": True},
]}
reg_path = T / "registry.json"
reg_path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")

appmod.TAINAN_SHANGQUAN_REPO = work
appmod.CURATED_REGISTRY_PATH = reg_path
appmod.CURATED_REPOS_DIR = repos
appmod.app.secret_key = appmod.app.secret_key or "test-only"
client = appmod.app.test_client()
with client.session_transaction() as s:
    s["logged_in"] = True


def index():
    return (work / "index.html").read_text(encoding="utf-8")


def entry(slug):
    return next(s for s in json.loads(reg_path.read_text(encoding="utf-8"))["sites"] if s["slug"] == slug)


def post(path):
    return client.post(path).get_data(as_text=True)


CASES = []


def check(name, ok):
    CASES.append((name, bool(ok)))
    print(("✅" if ok else "❌"), name)


page = client.get("/curation/admin").get_data(as_text=True)
check("後台清單：新店甲顯示『展示中』且有『下架』鈕", "展示中" in page and "/curation/admin/unlist/shop-a" in page)
check("後台清單：舊格式卡片的舊店乙也認得是展示中（有下架鈕）", "/curation/admin/unlist/shop-b" in page)
check("後台清單：大樹作品不出現『下架』鈕（沒有卡片）", "/curation/admin/unlist/work-c" not in page)

msg = post("/curation/admin/unlist/shop-a")
check("下架：回覆『已下架』，且沒有任何失敗提示", "已下架" in msg and "失敗" not in msg)
check("下架：首頁卡片消失", "新店甲" not in index() and "舊店乙" in index())
check("下架：名冊條目還在，標記 listed=False 並存了卡片原文", entry("shop-a").get("listed") is False and NEW.strip() in entry("shop-a")["card_html"])
check("下架：網站網址仍然打得開（200）", client.get("/curated/shop-a/").status_code == 200)
check("下架：網站資料夾仍在", (repos / "shop-a" / "index.html").is_file())
page = client.get("/curation/admin").get_data(as_text=True)
check("下架：後台仍列出它，標示『已下架・網站還在』，有『重新上架』鈕", "已下架・網站還在" in page and "/curation/admin/relist/shop-a" in page)
pushed = subprocess.run(["git", "--git-dir", str(remote), "log", "-1", "--format=%s"], capture_output=True, text=True).stdout
check("下架：已推到遠端（commit 訊息寫明只收起卡片）", "只收起卡片" in pushed)
check("重複下架：被擋下並說明", "已經是下架狀態" in post("/curation/admin/unlist/shop-a"))

msg = post("/curation/admin/relist/shop-a")
check("重新上架：回覆『已重新上架』", "已重新上架" in msg)
check("重新上架：首頁逐字回到下架前", index() == INDEX)
check("重新上架：名冊乾淨（沒有 listed／card_html 殘留）", not any(k in entry("shop-a") for k in ("listed", "card_html", "unlisted_at")))
check("展示中再按重新上架：被擋下", "現在就是展示狀態" in post("/curation/admin/relist/shop-a"))

post("/curation/admin/unlist/shop-b")
check("舊格式卡片：下架後首頁沒有舊店乙、網站仍 200", "舊店乙" not in index() and client.get("/curated/shop-b/").status_code == 200)
post("/curation/admin/relist/shop-b")
check("舊格式卡片：重新上架後兩張卡片都在、沒有重複", index().count("<article") == 2 and index().count("舊店乙") == 2)  # 註解＋標題各一次

check("大樹作品：按下架被擋下，說明本來就沒有展示", "本來就沒有展示" in post("/curation/admin/unlist/work-c"))
check("大樹作品：名冊條目沒被動到", "listed" not in entry("work-c"))

anon = appmod.app.test_client()
r = anon.post("/curation/admin/unlist/shop-a")
check("沒登入：下架被導去登入頁", r.status_code == 302 and "/admin/login" in r.headers.get("Location", ""))
check("沒登入：重新上架被導去登入頁", anon.post("/curation/admin/relist/shop-a").status_code == 302)
check("亂寫的 slug：404", client.post("/curation/admin/unlist/..%2Fetc").status_code in (404, 405))

passed = sum(1 for _, ok in CASES if ok)
print(f"\n結果：{passed} 通過 / {len(CASES) - passed} 失敗（共 {len(CASES)}）")
sys.exit(0 if passed == len(CASES) else 1)
