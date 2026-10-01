#!/bin/bash
# 雲端專用轉接：讓 Mac 上寫好的檢查程式在雲端照跑。用法：run_in_cloud.sh <scripts/底下的檔名>
# Mac 本機同一批檢查已由 ~/.claude/settings.json 負責，這裡直接略過，避免跑兩次。
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0

WS="$HOME/.openclaw/workspace"
if [ ! -e "$WS" ]; then
  mkdir -p "$HOME/.openclaw"
  ln -s "$(cd "$(dirname "$0")/../.." && pwd)" "$WS"
fi

SCRIPT="$1"; shift
case "$SCRIPT" in
  *.py) exec python3 "$WS/scripts/$SCRIPT" "$@" ;;  # 條件反射路由是 Python、要帶時刻參數
  *)    exec bash "$WS/scripts/$SCRIPT" "$@" ;;
esac
