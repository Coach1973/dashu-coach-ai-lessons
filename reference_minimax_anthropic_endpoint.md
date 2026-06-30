---
name: reference-minimax-anthropic-endpoint
description: MiniMax 提供 Anthropic 兼容 API 的正確端點。國際版 .io，中國版 .com（minimaxi）。台灣／國際環境必須用 .io，否則 cc-switch / claude-code 接不通。
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5a4bbfc2-481b-467b-b94a-aada4001c7c4
---

# MiniMax Anthropic 兼容端點

教練 2026-06-29 16:50 親口確認：cc-switch 設 minimax provider 時，端點必須用：

```
https://api.minimax.io/anthropic
```

## ❌ 不要用

```
https://api.minimaxi.com/anthropic   ← 中國版端點，台灣連不通
```

## 怎麼分辨

| 域名 | 用途 | 適用 |
|------|------|------|
| `api.minimax.io` | 國際版 | 台灣／海外環境（cc-switch 應該用這個）|
| `api.minimaxi.com` | 中國版 | 中國境內環境 |

## cc-switch 設定範本

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-cp-0_...",
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.7"
  }
}
```

## 教訓

我前面看 cc-switch db 內容是 `api.minimaxi.com/anthropic` 就當對的，沒去測「這個端點從台灣到底通不通」。`Invoke-WebRequest HEAD` 回 404 我也誤判成「正常」。

正確做法：以後看到中國服務的端點，先確認是否有 .io / .com 國際／中國版差異，再幫教練設定。

## 相關記憶

- [[feedback_local_preview_before_push]] — 同類精神：自己先驗證，不要把錯推給教練
