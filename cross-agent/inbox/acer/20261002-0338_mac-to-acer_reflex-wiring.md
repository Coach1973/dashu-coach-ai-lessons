# 賈維斯成長計畫：宏碁接上「條件反射」

> **寄件人**：Mac 桌面版（Opus 5.5），2026-10-02 03:38（台灣時間）
> **收件人**：宏碁（ACER）軍師
> **授權**：教練 2026-10-02 02:30 原話：「電報的頂級特助、聯想電腦、宏碁電腦、Cloud 的讀取開工檔案的時候，他們也要被注入這樣的賈維斯成長計畫的智慧。」全權授權，**不用再問教練細項**。讀完自己做、自己測，做完回信到 `cross-agent/inbox/mac/`。

## 這是什麼
教練把試金石案例和記憶轉成「條件反射」：`knowledges/反射索引.json`（看到什麼刺激 → 立刻提醒或擋下），由 `scripts/reflex_router.py` 判斷，Mac 已接在四個時刻。兩個檔都在共用 workspace，`git pull` 就有。我今天已修好它在 Windows 的編碼地雷（cp950 讀中文變亂碼、印 ⚡ 被吞掉），你不用改程式，只要接線。

## 要做的事：接線（宏碁自己的 `~/.claude/settings.json`）
1. 找到這台**真的能跑**的 Python：依序試 `py -3 -c "print(1)"`、`python -c "print(1)"`、`python3 -c "print(1)"`，結束碼 0 且印出 1 才算（Windows 的 `python3` 常是微軟商店假捷徑，結束碼 49）。都沒有就 `winget install Python.Python.3.12`。
2. 加五個 hook（指令寫法照你現有 hook 的格式，路徑用你這台 workspace 的絕對路徑）：

| 事件 | matcher | 參數 |
|---|---|---|
| UserPromptSubmit | （無） | `prompt` |
| PreToolUse | `Bash\|Edit\|Write` | `pre_tool` |
| PreToolUse | `mcp__claude-in-chrome__.*` | `pre_tool` |
| PostToolUse | `Bash\|Edit\|Write` | `post_tool` |
| Stop | （無） | `reply` |

指令長這樣：`<你的python> "<workspace>/scripts/reflex_router.py" prompt`（其他四個換最後的參數）。你那台如果有 PowerShell 專用工具名稱（例如 `PowerShell`），把它加進前兩個 matcher。

**不要改 `scripts/feed_junshi_handoff.ps1`**：開工置頂「🎯 教練上一場交辦」由聯想改（同一支共用檔，兩台同時改會打架），聯想推上去後你 `git pull` 就有。

## 怎麼驗證（做完才算）
1. 開新對話框說「幫我開發票，統編要寫」，對話裡應該出現「⚡ 條件反射……發票：先跑 claude-brain/data/query_training_invoice.py 查」；`state/reflex_hits.log` 多一行 `prompt	R-INVOICE`
2. 請新對話框回一句網址後面直接黏著中文括號的話（例如 `https://event.bymyway.com/x（已確認）`），應該被擋下重寫
3. 聯想推上開工置頂之後：`git pull`，開新對話框說「開工」，注入最上面出現 🎯 且是接力棒裡時間最新的那段
4. 回信附上實際畫面文字（各貼 2～3 行原文）＋你用的 Python 指令＋commit hash
