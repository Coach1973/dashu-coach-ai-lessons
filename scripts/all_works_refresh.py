#!/usr/bin/env python3
"""「完整作品一覽」資料產生器（教練 2026-10-15 交辦，百人軍火庫企劃書第七節第 1 項）

頁面：https://coach1973.github.io/all-works/（倉庫 Coach1973/all-works，本機 ~/github_repos/all-works）
這支腳本把「GitHub 全部倉庫」＋「策展名冊」合併成 data.json 推上去；大樹作品一覽（coach888）不在這裡抓，
頁面每次開啟時自己即時讀 https://event.bymyway.com/api/coach888/state（教練在作品集拖拉、改名都立刻反映）。

更新方式＝事件觸發，沒有任何排程或輪詢（教練已糾正 6 次）。觸發點：
  ① scripts/curation_process.py：每包上架處理完（含失敗）→ 背景跑一次
  ② event-signup/app.py：策展後台「下架／重新上架／刪除」按下去的那一刻
  ③ scripts/all_works_repo_hook.py：Claude Code 跑 `gh repo create`／`gh repo delete` 等指令之後（PostToolUse）
  ④ 頁面開啟時另外即時讀 GitHub 公開倉庫清單，補上別台電腦剛建、還沒觸發到的新倉庫

用法：
  python3 scripts/all_works_refresh.py            產生 data.json，有變動才 commit + push
  python3 scripts/all_works_refresh.py --dry-run  只印摘要，不寫檔
  python3 scripts/all_works_refresh.py --no-push  寫檔但不推
  python3 scripts/all_works_refresh.py --reason "上架 xxx"   寫進 commit 訊息
"""
import argparse
import concurrent.futures as cf
import fcntl
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

WS = Path(__file__).resolve().parent.parent
OWNER = "Coach1973"
REPO_DIR = Path.home() / "github_repos" / "all-works"
REGISTRY = WS / "event-signup" / "curated_sites_registry.json"
APP_PY = WS / "event-signup" / "app.py"
LOCK = WS / "state" / "all_works_refresh.lock"
ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/Users/bymyway/.local/bin:{os.environ.get('PATH', '')}"}

# 網址不照命名慣例、自動規則抓不到的對照（repo 名 → 它實際對外的網址）。
# 2026-10-15 逐一查證：同標題或 memory 記載（northern411＝northern-tw.netlify.app 兩邊標題相同）。
ALIASES = {
    "bni-chapters": ["chapters.bymyway.com"],
    "team-bymyway": ["team.bymyway.com"],
    "team01-guests": ["team01.bymyway.com"],
    "zhenxin-guests": ["zhenxin.bymyway.com"],
    "zhencheng-guests": ["sincere.bymyway.com"],      # 真誠分會
    "zhenzuan-guests": ["real-diamonds.bymyway.com"],  # 真鑽分會
    "zhengui-guests": ["real-wealth.bymyway.com"],     # 真貴籌備會
    "northern411": ["northern-tw.netlify.app"],
}

# 稱謂：「曾志雄博士」→ 也要搜得到「曾博士」（教練語音常這樣說）
TITLE_SUFFIX = "博士|老師|教授|醫師|律師|董事長|校長|教練|總經理|執行長|會長|理事長|創辦人|主任|院長|局長|主持人"
# 姓名（2~3 字）要緊貼在標點／空白／行首後面，才不會把「兼任助理教授」切成「任教授」這種假稱呼
ALIAS_RE = re.compile(rf"(?:^|[\s｜|、，,;；:：（(「【・/-])([一-鿿])[一-鿿]{{1,2}}({TITLE_SUFFIX})")


def canon(url: str) -> str:
    """網址正規化：去協定、參數、結尾斜線與 index.html，全小寫。頁面 JS 的 canon() 必須與此完全一致。"""
    p = urlparse(url.strip())
    path = re.sub(r"/index\.html?$", "", p.path, flags=re.I).rstrip("/")
    return (p.netloc + path).lower()


def token() -> str:
    r = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True, timeout=15, env=ENV)
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("無法從 git credential fill 取得 GitHub token")


