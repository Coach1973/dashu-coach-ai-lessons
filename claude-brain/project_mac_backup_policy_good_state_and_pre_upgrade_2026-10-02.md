---
name: project-mac-backup-policy-good-state-and-pre-upgrade-2026-10-02
description: Mac mini 時光機改成教練定的四條（點名正常才備份／升級前必備份／Amber 備份上限150GB／快取不備份），取代每小時自動備份；各條由哪支程式撐著
metadata:
  node_type: memory
  type: project
  originSessionId: 9df2876c-7681-432c-88e0-2fa87d0e2702
  modified: 2026-10-02T03:18:58.633Z
---

教練 2026-10-02 10:42 原話：3 天備份了 22 次有點多，要像聯想一鍵備份——電腦運行良好時備份、系統升級前備份，其他時間沒必要時時備份。11:12「請四條都做」，並自己把時光機備份頻率改成「手動」（設定檔 AutoBackup=0）。

背景：備份目的地是家裡 Amber X（466GB，`smb://amber-Coach/TimeMachine`，destination ID `0705F9A4-4103-4A5E-92FE-0102BDF7BEBF`）。10/02 09:14 Amber 警告剩 8%，暫停上傳／備份；10:05 自動恢復；AI 分類要超過 15% 才恢復。備份約 150GB，只佔 Amber 三分之一，其餘是影片照片等。

**四條與撐住的機制：**
1. 點名正常才備份：`scripts/daily_team_rollcall.py` 的 `backup_when_healthy()`（08:10 點名沒有 🔴 → `tmutil startbackup`；有紅燈不備份；連續 3 天沒備到 → 點名出 🟡）。備份日期讀 `/Library/Preferences/com.apple.TimeMachine.plist` 的 SnapshotDates（UTC），不需完整磁碟取用。
2. 升級前必備份：反射 `R-BACKUP-BEFORE-UPGRADE`（pre_tool block，`reflex_router.py` 的 `check: backup_recent`）：npm 全域裝 openclaw／openclaw update／brew upgrade／softwareupdate 前 6 小時內沒備份就擋，改成 `tmutil startbackup --block && <升級指令>`；ssh 遠端、--dry-run、update status 不擋。
3. 上限 150GB：`tmutil setquota <ID> 150`（要 root，教練輸入密碼那次一起做），滿了時光機自己刪最舊的。
4. 不備份：`~/.cache`、`~/.npm`、`~/.rustup`（tmutil addexclusion，約 13GB）；`~/Library/Caches` 系統本來就排除；`~/.nvm` 刻意保留（小龍蝦程式裝在裡面）。

**How to apply:** 有人問「為什麼沒每小時備份」「怎麼備份」照這四條答；要升級前先備份；別把頻率改回每小時。

相關：[[reference_amber_nas]]、[[feedback_event_driven_not_polling_pattern]]（每小時備份＝輪詢，教練要的是事件觸發）
