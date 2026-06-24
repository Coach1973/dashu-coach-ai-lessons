---
name: Hermes 接第三方 Anthropic 代理服務的正確方法
description: aiprimetech 代理封鎖 x-stainless-* headers，需修改 anthropic_adapter.py 加 hook 過濾；附 MiniMax vs aiprimetech 差異對比
type: feedback
originSessionId: 0d047e5b-f32f-438b-bf9b-ee1440e905b1
---
## 根本原因

代理服務（如 aiprimetech unlimited.aiprimetech.io）的 WAF 封鎖了 Anthropic SDK 自動加上的兩個 header：
- `x-stainless-*` telemetry headers（x-stainless-lang、x-stainless-os 等）
- `user-agent: Anthropic/Python x.x.x`

curl 直接打沒問題（不帶這些 headers），但 Hermes 走 anthropic SDK 就 403。

## 解法：修改 Hermes source code

檔案：`~/.hermes/hermes-agent/agent/anthropic_adapter.py`
函數：`build_anthropic_client`，在 `_is_third_party_anthropic_endpoint` 分支加入 httpx event hook：

```python
try:
    import httpx as _httpx_mod
    def _sanitize_headers(req: "_httpx_mod.Request") -> None:
        for _k in [k for k in req.headers.keys() if k.lower().startswith("x-stainless-")]:
            del req.headers[_k]
        if req.headers.get("user-agent", "").lower().startswith(("anthropic/", "openai/")):
            req.headers["user-agent"] = "python-httpx/0.27"
    kwargs["http_client"] = _httpx_mod.Client(
        event_hooks={"request": [_sanitize_headers]},
        timeout=_httpx_mod.Timeout(600.0),
    )
except Exception:
    pass
```

## config.yaml 正確設定

```yaml
model:
  default: claude-opus-4-7
  provider: anthropic
  api_mode: anthropic_messages
```

custom_providers 裡放一條（key_env 指向 .env 的變數）：
```yaml
- name: aiprimetech
  base_url: https://unlimited.aiprimetech.io
  key_env: ANTHROPIC_AUTH_TOKEN
  api_mode: anthropic_messages
```

## .env 必加的變數

```
ANTHROPIC_BASE_URL=https://unlimited.aiprimetech.io
ANTHROPIC_AUTH_TOKEN=sk-...
ANTHROPIC_API_KEY=sk-...
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
CLAUDE_CODE_ATTRIBUTION_HEADER=0
```

## auth.json 的陷阱

- Hermes 每次 403 就把 credential 標記 `last_status: exhausted`，之後跳過不送
- 改完設定後必須清 exhausted：`hermes auth reset anthropic` 或手動 python3 清除
- `hermes auth remove` 同時會把 .env 裡對應的 key 清掉並 suppress，小心

## MiniMax vs aiprimetech 差異

| | MiniMax | aiprimetech |
|---|---|---|
| base_url | https://api.minimax.io/anthropic | https://unlimited.aiprimetech.io |
| /anthropic 後綴 | 有（Hermes 自動識別 api_mode）| 無 |
| stainless headers | 允許 | 封鎖（403）|
| user-agent | 允許 | 封鎖（403）|
| 設定難度 | 簡單（只換 key）| 需改 source code |

**Why:** 這個 bug 排查花了數小時，來回送測超過 10 次，根本原因在代理服務的 WAF 封鎖 SDK telemetry headers，而不是 key 或 URL 問題。

**How to apply:** 未來接任何第三方 Anthropic-compatible 代理時，先用 curl 加上 x-stainless-* headers 測試是否被擋。如果被擋，套用上述 hook 修法。
