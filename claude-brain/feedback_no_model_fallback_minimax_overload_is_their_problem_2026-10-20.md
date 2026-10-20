---
name: feedback-no-model-fallback-minimax-overload-is-their-problem
description: 教練 10/20 裁示：MiniMax 過載(HTTP 529)是對方的事，不設備援模型、不接第二家付費 API；原因＝上次自動切換後忘了切回，一天燒掉 66 美金
metadata:
  node_type: memory
  type: feedback
  originSessionId: c07a66b5-34ac-4890-a710-97b4e1d5cefb
  modified: 2026-10-20T14:25:28.488Z
---

**裁示（教練 2026-10-20 22:24 台灣時間）**：小龍蝦全部分身只用 MiniMax-M3。MiniMax 過載（HTTP 529）時，**我們不做任何事**，也不接另一個付費 API 當備援。

**Why:** 教練之前遇過一次：他明說要用 MiniMax，系統卻自動轉去別的方案，轉過去之後沒切回來，**一天燒掉 66 美金額度**。他的邏輯：①過載可能只有 5～10 分鐘，備援不知道何時該切回；②切回失敗＝默默燒錢；③他的決定是「用 MiniMax」，不是「用貴的」。跟 [[feedback-line-push-needs-coach-approval-standing-order-2026-10-20]] 同一種痛：怕「事後才發現額度被扣光」。

**How to apply:**
- 看到「AI service is temporarily overloaded／HTTP 529／overloaded_error」→ 這是 MiniMax 那端的滿載，記為「已知、不處理」，**不建議設備援、不建議換模型**，換任何說法都不再問（執行細則 N2 第 ② 關：教練答過）。
- 現況已符合他的意思：openclaw.json 沒有任何模型備援欄位，日誌每次寫 `fallbackConfigured: false`、`decision: surface_error`（錯誤直接丟給使用者）；8 個分身（main/kong/peipei/bni_tainan/jiaolian_thoughts/yijing/yang/rongshuxia）全是 `minimax/MiniMax-M3`；`models.mode: replace`。
- 之後若有人想加備援、或系統更新帶入預設備援，要當成「會燒錢」先攔下，需教練明說。

**10/20 事件事實（不必重查）：** 10:13～11:03 共 11 次對話失敗（另 07:02 一次），MiniMax 回 `HTTP 529 The server cluster is currently under high load`；每次對話系統自動重試 7～9 次、約 70 秒後放棄；Telegram 與 LINE 都受影響。佩君老師（巴哈助理群）10:57～11:02 連發 5 句全失敗，13:52 起恢復；LINE 榮樹下群 10:43～10:50 失敗 4 次，吻合邱裕榮 10:49「直接把小龍蝦移除」。11:03:43 後無再發生。

**沒做、教練沒要求（N7 只記不動）：** 失敗時給使用者看的訊息（目前多數輪次靜默無回）；連續出錯後「對話重新綁定失敗」第二層症狀（寫不進錯誤訊息）。
