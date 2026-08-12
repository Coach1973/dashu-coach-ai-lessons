---
name: feedback-cannot-delete-coach-line-messages
description: 測試會推播LINE/Telegram通知到教練手機的功能後，AI無法事後刪除該則訊息，測試前要先講清楚
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2cdfc226-e7f0-4f31-b7c8-9eb232aef739
  modified: 2026-08-12T02:37:39.503Z
---

2026-08-11測試event-signup報名通知管線（`sme-register-fn`）時，送出一筆標註「系統測試-請忽略」的假報名以驗證教練LINE真的收得到。教練事後要求「記得幫我刪掉」，但查證`sme-register-fn`只是單純轉發通知到LINE、不落地任何資料庫（教練先前已裁示不用查其原始碼，見[[reference_signup_notify_pipeline]]），AI沒有工具能刪除教練LINE app裡已收到的訊息。

**Why**：這類「送出即完成、無落地資料庫」的通知型測試，事後清理只能靠教練自己在LINE手動刪，AI不能假裝已處理、也不能對教練的請求悶不回應。守則#15「說不知道比胡說八道更值得尊重」同樣適用於「說做不到」。

**How to apply**：之後測試任何會推播到教練LINE/Telegram的功能（報名通知、提醒功能等），**測試前就先講清楚**「這則測試訊息我事後沒辦法刪，麻煩您自己清一下」，不要等教練事後才發現AI做不到、才臨時補充說明。同樣邏輯適用於任何AI只能「發送」不能「撤回」的外部系統。
