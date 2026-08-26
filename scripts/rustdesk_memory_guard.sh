#!/bin/bash
# 定期檢查 RustDesk --server 記憶體用量，超過門檻才重啟（教練 2026-07-09 要求，2026-08-27 修復量錯單位的舊版）
#
# 🔴 2026-08-27 修復重大bug：舊版用 `ps -o rss` 量測，但這個數字跟 Activity Monitor／
#   教練實際看到的「真實記憶體」（macOS footprint，含壓縮記憶體、記憶體對應區段等）
#   可以差到10倍以上——實測當下 `ps RSS`=488MB，但 Activity Monitor 顯示 5.48GB。
#   結果是這支腳本從 2026-07-11 調高門檻到 800MB 後，過去約6週每天固定跑、
#   log看起來正常，但門檻用錯單位換算實際上永遠不會被觸發到，等於形同虛設，
#   直到教練自己在 Activity Monitor 看到 5.48GB 才發現。現在改用 `top -pid X -stats mem`
#   讀跟 Activity Monitor 同一份「真實記憶體」數字，才是教練真正在意的那個數字。
#
# 門檻：800MB（教練 2026-07-09 實測：剛重啟後若教練正在連線操作，短時間內會自然漲到
#   280~300MB，是畫面即時編碼傳輸的正常用量不是洩漏；門檻抓800MB只攔真正異常飆高，
#   不會在教練正常使用時誤殺斷線）。
# 重啟方式：kill --server process，RustDesk 自帶的 service（root 常駐）會在幾秒內自動
#   重新拉起一個乾淨的，不會整個 App 關閉重開，也不需要教練手動重新連線。
# 執行頻率：改成每10分鐘跑一次（原本每天固定05:00跑一次，太久才抓到一次，教練
#   凌晨看到5.48GB時最近一次檢查是13小時前的05:00，等於一整個工作天都沒人管）。

THRESHOLD_MB=800
LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/rustdesk_memory_guard.log"
NOTIFY_SCRIPT="/Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh"
TS=$(TZ=Asia/Taipei date "+%Y-%m-%d %H:%M:%S")

# 讀真實記憶體(footprint)，跟Activity Monitor同一個數字，不是ps RSS
read_footprint_mb() {
  local pid="$1"
  local raw
  raw=$(top -pid "$pid" -l 1 -stats mem 2>/dev/null | tail -1 | tr -d '[:space:]')
  if [[ "$raw" =~ ^([0-9]+)G$ ]]; then
    echo $(( ${BASH_REMATCH[1]} * 1024 ))
  elif [[ "$raw" =~ ^([0-9]+)M$ ]]; then
    echo "${BASH_REMATCH[1]}"
  elif [[ "$raw" =~ ^([0-9]+)K$ ]]; then
    echo $(( ${BASH_REMATCH[1]} / 1024 ))
  else
    echo ""
  fi
}

PID=$(pgrep -f "RustDesk --server" | head -1)

if [ -z "$PID" ]; then
  echo "[$TS] 找不到 RustDesk --server process，略過" >> "$LOG_FILE"
  exit 0
fi

MEM_MB=$(read_footprint_mb "$PID")

if [ -z "$MEM_MB" ]; then
  echo "[$TS] 讀取記憶體失敗(PID=$PID)，略過本次檢查" >> "$LOG_FILE"
  exit 0
fi

if [ "$MEM_MB" -gt "$THRESHOLD_MB" ]; then
  kill -TERM "$PID"
  sleep 5
  NEW_PID=$(pgrep -f "RustDesk --server" | head -1)
  NEW_MEM_MB=$(read_footprint_mb "${NEW_PID:-0}")
  echo "[$TS] 超過門檻（${MEM_MB}MB > ${THRESHOLD_MB}MB），已重啟。新 process PID=$NEW_PID，記憶體 ${NEW_MEM_MB:-未知}MB" >> "$LOG_FILE"
  bash "$NOTIFY_SCRIPT" "🖥️ RustDesk記憶體超標(${MEM_MB}MB)已自動重啟，現在${NEW_MEM_MB:-未知}MB，連線會自動恢復不用手動重連。" 3600 rustdesk_guard_restart 2>/dev/null || true
else
  echo "[$TS] 目前 ${MEM_MB}MB，未超過門檻，略過" >> "$LOG_FILE"
fi
