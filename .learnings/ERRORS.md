# 錯誤記錄

## 2026-05-26 04:05 - cron 環境變數導致 node not found

**症狀：** distill 增量蒸餾 cron 每次執行都失敗，日誌顯示 `node: command not found`

**原因：** cron 的 PATH 不包含 /opt/homebrew/bin，導致 shell wrapper 找不到 node

**解法：**
1. 修改 run_distill.sh 使用絕對路徑：/opt/homebrew/bin/node
2. 立即驗證：執行一次確認能跑
3. commit `5fc3f80d`

**預防：** 未來任何 cron wrapper 腳本一律使用絕對路徑，不依賴 PATH

**延伸修復：**
- `sync_handoff_to_claudemd.sh` 同樣有 `python3` 相對路徑問題，已修正為 `/opt/homebrew/bin/python3`，commit `f42a9374`

---

## 2026-05-25 21:27 - 重複輸出亂碼

**症狀：** 回覆「開新視窗」時，重複輸出「教練提醒」數十次，導致訊息異常膨脹。

**原因：**
- Context 過長導致判斷失常
- 沒有自我檢查機制

**解法：**
1. 輸出前強制檢查重複性
2. 發現異常立即停機並請教練開新視窗
3. 對話長度超過 20 則主動建議開新視窗

**教練反應：** 「有點無法接受」- 這是嚴重警告，必須立即改善。

---

## [ERR-20260605-001] memory_search 報錯

**Logged**: 2026-06-05T04:25:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### 症狀
- 呼叫 `memory_search` 工具時回傳：
  ```
  Unknown memory embedding provider: google
  Memory search is unavailable due to an embedding/provider error.
  ```
- `memory_get` 仍可正常運作（直接讀檔案不需要 embedding）

### 影響
- 無法用「語意搜尋」找記憶，要靠：
  1. `memory_get` 精確讀檔
  2. `find` / `grep` 搜檔名或內容
  3. `cat` 直接看

### 暫行處置
- 已記進 LRN-20260605-001：未來主工具壞了，先試備援不要直接放棄
- 修復需動 `openclaw.json` 的 embedding provider 設定（未授權前不動）

### 教練指示
- 「禁止未授權修改 openclaw.json」鐵律（MEMORY）
- 等教練明確下令才修

### Metadata
- Reproducible: yes
- Tags: memory_search, embedding, openclaw_config
- See Also: LRN-20260605-001

