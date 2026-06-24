---
name: reference-openclaw-hook-inject-format
description: "OpenClaw hook 的 event.context.inject 必須是 {role,content} 物件陣列，字串會被靜默忽略"
metadata: 
  node_type: memory
  type: reference
  originSessionId: cdae7e71-8e47-47bc-bf18-e9dbfee6ced3
---

# 🔴 OpenClaw Hook inject 格式鐵律

**規則**：OpenClaw hook 對 `event.context.inject` 的元素**必須是 `{ role: 'system', content: 'text' }` 物件**。
傳字串會被靜默忽略（沒錯誤，沒 log，但完全不會到 LLM context）。

## 證據

`/Users/bymyway/.openclaw/hooks/client-memory/handler.js` 範例：
```javascript
if (!event.context.inject) event.context.inject = [];
if (!Array.isArray(event.context.inject)) return;
event.context.inject.unshift({ role: 'system', content: block });
```

## RTO v0.1~v0.3 失效事故（2026-06-09 上午）

軍師寫 RTO handler 用 `event.context.inject.push(stringValue)` 連續三版（v0.1/v0.2/v0.3）都沒生效——
trajectory 裡 0 次出現「圓桌會議編排」字串。
表面看 dry-run 都正常（handler 邏輯對），但 OpenClaw 端 silent drop。

**修法**：`event.context.inject.unshift({ role: 'system', content: injection })`。

## How to apply（怎麼落地）

1. 寫新 hook 之前先看 client-memory 或 group-identity 怎麼注入
2. 注入用 `{ role, content }` 物件，role 通常是 `'system'`
3. 用 `unshift` 注入到開頭（優先級高），`push` 注入到尾（會被其他注入蓋過）
4. **驗證方式**：dry-run 不夠，要看真實 session 的 trajectory.jsonl 是否包含注入字串
5. **常見錯誤**：以為 push 字串就能注入（被靜默忽略，沒任何錯誤訊號）

關聯：[[feedback_false_success_report_pattern]]、[[feedback_settings_hook_verify]]、守則#05（commit hash 才算數，dry-run 通過 ≠ 真生效）
