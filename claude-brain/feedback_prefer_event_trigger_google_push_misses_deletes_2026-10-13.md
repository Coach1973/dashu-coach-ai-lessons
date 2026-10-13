---
name: feedback_prefer_event_trigger_google_push_misses_deletes_2026-10-13
description: 教練討厭輪詢；Google 日曆最後採「用到才現看」(ensure_fresh 60 秒)，不用通知通道；通知通道實測不通知刪除、壽命 7 天要換；接手別人輪詢先退一步問最簡單做法
metadata:
  type: feedback
---

【回顧，已不存在】10/13 晚一度走過彎路，這些全部已拆除，現況沒有任何 Google 相關定時工作：當時教練 21:15 說不喜歡輪詢，我先做了 Google 通知通道、保險核對、續約三層零件，教練連問「每個人同步行事曆都這麼麻煩嗎？」「為什麼到現在才想到？」之後，才退一步改成現在的「用到才現看」。

**Why:** 執行細則 N5 事件觸發優先；但「事件」不一定要對方通知我——**使用者要用資料的那一刻**就是最好的事件（預約頁開啟／預約／巴哈報行程）。新增行程通知 <10 秒到，但刪除行程 Google 不通知（3 分鐘以上沒來）、通道只活 7 天要換，維護成本大於好處。
**How to apply:** 接手別人做好的輪詢，先退一步問「用的人需要最新資料的那一刻，我能不能當下去拿」，不要先想外部通知／webhook。實作：`coach_schedule.py ensure_fresh(60)`，`google_synced_epoch` 判斷；Google 讀不到用現有資料。教訓：我在原設計上層層疊加(通知通道→保險→續約)，教練連問三次才退一步，應該在第一次聽到「不喜歡輪詢」時就問最簡單做法。相關：[[reference_google_calendar_private_ical_for_bots_2026-10-13]]
