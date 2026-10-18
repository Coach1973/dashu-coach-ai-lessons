---
name: reference-openclaw-transcripts-in-agent-sqlite
description: 小龍蝦（OpenClaw 2026.9.4）10 月起對話紀錄存在各分身的 sqlite，不是 jsonl；怎麼讀夥伴對話、查群組名、查誰說的
metadata:
  type: reference
---

- 位置：`~/.openclaw/agents/<agent>/agent/openclaw-agent.sqlite`（唯讀開：`sqlite3 -readonly`；總覽 `~/.openclaw/state/openclaw.sqlite` 的 `agent_databases`）。`agents/*/sessions/` 只剩舊的 `.reset`／`.deleted` 檔，找不到新對話別誤判成沒紀錄。
- 對話：表 `transcript_events`（`event_json`：message.role／content／`__openclaw`.senderId／senderName／transport.channel）＋ `session_windows`（`session_key`、`display_name`＝群組名、`channel`、`chat_type`）。
- 教練 ID：`6124913915`（電報）、`U895a0ad8e49d75f8303dc3d067282dc0`、`U168903487f0ba2b666ddc62b854de351`（LINE）；佩君老師電報 `8786886419`；邱裕榮 LINE `Ua52e2417c5e95d2d6ed478fa04671a58`。
- 外掛 hook 型別：`message_sending` 可 `{cancel:true}` 或改 content（`PluginHookMessageSendingResult`），`event.to` 是收件人；OpenClaw 只會刪結尾的 NO_REPLY（`tokens-*.mjs stripSilentToken`），前面文字照送。
- 這場用法：讀兩週夥伴對話盤點問題（2026-10-18，結果見接力棒與 `knowledges/特助心法21條_智能反應對照表.md`）。
