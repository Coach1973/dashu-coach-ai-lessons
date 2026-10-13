---
name: feedback_prefer_event_trigger_google_push_misses_deletes_2026-10-13
description: 教練討厭每15分鐘輪詢；Google日曆改用 events.watch 即時通知(新增<10秒)，但實測刪除不會通知，所以留每3小時保險＋每天續約
metadata:
  type: feedback
---

教練 10/13 21:15：「我很不喜歡這種每15分鐘就輪詢的機制，你確定要這麼做嗎？」→ 輪詢的理由(「Google 沒程式介面無法即時通知」)其實不成立，是接手時沿用沒重新檢討。

**Why:** 執行細則 N5：事件觸發優先，能觸發就別輪詢。
**How to apply:** 接手別人的輪詢排程先問「這件事發生當下能不能直接觸發」。Google Calendar：`scripts/gcal_watch.py`(start/renew/status/stop)＋`event-signup` 的 `/hooks/gcal-push`；不需先驗證網域；通道最長 7 天要續。**實測新增行程 <10 秒到、刪除行程 3 分鐘以上沒通知**——所以仍留一個每 3 小時的保險核對(cron b2a3dd9b)，並向教練講清楚「一天跑 8 次、只是防漏」。相關：[[reference_google_calendar_private_ical_for_bots_2026-10-13]]
