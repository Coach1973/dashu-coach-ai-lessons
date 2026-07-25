# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-25 05:08
> 對話記錄已完整存入 memory/2026-07-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-25.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-25 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 📊 2026-07-25 09:30 健康檢查偶發 timeout（CE=1）
- 上一場 09:30 跑 65s 後 LLM idle timeout 失敗（payload timeoutSeconds=600、provider 層無設定）
- 本場 10:01 正常完成（< 30s），視為偶發、不通知教練
- 若連續 3 次失敗需升級裁示

## 📊 2026-07-25 13:00 健康檢查偶發 timeout（CE=2）
- 上一場 13:00 跑 80s 後 LLM idle timeout 失敗（同 09:30 模式，payload timeoutSeconds=600 沒用，是 minimax provider 層問題）
- 本場 13:04 正常完成（視為偶發）
- CE=2 仍在觀察期，未達 3 次升級閾值
- 若 13:30 再失敗一次 → CE=3 需升級通知教練
