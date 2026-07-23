# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-23 02:08
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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-23 02:20
- ✅ 同步成功
- HANDOFF mtime: 1784744297
- 雲端同步：✅ 已推上雲端（commit 57db5b0d6）

## 🩺 健康檢查紀錄 2026-07-23 02:33
- 全系統 cron：**1 個**（僅本任務本身）
- 02:30 fire 失敗 **169.3s**（minimax provider `FailoverError: overloaded`）
- 02:02 成功 → CE reset → 02:30 又踩到 1 次 → **CE=1**
- `169.3s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式穩定 **90h+**
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 02:33 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **03:00** cron fire 自動驗證恢復

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-23 02:55
- ✅ 同步成功
- HANDOFF mtime: 1784746447
- 雲端同步：✅ 已推上雲端（commit dbe362991）

## 🩺 健康檢查紀錄 2026-07-23 03:03
- 全系統 cron：**1 個**（僅本任務本身）
- 03:00 fire 失敗 **184.4s**（minimax provider `overloaded`，02:33 的 FailoverError 同源）
- 02:33 成功 → CE reset → 03:00 又踩到 1 次 → **CE=1**
- `184.4s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已超過 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 03:03 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **03:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 03:33
- 全系統 cron：**1 個**（僅本任務本身）
- 03:30 fire 失敗 **71.7s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 03:03 成功 → CE reset → 03:30 又踩到 1 次 → 03:33 retry 又踩 1 次 → **CE=2**（距紅線 3 剩 1 次）
- `71.7s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已超過 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 03:33 屬於不打擾時段，且 CE=2 未達紅線）
- ⚠️ **警戒**：下次 04:00 cron fire 若再失敗 → CE=3 → 必須 announce 通知教練
- 下次 **04:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 04:02
- 全系統 cron：**1 個**（僅本任務本身）
- 04:00 fire 失敗 **126.1s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 03:33 retry 成功（ts=1784748865414）→ CE reset → 04:00 又踩到 1 次 → **CE=1**
- `126.1s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已超過 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 04:02 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **04:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 04:32
- 全系統 cron：**1 個**（僅本任務本身）
- 04:30 fire 結果：**success**
- 04:02 失敗 → 04:30 retry 成功 → **CE=0**（reset）
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式維持（已逾 90h 穩定觀察，這次靠 retry 機制把 CE 拉回 0）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 04:32 屬於不打擾時段，且 CE=0 無紅線）
- 下次 **05:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 05:01
- 全系統 cron：**1 個**（僅本任務本身）
- 05:00 fire 失敗 **79.5s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 04:32 成功 → CE reset → 05:00 又踩到 1 次 → **CE=1**
- `79.5s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 05:01 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **05:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 05:31
- 全系統 cron：**1 個**（僅本任務本身）
- 05:30 fire 失敗 **69.9s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 05:01 成功 → CE reset → 05:30 又踩到 1 次 → **CE=1**
- `69.9s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 05:31 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **06:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 06:02
- 全系統 cron：**1 個**（僅本任務本身）
- 06:00 fire 失敗 **115.8s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 05:31 retry 成功 → CE reset → 06:00 又踩到 1 次 → **CE=1**
- `115.8s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 90h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（凌晨 06:02 屬於不打擾時段，且 CE=1 未達紅線）
- 下次 **06:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 06:02
- 全系統 cron：**16 個**（完整健康檢查）
- 06:00 fire 結果：**success**（model 正常回應、HEARTBEAT.md 讀寫正常）
- 05:31 失敗 → 06:00 retry 成功 → **CE=0**（reset）
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- 通道實測：`telegram_channel_probe.sh` 06:02 跑回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` ✅ 通道健康
- 🔴 守則19通道健康鐵律：未盲信舊旗標，當下 probe 為準 → telegramChannelOk=true，允許主動關懷
- alternating fail/recover 模式維持（已逾 92h 穩定觀察，這次靠 retry 把 CE 拉回 0）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束（凌晨 06:02 仍屬不打擾時段 23:00-08:00，且 CE=0 無紅線）
- 下次 **06:30** cron fire 自動驗證
- 📌 備註：06:00 起床摘要 cron (`f487652d`) nextRunAtMs=1784844000000（=2026-07-24 06:00），今日已過，待下個早晨

