# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-18 02:38
> 對話記錄已完整存入 memory/2026-08-18.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-18.md 可能超過 50KB，讀了會造成模型空白回應）

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

## cycle=412 健康檢查（2026-08-18 03:12 週二凌晨）

| 項目 | 結果 |
|------|------|
| 第零步 sync_coach_last_message | ✅ exit 0｜教練沉默 **0.6h**（02:36 剛講話）|
| Cron 本體 46e67e2e | ✅ ok / CE=0 / 59631ms / model=minimax/MiniMax-M3 |
| Cron 列表（CLI 真相源） | tool API 只回 1 個（cycle=354 起已知過濾限制，不影響工作） |
| 已知非新發 error | cycle=388 (08-17 08:12) "Agent couldn't generate a response" + cycle=382 (08-17 03:12) "LLM request timed out 442s" — 皆 minimax 瞬時中斷，本輪已自恢復 |
| Timeout 紅線 | ✅ 59631ms ≪ 600s（9.9%） |
| HEARTBEAT ⬜ 待辦 | 0 項 |
| HEARTBEAT.md 行數 | 22（<500 警戒線 ✅）|
| healthcheck.log | 564 行（<1000 警戒線 ✅）|
| SOUL×3 齊全 + 棄用標記 | ✅ 2036/20631/1851 bytes |
| Repo1 / Repo2 | 112 持平 / 26（正常範圍）|
| .! 鎖定檔 | ✅ 無 |
| TG 通道探針（守則#19）| ✅ 本輪 03:12 當下實測 `{"ok":true}` |

**v4.0 三關判斷**（全 fail → 安靜結束，不 announce 教練）：
- 關卡一（本輪還壞嗎）→ ❌ 否（cron ok + CE=0 + 本輪成功 = 已恢復）
- 關卡二（provider 過載嗎）→ ❌ 否（無 FailoverError / 無 overloaded）
- 關卡三（影響教練嗎）→ ❌ 否（凌晨 03:12 sleep time + 教練 0.6h 剛發言 + 只是監控工具自己打嗝）

✅ 已自動維護：HEARTBEAT.md 已 append cycle=412
⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

下個 cron：04:12 健康檢查。

## cycle=413 健康檢查（2026-08-18 04:12 週二凌晨）

| 項目 | 結果 |
|------|------|
| 第零步 sync_coach_last_message | ✅ exit 0｜教練沉默 **1.6h**（02:36 最後發言，凌晨睡眠中）|
| Cron 列表（CLI 真相源） | 47 任務全部 enabled，**consecErr 全為 0**，無任何 lastError |
| Timeout 紅線 | ✅ 本任務 600s（尚未執行，無超時疑慮） |
| HEARTBEAT ⬜ 待辦 | 0 項 |
| HEARTBEAT.md 行數 | 50（<500 警戒線 ✅）|
| .! 鎖定檔 | ✅ 無 |

**v4.0 三關判斷**（全 fail → 安靜結束，不 announce 教練）：
- 關卡一（本輪還壞嗎）→ ❌ 否（cron 全部 ok + CE=0）
- 關卡二（provider 過載嗎）→ ❌ 否（無 FailoverError / 無 overloaded）
- 關卡三（影響教練嗎）→ ❌ 否（凌晨 04:12 sleep time + 教練在睡 + 無任務壞掉）

✅ 已自動維護：HEARTBEAT.md 已 append cycle=413
⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

下個 cron：05:12 健康檢查。
