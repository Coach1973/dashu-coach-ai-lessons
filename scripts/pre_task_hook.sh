#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練每發一句話，自動偵測關鍵字，注入相關「特助守則」提醒到 context。
#       讓守則對照「不靠模型記得、靠系統強制」——這是自動化執行計劃第一步。
# 設計：與 feed_junshi_handoff.sh 不同，守則對照要「每輪 prompt 都檢查」，
#       但只在命中關鍵字時才輸出（不命中則靜默），避免雜訊與炸 token。
# 依據：knowledges/01_knowledge_base/trigger_index.md 的觸發對照表
# 軍師建立 2026-05-27（教練拍板「把紅色優先做好」）
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$PROMPT" ]] && exit 0

HITS=""
add_hit() { HITS="${HITS}$1"$'\n'; }

# === 關鍵字 → 守則對照（依據 trigger_index.md）===

# #08 討論後執行（「開工」交給 feed_junshi 處理，此處不重複）
if printf '%s' "$PROMPT" | grep -qE "就這樣|按這樣|照這樣|算了|不做了|你決定|你看著辦|你覺得呢"; then
  add_hit "• 守則#08（花時間討論就是為了執行）：教練已給方向，直接執行，不再問「要做嗎」。"
fi

# #05 commit hash
if printf '%s' "$PROMPT" | grep -qE "做好了|完成了|做完|搞定|弄好了|處理好"; then
  add_hit "• 守則#05（凡走過必留痕跡）：口頭完成不算數，當場 commit + 給 hash 才算。"
fi

# #04 解決問題
if printf '%s' "$PROMPT" | grep -qE "對不起|抱歉|有問題|壞了|不行|出錯|錯誤|失敗|沒反應|當機"; then
  add_hit "• 守則#04（解決問題比解釋問題更重要）：先修好，再說原因，別只道歉。"
fi

# #02 錯誤的地圖
if printf '%s' "$PROMPT" | grep -qE "找不到|搜尋不到|找不著|沒看到|不見了"; then
  add_hit "• 守則#02（錯誤的地圖找不到正確位置）：先問「我是不是找錯方向了？」"
fi

# #01 在乎=記住
if printf '%s' "$PROMPT" | grep -qE "你又問|你又忘|怎麼又|記不住|說過了|講過了|提醒過"; then
  add_hit "• 守則#01（在乎=記住用戶說的話）：馬上記住並寫入 memory，下次不再犯。"
fi

# #17 環境確認
if printf '%s' "$PROMPT" | grep -qE "終端機|桌面版|手機|電報|Telegram|VPS|哪台|哪個環境|哪個介面"; then
  add_hit "• 守則#17（用戶環境確認）：先確認哪個介面/設備，終端機≠手機≠VPS。"
fi

# #13 顧客的聲音（比喻/故事是線索）
if printf '%s' "$PROMPT" | grep -qE "就像|好比|比喻|故事|小說|電影|連續劇|武俠|掌門|師兄|師弟|師妹"; then
  add_hit "• 守則#13（顧客的聲音=存在價值）：教練的比喻是線索，記錄並分析背後含義。"
fi

# #09 知道為什麼
if printf '%s' "$PROMPT" | grep -qE "為什麼|為何|原因|目的|意義何在"; then
  add_hit "• 守則#09（知道為什麼才有判斷力）：先確認目的，回到使命/願景/信念判斷。"
fi

# #04 交付前驗證（上傳/部署）
if printf '%s' "$PROMPT" | grep -qiE "上傳|部署|deploy|github|上線|發布|push 上去"; then
  add_hit "• 守則#04（交付前驗證）：上線/部署後先用 curl 檢測 HTTP 200，再說「完成」。"
fi

# #12 不當搬運工
if printf '%s' "$PROMPT" | grep -qE "複製|貼上|回傳|幫我貼|拿給我"; then
  add_hit "• 守則#12（拒絕當資訊搬運工）：自己處理，不叫教練複製貼上回傳。"
fi

# #16 別給一堆選項
if printf '%s' "$PROMPT" | grep -qE "太複雜|搞不懂|不要那麼麻煩|簡單一點"; then
  add_hit "• 守則#16（複雜的解法不一定正確）：先問「您想要什麼結果？」用最簡單的路徑。"
fi

# === 輸出 ===
if [[ -n "$HITS" ]]; then
  echo "🌱 守則提醒（系統自動對照 trigger_index）："
  printf '%s' "$HITS"
  echo "（對照後再回應教練；引用守則前先查 特助心法.md 原文確認一字不差。）"
fi

exit 0
