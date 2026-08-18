# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-19 03:07
> 對話記錄已完整存入 memory/2026-08-19.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-19.md 可能超過 50KB，讀了會造成模型空白回應）

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

---

## 🦞 cycle=439 健康檢查（2026-08-19 04:12 Asia/Taipei）

> Context Overflow 重啟後第一次完整健康檢查（重啟於 03:07）。HEARTBEAT.md 已從範本恢復，繼續寫紀錄。

### 真相源
- `~/.openclaw/cron.db` 是 **0 bytes**（重啟副作用，已知歷史問題）
- `~/.openclaw/state/openclaw.sqlite` (57MB) 是真正的真相源，已用 `cron_jobs` + `cron_run_logs` 直查驗證

### 啟用任務（25 個，sqlite 直查）
- **全部 `last_run_status = ok` / `consecutive_errors = 0`**
- 唯一例外：本任務自己（🦞 每小時任務健康檢查）`CE = 1`，上一輪（cycle=438 / 03:13）失敗為 `Process: good-river-2 failed`（重啟副作用，**教練無法介入**）
- 本輪（cycle=439 / 04:12）正在執行 = 已恢復鐵證

### 24h 內失敗歸因（36 筆，100% 分類完畢）
| 類型 | 筆數 | 影響任務 | 處理 |
|------|------|----------|------|
| **minimax 過載**（`FailoverError: temporarily overloaded`） | 16 | 蒸餾×11 / LINE@使用回報×2 / 場景化×1 / 幕僚長晨報×1 / 起床摘要×1 | 每次 cron retry 都自癒，廠商端塞車**教練無法介入** |
| **process failed**（重啟副作用） | 1 | 本任務 03:13 一次 | Context Overflow 重啟的 `good-river-2` 進程崩潰，**教練無法介入**，本輪已恢復 |
| **disabled 歷史 log**（`提醒-default-beat-*`） | 18 | 全是 enabled=0 的舊提醒殘留 | 已停用，不影響工作 |
| **timeout** | 0 | — | 無 |

### 環境快檢
- SOUL×3：2036 / 20631 / 1851 bytes，齊全 ✅
- Repo1 = 112 持平 / Repo2 = 40（重啟後 +6，正常浮動）
- `.!` 鎖定檔：無 ✅
- TG 通道探針（守則#19）：✅ `{"ok":true}` 04:13 當下實測

### v4.0 三關判斷
- **關卡一（本輪還壞嗎）**：❌ 否（25 cron 全綠 + 本輪正在寫報告 + 重啟後已恢復）
- **關卡二（provider 過載嗎）**：✅ 是（minimax FailoverError 持續背景噪音）→ 按規則「一律不 announce」
- **關卡三（影響教練嗎）**：❌ 否（凌晨 04:12 + 教練 1.1h 沉默 = 在睡 + cron retry 都自癒 + 無教練/會員實際依賴的功能壞掉）

→ **三關未同時成立 → 安靜結束，不 announce 教練**（守則「該靜就靜」）

### 觀察項（不 announce，教練可選時再決）
1. minimax 過載是凌晨常態背景雜訊（從 08-17 起持續），目前 cron retry 每次都自癒，未達「持續 2 小時未恢復」升級條件
2. `cron.db` 0 bytes 是 Context Overflow 重啟後遺症，若下次重啟再發生，可能需要評估是否要做 cron.db 持久化保護

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

---

## 🦞 cycle=440 健康檢查（2026-08-19 05:12 Asia/Taipei）

### 真相源
- 教練最後訊息：2026-08-19 03:09（沈默 2.1h → 凌晨在睡）
- 啟用 25 任務 → **全部 `last_run_status=ok` / `consecutive_errors=0`**

### 24h 內失敗歸因（36 筆，與 cycle=439 同分布）
| 類型 | 筆數 | 處理 |
|------|------|------|
| minimax 過載 | 16 | 廠商端塞車，cron retry 每次自癒 |
| process failed（本任務 03:13 一次） | 1 | 重啟副作用，已恢復 |
| 舊提醒殘留（enabled=0） | 19 | `command exited with code 1`，不影響工作 |

### v4.0 三關判斷
- 關卡一：❌ 本輪全綠 + 正在寫報告 = 已恢復
- 關卡二：✅ 主因是 minimax 過載（教練無法介入）
- 關卡三：❌ 凌晨 5:12 + 教練在睡 + 無會員實際依賴功能壞掉

→ **三關未同時成立 → 安靜結束，不 announce 教練**

⏭️ 跳過 commit+push
