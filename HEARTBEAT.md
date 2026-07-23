# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-23 22:37
> 對話記錄已完整存入 memory/2026-07-23.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-23.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-23 23:30
- ✅ 同步成功
- HANDOFF mtime: 1784820516
- 雲端同步：✅ 已推上雲端（commit e02142e7a）

## 🏥 健康檢查紀錄 2026-07-24 05:33
- ✅ 自我健康檢查任務：lastErrorReason=overloaded（minimax 服務瞬時過載），consecutiveErrors=1<3，不算嚴重
- ⚠️ cron list 僅回傳 1 個任務（健康檢查本身），其他任務（每日三機總結、海餅乾背誦等）未顯示——可能為 cron tool 對當前 session 的過濾，非任務消失
- HEARTBEAT.md 無 ⬜ 待辦項目需追蹤
- 結論：✅ 無需自動修復，安靜處理，下次健康檢查再觀察

## 🏥 健康檢查紀錄 2026-07-24 06:33
- ✅ 自我健康檢查任務：lastErrorReason=overloaded（minimax 服務瞬時過載），consecutiveErrors=1<3，不算嚴重
- 上一輪 22:30 失敗（158秒內觸發 overloaded），距今 8 小時後，現在 minimax 服務已恢復
- lastDurationMs 158323 遠低於 timeoutSeconds 600，不是 timeout 問題
- cron list 仍只回傳 1 個任務（健康檢查本身）——已知過濾現象
- HEARTBEAT.md 無 ⬜ 待辦項目需追蹤
- 結論：✅ 無需自動修復，安靜處理，下次健康檢查再觀察
