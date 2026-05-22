---
name: 各工具設定檔隔離鐵律
description: OpenCode/Opcode/終端機/OpenClaw四個系統設定檔完全獨立，操作時只能動對應的那一個
type: feedback
originSessionId: 8238ddb0-2252-48fc-9e7f-9159d991b108
---
四個工具的設定檔是完全獨立的，操作時絕不能跨界：

| 工具 | 設定位置 |
|------|----------|
| OpenCode | `~/.config/opencode/opencode.jsonc` |
| Opcode | Opcode 專屬 SQLite DB（用 `claude-easyclaude` wrapper script）|
| 終端機（Claude CLI）| `~/.claude/settings.json` + `~/.zshrc` |
| 小龍蝦（OpenClaw）| `~/.openclaw/openclaw.json` |

**Why:** 上次設定 OpenCode 接 Kimi 時，助教同時誤改了 `~/.openclaw/openclaw.json`，把小龍蝦主力模型換掉，導致所有 Telegram 對話都失敗（embedded agent 拿錯模型）。

**How to apply:** 接到任何設定任務前，先確認目標工具對應哪個設定檔，只動那一個，不看、不改其他設定檔。
