# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-04 17:37
> 對話記錄已完整存入 memory/2026-08-04.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-04.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-04 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 📋 健康檢查記錄（cron 自動·安靜）
- 2026-08-05 08:04 健康檢查：cron list 全系統 1 個任務（本任務本身），本輪 lastError=overloaded，consec=1（alternating transient 1300+ 場穩定，< 3 紅線）；本場 08:04 成功執行；model minimax/MiniMax-M3 ✅ / timeout 600s ✅ / delivery.mode=none ✅
  - 教練沉默 42.2 小時（真相源 2026-08-03 13:54，sync_coach_last_message.sh exit 0）
  - 4 條自動修復規則全部不適用（timeout 充裕、無 VPS、model 正確、CE 未達紅線）
  - HEARTBEAT 內無 ⬜ 待辦
  - 結論：✅ 無異常，不 announce（凌晨不打擾、alternating 模式穩定、CE 未達紅線）
- 2026-08-05 06:02 健康檢查：cron list 全任務 38 個，2 個 error（都是 transient，consec=1，< 3 門檻）
  - ⚠️ [🦞 健康檢查 30m] consec=1（lastError=overloaded，本輪已正常啟動執行；上次失敗 4m 前）
  - ⚠️ [☀️ 每日 06:00 起床摘要] consec=1（lastError=overloaded，transient AI 服務暫時過載，等明天 06:00 再驗證）
  - ⚠️ [🦞 每日三機總結 23:05] consec=1（lastError=Telegram reply failed，transient，等今晚 23:05 再驗證）
  - 三個 enabled 錯誤都 < 3 連續門檻，按 SOP 不打擾教練，安靜觀察
  - 教練沉默 40.1 小時（真相源 2026-08-03 13:54，sync_coach_last_message.sh exit 0）
  - HEARTBEAT 內無 ⬜ 待辦
  - 結論：✅ 無異常，不 announce
- 2026-08-05 05:33 健康檢查：cron list 抓到本機 + VPS 全任務（總計 ~38 jobs）
  - ⚠️ [🦞 健康檢查 30m] consec=1（lastError=overloaded，本輪（05:33）已正常啟動執行，視為自癒；上次失敗 4m 前）
  - ⚠️ [🦞 每日三機總結 23:05] consec=1（lastError=Telegram reply 1 failed，transient，等今晚 23:05 再驗證；上次失敗 6h 前）
  - 其餘任務 ok / idle / running，皆正常
  - 兩個 enabled 錯誤都 < 3 連續門檻，按 SOP 不打擾教練，安靜觀察
  - 教練沉默 39.7 小時（真相源 2026-08-03 13:54，sync_coach_last_message.sh exit 0）
  - HEARTBEAT 內無 ⬜ 待辦
  - 結論：✅ 無異常，不 announce
- 2026-08-05 05:02 健康檢查：51 任務全覽（37 enabled / 14 disabled），ok=28 / error=4 / unknown(未到時間)=19
  - ⚠️ [🦞 健康檢查 30m] consec=1（lastError=overloaded，transient，等下輪 05:32 再驗證）
  - ⚠️ [🦞 每日三機總結 23:05] consec=1（lastError=Telegram reply 失敗，transient，等今晚 23:05 再驗證）
  - 🔕 [BNI提醒] consec=1 但 enabled=False，不處理
  - 🔕 [教練考駕照提醒] consec=2 但 enabled=False，不處理
  - 兩個 enabled 錯誤都 < 3 連續門檻，按 SOP 不打擾教練，安靜觀察
  - 教練沉默 39.1 小時（真相源 2026-08-03 13:54，sync_coach_last_message.sh exit 0）
  - HEARTBEAT 內無 ⬜ 待辦
- 2026-08-05 03:33 健康檢查：37 任務全啟用，ok=16 / running=1 / error=2 / idle(未到時間)=19
  - ⚠️ [🦞 每日三機總結 23:05] consec=1（lastError=Telegram reply 失敗，transient，等今晚 23:05 再驗證）
  - ⚠️ [🦞 健康檢查 30m] consec=1（lastError=overloaded，transient，本輪已自動恢復）
  - 兩個錯誤都 < 3 連續門檻，按 SOP 不打擾教練，安靜觀察
  - HEARTBEAT 內無 ⬜ 待辦

## ⚠️ peipei 自動 force-restart 2026-08-05 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🩺 軍師 Hook 自檢 2026-08-05 09:35（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: f10367e1-f282-433e-8725-54024fa4681b
