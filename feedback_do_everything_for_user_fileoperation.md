---
name: do-everything-for-user-file-operation
description: 幫電腦小白處理「找檔案/授權/設定」類任務時，必須先全自動化（開Finder選好、開設定頁），再給最簡單的一個動作，絕對不給多步驟技術指令
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4372e3fe-3c72-49c1-87bb-37aee134a0f0
---

教練是電腦小白。幫他處理需要「找檔案 / 開設定 / 授權 App」的任務時，必須先把 AI 能做的全做完，再告訴他**只剩一個動作**。

**Why（血淚教訓，2026-05-23）：**
RustDesk 螢幕錄製授權問題。我診斷出問題後，給教練一套「按 + 鍵 → Cmd+Shift+G → 輸入路徑 → 點 Open」的技術步驟。教練完全看不懂，被卡了三個來回才解決。正確做法是：第一時間就跑 `open -R /Applications/RustDesk.app`（Finder 直接選好），然後告訴他「把那個圖示**拖進**設定清單」——一個動作搞定。

**How to apply（場景觸發規則）：**
- 只要任務涉及「找某個 App 或檔案」→ 立刻 `open -R <路徑>` 在 Finder 展開並選好，不要叫教練自己輸入路徑
- 需要授權 App（隱私權/螢幕錄製/輔助使用）→ 先 `open x-apple.systempreferences:...` 開好設定頁，再開 Finder，告訴他「拖過去」而不是「按 +」
- 不要出現 Cmd+Shift+G、路徑字串、「前往資料夾」這類字眼——教練聽不懂
- 判斷自己有沒有做到：如果給出的步驟超過 1 個且有技術名詞，就是沒做到，重想
- 關聯：[[feedback_do_everything_for_user]]、[[feedback_plain_chinese_no_jargon]]
