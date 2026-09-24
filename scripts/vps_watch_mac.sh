#!/bin/bash
# VPS 看守 Mac（2026-09-24 教練交辦，團隊協作體檢第2項）。部署位置：VPS /root/watch_mac.sh
#
# Mac 上所有監控（每日點名、巡檢、健檢）都跑在 Mac 自己身上，Mac 整台掛掉（停電/斷網/當機）
# 時沒有任何東西能報警。改由 VPS 每30分鐘看一次 Mac 對外的兩個入口，兩個都打不開、而且
# 連續兩次才通知（避免 Mac 重開機的幾分鐘被誤報），恢復時再通知一次。
# 通知用 VPS 自己的 Telegram 機器人直接送，不經過 Mac。
#
# 測試用環境變數：WATCH_URLS（換檢查目標）、STATE（換狀態檔）、DRY=1（只印不送）

URLS=${WATCH_URLS:-"https://openclaw.bymyway.com/health https://event.bymyway.com/"}
STATE=${STATE:-/root/.watch_mac_state}
LOG=/var/log/watch_mac.log
TS=$(TZ=Asia/Taipei date '+%m/%d %H:%M')

send() {
  if [ "${DRY:-0}" = "1" ]; then echo "[DRY] 會送出：$1"; return 0; fi
  python3 - "$1" <<'PY'
import json, sys, urllib.parse, urllib.request
tok = json.load(open("/root/openclaw/data/openclaw.json"))["channels"]["telegram"]["botToken"]
data = urllib.parse.urlencode({"chat_id": "6124913915", "text": sys.argv[1]}).encode()
ok = json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data=data, timeout=20))["ok"]
sys.exit(0 if ok else 1)
PY
}

reachable=0
for u in $URLS; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -A 'Mozilla/5.0 (vps-watch)' "$u")
  if [ "$code" -ge 200 ] && [ "$code" -lt 400 ]; then reachable=1; fi
done

read -r status fails < <(cat "$STATE" 2>/dev/null || echo "up 0")
fails=${fails:-0}

if [ "$reachable" -eq 1 ]; then
  if [ "$status" = "down" ]; then
    send "✅【VPS看守通知】家裡的 Mac mini 已恢復連線（${TS} 台灣時間）。"
  fi
  echo "up 0" > "$STATE"
else
  fails=$((fails + 1))
  if [ "$fails" -ge 2 ] && [ "$status" != "down" ]; then
    if send "🚨【VPS看守通知】家裡的 Mac mini 大約30分鐘前起就連不上了（${TS} 台灣時間）。小龍蝦、LINE小幫手、活動網站可能都停了，常見原因是停電、斷網或當機，請看一下 Mac。"; then
      echo "down $fails" > "$STATE"
    else
      echo "up $fails" > "$STATE"   # 沒送出去就不標記down，下一輪重試
    fi
  else
    echo "$status $fails" > "$STATE"
  fi
fi
echo "[$TS] reachable=$reachable state=$(cat "$STATE")" >> "$LOG"
