---
name: line-oa-bulk-tag-unknown-2026-11-02
description: LINE 官方帳號後台（大樹教育）清 Unknown 聊天：標籤怎麼加、為什麼 JS 假成功、免費標籤上限、沒有批次刪除
metadata:
  type: reference
---

大樹教育 LINE 官方帳號（chat.line.biz）有 909 個聊天，其中 57 個是 Unknown（已刪除／封鎖／移除）。2026-11-02 已全數加上「待清除Unknown」標籤並讀回確認，尚未刪除。

**怎麼加標籤（已實測）：**
- 聊天室右側面板：沒有標籤時有「新增標籤」連結；有系統自動標籤（如「近期沒有對話」）時該連結消失，改按旁邊的鉛筆圖示（`a.ml-1.text-oa-green` 裡的 `i.la-pen`）開同一個編輯視窗。
- 標籤輸入框用真正的 Enter 才會變成小方塊；JS 直接設值＋模擬 keydown 有時只寫入文字、沒有建立標籤。驗證：輸入後 `.bootstrap-tagsinput .tag` 數量要正確，儲存後重新開聊天室，面板 `.tag` 要有該標籤。
- 點聊天清單要點 `h6`（名字），點 `a` 或 DIV 不一定會切換聊天室。
- 安全檢查不能要求「只有一個小方塊」：既有標籤也會顯示成方塊，要改成「新增後數量＝原數量＋1」。

**限制：**
- 教練付 100 元後才能建立標籤（先前系統擋在 5 個）。
- 聊天清單沒有批次刪除：每個聊天要按「⋮」→「刪除」，要 57 次。
- 2026-11-02 我兩次報成功但其實沒存，靠重新載入才發現；之後一律以讀回為準。

**相關：** [[reference_line_quota_push_counts_per_member_registration_forward_2026-10-20]]（LINE 額度）、[[feedback_verify_only_changed_element_one_screenshot_2026-10-27]]（改完要驗證）
