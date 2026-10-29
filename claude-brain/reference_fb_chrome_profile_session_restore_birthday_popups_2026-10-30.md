---
name: fb-chrome-profile-session-restore-birthday-popups
description: FB 生日頁一直跳出來＝小龍蝦重開臉書專用 Chrome（9222）時還原舊分頁；兩個 profile 的 Sessions 已移走備份，重開驗證只剩 1 個空白分頁
metadata:
  node_type: memory
  type: reference
  originSessionId: 00a6da40-62cc-48e4-bda2-0945eb871b2e
  modified: 2026-10-29T17:27:44.114Z
---

2026-10-30 01:23（台灣時間）教練抱怨 `facebook.com/index.php?next=…friends/birthdays…` 一直跳出來、關了 20～30 個還有。

查到的：
- 該 Chrome 歷史在 01:23:21～25 五秒內載入這頁 45 次（轉換類型=reload，是還原分頁的特徵）；平常每天只有 1～2 次（每日生日腳本 `scripts/fb_birthday_scraper.js`）。
- 同一時段小龍蝦 main 分身在做 hsiuli 策展頁補貼 FB 的工作，01:22～01:25 連開 4 個可見 Chrome（profile：fb_session_data、fb_session_data_local、/tmp 複製的主 profile、imported），用 `pkill` 殺掉再重開。
- `fb_session_data_local` 與 `workspace/scripts/fb_session_data` 的 Sessions／Tabs 檔各約 7～12MB，各含 1100 多筆 birthdays 導覽紀錄；這頁是 FB 登入過期後的重導向頁（`index.php?next=`），代表那兩個 profile 的 FB 登入已過期。

已做：兩個 profile 的 `Default/Sessions` 移到 scratchpad 備份（`fb_sessions_backup_20261030/`，非刪除），`exit_type` 設 Normal，Cookies 沒動；用 9333 埠無頭重開驗證只有 1 個空白分頁。

沒解決／注意：
- 小龍蝦只要再測臉書登入，仍會開可見 Chrome 視窗（這是它的工作方式，沒改）。
- 生日腳本用的 FB 登入已過期，需教練哪天在專用 Chrome 登入一次（只有教練能登入）。

相關：[[reference_openclaw_silent_long_run_ack_reaction_2026-10-30]]
