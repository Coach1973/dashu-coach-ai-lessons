#!/bin/bash
# 教練口頭下令「釋放記憶體」時直接執行，不做門檻判斷——教練已經自己用眼睛看過
# Activity Monitor才下令，這裡只負責照做。2026-08-27建立（教練明確要求用指令
# 取代每10分鐘一次的自動輪詢：「我自己目視偵測就好」）。
#
# 跟 rustdesk_memory_guard.sh 的差異：guard腳本是每天05:00的自動安全網，
# 有門檻判斷(>800MB才動作)；這支是教練親口下令時的無條件立即重啟。

LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/rustdesk_memory_guard.log"
TS=$(TZ=Asia/Taipei date "+%Y-%m-%d %H:%M:%S")

PID=$(pgrep -f "RustDesk --server" | head -1)

if [ -z "$PID" ]; then
  echo "[$TS] 教練下令釋放記憶體，但找不到 RustDesk --server process" >> "$LOG_FILE"
  echo "找不到 RustDesk --server process，可能沒有在跑"
  exit 1
fi

BEFORE_RAW=$(top -pid "$PID" -l 1 -stats mem 2>/dev/null | tail -1 | tr -d '[:space:]')

kill -TERM "$PID"
sleep 5

NEW_PID=$(pgrep -f "RustDesk --server" | head -1)
AFTER_RAW=$(top -pid "${NEW_PID:-0}" -l 1 -stats mem 2>/dev/null | tail -1 | tr -d '[:space:]')

echo "[$TS] 教練下令釋放記憶體，已重啟。舊PID=$PID(${BEFORE_RAW}) -> 新PID=$NEW_PID(${AFTER_RAW})" >> "$LOG_FILE"
echo "已重啟 RustDesk：${BEFORE_RAW} -> ${AFTER_RAW}（新PID=$NEW_PID，連線會自動恢復不用手動重連）"
