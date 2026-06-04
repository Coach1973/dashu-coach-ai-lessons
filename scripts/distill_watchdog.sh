#!/bin/bash
# distill_watchdog.sh — 終端機對話蒸餾 watchdog
# 用途：每 15 分鐘檢查 pending_distill/ 是否有卡住 >2 小時的檔案
# 設計：軍師 2026-06-04（教練 C 選：犯錯自動入庫）
# 觸發：crontab 每 15 分鐘

WS="/Users/bymyway/.openclaw/workspace"
PENDING_DIR="$WS/terminal-notes/pending_distill"
LOG="/tmp/distill_watchdog.log"
TODAY=$(date '+%Y-%m-%d %H:%M')

echo "[$TODAY] === distill_watchdog 開始 ===" >> "$LOG"

if [ ! -d "$PENDING_DIR" ]; then
    echo "[$TODAY] pending_distill 目錄不存在" >> "$LOG"
    exit 0
fi

# 找出 pending 檔案裡 mtime > 2 小時的
STUCK_FILES=$(find "$PENDING_DIR" -name "*.txt" -mmin +120 2>/dev/null)
if [ -z "$STUCK_FILES" ]; then
    STUCK_COUNT=0
else
    STUCK_COUNT=$(echo "$STUCK_FILES" | wc -l | tr -d ' ')
fi

if [ "$STUCK_COUNT" -gt 0 ]; then
    echo "[$TODAY] ⚠️ 發現 $STUCK_COUNT 個卡住檔案" >> "$LOG"
    echo "$STUCK_FILES" >> "$LOG"
    
    # 構造 Telegram 通知訊息
    FILE_LIST=$(echo "$STUCK_FILES" | while read f; do
        basename "$f" .txt
    done | head -5 | tr '\n' ' ')
    
    MSG="🦞 蒸餾 watchdog 警報

時間：$TODAY
卡住檔案：$STUCK_COUNT 個
Session：${FILE_LIST}

這些 pending 檔案超過 2 小時沒被蒸餾，請檢查 cron / 狀態檔。"

    # 透過 openclaw CLI 推 Telegram
    /opt/homebrew/bin/openclaw message send \
        -t 6124913915 \
        -m "$MSG" \
        >> "$LOG" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[$TODAY] ✅ 通知已推送" >> "$LOG"
    else
        echo "[$TODAY] ❌ 通知推送失敗" >> "$LOG"
    fi
else
    echo "[$TODAY] ✅ pending 正常（0 個卡住）" >> "$LOG"
fi

# 同時檢查今天的蒸餾檔案是否存在
TODAY_FILE="$WS/distill/terminal_$(date +%Y-%m-%d).md"
if [ ! -f "$TODAY_FILE" ]; then
    HOURS_PAST=$(($(date +%s) - $(date -j -f '%Y-%m-%d' "$(date +%Y-%m-%d)" +%s 2>/dev/null || date -d "$(date +%Y-%m-%d)" +%s)))
    HOURS_PAST=$((HOURS_PAST / 3600))
    if [ "$HOURS_PAST" -gt 4 ]; then
        echo "[$TODAY] ⚠️ 今天已過 $HOURS_PAST 小時，蒸餾檔案仍不存在：$TODAY_FILE" >> "$LOG"
        /opt/homebrew/bin/openclaw message send \
            -t 6124913915 \
            -m "🦞 蒸餾 watchdog 提醒

今天 $(date +%Y-%m-%d) 已過 $HOURS_PAST 小時，
~/workspace/distill/terminal_$(date +%Y-%m-%d).md 尚未產生。
可能原因：終端機今日無新對話，或 cron 卡住。" \
            >> "$LOG" 2>&1
    fi
fi

echo "[$TODAY] === distill_watchdog 結束 ===" >> "$LOG"
