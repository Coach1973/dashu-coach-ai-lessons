---
name: feedback-no-screenshot-without-permission
description: 未經教練同意不可申請桌面截圖權限，curl 驗證通過即為完成，不需要截圖
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d045433-c07e-4194-8146-7178d4ce8a81
---

部署驗證時，curl grep 通過 = 驗收完成。不需要截圖，不申請桌面權限。

**Why:** 2026-05-30 部署超限戰網站後，未經教練同意擅自呼叫 request_access 申請 Safari 截圖權限。教練質問「沒有經我同意，為何截圖？」。守則提醒有注入但沒有被對照執行——「感覺對」≠「守則允許」。

**How to apply:** 每次準備呼叫工具前，先問三個問題：
1. 教練明確要求這個動作了嗎？
2. 這個動作超出原始任務範圍了嗎？
3. 現有的驗證方式已經夠了嗎？
三個問題任何一個讓步驟多餘，就不執行。
