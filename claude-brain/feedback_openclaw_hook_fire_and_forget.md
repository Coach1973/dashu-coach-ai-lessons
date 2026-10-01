---
name: feedback-openclaw-hook-fire-and-forget
description: 小龍蝦 hook 的 event.context.inject 沒有人讀（2026.9.4 原始碼再查證）；15 支逐支分類與處置表，會員三項已搬到外掛 member-context；要讓模型看到只能用外掛 before_prompt_build
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a436a74-e350-4ac4-8d63-f3b2f2e56b45
---

OpenClaw 的 hook（`~/.openclaw/hooks/*/handler.js`）寫進 `event.context.inject` 的東西**模型看不到**。

**Why（2026-10-02 用 2026.9.4 原始碼再查證）：**
- `message:preprocessed`：`get-reply-*.mjs` 的 `emitPreAgentMessageHooks` 用 `fireAndForgetHook()` 觸發、不等；傳進去的 context 是 `toInternalMessagePreprocessedContext()` 當場新建的物件，用完就丟，整個 dist 沒有任何地方讀 `inject`。
- `agent:bootstrap`：只認 `event.context.bootstrapFiles`（group-identity 註解早寫了），`inject` 一樣無效。
- 2026-07-08 這份記憶早就寫了，但沒進 MEMORY.md 索引，10-02 的「賈維斯成長計畫」設計仍以為 `rule-reminder` 有在注入（第二次同類錯）。

**受影響的 hook（注入部分從來沒生效，記錄／直接發訊息等其他動作照常）與處置（2026-10-02 逐支分類）：**

| hook | 原本想塞給模型的 | 處置 |
|---|---|---|
| line-user-memory | 每位朋友過去的對話 | ✅ 外掛 `member-context` 讀給模型看；寫入仍由 hook 做 |
| knowledge-search-inject | 知識庫段落（jiaolian_thoughts） | ✅ 搬到 `member-context`，hook 已關 |
| bni-calendar-inject | 大台南行事曆（bni_tainan） | ✅ 搬到 `member-context`，超過 4 小時先跑同步；hook 已關（9/10 拿掉 exec 後行事曆停在 8/30，10/12 進階MSP 地點已改線上） |
| rule-reminder | 守則提醒 | ✅ 反射索引接手；BNI 官方條文＝`R-BNI-OFFICIAL-TEXT`（`agents` 限 bni_tainan／jiaolian_thoughts）、語音糾偏＝`R-VOICE-CHECK`；hook 只剩 probe log |
| rustdesk-free-memory-trigger | 釋放記憶體的真實結果 | ⏳ 第二批：模型看不到結果，可能自己編數字 |
| group-activity-memory | 「活動討論群」彙整時的完整群紀錄 | ⏳ 第二批 |
| project-card-router | 專案卡 | ⏳ 第二批 |
| auto-goal | 「執行合約」 | 暫不搬，跟反射重疊，第二批再評 |
| client-memory（agent:bootstrap） | HEARTBEAT／守則／CLIENT_PROFILE／交接／LINE 媒體網址規則 | ❌ 不搬：HEARTBEAT 本來就是啟動檔；全分身注入會把內部狀態塞給會員 |
| usage-query | 「流量」快取 | ❌ 不搬：快取 7/8 起沒更新 |
| bot-relay-inbound | 其他機器人最近發言 | ❌ 不搬：BOT_MESSAGES.md 7/8 起沒更新 |
| round-table-orchestrator | 分工群圓桌會議 | 暫不搬，未查分工群是否還在用 |
| context-overflow-guard、session-summary-trigger | — | 不用搬，早就改成直接發訊息 |
| bni-reminder-schedule | — | 不在受影響名單：它直接排程，只有註解提到 inject（10-02 更正） |

驗證：真實路徑 `openclaw gateway call agent` 假會員（bni_tainan／jiaolian_thoughts）請模型逐字貼出，📓記憶、📅行事曆、⚡會員版官方條文、📚知識庫都收到。真實 LINE 流量的 ID 格式看 `state/member_context.log`（第 3 欄頻道、第 4 欄 `sender:` 或 `session:`）。

**How to apply：**
- 要讓模型看到：寫外掛，`api.on("before_prompt_build", (event, ctx) => ({ prependContext }))`，`openclaw.json` 的 `plugins.allow` 加 id、`plugins.entries.<id>` 設 `enabled:true` 與 `hooks.allowConversationAccess:true`；新外掛要完整重啟 gateway 才掛上（熱重載不會）。範本：`~/.openclaw/extensions/reflex-prompt/`（ctx 有 agentId、senderId、sessionKey、trigger）。
- 驗證：走 `openclaw gateway call agent`（獨立測試 sessionKey、`deliver:false`），請模型逐字貼出注入段；對話存在 `agents/<id>/agent/openclaw-agent.sqlite` 的 `transcript_events`，不在 sessions/*.jsonl。
- 機制防呆：反射 R-OC-HOOK-INJECT-DEAD（改 hook 寫 inject 時自動提醒）。

相關：[[reference_openclaw_hook_inject_format]]（已過時）
