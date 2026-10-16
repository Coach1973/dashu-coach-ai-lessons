#!/bin/bash
# 背景排程（openclaw_cron_daemon.sh）某個工作失敗的「當下」被呼叫——事件觸發，不輪詢。
# 同一個工作 30 分鐘內失敗滿 3 次 → 電報通知教練（同一工作 1 小時最多一則）＋寫信給 Mac 軍師（開工時會自動讀到）。
# 起因 2026-10-16：15:00～19:05 背景工作失敗 91 次沒有任何人知道，接力棒鏡像因此停了 4 小時。
# 本程式自己出任何錯都安靜結束（exit 0），絕不影響排程。
# 測試：CRON_FAIL_DRYRUN=1 CRON_FAIL_LOG=<假紀錄檔> CRON_FAIL_INBOX=<暫存資料夾> bash cron_fail_notify.sh <工作名>
JOB="$1"; [ -n "$JOB" ] || exit 0
LOG="${CRON_FAIL_LOG:-/tmp/openclaw_cron_daemon.log}"
WS=/Users/bymyway/.openclaw/workspace
INBOX="${CRON_FAIL_INBOX:-$WS/cross-agent/inbox/mac}"
N=$(python3 - "$JOB" "$LOG" <<'PY' 2>/dev/null
import sys, time, datetime
job, log = sys.argv[1], sys.argv[2]
since = datetime.datetime.fromtimestamp(time.time() - 30 * 60).strftime("%Y-%m-%d %H:%M:%S")
n = 0
for line in open(log, errors="ignore").read().splitlines()[-2000:]:
    if f"⚠️ {job} 失敗" in line and line[1:20] >= since:
        n += 1
print(n)
PY
)
[ "${N:-0}" -ge 3 ] 2>/dev/null || exit 0
NOW=$(date '+%m/%d %H:%M')
MSG="🛠️ Mac 上的自動工作「${JOB}」30 分鐘內失敗了 ${N} 次（${NOW} 台灣時間）。已寫信給軍師，軍師下次開工會先處理；網站本身另有守門員顧著。"
STAMP="/tmp/cron_fail_letter_${JOB//[^A-Za-z0-9_]/_}"
if [ -n "$CRON_FAIL_DRYRUN" ]; then echo "[演練] 會發電報：$MSG"; else
  bash "$WS/scripts/notify_coach.sh" "$MSG" 3600 "cron_fail_${JOB}" >/dev/null 2>&1
fi
if [ -n "$CRON_FAIL_DRYRUN" ] || [ ! -e "$STAMP" ] || [ $(( $(date +%s) - $(stat -f %m "$STAMP") )) -gt 3600 ]; then
  [ -z "$CRON_FAIL_DRYRUN" ] && touch "$STAMP"
  mkdir -p "$INBOX" 2>/dev/null
  F="$INBOX/$(date +%Y%m%d-%H%M)_cron-daemon-to-mac_${JOB//[^A-Za-z0-9_]/_}-failing.md"
  {
    echo "# 背景工作「${JOB}」一直失敗"
    echo
    echo "> **寄件人**：Mac 背景排程（openclaw_cron_daemon.sh，自動寄出）"
    echo "> **收件人**：Mac 軍師"
    echo "> **時間**：${NOW} 台灣時間"
    echo
    echo "30 分鐘內失敗 ${N} 次，已發電報讓教練知道。請先跑 \`python3 scripts/system_health_check.py\` 看是不是整個系統的問題（10/16 就是工作資料夾被換掉才全部失敗），再查這個工作自己的紀錄。"
    echo
    echo "## 最近的失敗紀錄"
    echo '```'
    grep "⚠️ ${JOB} 失敗" "$LOG" 2>/dev/null | tail -5
    echo '```'
  } > "$F" 2>/dev/null
  [ -n "$CRON_FAIL_DRYRUN" ] && echo "[演練] 寫了信：$F"
fi
exit 0
