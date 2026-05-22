---
name: MiniMax auth-profiles 格式鐵律
description: VPS 的 minimax auth-profiles.json 必須用 vars 格式，不得改動
type: feedback
originSessionId: fc9624b5-7d87-4cd9-9732-ba90930d30c3
---
絕對不要改動 VPS auth-profiles.json 裡 minimax / minimax-portal 的格式。

**正確格式（list + vars）：**
```json
[
  {
    "id": "minimax",
    "provider": "minimax",
    "vars": { "MINIMAX_API_KEY": "sk-cp-..." }
  },
  {
    "id": "minimax-portal",
    "provider": "minimax-portal",
    "vars": {
      "MINIMAX_OAUTH_TOKEN": "sk-cp-...",
      "MINIMAX_API_KEY": "sk-cp-..."
    }
  }
]
```

**Why:** MiniMax provider 透過環境變數注入 API Key，必須用 `vars.MINIMAX_API_KEY`。改成 `key` 格式會導致模型完全無回應。教練 MiniMax 帳號 5 小時內有 4500 次呼叫額度，流量充足，不需要改動。

**How to apply:** 未來任何修改 auth-profiles.json 的操作，只能新增其他 provider（如 google），minimax 和 minimax-portal 的 entry 保持原樣不動。
