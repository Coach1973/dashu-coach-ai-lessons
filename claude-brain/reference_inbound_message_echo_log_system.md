---
name: reference-inbound-message-echo-log-system
description: 訊息一進來當下就落地存底的機制，修復8/3教練訊息遺失問題，往後查「教練最後說話時間」先看這裡
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0042945d-d90c-456c-8ebb-8c6d854b1f9d
  modified: 2026-08-07T13:48:17.786Z
---

**存放位置**：`~/.openclaw/workspace/state/inbound_echo/YYYY-MM-DD.jsonl`（每行一則訊息，JSON 格式：ts/iso/agentId/channel/chatId/text，部分帶 source 欄位）

**兩個寫入來源**：
1. `~/.openclaw/hooks/inbound-message-echo-log/handler.js`（OpenClaw internal hook，事件 `message:preprocessed`，已註冊在 `~/.openclaw/openclaw.json` 的 `hooks.internal.entries`）——涵蓋小龍蝦 Telegram/LINE 收到的所有真人訊息，在 agent turn 開始處理前就同步落地
2. `~/.openclaw/workspace/scripts/log_junshi_activity_to_echo.sh`（Claude Code UserPromptSubmit hook，註冊在 `~/.claude/settings.json`）——涵蓋教練跟軍師（終端機/桌面版）的每一句話，見 [[feedback_junshi_activity_counts_as_xiaolongxia_contact]]

**下游讀取者**：`scripts/sync_coach_last_message.sh`（v3.4起）——算「教練最後一次真正說話時間」時，第一優先讀這份 echo log（用 chatId 比對教練身份：Telegram `6124913915` / LINE `u895a0ad8e49d75f8303dc3d067282dc0` / `u168903487f0ba2b666ddc62b854de351`），找不到才退回舊的 `memory/YYYY-MM-DD.md` 掃描。

**起因**：2026-08-06 教練回報「小龍蝦說我67小時沒說話，但我明明有講」。查證 `~/Library/Logs/openclaw/gateway.log`（真正的 gateway 原始日誌，不是任何中繼檔案）挖出鐵證：2026-08-03 15:58:42 教練從 Telegram 傳了一則24字訊息，gateway 收到了，但同一時段 MiniMax API 一直429限流，那輪 agent turn 疑似卡死——後續4小時完全沒回覆，訊息內容也從沒寫進 `memory/2026-08-03.md`，事後完全查不到教練當時說了什麼。舊版 `sync_coach_last_message.sh`（v3.2）只掃 memory 日記，agent turn 死掉=內容整段消失=沉默時數算錯，但這不是計算邏輯的bug，是上游資料就沒留下痕跡。

**How to apply**：
- 往後任何要跟教練報告「小龍蝦/軍師多久沒收到教練訊息」，直接查這份 echo log（或跑 `sync_coach_last_message.sh`），不要只信 `memory/*.md` 或 `heartbeat-state.json` 裡的舊快取值
- 如果發現這份 echo log 又抓不到某則已知真實存在的訊息，優先懷疑：①是不是又有 API 限流讓某輪 turn 死在收到訊息「之後」但 hook 執行「之前」的極短窗口 ②`hooks/inbound-message-echo-log/handler.js` 的欄位擷取邏輯是不是因為 OpenClaw 版本升級改了 `event.context` 欄位名稱（目前寫死用的欄位名稱已對照 `dist/message-hook-mappers-*.js` 原始碼查證過，見該檔案 `toInternalInboundMessageHookContextBase`）

Related: [[feedback_junshi_activity_counts_as_xiaolongxia_contact]]
