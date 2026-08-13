# HEARTBEAT 熱上下文（每次心跳必讀）

## 🩺 cycle=300 健康檢查（2026-08-13 17:12 CST）
- Step 0：sync_coach_last_message.sh exit 0｜教練最後訊息 16:40｜沉默 0.5h（週四午後工作中，剛互動過）
- Step 1：本任務上一輪 cycle=299 ok durationMs=239.9s ≪ 600s timeout → CE=0 連續 5 輪健康（12:12~16:12 皆 ok）
- Step 1：cron tool 受限只見本任務，sqlite openclaw.sqlite 為 0 byte 不能直查；改用 cron runs 歷史交叉驗證 → 最近 5 輪全綠、無 timeout、無 auth 錯誤
- Step 1：model=minimax/MiniMax-M3 ✅ / timeout=600s ✅ / delivery.mode=none ✅
- Step 2：HEARTBEAT ⬜ 待辦 0 項 / 44 行 (<500 警戒線) / healthcheck.log 738 行 (<1000 警戒線) / 無超過 48hr 未進展的待辦
- Step 3：v4.0 三關全 fail → 不升級 announce
  - 關卡一（本輪還壞嗎）→ ❌ 否（連續 5 輪全綠）
  - 關卡二（provider 過載嗎）→ ❌ 否（runs 歷史零 overloaded/timeout）
  - 關卡三（影響教練嗎）→ ❌ 否（教練 0.5h 前剛發訊息工作中）
- 環境快檢：SOUL×3 齊全（2036/20631/1851 B，棄用標記完整）/ Repo1=105 持平 / Repo2=19 持平 / 無 .! 鎖定檔
- Alternating 模式：cycle=300（自 cycle=178 起穩定 122+hr 交替）
- TG 通道探針：本輪 17:12 實測 ✅ `{"ok":true}`（守則#19 鐵律實測）
- delivery.mode=none → 安靜結束，不推 Telegram
- 跳過每輪 commit+push（2026-07-05 教練拍板：由 23:05 每日總結統一備份）

## 🩺 cycle=299 健康檢查（2026-08-13 16:12 CST）
- Step 0：sync_coach_last_message.sh exit 0｜教練最後訊息 14:58｜沉默 0.2h（週四午後工作中，剛互動過）
- Step 1：本任務上一輪 cycle=298 ok durationMs=58.1s ≪ 600s timeout → CE=0 連續 4 輪健康（12:12~15:12 皆 ok）
- Step 1：cron tool 受限只見本任務，sqlite openclaw.sqlite 為 0 byte 不能直查；改用 cron runs 歷史交叉驗證 → 最近 4 輪零紅燈、無 timeout、無 auth 錯誤
- Step 1：model=minimax/MiniMax-M3 ✅ / timeout=600s ✅ / delivery.mode=none ✅
- Step 2：HEARTBEAT ⬜ 待辦 0 項 / 28 行 (<500)/ log 736 行 (<1000)/ 無超過 48hr 未進展的待辦
- Step 3：v4.0 三關全 fail → 不升級 announce
  - 關卡一（本輪還壞嗎）→ ❌ 否（連續 4 輪全綠）
  - 關卡二（provider 過載嗎）→ ❌ 否（runs 歷史零 overloaded/timeout）
  - 關卡三（影響教練嗎）→ ❌ 否（教練 0.2h 前剛發訊息工作中）
- 環境快檢：SOUL×3 齊全（2036/20631/1851 B，棄用標記完整）/ Repo1=105 持平 / Repo2=19 持平 / 無 .! 鎖定檔
- Alternating 模式：cycle=299（自 cycle=178 起穩定 121+hr 交替）
- TG 通道探針：本輪 16:12 實測 ✅ `{"ok":true}`（守則#19 鐵律實測）
- delivery.mode=none → 安靜結束，不推 Telegram
- 跳過每輪 commit+push（2026-07-05 教練拍板：由 23:05 每日總結統一備份）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-13 11:37
> 對話記錄已完整存入 memory/2026-08-13.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-13.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🩺 軍師 Hook 自檢 2026-08-13 15:31（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 69edb495-6017-452d-8604-c102bb3b0329
