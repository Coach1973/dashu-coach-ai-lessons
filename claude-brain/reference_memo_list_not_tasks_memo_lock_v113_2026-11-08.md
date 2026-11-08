---
name: reference_memo_list_not_tasks_memo_lock_v113_2026-11-08
description: 教練丟「今日備忘錄／我今天要做的幾件事」＝他自己的待辦，不是交辦；小龍蝦去查資料跑25分鐘→safety-locks v1.13 備忘鎖（一輪最多4次工具）＋賈維斯卡住通知20分鐘冷卻
metadata:
  type: reference
---

11/08 15:47 教練在 LINE 丟今日備忘（5 件他自己要做的事），小龍蝦當交辦去查，一輪 25 分鐘、壓縮兩次後系統自動「Continue the current task」又跑；賈維斯「5 分鐘沒回話」通知 21 分鐘推 4 次。LINE 和 Telegram 的小龍蝦共用 `agent:main:main` 同一個對話，所以 LINE 丟的 Telegram 也在跑。

**修法（extensions/safety-locks v1.13、extensions/coach-context）**
- 備忘鎖：最新真人訊息含「備忘錄：」「我今天要做的幾件事」「今日待辦：」→ 一輪最多 4 次工具，之後擋並要它一兩句回「收到，已記下 N 件」。日誌字樣「📓 備忘清單模式」「📓🔒 備忘鎖觸發」。
- 卡住通知：同一個對話 20 分鐘內只推一次（日誌 progress-skip）。

**Why:** 教練：「我只是丟了一個今日備忘。」備忘＝記下來，等他點名才做。
**How to apply:** 以後教練說「又鬼打牆」先看日誌有沒有 📓 字樣；新的備忘說法沒被抓到就加進 MEMO_RE，不要加條文。

相關：[[reference_bots_quiet_no_exec_wake_v112_2026-11-08]]
