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

    # 1. relay_poll: 已退役（2026-07-08 Fable5 稽核，教練核准）
    #    relay 傳話系統 2026-07-02 改用官方 sessions_send，此輪詢空轉一個 5/25 的過期佇列
    #    原行存檔：bash "$WS/scripts/run_relay_poll.sh"

    # 2. split_memory: 10,40 (每小時 :10, :40，原 cron 設定)
    if [ "$CURRENT_MIN" = "10" ] || [ "$CURRENT_MIN" = "40" ]; then
        bash "$WS/scripts/split_memory.sh" >> "$LOG" 2>&1 || { echo "[$TS] ⚠️ split_memory 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "split_memory" >/dev/null 2>&1; }  # 10/16：失敗當下通知
    fi

    # 3. distill_watchdog + VPS polling healthcheck: */15 (:00, :15, :30, :45)
    if [ $((10#$CURRENT_MIN % 15)) -eq 0 ]; then
        bash "$WS/scripts/distill_watchdog.sh" >> "$LOG" 2>&1 || { echo "[$TS] ⚠️ distill_watchdog 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "distill_watchdog" >/dev/null 2>&1; }  # 10/16：失敗當下通知
        # vps_polling_healthcheck: 已移除（2026-08-12 全面體檢，教練核准）
        #   重複原因：LaunchAgent ai.openclaw.vps-polling-healthcheck.plist 已經
        #   用 StartInterval=900（每 15 分鐘）跑同一支腳本，等於同一件事每 15 分鐘
        #   被做兩次。保留 LaunchAgent 版（有 RunAtLoad、開機即跑、不依賴本 daemon 存活），
        #   本處移除。腳本本身檔頭註解寫的觸發來源也是 launchd，不是這裡。
        #   原行存檔：bash "$WS/scripts/vps_polling_healthcheck.sh"
    fi

    # 4. distill: 已移交 openclaw cron「每2小時增量記憶蒸餾」單引擎（2026-07-08 Fable5 稽核，教練核准）
    #    此處與 openclaw cron、LaunchAgent distill-incremental 三引擎重複，只保留 openclaw cron 版（功能超集+有監控）
    #    原排程存檔：每 2 小時整點 bash "$WS/scripts/run_distill.sh"

    # 5. heartbeat_audit: 每天 23:50（用 LAST_HEARTBEAT_DAY 防止重複）
    if [ "$CURRENT_HOUR:$CURRENT_MIN" = "23:50" ] && [ "$LAST_HEARTBEAT_DAY" != "$CURRENT_DAY" ]; then
        bash "$WS/scripts/heartbeat_audit.sh" >> "$LOG" 2>&1 || { echo "[$TS] ⚠️ heartbeat_audit 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "heartbeat_audit" >/dev/null 2>&1; }  # 10/16：失敗當下通知
        LAST_HEARTBEAT_DAY="$CURRENT_DAY"
    fi

    # 6. backup_terminal: 每 15 分鐘複製檔案（資料安全不打折，維持原頻率）
    #    commit/push: 2026-08-12 全面體檢後改成「每小時整點」才做（教練核准）
    #    起因：原本每 15 分鐘就 commit 一次，活躍日一天產生 40~79 筆 auto commit
    #    （實測 8/8 是 79 筆 / 全部 92 筆），教練真正要看的人工紀錄被淹沒。
    #    分開處理的理由：檔案「複製到 raw_sessions/」才是備份本體，維持 15 分鐘不動；
    #    commit 只是把它同步上雲端，批次到整點做，最多延後 45 分鐘上雲，
    #    且 session 結束時 session_end_auto_push.sh 會立刻補推一次，不會真的漏。
    #    2026-06-20 從系統 crontab 接管：原 cron 與 sync_handoff 撞 lock 96% 失敗
    if [ $((10#$CURRENT_MIN % 15)) -eq 0 ]; then
        bash "$WS/scripts/backup_terminal_sessions.sh" >> /tmp/backup_terminal.log 2>&1 || { echo "[$TS] ⚠️ backup_terminal_sessions 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "backup_terminal_sessions" >/dev/null 2>&1; }  # 10/16：失敗當下通知
    fi
    if [ "$CURRENT_MIN" = "00" ]; then
        bash "$WS/scripts/safe_git.sh" "$WS" "auto: 終端機對話備份 $(date '+%H:%M')" terminal-notes/raw_sessions >> /tmp/backup_terminal.log 2>&1 || { echo "[$TS] ⚠️ safe_git(backup) 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "safe_git(backup)" >/dev/null 2>&1; }  # 10/16：失敗當下通知
    fi

    # 7. sync_handoff + commit: */5 (:00, :05, :10, ...)
    #    2026-06-20 從系統 crontab 接管：原 cron 與 backup_terminal 撞 lock
    if [ $((10#$CURRENT_MIN % 5)) -eq 0 ]; then
        bash "$WS/scripts/sync_handoff_to_claudemd.sh" >> /tmp/sync_handoff.log 2>&1 || { echo "[$TS] ⚠️ sync_handoff 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "sync_handoff" >/dev/null 2>&1; }  # 10/16：失敗當下通知
    fi

    # 8. recall（查話系統）: */30 (:00, :30)
    if [ "$CURRENT_MIN" = "00" ] || [ "$CURRENT_MIN" = "30" ]; then
        /opt/homebrew/bin/python3 "$WS/scripts/recall.py" --harvest --build >> /tmp/recall.log 2>&1 || { echo "[$TS] ⚠️ recall 失敗" >> "$LOG"; bash "$WS/scripts/cron_fail_notify.sh" "recall" >/dev/null 2>&1; }  # 10/16：失敗當下通知
    fi

    sleep 60
done
