---
name: reference-worktree-session-edit-hook-blocks-openclaw-2026-10-15
description: 「開工」開的臨時 worktree 對話，Edit/Write 改 ~/.openclaw/** 的正式檔案會被 hook 擋；request_directory／change_directory 都解不了，要教練明說才能改走終端機補丁
metadata:
  node_type: memory
  type: reference
  originSessionId: 0ceac93f-49ab-403d-ab7d-987a5b68da20
  modified: 2026-10-15T18:24:59.423Z
---

10/15 開工的對話在 `~/.openclaw/.claude/worktrees/kaigong-xxx`（外層 repo 的陳舊 worktree，落後 8136 個 commit，裡面沒有 extensions／workspace 子資料夾）。PreToolUse hook 對 Edit 回「base repo checkout，請改 worktree 路徑」，但正式系統（scripts、extensions、openclaw.json、agents）都在 `~/.openclaw` 底下，改 worktree 副本沒有任何效果。

**試過沒用：** `request_directory` 授權 workspace（只多了讀寫許可，Edit 仍被擋）；`change_directory`（回「worktree 不能搬」）；環境訊息一度顯示「已不是 worktree」但 hook 仍擋。

**How to apply：** 遇到這個擋，不要自己繞去用 Bash 改；一次講清楚「臨時工作區擋了正式檔案，要改請你授權我用終端機指令」，教練同意（10/15 他回「可以，用終端機指令改正式檔案」）後才用 Bash＋python 補丁，改前備份到 `workspace/state/backup_<日期>_<主題>/`，改完跑測試、path-limited commit（`git commit -m … -- <路徑>`，避免帶進別的 job 的未提交變更）。`git add` 對被 .gitignore 的外掛資料夾要用 `git add -u -- <已追蹤檔>`。外層 repo 分支是 master（對照 origin/master）。

**10/16 補（總結收工時再碰到一次）**：教練說「總結」後，寫正式接力棒一樣被擋，我先講清楚並問一次，他回「可以，用終端機指令更新接力棒並推送（改前備份，只提交接力棒與封存檔）」才動手——同類授權每場要再問一次。做法：新棒內容與套用腳本先寫在 scratchpad、對副本演練，備份到 `workspace/state/backup_<日期>_handoff/`，再套用。**提交位置坑**：接力棒在 **`~/.openclaw/workspace` 自己的 git 倉庫**（分支 main，遠端 lessons／origin），外層 `~/.openclaw`（master）把 `workspace` 整個 .gitignore，在外層 `git add workspace/...` 會失敗；要 `cd ~/.openclaw/workspace` 再 path-limited commit（`af154b104`），推 `origin main`。倉庫裡常有別的程序的未提交檔（`.sync_markers/…`、`curated_sites_registry.json`），別帶進去。

相關：[[reference-openclaw-repo-dual-branch-trap-2026-09-10]]
