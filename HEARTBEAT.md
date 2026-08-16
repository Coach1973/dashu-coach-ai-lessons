# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-16 17:37
> 對話記錄已完整存入 memory/2026-08-16.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-16.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-16 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-16 20:26
- ✅ 同步成功
- HANDOFF mtime: 1786883169
- 雲端同步：✅ 已推上雲端（commit 5386e8fa3）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-16 20:35
- ✅ 同步成功
- HANDOFF mtime: 1786883731
- 雲端同步：✅ 已推上雲端（commit 3cda4a604）

## 🩺 軍師 Hook 自檢 2026-08-16 20:43（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 7d4244d1-db9c-42f8-97ad-dc02499cbe41

## 🩺 健康檢查 cycle=375 2026-08-16 21:12（v4.0 安靜結束）
- ✅ 23 cron 全 healthy（lastStatus=ok/running/idle, CE=0）
- ✅ sync_coach_last_message.sh exit 0｜教練沉默 0.0h（剛發言活躍）
- ✅ TG 通道實測 ok:true（守則#19 當下實測）
- ✅ HEARTBEAT.md 47 行 (<500) / 0 ⬜ 待辦
- ✅ SOUL×3 齊全，兩份舊版皆有「⚠️ 本檔已棄用」標記
- ✅ Repo1=112 持平 / Repo2=30 微動 / 無 .! 鎖定檔
- ⚠️ healthcheck.log 1008 行（已破 1000 警戒線，下次健康檢查留意，建議截前半部歸檔）
- v4.0 三關全 fail（現在沒壞 + 非 provider 過載 + 不影響工作）→ 安靜結束不推 Telegram

## 🪨 試金石策展提醒 2026-08-16 21:00
- top10_dynamic.md 已 39 天未更新
- 候選池：特助場景庫_自動增量.md 累積 50 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-16 22:00
- ✅ 同步成功
- HANDOFF mtime: 1786888704
