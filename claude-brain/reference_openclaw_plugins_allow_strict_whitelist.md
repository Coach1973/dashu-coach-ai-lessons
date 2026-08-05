---
name: reference-openclaw-plugins-allow-strict-whitelist
description: OpenClaw 的 plugins.allow 是全域嚴格白名單，只列幾個會關掉其他所有外掛（2026-08-05 查證原始碼）
metadata: 
  node_type: memory
  type: reference
  originSessionId: f10367e1-f282-433e-8725-54024fa4681b
  modified: 2026-08-05T01:56:59.066Z
---

# 🔴 `plugins.allow` 是「全域嚴格白名單」，不是「只管非內建外掛」

`~/.openclaw/openclaw.json` 的 `plugins.allow` 一旦有值，判斷邏輯是
（`dist/config-normalization-shared-*.js`，2026.6.33 查證原始碼）：

```
if (allow.length > 0 && !allow.includes(id)) → { enabled: false, cause: "not-in-allowlist" }
```

**沒列進去的一律關掉，內建（bundled）外掛也不例外。**

啟動警告 `[plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load`
講的是 `~/.openclaw/extensions/` 底下的外掛會自動載入，但**修法不是只列那幾個**——
接力棒原本建議只列 7 個（minimax/active-memory/memory-core/google/safety-locks/line/llama-cpp），
照做會把另外 41 個（telegram / browser / duckduckgo / anthropic / canvas …）全部關掉。

**正確做法**：白名單＝程式化取自 `openclaw plugins list --json` 裡 `status === "loaded"`
的全部 ID（2026-08-05 這台 Mac 是 48 個），不是憑印象列。改完必須重啟 gateway，
並比對 loaded 數量跟改動前一致、LINE/Telegram 通道都有 starting。

2026-08-05 已套用，commit `8b7e7dde`（`~/.openclaw` 外層 master）。
往後 `openclaw plugins install` 裝的會自動加進白名單；
手動丟進 `extensions/` 的要手動補 ID，否則會被擋（這正是白名單的用意）。

**Why**：這跟 [[試金石案例56]] 的 `toolsBySender` 萬用 deny 誤傷 cron 是同一種形狀的坑——
一條看似「加強安全」的全域規則，靠 catch-all 判斷，把不相干的功能整片打死，
而且失效方式是安靜的（沒有錯誤訊息，只是東西不見了）。

**How to apply**：看到任何 allow/deny/whitelist 型設定，動手前先查原始碼確認
「這是只管新東西，還是連既有的一起管」，再決定清單要列多完整；
套用後一定要拿「改動前的數量」當對照組驗證，不能只看有沒有報錯。

Related: [[feedback_check_master_index_before_claiming_cant_find]]、[[reference_openclaw_nested_git_repos]]
