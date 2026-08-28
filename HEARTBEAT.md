# HEARTBEAT 熱上下文（每次心跳必讀）

---

## 🩺 cycle=627 健康檢查紀錄（2026-08-28 10:12，週五早晨）

**檢查結果**：✅ 全綠，安靜通過，不通知教練

| 檢查項 | 結果 |
|--------|------|
| 第零步 `sync_coach_last_message.sh` | ✅ exit 0｜教練最後訊息 09:36:55（沉默 **0.6h**，當下 date 新鮮值，週五上午活躍中）|
| 本任務 46e67e2e | ✅ lastRunStatus=ok / CE=0 / durationMs≈157s < timeout=600s / model=minimax/MiniMax-M3 |
| cron_jobs SQLite 完整清點 | 148 總 / 25 enabled / **0 個 CE≥3** / **0 個 CE≥1** / 23 lastStatus=ok / 0 error |
| 錯誤型態掃描 | 0 overloaded / 0 timeout / 0 auth/apiKey / 0 任何其他 |
| HEARTBEAT.md ⬜ 真實待辦 | 0 項 |
| 環境快檢 | SOUL.md 三份齊全 (9015/1851/22220 bytes) ✅｜Repo1=23 / Repo2=25（遠低於 50 警戒線）✅｜無 `.!` 鎖定檔 ✅|
| TG 通道探針（守則#19 當下實測）| ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` |

**v4.0 三關判斷：**
- 關卡一（現在還壞嗎）→ ❌ fail（全 25 enabled cron 都 ok）
- 關卡二（provider overload 嗎）→ ❌ fail（0 個）
- 關卡三（影響教練/會員工作嗎）→ ❌ fail（無功能受阻）
→ **三關全 fail → 安靜處理，不通知教練**

**進步訊號**：前次 cycle=626 紀錄的 ☕幕僚長晨報 CE=1（07:00 因 06:00 context overflow gateway restart 中斷）→ 本輪已**完全恢復**為 CE=0（明早 07:00 retry 自然復原，整個 alternating mode 又走完一輪）

**已落痕跡：**
- ✅ `state/healthcheck.log` 追加 cycle=627 紀錄
- ✅ `state/heartbeat-state.json` 將更新（lastCycle=627 / TG 探針 10:12）
- ✅ `HEARTBEAT.md` prepend 本段
- ✅ cumulativeGreen = **9**（cycle=618~627 連 9 輪綠）

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

下個 cron：**11:12 健康檢查（cycle=628）**。


> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-28 10:00
> 對話記錄已完整存入 memory/2026-08-28.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-28.md 可能超過 50KB，讀了會造成模型空白回應）

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
