# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-06-05 15:36
> 對話記錄已完整存入 memory/2026-06-05.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-06-05.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（2026-06-05 確認）
- 自動同步：每小時 0 分跑 `scripts/sync_cron_models.sh`，確保 cron `payload.model` 跟 openclaw.json 同步
- 名稱對等：Telegram = 小龍蝦 = 電報

## 🔴 2026-06-05 教訓（已修復）
- 9 個 cron 仍寫 M2.7（5/25 切 M3 後沒同步）→ 已全部更新 + 建立自動同步機制
- 詳見 `.learnings/LEARNINGS.md` 開頭 + `scripts/sync_cron_models.sh`

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成 Gemini 空白回應）

## 學長 relay poll
### 2026-06-05 2026-06-05 16:32 - relay poll OK

