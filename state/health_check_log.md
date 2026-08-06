# 🦞 健康檢查歷史日誌

## 2026-08-06 02:32 CST (週四凌晨)

**檢查範圍**：cron_jobs 全部 50 個任務（從 sqlite 直接查，cron list API 只列 1 個有 bug，已用 workaround）。

**整體健康**：
- 36 個 enabled 任務，2 個有 CE > 0
- 34 個 enabled 任務 CE = 0 ✅（18 個 recurring + 18 個未來 at）

**錯誤任務**：

| Job | CE | lastDurationMs | lastError |
|---|---|---|---|
| 🦞 小龍蝦每日三機總結（每日23:05） | **2** | 283,593ms | `⚠️ 🎯 Update Goal: complete failed` |
| 🦞 每30分鐘任務健康檢查（本任務） | 1 | 88,464ms | `FailoverError: temporarily overloaded` |

**🦞 三機總結分析**（CE=2）：
- 2026-08-04 23:13 error：`⚠️ ✉️ Message: reply to 1, thread 0 failed`（duration 327s）→ **教練當天沒收到總結推播**（failureNotificationDelivery.delivered=false）
- 2026-08-05 23:11 error：`⚠️ 🎯 Update Goal: complete failed`（duration 283s）→ 教練**有收到** Telegram 推播（delivery.delivered=true），失敗的是 cron 內部 metadata 寫入，cron 系統誤判失敗
- 8/3 23:16 OK（commit 84a069f20 已 push）→ 8/4 失敗 → 8/5 失敗 = alternating 中斷，連 2 錯

**v4.0 三關判斷**：
- 關卡一（現在還壞？）：任務只在 23:05 跑，下次是今晚 23:05。現在 02:31，**沒過**（不屬於「正在壞」）。
- 關卡二（provider overload？）：錯誤是 tool-level（Message reply failed / Update Goal failed），不是 provider 端。**沒過**（不是 overload 但也不是設定錯）。
- 關卡三（影響工作？）：8/4 真影響（沒收到推播），8/5 偽失敗（有收到）。**過了**。

三關必須都過才 announce → 關卡一沒過 → **不 announce**，但升級警戒。

**自動修復**：無（不是設定問題、不是 timeout、不是 apiKey）。今晚 23:05 自動重試驗證。

**今晚升級觸發點**：今晚 23:05 跑完後若 CE ≥ 3 → 立即升級 announce「每日總結連 3 天未送達」，不再靜默。

**HEARTBEAT.md ⬜ 檢查**：
- 無 ⬜ 標記項目
- pendingCoachItems = 空
- 22:20 寄信提醒 Day 5/20 即將於今晚 22:20 觸發（at=2026-08-06T22:20+08:00）

**動作**：靜默處理，不發訊息給教練（cron delivery=none + failure_alert 未設 + v4.0 三關未全過）。

## 2026-07-25 05:33 CST

**檢查範圍**：cron list 總計 1 個任務（只有「健康檢查」本身，無其他任務需監控）。

**本次任務狀態**：
- consecutiveErrors：1（上次 5:31 失敗）
- lastStatus：error
- lastDurationMs：123,373ms（123 秒）
- lastErrorReason：timeout
- 診斷：`The model did not produce a response before the model idle timeout`

**分析**：
- 此錯誤是 **model provider 層級的 idle timeout**，不是 cron job timeoutSeconds（600 秒）太短
- 與教練指引的「1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）」自動修復規則**不吻合**
- 沒有對應的自動修復動作
- 連續錯誤 1 次 < 3 次門檻，不需通知教練

**動作**：靜默通過，等待下次（5:30 後）觀察是否再次發生。
若連續 3 次 model idle timeout，需升級裁決（model 換 provider 或調高 `models.providers.minimax.timeoutSeconds`）。

---

## 背景工作檢查（HEARTBEAT.md）

HEARTBEAT.md 目前內容僅為「重啟後第一件事」與「系統狀態」守則摘要，**沒有任何 ⬜ 待辦項目**，無背景工作需評估。
## 2026-07-25 06:02 CST (週六凌晨)

**檢查範圍**：cron list 總計 1 個任務（只有「健康檢查」本身，無其他任務需監控）。

**本次任務狀態**：
- consecutiveErrors：1（剛剛 06:00 fire 失敗 → 06:02 retry = 本場）
- lastStatus：error（剛 fire 失敗）
- lastDurationMs：87,258ms（87 秒）
- lastErrorReason：timeout（model idle timeout）
- 診斷：`The model did not produce a response before the model idle timeout`

**分析**：
- 此錯誤是 **model provider 層級的 idle timeout**，不是 cron job timeoutSeconds（600 秒）太短
- 與教練指引的「1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）」自動修復規則**不吻合**
- 沒有對應的自動修復動作
- 連續錯誤 1 次 < 3 次門檻，不需通知教練
- alternating fail/recover 模式 110h+ 穩定
- 錯誤本質：minimax provider 端臨時性問題，教練無法介入
- 週六凌晨 06:02，睡眠時段，無需打擾教練

