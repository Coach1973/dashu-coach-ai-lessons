# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-05-27 18:57
> 對話記錄已完整存入 memory/2026-05-27.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-05-27.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- Primary 模型：google/gemini-3.1-pro-preview
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成 Gemini 空白回應）

## 🔴 重大缺失記錄（2026-05-27）

**案例O：模型設定 kimi 未落地，手動切換無效，損失約 $60 USD**
- 根本原因：openclaw.json main model = kimi/kimi-k2.6，UI 切換不寫入設定檔，gateway 重啟就彈回
- 三天內無任何助教主動警告教練
- 已修復：main model → minimax/MiniMax-M2.7，gateway 重啟確認
- 已寫入失敗案例手冊案例O + top10_dynamic 排行 #0（最高優先）
- 教練原話：「60 塊美金不少錢啊」

**開工必查（本案後新增）：**
確認 main model 是否為 minimax/MiniMax-M2.7，不是就立刻修並重啟 gateway

## 學長 relay poll
### 2026-05-27 2026-05-27 21:32 - relay poll OK

