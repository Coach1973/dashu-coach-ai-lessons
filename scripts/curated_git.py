#!/usr/bin/env python3
"""策展網站（event.bymyway.com/curated/<slug>/）的 GitHub 版控。2026-09-30 教練交辦。

目的：每個策展網站都有一份 GitHub，聯想／宏碁的 Claude 桌面版貼上網址就能 clone 下來改、
在本機先看效果再 push。網站本身仍由這台 Mac 的 Flask 直接讀本機檔案服務。

用法：
  curated_git.py ensure <slug>   建／補 GitHub repo；本機有未存檔的修改就 commit＋push
  curated_git.py ensure-all      registry 裡每個站各跑一次 ensure
  curated_git.py sync <slug>     把 GitHub 最新版（例如聯想剛推上去的）拉到本機，網站跟著換新
  curated_git.py hook <slug>     替這個站的 GitHub 掛推送通知（推上去就自動 sync，2026-10-10）
  curated_git.py hook-all        registry 每個站都掛；SITE_SYNC 舊站用 hook-repo <GitHub repo 名>
  curated_git.py hook-repo <名>  替任意一個 Coach1973/<名> 掛推送通知
"""
from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
GITHUB_REPOS_DIR = Path("/Users/bymyway/github_repos")
REGISTRY_PATH = WORKSPACE / "event-signup" / "curated_sites_registry.json"
LOG_PATH = WORKSPACE / "distill" / "curated_git.log"
OWNER = "Coach1973"
WEBHOOK_URL = "https://event.bymyway.com/hooks/github-site"
ENV_PATH = WORKSPACE / "event-signup" / ".env"
GIT = ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com"]
_ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/Users/bymyway/.local/bin:{os.environ.get('PATH', '')}"}

DEFAULT_GITIGNORE = """*.bak*
.DS_Store
*.db
*.sqlite
*.sqlite3
.env
.env.*
*.pem
*.key
"""


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")
    print(msg)


def run(cmd: list, cwd: Path, check: bool = True, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=_ENV, check=check, timeout=timeout, capture_output=True, text=True)


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def site_dir(slug: str) -> Path:
    if slug not in {s["slug"] for s in load_registry().get("sites", [])}:
        raise RuntimeError(f"「{slug}」不在策展網站名單裡")
    d = GITHUB_REPOS_DIR / slug
    if not d.is_dir():
        raise RuntimeError(f"本機找不到資料夾 {d}")
    return d


def record_repo(slug: str, repo: str) -> None:
    reg = load_registry()
    for s in reg.get("sites", []):
        if s["slug"] == slug and s.get("repo") != repo:
            s["repo"] = repo
            REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
            return


def is_dirty(d: Path) -> bool:
    return bool(run(["git", "status", "--porcelain"], d).stdout.strip())


def current_branch(d: Path) -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"], d).stdout.strip()


def origin_repo_name(d: Path) -> str | None:
    """回傳 origin 指向的 repo 名稱；網址裡夾帶登入金鑰的順手改成乾淨網址（登入交給 git 的憑證管理）。"""
    r = run(["git", "remote", "get-url", "origin"], d, check=False)
    if r.returncode != 0:
        return None
    url = r.stdout.strip()
    name = url.rstrip("/").split("/")[-1].removesuffix(".git")
    if "@github.com" in url:
        run(["git", "remote", "set-url", "origin", f"https://github.com/{OWNER}/{name}.git"], d)
        log(f"🔒 {d.name}：origin 網址夾帶登入金鑰，已改成乾淨網址")
    return name


def github_repo_exists(name: str) -> bool:
    # gh 會跟著改名轉址（例如舊的 ai-story 已改名 _archived_ai-story），名稱要完全一樣才算存在
    r = run(["gh", "repo", "view", f"{OWNER}/{name}", "--json", "name", "-q", ".name"], WORKSPACE, check=False)
    return r.returncode == 0 and r.stdout.strip() == name


def create_private_repo(d: Path, slug: str) -> None:
    run(["gh", "repo", "create", f"{OWNER}/{slug}", "--private", "--source", str(d),
         "--remote", "origin", "--push"], d, timeout=600)


def pull_and_push(d: Path) -> None:
    branch = current_branch(d)
    run(["git", "fetch", "-q", "origin"], d)
    if run(["git", "rev-parse", "--verify", "-q", f"origin/{branch}"], d, check=False).returncode == 0:
        if run(GIT + ["rebase", "-q", f"origin/{branch}"], d, check=False).returncode != 0:
            run(["git", "rebase", "--abort"], d, check=False)
            raise RuntimeError("本機修改跟 GitHub 上的修改改到同一段，沒辦法自動合併，需要軍師人工處理")
    run(["git", "push", "-q", "-u", "origin", f"HEAD:{branch}"], d)


def save_local_changes(d: Path, message: str) -> None:
    if is_dirty(d):
        run(GIT + ["add", "-A"], d)
        run(GIT + ["commit", "-q", "-m", message], d)
        log(f"💾 {d.name}：本機有未存檔的修改，已存檔")


