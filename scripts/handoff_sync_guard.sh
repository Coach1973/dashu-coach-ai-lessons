#!/bin/bash
# Hook: PreToolUse, Bash matcher
# 用途：git commit 涉及 JUNSHI_HANDOFF_LATEST.md 時，偵測「新增了完成敘述，
#       卻沒同步更新開頭狀態追蹤總表」的落差，提醒但不擋（避免誤判擋住正常commit）。
# 起因：2026-09-18 v219把「10/3 Netlify部署失敗」問題解決並驗證，但只在文末新增
#       「本場戰果」敘述，沒回頭把狀態表那一列的🔒改成✅。下一棒(v220)照唸舊狀態表，
#       把已解決的問題重新丟給教練選，教練當場動怒糾正。詳見
#       claude-brain/feedback_stale_handoff_row_represented_as_unsolved_2026-09-18.md
set -uo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_name // ""' 2>/dev/null)
CMD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.command // ""' 2>/dev/null)

[[ "$TOOL_NAME" != "Bash" ]] && exit 0
echo "$CMD" | grep -qE "git commit" || exit 0

WS="/Users/bymyway/.openclaw/workspace"
HANDOFF="JUNSHI_HANDOFF_LATEST.md"
cd "$WS" 2>/dev/null || exit 0

# 只在 JUNSHI_HANDOFF_LATEST.md 有被 staged 修改時才檢查
git diff --cached --name-only 2>/dev/null | grep -qx "$HANDOFF" || exit 0

DIFF=$(git diff --cached -- "$HANDOFF" 2>/dev/null)
[[ -z "$DIFF" ]] && exit 0

# 判斷1：新增內容裡有沒有強完成訊號（新增行=以+開頭，排除+++檔頭行）
ADDED=$(printf '%s\n' "$DIFF" | grep -E "^\+[^+]")
HAS_COMPLETION_SIGNAL=0
if printf '%s\n' "$ADDED" | grep -qE "✅|已完成|已上線|已解決|已修復|deploy.*ready|curl.*200|驗證.*成功"; then
  HAS_COMPLETION_SIGNAL=1
fi

# 判斷2：這次diff有沒有動到開頭「現在真正待辦」狀態追蹤總表的任何一列
# 表格列的特徵：行內容以 | 開頭且含🔒或⏳或✅或🟢等狀態符號的table row
TABLE_TOUCHED=0
if printf '%s\n' "$DIFF" | grep -qE "^[+-]\| .*(🔒|⏳|✅|🟢|🟡|⚠️)"; then
  TABLE_TOUCHED=1
fi

if [[ "$HAS_COMPLETION_SIGNAL" -eq 1 && "$TABLE_TOUCHED" -eq 0 ]]; then
  cat >&2 <<'GUARD_EOF'
🌱 接力棒同步提醒（2026-09-18 教練親身經歷後建立，非硬性擋下）

這次 commit 對 JUNSHI_HANDOFF_LATEST.md 的新增內容裡出現「✅/已完成/已上線/已解決」
這類完成訊號，但 diff 沒有同時修改開頭「📋 現在真正待辦」狀態追蹤總表裡任何一列。

【自問】這次完成的事，狀態表裡有沒有對應的🔒/⏳舊列？如果有，記得同一輪改成✅，
不要只在文末新增敘述——下一棒（可能是你自己）只會照唸狀態表，沒同步會把已解決的
問題重新丟給教練選，這正是 [[feedback_stale_handoff_row_represented_as_unsolved_2026-09-18]]
案例的根因。

【如果這次完成的事本來就不在狀態表裡（新任務、非既有待辦項）】
這個提醒是誤判，直接繼續 commit 即可，不會被擋下。
GUARD_EOF
fi

exit 0
