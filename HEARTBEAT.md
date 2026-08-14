# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-14 17:38
> 對話記錄已完整存入 memory/2026-08-14.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-14.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-14 17:55:01
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🦞 健康檢查紀錄 2026-08-14 20:12（v4.0 規則）
- 22 個 cron 全 `lastRunStatus: ok`
- 今日曾出現 5 次 `FailoverError: overloaded`（蒸餾 9c3fc55d、起床摘要 f487652d、晨報 b73845c9、LINE 001a9b16、場景化升華 dc9bdf5c），皆自動 retry 成功
- v4.0 三關判斷：關卡一（現在仍壞）fail、關卡二（provider 暫時過載）fail、關卡三（影響工作）fail
- → 三關皆 fail，安靜結束，未 announce 教練
- 教練最後訊息 19:57:19（沉默 0.2h，工作中合理）
