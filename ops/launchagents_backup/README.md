# com.coach.* launchd 設定備份（2026-10-16）
10/16 台灣時間 08:44 這些設定檔從 ~/Library/LaunchAgents 全部消失，整批網站 530。還原：
`cp ops/launchagents_backup/com.coach.*.plist ~/Library/LaunchAgents/ && for f in ~/Library/LaunchAgents/com.coach.*.plist; do launchctl bootstrap gui/$(id -u) $f; done`
密碼／金鑰都在各專案 .env（plist 只 source 它），本目錄不含機密。
