#!/bin/bash
# Hook：UserPromptSubmit
# 用途：偵測教練 prompt 中提及「守則 #XX / 守則XX / 心法第 X 條」等明確編號，
#       自動從 ~/.openclaw/workspace/特助心法.md grep 該條完整原文，注入 context。
# 設計理念（Meta Automation，2026-06-06 教練親定）：
#       與其讓模型靠記憶引用守則（常被 #21 違反、捏造詮釋），
#       不如 hook 主動把「一字不差原文」塞進 context，模型沒有藉口錯引。
# 落實：守則#21（核心理念原文引用）+ E08（引用查證鐵律）的工程化檢查。
# 軍師建立 2026-06-06
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$PROMPT" ]] && exit 0

XINFA="$HOME/.openclaw/workspace/特助心法.md"
[[ -f "$XINFA" ]] || exit 0

# === 抓取教練提及的守則編號 ===
# 支援格式：守則#05 / 守則 #5 / 守則05 / 守則5 / 心法第5條 / 第5條 / #05
# 用 grep -oE 抓所有命中
RULES=$(printf '%s' "$PROMPT" | grep -oE '(守則[[:space:]]*#?|心法第|第|#)0?[0-9]{1,2}(條)?' \
        | grep -oE '[0-9]{1,2}' \
        | sort -u)

[[ -z "$RULES" ]] && exit 0

# 只保留 01-21 範圍
VALID_RULES=$(printf '%s\n' "$RULES" | awk '$1>=1 && $1<=21 {printf "%02d\n", $1}' | sort -u)
[[ -z "$VALID_RULES" ]] && exit 0

# 輸出開頭
printf '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '📜 守則原文自動引用（系統 grep 特助心法.md，一字不差）\n'
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '⚠️ 教練在 prompt 提到守則編號，以下是該條完整原文。\n'
printf '   引用時必須一字不差，禁止改寫（守則#21 + 執行細則N3）。\n\n'

# 逐條 grep 該守則完整段落（從 **NN. 到 下一個 **NN+1.）
while IFS= read -r RULE_NUM; do
  NEXT=$(printf '%d' $((10#$RULE_NUM + 1)))
  NEXT_PADDED=$(printf '%02d' "$NEXT")

  # awk 抓該條到下一條之間（不含下一條的標題行）
  CONTENT=$(awk -v start="^\\\\*\\\\*${RULE_NUM}\\\\." -v end="^\\\\*\\\\*${NEXT_PADDED}\\\\." '
    $0 ~ start { found=1 }
    found && $0 ~ end { exit }
    found { print }
  ' "$XINFA")

  if [[ -n "$CONTENT" ]]; then
    printf '%s\n' "$CONTENT"
    printf '\n──────────────────────────\n'
  fi
done <<< "$VALID_RULES"

printf '（來源：%s）\n' "$XINFA"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

exit 0
