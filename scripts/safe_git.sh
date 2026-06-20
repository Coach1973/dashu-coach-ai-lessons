#!/bin/bash
# safe_git.sh — 防止 git lock 衝突的 git commit/push 包裝
# 用途：避免多個 cron 同時 commit 時 index.lock 衝突（曾經 96% 失敗率）
# 用法：safe_git.sh <workspace_path> "<commit message>" [files...]
# 範例：safe_git.sh /Users/bymyway/.openclaw/workspace "auto: 備份" terminal-notes/raw_sessions
#
# 鎖機制（macOS 相容，不用 flock）：
#   - 用 Python fcntl.flock 實作阻塞式檔案鎖（最多等 30 秒）
#   - 拿不到鎖就放棄這輪 commit（讓下一輪接手）
#   - 拿到的話：git add → 檢查 staged → git commit → git push
#   - push 失敗不影響 commit（本機已留 commit，下次推即可）
# 軍師建立 2026-06-20（從 flock 版改寫，macOS 無 flock）

set -uo pipefail

WS="${1:?用法：safe_git.sh <workspace_path> <commit msg> [files...]}"
MSG="${2:?需要 commit message}"
shift 2
LOCK_FILE="/tmp/safe_git_workspace.lock"
LOG_PREFIX="[safe_git $(date '+%H:%M:%S')]"

cd "$WS" || { echo "$LOG_PREFIX ❌ workspace 不存在：$WS" >&2; exit 1; }

# 阻塞式 flock（用 Python fcntl，最多等 30 秒）
SAFE_GIT_LOCK_RC=$(/opt/homebrew/bin/python3 - "$LOCK_FILE" 30 <<'PYEOF'
import fcntl, sys, time, os
lock_path, max_wait = sys.argv[1], int(sys.argv[2])
fd = open(lock_path, 'w')
deadline = time.time() + max_wait
while True:
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # 拿到鎖！把 fd 編號傳回 shell（exit 時 fd 關閉會自動釋放鎖）
        print(fd.fileno())
        sys.exit(0)
    except BlockingIOError:
        if time.time() >= deadline:
            print("-1")
            sys.exit(1)
        time.sleep(0.5)
PYEOF
)

if [ "$SAFE_GIT_LOCK_RC" = "-1" ]; then
    echo "$LOG_PREFIX ⚠️ 30 秒內搶不到 git 鎖（其他 cron 還在 commit），本輪跳過"
    exit 0
fi
echo "$LOG_PREFIX 🔒 拿到 git 鎖，開始 commit"

# 檢查是否有實際變更需要 add（沒變化就提早結束，不生無意義 commit）
if [ $# -gt 0 ]; then
    if git diff --quiet -- "$@" 2>/dev/null \
       && [ -z "$(git ls-files --others --exclude-standard -- "$@" 2>/dev/null)" ]; then
        echo "$LOG_PREFIX ℹ️ 無變化：$*（不 commit）"
        exit 0
    fi
    git add -- "$@" 2>&1 | sed "s/^/$LOG_PREFIX /"
else
    git add -A 2>&1 | sed "s/^/$LOG_PREFIX /"
fi

# 檢查 staged 後是否真的有東西
if git diff --cached --quiet; then
    echo "$LOG_PREFIX ℹ️ staged 後無變化（不 commit）"
    exit 0
fi

# commit（重試 3 次保險）
COMMIT_OK=0
for i in 1 2 3; do
    if git commit -m "$MSG" >/dev/null 2>&1; then
        COMMIT_OK=1
        break
    fi
    sleep 2
done

if [ "$COMMIT_OK" -eq 0 ]; then
    echo "$LOG_PREFIX ❌ commit 連 3 次失敗" >&2
    exit 1
fi

COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "$LOG_PREFIX ✅ commit $COMMIT_HASH"

# push（網路失敗不影響 commit）
if git push origin main >/dev/null 2>&1; then
    echo "$LOG_PREFIX ✅ push 成功"
else
    echo "$LOG_PREFIX ⚠️ push 失敗（commit $COMMIT_HASH 已留本機，下次輪到再推）"
fi
