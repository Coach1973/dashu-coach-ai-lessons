#!/opt/homebrew/bin/python3
"""
safe_git.py — 防止 git lock 衝突的 git commit/push 包裝
用途：避免多個 cron 同時 commit 時 index.lock 衝突
用法：safe_git.py <workspace_path> "<commit message>" [files...]

鎖機制：
  - 用 fcntl.flock 實作阻塞式檔案鎖（最多等 30 秒）
  - 拿不到鎖就放棄這輪 commit
  - 拿到的話：git add → 檢查 staged → git commit → git push（全程持有鎖）
  - push 失敗不影響 commit（本機已留 commit，下次推即可）

建立：2026-06-20（從 flock bash 版改寫，macOS 無 flock，改用 fcntl）
"""
import fcntl
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

LOCK_FILE = "/tmp/safe_git_workspace.lock"
LOCK_WAIT_SEC = 30


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[safe_git {ts}] {msg}", flush=True)


def acquire_lock() -> int | None:
    """阻塞式 flock。成功回傳 fd，失敗回傳 None。"""
    fd = open(LOCK_FILE, "w")
    deadline = time.time() + LOCK_WAIT_SEC
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd.fileno()
        except BlockingIOError:
            if time.time() >= deadline:
                fd.close()
                return None
            time.sleep(0.5)


def run(cmd: list[str]) -> tuple[int, str, str]:
    """執行 shell 命令，回傳 (returncode, stdout, stderr)。"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    if len(sys.argv) < 3:
        log("用法：safe_git.py <workspace> <commit msg> [files...]")
        return 1

    ws = Path(sys.argv[1]).resolve()
    msg = sys.argv[2]
    files = sys.argv[3:] if len(sys.argv) > 3 else []

    if not ws.is_dir():
        log(f"workspace 不存在：{ws}")
        return 1

    os.chdir(ws)

    # 1. 搶鎖
    fd = acquire_lock()
    if fd is None:
        log(f"{LOCK_WAIT_SEC} 秒內搶不到 git 鎖（其他 cron 還在 commit），本輪跳過")
        return 0
    log(f"拿到 git 鎖（fd={fd}），開始 commit")

    try:
        # 2. 檢查是否有變化
        if files:
            rc, _, _ = run(["git", "diff", "--quiet", "--", *files])
            has_changes_in_tracked = rc != 0
            _, untracked, _ = run(["git", "ls-files", "--others", "--exclude-standard", "--", *files])
            has_untracked = bool(untracked)
            if not has_changes_in_tracked and not has_untracked:
                log(f"無變化：{files}（不 commit）")
                return 0
            rc, out, err = run(["git", "add", "--", *files])
            if out:
                log(out)
            if err:
                log(f"git add 警告：{err}")
        else:
            run(["git", "add", "-A"])

        # 3. 檢查 staged
        rc, _, _ = run(["git", "diff", "--cached", "--quiet"])
        if rc == 0:
            log("staged 後無變化（不 commit）")
            return 0

        # 4. commit（重試 3 次）
        commit_ok = False
        for attempt in range(1, 4):
            rc, _, err = run(["git", "commit", "-m", msg])
            if rc == 0:
                commit_ok = True
                break
            log(f"commit 第 {attempt} 次失敗：{err[:200]}")
            time.sleep(2)

        if not commit_ok:
            log("commit 連 3 次失敗")
            return 1

        rc, commit_hash, _ = run(["git", "rev-parse", "--short", "HEAD"])
        log(f"commit {commit_hash or 'unknown'}")

        # 5. push（網路失敗不影響 commit）
        rc, _, err = run(["git", "push", "origin", "main"])
        if rc == 0:
            log("push 成功")
        else:
            log(f"push 失敗（commit {commit_hash} 已留本機，下次輪到再推）")

        return 0

    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
