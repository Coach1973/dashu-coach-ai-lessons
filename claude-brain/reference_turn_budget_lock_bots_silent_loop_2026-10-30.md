---
name: reference-turn-budget-lock-bots-silent-loop-2026-10-30
description: 分身「沒反應」常是一輪跑很久一直換題目查、不回話（10/30 巴哈 70 分鐘 149 指令）；safety-locks v1.7 加悶頭鎖＋收尾鎖根治；止血用 sessions.abort＋reset
metadata:
  node_type: memory
  type: reference
  originSessionId: 69f187ed-0852-4168-84e4-c4322d41ad4f
  modified: 2026-10-30T03:51:42.497Z
---

**症狀**：教練說某分身（例：「8 號」＝巴哈，語音諧音）一直沒反應。不是當機——它在同一輪裡不停查程式，嘴上一直寫「現在收尾寫入」，但一輪沒結束，中間的話不會送到群組。
10/30 巴哈：10:22～11:48 一輪 149 次 exec，群組對話又塞到約 19 萬 token（預算 18.5 萬），每約 23 分鐘重壓縮一次。

**怎麼查**：`~/.openclaw/agents/<分身>/agent/openclaw-agent.sqlite` 的 transcript_events（mode=ro）數最後一則 user 之後的 toolCall 數、看 assistant text 有沒有反覆同一句；日誌 `/tmp/openclaw/openclaw-今天.log` grep 分身名＋overflow/lane task error（時間是 UTC 要 +8）。

**止血**：`openclaw gateway call sessions.abort --params '{"key":"agent:peipei:telegram:group:-5115910257","agentId":"peipei"}'` 再 `sessions.reset` 同參數；查 transcript 沒新事件才算停。

**根治（`extensions/safety-locks/index.js` v1.7，commit c4c155546）**：舊重複鎖只擋相同／八成像的指令，擋不到「一直換題目查」。
- 悶頭鎖：連續 30 次工具沒用 message send 對外講話 → 擋一次，要求先送進度。
- 收尾鎖：同一輪（ctx.runId，沒有就 sessionKey，閒置 10 分鐘重算）滿 30 分鐘或 200 次 → 只放行送訊息，逼它講結論＋自己選下一步。
- 門檻是 10/30 量 801 輪真資料定的：小龍蝦正常一輪最多 184 次、90% 在 29 次內；**不要改成限死 40 次**，會誤殺小龍蝦正常工作。
- 日誌關鍵字：`一輪工作計數開始`（含 ctx 欄位，確認有沒有 runId）、`悶頭鎖觸發`、`收尾鎖觸發`。

相關：[[reference-openclaw-compaction-timeout-infinite-retry-root-fix-2026-10-25]]、[[reference-openclaw-silent-long-run-ack-reaction-2026-10-30]]、[[reference-openclaw-agent-repeat-loop-and-guard-2026-10-12]]
