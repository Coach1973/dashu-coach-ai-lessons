#!/bin/bash
# notify_coach.sh — 自動化腳本要通知教練時的統一出口
#
# 建立原因（2026-08-25 賈維斯全系統體檢）：
#   體檢發現多支自動化「有跑、有結果，但只寫進 /tmp/*.log 或桌面 reminder.txt」，
#   教練根本看不到——機器忠實跑了好幾個月，成果全部倒進沒人開的檔案。
#   從此凡是「教練需要知道」的自動化輸出，一律走這支，不再寫死檔案當通知。
#
# 用法：
#   notify_coach.sh "訊息內容"
#   notify_coach.sh "訊息內容" <節流秒數> <節流鍵>   # 同一個鍵在秒數內只送一次
#
# 設計原則（教練 2026-08-05 親口：不影響工作就別吵我，浪費注意力）：
#   呼叫端自己要先判斷「這件事真的需要教練知道嗎」，本腳本只負責送達，不做內容判斷。
#   送達失敗一定留下紀錄，絕不 silent fail（體檢抓到的最貴 bug 形態）。

set -uo pipefail

COACH_CHAT_ID="6124913915"
OPENCLAW="/opt/homebrew/bin/openclaw"
LOG="/Users/bymyway/Library/Logs/openclaw/notify_coach.log"

MSG="${1:-}"
THROTTLE_SEC="${2:-0}"
THROTTLE_KEY="${3:-}"

mkdir -p "$(dirname "$LOG")"
ts() { date '+%Y-%m-%d %H:%M:%S'; }

if [[ -z "$MSG" ]]; then
    echo "[$(ts)] ❌ 呼叫錯誤：訊息內容是空的" >> "$LOG"
    exit 1
fi

# 節流：同一個鍵在指定秒數內只送一次，避免反覆打擾
# ⚠️ lock 只在「真的送出成功」之後才建立——送失敗還鎖住的話，
#    整個節流視窗內都不會再重試，等於一次失敗換來長時間靜音。
LOCK=""
if [[ -n "$THROTTLE_KEY" && "$THROTTLE_SEC" -gt 0 ]]; then
    LOCK="/tmp/.notify_coach_${THROTTLE_KEY}.lock"
    if [[ -f "$LOCK" ]]; then
        AGE=$(( $(date +%s) - $(stat -f %m "$LOCK") ))
        if (( AGE < THROTTLE_SEC )); then
            echo "[$(ts)] ⏭️ 節流跳過（key=$THROTTLE_KEY, ${AGE}s < ${THROTTLE_SEC}s）" >> "$LOG"
            exit 0
        fi
    fi
fi

# ⚠️ 不能用 `openclaw message send`：
#    ① 系統同時接了 telegram 與 line，不給 --channel 會直接報 Channel is required
#    ② 就算給了 --channel，CLI 從 cron/腳本這種外部環境跑時讀不到 bot token
#       （token 在 gateway 進程裡，不在環境變數），會報 Telegram bot token missing。
#    所以改成從 openclaw.json 讀 token 直接打 Telegram API，不依賴 CLI 的執行環境。
BOT_TOKEN=$(python3 -c "
import json
try:
    d = json.load(open('/Users/bymyway/.openclaw/openclaw.json'))
    print(d['channels']['telegram']['accounts']['bot_main']['botToken'])
except Exception:
    print('')
" 2>/dev/null)

if [[ -z "$BOT_TOKEN" ]]; then
    echo "[$(ts)] ❌ 讀不到 bot_main 的 Telegram token，訊息沒送出：$(echo "$MSG" | head -1)" >> "$LOG"
    exit 1
fi

# 2026-08-25 教練親口要求：這種訊息是程式自動發的、不是小龍蝦(AI)決定要講的，
# 但共用同一個Telegram bot帳號送出，教練分不出來哪句是AI講的、哪句是系統插播的
# （下午context輪數bug事件的直接教訓）。統一加標籤，教練一眼就能分辨來源。
LABELED_MSG="🤖【賈維斯自動通知】
${MSG}"

# Telegram 單則上限 4096 字，超過整則退回（2026-09-20 管家週報就這樣沒送到），按行切成多則送
RC=0
SENT=0
OUT=""
while IFS= read -r -d '' PART; do
    OUT=$(curl -s --max-time 20 \
        -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${COACH_CHAT_ID}" \
        --data-urlencode "text=${PART}" 2>&1)
    if echo "$OUT" | grep -q '"ok":true'; then
        SENT=$((SENT + 1))
    else
        RC=1
        break
    fi
done < <(printf '%s' "$LABELED_MSG" | python3 -c '
import sys
text, limit = sys.stdin.read(), 3500
parts, cur = [], ""
for line in text.split("\n"):
    while len(line) > limit:
        if cur:
            parts.append(cur)
            cur = ""
        parts.append(line[:limit])
        line = line[limit:]
    if cur and len(cur) + len(line) + 1 > limit:
        parts.append(cur)
        cur = line
    else:
        cur = line if not cur else cur + "\n" + line
if cur:
    parts.append(cur)
n = len(parts)
for i, p in enumerate(parts, 1):
    sys.stdout.write((f"({i}/{n})\n" if n > 1 else "") + p + "\0")
')
(( SENT == 0 )) && RC=1

if (( RC == 0 )); then
    echo "[$(ts)] ✅ 已送達教練：$(echo "$MSG" | head -1)" >> "$LOG"
    [[ -n "$LOCK" ]] && touch "$LOCK"
else
    echo "[$(ts)] ❌ 送出失敗（rc=$RC）：$(echo "$MSG" | head -1)" >> "$LOG"
    echo "[$(ts)]    openclaw 回應：$OUT" >> "$LOG"
fi

exit $RC
