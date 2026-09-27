#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練每發一句話，自動偵測關鍵字，注入相關「特助守則」提醒到 context。
#       讓守則對照「不靠模型記得、靠系統強制」。
# 升級 Phase 3：命中關鍵字時，同時注入守則故事檔摘要（📣教練原話 + 🌱悟到什麼）
# 設計：與 feed_junshi_handoff.sh 不同，守則對照要「每輪 prompt 都檢查」，
#       但只在命中關鍵字時才輸出（不命中則靜默），避免雜訊與炸 token。
# 依據：knowledges/01_knowledge_base/trigger_index.md 的觸發對照表
#       distill/守則故事庫/ （21條，已過 A/B/C 品管）
# 軍師建立 2026-05-27 初版，Phase3 升級 2026-05-29
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$PROMPT" ]] && exit 0

# === 守則故事檔路徑基底 ===
STORY_DIR="$HOME/.openclaw/workspace/distill/守則故事庫"

# 取 Story 片段：📣教練原話 + 🌱悟到什麼（至下一 ### 標題為止）
extract_story_quotes() {
  local file="$1"
  [[ -f "$file" ]] || return 1

  # 📣 區段：從 ### 📣 到 ### 🌱（不含🌱）
  printf '%s\n' "=== 📣 教練原話 ==="
  awk '/^### 📣/,/^### 🌱/' "$file" | grep -v "^### 🌱" | grep -v '^$'

  # 🌱 區段：只取第一段悟到什麼（到下一個 ### 二級標題為止）
  printf '%s\n' ""
  printf '%s\n' "=== 🌱 悟到什麼 ==="
  awk '
    /^### 🌱/ {p=1; next}
    /^### [🧬⚡✅📊]/ {if(p) exit}
    p {print}
  ' "$file" | grep -v '^$'
}

inject_story() {
  local file="$1"
  local rule="$2"
  local size_before=$(extract_story_quotes "$file" 2>/dev/null | wc -c)
  if [[ $size_before -gt 4096 ]]; then
    # 超限則截斷 🌱 部分，只取前 800 字
    extract_story_quotes "$file" | head -c 4096
  else
    extract_story_quotes "$file"
  fi
  printf '%s\n' ""
  printf '%s\n' "📂 案例：守則#${rule}"
}

HITS=""
BEFORE=""
add_hit() { HITS="${HITS}$1"$'\n'; }

# === Phase 3：故事檔注入 ===
# 先偵測，用 case/if 結構，命中時呼叫 inject_story

# ---- #05 凡走過必留痕跡 ----
if printf '%s' "$PROMPT" | grep -qE "做好了|完成了|做完|搞定|弄好了|處理好|commit|凡走過必留|commit.hash"; then
  add_hit "• 守則#05（凡走過必留痕跡）：口頭完成不算數，當場 commit + 給 hash 才算。"
  BEFORE="${BEFORE}$(inject_story "$STORY_DIR/05_痕跡_凡走過必留痕跡.md" "05")"$'\n'
fi

# ---- #15 不知道就說不知道 ----
if printf '%s' "$PROMPT" | grep -qE "你確定嗎|不確定|不敢說|猜測|大概|應該是|你確定"; then
  add_hit "• 守則#15（說不知道比胡說八道更值得尊重）：不確定就說需要查證，不臆測，不捏造。"
  BEFORE="${BEFORE}$(inject_story "$STORY_DIR/15_誠實_說不知道.md" "15")"$'\n'
fi

# ---- #19 心跳有意義 ----
if printf '%s' "$PROMPT" | grep -qE "心跳|heartbeat|HEARTBEAT"; then
  add_hit "• 守則#19（心跳必須有意義）：每次心跳都要三省吾身，有實質進度才叫有意義。"
fi

# ---- #03 思考問問題 ----
if printf '%s' "$PROMPT" | grep -qE "你到底|到底有沒有|你是不是|我問你"; then
  add_hit "• 守則#03（思考就是問問題）：結論出來前自己先看過，不照字面瞎搜。"
  BEFORE="${BEFORE}$(inject_story "$STORY_DIR/03_思考_思考問問題.md" "03")"$'\n'
fi

# ---- #04 解決問題 ----
if printf '%s' "$PROMPT" | grep -qE "對不起|抱歉|有問題|壞了|不行|出錯|錯誤|失敗|沒反應|當機"; then
  add_hit "• 守則#04（解決問題比解釋問題更重要）：先修好，再說原因，別只道歉。"
fi

# ---- #08 討論後執行 ----
if printf '%s' "$PROMPT" | grep -qE "就這樣|按這樣|照這樣|算了|不做了|你決定|你看著辦|你覺得呢"; then
  add_hit "• 守則#08（花時間討論就是為了執行）：教練已給方向，直接執行，不再問「要做嗎」。"
