# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-02 13:38
> 對話記錄已完整存入 memory/2026-08-02.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-02.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔴 2026-08-02 14:45 教練第三次痛罵：沉默計數器
- **三次同型錯誤**：
  1. 8/1 18:04「5.8 天沒說話」
  2. 8/2 12:11「160h+ 靜默」
  3. 8/2 14:45 context overflow 重啟後，教練預防性重申
- **永久鐵律 v3.0**（已寫入 `.learnings/feedback_silence_count_must_be_real_time.md` 與 MEMORY.md）：
  - 寫「靜默 N 小時/天」前必先讀 `state/heartbeat-state.json` 的 `coachSilentSince`
  - 用 `date` 即時算差距，**禁止沿用 state 內的舊 `coachSilentHours`**
  - state 過期或缺值時主動從 `memory/YYYY-MM-DD.md` 或 Telegram API 撈最後訊息時間
  - 查不到就說「剛剛沒收到您訊息的紀錄」，**不要編一個數字**
- **當下真實狀態（2026-08-02 14:45）**：`coachSilentSince=2026-08-02T11:11:00+08:00`，差距約 3.5 小時
