---
name: reference-turn-budget-lock-bots-silent-loop-2026-10-30
description: 分身「沒反應」常是一輪跑很久一直換題目查、不回話（10/30 巴哈 70 分鐘 149 指令）；safety-locks v1.7 加悶頭鎖＋收尾鎖根治；止血用 sessions.abort＋reset
metadata:
  node_type: memory
  type: reference
  originSessionId: 69f187ed-0852-4168-84e4-c4322d41ad4f
  modified: 2026-10-30T03:58:45.628Z
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

**10/30 研究結論（教練問「全世界沒人卡嗎／升級沒修嗎／赫米斯會不會比較好」）**：
- 近一個月教練為卡住開口約 24 次（向軍師 11 句＋直接催機器人 13 次，6 天）；記憶檔裡同月修過的卡住原因至少 8 種，每次不同。
- 官方 GitHub 9/30 後標題或內文含 stuck 的 issue 255 筆＝全球都有。本機 2026.9.4，最新 2026.10.9；10.2～10.8 修了多個卡住相關（訊息無限重試、工具逾時看得到、壓縮後迴圈）。升級要先把 Node 升到 24.22.1+，且 line_push_gate_patch.py 等改在 nvm 版程式的補丁要重打——待教練拍板。
- 官方內建 `tools.loopDetection` 預設關、官方建議小模型開 → 10/30 已開（5a41b6296，熱載入生效）。
- 赫米斯本身內建：max_turns 90、gateway_timeout 30 分、每 10 分回報進度、對話用到 50% 就壓縮；同樣用 MiniMax-M3。結論：赫米斯的「機制」比較好，但教練的工作（LINE／Telegram 多分身、群組綁定、行程外掛、各種鎖）全建在小龍蝦上，搬家成本大；做法是把赫米斯的機制搬進小龍蝦（v1.7＋loopDetection 已做，提早壓縮待做）。

相關：[[reference-openclaw-compaction-timeout-infinite-retry-root-fix-2026-10-25]]、[[reference-openclaw-silent-long-run-ack-reaction-2026-10-30]]、[[reference-openclaw-agent-repeat-loop-and-guard-2026-10-12]]
