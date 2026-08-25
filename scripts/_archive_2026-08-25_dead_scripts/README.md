# 封存腳本（2026-08-25 賈維斯全系統體檢）

這裡的腳本經過完整引用掃描，確認**全機沒有任何地方會呼叫它們**：
掃描範圍涵蓋 Claude Code settings、系統 crontab、LaunchAgent、
openclaw cron（含 cron.db）、git hooks、所有 hooks 目錄、
其他所有腳本的內容、workspace 根目錄的所有 .md 文件。

**是搬移不是刪除**——教練鐵律「珍貴資料只搬不刪」。
任何一支要用回來，直接搬回上一層即可，git 歷史也完整保留。

## 兩類

1. **一次性挖掘／分析工具**：當初做試金石案例挖掘、痛點排名 top30 計算時寫的工具，
   跑完產出結果就沒再用過（同一個功能有 4~7 個版本並存就是證據，
   例如 score_top30 / score_top30_v2 / score_top30_v3）。
2. **測試腳本**：驗證某支 hook 當時有沒有生效用的，該 hook 早已上線穩定運作。

## 沒有被搬進來的

任何還被 cron／hook／LaunchAgent／其他腳本引用的都留在原位，一支都沒動。
特別註記：`precommit_check_ps1_bom.sh` 第一版掃描曾誤判為死腳本，
原因是掃描來源漏了 `.git/hooks/`，補上後確認它正在被 pre-commit 使用，未歸檔。
