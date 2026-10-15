---
name: reference-review-cloud-branch-never-checkout-in-live-repo-2026-10-15
description: event.bymyway.com/curated/<slug>/ 直接讀 ~/github_repos/<slug> 的工作目錄；驗收雲端分支不可在那裡 checkout（會立刻上線），要另開 git worktree＋唯讀代理伺服器看
metadata:
  node_type: memory
  type: reference
  originSessionId: 0ceac93f-49ab-403d-ab7d-987a5b68da20
  modified: 2026-10-15T12:40:21.004Z
---

event-signup 的 `/curated/<slug>/` 路由直接讀 `~/github_repos/<slug>` 的**工作目錄**（app.py `CURATED_REPOS_DIR`＋`_serve_repo_file`），不是讀 GitHub。所以接力棒寫的「`cd ~/github_repos/rongtree && git checkout claude/rongtree-redesign`」會讓未驗收的雲端分支**立刻變成正式站**。

**How to apply（驗收雲端分支）：**
1. `git worktree add --detach <scratchpad>/xxx-review origin/claude/<分支>`，不動正式資料夾。
2. 在 scratchpad 放一支唯讀代理小伺服器：`/curated/<slug>/` 讀 worktree，其餘 GET 轉到 https://event.bymyway.com（API、/static/nav-burger.js），POST 一律 403（不寫任何資料）。用瀏覽器窗格＋DOM 數值檢查（內建瀏覽器截圖被截圖鎖擋，且教練要省流量）。
3. 驗完才在正式資料夾 `git merge --no-ff --no-commit origin/claude/<分支>`；**雲端交接信（docs/to_junshi）不要進網站目錄**（`_serve_repo_file` 只擋 .db/.py/.sh 等，.md 會公開）：`git reset -q HEAD -- docs` 後把信 `mv` 到 `workspace/knowledges/雲端來信存檔/`（`git rm` 會被 delete_guard 擋）。
4. commit＋push 後 curl 正式站：頁面 200、縮圖 `image/jpeg`、信件網址 404。

10/15 榮樹下改版就是這樣合併（commit `0cf9d29`）。瀏覽器窗格在背景時 `innerWidth` 會是 0、平滑捲動不會動：量錨點落點要先 `scroll-behavior:auto` 再設 `location.hash`。

相關：[[reference-curation-sop-2026-09-06]]、[[reference-cloud-work-map-and-where-lessons-live-2026-10-06]]

**同一個架構的另一面（10/15 張麗蝶 lidie）：** 教練說「GitHub（coach1973.github.io/<slug>）改了、event.bymyway.com/curated/<slug>/ 沒更新」＝正式站讀的是 Mac 本機 clone，GitHub 推上去要靠 webhook（`/hooks/github-site` → `curated_git.py sync`）才會拉回來。先查 `gh api repos/Coach1973/<slug>/hooks` 有沒有掛；沒有 → `python3 scripts/curated_git.py hook <slug>`，再到 `~/github_repos/<slug>` `git pull --ff-only` 補上這次。根因是店家上架路（`curation_process.py` 自己建 repo＋Pages）漏了 `ensure_curated_github`，10/15 已補（`curation_process.py` 同輪掛通知）；夜裡 `ensure-all` 只是兜底。

**更輕的做法（10/16 軍火庫設計稿實證）**：雲端交的是「單一 HTML 檔」（如 `arsenal-design/index.html`）時，不用 worktree 也不用代理伺服器：`git -C ~/github_repos/<slug> fetch` → `git show origin/<分支>:<路徑> > <scratchpad>/index.html` → `python3 -m http.server <埠> --bind 127.0.0.1`（目錄指向 scratchpad）→ 瀏覽器驗 → 殺伺服器。正式倉庫工作目錄全程不動（`git status` 仍在 main 乾淨）。驗「不同意公開者不外洩」要用「去掉 `<script>` 的 DOM」檢查，整頁 outerHTML 會把 script 裡的示範資料算進去而誤判外洩。內建瀏覽器截圖被截圖鎖擋，改用 DOM 數據（橫向捲動、字級、點擊區 44px、請求數）。