def webhook_secret() -> str:
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("GITHUB_WEBHOOK_SECRET="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("event-signup/.env 沒有 GITHUB_WEBHOOK_SECRET")


def ensure_hook(repo_name: str) -> str:
    """GitHub 推送 → event.bymyway.com/hooks/github-site → Mac 自動 sync。已掛過就不重掛（只更新暗號）。"""
    r = run(["gh", "api", f"repos/{OWNER}/{repo_name}/hooks", "-q", f'.[] | select(.config.url=="{WEBHOOK_URL}") | .id'],
            WORKSPACE, check=False)
    if r.returncode != 0:
        raise RuntimeError(f"讀不到 {repo_name} 的通知設定：{r.stderr.strip()[-200:]}")
    config = ["-f", f"config[url]={WEBHOOK_URL}", "-f", "config[content_type]=json",
              "-f", f"config[secret]={webhook_secret()}", "-f", "config[insecure_ssl]=0"]
    hook_id = r.stdout.strip().splitlines()[0] if r.stdout.strip() else ""
    # check=False＋自己丟錯：失敗訊息不能帶出指令全文（裡面有暗號），以免寫進會上傳的記錄檔
    if hook_id:
        r = run(["gh", "api", "-X", "PATCH", f"repos/{OWNER}/{repo_name}/hooks/{hook_id}", *config, "-F", "active=true"],
                WORKSPACE, check=False)
        if r.returncode != 0:
            raise RuntimeError(f"{repo_name} 通知更新失敗：{r.stderr.strip()[-200:]}")
        return "已掛過"
    r = run(["gh", "api", "-X", "POST", f"repos/{OWNER}/{repo_name}/hooks", "-f", "name=web", "-f", "events[]=push",
             "-F", "active=true", *config], WORKSPACE, check=False)
    if r.returncode != 0:
        raise RuntimeError(f"{repo_name} 掛通知失敗：{r.stderr.strip()[-200:]}")
    log(f"🔔 {repo_name}：已掛 GitHub 推送通知")
    return "新掛上"


def ensure_repo(slug: str) -> str:
    d = site_dir(slug)
    if not (d / ".git").is_dir():
        if github_repo_exists(slug):
            # 可能是跟策展無關、剛好同名的專案，自動接上去會蓋到別人的東西，寧可停下來
            raise RuntimeError(f"GitHub 上已經有同名的 {OWNER}/{slug}，為了不蓋到別的專案沒有自動連接，需要軍師確認")
        if not (d / ".gitignore").exists():
            (d / ".gitignore").write_text(DEFAULT_GITIGNORE, encoding="utf-8")
        run(["git", "init", "-q", "-b", "main"], d)
        run(GIT + ["add", "-A"], d)
        run(GIT + ["commit", "-q", "-m", "上架版本（自動建立 GitHub 版控）"], d)
        create_private_repo(d, slug)
        log(f"🆕 {slug}：已建立私有 GitHub repo 並推上去")
        name = slug
    else:
        name = origin_repo_name(d)
        if name is None:
            if github_repo_exists(slug):
                raise RuntimeError(f"本機有版控但沒有連到 GitHub，而 GitHub 上已有同名 {OWNER}/{slug}，需要軍師確認")
            create_private_repo(d, slug)
            log(f"🆕 {slug}：本機原有版控，已補建私有 GitHub repo")
            name = slug
        save_local_changes(d, "Mac本機修改自動存檔")
        pull_and_push(d)
    record_repo(slug, f"{OWNER}/{name}")
    ensure_hook(name)
    return f"https://github.com/{OWNER}/{name}"


def sync(slug: str) -> str:
    d = site_dir(slug)
    with open(d / ".git" / "curated_sync.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        before = run(["git", "rev-parse", "--short", "HEAD"], d).stdout.strip()
        save_local_changes(d, "Mac本機修改自動存檔（同步前）")
        pull_and_push(d)
        after = run(["git", "rev-parse", "--short", "HEAD"], d).stdout.strip()
    log(f"🔄 {slug}：同步完成 {before} → {after}")
    return after


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "ensure-all":
        failed = []
        for s in load_registry().get("sites", []):
            try:
                print(f"{s['slug']}: {ensure_repo(s['slug'])}")
            except Exception as e:  # noqa: BLE001
                failed.append(s["slug"])
                log(f"❌ {s['slug']}：{e}")
        print(f"完成，失敗 {len(failed)} 個：{failed}")
        sys.exit(1 if failed else 0)
    if cmd == "hook-all":
        failed = []
        for s in load_registry().get("sites", []):
            name = (s.get("repo") or f"{OWNER}/{s['slug']}").split("/")[-1]
            d = GITHUB_REPOS_DIR / s["slug"]
            if not (d / ".git").is_dir() or origin_repo_name(d) is None:
                continue  # GitHub 上還沒建 repo 的站，ensure 建好時會自己掛
            try:
                print(f"{s['slug']}: {ensure_hook(name)}")
            except Exception as e:  # noqa: BLE001
                failed.append(s["slug"])
                log(f"❌ hook {s['slug']}：{e}")
        print(f"完成，失敗 {len(failed)} 個：{failed}")
        sys.exit(1 if failed else 0)
    if len(sys.argv) == 3 and cmd in ("hook-repo", "hook"):
        try:
            name = sys.argv[2] if cmd == "hook-repo" else (origin_repo_name(site_dir(sys.argv[2])) or sys.argv[2])
            print(ensure_hook(name))
        except Exception as e:  # noqa: BLE001
            log(f"❌ {cmd} {sys.argv[2]}：{e}")
            sys.exit(1)
        return
    if len(sys.argv) != 3 or cmd not in ("ensure", "sync"):
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[2]
    try:
        print(ensure_repo(slug) if cmd == "ensure" else sync(slug))
    except Exception as e:  # noqa: BLE001
        log(f"❌ {cmd} {slug}：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
