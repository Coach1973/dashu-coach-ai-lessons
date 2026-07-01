#!/bin/bash
# 給其他機器（ACER/聯想/VPS）用的 Mac 存活檢查
# 用法：在別台機器的 workspace 跑，超過 15 分鐘沒心跳就 exit 1 + Telegram 推播
# ACER bash / 聯想 wsl / VPS 都能跑

WORKSPACE="${1:-$(dirname $(dirname $(realpath $0)))}"
FILE="$WORKSPACE/monitoring/mac_alive.txt"
THRESHOLD_SEC=900   # 15 分鐘
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_COACH_CHAT_ID:-6124913915}"

if [ ! -f "$FILE" ]; then
  echo "❌ 找不到 $FILE - 先 git pull"
  exit 2
fi

last_epoch=$(grep '^epoch:' "$FILE" | awk '{print $2}')
now_epoch=$(date +%s)
diff=$((now_epoch - last_epoch))

if [ "$diff" -gt "$THRESHOLD_SEC" ]; then
  mins=$((diff / 60))
  msg="🚨 Mac 掛機警報：Mac mini 已 ${mins} 分鐘沒心跳（超過 15 分鐘閾值）。最後心跳：$(grep '^last_seen:' $FILE | cut -d' ' -f2-)"
  echo "$msg"
  if [ -n "$BOT_TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -d chat_id="${CHAT_ID}" -d text="${msg}" > /dev/null
    echo "📱 已推播 Telegram"
  fi
  exit 1
else
  mins=$((diff / 60))
  echo "✅ Mac 存活（${mins} 分鐘前心跳）"
  exit 0
fi
