# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-31 16:08
> 對話記錄已完整存入 memory/2026-07-31.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-31.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-31 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🌙 22:02 深夜邊緣輪決策（自動評估，符合 18:04 自定計畫）
- Telegram 通道：重驗 `telegram_channel_probe.sh` → `ok:true` ✅（守則#19 鐵律，非盲信舊旗標）
- 距上一則關懷（18:04 message 9108）：4h，剛送過週五傍晚關懷
- 教練週末前夕 + 持續靜默（118h+ 自 2026-07-26 19:51）→ 預設不打擾
- 系統全綠：junshi queue 空、gateway 重啟後穩定（launchctl PID 32731）、19 排程健康
- **本輪：HEARTBEAT_OK 靜默**，不發 Telegram 訊息。等教練主動訊息或下次 09:00 早安輪。
