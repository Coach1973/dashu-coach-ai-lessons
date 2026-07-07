---
name: feedback-time-lock-hook-false-positive-fix
description: rule_taiwan_time_check.sh 上線首次真實對話就誤報，根因是把系統信封時間戳/自動注入提醒教材當成「AI讀過的UTC資料」
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2989d377-322b-4a22-a511-60d11dcf12e3
---

時間鎖 Stop hook（`scripts/rule_taiwan_time_check.sh`）上線後第一次在真實對話中誤報：軍師回覆「不客氣，教練！」零時鐘數字，仍被判定違規。

**根因**：舊版判斷「這輪有沒有碰過 UTC timestamp」時，直接掃整段 raw JSONL，但（1）每個對話事件自己的信封 `timestamp` 欄位本身就是 UTC 格式，永遠命中；（2）系統每輪自動注入的「時間鐵律提醒」文字裡寫死了一個教材範例 `2026-06-09T06:25:36.752Z`，也永遠命中。兩者都不是 AI 真正處理的外部資料。

**修法**：改成只抓對話「內容文字」（message/tool_result 的 text 欄位），排除信封層 `timestamp` key，並排除 `type=="attachment"` 的自動注入提醒事件。修完後 8/8 原始回歸測試全過，兩個真實觸發過的對話輪重新模擬也都改回不誤判。

**Why**：機關的價值在於「真的抓到問題」，如果連自己的教材範例都會誤觸發，之後每一輪都會被迫檢查，等於機關失能又擾民。

**How to apply**：往後任何用「grep 整段 JSONL」判斷「AI有沒有處理過某類資料」的 hook，都要注意信封欄位（timestamp/sessionId等）跟系統自動注入的 attachment/reminder 內容會污染判斷，只掃真正的訊息內容文字。

關聯：[[feedback_taiwan_time_always]]、試金石案例38（本機關的誕生案例）
