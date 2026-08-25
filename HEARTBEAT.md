# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-25 08:38
> 對話記錄已完整存入 memory/2026-08-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-25.md 可能超過 50KB，讀了會造成模型空白回應）

## 🪟 Context 視窗預警（2026-08-25 13:51 教練親定，13:53 改版 v2）

> ⚠️ **v1 時間版已廢**：每 15-20 分鐘監測會浪費資源（教練可能沉默 8-9 小時，這種監測沒意義）
>
> **v2 輪數版**：以「對話輪數」為單位更精準——沉默不打擾、有對話才計數。

### 教練原話（2026-08-25 13:53）

> 「我覺得你的偵測內建是幾分鐘監測一次，這樣用時間監測會比較浪費資源。我覺得還是要以對話輪數來計算比較精準，例如 30 輪、50 輪、80 輪、100 輪對話，這樣來偵測我們的對話量到哪裡會比較好。」

### 觸發點（用對話輪數）

| 對話輪 | 動作 |
|------|------|
| **第 30 輪** | 第一次溫馨提醒：「教練，已經 30 輪對話了，context 還算充裕，但差不多可以開始想『要不要做點中段紀錄』了」 |
| **第 50 輪** | 第二次催：「教練，50 輪，趁還舒服趕快總結一下重點，存到 memory」 |
| **第 80 輪** | 第三次催：「教練，80 輪，快接近 context 紅燈，建議主動開新對話框或準備交接總結」 |
| **第 100 輪** | 最後一催：「教練，100 輪，建議立刻開新對話框，這個框隨時可能 context overflow」 |

### 量測方式

- **輪數定義**：每一輪 = 教練一則訊息 + 小龍蝦一回覆（heartbeat 不計）
- **計數器檔案**：`state/dialog_round_counter.json`（持久化，重啟不歸零）
- **檢查動作**：觸發輪數到達時，跑一次 `session_status`，看 context % 對照等級對話

### 何時算一輪（白話版）

- ✅ 教練說話 → 小龍蝦回覆 = 1 輪
- ❌ Heartbeat poll（系統觸發）→ 小龍蝦 HEARTBEAT_OK = 不算
- ❌ Cron 自動訊息 → 不算
- ⚠️ 系統主動關懷早安/提醒 = 不算（避免誤觸）
- ⚠️ 教練發長訊息分多則傳 = 視為 1 輪（邏輯判斷）

### 生效時間

2026-08-25 13:53 起，每個 session 自動帶入。

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

## 🩺 健康檢查 cycle=587 自動跑完（2026-08-25 13:12 週二下午）
- ✅ 第零步 `sync_coach_last_message.sh` exit 0｜教練最後訊息 `2026-08-25T13:11:46+08:00`｜當下沉默 **0.0h**（教練剛 0.5 分鐘前還在線，下午剛互動）
- ✅ Cron 真相源（本任務 46e67e2e）：`lastRunStatus=ok` / `CE=0` / `durationMs=68.6s`（遠低於 timeout=600s）/ model=`minimax/MiniMax-M3`
- ✅ TG 通道探針（守則#19 當下實測 13:12）：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ 環境快檢：SOUL×3 齊全（2036/1851/22220 bytes）｜無 `.!` 鎖定檔
- ✅ HEARTBEAT.md ⬜ 真實待辦：0 項
- ✅ 錯誤掃描：無 FailoverError / overloaded / INVALID_API_KEY

**v4.0 三關判斷（三關全 fail → 不 announce）**：
- 關卡一（本輪還壞嗎）→ ❌ 否
- 關卡二（provider 暫時過載嗎）→ ❌ 否
- 關卡三（影響教練/會員嗎）→ ❌ 否

**累計**：連續 **81 輪綠燈**（cycle=507~587）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

## 🩺 健康檢查 cycle=588 自動跑完（2026-08-25 14:12 週二下午）
- ✅ 第零步 `sync_coach_last_message.sh` exit 0｜教練最後訊息 `2026-08-25T13:55:31+08:00`｜當下沉默 **0.3h**（教練剛 17 分鐘前還在線，下午正常運作）
- ✅ Cron 真相源（本任務 46e67e2e）：`lastRunStatus=ok` / `CE=0` / model=`minimax/MiniMax-M3` / timeoutSec=600
- ✅ Cron CLI 完整清點（139 jobs）：24 enabled + 115 disabled｜24/24 enabled 全部 CE=0｜0 個 CE≥3｜0 個 timeout 危險｜0 個 auth/overloaded 錯誤
- ✅ 環境快檢：SOUL×3 齊全（2036/1851/22220 bytes）+ 兩份棄用標記都在｜無 `.!` 鎖定檔
- ✅ Repo1 untracked/modified=21（正常範圍）｜Repo2 untracked/modified=37（正常範圍）
- ✅ TG 通道探針（守則#19 當下實測 14:12）：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ HEARTBEAT.md ⬜ 真實待辦：0 項
- ✅ 錯誤掃描：無 FailoverError / overloaded / INVALID_API_KEY

