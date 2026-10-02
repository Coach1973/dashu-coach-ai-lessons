#!/bin/sh
# 要教練輸入 Mac 密碼時用的視窗（2026-10-02 實測：會跳到畫面最前面，教練看得到；App 終端機面板教練看不到）。
# 用法：SUDO_ASKPASS=~/.openclaw/workspace/scripts/coach_password_dialog.sh COACH_PW_MSG="這次要做什麼" sudo -A <指令>
# 密碼只交給 sudo，不會出現在任何紀錄。sudo 從 Claude 的 Bash 工具下，才保有「完整磁碟取用」（tmutil 等需要）；
# osascript 的 administrator privileges 那條路會失去它。
MSG="${COACH_PW_MSG:-需要管理員權限。}"
/usr/bin/osascript \
  -e 'on run argv' \
  -e 'tell application "System Events"' \
  -e 'activate' \
  -e 'set r to display dialog (item 1 of argv) & return & return & "請輸入 Mac 開機密碼：" default answer "" with hidden answer with title "大樹教練・需要密碼" buttons {"取消", "確定"} default button "確定" with icon caution' \
  -e 'end tell' \
  -e 'return text returned of r' \
  -e 'end run' "$MSG"
