# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-05-25 02:38
> 對話記錄已完整存入 memory/2026-05-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-05-25.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- Primary 模型：google/gemini-3.1-pro-preview
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成 Gemini 空白回應）

## 學長心跳 — 2026-05-25 03:32
- Cron：14項全部正常 ✅
- Git：auto-backup OK（025828b1）
- Relay：03:33 relay poll OK
- shared-relay/：CONSENSUS.md 已讀，無新任務
- shared-context/：無 SUPERGROUP-MAP.md（僅有 commit_notify.log）
- ✅ cron:768246fb 已修復（03:39）
  - 問題：consecutiveErrors=2，狀態 error
  - 原因：編輯 HEARTBEAT.md 時文字不匹配
  - 修復：手動重置 jobs.json 狀態欄位
  - 結果：狀態恢復為 ok
- 系統健康，無需緊急介入

## 學長 relay poll
### 2026-05-25 2026-05-25 05:02 - relay poll OK

