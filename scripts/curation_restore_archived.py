#!/usr/bin/env python3
"""把被舊版「下架」(delete_curated_site) 搬走的策展網站救回來（2026-10-07 教練交辦）。

舊版下架一次做四件事：名冊移除、本機資料夾搬進 _archive_curation_test_folders/<slug>-deleted-<時間>、
GitHub repo 改名 _archived_<slug> 並關 Pages、策展中心卡片拔掉。這支腳本把它們反過來：
  1. 本機：把封存資料夾「複製」回 ~/github_repos/<slug>（封存區那份保留不刪）
  2. GitHub：repo 改回原名、重新開 Pages
  3. 名冊：補回條目（優先用 workspace git 歷史裡的原條目，找不到就從網站內容重建）
  4. 策展中心卡片：從下架那個 commit 的前一版取回，存進名冊 card_html，狀態設成「已下架・網站還在」
     （教練在後台按「重新上架」才會放回首頁；救回來不等於公開展示）

用法：python3 scripts/curation_restore_archived.py <slug> [--card-commit <tainan-shangquan 的下架 commit>] [--dry-run]
沒有 --card-commit 代表這個網站原本就沒有卡片（例如大樹作品），救回後只是普通網站。
"""
import argparse
import glob
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

GITHUB_REPOS = Path("/Users/bymyway/github_repos")
ARCHIVE_DIR = GITHUB_REPOS / "_archive_curation_test_folders"
SHANGQUAN = GITHUB_REPOS / "tainan-shangquan"
WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
REGISTRY = WORKSPACE / "event-signup" / "curated_sites_registry.json"
OWNER = "Coach1973"


def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} → {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def old_registry_entry(slug):
    """從 workspace git 歷史找這個 slug 當年的名冊條目（新→舊找，找到第一個）。"""
    needle = f'"slug": "{slug}"'
    rel = "event-signup/curated_sites_registry.json"
    for c in run(["git", "log", "--format=%H", "-S" + needle, "--", rel], cwd=WORKSPACE, check=False).split():
        try:
            data = json.loads(run(["git", "show", f"{c}:{rel}"], cwd=WORKSPACE))
        except Exception:  # noqa: BLE001
            continue
        for s in data.get("sites", []):
            if s.get("slug") == slug:
                return s
    return None


def rebuild_entry(slug, dest):
    text = (dest / "index.html").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    title = html.unescape(re.sub(r"\s+", " ", m.group(1)).strip()) if m else slug
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', text, re.S)
    first = run(["git", "log", "--reverse", "--format=%ad", "--date=format:%Y-%m-%d %H:%M"], cwd=dest, check=False).splitlines()
    return {
        "slug": slug, "title": title, "description": html.unescape(d.group(1)).strip() if d else "",
        "category": "", "uploaded_at": first[0] if first else "",
        "event_url": f"https://event.bymyway.com/curated/{slug}/",
        "github_pages_url": f"https://{OWNER.lower()}.github.io/{slug}/", "source_package": "", "status": "live",
    }


def card_from_commit(commit, title, slug):
    """下架 commit 的前一版首頁裡，找出這個網站的卡片原文（含前一行說明註解）。"""
    old = run(["git", "show", f"{commit}^:index.html"], cwd=SHANGQUAN)
    pat = re.compile(r"(?:[ \t]*<!--[^\n]*-->\n)?[ \t]*<article\b[^>]*>.*?</article>\n?", re.S)
    key = re.sub(r"\s+", "", title)[:10]
    for m in pat.finditer(old):
        block = m.group(0)
        if key and key in re.sub(r"\s+", "", block) or f"/{slug}/" in block:
            return block
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--card-commit")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    slug = a.slug

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if any(s["slug"] == slug for s in reg["sites"]):
        sys.exit(f"名冊裡已經有 {slug}，不需要救")
    cands = sorted(glob.glob(str(ARCHIVE_DIR / f"{slug}-deleted-*")))
    if not cands:
        sys.exit(f"封存區找不到 {slug}-deleted-*")
    src = Path(cands[-1])
    dest = GITHUB_REPOS / slug
    if dest.exists():
        sys.exit(f"{dest} 已經存在，為了不覆蓋任何東西，停止")
    print(f"來源：{src.name}\n目的：{dest}")
    if a.dry_run:
        print("（dry-run，到此為止）")
        return

    shutil.copytree(src, dest, symlinks=True)  # 複製，不是搬移：封存區那份保留
    print("① 本機資料夾已複製回來")

    note = []
    try:
        run(["gh", "repo", "rename", slug, "-R", f"{OWNER}/_archived_{slug}", "--yes"])
        branch = run(["gh", "api", f"repos/{OWNER}/{slug}", "--jq", ".default_branch"]).strip() or "main"
        run(["gh", "api", "-X", "POST", f"repos/{OWNER}/{slug}/pages", "-f", f"source[branch]={branch}", "-f", "source[path]=/"], check=False)
        print(f"② GitHub repo 已改回 {slug}，Pages 已重新開啟（分支 {branch}）")
    except Exception as e:  # noqa: BLE001
        note.append(f"GitHub 還原失敗：{e}")
        print("②", note[-1])

    entry = old_registry_entry(slug) or rebuild_entry(slug, dest)
    entry["status"] = "live"
    entry["event_url"] = f"https://event.bymyway.com/curated/{slug}/"
    if a.card_commit:
        card = card_from_commit(a.card_commit, entry.get("title", ""), slug)
        if card:
            tag = re.search(r'<span class="tag">(.*?)</span>', card)
            if tag and not entry.get("category"):
                entry["category"] = tag.group(1)
            entry["listed"] = False
            entry["card_html"] = card
            entry["unlisted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            print("③ 策展中心卡片已取回，狀態＝已下架・網站還在（按「重新上架」才會放回首頁）")
        else:
            note.append("找不到卡片原文，需要人工補")
            print("③", note[-1])
    else:
        print("③ 沒有指定卡片 commit：當作普通網站救回（沒有卡片）")
    reg["sites"].append(entry)
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"④ 名冊已補回：{entry.get('title')}")
    if note:
        print("⚠️ 需要注意：", "；".join(note))


if __name__ == "__main__":
    main()
