---
name: feedback-check-master-index-before-claiming-cant-find
description: 回報「查不到/沒有連線方式」前必須先查路徑大全等萬用索引檔；盤點類任務要窮舉底層資料結構不能只挑印象中顯眼的項目
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 653d13c6-1fa2-4eeb-9e87-fcb128d13ebe
  modified: 2026-08-02T15:42:52.798Z
---

在這個OpenClaw/小龍蝦系統裡工作時，兩條具體的自我檢查動作，缺一都會被教練當場抓到：

1. **任何「我查不到/連不上/沒辦法」的結論說出口之前，先查`workspace/路徑大全.md`跟`workspace/路徑大全_憑證層.md`**——這兩份檔案是這個系統的萬用查詢起點，VPS/Hermes的SSH密碼、各種API Key、帳密都在裡面。2026-08-02案例：SSH連VPS被拒絕就直接回報教練「查不到，需要教練給連線方式」，完全沒想到先查路徑大全，教練當場糾正「你根本是在沒有讀取開工檔案的情況底下跟我對話」。

2. **任何「盤點/列舉」類任務（幾個帳號、幾個agent、幾個網站），要對著底層資料結構（JSON物件的key、清單的item）逐一數清楚，不能只挑印象中有名稱標籤、顯眼好認的幾個**。2026-08-02案例：盤點LINE版小龍蝦有幾個帳號，`channels.line.accounts`底下明明有3個key（`default`/`bni_tainan`/`jiaolian_thoughts`），只點名了後兩個有名稱標籤的，漏算了沒有標籤的`default`（其實是教練專屬的「龍蝦小助教」），教練糾正「LINE版一共有三個，你是不是應該更新」。

**Why**：教練在這次糾正時明確拉高格局講的一句話——「你是所有資訊的大總管，是我們整個特助系統的軍師，所以你自己要想辦法完善……用你的邏輯跟系統去完成」。這不是單一任務的失誤，而是對「頂級特助如何自我要求」的期許：查證要主動、要窮舉，不能等教練一項一項提醒才補齊。

**How to apply**：這台Mac（`~/.openclaw`）上，遇到「連線資訊」問題先查路徑大全兩份檔案；遇到「盤點/列舉」問題先把相關設定物件完整dump出來數筆數，再組織成人類可讀清單。完整技術細節與教練原話見試金石案例55（`workspace/試金石/試金石_案例庫.md`）與接力棒v90（`workspace/JUNSHI_HANDOFF_LATEST.md`，commit `5dd8aad31`）。

Related: [[feedback_check_crossmachine_history_before_system_ops]]（同屬「操作前沒查現成資料就自己瞎猜」錯誤家族）
