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

# 判斷3（2026-09-24根源改版，會擋下）：「🙋要教練決定」區只能放三關全過的事。
# 教練：「同一類事情不要再重複來煩我了」。過去5次同類錯都只寫記憶，記憶打不過待辦表的具體內容，
# 所以改成提交當下由程式檢查：每件要寫明「只有教練能做」的原因＋「問過」日期，最多3件，三關規則不准被刪。
ASK_ERR=$(git show ":$HANDOFF" 2>/dev/null | /opt/homebrew/bin/python3 -c '
import sys
text = sys.stdin.read()
errs = []
required = ["① **只有教練能做**", "② **教練沒答過**", "③ **現在不問會卡住**", "**每件事最多問一次**", "### 🙋"]
missing = [r for r in required if r not in text]
if missing:
    errs.append("待辦表開頭的三關規則或🙋區被刪改了，缺：" + "、".join(missing) + "，請還原")
else:
    sec = text.split("### 🙋", 1)[1].split("\n###", 1)[0].split("\n## ", 1)[0]
    items = [l for l in sec.split("\n")[1:] if l.startswith("- ") or (l.startswith("|") and "---" not in l and "優先" not in l)]
    if len(items) > 3:
        errs.append(f"🙋區有{len(items)}件，上限3件——不急的請移到「🤫等教練自己提起」區")
    for l in items:
        if "只有教練" not in l or "問過" not in l:
            errs.append("缺三關說明：" + l[:60] + "（每件要寫「只有教練能做：原因」和「問過：日期或未問」）")
print("\n".join(errs))
')
if [[ -n "$ASK_ERR" ]]; then
  cat >&2 <<GUARD3_EOF
🚦 接力棒「🙋要教練決定」區沒過三關檢查，本次 commit 已擋下（2026-09-24教練要求根源解決「重複拿事情來煩教練」）

$ASK_ERR

三關：①只有教練能做 ②教練沒答過 ③現在不問會卡住。少一關的事，AI自己處理或放進🤫區。修好再 commit。
GUARD3_EOF
  exit 2
fi

exit 0
