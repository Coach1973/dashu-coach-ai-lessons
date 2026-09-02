---
name: reference_parallel_background_agents_shared_browser_contamination_2026-09-02
description: 同時開多個背景Agent各自用claude-in-chrome操作瀏覽器時，若共用同一個分頁會互相覆蓋navigate結果，造成資料污染風險
metadata: 
  node_type: memory
  type: reference
  originSessionId: b5eadffb-228e-4bea-97d2-aebdae1e4788
  modified: 2026-09-02T12:57:12.109Z
---

同時委派多個背景 Agent 各自用 claude-in-chrome 查 BNI Connect（每人一批筆數），若他們沿用系統預設回傳的同一個 tabId（例如 `list_connected_browsers`/`tabs_context_mcp` 傳回的既有分頁），會出現**分頁互搶**：Agent A 剛 navigate 到某個 cert_id 頁面，Agent B 幾乎同時 navigate 到別的 cert_id，A 接著讀到的其實是 B 剛導覽過去的內容，讀到「別人的證書」。

**Why**：claude-in-chrome 的分頁是跨 Agent 共用的資源，多個 Agent 若沒有各自建立專屬分頁（`tabs_create_mcp`），預設會操作到同一個既有 tabId，navigate 是非同步的，誰先誰後在毫秒級別無法保證。

**How to apply**：
1. 委派多個平行背景 Agent 各自處理一批瀏覽器抓取任務前，指示每個 Agent 第一步先 `tabs_create_mcp` 開自己專屬的新分頁，全程只用該 tabId，不要用系統回傳的既有/共用 tabId。
2. 每筆資料抓回後，要求 Agent 核對頁面回傳的「編號/ID」欄位是否跟目標一致，不一致就不寫入資料庫、回報異常，這是最後一道防線（2026-09-02 三批 BNI 信用証補公司欄位任務裡，靠這道核對機制擋下了所有可能的錯誤寫入）。
3. 若一開始沒交代要開專屬分頁，事後可以補一則訊息告知「其他 Agent 已完成並關閉分頁，衝突源已排除，請開新分頁繼續」，讓卡住的 Agent 恢復執行。

Related: [[feedback_delegate_bulk_browser_ops_to_background_agent_2026-08-27]]（同樣是委派背景Agent做大量瀏覽器操作，那次是單一Agent循序處理，這次是多Agent平行處理才踩到新坑）
