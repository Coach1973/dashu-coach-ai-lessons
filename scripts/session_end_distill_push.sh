#!/bin/bash
# Hook：Stop（session 結束時觸發）
# 用途：對齊教練 2026-06-30 新規則（ACER 軍師信 12:13）——
#       「session 結束時自動蒸餾推雲端，不靠定時 cron」
# 作者：Mac 軍師 Sonnet 4.6（2026-06-30 12:16）
# 與 cron */30 並存：cron 是兜底，本 hook 是即時。重複跑無害（內部已 dedup）。
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
DISTILL="$WORKSPACE/scripts/run_terminal_distill.sh"
LOG="/tmp/session_end_distill.log"

# 節流：同 session 結束 5 分鐘內不重複跑（避免快速來回對話時暴打）
LOCK="${TMPDIR:-/tmp}/session_end_distill.lock"
if [[ -f "$LOCK" ]]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$LOCK" 2>/dev/null || echo 0) ))
    [[ $AGE -lt 300 ]] && exit 0
fi
touch "$LOCK"

[[ ! -x "$DISTILL" ]] && exit 0

# 背景跑，不阻塞 Claude 退場
nohup bash "$DISTILL" >> "$LOG" 2>&1 &

exit 0
