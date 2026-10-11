---
name: reference-openclaw-agent-repeat-loop-and-guard-2026-10-12
description: 小龍蝦 10/12 凌晨每14秒重發同訊息＋重跑同生圖腳本65次以上的根因（exec 立刻回 still running＋對話內容超量）與 safety-locks v1.3 重複防呆鎖；查這類「小龍蝦當機？」的方法
metadata:
  type: reference
---

**症狀**：教練問「小龍蝦當機了嗎」，Telegram 重複收到同一則「在製作中、沒當機」約 110 則。
**真相**：閘道沒當機（launchd runs=1）。agent 的 exec 一送出就回 `Command still running (session …, pid …)`，模型下一輪覺得 02:12 的問題還沒答，又 `message send` ＋再跑 `joseph_cloth_v2.py`，每 14 秒一輪、65 次以上；對話內容 323,246 tokens（預算 184,800，route=compact_only）所以記不住剛做過。LK888 收費閘門把重複要求全擋成 cache_hit（214 筆），沒扣點。
**怎麼查（下次直接用）**：①`/tmp/openclaw/openclaw-日期.log`（JSON 行，看 telegram outbound send ok 間隔、safety-locks 偵測、model-fetch）②對話記錄在 SQLite：`~/.openclaw/agents/main/agent/openclaw-agent.sqlite` 的 `transcript_events`（session_id、seq、event_json、created_at 毫秒；用 mode=ro 開）③`state/lk888_ledger.jsonl` 查有沒有扣點。
**止血**：`openclaw sessions archive` 擋不住進行中的迴圈；要 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`（重啟前先確認 `openclaw --version` 與服務同版，案例73）。
**根治**：`extensions/safety-locks/index.js` v1.3（commit `a94d7a842`）：相同訊息（≥20字）同一對象 3 分鐘內不重發、相同長指令（timeoutSeconds≥120）10 分鐘內不重跑；記憶體內，重啟清空。**Why:** 靠模型自己別重複不可靠，機械式擋才有效。**How to apply:** 新增會真送出的工具管道時，同時想「模型重複呼叫」怎麼擋。

相關：[[reference-lk888-spend-guard-2026-09-26]]
