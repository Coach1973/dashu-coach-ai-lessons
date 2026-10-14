#!/usr/bin/env bash
# 開一個「獨立的」除錯用 Chrome 給 REA 連（不碰教練自己的 Chrome、不帶登入資料）
# 用法：start_debug_chrome.sh <網址> [--show]   （預設無頭；--show 才開出視窗）
# 關閉：start_debug_chrome.sh --stop
set -u
PORT=9333
URL="${1:-about:blank}"
MODE="--headless=new"
[ "${2:-}" = "--show" ] && MODE=""

case "$(uname -s)" in
  Darwin)
    CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    PROFILE="$HOME/.rea-chrome-profile" ;;
  *)
    CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
    PROFILE="$(cygpath -m "$LOCALAPPDATA")/rea-chrome-profile" ;;
esac

if [ "$URL" = "--stop" ]; then
  if [ "$(uname -s)" = "Darwin" ]; then
    pkill -f "rea-chrome-profile" && echo "已關閉除錯 Chrome" || echo "沒有在跑"
  else
    powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"name='chrome.exe'\" | Where-Object { \$_.CommandLine -like '*rea-chrome-profile*' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue }" 2>/dev/null
    echo "已關閉除錯 Chrome"
  fi
  exit 0
fi

if [ "$(uname -s)" = "Darwin" ]; then
  (nohup "$CH" --remote-debugging-port=$PORT --user-data-dir="$PROFILE" --no-first-run $MODE "$URL" >/dev/null 2>&1 &)
else
  # Git Bash 的背景程序會跟著腳本結束被收掉，改用 Start-Process 完全脫離
  ARGS="'--remote-debugging-port=$PORT','--user-data-dir=$PROFILE','--no-first-run'"
  [ -n "$MODE" ] && ARGS="$ARGS,'$MODE'"
  ARGS="$ARGS,'$URL'"
  powershell -NoProfile -Command "Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList $ARGS -WindowStyle Hidden"
fi
for i in $(seq 1 20); do
  curl -s "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1 && break
  sleep 1
done
sleep 3   # 等頁面載入
echo "CDP=http://127.0.0.1:$PORT"
rea list-browser-targets "http://127.0.0.1:$PORT" --format json 2>/dev/null \
  | grep -oE '"(id|target_id)": *"[A-F0-9]{20,}"' | head -1 | grep -oE '[A-F0-9]{20,}' | sed 's/^/TARGET=/'
