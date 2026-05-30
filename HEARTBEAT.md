# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-05-30 05:31
> 對話記錄已完整存入 memory/2026-05-30.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-05-30.md 可能超過 50KB，讀了會造成 Gemini 空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M2.7（已驗證 2026-05-30）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成 Gemini 空白回應）

## 🔴 Netlify 部署鐵律（2026-05-30 教練親定，全體強制）
- 每次部署扣 15 點，帳號已超用，6/25 歸零
- 未經教練親眼確認 ❌ 禁止推送
- 流程：本機改好 → 開瀏覽器給教練看 → 教練說「推」→ 一次推送
- 禁止 git push 部署、禁止推完再看、禁止連續推修小問題
- 違反 = 守則 #03 + #08 雙重違規

## 📌 心跳狀態（每次寫入，降低 token burn）
🦞 健康檢查報告（18:30）

✅ Git 自動備份：53c6eef2
✅ Cron 15 項全綠燈，無錯誤
✅ Model：MiniMax M2.7
✅ 蒸餾系統：pending_distill 有6個檔案（已新增 9e989647）
✅ relay poll OK（無新任務）
✅ shared-relay 已讀取

📌 待追蹤：蒸餾系統 67 個未完成（接力棒最高優先）
📌 待追蹤：守則故事庫品管（MiniMax 任務5個檔在 knowledges/）
📌 待追蹤：relay_poll.py UnicodeDecodeError

2026-05-30 18:30 ✅ 心跳正常，Git 53c6eef2，Cron 15/15 全綠燈

---

🦞 健康檢查報告（14:02）

✅ Git 自動備份：59017354
✅ Cron 14 項全綠燈，無錯誤（30分鐘健康檢查 running 是正常狀態）
✅ Model：MiniMax M2.7
✅ 無異常

⚠️ 犯錯記錄：distill_incremental.js 今日連續 3 次未執行
→ 根本原因：心跳任務每次都讀開工鐵律五步驟，無法安靜執行 cron 指令
→ 修復方向：改為純 cron 獨立執行，不綁心跳

⚠️ 待修：relay_poll.py UnicodeDecodeError（line 30）

## 學長 relay poll
### 2026-05-30 2026-05-30 22:04 - relay poll OK

