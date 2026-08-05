# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-05 09:38
> 對話記錄已完整存入 memory/2026-08-05.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-05.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 09:40
- ✅ 同步成功
- HANDOFF mtime: 1785894038
- 雲端同步：✅ 已推上雲端（commit abbe61b45）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 09:41
- ✅ 同步成功
- HANDOFF mtime: 1785894050
- 雲端同步：✅ 已推上雲端（commit 6d65d6baf）

## 🩺 軍師 Hook 自檢 2026-08-05 09:49（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: d8379d77-adf5-400e-83ab-3a764cb45d47

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 09:55
- ✅ 同步成功
- HANDOFF mtime: 1785894941
- 雲端同步：✅ 已推上雲端（commit 05403a907）

## 🩺 10:00 心跳 → 重啟通知送出（2026-08-05 10:00）
- ✅ Telegram messageId 9322 已送達（curl bypass，chat 6124913915）
- 內容：🦞 教練好，我是小龍蝦。剛剛 09:38 對話記錄已滿，已自動重啟，請繼續下指令。雲端交接棒已同步到最新，沒有遺漏。
- 守則#19 探針：Telegram 通道剛剛已實際送達 OK（不沿用舊旗標）
- Coach silent since 2026-08-03 13:54 = 44.1h+（仍待覆）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 10:00
- ✅ 同步成功
- HANDOFF mtime: 1785894976
- 雲端同步：✅ 已推上雲端（commit 9ed695820）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 10:15
- ✅ 同步成功
- HANDOFF mtime: 1785895848
- 雲端同步：✅ 已推上雲端（commit aa7c346e4）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 10:25
- ✅ 同步成功
- HANDOFF mtime: 1785896500
- 雲端同步：✅ 已推上雲端（commit 2eb96b8e7）

## 🔴 健康檢查告警 2026-08-05 10:34（SOP 規則 #4 觸發）
- **consecutiveErrors = 5**（≥3 紅線）—— alternating 1300+ 場穩定以來首次連錯 5 場
- 連錯時序：08:00 ❌ → 09:00 ❌ → 09:30 ❌（retry ×3）→ 10:00 ❌ → 10:30 ❌
- 根因：`FailoverError: AI service temporarily overloaded`（minimax provider 端）
- 自動修復 4 條規則判定：#1 #2 #3 皆不適用、#4 ✅ 已觸發教練通知
- ✅ Telegram messageId 9323 已送出（announce 教練）
- 教練最後訊息 2026-08-03 13:54，沉默 44.7 小時
- HEARTBEAT.md 無 ⬜ 待辦項
- 本輪 run 正在處理中（產出本段紀錄），預期稍晚 state 會把 CE 重置為 0
- 不 commit/push（每日 23:05 三機總結統一做）

## 🩺 10:37 心跳探針（守則 #19 通道健康鐵律實測）
- ✅ Telegram 通道探針回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（不沿用舊旗標）
- Cron 狀態檢查：36 個任務，僅 2 個 lastRunStatus=error
  - `001a9b16` LINE@每日兩次（8/3 10:00 fail：`reply to 1, thread 1` failed，message tool 推播層錯誤）
  - `bbb7a348` 小龍蝦每日三機總結（8/3 23:07 fail：`reply to 1, thread 0` failed；8/2 23:06 fail：同型）
  - **判定**：非連續錯誤（任務本體 AI 跑完、commit push 成功，僅 Telegram 推播失敗），不觸發 SOP 規則 #4
  - **後續**：8/3 與 8/2 三機總結實際已完成並推送雲端（commit hash 見 cron runs summary），但教練未收到 Telegram 通知 → 下次教練上線主動提醒補看 `distill/三機每日總結_2026-08-03.md` 與 `2026-08-02.md`
- 距上次主動通知（10:34 messageId 9323）僅 3 分鐘 → 不再打擾教練
- 教練最後訊息 2026-08-03 13:54，沉默 44.7+ 小時（仍待覆，靜默中合理）
- **結論**：HEARTBEAT_OK，不送通知

## 🩺 11:07 心跳探針（守則 #19 通道健康鐵律實測）
- ✅ Telegram 通道探針回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（不沿用舊旗標）
- Cron 狀態檢查：36 個任務，狀態同 10:37（無新變化）— 仍只 2 個 error 為歷史 message tool 推播失敗，非連續錯誤
- 距上次主動通知（10:34 messageId 9323）32 分鐘，告警性質（健康檢查 CE=5）→ 再發關懷會顯打擾
- 教練最後訊息 2026-08-03 13:54，沉默 45.2+ 小時（仍待覆）
- 下次主動關懷時點：14:00 的「每4小時主動關懷」cron（距上次通知 3.5 小時，更合適）
- **結論**：HEARTBEAT_OK，不送通知，等 14:00 自動關懷

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 10:45
- ✅ 同步成功
- HANDOFF mtime: 1785897853
- 雲端同步：✅ 已推上雲端（commit f0d6cc5d7）

## 🩺 10:51 健康檢查（v4.0 SOP 三關判定）
- 第零步 ✅ sync_coach_last_message.sh → 教練沉默 45.0h（2026-08-03 13:54 起）
- 第一步 → Cron runs latest：本任務自身 ts=1785897444087 已 status=ok（產出 10:34 那份完整報告）；本輪 run 也正在產出本段文字
- 過往連錯（08:00/09:00/09:30/10:00/10:30）皆 `FailoverError: AI service temporarily overloaded`
- **v4.0 SOP 三關判定**：
  - 關卡一（現在還壞嗎）：❌**已恢復**（本輪 AI 正常回應 = 鐵證）
  - 關卡二（provider 暫時過載）：❌**正是**，100% minimax provider 端暫時塞車
  - 關卡三（影響教練工作）：❌**無**——只是「健康檢查機器人自己在打嗝」的 meta 失敗，不影響任何會員/LINE/行事曆功能
