#!/bin/bash
# 雲端工作頁開場（SessionStart）：把教練在 Mac 上的全套規則交給雲端 Claude。
# Mac 本機的規則由 ~/.claude/CLAUDE.md 負責，這裡直接略過，避免重複載入。
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0

P="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

# 規則和檢查程式裡的路徑都寫 ~/.openclaw/workspace，雲端建一個同名捷徑指到專案本身
mkdir -p "$HOME/.openclaw"
[ -e "$HOME/.openclaw/workspace" ] || ln -s "$P" "$HOME/.openclaw/workspace"

if [ -d "$P/cloud_sync/skills" ]; then
  mkdir -p "$HOME/.claude/skills"
  cp -R "$P/cloud_sync/skills/." "$HOME/.claude/skills/"
fi

cat <<'EOF'
☁️ 這是雲端工作頁（雲端 Linux 主機，不是教練的 Mac）。以下是教練在 Mac 上的全套規則，雲端一體適用，不可以說「這在 Mac 上，我不知道」。
- 身份：依模型判定，Sonnet 5 以上（含 Opus、Fable）＝軍師。commit 前綴用 [Cloud]。
- 雲端做不到的只有「要動到教練 Mac 本機」的事：控制 Mac 上的程式與視窗、launchd 排程、本機 LINE／Telegram 閘道、Mac 上 Chrome 的登入狀態等。遇到這類事，說清楚「這件要回 Mac 桌面版做」；其他一律照規則直接做。
- 規則提到的技能，說明書在 cloud_sync/skills/<技能名稱>/SKILL.md。
- 下方規則若顯示被截斷，立刻用 Read 讀完 cloud_sync/GLOBAL_CLAUDE.md。

EOF
cat "$P/cloud_sync/GLOBAL_CLAUDE.md"
printf '\n\n=== 模型分工規則（knowledges/模型分工規則_Opus與Sonnet.md）===\n'
cat "$P/knowledges/模型分工規則_Opus與Sonnet.md"
exit 0