**動作**：靜默通過，等待下次（06:30 後）觀察是否再次發生。
若連續 3 次 model idle timeout（06:30 fire 也失敗 + 06:32 retry 也失敗 = CE=3），需升級裁決通知教練。

---

## 背景工作檢查（HEARTBEAT.md）

HEARTBEAT.md 目前內容僅為「重啟後第一件事」與「系統狀態」守則摘要，**沒有任何 ⬜ 待辦項目**，無背景工作需評估。

## 2026-07-25 08:03 CST (週六早上)

**檢查範圍**：cron list 總計 1 個任務（只有「健康檢查」本身）。

**本次任務狀態**：
- consecutiveErrors：1（07:30 fire 失敗 → 本場 08:02 retry = ✅ OK，CE 將 reset 回 0）
- lastStatus：error（07:30 fire 失敗）
- lastDurationMs：65,229ms（65 秒）
- lastErrorReason：timeout（model idle timeout，provider 端）
- 診斷：`The model did not produce a response before the model idle timeout`

**分析**：
- 此錯誤是 **model provider 層級的 idle timeout**，不是 cron job timeoutSeconds（600 秒）太短
- 與教練指引的「1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）」自動修復規則**不吻合**（65s ≪ 600s）
- 與教練指引的「3. INVALID_API_KEY」自動修復規則**不適用**（model 已為 minimax/MiniMax-M3）
- alternating fail/recover 模式已穩定 **118 小時+**（幾乎 5 天），是 provider 端常態波動
- CE=1，距 3 次紅線 2 次
- 週六早上 08:03，教練可能在睡回籠覺或晨間，不主動打擾

**動作**：靜默通過，等待下次（08:30 fire）觀察是否再次發生。
若連續 3 次 model idle timeout，需升級裁決通知教練（建議：調高 `models.providers.minimax.timeoutSeconds` 或切換 provider）。

---

## 背景工作檢查（HEARTBEAT.md）

HEARTBEAT.md 內容：
- ⚠️ 2026-07-25 05:08 因 Context Overflow 自動重啟（main session 已通知教練）
- 系統狀態／守則摘要
- **無任何 ⬜ 待辦項目**，無背景工作需評估

---

## 2026-07-27 23:03 CST (週一晚間)

**檢查範圍**：cron list 總計 19 個啟用任務（透過 sqlite 查詢 openclaw.sqlite）。

**錯誤任務（3 個，consecutive_errors=1，皆為 23:00 跑的任務）**：

| Job ID | 名稱 | lastDurationMs | timeoutSeconds | 錯誤 |
|---|---|---|---|---|
| dc9bdf5c-0a3c-4b37-ad91-dc7ee02e7cc1 | 🔴 場景化升華+系統健檢（每日23:00） | 144,430ms | (無) | FailoverError: AI service overloaded |
| 533cfe54-5a89-45e3-88dc-6c81749e3c90 | 🔴 場景化升華（每日23:00，蒸餾→格式D場景+痛點計分） | 122,457ms | 1800 | FailoverError: AI service overloaded |
| 46e67e2e-6332-4589-aae2-ee7e10dd7279 | 🦞 每30分鐘任務健康檢查（本任務） | 107,225ms | 600 | FailoverError: AI service overloaded |

**分析**：
- 三個任務幾乎**同時**在 23:00 觸發，都碰到同一個錯誤「AI service is temporarily overloaded」
- 這是 **MiniMax provider 端瞬時過載**，不是 cron 設定問題（timeout 不會這樣爆）
- 與規則「1. timeout 錯誤」**不吻合**（durationMs 110~144s ≪ timeoutSeconds 600/1800）
- 與規則「3. INVALID_API_KEY」**不適用**（model 已是 minimax/MiniMax-M3）
- consecutiveErrors=1，**遠未達 3 次紅線**

**自動修復**：無（provider 端瞬時 overload，無法自動修復，只能等下次重試）。
- 場景化升華 2 個任務明天 23:00 會自然重試
- 健康檢查本身 30 分鐘後再 fire（若持續 overload 升級 3 次則通知教練）

**動作**：靜默通過，不通知教練（依規則：只有需要裁決才 announce）。

---

## 2026-08-01 16:32 CST (週六午後)

**檢查範圍**：cron_jobs 表 21 個啟用任務全覽（sqlite 直接查 openclaw.sqlite）。

**整體健康**：
- 19/21 啟用任務 last_status = ok
- 1/21 last_status = error（本任務本身，consecutive_errors=1）
- 0/21 達連續錯誤 ≥3 紅線
- 無 invalid_api_key、無 timeout、無 VPS scp 錯誤

