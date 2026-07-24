# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-24 07:38
> 對話記錄已完整存入 memory/2026-07-24.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-24.md 可能超過 50KB，讀了會造成模型空白回應）

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

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-24 08:10
- ✅ 同步成功
- HANDOFF mtime: 1784851600
- 雲端同步：✅ 已推上雲端（commit d9de79dec）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-24 08:20
- ✅ 同步成功
- HANDOFF mtime: 1784852410
- 雲端同步：✅ 已推上雲端（commit 3fca2b074）

## 🩺 軍師 Hook 自檢 2026-07-24 08:24（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：OK，我想給你一個原則性的指�
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 2aedf319-34ef-4bb3-8704-d568dda3a347

## 🔄 執行細則.md→~/.claude/CLAUDE.md 自動同步 2026-07-24 08:27
- ✅ 同步成功
- SOURCE mtime: 1784852829

## 🩺 健康檢查 2026-07-24 08:32（Asia/Taipei）

**全系統 cron 狀態（main agent scope）：**
- 只有 1 個任務：🦞 每30分鐘任務健康檢查（就是本任務）
- consecutiveErrors = **1**
- lastErrorReason = `timeout`（LLM idle timeout，**與過去 110h 的 `overloaded` 不同**）
- lastDurationMs = **127.5s** ≪ 600s timeout ✅（不是 timeoutSeconds 設定問題）
- 08:00 fire 失敗 → 08:03 retry 成功 → 08:30 fire 又失敗（alternating 模式繼續）

**配置審查：**
- `model=minimax/MiniMax-M3` ✅
- `timeoutSeconds=600` ✅
- 無 apiKey/auth 錯誤

**自動修復評估（全不適用）：**
- ❌ timeout 錯誤 → 127.5s ≪ 600s（不是 timeout 設定太短）
- ❌ INVALID_API_KEY → model 已是 minimax/MiniMax-M3
- ❌ scp/ssh VPS → 無此類任務
- ❌ CE ≥ 3 → CE=1，未達紅線

**HEARTBEAT.md ⬜ 待自動化：**
- 無

**結論：** ✅ 安靜結束，不通知教練
- alternating fail/recover 模式延續（已逾 110h+）
- 錯誤從 `overloaded` 轉為 `timeout`，但本質都是 provider 端臨時性問題
- 127.5s 遠低於 600s timeout，配置完全正確
- CE=1 未達紅線 3

⚠️ 警戒：若 09:00 fire 失敗 → CE=2；09:30 再失敗 → CE=3 紅線 → 必須 announce 通知教練。

下次 09:00 cron fire 自動驗證。

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-24 08:40
- ✅ 同步成功
- HANDOFF mtime: 1784853366
- 雲端同步：✅ 已推上雲端（commit f22cd214e）
