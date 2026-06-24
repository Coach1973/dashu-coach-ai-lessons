---
name: mac
description: 教練 Mac 上三個 CLI 工具（hermes/opencode/claude）各自獨立 API key 與模型，加上 Claude Desktop APP 共用對話記錄但介面不同
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 53f39dea-1322-4a61-8db0-f08edafe8233
---

教練的 Mac 終端機（CLI，黑底框框）上有三個獨立 AI 工具，打不同指令就叫不同的出來，各自有獨立的 API key、設定檔、模型：

| 終端機指令 | 背後的工具 | 模型（2026-06-03） | 設定檔位置 |
|-----------|-----------|-------------------|-----------|
| `hermes` | Hermes Agent | MiniMax M3 | `~/.hermes/config.yaml` + `~/.hermes/auth.json` |
| `opencode` | OpenCode | DeepSeek V4 Pro | `~/.config/opencode/opencode.jsonc` |
| `claude` | Claude Code CLI | CC Switch 安排的模型 | `~/.claude/settings.json` |

另外還有一個 **UI 介面**（不是終端機）：
- **Claude Code Desktop APP**（桌面上的應用程式）= UI 介面
- 跟 Claude Code CLI **共用同一份對話記錄**，但介面不同
- **CC Switch 同時控制** Claude CLI 和 Claude Desktop APP 的模型

**🔴 Claude Desktop APP 完整能力對比表（教練 2026-06-03 + 2026-06-17 兩次親述定稿）：**

| 項目 | CLI（終端機版，黑底） | Desktop App（GUI 桌面版，能力同等或更強） |
|------|------------------|----------------------------------|
| 介面 | 純文字終端機 | 圖形 GUI，側邊欄、拖拉窗格、視覺化 |
| 視覺化 | 基本文字 diff | 內建視覺 diff、檔案樹、即時預覽、Markdown 渲染 |
| 多 session | 要 tmux / 多視窗 | 側邊欄一窗多任務 |
| 看歷史對話 | 進 jsonl 檔讀 | 點側邊欄 |
| 切換模型 | `/model` 指令 | 滑鼠選 + 推理強度 |
| 自動化 / 腳本 | ✅ 強（headless / CI/CD / CLI flag）| 較弱（互動為主）|
| 最新功能 | 通常最早拿到 | 較完整但稍慢 |
| 資源消耗 | 輕量、可背景跑 | 較重但視覺工具豐富 |
| 平台 | macOS / Linux / Windows（含 WSL）| macOS / Windows（無 Linux 原生）|
| **互相切換** | CLI 中打 `/desktop` 直接跳到 Desktop | — |
| **底層工具能力** | Bash / Read / Edit / Write 全套 | **完全相同**——一樣有 shell、能讀寫檔、git push、跑 PowerShell |
| **CLAUDE.md 燒錄檔** | `~/.claude/CLAUDE.md`（Mac）/ `%USERPROFILE%\.claude\CLAUDE.md`（Win）| **共用同路徑** |
| **同台機器對話記錄** | `~/.claude/projects/.../jsonl` | **共用同一份 jsonl** |
| **CC Switch 控制** | 是 | 是（兩者同步切模型）|

**🔴 鐵律：永遠不要再以為 Desktop App「沒有 shell、純聊天」——它跟 CLI 是同源產品，能力相同甚至 GUI 更強。**

再加上 Telegram 端：
- **小龍蝦（OpenClaw）** → `~/.openclaw/openclaw.json`（MiniMax M3）

**Why:** 教練已親述三次（2026-05 / 2026-06-03 / 2026-06-17），第三次特別丟官方文件 + Grok 對比表釐清。我若再記不住，就是踩守則 #01「記不住=不在乎」+ #07「同處跌倒」。

**How to apply:**
1. 接到「Desktop App」「Windows 桌面版 Claude」等字眼 → **先讀本檔，不要憑舊印象瞎答**
2. 接到設定任務先問：要動哪個工具？→ 只改對應的設定檔
3. 「終端機」教練可能指 hermes / opencode / claude 哪一個 → 要追問
4. Claude CLI 和 Claude Desktop App 是不同介面**但工具能力相同** → 不要再說 Desktop 沒手
5. 模型現況會變，但「各自獨立」的架構不會變