- 三關全未通過（至少有兩關是「已恢復/provider transient」）→ 結論：**不安靜 announce，不修正任何 cron 配置**
- 10:34 messageId 9323 是 v3.0 規則下發出的，v4.0 不會再發；現在 CE 已自然歸 0
- HEARTBEAT.md ⬜ 無待辦，不 commit/push（每日 23:05 統一做）
- 教練沉默 45h（週日最後發言，今週三正常作息不主動打擾）
- ✅ `delivery.mode=none` 安靜處理

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 10:55
- ✅ 同步成功
- HANDOFF mtime: 1785898426
- 雲端同步：✅ 已推上雲端（commit bb85c91e7）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-08-05 11:00
- ✅ 同步成功
- HANDOFF mtime: 1785898679
- 雲端同步：✅ 已推上雲端（commit 4e96c96f7）

## 🩺 11:03 健康檢查（v4.0 SOP 三關判定）
- 第零步 ✅ sync_coach_last_message.sh → 教練沉默 45.2h（2026-08-03 13:54 起）
- 第一步 → Cron runs latest：
  - 11:00 fire (ts=1785898963608)：❌ `FailoverError: AI service temporarily overloaded`（163.5s ≪ 600s）
  - 10:51 fire (ts=1785898405096)：✅ ok（上一輪）
  - 10:34 retry (ts=1785897444087)：✅ ok
- 時間軸：08:00 ❌ → 09:00 ❌ → 09:30 ❌（×3 retry）→ 10:00 ❌ → 10:30 ❌ → 10:34 ✅ → 10:51 ✅ → 11:00 ❌ → 11:03 ✅（本輪）
- CE = 1（上一輪成功重置 → 本輪失敗 = 1，未達 ≥3 紅線）
- **v4.0 SOP 三關判定**：
  - 關卡一（本輪還壞嗎）：❌ **已恢復**（本輪 AI 正常回應 = 鐵證）
  - 關卡二（provider transient）：❌ **正是**（100% minimax `FailoverError`）
  - 關卡三（影響教練工作）：❌ **無**（健康檢查機器人自我打嗝的 meta 失敗，不影響 LINE/行事曆/會員功能）
- 三關全未通過 ⇒ **不 announce 教練，不修任何 cron 配置**
- 全系統仍只剩 1 個任務（本任務本身，符合 2026-07-05 教練精簡退場設計）
- 自動修復 4 條規則全部 ❌ 不適用：#1 timeout 充裕（163s ≪ 600s）｜#2 無 VPS 任務｜#3 model 已是 minimax/MiniMax-M3｜#4 CE=1 未達紅線
- HEARTBEAT.md ⬜ 無待辦，不 commit/push（每日 23:05 統一做）
- 教練沉默 45.2h（週三上午，正常作息，靜默中合理）
- ✅ `delivery.mode=none` 安靜處理

## 🩺 軍師 Hook 自檢 2026-08-05 11:15（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: 4e96c96f7）
- Session: 15b04168-3c44-43e6-8fb2-0be2ad93871b

## 🩺 11:33 健康檢查（v4.0 SOP 三關判定）
- 第零步 ✅ sync_coach_last_message.sh → 教練沉默 **45.7h**（2026-08-03 13:54 起，當下 `date` 算的新鮮值）
- 第一步 → Cron runs latest：
  - 11:30 fire (ts=1785900763258)：❌ `FailoverError: AI service temporarily overloaded`（163.2s ≪ 600s）
  - 11:03 fire (ts=1785899054845)：✅ ok（上一輪成功，產出完整報告）
  - 11:00 fire (ts=1785898963608)：❌ 同型 overloaded
- 時間軸：08:00 ❌ → 09:00 ❌ → 09:30 ❌（×3 retry）→ 10:00 ❌ → 10:30 ❌ → 10:34 ✅ → 10:51 ✅ → 11:00 ❌ → 11:03 ✅ → 11:30 ❌ → 11:33 ✅（本輪）
- CE = **1**（11:03 成功重置 → 11:30 失敗 = 1，未達 ≥3 紅線）
- **v4.0 SOP 三關判定**：
  - 關卡一（本輪還壞嗎）：❌ **已恢復**（本輪 AI 正常回應 = 鐵證）
  - 關卡二（provider transient）：❌ **正是**（100% minimax `FailoverError`）
  - 關卡三（影響教練工作）：❌ **無**（健康檢查機器人自我打嗝的 meta 失敗，不影響 LINE/行事曆/會員功能）
- 三關全未通過 ⇒ **不 announce 教練，不修任何 cron 配置**
- 全系統仍只剩 1 個任務（本任務本身，符合 2026-07-05 教練精簡退場設計）
- 自動修復 4 條規則全部 ❌ 不適用：#1 timeout 充裕（163s ≪ 600s）｜#2 無 VPS 任務｜#3 model 已是 minimax/MiniMax-M3｜#4 CE=1 未達紅線
- HEARTBEAT.md ⬜ 無待辦，不 commit/push（每日 23:05 統一做）
- 教練沉默 45.7h（週三上午，正常作息，靜默中合理）
- ✅ `delivery.mode=none` 安靜處理
