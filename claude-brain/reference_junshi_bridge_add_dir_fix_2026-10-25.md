# 派工橋 claude -p 沙盒要加 --add-dir 才讀得到 github_repos（2026-10-25）

## 觸發情境

教練 2026-10-25 16:08 在 Telegram 交辦「林家旭 RESUME3 補件轉交軍師」，
我走任務橋（`state/JUNSHI_TASK_QUEUE` → `scripts/junshi_task_worker.sh`）派給軍師。
軍師回報**卡關**，錯誤訊息：

> For security, Claude Code may only list files in the allowed working directories for this session

軍師讀不到 `/Users/bymyway/github_repos/charles-lin/index.html`，`ls` 都被擋，
所以 `index.html` 一個字都沒改（他誠實回報，沒有假裝做完）。

## 根因

`junshi_task_worker.sh` 原本這樣呼叫：

```bash
TASK_OUTPUT=$("$CLAUDE_CLI" -p "$PROMPT" --permission-mode acceptEdits --output-format text ...)
```

`claude -p` 的允許存取範圍 = **當前工作目錄**（本次是 `~/.openclaw/workspace`）。
`github_repos/` 在 workspace 外面，所以整個 repo 對軍師不可見。
這跟「有沒有真的桌面版 Code 分頁」無關 —— 是 CLI 沙盒預設範圍問題，
透過手機 Remote Control 連進來反而不是重點。

## 修法（已落地並實測）

在 `scripts/junshi_task_worker.sh` 的 claude 呼叫列加 `--add-dir`：

```bash
TASK_OUTPUT=$("$CLAUDE_CLI" -p "$PROMPT" \
    --add-dir /Users/bymyway/github_repos \
    --add-dir /Users/bymyway/.claude-code/workspace \
    --add-dir /Users/bymyway/.openclaw/workspace \
    --permission-mode acceptEdits --output-format text 2>"$TASK_STDERR" | tail -c 3000) || true
```

`--add-dir` 是「把這個目錄加入允許存取清單」，不是提權，適合派工橋這種
「軍師要跨 repo 改檔」的用途。

### 實測驗證（不能只看有沒有加參數）

用完全相同的參數實跑一次 `claude -p`，要它列出 charles-lin 底下的檔名：

```
index.html
原始照片
```

→ 讀得到，根因確認解除。

## 兩個要注意的細節

1. **兩份腳本是同一個 inode（hardlink）**
   `~/.openclaw/workspace/scripts/junshi_task_worker.sh` 與
   `~/.claude-code/workspace/scripts/junshi_task_worker.sh` inode 同為 `50426503`
   （`ls -li` 驗證過），改一份兩份同步生效，不用另外同步。
   `cp` 會回報 `are identical (not copied)`，這是正常的。

2. **改完腳本後 git 顯示「沒改動」不是幻覺**
   workspace 有 session-end 自動同步機制，會在幾十秒內自己 commit
   （本次是 `e58d40fd7 [Mac] session-end 自動同步 2026-10-25 16:35`，HEAD 已含 `--add-dir`）。
   所以 `git diff` 空、`git add` 沒東西可加 → 查 `git log --oneline -3` 就會看到自動 commit。

## 教訓

- 軍師回報「卡在環境限制」時，**先看錯誤訊息指向哪個限制**，不要直接照他的建議
  開新 session 等下次 —— 派工橋本身可以修。
- 派工橋類的「跨 repo 執行」場景，`claude -p` 一定要帶 `--add-dir`，
  否則永遠只能在 workspace 裡打轉。

<!-- project: github.com/Coach1973/mac-openclaw-workflows -->
