---
name: reference-openclaw-nested-git-repos
description: /Users/bymyway/.openclaw 跟 /Users/bymyway/.openclaw/workspace 是兩個獨立git倉庫，別搞混分支
metadata: 
  node_type: memory
  type: reference
  originSessionId: 235960d2-ceaf-4f60-9d5d-6261adca7f0b
---

`/Users/bymyway/.openclaw`（外層）和 `/Users/bymyway/.openclaw/workspace`（內層）是**兩個完全獨立、各自 `git init` 的倉庫**，只是剛好都設定了同一個 GitHub remote 名字 `mac-openclaw-workflows`，歷史完全不相干（git 回報「拒絕合併無關的歷史」）。

- **外層**（repo root = `/Users/bymyway/.openclaw`）：分支 `master`，裝 `cron/jobs.json`、`openclaw.json` 等 OpenClaw 系統設定，只跟這台 Mac 自己的排程/設定有關，不是三機共用內容。
- **內層 `workspace/`**：分支 `main`（4500+ commit，remote 掛 `lessons` 備援），這才是真正的「三機共用大腦」，`claude-brain/`（149行 MEMORY.md 索引 + 158 個記憶檔）、`試金石/`、`distill/`、`knowledges/` 全部在這裡，`feed_junshi_handoff.sh`（開工pull）跟 `session_end_auto_push.sh`（收工push）都是對這個內層 repo 操作。`~/.claude/projects/-Users-bymyway--openclaw/memory` 其實是這個 repo 的 symlink 路徑（`git rev-parse --show-toplevel` 會指回 `~/.openclaw/workspace`），兩個路徑改的是同一份東西。
  - **🔴 2026-07-08 更新**：原本還多掛了一個過期的 `claude-workflows` remote（5月的舊倉庫HEAD，跟現在內容早就對不上），Windows機（聯想）那邊有人推送時繞去這個舊remote才發現問題、改推`origin`才成功。Mac這邊已用 `git remote remove claude-workflows` 清掉，只剩 `origin`(`mac-openclaw-workflows`) + `lessons`。**其他機器（Windows/ACER）若也還掛著這個舊remote，要各自在自己那台跑同樣的移除指令**，軍師沒有遠端權限直接幫其他機器改。

## Why
2026-07-05 查「小龍蝦設定跑掉」時，在外層資料夾跑 `git log`/`git push origin main` 一直失敗，一度誤判三機共用大腦壞了、main跟master分岔要合併——後來才發現是查錯資料夾，內層 workspace 的 main 分支其實運作正常（6分鐘前才剛同步過）。白忙一場的根因就是沒意識到這是兩個repo。

## How to apply
- 查 cron/openclaw.json 相關問題 → cd 到 `/Users/bymyway/.openclaw`（外層，master）
- 查記憶/試金石/知識庫/共用大腦相關問題 → cd 到 `/Users/bymyway/.openclaw/workspace`（內層，main）
- 兩邊 `git status`/`git log` 結果會完全不同，看到「unrelated histories」或分支對不起來，先確認自己在哪一層，不要假設是同一個repo分岔
- 相關：[[project_auto_distill_mission]]
