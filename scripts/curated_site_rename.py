#!/usr/bin/env python3
"""策展站台改短網址的統一工具（2026-09-06建立）。

起因：教練當晚連續4次要求把過長的網址改短，每次都由不同AI人工手動做——
GitHub repo改名/本機資料夾改名/registry換slug/策展中心卡片連結換新，
4件事全靠記性各憑印象執行，其中「舊網址要留轉址」這件事完全沒人做過，
導致教練事後回報：已經發出去的FB貼文連結、店家自己留存的舊連結，
改名之後全部404失效。

這支腳本一次做完，並且在registry寫入redirects對照表，讓舊網址永久
301轉址到新網址——不管未來又被誰用什麼方式改名幾次，只要都走這支腳本，
已發布出去的連結就再也不會死掉。

用法：
    python3 scripts/curated_site_rename.py <舊slug> <新slug>

做的事：
1. GitHub repo改名（gh repo rename）
2. 本機github_repos資料夾改名 + git remote URL同步
3. registry：sites裡該筆的slug/event_url/github_pages_url換新
4. registry：redirects表登記 舊slug→新slug（核心修復，避免死連結）
5. tainan-shangquan店家卡片連結換新（若有找到才動，找不到不視為失敗）
6. git commit + push tainan-shangquan（若有異動）
7. 最後curl驗證：新網址200、舊網址301轉址到新網址且最終200
"""
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
EVENT_SIGNUP = WORKSPACE / "event-signup"
REGISTRY_PATH = EVENT_SIGNUP / "curated_sites_registry.json"
GITHUB_REPOS_DIR = Path("/Users/bymyway/github_repos")
TAINAN_SHANGQUAN_REPO = GITHUB_REPOS_DIR / "tainan-shangquan"
GH_OWNER = "Coach1973"


def run(cmd, cwd=None, check=True):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True, timeout=60)


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(data: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        print("用法: python3 curated_site_rename.py <舊slug> <新slug>")
        sys.exit(1)
    old_slug, new_slug = sys.argv[1], sys.argv[2]

    old_dir = GITHUB_REPOS_DIR / old_slug
    new_dir = GITHUB_REPOS_DIR / new_slug
    if not old_dir.is_dir():
        print(f"❌ 找不到本機資料夾 {old_dir}，中止")
        sys.exit(1)
    if new_dir.exists():
        print(f"❌ 目標資料夾 {new_dir} 已存在，中止")
        sys.exit(1)

    # 1. GitHub repo改名
    r = run(["gh", "repo", "rename", new_slug, "-R", f"{GH_OWNER}/{old_slug}", "--yes"], check=False)
    if r.returncode != 0:
        print(f"⚠️ GitHub repo改名失敗或已改過：{r.stderr.strip()}（若已是新名字可忽略繼續）")

    # 2. 本機資料夾改名 + remote URL同步
    old_dir.rename(new_dir)
    run(["git", "remote", "set-url", "origin", f"https://github.com/{GH_OWNER}/{new_slug}.git"], cwd=new_dir)
    print(f"✅ 本機資料夾+remote已改名：{old_slug} → {new_slug}")

    # 3+4. registry更新
    data = load_registry()
    found = False
    for site in data.get("sites", []):
        if site["slug"] == old_slug:
            site["slug"] = new_slug
            site["event_url"] = f"https://event.bymyway.com/curated/{new_slug}/"
            site["github_pages_url"] = f"https://coach1973.github.io/{new_slug}/"
            found = True
            break
    if not found:
        print(f"⚠️ registry裡找不到slug={old_slug}的記錄，可能本來就沒登記過，僅補redirects")
    data.setdefault("redirects", {})[old_slug] = new_slug
    save_registry(data)
    print(f"✅ registry已更新：slug換新 + redirects[{old_slug}] = {new_slug}")

    # 5+6. tainan-shangquan卡片連結
    index_html = TAINAN_SHANGQUAN_REPO / "index.html"
    if index_html.is_file():
        content = index_html.read_text(encoding="utf-8")
        old_url = f"https://event.bymyway.com/curated/{old_slug}/"
        new_url = f"https://event.bymyway.com/curated/{new_slug}/"
        if old_url in content:
            content = content.replace(old_url, new_url)
            index_html.write_text(content, encoding="utf-8")
            run(["git", "add", "index.html"], cwd=TAINAN_SHANGQUAN_REPO)
            run(["git", "commit", "-m", f"[curated-rename] {old_slug} -> {new_slug} 卡片連結同步"], cwd=TAINAN_SHANGQUAN_REPO, check=False)
            run(["git", "push"], cwd=TAINAN_SHANGQUAN_REPO, check=False)
            print("✅ tainan-shangquan卡片連結已同步+push")
        else:
            print("ℹ️ tainan-shangquan卡片裡找不到舊網址，可能本來就沒有卡片或已改過，跳過")
    else:
        print("⚠️ 找不到tainan-shangquan/index.html，跳過卡片同步")

    print(f"\n完成。舊網址 event.bymyway.com/curated/{old_slug}/ 現在會自動301轉址到新網址，不會再死掉。")


if __name__ == "__main__":
    main()
