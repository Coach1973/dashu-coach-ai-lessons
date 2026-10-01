---
name: feedback-openclaw-hook-fire-and-forget
description: 小龍蝦 hook 的 event.context.inject 沒有人讀（2026.9.4 原始碼再查證）：13 個 hook 的注入從未送到模型；要讓模型看到只能用外掛 before_prompt_build
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

**受影響的 hook（注入部分從來沒生效，記錄／直接發訊息等其他動作照常）：** rule-reminder、auto-goal、bni-calendar-inject、bni-reminder-schedule、bot-relay-inbound、context-overflow-guard、group-activity-memory、knowledge-search-inject、line-user-memory、project-card-router、round-table-orchestrator、rustdesk-free-memory-trigger、session-summary-trigger、usage-query（message:preprocessed）；client-memory（agent:bootstrap）。

**How to apply：**
- 要讓模型看到：寫外掛，`api.on("before_prompt_build", (event, ctx) => ({ prependContext }))`，`openclaw.json` 的 `plugins.allow` 加 id、`plugins.entries.<id>` 設 `enabled:true` 與 `hooks.allowConversationAccess:true`；新外掛要完整重啟 gateway 才掛上（熱重載不會）。範本：`~/.openclaw/extensions/reflex-prompt/`（ctx 有 agentId、senderId、sessionKey、trigger）。
- 驗證：走 `openclaw gateway call agent`（獨立測試 sessionKey、`deliver:false`），請模型逐字貼出注入段；對話存在 `agents/<id>/agent/openclaw-agent.sqlite` 的 `transcript_events`，不在 sessions/*.jsonl。
- 機制防呆：反射 R-OC-HOOK-INJECT-DEAD（改 hook 寫 inject 時自動提醒）。

相關：[[reference_openclaw_hook_inject_format]]（已過時）
