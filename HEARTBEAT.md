# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-09-15 15:00
> 對話記錄已完整存入 memory/2026-09-15.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-09-15.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-15 17:10
- ✅ 同步成功
- HANDOFF mtime: 1789463185
- 雲端同步：push 失敗（離線或網路問題，commit 已留本機）

## 🩺 軍師 Hook 自檢 2026-09-15 20:22（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: b2de19609）
- 小龍蝦信箱：（信箱查無新信）
- Session: 01fe63bd-b2f3-49bf-9c6c-6bab0ccd332b

## 🩺 軍師 Hook 自檢 2026-09-15 21:20（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: 01bc18d97）
- 小龍蝦信箱：（信箱查無新信）
- Session: 56b9f8ed-5dc0-425a-a86f-82908e70377e

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-16 02:02
- ✅ 同步成功
- HANDOFF mtime: 1789495347
- 雲端同步：✅ 已推上雲端（commit 3432f46dd）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-16 02:07
- ✅ 同步成功
- HANDOFF mtime: 1789495648
- 雲端同步：✅ 已推上雲端（commit d2edc9f8a）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-16 02:52
- ✅ 同步成功
- HANDOFF mtime: 1789498364
- 雲端同步：✅ 已推上雲端（commit 9c3c0451d）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-16 03:20
- ✅ 同步成功
- HANDOFF mtime: 1789499945
- 雲端同步：✅ 已推上雲端（commit 0f429605f）

## 🩺 軍師 Hook 自檢 2026-09-16 03:25（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: 61abc74ad）
- 小龍蝦信箱：（信箱查無新信）
- Session: 36ae39e7-1951-48a3-b92b-0aca54588c2e

## 🔴🔴🔴 2026-09-16 04:03~04:13 重大事故：main gateway+小二雙雙down機45分鐘，已修復
- **起因**：終端機PATH解析到新版openclaw(2026.9.4)，正式launchd服務用舊版(2026.6.34)，版本落差導致state資料庫schema被新版升級到17，舊版打不開
- **引爆點**：軍師為了讓新hook生效執行`launchctl kickstart -k`重啟main gateway，直接撞上版本不相容
- **連帶損害**：搶修過程中誤`kill -9`一個PID，實為小二(test2)的子行程，小二也連帶停止服務
- **已修復**：main gateway改用新版執行檔(plist)+`openclaw doctor --fix`完成schema/session store遷移+`openclaw gateway start`重新啟用；小二用`nohup`手動重新拉起
- **驗證通過**：main gateway 24個hook全載入(含新的industry-chain-sop)、LINE三帳號+Telegram三帳號provider正常、process穩定15秒+無ERROR；小二`gateway ready`+bot_test2 provider正常
- **副作用**：`doctor --fix`把`HEARTBEAT.md`/`TOOLS.md`從檔案系統清掉(遷移到SQLite的副作用)，已用`git checkout HEAD --`從git歷史救回，內容零遺漏
- **完整記錄**：試金石案例73
- ⚠️ **下次任何人要重啟main gateway前，先確認`which openclaw`跟launchd plist裡的執行檔路徑是否一致，不一致先不要重啟**
