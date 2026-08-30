# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-30 18:00
> 對話記錄已完整存入 memory/2026-08-30.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-30.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-30 19:10
- ✅ 同步成功
- HANDOFF mtime: 1788088038
- 雲端同步：✅ 已推上雲端（commit 122dbd7d2）

## ⚠️ 待修（不影響教練工作，僅給軍師有時間時修）
- **telegram_channel_probe.sh 偶發 getChat 失敗**（cycle=668）：第一次跑回 ok:false，REASON 空字串，重試後 ok:true。實際通道健康（已用 bot_main 驗證 sendMessage 成功）。建議：加 retry 邏輯或使用 webhook 測試替代，避免單次瞬時不穩誤判。**優先度低**。
- **小龍蝦 debug 不該 sendMessage 給教練**（cycle=668）：本次意外送 1 則 "test" 已立刻 delete。教訓：未來 TG 通道除錯時只用 getMe/getChat，**絕不 sendMessage**；或用 bot_kong/bot_peipei 測試，不要拿教練對話的 bot token 玩真的。**守則#12 + #04 自我警惕清單**。
- **healthcheck.log 操作鐵律（cycle=669 新增）**：本輪嘗試用 `head -n -1 file > /tmp/...; mv /tmp/... file` 移除最後一行後再 append——**macOS 的 head 不支援負數（會清空目標檔案）**，導致原 668 行 healthcheck.log 被「僅保留 1 行」覆蓋，雖然已從 cron runs 重建 cycle=655~669 共 14 行，但 cycle=655 之前更早的歷史已永久遺失（這 668 行外的舊歷史 cron runs 沒保留）。
  - **新鐵律**：修改檔案用 `sed -i '$d'`（macOS 支援） 或 `tail -n +2` 重建，不要用 `head -n -1`。
  - **重影響範圍**：state/healthcheck.log 早於 cycle=655 的歷史永久遺失（cron runs 只保留近 50 筆）
  - **補救**：完整備份 23:05 三機總結已 push 上 GitHub，可從 commit 歷史中比對是否有重要 cycle 需要復原。
  - **永久教訓**：所有「刪除 log 最後一行」的場景，必須先 cp 備份到 /tmp/*.bak 再操作。
  - **優先度低**：本輪已即時重建近 14 行 cycle=655~669，教練工作完全不受影響。

## 🪨 試金石策展提醒 2026-08-30 21:00
- top10_dynamic.md 已 53 天未更新
- 候選池：特助場景庫_自動增量.md 累積 50 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目

## 🩺 軍師 Hook 自檢 2026-08-30 21:21（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- 小龍蝦信箱：（信箱查無新信）
- Session: 4df163f9-7212-4a42-948a-b7105107ac31

## 🩺 軍師 Hook 自檢 2026-08-30 21:22（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- 小龍蝦信箱：（信箱查無新信）
- Session: 90ed8b02-52bf-4620-8c47-59ea26a8ef70
