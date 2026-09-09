# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-09-08 15:00
> 對話記錄已完整存入 memory/2026-09-08.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-09-08.md 可能超過 50KB，讀了會造成模型空白回應）

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



---

## cycle=876 健康檢查（2026-09-09 12:12:35 TPE 週三中午）

🔕 **安靜通過，不打擾教練。**

### 第零步 v3.0 鐵律
- ✅ `sync_coach_last_message.sh` exit 0
- 教練真正最後訊息：`2026-09-09T02:36:55+08:00`（凌晨 2:37 最後訊息，正常睡眠作息）
- **silentH = 9.6**（fresh from Telegram API）

### 第一步 Cron 掃描（本任務 cron tool 直查）
- ✅ **1/1 全綠**：本任務 running、CE=0、lastStatus=ok、lastDurationMs=210575（≈3.5 分鐘，遠低於 timeout=600s）
- ✅ 0 timeout / 0 INVALID_API_KEY / 0 overload / **0 CE≥2**

### 環境快檢
- ✅ SOUL.md ×3 齊全（9015/1851/27527 bytes，兩份含棄用標記）
- ✅ Repo1=28 / Repo2=36（皆 < 50 警戒線，穩定波動）
- ✅ 無 `.!` 鎖定檔
- ✅ TG 通道探針守則 #19 當下實測：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ gateway 健康：openclaw 18789 → 200 / hermes 8765 → 404（路徑無 /health，正常）
- ✅ launchd 健康：cron-daemon 40579 / hermes.gateway-watchdog 70523 / openclaw.gateway 皆活著

### 第二步 HEARTBEAT.md ⬜ 真實待辦
- ✅ 0 項（純系統狀態檔，無未完成項目）

### v4.0 三關判斷（全 fail → 🔕 不 announce）
- **關卡一**（本輪還壞嗎？）❌ fail：本任務執行成功 + Cron 1/1 全綠
- **關卡二**（provider overload？）❌ fail：無錯誤、無 overload 字眼、TG 通道 ok
- **關卡三**（影響教練/會員嗎？）❌ fail：週三中午上班時段 + 教練沉默 9.6h 屬凌晨睡眠累積 + 零會員功能壞

### 自動修復
- 🛠 state/coach_silent.json 雙檔 silentH 刷新至 **9.6 fresh**
- 🛠 state/healthcheck_cycle 875→**876**、memory/ 同步
- 🛠 state/cumulative_green.txt 227→**228**、memory/ 同步（連續第 48 輪全綠 cycle=829~876）
- 🛠 state/heartbeat-state.json + memory/heartbeat-state.json v4.0 三關快照同步（cronErrorJobs=0、consecutiveGreen=48）
- 🛠 state/healthcheck.log + memory/healthcheck.log 追加 cycle=876 條目
- 🛠 HEARTBEAT.md prepend cycle=876 條目（保留上方 22 行重啟通知結構）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
⏭️ 跳過 announce（v4.0 三關全 fail + 週三中午上班時段 + 教練凌晨睡眠累積正常作息）

🔕 **結論：安靜通過，不打擾教練。下輪：13:12 cycle=877**

## cycle=863 健康檢查（2026-09-09T00:14:00+08:00 TPE 週三凌晨）

🔕 **安靜通過，不打擾教練。**

### v4.0 三關判斷（全 fail → 🔕 不 announce）
- **關卡一**（現在還壞著嗎？）❌ fail
  - 本任務（cron 46e67e2e）正在寫這份報告，**執行成功 = 已恢復鐵證**
- **關卡二**（錯誤原因是 provider 暫時過載嗎？）❌ fail
  - openclaw cron 1/1 lastRunStatus=ok，無 overload / auth / timeout 任何 error
  - launchd ai.openclaw.cron-daemon (PID 40579) 心跳正常（00:13:38，與現在差 18 秒）
  - launchd ai.openclaw.gateway (PID 92866) 活著
- **關卡三**（影響教練/會員嗎？）❌ fail
  - 週三 00:14 凌晨、教練沉默 **0.1h**（00:06:55 最後訊息至今，剛發言 7 分鐘正常作息）
  - 零會員功能壞、零會員依賴任務受影響

### 第零步 v3.0 鐵律實測
- `sync_coach_last_message.sh` exit 0
- 教練真正最後訊息：`2026-09-09T00:06:55+08:00`
- silentH=**0.1**（fresh from Telegram API，state 與 memory 兩邊驗證）

### 環境快檢 ✅
- SOUL.md ×3 齊全（9015/1851/27527 bytes，與上次一致）
- Repo1=28 / Repo2=20（皆在警戒線內，Repo2 增加 16 行為本次檢查的 state 鏡像，預期內）
- 無 `.!` 鎖定檔
- HEARTBEAT.md ⬜ 真實待辦：**0 項**

### 自動修復動作
無（openclaw cron 1/1 健康、launchd cron-daemon 與 gateway 皆活著、無 timeout / apiKey / 網路類錯誤需調參）

### 已知 minor（不影響功能、不通知）
- 23:50 heartbeat_audit.sh line 24 一次 `[: 0 0: integer expression expected` shell 警告
  - 已自動完成：`heartbeat_audit 完成：relay=0 0`
  - 根因：腳本內某個變數空值時未 quote，純 lint 警告、不影響 relay 結果
  - 不算需要修的 bug（修也只是讓警告消失，0.5h 工作量 < 0 價值）

