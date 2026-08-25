#!/bin/bash
# Hook: UserPromptSubmit
# 用途：把「當下台灣時間」+「永遠台灣時間鐵律」注入 context
# 教練 2026-06-09 親罵：UTC/Z 時間講了 N 次違反，從此寫死系統
# 軍師建立 2026-06-09 14:32 台灣時間
#
# 2026-08-12 全面體檢第1項改動（節流，教練核准）：
#   原版每一則訊息都把同一段 5 行鐵律全文重貼一次——一場 40 輪的對話
#   等於同一段文字貼 40 遍。而「現在幾點」session_time_context.sh
#   每輪本來就會報，這裡再報一次是純重複。
#   改成：鐵律全文只在「開場第一輪」與「之後每 20 輪」貼一次
#   （20 輪這個節點跟 session_length_hook.sh / periodic_xinfa_reload_hook.sh
#   同一套 band 設計——長對話 context 被壓縮後還是會被重新提醒，
#   不是貼一次就放生）。非節點輪次完全靜默，時鐘交給 session_time_context.sh。
set -uo pipefail

RELOAD_EVERY=20

INPUT=$(cat 2>/dev/null || true)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
[[ -z "$SESSION_ID" || "$SESSION_ID" == "null" ]] && SESSION_ID="nosession"
SAFE_SESSION=$(printf '%s' "$SESSION_ID" | tr -c 'a-zA-Z0-9_-' '_')
COUNTER="${TMPDIR:-/tmp}/inject_tw_time_${SAFE_SESSION}.count"

N=0
[[ -f "$COUNTER" ]] && N=$(cat "$COUNTER" 2>/dev/null || echo 0)
[[ "$N" =~ ^[0-9]+$ ]] || N=0
N=$((N + 1))
echo "$N" > "$COUNTER" 2>/dev/null || true

# 順手清掉三天前的舊計數檔
find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'inject_tw_time_*.count' -mtime +3 -delete 2>/dev/null || true

# 不是節點輪次 → 靜默（時鐘由 session_time_context.sh 每輪提供）
if [[ "$N" -ne 1 && $((N % RELOAD_EVERY)) -ne 0 ]]; then
  exit 0
fi

# 強制 Asia/Taipei，不管系統時區是什麼
TW_NOW=$(TZ='Asia/Taipei' date '+%Y-%m-%d %A %H:%M:%S')

cat <<INJECT
🕐 **當下台灣時間：${TW_NOW}（GMT+8）**

🔴 **時間鐵律（教練 2026-06-09 親罵後寫死，違反 = 守則 #07 同處跌倒）**：
- 跟教練講時間 → **永遠先換算成台灣時間**（Asia/Taipei，UTC+8）
- 看到 ISO 字串「\`2026-06-09T06:25:36.752Z\`」→ Z = UTC → **+8 變 14:25:36（下午 2:25）**
- 禁止口語講「06:24」「06:25」等 Z 時間——這是 UTC，不是台灣時間
- 對教練講「上午 6 點半」「下午 2 點半」用白話，不用 24 小時制更好
INJECT

exit 0
