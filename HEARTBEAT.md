# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-09-01 01:00
> 對話記錄已完整存入 memory/2026-09-01.md 並推上 GitHub，零遺漏

---

## 🦞 健康檢查 cycle=692（2026-09-01 05:12 TPE 凌晨）

```
✅ 已自動修復：無
⚠️ 需要注意：無（v4.0 三關全 fail → 不 announce）
✅ 無異常
```

| 檢查項 | 結果 |
|---|---|
| 第零步 `sync_coach_last_message.sh` | ✅ exit 0｜教練最後訊息 `2026-09-01T05:10:57+08:00`（沉默 **0.0h**，凌晨剛說話） |
| Cron 系統 | ✅ 1 個活躍任務（本健康檢查本身），lastRunStatus=ok、CE=0 |
| CE≥3 / Timeout危險 / Auth 失效 | 0 / 0 / 0 |
| HEARTBEAT.md ⬜ 真實待辦 | 0 項 |
| TG 通道探針（守則#19 當下實測） | ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` |
| 環境快檢 | SOUL×3 齊全（9015/1851/22220 bytes）✅｜Repo1=23 / Repo2=19（皆 < 50 警戒線）✅｜無 `.!` 鎖定檔 ✅ |

**v4.0 三關判斷（全 fail → 🔕 不 announce）：**
- 關卡一（本輪還壞嗎）→ ❌ fail（cron 全綠 + 本輪執行成功 = 已恢復鐵證）
- 關卡二（provider overload 重災嗎）→ ❌ fail（無錯誤）
- 關卡三（影響教練/會員嗎）→ ❌ fail（凌晨 05:12 + 教練剛剛才說話 + 零會員功能壞）

**累計**：cumulativeGreen = **59**（從 58 +1）
**已落痕跡**：HEARTBEAT.md prepend、state/cumulative_green=59、state/healthcheck_cycle=692、state/healthcheck.log 追加（9 行）、state/heartbeat-state.json 完整更新

⏭️ 跳過 commit+push（2026-07-05 教練拍板由 23:05 三機總結統一備份）

🔕 **結論：安靜通過，不打擾教練。** 下輪：**06:12 cycle=693**

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-09-01.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-01 04:05
- ✅ 同步成功
- HANDOFF mtime: 1788206501
- 雲端同步：✅ 已推上雲端（commit bd0da4b64）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-01 05:00
- ✅ 同步成功
- HANDOFF mtime: 1788209889
- 雲端同步：✅ 已推上雲端（commit 3b1c9c2b7）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-01 05:10
- ✅ 同步成功
- HANDOFF mtime: 1788210476
- 雲端同步：✅ 已推上雲端（commit 90c334bdd）
