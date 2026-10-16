# com.coach.* launchd 設定備份（2026-10-16 更新為完整版）

這裡是所有網站「程式＋通道」自動啟動設定的正本（25 個 com.coach.*.plist），守門員以這裡為準。

- **起因**：10/3～10/4 之間 ~/Library/LaunchAgents 的 com.coach.* 被刪，服務靠記憶體撐到 10/16 08:44 登出後全斷。
  10/16 中午手機重建的版本有 5 個少了 `source .env`，並缺真鑽（zhenzuan）兩個和名片監看（namecard-amber-watch）；
  12:50 已改用 Time Machine 10/03 01:10 的原檔還原，本目錄現在就是那份原檔。
- **守門員**：`scripts/launchagents_guard.sh`，由 `ai.openclaw.launchagents-guard.plist`（本目錄也有一份）監看
  ~/Library/LaunchAgents，少檔就補回並載入，再通知教練。每次登入也會跑一次。
- **網站實測（10/16 加）**：守門員跑完後會用公開網址逐一實測 13 個網站，連不上（530／1033／000）等約 75 秒仍不通才通知教練；新增或移除網站要同步改 `scripts/launchagents_guard.sh` 的 `SITES`。zhencheng 在 ~/.cloudflared 有設定但沒有服務，故不列入。
- **要正式停掉某個服務**：從本目錄刪掉那個 plist 並 commit，否則守門員會補回來。
- **新增服務**：plist 放進 ~/Library/LaunchAgents 後，也複製一份到這裡並 commit。
- 密碼／金鑰都在各專案 .env（plist 只 source 它），本目錄不含機密。
- 手動全部還原：`cp ops/launchagents_backup/com.coach.*.plist ~/Library/LaunchAgents/ && for f in ~/Library/LaunchAgents/com.coach.*.plist; do launchctl bootstrap gui/$(id -u) $f 2>/dev/null; done`
