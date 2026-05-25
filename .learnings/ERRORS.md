# 錯誤記錄

## 2026-05-26 04:05 - cron 環境變數導致 node not found

**症狀：** distill 增量蒸餾 cron 每次執行都失敗，日誌顯示 `node: command not found`

**原因：** cron 的 PATH 不包含 /opt/homebrew/bin，導致 shell wrapper 找不到 node

**解法：**
1. 修改 run_distill.sh 使用絕對路徑：/opt/homebrew/bin/node
2. 立即驗證：執行一次確認能跑
3. commit `5fc3f80d`

**預防：** 未來任何 cron wrapper 腳本一律使用絕對路徑，不依賴 PATH

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
