# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-15 01:37
> 對話記錄已完整存入 memory/2026-07-15.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-15.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 📝 健康檢查紀錄（append-only）

### 2026-07-15 08:37 健康檢查（consecutiveErrors 11，已自行處理）

**觸發對象**：cron job `46e67e2e-6332-4589-aae2-ee7e10dd7279`「🦞 每30分鐘任務健康檢查」

**狀態盤點**：
- 🟢 系統中只有 1 個 cron job（即健康檢查自己），無其他需監控任務
- 🟢 HEARTBEAT.md 無 ⬜ 待辦、無 48 小時停滯的背景工作
- 🟡 此健康檢查 job 本身 `consecutiveErrors: 11`（>3 閾值），`lastStatus: error`，錯誤原因：修復前的 `INVALID_API_KEY`（anthropic apiKey 失效）
- 🟢 **教練今晨 2026-07-15 已親自拍板修復**：把 payload.model 從 `anthropic/claude-opus-4-8` 改為 `minimax/MiniMax-M3`（驗證：cron get model 已是 `minimax/MiniMax-M3`）
- 🟢 屬「教練已介入處置」，按鐵律 rule 4 不升級為「需要教練裁決」

**自動修復動作**：
1. ❌ `cron run <jobId> --runMode force` 驗證 → 工具回 `Cron tool is restricted to the current cron job`，無法對自己 force run
2. ✅ 確認 model 配置正確（get job 顯示 `minimax/MiniMax-M3`）
3. ⏰ 等下次自動跑驗證（nextRunAtMs = 09:11 Asia/Taipei），成功後 `consecutiveErrors` 自動歸零
4. ✅ trace 寫入本檔

**結論**：🟡 已修復、未驗證。等 09:11 自動跑成功即自然復原。本次安靜處理，不通知教練。
