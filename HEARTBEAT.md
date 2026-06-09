# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-06-09 11:06
> 對話記錄已完整存入 memory/2026-06-09.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-06-09.md 可能超過 50KB，讀了會造成模型空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## 🛠 2026-06-09 12:24 軍師治本紀錄（給下一棒）
- `auto-fix-session-lock.sh` 兩坑已治本（commit `de2ff04`）
  - 門檻 500KB → 5MB（之前太低，每 2 分鐘誤殺 gateway）
  - `do_clear_sessions` 加 `glob *.trajectory.jsonl`（之前只刪 sessions.json 的 sessionFile 小檔，大檔沒清 → 死循環）
- RustDesk 門檻 600MB → 1024MB（commit `cebb72a`）
- v2.4 圓桌會議實測通過：三隻機都回應、議程順序生效（學長→學妹→學弟）、互相聽得到（學弟引用 H 過往答案）
- 下一場待修：bot-relay handler.js `botId` 還標 unknown（agentId 取錯欄位），看內容能辨識三隻機但 BOT_MESSAGES.md 統計失準

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 學長 relay poll
### 2026-06-09 2026-06-09 12:14 - relay poll OK

