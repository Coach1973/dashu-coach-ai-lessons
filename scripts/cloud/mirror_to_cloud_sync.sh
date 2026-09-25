#!/bin/bash
# Mac 端：把只存在 ~/.claude/ 的全域規則與自訂技能，複製進 workspace/cloud_sync/，
# 讓雲端工作頁（只讀得到 GitHub 上的專案）也吃到同一套規則。
# 觸發：session_end_auto_push.sh（每則回覆結束時），複製完由它一起 commit + push。
WS="/Users/bymyway/.openclaw/workspace"
DEST="$WS/cloud_sync"
mkdir -p "$DEST/skills"

cmp -s "$HOME/.claude/CLAUDE.md" "$DEST/GLOBAL_CLAUDE.md" || cp "$HOME/.claude/CLAUDE.md" "$DEST/GLOBAL_CLAUDE.md"

# synced/ 是 claude.ai 帳號同步下來的官方技能，雲端本來就吃得到，不複製
for d in "$HOME"/.claude/skills/*/; do
  name=$(basename "$d")
  [ "$name" = "synced" ] && continue
  [ -f "$d/SKILL.md" ] || continue
  mkdir -p "$DEST/skills/$name"
  cp -R "$d." "$DEST/skills/$name/"
done
exit 0
