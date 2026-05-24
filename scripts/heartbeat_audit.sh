#!/bin/bash
# heartbeat_audit.sh — 每天 23:50 統計 HEARTBEAT.md 的 OK 心跳數
# 觸發：系統 crontab（每天 23:50）
# 用途：追蹤 relay polling 是否正常運作
# 設計：軍師，2026-05-24

WS="/Users/bymyway/.openclaw/workspace"
HB="$WS/HEARTBEAT.md"
LOG="$WS/heartbeat_audit.log"
TODAY=$(date +%Y-%m-%d)

if [ ! -f "$HB" ]; then
    echo "[$TODAY] HEARTBEAT.md 不存在" >> "$LOG"
    exit 0
fi

# 統計今天的 OK 心跳數
OK_COUNT=$(grep -c "relay poll OK\|heartbeat OK\|HB_OK" "$HB" 2>/dev/null || echo 0)
RELAY_COUNT=$(grep -c "relay poll OK" "$HB" 2>/dev/null || echo 0)

echo "[$TODAY] OK 心跳統計: relay=$RELAY_COUNT total=$OK_COUNT" >> "$LOG"

# 如果今天 relay 心跳為 0，發送警告到 reminder.txt
if [ "$RELAY_COUNT" -eq 0 ]; then
    echo "⚠️ $(date '+%H:%M') 警告：今天 relay poll 零心跳，relay_poll.py 可能未正常運作" >> /Users/bymyway/Desktop/reminder.txt
fi

echo "✅ heartbeat_audit 完成：relay=$RELAY_COUNT"
