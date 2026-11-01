---
name: reference_ai_impact_stats_db_wiped_by_auto_stash_marks_sync_2026-11-01
description: 互動頁(ai-impact)統計歸零＝收工自動備份 git stash -u 把 workspace 內未進 git 的 nmda_ai.db 換成空檔；已搬到 ~/.openclaw/data 並改 /marks/sync 整份冪等同步
metadata:
  type: reference
---

互動頁 https://event.bymyway.com/curated/ai-impact/ 統計「沒顯示」有三層原因（11/01 查到）：
1. 10/31 現場（13:00 起）頁面是單機模式，70～80 人的票只在各自手機，伺服器從沒收到，救不回（第一次連線 16:53）。
2. `session_end_auto_push.sh` 收工會 `git stash -u`，把 workspace 內未進 git 的 `nmda_ai.db` 收走、程式又建空檔 → 「no such table: polls」、state 回 500、票全歸零。同類 [[reference_workspace_stash_u_clobbers_background_outputs_2026-10-26]]。
3. 頁面用加減票＋瀏覽器記得「已勾」，伺服器歸零後再點變 −1，畫面與統計對不上。

**Why:** 教練要廣發、公開看統計、同 IP 重複也照算、不需要送出鈕。
**How to apply:** 活資料庫一律放 workspace 外（現在 `~/.openclaw/data/nmda_ai.db`）；每次連線自動補表；投票改 `POST /api/nmda-ai/marks/sync`（訪客整份勾選，伺服器重算）；同 IP 上限 600/分。commit 35e0a0a66、9027f4197（後端）、df02da8（頁面）。修完要用「全新訪客的真瀏覽器」點一次再看伺服器數字（腳本在 scratchpad，puppeteer-core＋Chrome）。
