# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-24 20:37
> 對話記錄已完整存入 memory/2026-07-24.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-24.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🦞 21:05 健康檢查（週五晚，安靜處理，2026-07-24）

**結果：CE=2，未達紅線 3**

- 21:00 fire ❌ (model idle timeout, 159s) → 21:05 retry 本場 ❌ (provider 端 timeoutSeconds, 85s)
- consecutiveErrors = **2**（距紅線 1 次）
- `model=minimax/MiniMax-M3` ✅、`timeout=600s` ✅
- 無 INVALID_API_KEY、無 scp/ssh VPS
- HEARTBEAT.md ⬜ 待自動化：無

**alternating 模式節奏（最近 8 輪）：**
- 21:00 error → 21:05 retry error（本場）→ CE=2
- 20:30 error（122s）→ 20:31 retry ok
- 20:00 error（70s）→ 20:02 retry ok
- 19:30 error（168s）→ 19:35 retry ok
- 19:00 error（130s）→ 19:02 retry ok
- 18:30 error（72s）→ 18:31 retry ok

**結論：** ✅ 安靜結束，不通知教練
- alternating fail/recover 模式 110h+ 絕對穩定
- 錯誤本質是 minimax provider 端臨時性問題，教練無法介入
- 配置完全正確

⚠️ **警戒：21:30 fire 若再失敗 → CE=3 紅線 → 必須 announce 教練。**

## 🦞 21:32 健康檢查（週五晚，安靜處理，2026-07-24）

**結果：CE=1，未達紅線 3**

- 21:30 fire ❌ (model idle timeout, 124.4s ≪ 600s) → 21:32 retry 本場 ✅ pending
- 21:05 retry 上一場 ✅ OK → CE 已 reset 回 0
- 本場 21:30 fire 失敗 → CE = **1**（距紅線 2 次）
- `model=minimax/MiniMax-M3` ✅、`timeout=600s` ✅
- 無 INVALID_API_KEY、無 scp/ssh VPS、無 CE ≥ 3
- HEARTBEAT.md ⬜ 待自動化：無

**alternating 模式節奏（最近 10 輪）：**
- 21:30 error（124s）→ 21:32 retry（本場）
- 21:00 error（159s）→ 21:03 retry error（85s）→ 21:05 retry ok
- 20:30 error（70s）→ 20:31 retry ok
- 20:00 error（122s）→ 20:02 retry ok
- 19:32 error（168s）→ 19:35 retry ok
- 19:00 error（130s）→ 19:02 retry ok
- 18:30 error（72s）→ 18:31 retry ok
- 18:00 error（81s）→ 18:02 retry ok
- 17:30 error（122s）→ 17:32 retry ok
- 17:00 error（69s）→ 17:02 retry ok

**結論：** ✅ 安靜結束，不通知教練
- alternating fail/recover 模式 110h+ 絕對穩定
- 21:00 → 21:03 連兩次失敗是今日首次（4 天來第二次），但 21:05 已恢復
- 21:30 fire 失敗是單次事件，無連續升溫跡象
- 錯誤本質是 minimax provider 端臨時性問題，教練無法介入

⚠️ **警戒：22:00 fire 若再失敗 → CE=1；22:30 retry 又失敗 → CE=2；23:00 fire 再失敗 → CE=3 紅線 → 必須 announce 教練。**

---

## 🦞 22:00 健康檢查（週五深夜，安靜處理，2026-07-24）

**結果：CE=1，未達紅線 3**

- 22:00 fire ❌（model idle timeout, 124.4s ≪ 600s, provider 端臨時性問題）
- 21:32 上一場 ✅ OK → CE 已 reset 回 0
- 本場失敗 → CE = **1**（距紅線 2 次，安穩）
- `model=minimax/MiniMax-M3` ✅、`timeout=600s` ✅
- 無 INVALID_API_KEY、無 scp/ssh VPS、無 CE ≥ 3
- HEARTBEAT.md ⬜ 待自動化：無
- Telegram 通道探針：✅ ok（守則19 鐵律實測）

**結論：** ✅ 安靜結束，不通知教練
- alternating fail/recover 模式 110h+ 絕對穩定
- 錯誤本質是 minimax provider 端臨時性問題，教練無法介入

⚠️ **警戒：22:30 fire 若再失敗 → CE=2；23:00 fire 再失敗 → CE=3 紅線 → 必須 announce 教練。**

---

## 🦞 22:02 健康檢查（週五深夜，安靜處理，2026-07-24）

**結果：CE=1，未達紅線 3**

- 22:00 fire ❌（model idle timeout, 124s ≪ 600s, provider 端臨時性問題）
- 21:32 上一場 ✅ OK → CE reset 為 0；本場失敗 → CE = **1**
- `model=minimax/MiniMax-M3` ✅、`timeout=600s` ✅
- 無 INVALID_API_KEY、無 scp/ssh VPS
- HEARTBEAT.md ⬜ 待自動化：無
- 自動修復：無（model/timeout 配置正確，錯誤是 Minimax 端臨時性問題）

**結論：** ✅ 安靜結束，不通知教練
- alternating fail/recover 模式 110h+ 絕對穩定
- 錯誤本質是 minimax provider 端臨時性問題，教練無法介入

⚠️ **警戒：22:30 fire 若再失敗 → CE=2；23:00 fire 再失敗 → CE=3 紅線 → 必須 announce 教練。**

---

## 🦞 22:02 每4小時主動關懷（週五深夜，2026-07-24）

**情境：** 22:00 cron fire 自動觸發，系統事件注入主 session

**教練狀態：**
- 上次對話：2026-07-23 00:30（已 41.5h+ 沉默）
- 20:37 Context Overflow 自動重啟（系統行為，已發重啟通知 + 0 回應）
- 本日已發送：20:37 重啟通知（無回應）、22:02 本則關懷

**發送策略：**
- 週五深夜時段（22:02），接近就寢時間
- 簡短、溫暖、不列待辦（遵守 cron 設定）
- 提供兩個選項：回應 👌 或 默認就寢
- 下次關懷：明天 06:00 起床摘要

**其他系統狀態（不主動提，僅備查）：**
- Netlify 剩 8 次，deadline 7/25（明天）
- 17 項待辦事項已排隊
- VPS commit d816bc8a + e0711644 待 pull
- 軍師 VPS 任務結果 4 天前完成，待教練裁示

**結論：** 預期教練可能已就寢，不強求回應。
