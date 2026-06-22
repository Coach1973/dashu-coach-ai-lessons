#!/bin/bash
# Hook: Stop（Mac 端）
# 用途: Session 結束時自動把接力棒/記憶/心跳 push 到 GitHub，
#       讓 Windows 軍師下次「開工」git pull 就拿到 Mac 最新進度，教練不當搬運工。
# 設計:
#   - 只 push 同步相關檔（接力棒、心跳、memory/、knowledges/）
#   - 沒實質變動就不 commit（避免 git noise）
#   - 10 秒鎖：同 session 重複 Stop 不重跑
#   - 失敗靜默退出，不阻塞 hook 鏈
set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
LOG="$WS/HEARTBEAT.md"
LOCK="/tmp/session_end_push.lock"

# 10 秒內重複觸發直接退出（Stop hook 可能連續觸發）
if [[ -f "$LOCK" ]]; then
  AGE=$(( $(date +%s) - $(stat -f %m "$LOCK" 2>/dev/null || echo 0) ))
  [[ "$AGE" -lt 10 ]] && exit 0
fi
touch "$LOCK"

cd "$WS" 2>/dev/null || exit 0

# 只追蹤同步相關檔（避免 push noise，例如 node_modules、log）
SYNC_PATHS=(
  "JUNSHI_HANDOFF_LATEST.md"
  "CLAUDE.md"
  "HEARTBEAT.md"
  "memory/"
  "knowledges/"
  "試金石/"
  "scripts/"
)

# 過濾出真的有變動的路徑
DIRTY=()
for p in "${SYNC_PATHS[@]}"; do
  if [[ -e "$p" ]] && ! git diff --quiet -- "$p" 2>/dev/null; then
    DIRTY+=("$p")
  fi
  # untracked 新檔也算
  if [[ -e "$p" ]] && git ls-files --others --exclude-standard -- "$p" 2>/dev/null | grep -q .; then
    DIRTY+=("$p")
  fi
done

# 去重
DIRTY=($(printf '%s\n' "${DIRTY[@]}" | sort -u))

if [[ ${#DIRTY[@]} -eq 0 ]]; then
  exit 0
fi

# 加入 stage
git add "${DIRTY[@]}" 2>/dev/null

# 確認 stage 有東西才 commit
if git diff --cached --quiet 2>/dev/null; then
  exit 0
fi

STAMP=$(date '+%Y-%m-%d %H:%M')
COMMIT_MSG="[Mac] session-end 自動同步 $STAMP"

PUSH_RESULT="❓ unknown"
if git commit -m "$COMMIT_MSG" >/dev/null 2>&1; then
  COMMIT_HASH=$(git rev-parse --short HEAD)
  if git push origin main >/dev/null 2>&1; then
    PUSH_RESULT="✅ pushed $COMMIT_HASH"
  else
    PUSH_RESULT="⚠️ commit $COMMIT_HASH 本機留底，push 失敗（離線/網路）"
  fi
else
  PUSH_RESULT="ℹ️ 沒實質變動"
fi

# 寫心跳留證
{
  echo ""
  echo "## 🚀 Session-End 雲端同步 $STAMP（Mac）"
  echo "- $PUSH_RESULT"
  echo "- 同步路徑：${DIRTY[*]}"
} >> "$LOG" 2>/dev/null || true

exit 0
