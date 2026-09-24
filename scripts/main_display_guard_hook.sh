#!/bin/bash
# Hook：PostToolUse（Bash / Edit / Write / computer-use open_application）
# 用途：AI 開了 App、視窗或 Chrome 之後，自動把跑到副螢幕的視窗搬回主螢幕。
# 起因：2026-09-25 教練副螢幕（擴充塢附的，接著 SSD 和連接埠，不能拔、從不看）
#       我 open 系統設定落在副螢幕，教練兩次說沒看到。教練：「下次任何的顯示，請都顯示在有桌面的主螢幕」。
input=$(cat)
trigger=$(printf '%s' "$input" | /usr/bin/python3 -c '
import json, re, sys
d = json.load(sys.stdin)
t = d.get("tool_name", "")
ti = d.get("tool_input") or {}
if t == "Bash":
    print(1 if re.search(r"(^|[\s;&|(])open\s|osascript", ti.get("command", "")) else 0)
elif t in ("Edit", "Write"):
    print(1 if str(ti.get("file_path", "")).lower().endswith(".html") else 0)
else:
    print(1 if t.endswith("open_application") else 0)
' 2>/dev/null)
[ "$trigger" = "1" ] || exit 0

SWEEP="$HOME/.openclaw/workspace/scripts/move_windows_to_main_display.sh"
LOG="$HOME/.openclaw/workspace/logs/main_display_guard.log"
# App 開視窗需要一點時間，2 秒、5 秒各掃一次；背景執行不拖慢工具
nohup bash -c '
for d in 2 3; do
  sleep "$d"
  out=$("$0")
  case "$out" in *"視窗 0 個"*) ;; *) echo "$(date "+%F %T") $out" >> "$1" ;; esac
done' "$SWEEP" "$LOG" >/dev/null 2>&1 &
exit 0
