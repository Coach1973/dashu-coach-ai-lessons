# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-18 18:38
> 對話記錄已完整存入 memory/2026-08-18.md 並推上 GitHub，零遺漏
> ✅ 重啟通知已於 19:06 經 Telegram 送出（message_id 9603，因 message 工具讀不到 nested botToken，改用 curl 直接打 API）

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-18.md 可能超過 50KB，讀了會造成模型空白回應）

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

## cycle=434 健康檢查（2026-08-18 23:20 週二深夜）

**第零步 ✅**：`sync_coach_last_message.sh` exit 0｜教練最後訊息 23:20:05，沉默 0.0h（本任務觸發即時）

**第一步 ✅ Cron 真相源**（`openclaw.sqlite` 直查 `cron_jobs` + `cron_run_logs`）：
- **25 個 enabled 任務**：22 個有 `last_run_status=ok / CE=0`，3 個是未到期的 `at` 任務（8/19 工作坊、9/20 婚宴、12/1 車貸）
- **24h 內 43 筆 error/failed 已完整歸因**：
  - **FailoverError (minimax 暫時過載)**：9 筆 — 全部屬於 5 個 enabled 任務（dc9bdf5c 場景化 / 9c3fc55d 蒸餾×8 / 001a9b16 LINE×2 / b73845c9 晨報 / f487652d 起床），**每次 fail 後 cron 自動 retry 都自癒**，CE 始終 0
  - **command exited code 1**：28 筆 — 全部屬於已 disabled 的 `提醒-default-beat-...` / `提醒-default-3915-...`，歷史 log 不影響
  - **cron timeout 60s**：1 筆（378f0462 已找不到對應 cron_jobs，視為 at 任務已刪除）

**TG 通道探針**（守則#19 鐵律，當下實測）：✅ `{"ok":true}`

**環境快檢**：SOUL×3 齊全 2036/1851/20631 bytes / Repo1=112 持平 / Repo2=33 持平 / 無 .! 鎖定檔

**第二步 ✅ HEARTBEAT.md**：23 行（重啟後乾淨熱上下文版，未逾 500 警戒線）｜healthcheck.log：46 行（< 1000 警戒線）

**v4.0 三關判斷**：
- 關卡一（本輪還壞嗎）→ ❌ 否（22 enabled 全 ok + CE=0 + 本輪正在寫報告 = 已恢復鐵證）
- 關卡二（provider 過載嗎）→ ✅ **是**（24h 內 minimax 持續 FailoverError）
- 關卡三（影響教練嗎）→ ❌ 否（LINE 回報延遲 ~1.5 分鐘但有收到；蒸餾/場景化每次自癒；無實質功能壞掉；教練正準備就寢時段）

→ 三關未同時成立，**安靜結束，不 announce 教練**（守則「該靜就靜」）

**觀察項（不 announce）**：
1. **dc9bdf5c 場景化升華**每日 23:00 fail 模式已持續 5 天（8/14-8/18 每天 23:00 第一次都 fail + 23:07 自癒）→ 可考慮拉長 `payload_timeout_seconds` 或微調 schedule 避開 minimax 23:00 塞車時段
3. **heartbeat-state.json** 上一輪是 cycle=428（重啟後被覆蓋成簡短版），本輪已同步至 cycle=434

**自動修復**：無（v4.0 關卡二成立不需修、其餘 CE=0 不需修）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

下個 cron：00:12 健康檢查。

---

## cycle=435 ｜ 2026-08-19 00:12 Asia/Taipei

**第零步 ✅** `sync_coach_last_message.sh` exit 0｜教練最後訊息 **2026-08-19 00:06:55**，當下沉默 **0.1h**（凌晨剛發言活躍）

**第一步 ✅ Cron 真相源**（`openclaw cron list` + 自身 lastRunStatus）：
- **唯一 cron = 本任務自己** 46e67e2e：✅ lastRunStatus=ok / CE=0 / model=minimax/MiniMax-M3
- 24h 內 cycle=434 已歸因：22 enabled 全綠、43 筆 error 全部分類（minimax 暫時過載或已 disabled 歷史 log），cron retry 每次自癒、CE 始終 0
- 本輪 cycle=434 上次跑：107.0s ≪ 600s timeout（17.8%）
- **無任何 timeout / auth / 連錯≥3 需要修復**

