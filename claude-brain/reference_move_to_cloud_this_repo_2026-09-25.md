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
