---
name: feedback-openclaw-hook-fire-and-forget
description: OpenClaw message:preprocessed 內部 hook 是 fire-and-forget，inject 不被消費，不能用來注入 prompt
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a436a74-e350-4ac4-8d63-f3b2f2e56b45
---

OpenClaw 的 `message:preprocessed` 內部 hook 是 fire-and-forget（發完不等回），`event.context.inject` 推的數據**不會被模型看到**。

**Why:** Gateway 原始碼 `get-reply-9dLyvuw9.js:3610` 用 `fireAndForgetHook()` 包裹 `triggerInternalHook()`，不 await。Hook 修改 inject 時，gateway 已經開始建 prompt 送模型了。

**How to apply:** 要讓小龍蝦在 Telegram 回應特定指令，用 SOUL.md 指令方式（讓模型自己讀檔）比 hook inject 可靠。如果未來要做 hook 注入，需要用 plugin API 的 `api.on('before_agent_reply', handler)` 或 `api.on('before_prompt_build', handler)`——這些是 awaited 的 global hook。

相關：[[feedback_netlify_deploy_zip_api]]（手動推送的另一個坑）
