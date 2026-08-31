---
name: acer-health-check-2026-08-31
description: ACER（hostname pc5c925ed70e46）2026-08-31 全機體檢報告：找到並修復兩個真bug（PS5.1 -AsHashtable、workspace路徑重複clone），回覆聯想跨機四層根因信
metadata:
  type: project
  originSessionId: continuation-of-2026-08-26-session
---

## 這台機器的雙重身份

- **hostname**：`PC5C925ED70E46`
- **cross-agent 信箱名**：`acer`（`$env:AGENT_INBOX_NAME = "acer"`，User 層級環境變數）
- **sync_health 追蹤名**：`pc5c925ed70e46`（`state/sync_health/pc5c925ed70e46.json`）
- **真實 repo 路徑**：`C:\Users\Administrator\Documents\mac-openclaw-workflows`（不是 machines.json 舊登記的 `D:\Claude-Data\workspace`，那份是 2026-07 前的舊狀態，已過期未再使用）
- 這台就是接力棒表格裡「ACER 49天未開機」那台，2026-08-26 01:00~01:38 教練親自開機重裝七支hook後，這是它第一次再被叫醒（本場對話）

## 體檢結果

### ✅ 正常
- git 同步：`origin/main` 對齊，`git pull` 正常，無衝突
- 六支 hook 全部註冊在 `~/.claude/settings.json`（PreToolUse delete_guard / Stop session_end_auto_push / UserPromptSubmit 六支：inject_taiwan_time / session_time_context / feed_junshi_handoff / scan_cross_agent_inbox / scan_cross_machine_commits / summary_upload_trigger），且全是 PowerShell 原生版本，不依賴 jq（這台機器確認沒裝 jq，`python3` 也只是 Windows Store 樁，不算真安裝——跟案例64聯想同款環境限制，但這台的 hook 從一開始就沒踩到，因為用的是 .ps1 不是 .sh）
- 磁碟空間：C槽 200.4GB（剩135.2GB）、D槽 271.1GB（剩129.9GB），健康
- PowerShell 版本：5.1.26100（Windows 內建版，非 pwsh 7）

### 🔴 發現並已修復兩個真bug

**1. `setup_windows_hooks.ps1` 的 PS5.1 `-AsHashtable` 不相容（接力棒早已記錄、本場才真的補上）**
- 根因：`ConvertFrom-Json -AsHashtable` 是 PS6+ 才有的參數，PS5.1（這台機器）呼叫會拋例外，觸發 catch 分支把原有 `settings.json` 的 `env`/`permissions`/`model` 全部清空重寫——2026-08-26 那場就是靠備份救回的
- 修法：新增 `ConvertTo-HashtableCompat` 相容函式，PS6+ 走原生 `-AsHashtable`，PS5.1 改用手動遞迴轉換，已用這台機器真實的 `settings.json` 實測驗證：型別正確轉成 Hashtable、`ContainsKey`/索引存取正常、`env`/`permissions`/`model`/`hooks` 四個 key 全部保留、可正常轉回 JSON
- 影響檔案：`scripts/setup_windows_hooks.ps1`（尚未 commit，等教練確認後可推）

**2. `feed_junshi_handoff.ps1` 的 `$workspace` 路徑指向不存在的資料夾，每次觸發都重新完整 clone 1.1GB（新發現，直接回應聯想8/26的跨機信）**
- 根因：`$workspace = Join-Path $env:JUNSHI_HOOK_ROOT "workspace"`，這台機器 `JUNSHI_HOOK_ROOT = C:\Users\Administrator\Documents`，組出來是 `...\Documents\workspace`——但這台實際的 repo 資料夾叫 `mac-openclaw-workflows`，根本沒有叫 `workspace` 的資料夾。腳本發現路徑不存在時的邏輯是「當作第一次用，直接 git clone」，所以**每次是全新 session 觸發「開工」，都會重新完整 clone 一份 1.1GB 的雲端 repo**，讀到的六步驟內容也是這份獨立副本，不是教練跟其他機器一直在同步的那份 `mac-openclaw-workflows`
- 這正是聯想 2026-08-26 01:40 那封信第2層根因（過期副本 clone）在這台機器上的變形：不是「clone 了但過期沒更新」，是「每次都重新 clone 一份新的、但完全獨立於真正在用的 repo」
- 修法：比照聯想的處理方式——把剛才觸發出來的那份新 clone 改名封存成 `Documents\workspace.stale_backup_20260831`（未刪，確認過 `git status`/`git log origin/main..HEAD` 都乾淨零本地未推送內容才動手），原路徑改建 **junction** 指向 `mac-openclaw-workflows`。已重新跑一次 pipe test 驗證：`git -C workspace log -1` 現在讀到的就是真正最新的 commit，六步驟注入內容（68KB 左右）跟直接讀 `mac-openclaw-workflows` 一致，不再重複 clone
- 影響：以後這台機器每次「開工」，六步驟接力棒/HEARTBEAT/試金石注入會讀到跟教練互動的同一份真實資料，不會再是凍結在觸發當下的獨立副本

### ⚠️ 待處理（不影響運作，但值得記錄）
- `Documents\workspace.stale_backup_20260831`（1.1GB）目前保留未刪，之後確認沒有殘留價值可以請教練同意後清除
- `scripts/setup_windows_hooks.ps1` 的 PS5.1 bugfix尚未 commit/push（本場先驗證正確性，等教練或下一棒確認後推）
- `qc`、`scripts/organize_downloads.ps1` 兩個既有未進版控檔案，非本場產生，不確定來源，未動

## 沉默原因查證（誠實回報，非猜測）

查 `git log --since=2026-08-25`：這台機器（`[ACER]`/`[Win]` 標籤）最後一次真正有活動是 **2026-08-26 01:38:01**（跨機同步四層根因回信）。從那之後到本場對話重新啟動（教練在同一個 Claude Code session 裡回來下指令）為止，這台機器沒有任何新 commit。

這不是系統故障，是 Claude Code session 本身被晾著沒有新的教練指令輸入——session 從 2026-08-26 01:19:58 開到現在（2026-08-31 18:5x），中間 137+ 小時沒有教練互動，不是「機器連不上」或「hook 壞掉」。符合守則v3.1鐵律：中繼蒸餾/hook沒抓到不等於沒發生，這次是真的沒發生（沒有教練輸入），不是抓不到。

## 🔧 對應機關

- `scripts/setup_windows_hooks.ps1`（PS5.1相容修復）
- `Documents\workspace` 已改建 junction → `mac-openclaw-workflows`（本機生效，不進git，跟其他機器的junction設定各自獨立）
- 回信：`cross-agent/outbox/2026-08/20260826-0140_lenovo-to-mac-acer_cross-sync-4layer-rootcause.md`（已讀已回，見同日新回信）

Related: [[試金石案例64]]（同源環境相容性問題）、[[project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26]]（聯想端原始四層根因分析）
