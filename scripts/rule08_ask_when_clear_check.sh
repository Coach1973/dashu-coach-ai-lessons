#!/bin/bash
# ⚠️ 【功能已合併，本檔不再單獨註冊】2026-08-25 賈維斯體檢標註
# 這支的邏輯已於 2026-08-12 併入 scripts/stop_rules_master.py（12 支 Stop hook 合成單一總管，
# 避免每支各自重讀同一份 transcript，實測 14MB 檔 1.111 秒 → 0.066 秒）。
# 所以它「沒註冊進 settings.json」是正確狀態，不是漏裝。
# 原本的「# Hook：Stop」宣告改成下面這行，避免 audit_claude_hooks_registered.sh 每次都誤報。
# 已合併：Stop（實際執行者為 stop_rules_master.py）
# 用途：偵測 AI 這一輪輸出裡是否在「方向已經清楚」的情況下，
#       還多此一舉問教練「要不要/是否需要」——命中就提醒自問方向是否真的不明。
# 起因（2026-07-02 教練親口）：查過去32天真實對話紀錄，
#       守則#08「花時間討論就是為了執行」被違反至少6次
#       （06-08教練直接說「你已經找到方案還等我拍板？」、
#       06-23教練清晨6點已在工作卻被AI多問、
#       06-30「討論就是為了執行，不是嗎」、
#       07-01連續兩次「現在就做，為什麼要等」）——
#       跟案例37的HTML問題同樣頻率。
# 對齊守則#08 + E06（方向分流鐵律：方向清楚直接做，方向模糊才問）。
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈。
# 刻意設計成 Warn 級（不阻擋回覆）——因為「危險/不可逆操作前確認」
# 和「方向真的模糊時發問」都是合理行為，不能被這條誤殺（案例34教訓）。
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# 2026-08-12 體檢第2項：transcript 解析改走 lib/stop_ctx.sh 共用快取
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
CTX=$(bash /Users/bymyway/.openclaw/workspace/scripts/lib/stop_ctx.sh "$TRANSCRIPT_PATH" "$SESSION_ID" 2>/dev/null) || exit 0
LAST_TEXT=$(printf '%s' "$CTX" | /usr/bin/jq -r '.last_assistant_text // ""' 2>/dev/null)

[[ -z "$LAST_TEXT" ]] && exit 0

# 多此一舉徵詢式語言（方向可能已經清楚，卻還在問要不要做）
ASK_PATTERNS=(
  "要不要我"
  "是否需要我"
  "您希望我"
  "需要我.*嗎"
  "要我.*嗎"
  "要不要.*進行"
  "是否.*繼續"
)

# 白名單：不可逆/危險操作前的確認是合理的（E11五道閘門保護範圍）、
# 方向真的模糊需要問（守則#16好問句工具箱）、已在AskUserQuestion工具內問過、
# 討論過去案例
WHITELIST_PATTERN='不可逆|刪除|危險|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|方向不明|方向模糊|不確定您想要|多種.*(方式|方案|解讀)'

HITS=""
while IFS= read -r LINE; do
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  for PATTERN in "${ASK_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qE "$PATTERN"; then
      HITS+="  • 偵測到疑似多此一舉的徵詢：「$(printf '%s' "$LINE" | cut -c1-60)...」"$'\n'
      break
    fi
  done
done <<< "$LAST_TEXT"

[[ -z "$HITS" ]] && exit 0

LOG="$HOME/.openclaw/workspace/distill/rule08_ask_violations.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
    "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
  printf '%s' "$HITS"
  printf '%s\n' '---'
} >> "$LOG"

{
  printf '\n🌱 守則#08 多此一舉徵詢偵測（系統 grep，Warn 級提醒，非強制擋死）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '這一輪回覆裡出現「要不要我/是否需要」這類徵詢語言：\n'
  printf '%s' "$HITS"
  printf '\n📜 守則#08 原文：\n'
  printf '  「除非這個決定是不可逆的，否則就應該立即去執行。」\n\n'
  printf '2026-07-02 教練查過去32天對話紀錄：這條守則已被違反至少6次，\n'
  printf '跟案例37的HTML問題同樣頻率，這是機關化提醒，不是又一次空談。\n\n'
  printf '✅ 停下來自問（執行細則N2：什麼時候可以問教練）：\n'
  printf '  1. 這件事教練的方向真的模糊嗎？還是其實已經說清楚了，我在多問？\n'
  printf '  2. 這個決定不可逆嗎？不可逆才需要問，可逆的話直接做。\n'
  printf '  3. 如果方向真的不清楚 → 保留這句問話，這是對的。\n'
  printf '  4. 如果方向其實清楚 → 刪掉徵詢語言，直接改成「我要做 X」的陳述句。\n\n'
  printf '本次為提醒，不阻擋回覆送出；違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 0
