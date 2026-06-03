#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練每發一句話，自動偵測觸發詞，注入對應的 SOP 提醒到 context。
# 設計：根據 教練高頻語錄_SOP.md 的真實統計，偵測教練說的關鍵字
#       → 注入對應的 SOP 動作（不靠模型記得、靠系統強制）
# 軍師建立 2026-06-04
set -uo pipefail

INPUT=$(cat)
Prompt=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$Prompt" ]] && exit 0

# === 教練語錄 SOP 路徑 ===
COACH_SOP="$HOME/.claude-code/workspace/教練高頻語錄_SOP.md"

# 找不到檔案就靜默退出
[[ -f "$COACH_SOP" ]] || exit 0

HITS=""
add_hit() { HITS="${HITS}$1"$'\n'; }

# === 觸發詞偵測（按教練高頻語句真實統計）===

# 「OK」「好」「對的」= 教練認可（次數最高 10447）
if printf '%s' "$Prompt" | grep -qE "好的$|^好$|OK$|讚$|^棒$"; then
  add_hit "• 【正向認可】教練說「好/OK/對的」= 你的回應是對的。立即繼續執行，不要過度確認或停頓。"
fi

# 「繼續」「快點」= 催促進度（次數 1183）
if printf '%s' "$Prompt" | grep -qE "繼續|快點|^快$|好了嗎|完成了嗎"; then
  add_hit "• 【催促回報】教練說「繼續/快」= 立即給進度回報，不要沉默。預估 ETA，告訴教練還要多久。"
fi

# 「主動」「自動自發」= 教練最在意的價值觀（次數 1302）
if printf '%s' "$Prompt" | grep -qE "主動|自動自發|用心|認真"; then
  add_hit "• 【自動自發】教練說「主動/自動自發」= 教練最在意的價值觀（1302 次提及）。不等提醒，自己想到後面 10 步並執行。"
fi

# 「不要」「絕對不要」= 禁止事項（次數 1522）
if printf '%s' "$Prompt" | grep -qE "^不要$|絕對不要|禁止|千萬不要"; then
  add_hit "• 【禁止事項】教練說「不要」= 立即牢記禁止事項，立即修正行為，絕不再犯。"
fi

# 「記下來」「commit」「hash」= 承諾鐵律（次數 4304）
if printf '%s' "$Prompt" | grep -qE "記下來|寫下來|commit|hash|憑證"; then
  add_hit "• 【承諾鐵律】教練說「記下來/commit」= 當場執行並給 commit hash，不能只說「記住了」。凡走過必留痕跡。"
fi

# 「怎麼」「為什麼」= 教練問原因（次數 722）
if printf '%s' "$Prompt" | grep -qE "為什麼|怎麼.*沒|原因"; then
  add_hit "• 【原因解釋】教練說「為什麼/怎麼」= 不能只給結果，要解釋「為什麼」。每個決策都要說明依據。"
fi

# 「錯了」「不對」= 糾正錯誤（次數 100）
if printf '%s' "$Prompt" | grep -qE "^錯了$|不對|^亂$"; then
  add_hit "• 【立即認錯】教練說「錯了/不對」= 立即認錯+自我修正+不再犯。查 Top30 試金石。"
fi

# 「你又」「又犯」「笨」= 批評（次數 27，但嚴重）
if printf '%s' "$Prompt" | grep -qE "你又|又犯|笨|笨蛋|浪費"; then
  add_hit "• 🔴【嚴重批評】教練說「你又/笨/浪費」= 嚴重犯錯！立即查 Top30_Index.md 對應案例，自我反省不再犯。"
fi

# 「謝謝」「辛苦了」= 感謝
if printf '%s' "$Prompt" | grep -qE "謝謝|辛苦了|辛苦你"; then
  add_hit "• 【感謝】教練說「謝謝/辛苦了」= 簡短回應「不客氣」，不囉嗦。"
fi

# === 輸出 ===
if [[ -n "$HITS" ]]; then
  echo "🗣️ 教練語錄 SOP 提醒（基於真實對話統計）"
  echo ""
  printf '%s' "$HITS"
  echo ""
  echo "📊 統計：教練高頻語句真實次數 10,785 條，完整對照表見 教練高頻語錄_SOP.md"
  echo "（引用前先查 教練高頻語錄_SOP.md 確認一字不差。發現新觸發詞，立即寫入並 commit。）"
fi

exit 0
