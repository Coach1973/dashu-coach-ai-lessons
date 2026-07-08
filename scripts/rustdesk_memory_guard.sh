#!/bin/bash
# 每天固定時間檢查 RustDesk --server 記憶體用量，超過門檻才重啟（教練 2026-07-09 要求）
# 門檻：800MB（2026-07-09 實測發現：剛重啟後只要教練正在連線操作，1分鐘內就會自然漲到 280~300MB，
#   這是畫面即時編碼傳輸的正常用量，不是洩漏。門檻設太低會在教練正在用的時候一直誤殺、一直斷線。
#   800MB 只抓真正異常飆高的狀況，正常使用不會被打斷。）
# 重啟方式：kill --server process，RustDesk 自帶的 service（root 常駐）會在幾秒內自動重新拉起一個乾淨的
# 不會整個 App 關閉重開，也不需要教練手動重新連線

THRESHOLD_KB=800000
LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/rustdesk_memory_guard.log"
TS=$(TZ=Asia/Taipei date "+%Y-%m-%d %H:%M:%S")

PID=$(pgrep -f "RustDesk --server" | head -1)

if [ -z "$PID" ]; then
  echo "[$TS] 找不到 RustDesk --server process，略過" >> "$LOG_FILE"
  exit 0
fi

RSS_KB=$(ps -o rss= -p "$PID" | tr -d ' ')
RSS_MB=$((RSS_KB / 1024))

if [ "$RSS_KB" -gt "$THRESHOLD_KB" ]; then
  kill -TERM "$PID"
  sleep 5
  NEW_PID=$(pgrep -f "RustDesk --server" | head -1)
  NEW_RSS_KB=$(ps -o rss= -p "$NEW_PID" 2>/dev/null | tr -d ' ')
  NEW_RSS_MB=$(( ${NEW_RSS_KB:-0} / 1024 ))
  echo "[$TS] 超過門檻（${RSS_MB}MB > 200MB），已重啟。新 process PID=$NEW_PID，記憶體 ${NEW_RSS_MB}MB" >> "$LOG_FILE"
else
  echo "[$TS] 目前 ${RSS_MB}MB，未超過門檻，略過" >> "$LOG_FILE"
fi
