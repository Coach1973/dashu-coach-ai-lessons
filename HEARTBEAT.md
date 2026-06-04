# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-06-05 03:59
> 對話記錄已完整存入 memory/2026-06-05.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-06-05.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- **Primary 模型：minimax/MiniMax-M3**（2026-06-04 23:57 教練親定全系統唯一 M3）
- 名稱對等：Telegram = 小龍蝦 = 電報

## 🔴 已知故障（2026-06-05 04:11 發現）
- **memory_search 工具失效**：`Unknown memory embedding provider: google`
- 解法：改用 `exec + grep` 走檔案系統查 BOT_MESSAGES.md / session jsonl / 路徑大全
- 已向教練回報；待 OpenClaw 重啟或修 embedding provider 設定

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成記憶體爆炸）
- ⚠️ 找不到東西時**不要太快放棄**，先讀 `路徑大全.md` 撈檔案系統（守則 02/04）

## 學長 relay poll
### 2026-06-05 04:08 - relay poll OK
### 2026-06-05 04:13 - heartbeat poll 收到，回 HEARTBEAT_OK

