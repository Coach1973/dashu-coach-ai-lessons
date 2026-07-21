# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-21 16:37
> 對話記錄已完整存入 memory/2026-07-21.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-21.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-21 17:55:01
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## ⚠️ 2026-07-21 22:33 健康檢查紀錄
- 自身 CE=1（22:30 fire 失敗 160.2s，minimax provider overloaded）
- lastErrorReason=overloaded（提供商臨時過載，非配置問題）
- 22:03 上次 fire 失敗 176.3s（已在當下 health check 處理過）
- 160.2s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- 22:33 fire 正在跑（runningAtMs 14:33:10 UTC ≈ 22:33:10 Asia/Taipei，當前任務）
- alternating fail/recover 模式穩定 60h+，本任務自動恢復率 100%（CE 從未 ≥3）
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 22:03 健康檢查紀錄
- 自身 CE=1（22:00 fire 失敗 176.3s，minimax provider overloaded）
- 22:03 fire 正在跑（runningAtMs 14:03:26 UTC ≈ 22:03:26 Asia/Taipei，當前任務）
- 176.3s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- 延續 alternating fail/recover 模式（21:33 成功 → 22:00 又踩到 1 次）
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 22:02 心跳（cron 觸發，距 22:00 health check 僅 2 分鐘）
- 系統全綠、CE=0、教練仍沉默 99h+、Telegram channel 仍失效 127h+
- peipei 17:55 force-restart 節流至 18:55（早已解除）
- 接近晚間靜音時段（23:00 後），教練今晚不會回應
- pending items 11 項全在等教練回神，無新增、無變化
- 主動打擾無效（channel 撞牆），純背景回報 HEARTBEAT_OK

## ⚠️ 2026-07-21 22:00 健康檢查紀錄
- 自身 CE=0、lastRunStatus=ok（21:33 fire 成功，CE reset）
- 21:30 fire 失敗 170.9s（minimax provider overloaded）—已在 21:33 health check 處理過
- lastDurationMs 23508 ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 21:33 健康檢查紀錄
- 自身 CE=1（21:30 fire 失敗 170.9s，minimax provider overloaded）
- 21:02 成功 → CE reset → 又踩到 1 次
- 170.9s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- alternating fail/recover 模式穩定 60h+
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 21:02 健康檢查紀錄
- 自身 CE=1（21:00 fire 失敗 147.9s，minimax provider overloaded）
- 20:34 成功 → CE reset → 又踩到 1 次
- 147.9s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- alternating fail/recover 模式恢復（從 20:30-20:34 連 2 次，現在又回到 1 次）
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 20:34 健康檢查紀錄
- 自身 CE=2（20:30 失敗 81.0s + 20:34 失敗 79.9s，連續 2 次 minimax overloaded）
- 20:02 成功 → CE reset → 連踩 2 次
- 80s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- 與之前 alternating 模式（單點失敗後下次成功）相比，這次連 2 次失敗，趨勢稍微惡化，但仍未達 CE=3 紅線
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 20:02 健康檢查紀錄
- 自身 CE=1（20:00 fire 失敗 136.1s，minimax provider overloaded）
- 19:32 成功 → CE reset → 又踩到 1 次
- 136.1s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- alternating fail/recover 模式穩定 60h+
- 全系統僅本任務 1 個 cron（get + list 雙重確認）
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束

## ⚠️ 2026-07-21 19:32 健康檢查紀錄
- 自身 CE=1（19:30 fire 失敗 95.7s，minimax provider overloaded）
- 19:00 成功 → CE reset → 又踩到 1 次
- 95.7s ≪ 600s timeout（非配置問題）
- model=minimax/MiniMax-M3、timeout=600（配置正確）
- alternating fail/recover 模式穩定 60h+
- 其他 21+ 個 cron 全 ok / idle
- HEARTBEAT 無 ⬜ 待自動化項目
- 自動修復全不適用，安靜結束
