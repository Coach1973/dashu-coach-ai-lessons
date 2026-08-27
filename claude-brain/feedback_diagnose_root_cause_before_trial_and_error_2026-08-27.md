---
name: feedback_diagnose_root_cause_before_trial_and_error_2026-08-27
description: 遇到API/平台權限卡住時，先查證根本原因(官方文件/開發者論壇/錯誤訊息全文)，不要靠大量UI試錯當偵錯手段
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d76b6a30-a574-4cfd-86f4-12b960d099e3
  modified: 2026-08-27T08:48:26.204Z
---

遇到「平台/API權限設定不生效」這類問題時，第一步應該是**假設網路上已經有人踩過同樣的坑**，直接搜尋官方文件、開發者論壇、錯誤訊息全文，找出根本原因後再動手；不要靠反覆排列組合的UI操作（換設定、清快取、開新分頁、重新授權）當作偵錯手段。

**Why**：2026-08-27 幫教練建FB粉專自動發文的Graph API App時，`pages_manage_posts`權限一直授權失敗。我花了大量時間/token做各種UI試錯（切換使用案例分類、手動加權限、開新分頁重試、猜測New Pages Experience限制、猜App Review需求），教練也配合按了好幾次。最後真正的根本原因，是Facebook自己在Meta Business Suite「安全中心」頁面白紙黑字寫的「商家驗證未完成」——這個資訊只要早點去查證(WebSearch或直接去看安全中心頁面)就能立刻找到，不需要繞一大圈試錯。教練當場糾正：「早一點找到嘛，浪費了大半的時間最後才找到關鍵」，並要求列入檢討。

**How to apply**：
1. 遇到「設定看起來對、但就是不生效」的平台/API問題，先做一次WebSearch查證官方說明或社群踩坑記錄，不要跳過這步直接開始試錯
2. 檢查該平台是否有專門的「狀態/安全中心/必要動作」頁面會直接列出真正卡住的原因（很多平台如Facebook/Google/AWS都有這類集中告警頁面），優先去看這些頁面而非到處點擊猜測
3. 如果已經試錯超過3-5輪還沒進展，停下來先查證根本原因，不要繼續加碼試錯
4. 跟[[feedback_junshi_token_economy_outsource]]同精神：試錯消耗的是教練寶貴的token額度，查證的成本遠低於試錯的成本，應該優先查證
