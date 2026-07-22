---
name: feedback-verify-channel-health-not-stale-flag
description: 監控旗標說某通道/服務壞了時，先用真相源實測(getMe等)再信，尤其會憋住對教練服務的黏著旗標
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4baaa0b3-0d69-4b71-8929-35854a8ee090
  modified: 2026-07-22T02:16:20.480Z
---

任何「通道/服務健康」的監控旗標（例如 HEARTBEAT `systemSnapshot.telegramChannelOk`），在拿它當結論或據以「停止某項對教練的服務」之前，一定要先用成本極低的真相源實測一次——Telegram 就是 `getMe` + `getChat` 一兩個 API call。不能拿一個存在 json/state 裡、可能過期的布林值當現況。

**Why:** 2026-07-22 全面體檢查到 HEARTBEAT 誤報「Telegram bot token 失效 133h+」，實測 3 個 token 全部活著、bot 到教練 chat 通道正常、polling 沒卡。這個假旗標讓系統這 5.5 天每次心跳都判斷「主動打擾撞牆、安靜結束」，把 11 項真實待辦全部憋住沒推給教練——假警報改變了 AI 對教練的行為（從此裝啞巴），比單純誤報傷害大得多，直接違反守則 #11 主動關懷。這是「盲信衍生旗標不查真相源」錯誤家族第三犯（前兩次：[[feedback_verify_activity_via_git_log_not_relay_file]] 案例52 記憶斷層、案例50 VPS polling stale）。試金石案例53。

**How to apply:** ①看到任何 `xxxOk=false`／「某功能失效 N 小時」的系統注記，先反問「這旗標是不是曾失敗一次就設 true、之後沒復驗的黏著旗標」，成本低就立刻實測真相源覆核。②設計監控旗標時，凡會觸發「停止對教練某服務」的旗標，必須配「每次心跳用真相源復驗，成立才維持、不成立立刻清掉」的機制，不能只設不清。③三個 Mac bot：bot_main=@openclaw_macbook4_bot、bot_kong=@CoachWu_openclaw_bot、bot_peipei=@coachwu_lenovo_bot；教練 chat=6124913915。
