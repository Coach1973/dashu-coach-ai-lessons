#!/bin/bash
# Hook：PostToolUse（Write|Edit|Bash）
# 用途：AI 寫下教訓／記憶的「那一刻」，逼它走轉換三問，而不是只把案例丟進抽屜。
# 起因：2026-10-02 教練：「寶貴的經驗總是會忘記，就像記錄下來放在抽屜一樣，根本沒有拿出來看。」
#       試金石已 81 案、40 萬字，記憶 448 檔，錯照樣再犯；今天的網址錯坑了教練十幾二十次，
#       沒有任何一條記錄抓到，最後是改 3 行程式才永久消失。
#       設計見 knowledges/2026-10-02_記憶系統根本改版_從抽屜到工作站.md
# 只在寫「試金石／記憶／蒸餾」時出聲，其餘一律安靜（不花教練額度）。
set -uo pipefail
INPUT=$(cat)
TOOL=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_name // ""' 2>/dev/null)
case "$TOOL" in
  Write|Edit) TARGET=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.file_path // ""' 2>/dev/null) ;;
  Bash)       TARGET=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.command // ""' 2>/dev/null)
              # Bash 只認「寫入」動作，避免 cat/grep 讀檔也出聲
              printf '%s' "$TARGET" | grep -qE '(>>|> |tee |sed -i|cp |mv )' || exit 0 ;;
  *) exit 0 ;;
esac
printf '%s' "$TARGET" | grep -qE '試金石_案例庫\.md|/memory/[^ ]*\.md|claude-brain/[^ ]*\.md|/distill/' || exit 0
# 情境目錄本身的更新不再提醒（那就是三問的第②步）
printf '%s' "$TARGET" | grep -q '情境目錄' && exit 0

MSG='🔁 你剛寫下一筆教訓／記憶。寫下來≠會用（教練2026-10-02：「記錄下來放在抽屜，根本沒有拿出來看」）。現在走轉換三問：①能不能改程式／範本／工具，讓這個錯不可能再發生？能→這一輪就改，案例只當歷史。②不能→它發生在哪個時刻（寫通知、部署、刪檔、問教練、遠端連線…）？把一行提示補進 knowledges/情境目錄.md 那個時刻底下。③都不是→是判斷問題，對照特助心法21條原文是哪一條。回報教練時說你走了哪一條。'
/usr/bin/jq -n --arg m "$MSG" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$m}}'
exit 0
