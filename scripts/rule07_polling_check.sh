#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：偵測 AI 這一輪輸出裡是否「提議/設計」了定時輪詢機制
#       （每X分鐘檢查、cron定時掃描等），命中就強制先說明
#       為什麼不能用事件驅動，逼自己先想過再動手。
# 起因（2026-07-02 教練親口）：同一場對話裡連續 3 次設計成輪詢
#       （心跳燈塔、蒸餾提煉建議、陌生用戶自動開通第一版），
#       教練點破：commit/記憶檔只是被動記錄，不會自動阻止重犯，
#       要做成真正會擋的機關才有意義。
# 對齊守則#07「不要在同一個地方跌倒兩次」+ 案例32/36。
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

# 輪詢設計語言偵測（提議/建立定時檢查機制的用詞）
POLLING_PATTERNS=(
  "每.*分鐘.*檢查"
  "每.*分鐘.*看一次"
  "每.*分鐘.*跑一次"
  "每隔.*分鐘"
  "每隔.*秒"
  "定時.*檢查"
  "定時.*輪詢"
  "cron.*檢查"
  "cron.*輪詢"
  "背景.*每.*分鐘"
  "輪詢.*機制"
)

# 白名單：討論/反省/引用過去案例時常見的詞，出現就跳過該行
WHITELIST_PATTERN='守則|案例|教訓|之前|已經|過去|糾正|檢討|反省|不要再|避免再|不應該|不能再|同一個地方|同一場對話|連續.*次|拆除|改成事件|改用事件|事件驅動|事件觸發|拿掉|廢除|退役|取消|移除輪詢'

HITS=""
while IFS= read -r LINE; do
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  for PATTERN in "${POLLING_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qE "$PATTERN"; then
      HITS+="  • 偵測到疑似輪詢設計：「$(printf '%s' "$LINE" | cut -c1-60)...」"$'\n'
      break
    fi
  done
done <<< "$LAST_TEXT"

[[ -z "$HITS" ]] && exit 0

# 命中輪詢語言 → 檢查整段有沒有明確提到「已考慮過事件驅動並說明為何非用輪詢不可」
HAS_JUSTIFICATION=""
if printf '%s' "$LAST_TEXT" | grep -qE '事件驅動不可行|沒有現成的事件掛鉤|系統不支援事件觸發|只能用輪詢是因為'; then
  HAS_JUSTIFICATION="yes"
fi

if [[ -z "$HAS_JUSTIFICATION" ]]; then
  HITS=$(printf '%s' "$HITS" | sort -u)

  LOG="$HOME/.openclaw/workspace/distill/rule07_polling_violations.log"
  mkdir -p "$(dirname "$LOG")"
  {
    printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
      "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
    printf '%s' "$HITS"
    printf '%s\n' '---'
  } >> "$LOG"

  {
    printf '\n🚨 守則#07 輪詢設計偵測（系統 grep，deterministic check）\n'
    printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
    printf '這一輪回覆裡出現「定時/每X分鐘檢查」的輪詢設計：\n'
    printf '%s' "$HITS"
    printf '\n📜 守則#07 原文（特助心法.md）：\n'
    printf '  「不要在同一個地方跌倒兩次，就是最大的成功。」\n'
    printf '  「不可能不犯錯，但不要一直犯同樣的錯。」\n\n'
    printf '2026-07-02 教練已對同一個錯誤糾正 3 次（心跳燈塔/蒸餾提煉/自動開通），\n'
    printf '這是第 4 次以後的自動攔截，不能再靠記性。\n\n'
    printf '✅ 停下來自問：\n'
    printf '  1. 這件事有沒有現成的事件掛鉤（hook/signal/webhook/restart-policy）可以直接觸發？\n'
    printf '  2. 如果真的沒有，在回覆裡明確寫出「事件驅動不可行，因為XXX」再繼續。\n'
    printf '  3. 如果只是在討論/引用過去案例，把這句話改寫得更明確是在「回顧」不是「提議」。\n\n'
    printf '違規記錄已寫入：%s\n' "$LOG"
    printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  } >&2

  exit 2
fi

exit 0
