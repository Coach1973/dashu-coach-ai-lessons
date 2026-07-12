#!/bin/bash
# Hook：SessionStart（Claude Code 新session開始時觸發）
# 用途：徹底解決「鎖做好了但沒裝上」這個系統性問題（2026-07-12教練重話：
#       「不要老是糊弄我，每次都跟我說做好了，等我發現沒有才解釋原因」）。
# 起因：同一場對話裡連續抓到3支鎖（rule07_polling_check.sh、
#       rule_html_chrome_check.sh、web_preview_verify_guard.sh）都寫好了
#       卻從未接進 ~/.claude/settings.json，稽核後發現 scripts/ 目錄底下
#       共有23支腳本聲稱自己是Claude Code hook，只有3支真的被註冊過。
#       CLAUDE.md甚至還記載著「已註冊」的錯誤資訊，文件跟現實脫節。
# 做法：掃描 scripts/*.sh 開頭的「# Hook：EVENT」宣告，比對
#       ~/.claude/settings.json 裡有沒有真的登記這支腳本的絕對路徑，
#       兩邊對不上就直接列出來，不靠人記得去查。
# 這支腳本本身也要記得手動裝進 settings.json 的 SessionStart，不然又是
# 同一個笑話——它自己就是活生生的反面教材，裝上之後歡迎隨時重新稽核。
set -uo pipefail

SCRIPTS_DIR="$HOME/.openclaw/workspace/scripts"
SETTINGS="$HOME/.claude/settings.json"

[[ -f "$SETTINGS" ]] || { echo "🔴 找不到 $SETTINGS"; exit 0; }

MISSING=""
while IFS= read -r -d '' f; do
  hookline=$(grep -m1 -E "^# Hook[：:]" "$f" 2>/dev/null)
  [[ -z "$hookline" ]] && continue
  abspath=$(cd "$(dirname "$f")" && pwd)/$(basename "$f")
  if ! grep -qF "$abspath" "$SETTINGS" 2>/dev/null; then
    MISSING+="  • $(basename "$f")  →  $hookline"$'\n'
  fi
done < <(find "$SCRIPTS_DIR" -maxdepth 1 -name "*.sh" -print0)

if [[ -n "$MISSING" ]]; then
  {
    echo ""
    echo "🔴🔒 Hook稽核：發現「宣告是hook但沒註冊進settings.json」的腳本"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf '%s' "$MISSING"
    echo "以上腳本檔頭寫著自己是Claude Code hook，但實際沒接進"
    echo "$SETTINGS，形同虛設。請人工確認每支腳本內容是否仍然適用，"
    echo "適用的話補進settings.json，不適用的話把檔頭的「# Hook：」宣告"
    echo "拿掉，避免下次稽核又誤報。"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  } >&2
fi

exit 0
