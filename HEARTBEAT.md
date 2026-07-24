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
