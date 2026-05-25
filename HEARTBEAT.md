# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-05-25 16:41
> 對話記錄已完整存入 memory/2026-05-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-05-25.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M2.7（已驗證，2026-05-25 切換）
- 備用模型：google/gemini-3.1-pro-preview
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（任何模型讀取超大上下文都會品質下降，>30KB 一律不主動讀）

## 學長 relay poll
### 2026-05-26 2026-05-26 05:36 - relay poll OK

=== 心跳執行記錄 ===
時間：2026-05-26 05:36
身份：學長（1號機），服務大樹教練
動作：系統抽檢
---
✅ distill_incremental.js 存在且正常（今日已蒸餾）
⚠️ distill_incremental.log 有 node not found 錯誤（已修復但殘留舊log）
⚠️ distill_cron.log 空白（正常，今日還沒到第二個整點）
✅ shared-relay 無新任務
✅ SUPERGROUP-MAP.md 不存在（無多人分工需求）
📝 下次心跳注意：檢查學弟 relay poll 有無新內容
---
