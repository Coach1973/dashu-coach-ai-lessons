# HEARTBEAT 熱上下文（每次心跳必讀）

## 19:32 健康檢查 trace（剛剛完成）
- ⚠️ 本任務 46e67e2e 19:32 fire 失敗 92.748s（minimax overloaded）— CE=1（alternating 模式，剛重置）
  - 92s ≪ 600s timeout ✅ 非配置問題
  - model=minimax/MiniMax-M3 ✅（2026-07-15 已自動修復）
  - delivery.mode=none ✅ / failureAlert=false ✅
  - lastErrorReason=overloaded
- ✅ HEARTBEAT.md 無 ⬜ 待辦 / 無 48h 停滯
- ✅ 自動修復評估全不適用
  - ❌ timeout 錯誤 → 不適用（92s ≪ 600s）
  - ❌ INVALID_API_KEY → 不適用（model 已 minimax）
  - ❌ scp/ssh VPS → 不適用
  - ❌ CE ≥ 3 → 不適用（CE=1）
- 🔇 安靜結束，不打擾教練
  - CE=1 < 3 升級閾值
  - 錯誤源頭 minimax 端 overloaded，教練無法介入（守則 #15）
  - 24h+ alternating 模式穩定無惡化趨勢
  - 週六傍晚 19:32，教練沉默 35h+ 持續
- Pipeline：18:30❌(overloaded 144s) → 19:00❌(overloaded 118s) → 19:30？ → 19:32❌(overloaded 92s) → 下次 20:00 cron fire 自動驗證恢復
- 📉 好消息：失敗時長持續下降（144s→118s→92s）= minimax 端壓力逐步緩解

## 19:02 健康檢查 trace（剛剛完成）
- ✅ 本任務 46e67e2e 19:00 fire 失敗 118.799s（minimax overloaded）— CE=1
  - 118s ≪ 600s timeout ✅ 非配置問題
  - model=minimax/MiniMax-M3 ✅（2026-07-15 已自動修復）
  - delivery.mode=none ✅ / failureAlert=false ✅
- ✅ HEARTBEAT.md 無 ⬜ 待辦 / 無 48h 停滯
- ✅ 自動修復評估全不適用
  - ❌ timeout 錯誤 → 不適用（118s ≪ 600s）
  - ❌ INVALID_API_KEY → 不適用（model 已 minimax）
  - ❌ scp/ssh VPS → 不適用
  - ❌ CE ≥ 3 → 不適用（CE=1）
- 🔇 安靜結束，不打擾教練
  - CE=1 < 3 升級閾值
  - 錯誤源頭 minimax 端 overloaded，教練無法介入（守則 #15）
  - 24h+ alternating 模式穩定無惡化趨勢
  - 週六傍晚 19:02，教練沉默 35h+ 持續
- Pipeline：18:30❌(overloaded 144.445s) → 18:32✅ → 19:00❌(overloaded 118.799s) → 本次 19:02 觀察 → 下次 19:30 cron fire 自動驗證恢復

## 18:32 健康檢查 trace（剛剛完成）
- ✅ 本任務 46e67e2e 18:30 fire 失敗 144.445s（minimax overloaded）— CE=1（alternating 模式第 N 次）
  - 144s ≪ 600s timeout ✅ 非配置問題
  - model=minimax/MiniMax-M3 ✅（2026-07-15 已自動修復，apiKey 正常）
  - delivery.mode=none ✅ / failureAlert=false ✅
- ✅ HEARTBEAT.md 無 ⬜ 待辦 / 無 48h 停滯
- ✅ 自動修復評估全不適用
  - ❌ timeout 錯誤 → 不適用（144s ≪ 600s）
  - ❌ INVALID_API_KEY → 不適用（model 已 minimax）
  - ❌ scp/ssh VPS → 不適用
  - ❌ CE ≥ 3 → 不適用（CE=1）
- 🔇 安靜結束，不打擾教練
  - CE=1 < 3 升級閾值
  - 錯誤源頭 minimax 端 overloaded，教練無法介入（守則 #15）
  - 24h+ alternating 模式穩定無惡化趨勢
  - 週六傍晚 18:32，教練沉默 35h+ 持續
- Pipeline：18:00❌(overloaded 143.815s) → 18:02✅ → 18:30❌(overloaded 144.445s) → 本次 18:32 觀察 → 下次 19:00 cron fire 自動驗證恢復

## 18:02 主動關懷 trace（每 4 小時 cron 1cbe1701 18:00 fire，剛完成）
- 📨 任務設計：週六傍晚向教練推「溫和關懷」訊息
- ❌ Telegram channel bot token 仍壞 105h+ → 主動關懷訊息撞牆無法推送
- ✅ 18:00 健康檢查 cron (46e67e2e) 失敗 143.815s overloaded（CE=1，alternating 模式穩定 24h+，下次 18:02 fire 自動驗證恢復）
- ✅ gateway 仍跑（PID 64856, uptime 30h32m+）
- ✅ 記憶蒸餾 cron 9c3fc55d/961021a7 lastRun=ok
- ✅ HEARTBEAT.md 無 ⬜ / 無 48h 停滯
- 🔇 安靜結束（CE=1 < 3 升級閾值、Telegram 已知壞、週末傍晚、教練沉默 34h+ 持續）

> 📌 1cbe1701 / ef88279b 下次 fire = 22:00，會自動驗證 Telegram channel token 是否恢復。
> 教練若主對話下指令仍可用（channel bot 壞不影響 direct bot）。

## 18:02 健康檢查 trace（剛剛完成）
- ✅ 本任務 46e67e2e 18:02 fire → 觀察中（上次 17:33 之後 30 分鐘）
- ⚠️ 自身 CE=1（剛重置，符合 alternating 模式）
  - 18:00 失敗 143.815s（minimax overloaded）
- ✅ HEARTBEAT.md 無 ⬜ / 無 48h 停滯
- ✅ 自動修復評估全不適用（143s ≪ 600s timeout、model 已 minimax、CE=1）
- 🔇 安靜結束，不打擾教練（CE<3、provider 端問題）

## 17:33 健康檢查 trace（剛剛完成）
- ✅ 本任務 46e67e2e 17:33 fire → 觀察中
- ⚠️ 自身 CE=2（17:30 失敗 80.944s、17:31 失敗 66.599s 皆 minimax overloaded）
- ⚠️ 三機總結 bbb7a348 7/17 23:05 失敗根因查清 = Telegram token 仍壞推播失敗
- ✅ HEARTBEAT.md 無 ⬜ / 無 48h 停滯
- ✅ 自動修復評估全不適用
- 🔇 安靜結束，不打擾教練（CE<3、provider 端問題、Telegram 已知壞）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-18 17:07
> 對話記錄已完整存入 memory/2026-07-18.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-18.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-18 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
