# LEARNINGS.md — 持續改進記錄

> 建立時間：2026-05-31
> 用途：每次犯錯、每次修正、每次悟到新道理，都寫在這裡
> 提升路徑：LEARNINGS.md → distill/failure-case-handbook.md → SOUL.md / AGENTS.md

---

## 2026-06-01｜自我優化檢查（22:00）

### 發現問題

**問題1：HEARTBEAT.md 模型名稱仍然過時 ✅已修復**
- HEARTBEAT.md 仍寫「google/gemini-3.1-pro-preview」
- 實際模型是「minimax/MiniMax-M2.7」（教練2026-05-25切換）
- 影響：每次心跳、教練問到模型時都會報錯
- **改進：已更新 HEARTBEAT.md 模型欄位為 minimax/MiniMax-M2.7**

**問題2：增量蒸餾抓不到實質對話（M16，🟢 活躍）**
- distill_incremental.js 跑了整天，日誌全是「NO_NEW_ENTRIES」或「已蒸餾，結束」
- 根本原因：教練使用 third-person note-taker prompt，把所有回覆變成「- System...」「- OpenClaw replied HEARTBEAT_OK」格式，「🦞 小龍蝦：」區塊的內容大量被 SKIP_PATTERNS 和 30字門檻過濾掉
- 2026-06-01 只蒸出 1 則（讀 HEARTBEAT.md），而 2026-05-31 有 39 則（格式不同）
- **方向：維持現狀，等教練有具體指示再優化蒸餾邏輯**

**問題3：memory/2026-06-01.md 已達 140KB（696行）**
- 下午 14:33 有一個 Context Overflow 自動重啟
- split_memory.sh 會在 150KB 自動分割

### 今晚攝取的教練碎碎念

掃描了以下檔案：
- `.lessons_upload/教練碎碎念.md`（v1.2, 15872 bytes, 更新至 2026-05-01）
- `distill/特助心法_教練詮釋版.md`（已完整內嵌於 SOUL.md）

主要新增理解：
1. **1.7 長時間任務預先安撫**：接到長時間任務，第一時間發安撫+進度提示，不能讓教練乾等
2. **2.6 Rate Limit vs Quota Exceeded**：429 是暫時限流（等就恢復），不能自行降級模型
3. **3.1 模型 Zero Tolerance**：寫入模型名稱前必須用 validate-models.sh 確認，不能憑記憶
4. **3.2 DOM 模式優先**：能用指令做的事絕對不用截圖，省 100 倍 token
5. **3.3 memory 檔限制**：HEARTBEAT.md 必須 < 8KB，禁止包含「讀 memory/today.md」指令

以上均已反映在 SOUL.md（鐵律三條 + 特助心法）和 top10_dynamic.md（M16）。

### 待教練確認
- 增量蒸餾優化方向是否優先？還是維持現狀，等有需要時再改？

---

## 2026-05-31｜自我優化檢查（22:00）

### 發現問題

**問題1：HEARTBEAT.md 模型資訊過時**
- HEARTBEAT.md 寫「google/gemini-3.1-pro-preview」
- 實際執行模型是「minimax/MiniMax-M2.7」（2026-05-25 教練切換）
- 影響：心跳時誤報模型狀態，造成誤判

**問題2：heartbeat-state.json 失蹤**
- 状態追蹤檔案不存在的狀態，導致心跳檢查沒有參考依據
- 原因：可能被清理或未正確初始化

**問題3：孔大哥生日（5/31）追蹤盲點**
- 系統有提醒「今天 5/31 是孔大哥生日」，但沒有確認 FB 祝賀是否執行
- 屬於「說了沒做」的變形——追蹤到但沒有闭环

### 改進動作

1. ✅ 更新 HEARTBEAT.md 模型欄位（commit hash 需補）
2. ✅ 重建 heartbeat-state.json
3. ✅ 建立 .learnings/LEARNINGS.md（本檔）

### 待觀察

- 15:25 區間迴圈攻擊（26 次 HEARTBEAT_OK）— M15 已列入 top10_dynamic.md，但根本原因尚未完全修復
- 「增量蒸餾抓不到實質行為（只抓到系統通知）」— M16 持續活躍，需要修正蒸餾邏輯的方向

---

## 2026-05-26｜增量蒸餾腳本不存在（已修復）

**問題：** cron 跑了 7 天，但 distill_incremental.js 不存在，每次都 fail
**根本原因：** cron PATH 不含 /opt/homebrew/bin，node command not found
**解法：** 修改 run_distill.sh 使用絕對路徑 `/opt/homebrew/bin/node`
**commit：** `5fc3f80d`

---

## 2026-05-25｜重複輸出亂碼

**問題：** 回覆「開新視窗」時重複輸出「教練提醒」數十次
**原因：** Context 過長導致判斷失常
**預防：** 對話超過 20 則主動建議開新視窗