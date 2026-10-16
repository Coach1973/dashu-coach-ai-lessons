---
name: feedback_hooks_must_fail_open_never_block_coach_2026-10-16
description: 🔴🔴 重大疏失：AI 寫的檢查程式自己不見時 python 回 2，把教練每句話都擋掉 3.5 小時（10/16 15:00～18:26）；所有會擋人的檢查程式壞了一律放行；workspace 被拉錯分支(origin master)換掉的認法與救法
metadata:
  node_type: memory
  type: feedback
  originSessionId: cf0feb25-cf92-471e-881b-4e0724e55f1e
  modified: 2026-10-16T10:36:12.329Z
---

**事實**：10/16 15:00:32（台灣時間）workspace 執行了 `git pull --rebase --autostash origin master`。master 是 ~/.openclaw 另一條歷史（兩個倉庫推到同一個 GitHub 的不同分支：workspace＝main，~/.openclaw＝master），workspace 被換成另一套檔、卡在 rebase 中途。settings.json 的 python 檢查程式檔案不見 → python 回 2 → Claude Code 把教練的話擋下（手機、每個對話框都一樣）。教練在外面 3.5 小時下不了任何指令，列為重大疏失（試金石123）。

**Why:** 教練原話：「寫一個指令，寫到我連主人親自下命令都不行，那要你何用？」「就你寫的，不然還會有誰？」→ 不要辯解、不要再查，直接承認是我們寫的並修好。

**How to apply:**
- 新增或修改任何 hook：寫法一律 `f=<路徑>; [ -f "$f" ] || exit 0; exec ...`（檔案不在就放行）。只有 PreToolUse 的危險指令守門（delete_guard 等）可以刻意回 2。
- 認法：`git -C ~/.openclaw/workspace status` 出現「重定基底動作正在進行中」、分支空白、HEAD 是 ~/.openclaw 的提交 → 就是這種情況。
- 救法：先備份 15:00 之後寫入的檔 → `git rebase --quit`（暫存會存進 stash list）→ `git checkout -f main` → `git stash apply <那筆 sha>`。`rebase --abort` 會因為「未追蹤檔擋路」失敗（state 不變，不會壞）。數缺檔要用 `git -c core.quotepath=off ls-files -z`，不然中文檔名會誤算成不見。
- 現在 workspace 有 `.git/hooks/pre-rebase`（副本 ops/git_hooks/pre-rebase）擋沒有共同歷史的 rebase；換電腦或重 clone 要記得裝回去。
- 誰下的 pull 還不知道；pre-rebase 擋著，誰再下都不會壞。相關：[[reference_launchagents_plists_deleted_outage_2026-10-16]]
