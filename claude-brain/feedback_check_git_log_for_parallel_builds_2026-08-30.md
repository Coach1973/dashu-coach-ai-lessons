---
name: feedback-check-git-log-for-parallel-builds-2026-08-30
description: 接到教練口頭構想開工前，先查相關repo的近期git log，確認有沒有其他對話框/機器已在做同一件事
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0f9618ae-e25f-4bf7-a476-73d71acabdd7
  modified: 2026-08-30T03:57:08.808Z
---

2026-08-30本場（Mac終端機）從零建置真誠分會邀約來賓系統，做到快完成才在查bni-chapters的git log時，意外發現commit `c6ce0f2`（作者CoachWU，時間戳2026-08-30 01:44:59，跟本場session開始時間幾乎重疊）——**另一個對話框幾乎同一時間收到教練類似構想，獨立在bni-chapters裡做了一份架構完全不同的實作**（整合進既有後台唯讀顯示，功能範圍只有最初版）。兩套系統各自的SQLite資料庫互不相通，教練若同時使用兩邊會看到不一樣的數字，且教練本人事前並不知道兩邊都在做。

**why 為什麼會發生**：教練習慣同時開多個對話框/機器交辦任務（Mac終端機/桌面版/聯想/ACER），同一個構想有可能同時講給不只一個session聽，而各session彼此看不到對方的工作內容，只能靠git歷史事後比對才會發現。

**how 怎麼應用**：接到「做一個新功能/新網站」這類教練口頭構想，開工前（尤其是要花大量時間力氣的建置類任務）先花一分鐘查一下最可能相關的repo（`git log --oneline -10`或`git log --since="1 hour ago"`）跟`workspace`的跨機動態注入（UserPromptSubmit hook已經會顯示「最近24小時其他機器commit」，但同一天內、同一小時內的commit有時來得及顯示、有時還沒推送上來看不到），確認沒有其他session已經在做或剛做完同一件事。發現得越早，跟教練確認方向的成本越低；本場是做到接近完成才發現，等於有一部分工是重複的。

**跟既有記憶的關係**：跟[[reference_workspace_git_concurrent_machine_race_2026-08-28]]同一種「多機/多對話框並發」根源問題，但那條講的是「同一份檔案被兩邊改到，push時衝突」，這條講的是「兩邊各自獨立做出兩份完全不同、互不相通的實作」——後者比前者更難察覺，因為git不會報merge conflict提醒你，只有主動去查log才會發現。

Related: [[reference_workspace_git_concurrent_machine_race_2026-08-28]]
