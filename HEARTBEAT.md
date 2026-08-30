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
