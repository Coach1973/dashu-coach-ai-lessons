#!/bin/bash
# Hook：UserPromptSubmit（Mac 終端機版）
# 用途：每次教練講話時掃 cross-agent/inbox/mac/，有新信主動報告
# 設計：有信才注入，沒信靜默退出（不干擾正常對話）
# 對應：教練 2026-06-26 0:17 親口「以後跨機統一路徑，叫他們自己去讀」
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
INBOX="$WORKSPACE/cross-agent/inbox/mac"

# 先 git pull 確保本地最新（節流：5 分鐘內不重複 pull）
PULL_LOCK="${TMPDIR:-/tmp}/inbox_git_pull.lock"
NEED_PULL=true
if [[ -f "$PULL_LOCK" ]]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$PULL_LOCK" 2>/dev/null || echo 0) ))
    [[ $LOCK_AGE -lt 300 ]] && NEED_PULL=false
fi
if $NEED_PULL && [[ -d "$WORKSPACE/.git" ]]; then
    git -C "$WORKSPACE" pull --quiet 2>/dev/null || true
    touch "$PULL_LOCK"
fi

[[ ! -d "$INBOX" ]] && exit 0

# 只列 .md 檔，按時間倒序
NEW_LETTERS=$(ls -t "$INBOX"/*.md 2>/dev/null)
[[ -z "$NEW_LETTERS" ]] && exit 0

COUNT=$(printf '%s\n' "$NEW_LETTERS" | wc -l | tr -d ' ')

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📬 跨機軍師信箱（Mac 收件匣有 ${COUNT} 封未讀）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

未讀清單（新→舊）：
$(printf '%s\n' "$NEW_LETTERS" | while read -r f; do printf '  📨 %s\n' "$(basename "$f")"; done)

🎯 教練口令字典：
  • 「讀信」「跨機有信」「{機器}有事交代」 → Mac 軍師自動讀取最新封並執行/回報
  • 處理完務必 mv 到 cross-agent/outbox/$(date +%Y-%m)/ 歸檔，不留在 inbox

📁 完整路徑：$INBOX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

exit 0
