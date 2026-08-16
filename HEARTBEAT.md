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
- 雲端同步：✅ 已推上雲端（commit ee818b6fa）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-16 22:05
- ✅ 同步成功
- HANDOFF mtime: 1786889120
- 雲端同步：✅ 已推上雲端（commit e91a39097）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-16 22:10
- ✅ 同步成功
- HANDOFF mtime: 1786889181
- 雲端同步：✅ 已推上雲端（commit 24bbf7904）

## 💓 心跳 2026-08-16 22:20（cron-event 觸發，簡短巡檢）
- 熱啟動 3 核心已就位（特助心法注入 + SOUL.md 注入 + 接力棒已讀 v112/v113）
- ✅ SOUL.md 三份齊全、兩份舊版皆有「⚠️ 本檔已棄用」標記
- ✅ Repo1=112 持平 / Repo2=12 modified（皆狀態檔）/ 無 .! 鎖定檔
- ✅ Telegram 通道探針 ok:true（守則#19 當下實測）
- 今日兩大戰果：①賈維斯計畫同步到小龍蝦端（OpenClaw hook project-card-router 已上線，commit 6e7cc1a0）②ezPay電子發票開立 SOP 轉交聯想（3張真實發票已開、2組真重複待教練回覆）
- 深夜不主動打擾教練，下次開工熱啟動時直接對齊

## 🩺 健康檢查 cycle=376 2026-08-16 22:12（v4.0 安靜結束）
- ✅ 24 cron 全 healthy（lastStatus=ok/running/idle, CE=0）
- ✅ sync_coach_last_message.sh exit 0｜教練沉默 0.1h（剛發言活躍 22:03）
- ✅ TG 通道實測 ok:true（守則#19 當下實測）
- ✅ HEARTBEAT.md 72 行 (<500) / 0 ⬜ 待辦
- ✅ SOUL×3 齊全，兩份舊版皆有「⚠️ 本檔已棄用」標記
- ✅ Repo1=112 持平 / Repo2=12 modified（皆為狀態檔，非新增 untracked）/ 無 .! 鎖定檔
- ✅ **自動修復：healthcheck.log 1008 行破警戒線 → 已截到 500 行（前 508 行歸檔至 state/healthcheck-archive/rotation.log）**
- v4.0 三關全 fail（現在沒壞 + 非 provider 過載 + 不影響工作）→ 安靜結束不推 Telegram

## 🩺 健康檢查 cycle=377 2026-08-16 23:12（v4.0 安靜結束）
- Step 0: sync_coach_last_message.sh exit 0｜教練最後訊息 2026-08-16T23:07:39｜當下沉默 0.1h（週日深夜剛發言活躍）
- Step 1: SQLite 直查 cron_jobs → 24 cron 全 healthy（22 ok + 2 idle 待觸發 + 0 error / 0 個 CE≥3）
- Step 1: self cron 46e67e2e lastStatus=ok / lastDurationMs=107171ms(107s) ≪ 600s timeout / CE=0
- Step 1: model=minimax/MiniMax-M3 ✅ / timeout=600s ✅ / delivery.mode=none ✅
- Step 2: HEARTBEAT.md 90 行 (<500 警戒線) / 0 個 ⬜ 真實待辦（grep 結果皆是歷史「0 ⬜」字串）
- Step 2: healthcheck.log 45 行（<1000 警戒線，cycle=376 22:12 自動縮減歸檔生效）
- Step 2: 環境快檢 ✅ SOUL×3 齊全 (2036/20631/1851 bytes) 兩份舊版皆有「⚠️ 本檔已棄用」標記 / Repo1=112 持平 / Repo2=5 微動（皆狀態檔）/ 無 .! 鎖定檔
- Step 2: TG 通道探針本輪 23:12 實測 ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（守則#19 鐵律當下實測）
- 已知噪音（非本次新發現）：sync-* 兩個 cron (37593697/aa1ad73b) delivery fail-closed: no route，但 lastStatus=ok、CE=0，屬教練不直接依賴的內部 sync job，連續多日如此，不升級 announce
- v4.0 三關全 fail：
  - 關卡一（本輪還壞嗎）→ ❌ 否（24 cron 全 healthy + 本輪成功 + CE=0）
  - 關卡二（provider 過載嗎）→ ❌ 否（無 FailoverError 紀錄）
  - 關卡三（影響教練嗎）→ ❌ 否（教練 23:07 剛發言活躍 + 健康檢查本身正常 + 無會員功能受影響）
- → 三關皆 fail，安靜結束，未 announce 教練
- 下個 cron: 00:00 海餅乾精神背誦（in 48m）→ 06:00 起床摘要（in 6h48m）→ 07:00 ☕ 幕僚長晨報（in 7h48m）

## 🩺 軍師 Hook 自檢 2026-08-16 23:52（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: ed21277a-b31b-465c-951d-965316ab4b7f
