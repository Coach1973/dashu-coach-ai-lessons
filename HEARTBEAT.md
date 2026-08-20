# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-20 20:07
> 對話記錄已完整存入 memory/2026-08-20.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-20.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 健康檢查 cycle=466（2026-08-20 20:14:46）
- 第零步 ✅ exit 0，教練沉默 0.1 小時
- cron 失敗掃描：所有週期任務最新一次都成功，無需自動修復
- v4.0 三關判斷：不 announce

## 健康檢查 cycle=467（2026-08-20 21:12）
- 第零步 ✅ exit 0，教練最後訊息 2026-08-20 20:06:55（沉默 1.1 小時，符合 context overflow 後重啟的正常現象，無打擾必要）
- cron 掃描：目前只有 1 個啟用 cron job（本任務自己），lastRunStatus=ok，無失敗任務
- HEARTBEAT ⬜ 檢查：無未辦項目
- v4.0 三關判斷：不 announce，安靜記錄

## 健康檢查 cycle=468（2026-08-20 22:00）
- 第零步 ✅ exit 0，教練沉默 ~1.9h（context overflow 後正常沈默，無打擾必要）
- TG 通道本輪實測 ok:true（bot=openclaw_macbook4_bot, chat=6124913915，遵守守則 #19 不盲信舊旗標）
- cron 掃描：27 個啟用 job 全部 lastRunStatus=ok，無失敗任務；4 個 `提醒-default-beat-1787248800000` 同時段排程（明天 06:00），為 beat polling 規律產物，無異常
- HEARTBEAT ⬜ 檢查：無未辦項目
- v4.0 三關判斷：不 announce（深夜前 1h、教練沉默 < 4h、無緊急）→ 安靜記錄
- 待觀察：23:00 場景化升華、23:05 三機每日總結 1h 後即將排程

## 健康檢查 cycle=469（2026-08-20 22:12）
- 第零步 ✅ exit 0，教練最後訊息 20:06:55，沉默 2.1h（context overflow 重啟後正常沈默）
- cron 掃描：本任務 lastRunStatus=ok / CE=0 / durationMs=13795（健康，遠低於 timeout=600s）；cron tool 已知過濾限制僅回本任務；過去 24h 偶發為本任務 Edit HEARTBEAT.md transient，cron retry 全部自癒
- 環境快檢：SOUL×3 齊全 ✅ / Repo1=112 持平 / Repo2=25 持平 / 無 .! 鎖 ✅
- TG 通道探針（守則#19 當下實測）：✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- HEARTBEAT � 真實待辦：0 項
- HEARTBEAT.md：41 行（<500 警戒線）
- v4.0 三關判斷（三關全 fail → 不 announce）：
  - 關卡一（本輪還壞嗎）→ ❌ 否（上一輪 ok + 本輪執行成功 + CE=0）
  - 關卡二（provider 暫時過載嗎）→ ❌ 否（無 FailoverError / 無 overloaded）
  - 關卡三（影響教練/會員嗎）→ ❌ 否（22:12 深夜時段 + 教練 context overflow 後正常沈默 + 無會員功能壞）
- 待觀察：23:00 場景化升華（49 分鐘後）、23:05 三機每日總結（54 分鐘後）

## 健康檢查 cycle=470（2026-08-20 22:20）
- 第零步 ✅ exit 0，教練沉默 ~2.2h（context overflow 重啟後正常沈默）
- **本輪觸發源**：cron job `56b65afe-d5d3-40a6-9d9c-52d606da206c`（📨 晚間 22:20 提醒寄 50 封信｜20天計畫，8/12~8/21）──本任務就是信件提醒事件，不是普通心跳
- TG 通道探針（守則#19 當下實測）：✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- 環境快檢：SOUL×3 齊全 ✅ / Repo1=112 持平 / Repo2=25 持平 / 無 .! 鎖 ✅
- cron 掃描：27 個啟用 job 全部 lastRunStatus=ok，無失敗任務
- **20 天計畫進度**：今天是 8/20（第 19/20 天），明天 8/21 是最後一天（第 20/20 天）
- 已主動發 TG 訊息到教練主對話（chat 6124913915），內容包含「提醒寄信」+「19/20 天進度」+「明天最後一天」
- v4.0 三關判斷：本輪觸發源是「事件 cron」（不是普通 heartbeat），且教練沉默 2.2h 主對話未呼應 → **主動 anneal 提醒**（已完成）
- 待觀察：23:00 場景化升華（40 分鐘後）、23:05 三機每日總結（45 分鐘後）
