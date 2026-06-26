#!/bin/bash
# Hook: UserPromptSubmit
# 用途：開工時自動掃描 git log 最近 24 小時其他機器的 commit，
#       防止跨機交接任務漏接（不依賴寄信，系統自動抓）
# 起因：2026-06-26 聯想交接講座行銷頁給 ACER，但沒寄信，
#       ACER 和 Mac 都漏接，教練自己提醒 = 搬運工（守則 #12 違規）
# 對應 Windows 版: scan_cross_machine_commits.ps1
set -uo pipefail

# 同 session 只跑一次
MARKER_DIR="${TMPDIR:-/tmp}/cross_machine_markers"
mkdir -p "$MARKER_DIR"

# 讀 stdin JSON 取 session_id
SESSION_ID=""
if read -t 1 RAW_INPUT 2>/dev/null; then
    SESSION_ID=$(echo "$RAW_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null || echo "")
fi
MARKER="$MARKER_DIR/scanned_${SESSION_ID}"
[ -f "$MARKER" ] && exit 0

WORKSPACE="$HOME/.openclaw/workspace"
[ -d "$WORKSPACE" ] || exit 0

cd "$WORKSPACE" || exit 0

# 判斷自己是誰（Mac）
MY_PREFIX="[Mac]"

# 掃最近 24 小時的 commit，排除 auto-backup 和自己的
COMMITS=$(git log --all --oneline --since="24 hours ago" --format="%h|%ai|%s" 2>/dev/null \
    | grep -v "auto-backup" \
    | grep -v "auto:" \
    | grep -vF "$MY_PREFIX" \
    | grep -v "Merge branch" \
    | grep -iv "Co-Authored-By" \
    | head -15)

[ -z "$COMMITS" ] && { touch "$MARKER"; exit 0; }

# 過濾出有實質內容的（交接/任務/建立/修復/上線 等關鍵動作）
RELEVANT=""
COUNT=0
while IFS='|' read -r hash datetime msg; do
    # 跳過空行
    [ -z "$hash" ] && continue
    COUNT=$((COUNT + 1))
    # 轉台灣時間顯示
    tw_time=$(TZ='Asia/Taipei' date -j -f "%Y-%m-%d %H:%M:%S %z" "$datetime" "+%m/%d %H:%M" 2>/dev/null || echo "$datetime")
    RELEVANT="${RELEVANT}  • ${tw_time} \`${hash}\` ${msg}
"
done <<< "$COMMITS"

[ "$COUNT" -eq 0 ] && { touch "$MARKER"; exit 0; }

cat <<INJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 跨機動態（最近 24 小時其他機器的 ${COUNT} 筆 commit）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${RELEVANT}
⚠️ 如有「交接」「handoff」相關 commit，請主動讀取並回報教練。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INJECT

touch "$MARKER"
exit 0
