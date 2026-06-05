#!/bin/bash
# openclaw_cron_daemon.sh — 永久背景跑，模擬 cron 行為
# 設計：minimax-m3 軍師，2026-06-05
# 起因：macOS cron scheduler 卡住（5 個原 cron job 停跑），sudo 重啟需互動密碼
#       → 改用 KeepAlive LaunchAgent + while 迴圈
# 觸發：LaunchAgent ai.openclaw.cron-daemon.plist 啟動
# 終止：launchctl bootout ai.openclaw.cron-daemon
# 設計：每分鐘醒來跑對應的腳本（依原 cron 排程邏輯）

WS="/Users/bymyway/.openclaw/workspace"
LOG="/tmp/openclaw_cron_daemon.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === openclaw_cron_daemon 啟動 ===" >> "$LOG"

LAST_HEARTBEAT_DAY=""

while true; do
    CURRENT_MIN=$(date '+%M')
    CURRENT_HOUR=$(date '+%H')
    CURRENT_DAY=$(date '+%d')
    TS=$(date '+%Y-%m-%d %H:%M:%S')

    # 每次迴圈都留一行心跳，證明 daemon 活著
    echo "[$TS] 心跳 :${CURRENT_MIN}" >> "$LOG"

    # 1. relay_poll: 每分鐘
    bash "$WS/scripts/run_relay_poll.sh" >> "$LOG" 2>&1 || echo "[$TS] ⚠️ relay_poll 失敗" >> "$LOG"

    # 2. split_memory: 10,40 (每小時 :10, :40，原 cron 設定)
    if [ "$CURRENT_MIN" = "10" ] || [ "$CURRENT_MIN" = "40" ]; then
        bash "$WS/scripts/split_memory.sh" >> "$LOG" 2>&1 || echo "[$TS] ⚠️ split_memory 失敗" >> "$LOG"
    fi

    # 3. distill_watchdog: */15 (:00, :15, :30, :45)
    if [ $((10#$CURRENT_MIN % 15)) -eq 0 ]; then
        bash "$WS/scripts/distill_watchdog.sh" >> "$LOG" 2>&1 || echo "[$TS] ⚠️ distill_watchdog 失敗" >> "$LOG"
    fi

    # 4. distill: 0 */2 (每 2 小時整點 0,2,4,6,8,10,12,14,16,18,20,22)
    if [ "$CURRENT_MIN" = "00" ] && [ $((10#$CURRENT_HOUR % 2)) -eq 0 ]; then
        bash "$WS/scripts/run_distill.sh" >> "$LOG" 2>&1 || echo "[$TS] ⚠️ run_distill 失敗" >> "$LOG"
    fi

    # 5. heartbeat_audit: 每天 23:50（用 LAST_HEARTBEAT_DAY 防止重複）
    if [ "$CURRENT_HOUR:$CURRENT_MIN" = "23:50" ] && [ "$LAST_HEARTBEAT_DAY" != "$CURRENT_DAY" ]; then
        bash "$WS/scripts/heartbeat_audit.sh" >> "$LOG" 2>&1 || echo "[$TS] ⚠️ heartbeat_audit 失敗" >> "$LOG"
        LAST_HEARTBEAT_DAY="$CURRENT_DAY"
    fi

    sleep 60
done