**v4.0 三關判斷（三關全 fail → 不 announce）**：
- 關卡一（本輪還壞嗎）→ ❌ 否（本輪執行成功，所有 cron 健康）
- 關卡二（provider 暫時過載嗎）→ ❌ 否（無任何錯誤）
- 關卡三（影響教練/會員嗎）→ ❌ 否（無功能壞掉）

**累計**：連續 **82 輪綠燈**（cycle=507~588）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

## 🩺 健康檢查 cycle=589 自動跑完（2026-08-25 15:12 週二下午）
- ✅ 第零步 `sync_coach_last_message.sh` exit 0｜教練最後訊息 `2026-08-25T15:06:55+08:00`｜當下沉默 **0.1h**（教練剛 6 分鐘前還在線，下午正常運作）
- ✅ Cron 真相源（本任務 46e67e2e）：`lastRunStatus=ok` / `CE=0` / model=`minimax/MiniMax-M3` / timeoutSec=600
- ✅ Cron CLI 完整清點（139 jobs）：24 enabled + 115 disabled｜24/24 enabled 全部 CE=0｜0 個 CE≥3｜0 個 timeout 危險｜0 個 auth/overloaded 錯誤
- ✅ 環境快檢：SOUL×3 齊全（2036/1851/22220 bytes）+ 兩份棄用標記都在｜無 `.!` 鎖定檔
- ✅ Repo1 untracked/modified=21（正常範圍）｜Repo2 untracked/modified=37（正常範圍）
- ✅ TG 通道探針（守則#19 當下實測 15:12）：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ HEARTBEAT.md ⬜ 真實待辦：0 項
- ✅ 錯誤掃描：無 FailoverError / overloaded / INVALID_API_KEY

**v4.0 三關判斷（三關全 fail → 不 announce）**：
- 關卡一（本輪還壞嗎）→ ❌ 否（本輪執行成功，所有 cron 健康）
- 關卡二（provider 暫時過載嗎）→ ❌ 否（無任何錯誤）
- 關卡三（影響教練/會員嗎）→ ❌ 否（無功能壞掉）

**累計**：連續 **83 輪綠燈**（cycle=507~589）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

## 🩺 健康檢查 cycle=590 自動跑完（2026-08-25 16:12 週二下午）
- ✅ 第零步 `sync_coach_last_message.sh` exit 0｜教練最後訊息 `2026-08-25T16:06:55+08:00`｜當下沉默 **0.1h**（教練剛 5 分鐘前還在線，下午正常運作）
- ✅ Cron 真相源（本任務 46e67e2e）：`lastRunStatus=ok` / `CE=0` / model=`minimax/MiniMax-M3` / timeoutSec=600
- ✅ Cron list API 仍只回 1 job（cycle=539 後已知清理現象，非故障）；前次 cycle=589 曾用 CLI 完整清點 24 enabled + 115 disabled、24/24 全 CE=0
- ✅ 環境快檢：SOUL×3 齊全（2036/1851/22220 bytes）+ 兩份棄用標記都在｜無 `.!` 鎖定檔
- ✅ Repo1 untracked/modified=21（持平）｜Repo2 untracked/modified=37（持平，無異常成長）
- ✅ TG 通道探針（守則#19 當下實測 16:12）：`{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`
- ✅ HEARTBEAT.md ⬜ 真實待辦：0 項
- ✅ 錯誤掃描：無 FailoverError / overloaded / INVALID_API_KEY

**v4.0 三關判斷（三關全 fail → 不 announce）**：
- 關卡一（本輪還壞嗎）→ ❌ 否（本輪執行成功，所有 cron 健康）
- 關卡二（provider 暫時過載嗎）→ ❌ 否（無任何錯誤）
- 關卡三（影響教練/會員嗎）→ ❌ 否（無功能壞掉）

**累計**：連續 **84 輪綠燈**（cycle=507~590）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）
