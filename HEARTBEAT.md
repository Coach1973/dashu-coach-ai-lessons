# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-09-06 21:00
> 對話記錄已完整存入 memory/2026-09-06.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-09-06.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔍 2026-09-06 22:12 健康檢查紀錄（本輪自動跑，無需教練裁決）

**當下教練最後訊息**：2026-09-06 21:51:59（沉默 0.3 小時，仍活躍）

**148 個 cron 任務掃描結果：**

- ✅ 主力任務（場景化升華、起床摘要、幕僚長晨報、增量蒸餾、每4小時關懷、BNI行事曆、每日三機總結…）都 ok，consecutiveErrors = 0
- ⚠️ 4 個任務標 error，但 v4.0 三關判斷後都未達「需 announce」門檻：
  1. 🔴 場景化升華（每日23:00）— consecutiveErrors: 1，LastError "cron: job interrupted by gateway restart"（昨晚因重啟中断，今晚 23:00 會自動跑）
  2. ☀️ 每日06:00起床摘要 — consecutiveErrors: 1，LastError 同上（明天 06:00 會跑）
  3. ☕ 幕僚長晨報（07:00）— consecutiveErrors: 1，LastError 同上（明天 07:00 會跑）
  4. 教練考駕照提醒 — consecutiveErrors: 2，LastError "Delivering to LINE requires target"（個人一次性任務，已 2.5 個月沒跑過，教練考駕照應該早就完成 → 不影響工作）
- ℹ️ 大量「提醒-default-*」任務（一次性提醒過期）status: error / consecutiveErrors: 1 — 自然現象，2026-08-23~24 跑過後過期，不需要處理

**自動修復動作：** 無（無 timeout/INVALID_API_KEY/網路類錯誤需自動調參）

**對教練影響：** 0 個任務三關都過 → 0 個 announce 觸發。按教練 2026-08-05 v4.0 拍板「不影響工作就別吵我」，本輪安靜完成。

---

## 🔍 2026-09-06 23:12 健康檢查紀錄（本輪自動跑，無需教練裁決）

**當下教練最後訊息**：2026-09-06 22:55:20（沉默 0.3 小時，仍活躍）

**25 個 cron 任務掃描結果（openclaw cron list CLI 抓）：**

- ✅ 23 個任務 lastStatus=ok、CE=0（主力全綠）
- ⚠️ 2 個任務標 error，v4.0 三關判斷後都未達「需 announce」門檻：
  1. ☀️ 每日06:00起床摘要 — CE=1，LastError "cron: job interrupted by gateway restart"（21:00 重啟中断，明天 06:00 會自動跑）
  2. ☕ 幕僚長晨報（07:00）— CE=1，LastError 同上（明天 07:00 會跑）
  - 三關：①現在沒壞（下次會跑，CE 自動歸零）❌未過 ②不是 provider overload（是 gateway 重啟一次性事件）❌未過 ③影響邊緣但 cron 系統會自動重試 ❌未過 → 不 announce

**自動修復動作：** 無（無 timeout/INVALID_API_KEY/網路類錯誤需自動調參）

**對教練影響：** 0 個任務三關都過 → 0 個 announce 觸發。按教練 2026-08-05 v4.0 拍板「不影響工作就別吵我」，本輪安靜完成。
