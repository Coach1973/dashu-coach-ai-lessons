# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-13 05:37
> 對話記錄已完整存入 memory/2026-07-13.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-13.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-13 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## ⚠️ Telegram channel 異常 2026-07-13 14:02
- 現象：message 工具回報「Telegram bot token missing」
- 檢查：env 無 TELEGRAM_BOT_TOKEN、openclaw.json telegram 區段 enabled=true 但無 token
- 影響：無法主動推訊給教練（Netlify 50% + 光線尺 ATM 1 萬元兩件事未推送）
- 修復：教練下次回應時請他補 token 或重啟 gateway；目前只在 OpenClaw 回合回報

## 📋 14:00 心跳待辦（等教練回應時一次告知）
1. Netlify 50% 用量 — 建議登入查看
2. 光線尺顧問 ATM NT$10,000 入金（13:25）— 請對帳
3. Telegram channel 異常（bot token 失效）— 需處理

## ⚠️ peipei 自動 force-restart 2026-07-13 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
