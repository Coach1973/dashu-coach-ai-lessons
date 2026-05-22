---
name: 未經教練允許禁止修改openclaw.json模型設定
description: 教練明確聲明：未經允許不得更動~/.openclaw/openclaw.json中的模型設定，特別是agents.list的model欄位
type: feedback
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
教練明確禁令：**未經教練明確授權，禁止修改 `~/.openclaw/openclaw.json` 中任何模型相關欄位**。

**Why:** 教練在對話中明確說過「未經教練允許，小龍蝦那邊是不允許更改模型的」。上次因為幫 OpenCode 設定 Kimi，卻同時改動了 openclaw.json，導致小龍蝦主力模型從 minimax/MiniMax-M2.7 被換掉，造成系統全面故障。

**How to apply:**
- 幫教練設定 OpenCode → 只動 `~/.config/opencode/opencode.jsonc`
- 幫教練設定 Opcode → 只動 Opcode 的 SQLite DB 或 wrapper script
- 幫教練設定終端機 → 只動 `~/.claude/settings.json` 或 `~/.zshrc`
- `~/.openclaw/openclaw.json` 中的 `agents.list[*].model` 欄位：除非教練明說「幫我改小龍蝦的模型」，否則**一律不碰**
- 即使在排查問題時，對 openclaw.json 的任何修改都必須先徵得教練同意
