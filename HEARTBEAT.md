# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-25 08:38
> 對話記錄已完整存入 memory/2026-08-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-25.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-25 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🩺 健康檢查紀錄（2026-08-25 10:13 自動跑完）
- 教練最後訊息：2026-08-25 01:51:55，沉默 8.4 小時（凌晨睡眠，正常不打擾）
- **所有 24 個 enabled cron 任務：consecutive_errors=0 ✅ 全員健康**
- 過去 24 小時有 5 個任務曾因 minimax `FailoverError: The AI service is temporarily overloaded` 失敗：
  - 每2小時增量記憶蒸餾（02:00 / 04:00 / 10:00）
  - 起床摘要 06:00、幕僚長晨報 07:00、LINE 回報 08:00
  - 場景化升華+系統健檢 23:00（昨日）
- **已全部自行恢復**（目前 consecutive_errors=0），不影響當前工作
- v4.0 三關判斷：關卡一不通過（現在沒壞）、關卡二通過（provider 暫時過載）→ 安靜處理，不 announce
- 24h 內唯一非過載錯誤：🦞 健康檢查本身 8/24 15:12 被 gateway 重啟打斷 43s → 已恢復
- 結論：✅ 無異常，本輪不打擾教練

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-25 12:10
- ✅ 同步成功
- HANDOFF mtime: 1787630780
- 雲端同步：✅ 已推上雲端（commit d97830ce9）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-25 13:05
- ✅ 同步成功
- HANDOFF mtime: 1787634266
- 雲端同步：✅ 已推上雲端（commit 8cafb6765）

## 🩺 軍師 Hook 自檢 2026-08-25 13:06（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- 小龍蝦信箱：（信箱查無新信）
- Session: 84150fda-42bc-4356-acc0-ad3d3b4a8c7a
