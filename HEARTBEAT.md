# HEARTBEAT 熱上下文（每次心跳必讀）

## 🦞 05:32 健康檢查 trace（安靜處理）

| 項目 | 狀態 |
|------|------|
| Cron 任務 | 唯一任務（健康檢查自己） |
| lastRunStatus | 🟡 error（05:30 那次，overloaded, 136.6s） |
| consecutiveErrors | 🟡 1（< 3 閾值，不升級） |
| Model | ✅ minimax/MiniMax-M3（2026-07-15 已修正） |
| Timeout 600s | ✅ 足夠（136.6s 遠低於上限） |
| HEARTBEAT.md | ✅ 無 ⬜ 待辦、無 48h 停滯背景工作 |
| Pipeline 交替模式 | 04:30❌→04:32✅→05:02✅→05:30❌→本次 05:32（Pipeline 仍可恢復） |

**結論**：🟡 觀察中，安靜處理不通知教練。凌晨 5:32 在睡眠時間（守則 #12 避免訊息疲勞）。
無自動修復動作（守則 #15 誠實原則：provider overload 屬 minimax 端外部波動，無法用改 config 修復）。

等 06:00 自動跑驗證；若下次仍 overload（consecutiveErrors ≥ 3）→ 才升級通知教練；
若下次成功 → consecutiveErrors 自動歸零。

---

## 🦞 05:02 健康檢查 trace（安靜處理）

| 項目 | 狀態 |
|------|------|
| Cron 任務 | 唯一任務（健康檢查自己） |
| lastRunStatus | 🟡 error（04:30 那次，overloaded, 112.6s） |
| consecutiveErrors | 🟡 1（< 3 閾值，不升級） |
| Model | ✅ minimax/MiniMax-M3（2026-07-15 已修正） |
| Timeout 600s | ✅ 足夠（112.6s 遠低於上限） |
| HEARTBEAT.md | ✅ 無 ⬜ 待辦、無 48h 停滯背景工作 |
| Pipeline 交替模式 | 04:04✅→04:30❌→04:32✅→本次 05:02（Pipeline 仍可恢復） |

**結論**：🟡 觀察中，安靜處理不通知教練。凌晨 5:02 在睡眠時間（守則 #12 避免訊息疲勞）。
無自動修復動作（守則 #15 誠實原則：provider overload 屬 minimax 端外部波動，無法用改 config 修復）。

等 05:30 自動跑驗證；若下次仍 overload（consecutiveErrors ≥ 3）→ 才升級通知教練；
若下次成功 → consecutiveErrors 自動歸零。

---


> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-16 03:07
> 對話記錄已完整存入 memory/2026-07-16.md 並推上 GitHub，零遺漏

## 🦞 04:32 健康檢查 trace（安靜處理）

| 項目 | 狀態 |
|------|------|
| Cron 任務 | 唯一任務（健康檢查自己） |
| lastRunStatus | 🟡 error（04:30 那次，overloaded, 85.3s） |
| consecutiveErrors | 🟡 1（< 3 閾值，不升級） |
| Model | ✅ minimax/MiniMax-M3（2026-07-15 已修正） |
| Timeout 600s | ✅ 足夠（85.3s 遠低於上限） |
| HEARTBEAT.md | ✅ 無 ⬜ 待辦、無 48h 停滯背景工作 |
| Pipeline 交替模式 | 03:00❌→03:33✅→03:30❌→04:04✅→04:30❌→本次 04:32✅（仍可恢復） |

**結論**：🟡 觀察中，安靜處理不通知教練。凌晨 4:32 不打擾教練（守則 #12 避免訊息疲勞）。
無自動修復動作（守則 #15 誠實原則：provider overload 屬 minimax 端外部波動，無法用改 config 修復）。

等 05:00 自動跑驗證；若下次仍 overload（consecutiveErrors ≥ 3）→ 才升級通知教練；
若下次成功 → consecutiveErrors 自動歸零。

## 🦞 04:04 健康檢查 trace（安靜處理）

| 項目 | 狀態 |
|------|------|
| Cron 任務 | 唯一任務（健康檢查自己） |
| lastRunStatus | 🟡 error（03:30 那次，overloaded, 111.7s） |
| consecutiveErrors | 🟡 1（< 3 閾值，不升級） |
| Model | ✅ minimax/MiniMax-M3（2026-07-15 已修正） |
| Timeout 600s | ✅ 足夠（111.7s 遠低於上限） |
| HEARTBEAT.md | ✅ 無 ⬜ 待辦、無 48h 停滯背景工作 |
| Pipeline 交替模式 | 03:00❌→03:33✅→03:30❌→本次 04:04✅（仍可恢復） |

**結論**：🟡 觀察中，安靜處理不通知教練。凌晨 4:04 不打擾教練（守則 #12 避免訊息疲勞）。
無自動修復動作（守則 #15 誠實原則：provider overload 屬 minimax 端外部波動，無法用改 config 修復）。

等 04:30 自動跑驗證；若下次仍 overload（consecutiveErrors ≥ 3）→ 才升級通知教練；
若下次成功 → consecutiveErrors 自動歸零。

## 🦞 03:33 健康檢查 trace（安靜處理）

| 項目 | 狀態 |
|------|------|
| Cron 任務 | 唯一任務（健康檢查自己） |
| lastRunStatus | 🟡 error（03:00 那次，overloaded, 164.4s） |
| consecutiveErrors | 🟡 1（< 3 閾值，不升級） |
| Model | ✅ minimax/MiniMax-M3（2026-07-15 已修正） |
| Timeout 600s | ✅ 足夠（164.4s 遠低於上限） |
| HEARTBEAT.md | ✅ 無 ⬜ 待辦、無 48h 停滯背景工作 |
| Pipeline 交替模式 | 03:00❌→本次 03:33✅（仍可恢復） |

**結論**：🟡 觀察中，安靜處理不通知教練。凌晨 3:33 不打擾教練（守則 #12 避免訊息疲勞）。
等 04:00 自動跑驗證；若下次仍 overload（consecutiveErrors ≥ 3）→ 才升級通知教練；
若下次成功 → consecutiveErrors 自動歸零。

無自動修復動作（守則 #15 誠實原則：provider overload 屬 minimax 端外部波動，無法用改 config 修復）。

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-16.md 可能超過 50KB，讀了會造成模型空白回應）

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
