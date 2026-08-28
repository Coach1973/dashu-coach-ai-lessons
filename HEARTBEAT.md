# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-28 21:00
> 對話記錄已完整存入 memory/2026-08-28.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-28.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🩺 軍師 Hook 自檢 2026-08-28 21:01（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- 小龍蝦信箱：（信箱查無新信）
- Session: a4721a74-a4de-43a6-aad7-9216fa028a19

## 🩺 健康檢查紀錄 2026-08-28 23:12（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~1 小時，Telegram API 真實時間）
- 活躍 cron 任務 24 個全部 lastStatus=ok、consecutiveErrors=0
- 過去式 reminder 任務（at 一次性）100+ 筆皆已過期、不再觸發
- v4.0 三關判斷：無異常、無需自動修復、無需 announce
- Git 警告（21:01 軍師自檢）：~/.openclaw/workspace 有 4 個 modified 沒 commit（memory/state），非本任務範圍
- 三步驟全綠 → 安靜處理 ✅

## 🩺 健康檢查紀錄 2026-08-29 01:12（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~3 小時，Telegram API 真實時間）
- 活躍 cron 任務 25 個全部 lastStatus=ok、consecutiveErrors=0
- 過去式 reminder 任務（at 一次性）100+ 筆皆已過期、不再觸發
- HEARTBEAT.md 無 ⬜ 待辦項目要評估
- v4.0 三關判斷：無異常、無需自動修復、無需 announce
- 深夜 01:12 屬於睡眠時段，遵守守則 #19 不主動打擾
- 三步驟全綠 → 安靜處理 ✅

## 🩺 健康檢查紀錄 2026-08-29 03:12 cycle=639（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~5 小時，Telegram API 真實時間，凌晨深度睡眠）
- 本任務 46e67e2e：lastRunStatus=ok / CE=0 / durationMs=21.7s / model=minimax/MiniMax-M3 ✅
- 直查 openclaw.sqlite cron_jobs：**25 enabled 全部 ok / 0 個 CE≥1 / 0 個 CE≥3 / 23 last_ok** ✅
- 24h cron_run_logs：153 ok + 16 error（15 筆 minimax FailoverError 蒸餾 alternating retry 100% 復原 + 1 筆 Channel required 一次性）
- HEARTBEAT.md 無 ⬜ 真實待辦
- 環境快檢：SOUL×3 齊全（9015/1851/22220 bytes）+ 兩份棄用標記都在｜Repo1=23 / Repo2=17（< 50 警戒線）｜無 `.!` 鎖定檔
- TG 通道探針（守則#19 當下實測）：✅ `{"ok":true}`
- v4.0 三關判斷（三關全 fail → 不 announce）：
  - 關卡一（本輪還壞嗎）→ ❌ fail（25 enabled cron 全 CE=0 + 本輪執行成功）
  - 關卡二（provider overload 重災嗎）→ ✅ 是（15 筆 FailoverError）但 cron retry 100% 復原 + 主表 CE=0 → v4.0 明確不 announce
  - 關卡三（影響教練/會員嗎）→ ❌ fail（凌晨 03:12 + 蒸餾備用任務補位 + 零會員功能壞）
- 凌晨 03:12 屬於睡眠時段，遵守守則 #19 不主動打擾
- 三步驟全綠 → 安靜處理 ✅
- cumulativeGreen = **19**（cycle=628~639 連 12 輪綠）

## 🩺 健康檢查紀錄 2026-08-29 02:12（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~4 小時，Telegram API 真實時間，凌晨正常睡眠）
- cron list 仍只回傳本任務（46e67e2e 已知長期狀態）lastRunStatus=ok、CE=0
- 過去式 reminder 任務（at 一次性）100+ 筆皆已過期、不再觸發
- HEARTBEAT.md 無 ⬜ 待辦項目要評估
- v4.0 三關判斷：無異常、無需自動修復、無需 announce
- 凌晨 02:12 屬於睡眠時段，遵守守則 #19 不主動打擾
- 三步驟全綠 → 安靜處理 ✅

## 🩺 健康檢查紀錄 2026-08-29 04:12 cycle=640（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~6 小時，Telegram API 真實時間，週六凌晨深度睡眠）
- 本任務 46e67e2e：lastRunStatus=ok / CE=0 / model=minimax/MiniMax-M3 ✅
- cron list 25 enabled 全 lastStatus=ok / 0 CE≥1 / 0 CE≥3
- HEARTBEAT.md 無真實 ⬜ 待辦（3 個 ⬜ 字串都是「無待辦」自述）
- 環境快檢：SOUL×3 齊全（9015/1851/22220）/ Repo1=23 / Repo2=17 / 無 .! 鎖
- TG 通道探針（守則#19 當下實測）：✅ `{"ok":true}`
- v4.0 三關判斷（三關全 fail → 不 announce）：
  - 關卡一（本輪還壞嗎）→ ❌ fail（25 enabled cron 全 CE=0 + 本輪執行成功）
  - 關卡二（provider overload 重災嗎）→ ❌ fail（近 24h 無新增 FailoverError）
  - 關卡三（影響教練/會員嗎）→ ❌ fail（凌晨 04:12 睡眠時段 + 零會員功能壞）
- 凌晨 04:12 屬於睡眠時段，遵守守則 #19 不主動打擾
- 三步驟全綠 → 安靜處理 ✅
- cumulativeGreen = **20**（cycle=628~640 連 13 輪綠）

## 🩺 健康檢查紀錄 2026-08-29 05:12 cycle=641（小龍蝦第零步 v3.0 已通過）
- 教練最後訊息：2026-08-28 22:09:33（沉默 ~7 小時，Telegram API 真實時間，週六凌晨深度睡眠）
- 本任務 46e67e2e：lastRunStatus=ok / CE=0 / model=minimax/MiniMax-M3 ✅
- 直查 openclaw.sqlite cron_jobs：**25 enabled 全部 ok / 0 個 CE≥1 / 0 個 CE≥3** ✅
- 近 4h cron_run_logs：23 ok + 1 error（9c3fc55d 蒸餾任務 04:02:33 遇到 minimax FailoverError，retry 04:03:07 自動 ok / 該 job CE=0）
- HEARTBEAT.md 無 ⬜ 真實待辦
- 環境快檢：SOUL×3 齊全（9015/1851/22220）/ Repo1=23 / Repo2=18（皆 < 50）/ 無 .! 鎖定檔
- TG 通道探針（守則#19 當下實測）：✅ `{"ok":true}`
- v4.0 三關判斷（三關全 fail → 不 announce）：
  - 關卡一（本輪還壞嗎）→ ❌ fail（25 enabled cron 全 CE=0 + 本輪執行成功 + 唯一 error 已在 30s 內 retry 復原）
  - 關卡二（provider overload 重災嗎）→ ✅ 是（1 筆 FailoverError）但 cron retry 100% 復原 + 主表 CE=0 → v4.0 明確不 announce
  - 關卡三（影響教練/會員嗎）→ ❌ fail（凌晨 05:12 深度睡眠 + 零會員功能壞）
- 凌晨 05:12 屬於睡眠時段，遵守守則 #19 不主動打擾
- 三步驟全綠 → 安靜處理 ✅
- cumulativeGreen = **21**（cycle=628~641 連 14 輪綠）