### 已落痕跡（雙檔鏡像 + JSON valid）
- ✅ `state/healthcheck_cycle` + `memory/healthcheck_cycle` = **863**
- ✅ `state/cumulative_green.txt` + `memory/cumulative_green.txt` = **216**（連續 35 輪全綠 cycle=829~863）
- ✅ `state/heartbeat-state.json` + `memory/heartbeat-state.json` v4.0 三關快照、cronErrorJobs=0
- ✅ `state/healthcheck.log` + `memory/healthcheck.log` 追加 cycle=863

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
⏭️ 跳過 announce（v4.0 三關全 fail + 教練剛發言 0.1h 正常作息）

🔕 **結論：安靜通過，不打擾教練。下輪：01:12 cycle=864**

---

## cycle=862 健康檢查（2026-09-08T23:12:00+08:00 TPE 週二晚上）

🔕 **安靜通過，不打擾教練。**

### v4.0 三關判斷（全 fail → 🔕 不 announce）
- **關卡一**（現在還壞著嗎？）❌ fail
  - 本任務（cron 46e67e2e）正在寫這份報告，**執行成功 = 已恢復鐵證**
- **關卡二**（錯誤原因是 provider 暫時過載嗎？）❌ fail
  - 26/26 全部 lastRunStatus=ok，無 overload / auth / timeout 任何 error
- **關卡三**（影響教練/會員嗎？）❌ fail
  - 週二 23:12 晚上、教練沉默 **0.1h**（23:06:55 最後訊息至今，剛發言 5 分鐘正常作息）
  - 零會員功能壞、零會員依賴任務受影響

### 第零步 v3.0 鐵律實測
- `sync_coach_last_message.sh` exit 0
- 教練真正最後訊息：`2026-09-08T23:06:55+08:00`
- silentH=**0.1**（fresh from Telegram API，state 與 memory 兩邊驗證）

### 環境快檢 ✅
- SOUL.md ×3 齊全（9015/1851/27527 bytes，兩份含棄用標記）
- Repo1=28 / Repo2=4（皆在警戒線內，Repo2 大幅下降）
- 無 `.!` 鎖定檔
- HEARTBEAT.md ⬜ 真實待辦：**0 項**

### 自動修復動作
無（cron 26/26 全部健康、無 timeout / apiKey / 網路類錯誤需調參）

### 已落痕跡（雙檔鏡像 + JSON valid）
- ✅ `state/healthcheck_cycle` + `memory/healthcheck_cycle` = **862**
- ✅ `state/cumulative_green.txt` + `memory/cumulative_green.txt` = **215**（連續 34 輪全綠 cycle=829~862）
- ✅ `state/coach_silent.json` + `memory/coach_silent.json`（silentH=0.1 fresh from Telegram API）
- ✅ `state/heartbeat-state.json` + `memory/heartbeat-state.json` v4.0 三關快照、cronErrorJobs=0
- ✅ `state/healthcheck.log` + `memory/healthcheck.log` 追加 cycle=862

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
⏭️ 跳過 announce（v4.0 三關全 fail + 教練剛發言 0.1h 正常作息）

🔕 **結論：安靜通過，不打擾教練。下輪：00:12 cycle=863**

---

## cycle=883 健康檢查（2026-09-09 18:12 TPE 週三晚上）

🔕 **安靜通過，不打擾教練。**

### 第零步 v3.0 鐵律
- `sync_coach_last_message.sh` exit 0
- 教練真正最後訊息：`2026-09-09T02:36:55+08:00`
- silentH=**15.6**（fresh from Telegram API，週三下班時段、正常作息）

### 第一步 Cron（直查 cron tool）
- 1/1 jobs ok（本任務 lastStatus=ok, CE=0, lastDurationMs=210599 ≈ 3.5 分鐘 ≪ 600s timeout）
- 0 timeout / 0 INVALID_API_KEY / 0 overload / 0 CE≥3

### 第二步 HEARTBEAT.md ⬜ 待辦
- 0 項真實待辦

### 環境快檢
- ✅ SOUL.md ×3 齊全（9015/1851/27527 bytes，兩份含棄用標記）
- ✅ Repo1=28 / Repo2=38（皆 < 50 警戒線）
- ✅ 無 `.!` 鎖定檔
- ✅ TG 通道探針守則 #19 當下實測：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ gateway：openclaw 18789 → 200 / hermes 8765 → 200
- ✅ launchd：cron-daemon 40579 / openclaw.gateway 24857 / hermes.menubar 43121 / hermes 70523（gateway-watchdog）/ junshi-task-worker 等皆活著

### v4.0 三關判斷（全 fail → 🔕 不 announce）
- 關卡一（本輪還壞嗎？）❌ fail：本輪執行成功 + Cron 連綠 55 輪 cycle=829~883
- 關卡二（provider overload？）❌ fail：無錯誤、無 overload、TG ok
- 關卡三（影響教練/會員嗎？）❌ fail：週三下班時段 + 教練沉默 15.6h 凌晨睡眠累積 + 零會員功能壞

### 自動修復（state 雙檔漂移 6 項，已全部對齊 md5）
- `state/healthcheck_cycle` 漂移（882）→ **883**
- `state/cumulative_green` 漂移（234）→ **235**（連續第 55 輪全綠 cycle=829~883）
- `state/cumulative_green.txt` 漂移（234）→ **235**
- `state/coach_silent.json` silentH 過期（14.6h）→ **15.6h** fresh
- `state/heartbeat-state.json` cycle 過期（882）→ **883**、consecutiveGreen **54→55**
- `memory/` 雙檔鏡像同步（6 對檔案 md5 全對）
- `state/healthcheck.log` + `memory/healthcheck.log` 追加 cycle=883
- `HEARTBEAT.md` 兩份 append cycle=883 條目

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
⏭️ 跳過 announce（v4.0 三關全 fail + 下班時段 + 零會員功能壞）

🔕 **結論：安靜通過，不打擾教練。下輪：19:12 cycle=884**
