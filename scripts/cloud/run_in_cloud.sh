#!/bin/bash
# 雲端專用轉接：讓 Mac 上寫好的檢查程式在雲端照跑。用法：run_in_cloud.sh <scripts/底下的檔名>
# Mac 本機同一批檢查已由 ~/.claude/settings.json 負責，這裡直接略過，避免跑兩次。
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0

P="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
mkdir -p "$HOME/.openclaw"
[ -e "$HOME/.openclaw/workspace" ] || ln -s "$P" "$HOME/.openclaw/workspace"

exec bash "$P/scripts/$1"
