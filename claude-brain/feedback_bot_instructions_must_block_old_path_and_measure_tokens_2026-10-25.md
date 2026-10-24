---
name: feedback-bot-instructions-must-block-old-path-and-measure-tokens-2026-10-25
description: 🔴🔴🔴 最高等級：給分身（巴哈等）寫指令＝同一輪做到三件事——程式擋死舊路、讓分身真跑一次量步數與 token、清掉長對話；只寫說明檔＝巴哈繞路燒光 MiniMax 全機額度（案例133）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7524592b-4f47-4531-b911-cb160f0d0640
  modified: 2026-10-24T16:16:28.910Z
---

**事件（2026-10-24 晚～10/25 00:15）**：我替巴哈寫「做海報只跑 poster_new_person.py 一行」，只寫在 SOP／SOUL 說明。巴哈照舊習慣自己寫程式裁照片、看圖、用 gen_multi.py，一位理監事 100～118 步、400～800 萬 token，5 小時燒 1.18 億 token，00:06 MiniMax 全機額度打滿，小龍蝦和所有分身停擺，教練只能乾等。教練：「為什麼你在寫指令的時候就不能自我檢查呢？」「嚴重的低級錯誤……一次就把它做對。」要求寫進賈維斯最高等級。

**Why:** 分身不會因為說明檔改了就改做法——它帶著長對話裡的舊習慣、自己會繞路。繞一次路就燒掉全家共用的額度，代價是教練工作停擺。同類已發生 3 次（10/22、10/24 早、10/24 晚）。

**How to apply（一次到位，缺一不交付）：**
1. **擋死舊路**：在花錢／出力的那一關用程式擋（例：`lk888_guard.py` 的 `_bahai_offpath`），錯的做法跑不動，並在擋下訊息裡直接給正確那一行。
2. **真跑一次量用量**：讓分身用真資料做一次，查它的 sqlite（`transcript_events` usage、created_at 毫秒）數步數與每步 token；一件事 10 步內、每步 3 萬 token 內，超過＝它在繞路，回頭改。
3. **清長對話**：先 `sqlite3 … ".backup state/backup_…sqlite"`，再 `openclaw sessions delete --agent <id> --yes "<session key>"`。
4. 反射 `R-BOT-COMMAND-SELFCHECK`（block）會在我改 `agents/*/SOUL|AGENTS|SOP_*` 時擋下，三件做完 touch `state/BOT_COMMAND_CHECKED` 才放行。
5. 額度打滿時先量各分身 5 小時 token 找元兇（見 [[feedback-lk888-hourly-cap-raised-and-minimax-quota-burner-2026-10-25]]）。

相關：[[feedback-hand-verified-command-to-bots-not-sop-prose-2026-10-24]]、[[reference-peipei-group-context-overflow-blocks-main-lane]]