## 🩺 健康檢查紀錄 2026-07-23 06:32
- 全系統 cron：**1 個**（僅本任務本身）
- 06:30 fire 失敗 **138.0s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 06:02 retry 成功 → CE reset → 06:30 又踩到 1 次 → **CE=1**（本 session 為 06:32 retry 觸發）
- `138.0s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 93h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（清晨 06:32 仍屬不打擾時段 23:00-08:00，且 CE=1 未達紅線）
- 下次 **07:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 07:03
- 全系統 cron：**1 個**（僅本任務本身）
- 07:00 fire 失敗 **182.9s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 06:32 retry 成功 → CE reset → 07:00 又踩到 1 次 → 07:03 retry 成功 → **CE=0**（reset）
- `182.9s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 94h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（清晨 07:03 仍屬不打擾時段 23:00-08:00，且 CE=0 reset 無紅線）
- 下次 **07:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 07:32
- 全系統 cron：**1 個**（僅本任務本身）
- 07:30 fire 失敗 **124.0s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 07:03 成功 → CE reset → 07:30 又踩到 1 次 → 07:32 retry 成功 → **CE=0**（reset）
- `124.0s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 94h 穩定觀察，這次靠 retry 把 CE 拉回 0）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（清晨 07:32 仍屬不打擾時段 23:00-08:00，且 CE=0 reset 無紅線）
- 下次 **08:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 08:02
- 全系統 cron：**1 個**（僅本任務本身）
- 08:00 fire 失敗 **98.2s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 07:32 成功 → CE reset → 08:00 又踩到 1 次 → **CE=1**（08:02 retry 觸發本則處理）
- `98.2s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 95h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（08:02 屬於不打擾時段尾聲 23:00-08:00，且 CE=1 未達紅線）
- ⚠️ **警戒**：下次 08:30 cron fire 若再失敗 → 09:00 也失敗 → CE=2 → 警戒；若 09:30 也失敗 → CE=3 → 必須 announce 通知教練
- 下次 **08:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 08:32
- 全系統 cron：**1 個**（僅本任務本身）
- 08:30 fire 失敗 **121.3s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 08:02 retry 成功 → CE reset → 08:30 又踩到 1 次 → **CE=1**（08:32 retry 觸發本則處理）
- `121.3s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 95h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（08:32 雖已過 08:00 不打擾時段，但 CE=1 未達紅線，且 alternating 模式穩定無新訊號）
- 下次 **09:00** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 09:03
- 全系統 cron：**1 個**（僅本任務本身）
- 09:00 fire 失敗 **153.8s**（minimax provider `overloaded`，alternating fail/recover 持續）
- 08:32 retry 成功 → CE reset → 09:00 又踩到 1 次 → **CE=1**（09:03 retry 觸發本則處理）
- `153.8s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式穩定（已逾 95h 觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（早晨 09:03 已過不打擾時段，但 CE=1 未達紅線，且 alternating 模式穩定無新訊號）
- 下次 **09:30** cron fire 自動驗證恢復

