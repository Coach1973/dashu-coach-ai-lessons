---
name: openclaw-silent-long-run-ack-reaction
description: 小龍蝦 DM「讀了沒回」不是當機，是一輪工作跑 20 分鐘沒中間回覆＋對話整理兩次各約 4 分鐘；已開 DM 收到反應（ackReactionScope=direct）與狀態反應
metadata:
  node_type: memory
  type: reference
  originSessionId: 00a6da40-62cc-48e4-bda2-0945eb871b2e
  modified: 2026-10-29T17:21:35.971Z
---

2026-10-30 01:00（台灣時間）教練在 Telegram 對小龍蝦（main 分身）說「不要一直吵」，18 分鐘沒回。查證結果：

- 沒當機。小龍蝦把那句話當成「待辦自己全做掉」，連續跑 exec／edit／子代理超過 20 分鐘，中間文字不會推送到 Telegram（只有最後回覆才送），所以教練看起來像已讀不回。
- 該輪內 main:main 對話在 186.8k／上限 184.8k token 附近，被 midTurnPrecheck 擋下整理了兩次：01:01:44→01:05:54、01:15:42→01:19:35，每次約 4 分鐘（MiniMax-M3 整理 187k token），整理後約 10 分鐘又滿。
- 預設 `messages.ackReactionScope` 是 group-mentions，DM 完全沒有「收到」反應。

已做：`openclaw config patch` 設 `messages.ackReactionScope="direct"`、`messages.statusReactions.enabled=true`（messages 熱載入，等進行中那輪結束後 line／telegram 通道重載）；備份 `workspace/state/backup_20261030_ack_reaction/openclaw.json.bak`。**尚未用真實 DM 驗證反應有沒有出現**。

沒動（待教練提起才做）：main 分身思考長度（thinking 區塊每輪 5～17KB 是對話快速變滿的主因之一，推論、未量測）、換新對話。

相關：[[reference_openclaw_compaction_timeout_infinite_retry_root_fix_2026-10-25]]
