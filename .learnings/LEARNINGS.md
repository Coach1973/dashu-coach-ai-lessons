# LEARNINGS.md — 持續改進記錄

> 建立時間：2026-05-31
> 用途：每次犯錯、每次修正、每次悟到新道理，都寫在這裡
> 提升路徑：LEARNINGS.md → distill/failure-case-handbook.md → SOUL.md / AGENTS.md

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
- 「增量蒸餾只抓到系統通知」— M16 持續活躍，需要修正蒸餾邏輯的方向

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