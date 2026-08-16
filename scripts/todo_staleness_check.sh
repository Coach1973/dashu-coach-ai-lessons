#!/bin/bash
# todo_staleness_check.sh — 賈維斯計畫 Phase 3
# 用途：讀JUNSHI_HANDOFF_LATEST.md開頭的「現在真正待辦」總表，找出：
#   ①卡住超過7天還沒解決的項目（🔒/⏳/⚠️狀態）
#   ②任務描述裡提到的日期，落在未來3天內的項目（快到期提醒）
# 全部正常（沒有卡太久、沒有快到期）時安靜輸出空字串，不吵教練
# 建立：2026-08-16 賈維斯計畫Phase3
set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
HANDOFF="$WS/JUNSHI_HANDOFF_LATEST.md"
STATE_FILE="$WS/state/todo_staleness.json"
TMP_ROWS=$(mktemp)
trap 'rm -f "$TMP_ROWS"' EXIT

[ -f "$HANDOFF" ] || exit 0
mkdir -p "$WS/state"
[ -f "$STATE_FILE" ] || echo '{}' > "$STATE_FILE"

# 只取「現在真正待辦」表格區塊：從表頭列開始，到下一個 ## 標題為止
awk '
  /^\| 優先/ { intable=1; next }
  /^\|---/ { next }
  intable && /^#/ { exit }
  intable && /^\|/ { print }
' "$HANDOFF" > "$TMP_ROWS"

python3 "$WS/scripts/todo_staleness_check.py" "$TMP_ROWS" "$STATE_FILE"