**錯誤任務（1 個）**：

| Job | agent | consecutive | lastDurationMs | error |
|---|---|---|---|---|
| 🦞 每30分鐘任務健康檢查（本任務） | main | 1 | 113258ms（< 600s timeout） | FailoverError: AI service overloaded |

**分析**：
- 與 2026-07-27 23:03 事件**同型**：MiniMax provider 端瞬時 overload
- durationMs 113s ≪ timeoutSeconds 600s → **非 timeout 設定問題**
- model 已是 minimax/MiniMax-M3 → **非 auth 問題**
- consecutive_errors=1 → **遠未達 3 次紅線**

**自動修復**：無（provider 端瞬時事件，等下次重試自然恢復）。
- 16:00 跑是 ok，16:30 撞 overload，預期 17:00 自動恢復
- 若連續 3 次仍 overload 才升級通知教練

**HEARTBEAT.md 檢查**：
- 無 ⬜ 待辦項目
- pendingCoachItems 多為卡等教練給細節的任務，非自動化可解

**動作**：靜默通過，不通知教練（依規則：只有需要裁決才 announce）。

## 2026-08-01 18:34 CST (週六傍晚)

**檢查範圍**：cron_jobs 表 21 個啟用任務全覽（sqlite 直接查 openclaw.sqlite）。

**整體健康**：
- 19/21 啟用任務 last_status = ok
- 1/21 last_status = error（本任務本身，consecutive_errors=1）
- 0/21 達連續錯誤 ≥3 紅線
- 無 invalid_api_key、無 timeout、無 VPS scp 錯誤

**錯誤任務（1 個）**：

| Job | agent | consecutive | lastDurationMs | error |
|---|---|---|---|---|
| 🦞 每30分鐘任務健康檢查（本任務） | main | 1 | 146401ms（< 600s timeout） | FailoverError: The AI service is temporarily overloaded |

**分析**：
- 與 2026-07-27 23:03 / 2026-08-01 16:32 事件**完全同型**：MiniMax provider 端瞬時 overload
- durationMs 146s ≪ timeoutSeconds 600s → **非 timeout 設定問題**
- model 已是 minimax/MiniMax-M3 → **非 auth 問題**
- consecutive_errors=1 → **遠未達 3 次紅線**
- alternating fail/recover 模式穩定 5+ 天，純屬 provider 端波動

**自動修復**：無（provider 端瞬時事件，等下次重試自然恢復）。
- 18:00 fire 撞 overload，預期 18:30 retry 自動恢復（pattern 穩定）
- 若連續 3 次仍 overload 才升級通知教練

**HEARTBEAT.md 檢查**：
- 無 ⬜ 待辦項目
- pendingCoachItems 多為卡等教練給細節的任務，非自動化可解
- 教練 11:58 已上線，原 122h+ 靜默紀錄作廢

**動作**：靜默通過，不通知教練（依規則：只有需要裁決才 announce）。

## 2026-08-01 19:32 CST (週六傍晚)

**檢查範圍**：cron_jobs 表 21 個啟用任務全覽（sqlite 直接查 openclaw.sqlite）。

**整體健康**：
- 20/21 啟用任務 last_status = ok
- 1/21 last_status = error（本任務本身，consecutive_errors=1）
- 0/21 達連續錯誤 ≥3 紅線
- 無 invalid_api_key、無 timeout、無 VPS scp 錯誤

**錯誤任務（1 個）**：

| Job | agent | consecutive | lastDurationMs | error |
|---|---|---|---|---|
| 🦞 每30分鐘任務健康檢查（本任務） | main | 1 | 144,801ms（< 600s timeout） | FailoverError: The AI service is temporarily overloaded |

**分析**：
- 與 2026-07-27 23:03 / 2026-08-01 16:32 / 18:34 事件**完全同型**：MiniMax provider 端瞬時 overload
- durationMs 144s ≪ timeoutSeconds 600s → **非 timeout 設定問題**
- model 已是 minimax/MiniMax-M3 → **非 auth 問題**
- consecutive_errors=1 → **遠未達 3 次紅線**
- alternating fail/recover 模式穩定 5+ 天，純屬 provider 端波動

**自動修復**：無（provider 端瞬時事件，等下次重試自然恢復）。
- 19:00 fire 撞 overload，預期 19:30 retry 自動恢復（pattern 穩定）
- 若連續 3 次仍 overload 才升級通知教練

**HEARTBEAT.md 檢查**：
- 無 ⬜ 待辦項目
- pendingCoachItems 多為卡等教練給細節的任務，非自動化可解
- 教練 11:58 已上線（HEARTBEAT.md 已於 18:11 修正靜默紀錄）

**動作**：靜默通過，不通知教練（依規則：只有需要裁決才 announce）。
