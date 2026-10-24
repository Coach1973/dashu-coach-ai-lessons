---
name: feedback-lk888-hourly-cap-raised-and-minimax-quota-burner-2026-10-25
description: 教練 10/25 00:03 說 LK888 出圖「不需要設限」→ 每小時上限 40 改 200；同晚 MiniMax Token Plan 打滿(2056)是巴哈 peipei 5 小時燒 118M token（每次呼叫約 10 萬）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7524592b-4f47-4531-b911-cb160f0d0640
  modified: 2026-10-24T16:10:01.931Z
---

10/25 00:01 LK888 收費閘門（`scripts/lk888_guard.py` MAX_PAID_PER_HOUR）一小時 40 次煞車，教練正在請巴哈大量做理監事海報，回「沒有問題，不需要設限……請繼續」。已改 200（保留煞車防暴衝，同一張 24 小時 3 次不變），commit 見 workspace 10/25。

同晚 00:06 起 MiniMax「Token Plan usage limit reached (2056)」：查各分身 sqlite（transcript_events usage 欄位，created_at 是毫秒）最近 5 小時，peipei 1158 次呼叫 118.3M token，main 只有 1.6M。原因是巴哈群組對話很長、每次呼叫帶約 10 萬 token。MiniMax 是全機共用帳號、5 小時滾動額度，花錢升級／買 Credits 只有教練能決定（教練 10/20 也定過不接備援）。

**Why:** 教練工作中被系統擋住會不高興；額度打滿的元兇要用數字講，不要猜。
**How to apply:** 再看到 2056 → 先跑同樣的 5 小時 token 統計找元兇；巴哈一批海報做完再把群組對話清掉（先備份 sqlite），避免下一批又每次帶 10 萬 token。相關：[[reference-peipei-group-context-overflow-blocks-main-lane]]、[[feedback-no-model-fallback-minimax-overload-is-their-problem-2026-10-20]]
