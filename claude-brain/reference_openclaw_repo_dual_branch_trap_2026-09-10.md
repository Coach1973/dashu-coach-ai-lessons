---
name: reference-openclaw-repo-dual-branch-trap-2026-09-10
description: ~/.openclaw外層repo(mac-openclaw-workflows)遠端同時有main/master兩分支，本地在master卻對照main導致誤判為落後100個commit，正確操作是永遠對照origin/master
metadata: 
  node_type: memory
  type: reference
  originSessionId: 939403d3-b038-4842-82cf-6e7e35bacb99
  modified: 2026-09-10T14:28:15.761Z
---

`~/.openclaw`（外層repo，remote同為`Coach1973/mac-openclaw-workflows.git`，跟`~/.openclaw/workspace`是分開的獨立repo）的遠端同時存在`origin/main`和`origin/master`兩個分支，內容差異巨大（`main`可能是某個worktree/agent自動建立的分支，內容包含`.memsearch/`等完全不同的歷史）。本地分支其實是`master`。

**事故經過**：2026-09-10修`hooks/invoice-inbound/handler.js`後`git push origin main`被拒（non-fast-forward），誤以為落後遠端要pull整合，`git pull --rebase origin main`跑到100個commit時在`USER.md`撞上add/add衝突。查`git branch -r`才發現`origin/main`跟`origin/master`是完全不同的兩條歷史，本地`master`其實跟`origin/master`完全同步（`git log --oneline origin/master..master`只多我這一個新commit，零衝突）。用`git reset --soft origin/main`嘗試修正時一度把HEAD指向一個內容差異驚人的commit（大量`.memsearch/memory/*.md`檔案增減），及時用`git reflog`+`git reset --hard`救回原本的commit，改push到正確的`origin master`才順利成功。

**Why**：對這個外層repo做任何git操作前，先跑`git branch --show-current`確認本地分支名稱，再用該分支名稱對照`origin/<同名分支>`，不要憑印象假設是`main`——這個假設在多數repo成立，但這個特定repo是例外。

**How to apply**：
1. 任何要在`~/.openclaw`（非`workspace`）做commit/push/pull的任務，第一步先`git branch --show-current`+`git branch -r`確認分支對應關係
2. 如果push被拒、以為要pull整合，先用`git log --oneline origin/<本地分支名>..<本地分支名>`確認真正的落後/超前關係，不要對著錯的遠端分支做rebase
3. `git reset --soft`看到diff異常龐大（幾百個檔案、無關的目錄如`.memsearch/`）時，立刻停手用`git reflog`+`git reset --hard`回到操作前狀態，不要繼續往下推

Related: [[feedback_verify_tool_permission_before_claiming_2026-09-06]]（同一類「查證前先確認基本事實，不要憑經驗套用」教訓）
