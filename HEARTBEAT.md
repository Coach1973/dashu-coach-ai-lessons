# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-05-23 13:36
> 對話記錄已完整存入 memory/2026-05-23.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-05-23.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

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

---

## 心跳執行記錄

### 2026-05-23 14:05（第7次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- 檢查無新任務（shared-context 空的）
- 發現 .memsearch/memory/2026-05-23.md 和 state/session_counter.json 未 push
- 已 commit 並 push（c1b172fc）
- 待：commit .lessons_upload 或確認是否需要
- 系統正常，無需通知教練

### 2026-05-23 17:05（第10次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- shared-context 空，無新任務
- Git 乾淨（Cron 正常）
- 系統正常，無需通知教練

### 2026-05-23 18:05（第11次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- 檢查：shared-context 空，Git 有 3 個未 commit（.memsearch、session_counter、.lessons_upload）
- 已 commit + push（9e06254e）
- 系統正常，無需通知教練

### 2026-05-23 18:35（第12次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- shared-context 空，無新任務
- Git 乾淨，系統正常，無需通知教練

### 2026-05-23 16:05（第9次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- shared-context 空，無新任務
- Git 乾淨（Cron 正常）
- 系統正常，無需通知教練

### 2026-05-23 19:35（第12次心跳）
- 身份：2號機，小龍蝦學弟，服務孔大哥
- shared-context 空，無新任務
- Git 有 3 個未 commit 已 commit + push（71129a9c）
- 系統正常，無需通知教練

### 2026-05-23 19:05（目標心跳）
- 身份：1號機，小龍蝦學長，服務大樹教練
- 發現 .memsearch/memory/2026-05-23.md 和 state/session_counter.json 未 push
- 已 commit（35519f27）並 push origin/main
- Git 狀態：乾淨
- 系統正常，無需通知教練
