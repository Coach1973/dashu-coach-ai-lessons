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
