---
name: reference_launchagents_plists_deleted_outage_2026-10-16
description: 10/16 十幾個 *.bymyway.com 網站斷線根因：com.coach.* 自動啟動設定檔在 10/3～10/4 被刪、服務靠記憶體撐了 12 天，08:44 Mac 登出後全斷；原檔在 Time Machine 10/03 01:10 備份；手機修復漏了 .env 和真鑽，已用原檔還原
metadata:
  node_type: memory
  type: reference
  originSessionId: 5f6b7aeb-e52c-466c-8c58-907bd13abbd1
  modified: 2026-10-16T05:15:56.719Z
---

**時間線（台灣時間）**
- 10/03 01:10 Time Machine 備份：`~/Library/LaunchAgents` 裡 25 個 `com.coach.*.plist` 都在。01:37 自動更新 macOS 26.7.1、01:40 重開機，01:42 登入後全部正常啟動。
- 10/03 01:42 ～ 10/04 14:07 之間：com.coach.* 設定檔全被刪（10/04 14:07 有對話發現 curation-watch 不見，只重建那一個）。
- **刪的是清理軟體 CleanerCat（/Applications/CleanerCat.app，com.lightyear.CleanerCat）**，10/16 13:2x 查證：①它的使用日期有 10/04，設定裡 `lastCleanDate=2026-10-04`、當天 `dailyCleanCount=4`，資料夾 10/04 13:42 有寫入；②它的「已解除安裝 App 殘留檔（Uninstall Leftovers）」功能靠 `bundle_mappings.json` 判斷開機設定屬於哪個 App——表裡認得 openclaw、hermes（所以 ai.openclaw.*、ai.hermes.* 沒事），**不認得 com.coach、cloudflared**，就把它們當殘留檔清掉；③Claude／小龍蝦 8 個分身／赫米斯的紀錄都沒有刪除指令，也沒有 AI 操作 CleanerCat。它沒有自動排程、不常駐，是有人在畫面上手動按清理——**教練 10/16 13:19 親口確認是他本人按的**（這台 Mac 只有他能操作）。教練說以前清完重開機都沒事：查證過去使用是 4/7、4/29、5/23、5/24、6/5，當時網站設定檔大多還沒建（現存最早 7/13）；10/4 是第一次在有這些設定檔時清理，而且它的規則表 bundle_mappings.json 正好在 10/4 13:42:09 更新。教練看法：這是 CleanerCat 的 bug（把不屬於任何 App 的開機設定當殘留檔）。**用 CleanerCat 時不要勾「Uninstall Leftovers／殘留檔」，或先排除 ~/Library/LaunchAgents**；就算清掉，守門員也會補回。
- 10/05、10/09、10/12、10/13、10/14、10/15、10/16 02:32，至少 7 個對話都看到「No such file」或 ls 找不到，**沒有人當警訊處理**（包括我 10/16 02:32 重啟 event-webapp 時）。服務還在跑，是因為 launchd 記憶體裡還留著設定。
- 10/16 08:44:55 Mac 登出（install.log：loginwindow logoutNoReturn，不是系統更新）。當時聯想（Tailscale 100.95.122.29 = tree）從 05:00 起就一直用 RustDesk 連著，08:44:28 有遠端滑鼠點擊，最可能是遠端誤點登出。08:45 重新登入，小龍蝦 gateway 自動起來，但網站的設定檔已不在，**所有網站和通道都沒有再起來**。
- 11:52～12:20 教練用手機開的對話（session 33476b01）重建了 12 個設定檔（commit 723d246f4）。但 bni-chapters／mentor100／namecard／peipei-event／team 這 5 個漏了 `source .env`（後台登入、LINE 通知、名片辨識失效，資料沒外洩，因為頁面仍導向登入）。真鑽被誤判為「教練 9/18 說停用」而沒拉；接力棒原文其實是「**解**真鑽 DB 4 週停擺」。名片自動辨識 amber-watch 也被說成「找不回來」。
- 12:50 我用 TM 原檔把這 8 個還原（bootout → 複製 → bootstrap），12 個網域都回 200，真鑽回來。還原前的版本備份在 `workspace/state/backup_20261016_launchagents_before_restore/`。

**怎麼查、怎麼救**
- 警訊：`launchctl print gui/$(id -u)/<label>` 顯示 `path = ~/Library/LaunchAgents/x.plist`，但 `ls` 找不到那個檔 → 下次登出或重開機就會斷，**當場就要補**。
- 原檔：`tmutil listbackups` → `/Volumes/.timemachine/<id>/<日期>.backup/<日期>.backup/Data/Users/bymyway/Library/LaunchAgents/`（列一次就會自動掛上）。
- 這些網站的程式設定多半是 `/bin/bash -c "set -a; source <repo>/.env; set +a; exec venv/bin/python3 app.py"`；重建時少了 `.env`，網站照樣會回 200，看不出壞了。比對要看設定名稱，不能只看網址通不通。
- 還原：`launchctl bootout gui/$U/<label>`，再 `cp` 原檔，最後 `launchctl bootstrap gui/$U <plist>`。

**已上線的防線（10/16 12:58，`f90ba2012`）**：守門員 `scripts/launchagents_guard.sh`＋`ai.openclaw.launchagents-guard`（launchd WatchPaths 監看 LaunchAgents，登入時也跑），以 `ops/launchagents_backup/`（Time Machine 原檔 25 個＋守門員自己）為準，少檔補回、沒載入就載入、電報通知（10 分鐘節流），紀錄在 `~/Library/Logs/openclaw/launchagents_guard.log`。實測刪檔 10 秒內補回、卸載後自動重載。**要正式停掉某服務＝同時從 ops/launchagents_backup 刪掉並 commit，否則會被補回。** 反射 R-LAUNCHAGENTS-PLIST-MISSING（試金石 122）。worktree 對話寫正式目錄要教練授權，見 [[reference_worktree_session_edit_hook_blocks_openclaw_2026-10-15]]。
**還沒有**：網站本身掛了（例如通道掛掉）主動通知教練的外部偵測；這次教練是 3 小時後自己從手機發現的。
