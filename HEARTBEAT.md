# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-09-09 18:00
> 對話記錄已完整存入 memory/2026-09-09.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-09-09.md 可能超過 50KB，讀了會造成模型空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）


---

## cycle=883 健康檢查（2026-09-09 18:12 TPE 週三晚上）

🔕 **安靜通過，不打擾教練。**

- **第零步**：sync_coach_last_message.sh exit 0｜silentH=**15.6** fresh from TG API
- **第一步 Cron**：1/1 ok（本任務 lastStatus=ok/CE=0/lastDurationMs=210s ≪ 600s timeout）｜0 timeout/INVALID_API_KEY/overload/CE≥3
- **第二步 HEARTBEAT ⬜**：0 項
- **環境快檢**：SOUL×3 齊全（9015/1851/27527 bytes）｜Repo1=28/Repo2=38｜無 `.!` 鎖定檔
- **TG 探針守則#19**：ok:true ✅
- **gateway**：openclaw 18789/200 + hermes 8765/200 ✅
- **launchd**：cron-daemon 40579 / openclaw.gateway 24857 / hermes.menubar 43121 等全綠
- **v4.0 三關**：全 fail → 🔕 不 announce（本輪成功 + 無 overload + 下班時段 + 零會員功能壞）
- **State 雙檔鏡像**：cycle 882→**883**｜cumulativeGreen 234→**235**（連55輪全綠 cycle=829~883）｜silentH=15.6 fresh
- ⏭️ 跳過 commit+push（23:05 三機總結統一備份）｜跳過 announce

🔕 **下輪：19:12 cycle=884**

---

## cycle=884 健康檢查（2026-09-09 19:12 TPE 週三晚上）

🔕 **安靜通過，不打擾教練。**

- **第零步**：sync_coach_last_message.sh exit 0｜silentH=**16.6** fresh from TG API（since 02:36:55）
- **第一步 Cron**：1/1 ok（本任務 lastStatus=ok/CE=0）｜0 timeout/INVALID_API_KEY/overload/CE≥3
- **第二步 HEARTBEAT ⬜**：0 項
- **環境快檢**：SOUL×3 齊全｜Repo1=28/Repo2=38（自然波動 < 50 警戒線）｜無 `.!` 鎖定檔
- **TG 探針守則#19**：ok:true ✅（當下實測）
- **gateway**：openclaw 18789/200 + hermes 8765/200 ✅（hermes 服務實際活著，launchd -9 是上次 SIGKILL 殘留，watchdog 已接手）
- **launchd**：cron-daemon 40579 / hermes.gateway 70523（state=running, pid=70523）等全綠
- **v4.0 三關**：全 fail → 🔕 不 announce（本輪成功 + 無 overload + 下班時段 + 零會員功能壞）
- **State 雙檔鏡像**：cycle 883→**884**｜cumulativeGreen 235→**236**（連56輪全綠 cycle=829~884）｜consecutiveGreen 55→**56**｜silentH=16.6 fresh
- ⏭️ 跳過 commit+push（23:05 三機總結統一備份）｜跳過 announce

🔕 **下輪：20:12 cycle=885**

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-09 19:30
- ✅ 同步成功
- HANDOFF mtime: 1788953449
- 雲端同步：✅ 已推上雲端（commit b7cd578ab）
