#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練說「總結」時，自動注入「收工動作清單」，觸發總結+更新接力棒+commit+push。
# 設計：對稱於 feed_junshi_handoff.sh（開工＝session開始注入六步驟），本支處理 session 結束訊號。
# 起因：2026-08-03 教練要求——以後只要說「總結」兩個字，就代表要執行「總結並上傳」全部步驟，
#       同時代表教練要開新對話框。過去教練每次都要打完整句「總結上傳，我要開新對話」，
#       現在「總結」單獨出現就該觸發同一套理解，不用教練每次重講一次。
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""')

# 觸發詞判定：整句主要是「總結」類指令才觸發，避免長句子裡順口提到「總結」誤觸發
# （例如「幫我寫一份年度總結報告」不該觸發收工流程）
if ! printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*總結[[:space:]。！!，,]*$|^總結[，,]|總結上傳|總結一下"; then
  exit 0
fi

cat <<'EOF'
🔴 教練說「總結」＝收工暗號（比照「開工」對稱設計，2026-08-03教練親定）。
讀到這句話，立即依序執行以下步驟，不用再問「要不要」：

1. 【總結本場】守則#14——把這場對話濃縮成300~500字重點：做了什麼、卡在哪、下一步是什麼
2. 【更新接力棒】N9交接鐵律——把總結寫進 JUNSHI_HANDOFF_LATEST.md 開頭「現在真正待辦」表 + 新增一棒敘述
3. 【判斷是否寫記憶】N8記憶鐵律六種情況——本場若有教訓/發現符合清單任一條，寫進 memory/試金石
4. 【commit + push】N1鐵律——完成以上更新後，commit + push，附上 commit hash 給教練
5. 【更新公開交接棒「隨身軍師」，網址 https://coach1973.github.io/ai-go/status.html 】改寫 ~/github_repos/ai-go/status.md（唯一手改來源，status.html 由 publish_public_status.sh 自動轉出不用手動改）：「最後更新」時間、「主線任務」（含下一步）、「卡在哪、已經排除的做法」、「決策紀錄」（本場教練新定案的補進去）、「最近進展」（只留最近3天）、「等教練決定」、詞彙表（本場新出現的教練口語補進去）。只寫教練自己的事——不寫帳密、主機位址、檔案路徑、別人的名字與個資與金額（會員、客戶、發票對象，要提就用代號「客戶A」）。然後跑 bash ~/.openclaw/workspace/scripts/publish_public_status.sh（先機密掃描、擋下就改掉重跑），回報時附它印出的 commit hash
6. 教練這句話同時代表他即將開新對話框——不用問「還有其他事嗎」，完成上述五步驟收尾即可回報
EOF
exit 0
