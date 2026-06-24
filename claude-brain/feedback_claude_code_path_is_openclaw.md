---
name: feedback-claude-code-path-is-openclaw
description: 給 Opus 終端機的指令必須說明：.claude-code/workspace 是 symlink，指向 .openclaw/workspace，路徑要用 .openclaw
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1d11d353-c3d3-43f9-9af7-0a36ca365cb3
---

給任何 Opus 終端機下指令時，開頭必須加這段說明：

**Why:** Claude Code CLI 的 Bash tool 預設 cwd 是 `~/.claude-code/workspace`（空目錄）。實際所有工作檔案都在 `~/.openclaw/workspace`。雖然已建立 symlink（`.claude-code/workspace` → `.openclaw/workspace`），但 Opus 終端機容易搞混，必須在指令裡明確告知。

**How to apply:** 每份給 Opus 終端機的指令，環境驗證三件套改成：

```
cd /Users/bymyway/.openclaw/workspace && pwd && ls distill/ | head -5
```

不要用 `~/.claude-code/workspace`，直接用 `~/.openclaw/workspace` 絕對路徑。

若對方回報「找不到檔案」，第一步永遠是：
「你現在的 pwd 是什麼？改用 /Users/bymyway/.openclaw/workspace 絕對路徑重跑。」
