---
name: reference-bni-palms-vs-detail-report-discrepancy
description: BNI Connect「分會-PALMS摘要報告」跟「地區-查看來賓/分會訪問報告」的「來賓」數字口徑不同，PALMS才是官方認證數字
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f78a0b4-707b-4ef1-b821-93e5f2584e4f
  modified: 2026-09-01T02:53:57.401Z
---

BNI Connect有兩種報表都能查「來賓」數字，但統計口徑不同，數字差很多（真鑽分會實測：郭政輝明細報表只有106筆，PALMS官方認證是303筆，落差原因未查證出來，可能是明細報表只記錄「Invited By」欄位有匹配到的部分邀約，PALMS涵蓋更廣）：

- **「分會-PALMS摘要報告」**：官方績效指標報表，可自訂「從/至」日期，每份是**固定期間的累積總數快照**（不是逐筆明細），第13欄「來賓」是官方認證數字，第59列（最後一列）「總數」是官方宣告的總計。
- **「地區-查看來賓」／「分會訪問報告」**：逐筆明細報表，含每一筆的訪問日期+Invited By欄位，可以做任意時間窗篩選，但總數比PALMS少很多。

**How to apply：** 之後任何需要「某人邀了幾位來賓」這種準確數字的任務，一律用PALMS報表當資料源，不要用明細報表（除非只是要抓「日期」這種PALMS沒有的欄位，且知道數字會偏低）。PALMS報表要多個時間窗就要教練逐一匯出多份（同一個「至」不同「從」），這些快照天生是巢狀（近N個月的快照必然包含近N-1個月全部資料），可以用來反推子區間差值，也可以直接把每份快照當一個時間窗選項使用，不需要95份逐月匯出。詳見 [[project_bni_training_guests_dashboard_2026-09-01]]（若有建立）。
