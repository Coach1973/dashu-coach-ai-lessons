#!/bin/bash
# 教練口頭下令「全部釋放」時執行：關瀏覽器/赫米斯/LINE/Typeless四個常駐App
# 釋放記憶體，同時重啟RustDesk(連線軟體)。2026-09-02教練親口定義範圍：
# 「如果我要釋放記憶體，指令可能就叫做『全部釋放』：關掉瀏覽器、關掉赫米斯、
# 關掉LINE、關掉語音輸入法(Typeless)、同時重啟連線軟體」。
#
# 跟 rustdesk_free_memory.sh 的差異：那支只重啟RustDesk一項；這支是教練親口
# 下令「全部」時的完整版，涵蓋五個動作。RustDesk仍是「重啟」不是「關掉」，
# 因為教練很可能是透過RustDesk下達這個指令的，關掉不重啟會斷線。

LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/rustdesk_memory_guard.log"
TS=$(TZ=Asia/Taipei date "+%Y-%m-%d %H:%M:%S")
UID_NUM=$(id -u)
RESULTS=()

is_running() {
  osascript -e "tell application \"System Events\" to (name of processes) contains \"$1\"" 2>/dev/null | grep -q "true"
}

quit_app() {
  local app_name="$1"
  local label="$2"
  if is_running "$app_name"; then
    osascript -e "tell application \"$app_name\" to quit" 2>/dev/null
    sleep 1
    if is_running "$app_name"; then
      RESULTS+=("$label：已送出關閉指令，仍在結束中")
    else
      RESULTS+=("$label：已關閉")
    fi
  else
    RESULTS+=("$label：本來就沒在跑")
  fi
}

# 1. 關掉瀏覽器（Chrome）
quit_app "Google Chrome" "瀏覽器(Chrome)"

# 2. 關掉赫米斯「桌面版App」（menubar/desktop/config-watcher三個GUI相關服務）
#    🔴 2026-09-19教練親口糾正：ai.hermes.gateway是Telegram 24小時運作的後端
#    (python -m hermes_cli.main gateway，跟教練在Telegram上聊天的就是這個
#    process)，跟「桌面版App」是兩回事——教練說「全部釋放」指的是關掉佔記憶體
#    的桌面GUI程式，從來不包含要把Telegram也斷線。舊版本把gateway一起bootout，
#    導致教練在Telegram上完全聯絡不到赫米斯長達16小時、且看門狗機制把這個
#    狀態當成「故意關閉」不會提醒，教練完全不知情才發現。已改成只關三個GUI
#    服務，gateway永遠不動，維持24小時運作。
HERMES_DESKTOP_WAS_RUNNING=$(pgrep -f "Hermes.app|hermes-menubar-v2.py" | head -1)
for label in ai.hermes.menubar ai.hermes.desktop ai.hermes.config-watcher; do
  launchctl bootout "gui/${UID_NUM}/${label}" >/dev/null 2>&1
done
if [ -n "$HERMES_DESKTOP_WAS_RUNNING" ]; then
  RESULTS+=("赫米斯桌面版App：已關閉(gateway後端維持24小時運作，未受影響)")
else
  RESULTS+=("赫米斯桌面版App：本來就沒在跑(gateway後端維持24小時運作，未受影響)")
fi

# 3. 關掉LINE
quit_app "LINE" "LINE"

# 4. 關掉語音輸入法（Typeless）
quit_app "Typeless" "語音輸入法(Typeless)"

# 5. 同時重啟連線軟體（RustDesk，KeepAlive會自動拉起新process，連線自動恢復）
RD_PID=$(pgrep -f "RustDesk --server" | head -1)
if [ -n "$RD_PID" ]; then
  BEFORE_RAW=$(top -pid "$RD_PID" -l 1 -stats mem 2>/dev/null | tail -1 | tr -d '[:space:]')
  kill -TERM "$RD_PID"
  sleep 5
  NEW_PID=$(pgrep -f "RustDesk --server" | head -1)
  AFTER_RAW=$(top -pid "${NEW_PID:-0}" -l 1 -stats mem 2>/dev/null | tail -1 | tr -d '[:space:]')
  RESULTS+=("連線軟體(RustDesk)：已重啟 舊PID=$RD_PID(${BEFORE_RAW}) -> 新PID=$NEW_PID(${AFTER_RAW})，連線會自動恢復")
else
  RESULTS+=("連線軟體(RustDesk)：找不到process，可能沒在跑")
fi

{
  echo "[$TS] 教練下令「全部釋放」，執行結果："
  for r in "${RESULTS[@]}"; do echo "  - $r"; done
} >> "$LOG_FILE"

echo "已執行全部釋放："
for r in "${RESULTS[@]}"; do echo "・$r"; done
