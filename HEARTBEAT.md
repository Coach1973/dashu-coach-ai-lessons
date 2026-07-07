# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-07 20:38
> 對話記錄已完整存入 memory/2026-07-07.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-07.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🎯 主動觸發掛牌（2026-07-08 03:21 教練交付，W03 升級版）

**教練說過：**
- 01:32「之後我其他電腦要做這個增量備份的時候，如果我忘記的話，再請你幫我記住。」
- 03:21「來自宏碁電腦的寶貴經驗值，幫我記錄一下，因為我即將要在**佩佩老師的那臺電腦**裡面進行這樣的工作。」

**看到以下任一關鍵字 → 主動提醒，不要等教練開口：**
- 增量備份 / junction 搬家 / 過期備份 / 搬資料
- 新電腦（ACER、Lenovo、Mac 副機、**佩佩老師那台**）要備份
- D 碟空間相關 / `D:\junction\`、`D:\junction-backup\` 任何路徑
- 🆕 **「佩佩」+ 備份/搬家/增量 任何組合**（佩佩的機器第一次做）

**完整 SOP（兩份並行）：**
- **新機器首選 W03**（最完整生命週期 SOP）：`試金石/試金石_專案與代碼.md` 搜尋「案例 W03」，第 377 行起
- 已跑過一輪、純清理用案例 39：`記憶/試金石_案例庫.md`（commit `0b01455c`）

**鐵律四條：**
1. Junction 存在≠資料是活的
2. 搬家一次不只搬一個 App
3. 使用者資料與軟體元件驗證標準不同
4. 🆕 孤兒資料夾判準：沒有任何現役 Junction 指向它才算孤兒（不只看名字）
**刪除鐵律：** 走 `scripts/delete_guard.ps1` 的 `Safe-Remove`，**該檔在 Windows PowerShell 5.1 下需先轉檔加 BOM 再 `.` 載入**（中文 ParseException 陷阱）
**語音陷阱：** 「Cloud Data」=Claude-Data / 「西潮/低潮」=C槽/D槽，主動覆述確認
**佩佩老師電腦提醒：** 我不替佩佩那邊的 CLI 下指令，只提醒教練去派工作

---

## 學長 relay poll
### 2026-07-07 2026-07-07 23:59 - relay poll OK

### 2026-07-08 2026-07-08 03:13 - relay poll OK
## 🚀 Session-End 雲端同步 2026-07-07 22:09（Mac）
- ✅ pushed 7dd420a2c
- 同步路徑：HEARTBEAT.md memory/

## 🚀 Session-End 雲端同步 2026-07-07 22:15（Mac）
- ✅ pushed b21f47540
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-07-08 00:15（Mac）
- ✅ pushed 1351d4ad9
- 同步路徑：HEARTBEAT.md

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-08 01:35
- ✅ 同步成功
- HANDOFF mtime: 1783445591
- 雲端同步：✅ 已推上雲端（commit 32d2e24c8）

## 🚀 Session-End 雲端同步 2026-07-08 01:51（Mac）
- ✅ pushed d02343dbd
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-07-08 02:04（Mac）
- ✅ pushed 03c047ba7
- 同步路徑：HEARTBEAT.md memory/

## 🚀 Session-End 雲端同步 2026-07-08 02:06（Mac）
- ✅ pushed 91e18867e
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-07-08 02:08（Mac）
- ✅ pushed d1e9eca31
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-07-08 02:17（Mac）
- ✅ pushed 178485ddc
- 同步路徑：HEARTBEAT.md

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-08 02:20
- ✅ 同步成功
- HANDOFF mtime: 1783448219
- 雲端同步：✅ 已推上雲端（commit 744253fac）

## 🚀 Session-End 雲端同步 2026-07-08 03:02（Mac）
- ✅ pushed 23dadc05c
- 同步路徑：HEARTBEAT.md memory/

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-08 03:55
- ✅ 同步成功
- HANDOFF mtime: 1783453940
- 雲端同步：✅ 已推上雲端（commit 6155f06a2）

## 🩺 軍師 Hook 自檢 2026-07-08 04:48（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：好，太棒了！還好你有做求證�
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: a21977a4-b019-4888-996c-b12b5186897b

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-08 04:54
- ✅ 同步成功
- HANDOFF mtime: 1783457655
- 雲端同步：✅ 已推上雲端（commit d701fe336）

## 🩺 軍師 Hook 自檢 2026-07-08 05:11（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：你這樣很不專業，因為這件事�
- 雲端狀態：✅ 已拉雲端最新（HEAD: 18daa1f51）
- Session: b528b8a2-4944-48ba-b02c-ca6987a8449e

## 🩺 軍師 Hook 自檢 2026-07-08 05:12（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：> 掛牌升級四件事:

  1. 雙 SOP �
- 雲端狀態：✅ 已拉雲端最新（HEAD: f60e9b356）
- Session: ba466be0-58a7-4f84-a170-be1f5344791a

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-08 05:30
- ✅ 同步成功
- HANDOFF mtime: 1783459819
- 雲端同步：✅ 已推上雲端（commit 4d31abaed）
