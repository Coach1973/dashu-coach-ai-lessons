---
name: reference-move-to-cloud-this-repo-2026-09-25
description: 雲端工作頁(claude.ai/code)怎麼吃到教練全套規則(cloud_sync+專案.claude/settings.json，main/master兩條都通，已實測)；外層~/.openclaw master分岔09-25已查證安全合併；AI可用claude --cloud開測試頁、claude -p --cloud傳話給既有雲端頁
metadata:
  node_type: memory
  type: reference
  originSessionId: 7dfd3491-32da-49ec-be24-a2c0d54e850c
  modified: 2026-09-25T02:39:31.968Z
---

# 雲端工作頁與這個 repo

## 1. 雲端怎麼吃到教練的規則（2026-09-25 建立，兩條路都實測通過）
官方規則：雲端只讀 GitHub 專案裡的東西（專案 CLAUDE.md、專案 `.claude/settings.json` 的 hooks、`.claude/skills`），**讀不到 Mac 的 `~/.claude/`**（全域 CLAUDE.md、30 支 hook 的註冊、11 個自訂技能全在那裡）。所以 09-25 以前雲端說「模型分工規則我不知道」。

現在的機制：
- `workspace/cloud_sync/`：`~/.claude/CLAUDE.md` 與自訂技能的副本。`session_end_auto_push.sh`（每則回覆結束）先跑 `scripts/cloud/mirror_to_cloud_sync.sh` 再 commit+push，Mac 改規則雲端自動跟上。
- `workspace/.claude/settings.json`（main 分支）：雲端開場注入全套規則＋模型分工規則，並照跑時間/守則提醒/執行合約/守則原文/模型分工/刪檔鎖/結束檢查 7 支。全部經 `scripts/cloud/run_in_cloud.sh`，只在 `CLAUDE_CODE_REMOTE=true` 時執行，Mac 本機直接略過（避免跟 `~/.claude/settings.json` 重跑）。
- 外層 `~/.openclaw/.claude/settings.json` + `cloud_bootstrap.sh`（master 分支，桌面版「Continue in cloud」會落在這條）：開場先把 main 的規則/接力棒/試金石/memory 稀疏下載到雲端 `~/.openclaw/workspace`（約 48MB），再交給同一支開場程式。
- 雲端一律把 workspace 放在 `~/.openclaw/workspace`，規則裡所有 `~/.openclaw/workspace/...` 路徑在雲端直接有效。
- 要新增雲端也要跑的 hook：兩個 settings.json 都要加，且腳本不能用 Mac 專屬指令（stat -f、osascript、/opt/homebrew…）。

## 2. AI 自己就能操作雲端（不用叫教練轉話）
- `claude --cloud "任務"`：開新雲端頁（以目前資料夾的 GitHub 分支為準，要先 push）。需要真終端機，Bash 工具裡用 `script -q <log> claude --cloud "..." < /dev/null`，session id 從 log grep。
- `claude -p "訊息" --cloud <session_id>`：傳話給**已存在**的雲端頁（09-25 軍師一度誤說「沒有管道傳話」，是錯的）。
- 驗收技巧：叫雲端頁把結果寫成檔案 commit+push，本機 `git ls-remote origin 'refs/heads/claude/*'` 抓分支讀檔；測完刪測試分支。
- 雲端頁本機 `list_sessions`/`get_session` 查不到，教練要看只能開 claude.ai/code。

## 3. 外層 `~/.openclaw` repo 的分岔真相（09-25 查證）
09-25 前本機 master「領先26/落後25」，一直被當成「9/19 金鑰清除留下的分岔、push 會把舊金鑰推回去」。用 `git merge-base --is-ancestor` 查證：**舊金鑰 commit（如 f193a4eba）不在 master 上**，只在本機的 `main` 與 `claude/hungry-jackson-a81b31` 兩條舊分支；master 的分岔只是各機器平行 commit。已正常合併推送（f517ec524），master 與遠端同步。**危險的是外層 repo 本機那兩條舊分支——永遠不要 push 它們。**
move_to_cloud 若遇 uncommitted changes：逐一檢查再 commit，不要 `git add -A`（09-25 曾抓到 533MB 漫畫素材差點被 commit）。

