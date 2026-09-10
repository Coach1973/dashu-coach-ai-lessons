---
name: reference-invoice-inbound-heartbeat-disguise-2026-09-10
description: "invoice-inbound hook誤報bug二度發作——9/6修法靠channel==='heartbeat'排除心跳事件，但心跳排程改偽裝成channel='telegram'/chatId=教練真實ID後排除完全失效，改成偵測文字內容本身的固定prompt特徵才根治"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 939403d3-b038-4842-82cf-6e7e35bacb99
  modified: 2026-09-10T14:28:43.368Z
---

`hooks/invoice-inbound/handler.js`（教練傳的發票統編/載具當下落地不靠agent記得）連續兩次因同一根因誤報：每30分鐘一次的心跳健檢prompt（"Read HEARTBEAT.md if it exists..."）裡的系統狀態文字（如"0 INVALID_API_KEY"，其中"INVALID"恰好是7碼大寫英文字母）被手機發票載具正則`/[A-Z0-9.\-+]{7}/`誤判成真的發票資訊，寫進`state/invoice_inbox/`並發靜音Telegram通知。

**第一次(2026-09-06，commit`d5adde4fd`)**：查到心跳事件的`channel`/`chatId`欄位固定是字串`'heartbeat'`，直接排除`resolveChannel(event)==='heartbeat'`。9項測試全過，教練當場確認不再誤報。

**第二次(2026-09-10)**：教練半夜連14次(9/9 23:07~9/10 03:36)又收到同款亂碼通知。查`state/invoice_inbox/2026-09.jsonl`發現9/6的記錄`channel`確實是`heartbeat`，但9/9晚上起的記錄`channel`變成`telegram`、`chatId`變成教練真實ID`6124913915`——**心跳排程本身的事件標示方式改了**（可能OpenClaw版本升級或心跳觸發機制調整），讓它跟教練真的用Telegram講話在`channel`/`chatId`欄位上完全無法區分，9/6的排除邏輯因此失效。

**根治**：不再依賴`channel`/`chatId`這種容易隨系統版本改變格式的間接欄位，改成直接偵測**文字內容本身**是否為心跳排程固定注入的prompt模板（正則比對開頭`/^Read HEARTBEAT\.md if it exists/`）。這個特徵是心跳排程寫死的模板字串，不會因為事件標示方式改變而跟著變。

**Why**：用「事件的中繼資料（channel/chatId/sessionKey）」判斷「這是不是心跳」是脆弱的，這些欄位是系統內部實作細節，會隨版本升級改變含義；用「訊息內容本身有沒有某個固定特徵」判斷更穩固，因為那是業務邏輯層的事實，不受底層事件系統怎麼包裝影響。

**How to apply**：
1. 任何hook要排除「這是系統自動觸發，不是真人在講話」的情境，優先看訊息**內容特徵**（固定prompt開頭、固定格式），其次才考慮channel/chatId這類中繼資料，且中繼資料判斷要當作輔助防護，不能是唯一防線
2. 這類「誤報bug修好又復發」的情況，第一步先比對兩次的原始log數據（`state/invoice_inbox/`這類落地檔案），找出「哪個欄位變了」，不要假設是同一個修法失效要重寫全部邏輯——往往只是某個判斷依據本身不穩固
3. 相關程式碼：`hooks/invoice-inbound/handler.js`（`.openclaw`外層repo，commit`5dd58e7bf`）、測試`scripts/test_invoice_inbound_hook.js`（workspace repo，commit`d5dc5ee91`）

Related: [[reference_openclaw_repo_dual_branch_trap_2026-09-10]]（同一輪修復裡踩到的另一個獨立教訓，git分支混淆）
