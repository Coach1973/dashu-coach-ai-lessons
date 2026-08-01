# HEARTBEAT 熱上下文（每次心跳必讀）

> 最近重啟：2026-08-01 02:07（Context Overflow 自動重啟）
> 對話記錄已完整存入 memory/2026-08-01.md 並推上 GitHub，零遺漏

## ⚡ 系統狀態（2026-08-01 11:33 健康檢查更新）
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報
- 教練靜默 122h+（自 2026-07-26 19:51 起）
- 11:32 健康檢查：lastRunStatus=error，consecutiveErrors=1，lastErrorReason="overloaded"（MiniMax API 暫時過載），lastDurationMs=141s << timeoutSeconds=600s（非 timeout 錯誤），consecutiveErrors 未達 3 次門檻，無需自動修復亦無需通知教練，下個 30 分鐘週期會自動重試
- 09:00 早安輪已評估：Telegram 通道健康（探針 ok:true）、系統 19 排程全綠（30 分鐘健康檢查 09:00 1 次瞬斷後 09:02 retry 成功）、無 urgent 訊息
- 本輪送出週六早安（簡短不囉嗦，尊重教練週末休息推定）

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## ⚠️ peipei 自動 force-restart 2026-08-01 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
