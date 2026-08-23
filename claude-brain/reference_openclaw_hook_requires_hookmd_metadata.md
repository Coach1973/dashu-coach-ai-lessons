---
name: reference_openclaw_hook_requires_hookmd_metadata
description: OpenClaw hook 光有 handler.js + openclaw.json 註冊不會生效，必須同時有 HOOK.md 宣告 metadata.events，否則載入器靜默跳過
metadata: 
  node_type: memory
  type: reference
  originSessionId: c0394d00-7e60-4062-8d89-8edafcf326b1
  modified: 2026-08-23T20:05:00.031Z
---

新增 OpenClaw internal hook 時，**三個條件缺一不可**，少任何一個都是「檔案在、設定也對、但根本沒在跑」：

1. `~/.openclaw/hooks/<name>/handler.js`（export function）
2. `openclaw.json` 的 `hooks.internal.entries.<name>` 且 `enabled: true`
3. 🔴 **`~/.openclaw/hooks/<name>/HOOK.md`，frontmatter 裡要有 `metadata: {"openclaw":{"events":["message:preprocessed"]}}`**

第 3 點是 2026-08-24 建 `invoice-inbound` 時踩到的。查 openclaw 2026.6.33 原始碼
`dist/loader-DsLw8DD3.js` 的 `loadInternalHooks()` 確認：

```js
const events = entry.metadata?.events ?? [];
if (events.length === 0) {
  log.warn(`Hook '...' has no events defined in metadata`);
  continue;          // ← 直接跳過，不載入
}
```

只有一句 `log.warn`，gateway 照常啟動、沒有錯誤、hook 就是不會跑。

**怎麼確認 hook 真的活著（唯一可信驗證）**：重啟 gateway 後比對數字——
```
grep -a "loaded .* internal hook" ~/Library/Logs/openclaw/gateway.log | tail -1
```
這個數字必須等於 `openclaw.json` 裡 `enabled:true` 的筆數。不相等就是有 hook 沒載入。
（實測當時：設定 16 支、log 只有 15 支，補上 HOOK.md 後才變 16。）

**常見 events**：`message:preprocessed`（agent 處理前，最常用）、`message:received`、
`message:sending`、`message:sent`、`agent:bootstrap`。

呼應 [[feedback_lock_must_be_hook_not_optin]]（檔案存在 ≠ 鎖有效）跟
[[feedback_settings_hook_verify]]（hook 任務要模擬觸發驗證）——同一個道理的第三種變形：
**這次是「註冊了 ≠ 載入了」**。

Related: [[project_hook_orphans_never_registered_2026-08-24]]、[[reference_mac_hook_scheduler_architecture_2026-08-12]]