def gh_get(tok: str, path: str):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={
        "Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json", "User-Agent": "all-works-refresh"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def fetch_repos(tok: str) -> list:
    out, page = [], 1
    while True:
        chunk = gh_get(tok, f"user/repos?per_page=100&affiliation=owner&page={page}")
        out += chunk
        if len(chunk) < 100:
            return out
        page += 1


def fetch_pages_urls(tok: str, repos: list) -> dict:
    def one(r):
        try:
            return r["name"], gh_get(tok, f"repos/{OWNER}/{r['name']}/pages").get("html_url") or ""
        except Exception:  # noqa: BLE001  Pages 設定讀不到就退回預設網址，不擋整份
            return r["name"], f"https://{OWNER.lower()}.github.io/{r['name']}/"
    with cf.ThreadPoolExecutor(8) as ex:
        return dict(ex.map(one, [r for r in repos if r.get("has_pages")]))


def route_map() -> dict:
    """event-signup/app.py 裡「網址路徑 → 哪個 GitHub 倉庫資料夾」，例如 /DIY3 → diy-studio-workshop。讀不到就空的。"""
    try:
        src = APP_PY.read_text(encoding="utf-8")
    except OSError:
        return {}
    var_dir = {m.group(1): m.group(2) for m in re.finditer(
        r'^([A-Z][A-Z0-9_]*)\s*=\s*Path\("/Users/bymyway/github_repos/([^"/]+)"\)', src, re.M)}
    out = {}
    for m in re.finditer(r'@app\.route\("(/[^"<]*?)/?"[^)]*\)\s*\ndef\s+\w+\([^)]*\):(.*?)(?=\n@app\.route|\ndef |\Z)', src, re.S):
        v = re.search(r"_serve_repo_file\(\s*([A-Z][A-Z0-9_]*)", m.group(2))
        if v and v.group(1) in var_dir:
            out.setdefault(var_dir[v.group(1)].lower(), "event.bymyway.com" + m.group(1))
    return out


def aliases_for(text: str) -> list:
    return sorted({m.group(1) + m.group(2) for m in ALIAS_RE.finditer(text)})


def short(s: str, n: int = 140) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def date_of(s: str) -> str:
    return (s or "")[:10]


def build(repos: list, pages: dict, registry: dict, routes: dict) -> dict:
    sites = registry.get("sites", [])
    reg_by_repo = {}
    for s in sites:
        name = (s.get("repo") or "").split("/")[-1] or s["slug"]
        reg_by_repo.setdefault(name.lower(), s)
    redirects = registry.get("redirects", {})
    items, seen_repo = [], set()

    def keys_for(name: str, reg: dict | None, extra: list) -> list:
        n = name.lower()
        ks = [f"coach1973.github.io/{n}", f"event.bymyway.com/curated/{n}", f"event.bymyway.com/{n}",
              f"{n}.netlify.app", f"{n}.bymyway.com"]
        if reg:
            ks += [f"event.bymyway.com/curated/{reg['slug'].lower()}"]
            ks += [f"event.bymyway.com/curated/{old.lower()}" for old, new in redirects.items() if new == reg["slug"]]
            for u in (reg.get("event_url"), reg.get("github_pages_url")):
                if u:
                    ks.append(canon(u))
        ks += [canon("https://" + e) for e in extra]
        return sorted(set(ks))

    for r in repos:
        name, low = r["name"], r["name"].lower()
        seen_repo.add(low)
        reg = reg_by_repo.get(low)
        extra = list(ALIASES.get(name, []))
        if low in routes:
            extra.append(routes[low])
        urls = []
        if reg and reg.get("event_url"):
            urls.append(reg["event_url"])
        urls += ["https://" + e + "/" for e in extra]
        if r.get("has_pages") and pages.get(name):
            urls.append(pages[name])
        if not urls:
            urls.append(r["html_url"])
        archived_copy = low.startswith("_archived_")
        shown = name[len("_archived_"):] if archived_copy else name
        title = (reg or {}).get("title") or ("" if r.get("private") else (r.get("description") or "")) or shown
        desc = (reg or {}).get("description") or ("" if r.get("private") else (r.get("description") or ""))
        if reg:
            cat = reg.get("category") or ""
            cat = "教練個人創作" if cat == "教練個人創作" else (f"策展・{cat}" if cat else "策展中心")
        elif archived_copy:
            cat = "封存副本"
        elif urls[0] == r["html_url"]:
            cat = "程式／內部倉庫"
        else:
            cat = "GitHub 網頁"
        delisted = archived_copy or (reg is not None and reg.get("listed") is False)
        items.append({
            "id": low,
            "name": short(("【封存副本】" if archived_copy else "") + title, 90),
            "desc": short(desc),
            "url": urls[0],
            "repoUrl": r["html_url"],
            "repo": name,
            "private": bool(r.get("private")),
            "archived": bool(r.get("archived")),
            "keys": keys_for(name, reg, extra),
            "cat": cat,
            "updated": max(date_of(r.get("pushed_at")), date_of((reg or {}).get("uploaded_at"))),
            "inRegistry": reg is not None,
            "delisted": delisted,
            "unlistedAt": (reg or {}).get("unlisted_at", ""),
            "aliases": aliases_for(f"{title} {desc}"),
        })

    # 名冊有、GitHub 帳號底下找不到對應倉庫的（例如倉庫改過名）：仍然要列出來
    for low, reg in reg_by_repo.items():
        if low in seen_repo:
            continue
        title, desc = reg.get("title") or reg["slug"], reg.get("description") or ""
        cat = reg.get("category") or ""
        items.append({
            "id": "reg:" + reg["slug"].lower(), "name": short(title, 90), "desc": short(desc),
            "url": reg.get("event_url") or reg.get("github_pages_url") or "", "repoUrl": "", "repo": "",
            "private": False, "archived": False, "keys": keys_for(reg["slug"], reg, []),
            "cat": "教練個人創作" if cat == "教練個人創作" else (f"策展・{cat}" if cat else "策展中心"),
            "updated": date_of(reg.get("uploaded_at")), "inRegistry": True,
            "delisted": reg.get("listed") is False, "unlistedAt": reg.get("unlisted_at", ""),
            "aliases": aliases_for(f"{title} {desc}"),
        })
    items.sort(key=lambda x: (x["updated"], x["id"]), reverse=True)
    return {"owner": OWNER, "items": items}


def git(*args, cwd=REPO_DIR, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True, env=ENV, timeout=90)


def publish(tok: str, reason: str) -> str:
    git("add", "data.json")
    if not git("status", "--porcelain", "data.json").stdout.strip():
        return "資料沒有變動，不推"
    git("-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com", "commit", "-q", "-m",
        f"[Mac] 完整作品一覽資料更新：{reason}")
    remote = f"https://{OWNER}:{tok}@github.com/{OWNER}/all-works.git"
    git("push", "-q", remote, "HEAD:main")
    return "已 commit + push：" + git("rev-parse", "--short", "HEAD").stdout.strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--reason", default="事件觸發")
    a = ap.parse_args(argv)
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)   # 同時被兩個觸發點叫到時排隊，後到的等前面跑完再跑（拿到最新狀態）
        tok = token()
        repos = fetch_repos(tok)
        data = build(repos, fetch_pages_urls(tok, repos),
                     json.loads(REGISTRY.read_text(encoding="utf-8")), route_map())
        n_priv = sum(1 for i in data["items"] if i["private"])
        summary = f"{len(data['items'])} 筆（GitHub {len(repos)} 個倉庫，其中私有 {n_priv}；名冊 {sum(1 for i in data['items'] if i['inRegistry'])} 站）"
        if a.dry_run:
            print("dry-run：" + summary)
            return 0
        if not (REPO_DIR / ".git").is_dir():
            print("找不到本機 all-works 倉庫，先建好：" + str(REPO_DIR))
            return 1
        out = REPO_DIR / "data.json"
        # generated 時間只在內容真的變動時才更新，避免每次觸發都產生一筆沒意義的 commit
        old = {}
        if out.exists():
            try:
                old = json.loads(out.read_text(encoding="utf-8"))
            except ValueError:
                old = {}
        data["generated"] = old.get("generated", "") if old.get("items") == data["items"] else \
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(summary)
        if not a.no_push:
            print(publish(tok, a.reason))
    return 0


if __name__ == "__main__":
    sys.exit(main())
