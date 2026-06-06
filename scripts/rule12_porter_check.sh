#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：偵測 AI 上一輪輸出是否出現「叫教練搬運」句型（違反守則#12）
#       命中 → exit 2 強制 Claude 重做，並輸出修正指引
# 設計理念（Meta Automation，2026-06-06 教練親定）：
#       不靠模型自覺，用 grep 確定性檢查；error message 必須 actionable
#       影片要點：「不要只是說錯了，要告訴他應該怎麼做」
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-06-06
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

# 已經循環過一次了，本次放行（避免無限迴圈）
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# 抓取最後一條 assistant 訊息的 text content
# Claude Code transcript 是 jsonl，每行一個 event
LAST_TEXT=$(tail -100 "$TRANSCRIPT_PATH" | \
  /usr/bin/jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text' 2>/dev/null | \
  tail -200)

[[ -z "$LAST_TEXT" ]] && exit 0

# 禁止句型清單（搬運工句型）
PATTERNS=(
  "請你複製"
  "請你貼"
  "請您複製"
  "請您貼"
  "請您回傳"
  "請你回傳"
  "麻煩你貼"
  "麻煩您貼"
  "麻煩你複製"
  "麻煩您複製"
  "麻煩你回傳"
  "麻煩貼一下"
  "麻煩複製"
  "請貼一下"
  "請複製一下"
  "請幫我貼"
  "請幫我複製"
  "可以複製貼上"
  "請把這段貼"
  "請把結果貼"
  "請把輸出貼"
  "請把這段複製"
)

# 白名單關鍵字：含這些字代表該行是在「討論/列舉/解釋」守則，不是真的叫教練搬運
# 例如：「禁止句型清單包含『請你貼』」應該跳過
WHITELIST_PATTERN='禁止|不要|不應|不准|不會|不可|違反|列舉|引用|以下|清單|句型|守則|原文|案例|範例|示例|例如|諸如|偵測到|命中|示範|black\?list|black list|偵測|抓到|grep|hook|測試'

HITS=""
# 逐行檢查（按換行符拆分）
while IFS= read -r LINE; do
  # 該行含白名單關鍵字 → 跳過（是討論/列舉，不是真叫搬運）
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  # 去掉中文引號「...」內的內容（引號內是舉例/引用，不是真的叫搬運）
  CLEAN_LINE=$(printf '%s' "$LINE" | sed 's/「[^」]*」//g')
  # 檢查清理後的行有無禁止句型
  for PATTERN in "${PATTERNS[@]}"; do
    if printf '%s' "$CLEAN_LINE" | grep -qF "$PATTERN"; then
      HITS+="  • 偵測到「${PATTERN}」"$'\n'
    fi
  done
done <<< "$LAST_TEXT"

# 去重
HITS=$(printf '%s' "$HITS" | sort -u)
[[ -n "$HITS" ]] && HITS+=$'\n'

# 沒命中 → 放行
[[ -z "$HITS" ]] && exit 0

# 命中 → 記錄違規 + 阻止停止 + 注入修正指引
LOG="$HOME/.openclaw/workspace/distill/rule12_violations.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
    "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
  printf '%s' "$HITS"
  printf '%s\n' '---'
} >> "$LOG"

# stderr 輸出會在 exit 2 時被 Claude 看到，作為「重做指引」
{
  printf '\n🚨 守則#12 違規偵測（系統 grep，deterministic check）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '剛才回覆出現「叫教練搬運」的禁止句型：\n'
  printf '%s' "$HITS"
  printf '\n📜 守則#12 原文（特助心法.md）：\n'
  printf '  「永遠不要叫用戶幫你複製這個、貼上那個、再回傳這個。」\n'
  printf '  「只要是任何 AI 能夠做到的事，你都不應該說你做不到。」\n\n'
  printf '✅ 正確做法（請立刻重做）：\n'
  printf '  1. 自己用 Bash/Read/Grep 工具拿到需要的資訊\n'
  printf '  2. 如果真的拿不到（例如教練手機上的截圖），明確說「我拿不到 X，需要您 Y」\n'
  printf '     而不是用「請貼一下/麻煩複製」這種搬運工句型\n'
  printf '  3. 重新生成回覆，去掉所有禁止句型\n\n'
  printf '違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

# exit 2 = 阻止 Claude 停止，stderr 內容會被當作「修正指引」注入給 Claude
exit 2