## 相關
[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]、[[feedback_git_add_a_risk_with_db_backup_files_2026-09-01]]、[[feedback_model_tier_advisor_opus_vs_sonnet_2026-09-25]]

## 4. 2026-10-05 20:55 補：claude --cloud 在「沒信任過的資料夾」會卡住
在 `~/github_repos/bni-chapters` 執行 `script -q log claude --cloud "..."`，啟動器停在「Is this a project you trust? Yes, I trust this folder」等 Enter，不是掛掉；按信任＝改使用者的信任設定，要教練同意才按（或教練在 claude.ai/code 選 repo 自己開）。已用 `pkill -9 -f "claude --cloud"` 收掉，沒開出雲端頁、沒花雲端額度。bni-chapters repo＝`Coach1973/bni-chapters`（預設分支 master，61 個檔、2.6MB，資料庫／.env／uploads 都在 .gitignore），雲端拿得到程式、拿不到正式資料庫與 .env，要測試得用假資料庫。教練週額度 10/05 20:54 已 76%（週三 13:00 台灣時間重置）；本場對話框已 38 萬 token，每輪都要重讀，開新對話框是最直接的省法。

## 5. 2026-10-06 補：開雲端對話要用「終端機分頁」，不要用 Bash 背景 script
- 10/05 23:19 用 `mcp__terminal__run_in_terminal`（真終端機分頁）跑 `cd ~/github_repos/bni-chapters && claude --cloud "..."`：雲端頁頂端掛著 bni-chapters 倉庫與分支，推得上去。
- 10/06 02:12 改用 Bash 工具 `( script -q log claude --cloud "..." < /dev/null & )`：session 建立了（`Created cloud session`），但**沒掛倉庫**（頁面只有 Environment: Default；雲端說沒有 origin、`GitHub access to this repository is not enabled for this session`），做完 4 個 commit 推不出去。觀察到的差異只有開法；確切原因沒查證，但以後一律走終端機分頁。
- 開完要驗：雲端頁（claude.ai/code/session_...）頂端要看得到倉庫名與分支；沒有就是開壞了，別讓它開工。
- 補救：教練在網頁版自己把倉庫接上既有對話即可（10/06 02:43 教練做了），雲端不用重做。誤請雲端「貼出 diff」會白耗教練額度，發現開壞時第一動作是停手回報。

## 6. 2026-10-15 補：開雲端對話改用「Chrome 開 claude.ai/code 新增工作階段」，不要用終端機 `claude --cloud`
- 教練用手機／遠端時看不到 Mac 終端機分頁，`claude --cloud` 停在「信任這個資料夾」他根本不知道（10/15 他說「它並沒有跳出來」），而且按信任是改安全設定、只能他按，白等 10 分鐘。
- 做法：教練先在 claude.ai/code 把倉庫加進雲端（他 10/15 手動加了 rongtree，倉庫清單有搜尋框，打 repo 名篩選）。之後我用 claude-in-chrome：開 claude.ai/code → 倉庫下拉選 Coach1973/<repo>（選項要用 find 找 ref 再點；JS 取清單是虛擬捲動只列前 87 個，要在搜尋框輸入）→ 模型下拉選 Opus 5.5（預設是 Sonnet 5.5 超高）→ 提示詞是 ProseMirror，用 `focus(); execCommand('insertText', false, 文字)` 填入 → 按「傳送」。實測成功：榮樹下改版雲端對話 `session_01UN5wbKUBNK5RsdQUJKiQXo`（https://claude.ai/code/session_01UN5wbKUBNK5RsdQUJKiQXo）。
- 任務書放 `workspace/state/cloud_briefs/`，雲端只准推自己的分支（榮樹下 main 推上去會自動換新正式站）；收回方式：`git -C ~/github_repos/<repo> fetch && git branch -r | grep claude`，雲端信放分支 `docs/to_junshi/`。
- 螢幕截圖被截圖鎖擋，操作網頁用 find／read_page／javascript_tool 讀結構即可。
