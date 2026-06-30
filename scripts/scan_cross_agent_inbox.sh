#!/bin/bash
# Hook：UserPromptSubmit（Mac 終端機版）v2 — 2026-06-30 升級
# 用途：每次教練講話時掃 cross-agent/inbox/mac/，有新信主動報告
# v2 新增：偵測「讀信/開工/讀取信件/{機器}有事」等暗號 → 自動 cat 全文進對話
# 設計：有信才注入，沒信靜默退出（不干擾正常對話）
# 對應：教練 2026-06-26 0:17「跨機統一路徑」+ 2026-06-30 12:04「一句口令自動讀內文」
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
INBOX="$WORKSPACE/cross-agent/inbox/mac"

# 讀 stdin JSON 拿 prompt（hook 機制）— 用來偵測暗號
INPUT=$(cat 2>/dev/null || echo '{}')
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null || echo "")
# 暗號偵測：任一命中 → 自動 cat 信件全文
TRIGGER_FULL=false
if printf '%s' "$PROMPT" | grep -qE "讀信|讀取信件|跨機有信|有事交代|有事要|去讀|開工|信箱|inbox"; then
    TRIGGER_FULL=true
fi

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
  • 「讀信」「讀取信件」「跨機有信」「{機器}有事交代」「開工」 → 自動 cat 全文進對話
  • 處理完務必 mv 到 cross-agent/outbox/$(date +%Y-%m)/ 歸檔

📁 完整路徑：$INBOX
EOF

# v2 暗號觸發 → 自動 cat 所有未讀全文
if $TRIGGER_FULL; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📖 暗號偵測 → 自動展開全部信件內文"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf '%s\n' "$NEW_LETTERS" | while read -r f; do
        echo ""
        echo "════════════════════════════════════════"
        echo "📨 $(basename "$f")"
        echo "════════════════════════════════════════"
        cat "$f"
        echo ""
    done
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ 讀完後請：(1) 執行任務 (2) 回信對方 inbox (3) mv 到 outbox/$(date +%Y-%m)/"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

exit 0
