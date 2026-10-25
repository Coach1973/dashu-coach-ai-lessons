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

**10/26 00:25 教練糾正（我又說「額度用完」）**：教練貼 MiniMax 後台：5 小時額度只用 13%、週額度 79%。實情是額度在 10/25 22:00～23:03（台灣時間）用完過，之後恢復，但小龍蝦把帳號標成「限流冷卻」（連錯 14 次→冷卻倍增、套件寫死最長 24 小時），標記冷卻到 00:43；聊天打得過去，**整理對話卻拒用冷卻中的帳號**→對話塞爆→罷工。燒額度的元兇不是海報，是佩佩老師的「台鐵標案研究」：巴哈派小幫手，一個跑 898 步、1.29 億 token（每步約 14 萬），還陷入回報失敗重送迴圈。
**根治**：①看門員看到「probing cooldowned auth profile」或「auth candidates are temporarily unavailable」就清掉各分身的限流冷卻（`clear_rate_limit_cooldowns`，workspace 19aa8a39f，用真實副本實測過）②`agents.defaults.subagents`＝一層、同時 2 個、每個 10 分鐘（929586963，閘道已熱載入）。
**How to apply:** 教練問「為什麼不能跑」，先查各分身 sqlite `auth_profile_state` 的 cooldownUntil 與日誌最後一次 usage limit 時間，**講「額度」前必須附時間點與目前狀態**，不准用過去式的錯誤當現況。
