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

## cycle=861 健康檢查（2026-09-08T22:12:30+08:00 TPE 週二晚上）

🔕 **安靜通過，不打擾教練。**

### v4.0 三關判斷（全 fail → 🔕 不 announce）

- **關卡一**（本輪還壞嗎？）❌ fail
  - Cron **26/26 全部健康**（CLI fallback 撈到完整 26 任務）：本任務 ok/CE=0 + 25 ok/CE=0
  - 23 lastRunStatus=ok + 3 at-pending idle（9/16 胸章、9/20 婚宴、12/1 車貸，未到執行時間正常）
  - 0 timeout / 0 INVALID_API_KEY / 0 overload / 0 CE≥3
- **關卡二**（provider overload？）❌ fail
  - 無錯誤訊息、無 overload 字眼
  - TG 通道探針守則 #19 當下實測 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- **關卡三**（影響教練/會員嗎？）❌ fail
  - 週二 22:12 晚上、教練沉默 **0.6h**（21:38 最後訊息至今，剛發言不久正常作息）
  - 零會員功能壞、零會員依賴任務受影響

### 第零步 v3.0 鐵律實測
- `sync_coach_last_message.sh` exit 0
- 教練真正最後訊息：`2026-09-08T21:38:50+08:00`
- silentH=**0.6**（fresh from Telegram API，echo log + memory 兩邊驗證）

### 環境快檢 ✅
- SOUL.md ×3 齊全（9015/1851/27527 bytes，兩份含棄用標記）
- Repo1=28 / Repo2=52（皆在警戒線邊，自然波動）
- 無 `.!` 鎖定檔
- HEARTBEAT.md ⬜ 真實待辦：**0 項**

### 自動修復動作
無（cron 26/26 全部健康、無 timeout / apiKey / 網路類錯誤需調參）

### 已落痕跡（雙檔鏡像 + JSON valid）
- ✅ `state/healthcheck_cycle` + `memory/healthcheck_cycle` = **861**
- ✅ `state/cumulative_green.txt` + `memory/cumulative_green.txt` = **214**（連續 33 輪全綠 cycle=829~861）
- ✅ `state/coach_silent.json` + `memory/coach_silent.json`（silentH=0.6 fresh from Telegram API）
- ✅ `state/heartbeat-state.json` + `memory/heartbeat-state.json` v4.0 三關快照、cronErrorJobs=0
- ✅ `state/healthcheck.log` + `memory/healthcheck.log` 追加 cycle=861

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
⏭️ 跳過 announce（v4.0 三關全 fail + 教練剛發言 0.6h 正常作息）

🔕 **結論：安靜通過，不打擾教練。下輪：23:12 cycle=862**
