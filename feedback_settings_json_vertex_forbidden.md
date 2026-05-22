---
name: settings.json 禁止加 CLAUDE_CODE_USE_VERTEX 或 ANTHROPIC_ API vars
description: settings.json 的 env 會覆蓋 claude-easyclaude 的設定，導致 Opcode 報 Google ADC 錯誤；ANTHROPIC_ vars 應只放在 ~/.zshrc
type: feedback
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
**規則：`~/.claude/settings.json` 的 `env` 區塊絕對不能加以下任何 key：**
- `CLAUDE_CODE_USE_VERTEX`（或任何 `CLAUDE_CODE_USE_*`）
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL`
- `ANTHROPIC_SMALL_FAST_MODEL`

settings.json 的 `env` 區塊只能保留：
```json
{
  "API_TIMEOUT_MS": "3000000",
  "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
}
```

**Why:** settings.json 的 env 會被 claude binary **無條件覆蓋**到 process env 上（即使 process env 已有同名 var）。Opcode 用 `claude-easyclaude` wrapper 設定 EasyClaude URL，但 settings.json 的 MiniMax vars 蓋掉了它。Opcode（20人民幣 Claude）為修終端機「Not logged in」把 `CLAUDE_CODE_USE_VERTEX=true` 加進去，導致 claude binary 嘗試 Google Vertex AI 認證，沒有 ADC 憑證就報 "Could not load the default credentials"。MiniMax vars 已在 `~/.zshrc` → 終端機照常，settings.json 不需要重複設定。

**How to apply:**
- 任何想修終端機 API routing 的問題 → 改 `~/.zshrc`，不動 settings.json
- settings.json 只放與 claude CLI 行為相關的 flag（timeout、telemetry 等）
- 不論什麼理由，絕對不在 settings.json 加 `CLAUDE_CODE_USE_VERTEX`
