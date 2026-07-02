#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：偵測 AI 這一輪輸出裡是否用「猜測性語言」交付答案/結果，
#       卻沒有明確做過查證動作——命中就強制先自問有沒有真的驗證過。
# 起因（2026-07-02 教練親口）：查過去32天真實對話紀錄，
#       守則#03「思考就是問問題」被違反至少6次（06-02瞎編文章沒讀歷史、
#       06-08圖片消失重複犯錯、06-17承認瞎猜、06-26沒確認時間、
#       06-30承認「亂猜」），跟案例37的HTML問題同樣頻率——
#       教練點破「你只查案例庫筆數，不是查真實對話紀錄，這樣不精準」。
# 對齊守則#03 + #15（誠實說不知道 vs 亂猜）。
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

LAST_TEXT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json

path = sys.argv[1]
try:
    with open(path) as f:
        lines = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)

for line in reversed(lines):
    try:
        evt = json.loads(line)
        if evt.get('type') == 'assistant':
            contents = evt.get('message', {}).get('content', [])
            texts = [c.get('text', '') for c in contents if c.get('type') == 'text']
            print('\n'.join(texts))
            break
    except Exception:
        continue
PYEOF
)

[[ -z "$LAST_TEXT" ]] && exit 0

# 猜測性語言（交付答案/結果時用的不確定用詞，卻沒有明確查證動作）
GUESS_PATTERNS=(
  "應該是"
  "應該可以"
  "應該沒問題"
  "大概是"
  "我猜"
  "猜測"
  "推測應該"
  "可能是因為"
)

# 白名單：誠實說不知道（守則#15正確行為）、討論過去案例、已明確查證過
WHITELIST_PATTERN='不確定|需要查證|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|已驗證|已確認|測試通過|查證後|實測|跑過.*確認|讀取.*確認'

HITS=""
while IFS= read -r LINE; do
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  for PATTERN in "${GUESS_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qE "$PATTERN"; then
      HITS+="  • 偵測到疑似未查證就交付：「$(printf '%s' "$LINE" | cut -c1-60)...」"$'\n'
      break
    fi
  done
done <<< "$LAST_TEXT"

[[ -z "$HITS" ]] && exit 0

LOG="$HOME/.openclaw/workspace/distill/rule03_verify_violations.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
    "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
  printf '%s' "$HITS"
  printf '%s\n' '---'
} >> "$LOG"

{
  printf '\n🌱 守則#03 未查證交付偵測（系統 grep，Warn 級提醒，非強制擋死）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '這一輪回覆裡出現「應該是/大概/我猜」這類猜測語言：\n'
  printf '%s' "$HITS"
  printf '\n📜 守則#03 原文：\n'
  printf '  「在回答用戶之前，一定要先經過自我驗證再給出答案。」\n\n'
  printf '2026-07-02 教練查過去32天對話紀錄：這條守則已被違反至少6次，\n'
  printf '跟案例37的HTML問題同樣頻率，這是機關化提醒，不是又一次空談。\n\n'
  printf '✅ 停下來自問：\n'
  printf '  1. 這句話的內容，我剛才真的用工具查證過嗎？還是憑印象講的？\n'
  printf '  2. 如果沒查證 → 現在補查，或誠實說「不確定，需要查證」（守則#15）。\n'
  printf '  3. 如果已經查證過 → 把查證過程講出來（怎麼查的、結果是什麼），\n'
  printf '     不要只寫結論。\n\n'
  printf '本次為提醒，不阻擋回覆送出；違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 0
