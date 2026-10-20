#!/bin/bash
# 雲端對話開場（SessionStart）：把大樹教練的規則交給雲端 Claude。
# 這個檔案由 Mac 的 scripts/cloud/sync_rules_to_repos.py 自動同步進來，請勿在倉庫裡手改。
# Mac 本機另有全套規則（~/.claude/），這裡只在雲端執行；壞了一律放行（exit 0），不擋教練。
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
D="$(cd "$(dirname "$0")" && pwd)"
[ -f "$D/core.md" ] && cat "$D/core.md"
exit 0
