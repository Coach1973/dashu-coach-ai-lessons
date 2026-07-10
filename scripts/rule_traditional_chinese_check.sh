#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：掃描這一輪最終回覆文字，偵測是否混入簡體字，命中 → exit 2 強制重新檢查並修正
# 設計理念：不靠模型自覺（今天同一場對話已經犯兩次，證明「自己小心」不可靠），用 grep 確定性檢查
# 對齊：全繁體中文鐵律（memory: feedback_chinese_only.md，試金石案例44）
# 觸發案例：2026-07-10 案例44——長篇技術回覆滑成簡體字，教練重話糾正；
#           同一場對話裡再犯第二次（額外收穫→额外收获等），教練：「非得要顯示簡體字是嗎？」
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-07-10（案例44同場二犯後）
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

RESULT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json

path = sys.argv[1]
try:
    with open(path) as f:
        lines = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)

last_assistant_text = ""
for i in range(len(lines) - 1, -1, -1):
    try:
        evt = json.loads(lines[i])
    except Exception:
        continue
    if evt.get('type') == 'assistant':
        msg = evt.get('message', {})
        content = msg.get('content')
        if isinstance(content, list):
            texts = [c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') == 'text']
            last_assistant_text = '\n'.join(texts)
        elif isinstance(content, str):
            last_assistant_text = content
        break

print(json.dumps({'last_assistant_text': last_assistant_text}))
PYEOF
)

[[ -z "$RESULT" ]] && exit 0
LAST_TEXT=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.last_assistant_text')
[[ -z "$LAST_TEXT" ]] && exit 0

# 簡體字專用字元表（僅列「簡體特有、不會出現在正常繁體文字」的高頻字，避免誤判）
SIMPLIFIED_CHARS='这|讲|们|读|时|间|触|设|帐|额|门|儿|发|开|关|报|华|归|图|网|页|数|应|术|处|战|显|复|备|环|层|阶|观|议|语|记|认|识|让|从|众|学|国|说|话|现|会|对|还|过|动|转|输|变|传|车|军|阵|队|员|团|独|电|视|频|络|该|种|样|专|习|亲|头|简|构|济|导|济|计|谁|难|临|尽|尝|双|书|终|绝|细|统|继|绍'

MATCHED=""
while IFS= read -r ch; do
  [[ -z "$ch" ]] && continue
  MATCHED="${MATCHED}${ch}、"
done < <(printf '%s' "$LAST_TEXT" | grep -oE "$SIMPLIFIED_CHARS" | sort -u)
MATCHED="${MATCHED%、}"

[[ -z "$MATCHED" ]] && exit 0

LOG="$HOME/.openclaw/workspace/distill/rule_traditional_chinese_violations.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] session=%s matched=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
    "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)" \
    "$MATCHED"
} >> "$LOG"

{
  printf '\n🈶🔒 繁體字鎖違規偵測（系統 grep，deterministic check）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '這一輪回覆裡偵測到疑似簡體字：%s\n\n' "$MATCHED"
  printf '📜 全繁體中文鐵律（教練唯一指定，試金石案例44 二犯，2026-07-10）：\n'
  printf '  「對話全程繁體中文，不夾簡體、不夾英文」\n\n'
  printf '✅ 正確做法（請立刻檢查並修正）：\n'
  printf '  1. 回頭逐字檢查剛才的回覆，把上面列出的每個字改成繁體對應字\n'
  printf '  2. 常見對照：这→這 讲→講 们→們 读→讀 时→時 间→間 设→設 额→額 发→發 开→開 关→關\n'
  printf '  3. 重新輸出乾淨的繁體版本給教練，不要只回覆這次有改就好，要整段重新確認過一遍\n\n'
  printf '違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 2