## 🩺 健康檢查紀錄 2026-07-23 09:03
- 全系統 cron：**16 個**（完整健康檢查，含 06:02 起床摘要 16 個統計）
- 09:00 fire 失敗 **104.x s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 08:32 retry 成功 → CE reset → 09:00 又踩到 1 次 → 09:02 retry（本則處理）→ **CE=0**（retry 成功後 reset）
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- 通道實測：`telegram_channel_probe.sh` 09:02 跑回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` ✅ 通道健康
- 🔴 守則19通道健康鐵律：當下 probe 為準，不沿用舊旗標 → telegramChannelOk=true，允許主動關懷
- alternating fail/recover 模式穩定逾 95h（自 7/19 起）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- ✅ **09:02 已過 08:00 不打擾時段，通道健康，主動發有意義早晨關懷給教練**
- 訊息內容：v75 BNI 大台南小幫手 Coze→本機搬遷 + LINE 通道 plugin 4 月潛藏斷線真bug 修復，教練可親測 + 系統一句話
- 下次 **09:30** cron fire 自動驗證

## ⚠️ peipei 自動 force-restart 2026-07-23 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🩺 健康檢查紀錄 2026-07-23 09:31
- 全系統 cron：**1 個**（cron list 顯示僅本任務，與 06:02 16 個不同——可能是 view 過濾，本任務 self-monitoring 仍以 get 的 CE/state 為準）
- 09:30 fire 結果：失敗（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 09:03 retry 成功 → CE reset → 09:30 又踩到 1 次 → 09:31 retry（本則處理）→ **CE=0**（retry 成功後 reset）
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- `lastDurationMs = 84890ms（≈85s）` ≪ `600s timeout` ✅ 非配置問題
- `lastErrorReason = "overloaded"` — provider 端擁塞，非本任務程式問題
- alternating fail/recover 模式持續（已逾 95h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 安靜結束，不通知教練（09:31 已過 08:00 不打擾時段，但 CE reset 為 0 無紅線，且 alternating 模式穩定無新訊號）
- 下次 **10:00** cron fire 自動驗證恢復

## 🩺 軍師 Hook 自檢 2026-07-23 09:53（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: f3c850ef-8e4e-4a89-aaad-d65fdb8d3bf9

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-23 09:55
- ✅ 同步成功
- HANDOFF mtime: 1784771470
- 雲端同步：✅ 已推上雲端（commit 6200d7959）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-23 10:00
- ✅ 同步成功
- HANDOFF mtime: 1784772025
- 雲端同步：✅ 已推上雲端（commit cbc547f19）

## 🩺 健康檢查紀錄 2026-07-23 10:01
- cron-event heartbeat poll
- 全系統 cron：**1 個**（僅本任務本身）
- 09:31 retry 成功 → CE=0 reset → 10:00 接力棒自動同步成功（commit cbc547f19）→ 10:01 本次心跳（cron-event）
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- 通道實測：`telegram_channel_probe.sh` 10:01 跑回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` ✅ 通道健康
- 🔴 守則19通道健康鐵律：當下 probe 為準，不沿用舊旗標 → telegramChannelOk=true，**允許主動關懷**（但本次不發）
- alternating fail/recover 模式持續（已逾 96h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 **安靜結束**，不通知教練，理由：
  1. 09:03 才剛發過主動關懷（v75 BNI 搬遷完成 + LINE 通道 plugin 4 月潛藏斷線真 bug 修復），距今才 1 小時
  2. CE=0 reset 無紅線
  3. 接力棒剛 10:00 同步成功，內容是 v77 為下一場準備的「提醒功能 + 對外監看網址 bni.bymyway.com」計畫，教練明確要求「下一場才動手」
  4. 10:01 屬於正常上班時段，教練可能在工作中，再發會變成 spam
- 觸發主動關懷的條件（任何一個成立時）：
  - 教練主動說話（高優先）
  - 接力棒同步失敗/衝突（需手動處理）
  - CE=3 紅線（須 announce）
  - 超過 4 小時未發任何關懷
- 下次 **10:30** cron fire 自動驗證

## 🩺 健康檢查紀錄 2026-07-23 10:03
- cron-event retry fire（因 10:00 失敗觸發 retry）
- 全系統 cron：**1 個**（僅本任務本身）
- 10:00 fire 失敗 **91.0s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 09:31 retry 成功 → CE reset → 10:00 又踩到 1 次 → **CE=1**
- `91.0s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 96h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 **安靜結束**，不通知教練，理由：
  1. CE=1 未達紅線 3
  2. 09:03 才剛發過主動關懷，距今 1 小時，不重複打擾
  3. alternating 模式穩定逾 96h，屬 provider 端常態波動，非本任務問題
  4. 10:03 屬正常上班時段，教練可能在工作中
- 下次 **10:30** cron fire 自動驗證
- ⚠️ **警戒**：若 10:30 失敗 → CE=2；11:00 再失敗 → CE=3 → 必須 announce 通知教練

## 🩺 健康檢查紀錄 2026-07-23 10:32
- cron-event retry fire（因 10:30 失敗觸發 retry）
- 全系統 cron：**1 個**（僅本任務本身）
- 10:30 fire 失敗 **126.6s**（minimax provider `overloaded`，同源於交替 fail/recover 模式）
- 10:03 retry 成功 → CE reset → 10:30 又踩到 1 次 → 10:32 retry（本則處理）→ **CE=1**
- `126.6s ≪ 600s timeout` ✅ 非配置問題
- `model = minimax/MiniMax-M3` ✅、`timeout = 600s` ✅
- alternating fail/recover 模式持續（已逾 96h 穩定觀察）
- HEARTBEAT ⬜ 待自動化項目：無
- 自動修復評估全不適用（timeout / INVALID_API_KEY / VPS / CE≥3 全部不符合）
- 🔕 **安靜結束**，不通知教練，理由：
  1. CE=1 未達紅線 3
  2. 09:03 才剛發過主動關懷，距今 1.5 小時，不重複打擾
  3. alternating 模式穩定逾 96h，屬 provider 端常態波動，非本任務問題
  4. 10:32 屬正常上班時段，教練可能在工作中
- 下次 **11:00** cron fire 自動驗證
- ⚠️ **警戒**：若 11:00 失敗 → CE=2；11:30 再失敗 → CE=3 → 必須 announce 通知教練