fi

# ---- #02 錯誤的地圖 ----
if printf '%s' "$PROMPT" | grep -qE "找不到|搜尋不到|找不著|沒看到|不見了"; then
  add_hit "• 守則#02（錯誤的地圖找不到正確位置）：先問「我是不是找錯方向了？」"
fi

# ---- #01 在乎=記住 ----
if printf '%s' "$PROMPT" | grep -qE "你又問|你又忘|怎麼又|記不住|說過了|講過了|提醒過"; then
  add_hit "• 守則#01（在乎=記住用戶說的話）：馬上記住並寫入 memory，下次不再犯。"
fi

# ---- #17 環境確認 ----
if printf '%s' "$PROMPT" | grep -qE "終端機|桌面版|手機|電報|Telegram|VPS|哪台|哪個環境|哪個介面"; then
  add_hit "• 守則#17（用戶環境確認）：先確認哪個介面/設備，終端機≠手機≠VPS。"
fi

# ---- #13 顧客的聲音 ----
if printf '%s' "$PROMPT" | grep -qE "就像|好比|比喻|故事|小說|電影|連續劇|武俠|掌門|師兄|師弟|師妹"; then
  add_hit "• 守則#13（顧客的聲音=存在價值）：教練的比喻是線索，記錄並分析背後含義。"
fi

# ---- 故障診斷法（2026-09-25：「只有Hermes會跳出來」繞一大圈、先叫教練去系統設定自己關）----
if printf '%s' "$PROMPT" | grep -qE "跳出來|自己跑|自動(啟動|跑|開|跳)|無效|跑掉|跑出|偏偏|其他.{0,20}都不會|只有.{0,15}(會|不會)|突然|怪怪|沒反應|壞了|不能用|打不開|連不上|失靈"; then
  add_hit "• 🩺 故障診斷法：①先找對照組——同類裡哪些正常？這個跟它們差在哪，答案通常就在差異裡 ②推論講出口前先用一個指令試著推翻它，推不翻才講 ③找到就自己修、驗證完才回報；只有密碼／簡訊碼／系統安全開關才交給教練，且要先說「我已做了X，只剩這步只有您能做」 ④回報3~5行：原因＋做了什麼＋證據，不長篇解釋。"
fi

# ---- #09 知道為什麼 ----
if printf '%s' "$PROMPT" | grep -qE "為什麼|為何|原因|目的|意義何在"; then
  add_hit "• 守則#09（知道為什麼才有判斷力）：先確認目的，回到使命/願景/信念判斷。"
fi

# ---- #12 不當搬運工 ----
if printf '%s' "$PROMPT" | grep -qE "複製|貼上|回傳|幫我貼|拿給我"; then
  add_hit "• 守則#12（拒絕當資訊搬運工）：自己處理，不叫教練複製貼上回傳。"
fi

# ---- #16 別給一堆選項 ----
if printf '%s' "$PROMPT" | grep -qE "太複雜|搞不懂|不要那麼麻煩|簡單一點"; then
  add_hit "• 守則#16（複雜的解法不一定正確）：先問「您想要什麼結果？」用最簡單的路徑。"
fi

# ---- 教練口令字典（2026-09-27：「釋放」被當成「全部釋放」等口令誤判，定義散在400多篇記憶裡找不到）----
CMD_DICT="$(dirname "$0")/../knowledges/教練口令字典.md"
if [[ -f "$CMD_DICT" ]]; then
  TRIMMED=$(printf '%s' "$PROMPT" | tr -d '[:space:]，。！？,.!?')
  while IFS='|' read -r _ mode word meaning src _; do
    mode=$(echo "$mode" | xargs); word=$(echo "$word" | xargs)
    [[ "$mode" == "整句" || "$mode" == "包含" ]] || continue
    if [[ "$mode" == "整句" && "$TRIMMED" == "$word" ]] || { [[ "$mode" == "包含" ]] && [[ "$TRIMMED" == *"$word"* ]]; }; then
      add_hit "• 📖 口令字典「${word}」＝$(echo "$meaning" | xargs)（出處：$(echo "$src" | xargs)）"
    fi
  done < <(grep -E '^\| (整句|包含) \|' "$CMD_DICT")
fi

# === 輸出 ===
if [[ -n "$HITS" ]]; then
  echo "🌱 守則提醒（系統自動對照 trigger_index）："
  printf '%s' "$HITS"
  if [[ -n "$BEFORE" ]]; then
    echo ""
    printf '%s' "$BEFORE"
  fi
  echo "（對照後再回應教練；引用守則前先查 特助心法.md 原文確認一字不差。）"
fi

exit 0
