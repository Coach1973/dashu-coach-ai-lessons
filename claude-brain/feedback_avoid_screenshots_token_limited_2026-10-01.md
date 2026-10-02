---
name: avoid-screenshots-token-limited
description: 教練流量有限，驗證網頁盡量用文字方式(curl/DOM/數值)不要截圖看圖，截圖很耗token
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f36b59a3-f552-535f-bdca-e3da6b7ecb04
  modified: 2026-10-01T01:57:18.559Z
---

驗證網頁／格式時，優先用不看圖的方法（curl 抓 HTML 比對關鍵字、Playwright 讀 DOM 數值、API 回傳），不要截圖再用 Read 看圖。

**Why:** 教練 2026-10-01 明說看圖很消耗 token，他的流量有限，沒辦法讓我經常截圖。

**How to apply:** 只有文字檢查確實無法判斷版面（例如跑版）或教練明確要求「截圖給我看」時才截圖；其餘一律文字驗證。與 N4「親眼驗證」不衝突：用真實 Chrome 讀 DOM 也算親眼驗證。見 [[feedback_screenshot_rules_consolidated]]。
