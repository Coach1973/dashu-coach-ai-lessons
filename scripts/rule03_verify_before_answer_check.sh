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
  "瞎猜"
  "亂猜"
  "自行判斷"
  "自己判斷.{0,4}(而)?沒.{0,2}問"
)

# 肯定式誤判語言（2026-07-02 教練親抓：沒有hedge詞，用肯定語氣宣稱「發現問題」，
# 卻沒先查現有記憶檔/SOP——government-grow誤判「無鎖=漏洞」就是這種樣貌）
CONFIDENT_CLAIM_PATTERNS=(
  "之前沒發現的"
  "發現.{0,4}漏洞"
  "這是.{0,4}漏洞"
  "完全沒有.{0,4}(攔截|防護|保護)"
)

# 白名單：誠實說不知道（守則#15正確行為）、討論過去案例、已明確查證過
WHITELIST_PATTERN='不確定|需要查證|案例[0-9三十二四五六七八九十]|教訓|檢討|反省|已驗證|已確認|測試通過|查證後|實測|跑過.*確認|讀取.*確認'

GUESS_HITS=""
CONFIDENT_HITS=""
while IFS= read -r LINE; do
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  for PATTERN in "${GUESS_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qE "$PATTERN"; then
      GUESS_HITS+="  • 偵測到疑似未查證就交付：「$(printf '%s' "$LINE" | cut -c1-60)...」"$'\n'
      break
    fi
  done
  for PATTERN in "${CONFIDENT_CLAIM_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qE "$PATTERN"; then
      CONFIDENT_HITS+="  • 偵測到疑似肯定式誤判（沒hedge詞卻宣稱發現問題）：「$(printf '%s' "$LINE" | cut -c1-60)...」"$'\n'
      break
    fi
  done
done <<< "$LAST_TEXT"

# 肯定式誤判額外檢查：這輪對話有沒有查過記憶檔/SOP的證據（Grep/Read命中memory或特助心法/SOP）
if [[ -n "$CONFIDENT_HITS" && -n "$TRANSCRIPT_PATH" && -f "$TRANSCRIPT_PATH" ]]; then
  HAS_MEMORY_CHECK=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json
path = sys.argv[1]
try:
    with open(path, encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]
except Exception:
    print("unknown"); sys.exit(0)
recent = lines[-40:]
found = False
for line in recent:
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get('type') != 'assistant':
        continue
    for c in evt.get('message', {}).get('content', []):
        if not isinstance(c, dict) or c.get('type') != 'tool_use':
            continue
        name = c.get('name', '')
        tin = c.get('input', {})
        target = str(tin.get('file_path', '')) + str(tin.get('pattern', '')) + str(tin.get('path', ''))
        if name in ('Grep', 'Read') and ('memory' in target or 'SOP' in target or '特助心法' in target or '試金石' in target):
            found = True
print("yes" if found else "no")
PYEOF
)
  # 已經查過記憶檔 → 這則肯定式宣稱是有根據的，不算違規
  [[ "$HAS_MEMORY_CHECK" == "yes" ]] && CONFIDENT_HITS=""
fi

HITS="${GUESS_HITS}${CONFIDENT_HITS}"
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
