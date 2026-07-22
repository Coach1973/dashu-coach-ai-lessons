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
