# HANDOFF.md — 助教交接檔案
> 這個檔案是 Claude 助教（桌面版）與終端機助教（API版）之間的工作接力棒。
> 每次開始工作前必讀，每次工作有進展時更新。

---

## 當前狀態（2026-04-19 上午 11:00 更新）

**原因：** Claude API 服務今晚不穩定，Bash 工具持續被安全分類器擋住，終端機助教無法執行任何 SSH 指令。
**結果：** VPS 相關任務全部暫停，等明天服務恢復後繼續。

---

## 待完成任務（按優先順序）

- [ ] **任務一：VPS SOUL.md 防幻覺鐵律**
  - 任務檔：`~/Desktop/vps_soul_fix_task_v2.md`
  - 說明：在 VPS SOUL.md 末尾追加海餅乾三大信念與十大守則的硬編碼鎖定鐵律
  - 注意：原版 `vps_soul_fix_task.md` 會卡死（SSH 未帶密碼），**必須用 v2 版**

- [ ] **任務二：記憶蒸餾系統升級**
  - 任務檔：`~/Desktop/vps_memory_distill_task.md`
  - 說明：安裝 client-memory hook + 每2小時增量蒸餾 cron job，解決 context overflow 後資訊遺失的問題
  - 注意：先確認 `~/Desktop/HANDOFF_VPS_Memory.md` 的第一版是否已安裝，再跑升級版

- [ ] **任務三：NotebookLM 雙向搬家**
  - 任務檔：`~/Desktop/migration_task.md`
  - 說明：把錯誤帳號的筆記本互相搬移（只複製，不刪除）

---

## 三助教分工

| 助教 | 工具 | 職責 |
|------|------|------|
| 小龍蝦助教 | Gemini Pro（VPS Telegram） | 統籌規劃、記錄、發想 |
| Claude 助教 | Claude Pro 桌面版（Mac mini） | 可行性評估、審核、設計方案 |
| 終端機助教 | Claude API（Mac mini 終端機） | 實際執行指令、跑程式 |

---

## VPS 關鍵資訊

- IP：43.245.60.200
- 密碼：9kdxvQN2
- SSH 標準指令：`sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200`
- Telegram Bot：@coach_bymyway_bot
- 模型：MiniMax M2.7

---

## 明天啟動方式

終端機助教明天服務恢復後，直接貼：
```
讀取 ~/Desktop/HANDOFF.md，從「待完成任務」的第一個未完成項目開始執行。
```
