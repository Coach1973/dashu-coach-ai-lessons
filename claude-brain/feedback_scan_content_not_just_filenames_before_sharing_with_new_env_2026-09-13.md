---
name: feedback-scan-content-not-just-filenames-before-sharing-with-new-env
description: 把正式資料複製給新/實驗性AI環境前，要grep實際文字內容找機密字串，不能只靠排除已知憑證檔名
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11a2e6f7-ce7e-4da5-b3a8-cbbc80201700
  modified: 2026-09-12T18:28:26.958Z
---

把workspace記憶/知識庫複製給一個全新、未充分驗證的環境（例如OpenClaw 2.0隔離測試實例）之前，只排除已知的憑證檔案（如`路徑大全_憑證層.md`）不夠——本場對話中討論MiniMax Key跟Telegram bot token時，`verbatim/`原始逐字稿即時記錄機制已經把這些完整明文存進當天的記錄檔，複製整個`memory/`資料夾時這些機密就跟著被複製過去，不會出現在任何憑證檔名清單裡。

**Why**：教練當場貼出的敏感資訊（API Key、bot token）會被系統的逐字稿/log機制忠實記錄下來，這些記錄檔通常散落在`verbatim/`、`terminal-notes/`、session log等非「憑證」命名的路徑裡。單純排除檔名含「憑證」「credential」的檔案，防不住這種「對話當下貼出的機密被順手記錄」的情況。

**How to apply**：任何把正式資料複製/分享給新環境（新AI實例、外部協作者、備份到別處）之前，先對複製範圍跑一次`grep`掃描常見金鑰格式（`sk-`開頭、長度異常的英數混合字串、`AAH`開頭的Telegram token格式等），而不是只靠排除已知檔名。發現命中就整份移出（用「搬到隔離區」而非直接刪除，呼應[[feedback_data_move_du_sh_verify]]同樣的搬移優先原則），複製完成後務必re-verify確認掃描結果乾淨才算完成。