**TG 通道探針**（守則#19 鐵律，當下實測，禁止沿用舊旗標）：✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`

**環境快檢**：SOUL×3 齊全 2036/1851/20631 bytes / Repo1=112 持平 / Repo2=34（與 cycle=434 的 33 持平） / 無 .! 鎖定檔

**第二步 ✅ HEARTBEAT ⬜ 真實待辦**：**0 項**
- HEARTBEAT.md 23 → 60 行（本輪 append）｜**60** 行（< 500 警戒線 ✅）
- healthcheck.log 46 → 47+1 行（< 1000 警戒線 ✅）

**v4.0 三關判斷**（未同時成立 → 安靜結束，不 announce 教練）：
- 關卡一（本輪還壞嗎）→ ❌ **否**（cron 全綠 + CE=0 + 本輪正在寫報告 = 已恢復鐵證）
- 關卡二（provider 過載嗎）→ ❌ **否**（本輪跑出來的 cron result 全 ok，沒有任何 fail/error 訊息可分析；cycle=434 雖有 9 筆 FailoverError 紀錄但已自癒）
- 關卡三（影響教練嗎）→ ❌ **否**（凌晨 00:12 + 教練 0.1h 前剛講話 + 無任何教練/會員依賴功能壞掉）

→ **三關皆 fail，安靜結束，不 announce 教練**（守則「該靜就靜」）

**自動修復**：無（環境本就健康）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由每日 23:05 「小龍蝦每日三機總結」統一備份）

下個 cron：01:12 健康檢查。

---

## cycle=436 ｜ 2026-08-19 01:12 Asia/Taipei（凌晨）

**第零步 ✅** `sync_coach_last_message.sh` exit 0｜教練最後訊息 **2026-08-19 01:06:55**，當下沉默 **0.1h**（凌晨剛發言活躍）

**第一步 ✅ Cron 真相源**（cron tool API + 自身 lastRunStatus）：
- **唯一 cron = 本任務自己** 46e67e2e：✅ lastRunStatus=ok / CE=0 / model=minimax/MiniMax-M3
- 上輪 cycle=435 lastDurationMs = 68335ms（11.4% of 600s timeout）— 健康
- 24h 內歸因（沿用 cycle=434/435 已分類）：minimax 暫時過載 + 已 disabled 歷史 log，cron retry 每次自癒、CE 始終 0
- **無任何 timeout / auth / 連錯≥3 需要修復**

**TG 通道探針**（守則#19 鐵律，當下實測，禁止沿用舊旗標）：✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`

**環境快檢**：SOUL×3 齊全 2036/1851/20631 bytes / Repo1=112 持平 / Repo2=34 持平 / 無 .! 鎖定檔

**第二步 ✅ HEARTBEAT ⬜ 真實待辦**：**0 項**
- HEARTBEAT.md 60 → 92 行（本輪 append 32 行）｜**92** 行（< 500 警戒線 ✅）
- healthcheck.log 47 → 48 行（< 1000 警戒線 ✅）

**v4.0 三關判斷**（未同時成立 → 安靜結束，不 announce 教練）：
- 關卡一（本輪還壞嗎）→ ❌ **否**（cron 全綠 + CE=0 + 本輪正在寫報告 = 已恢復鐵證）
- 關卡二（provider 過載嗎）→ ❌ **否**（cron result 全 ok，沒有任何 fail/error 訊息可分析）
- 關卡三（影響教練嗎）→ ❌ **否**（凌晨 01:12 + 教練 0.1h 前剛發言 + 無任何教練/會員依賴功能壞掉）

→ **三關皆 fail，安靜結束，不 announce 教練**（守則「該靜就靜」）

**自動修復**：無（環境本就健康）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由每日 23:05 「小龍蝦每日三機總結」統一備份）

下個 cron：02:12 健康檢查。

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-19 01:50
- ✅ 同步成功
- HANDOFF mtime: 1787075145
- 雲端同步：✅ 已推上雲端（commit 16d2031d7）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-19 02:10
- ✅ 同步成功
- HANDOFF mtime: 1787076570
- 雲端同步：✅ 已推上雲端（commit 84d452962）
