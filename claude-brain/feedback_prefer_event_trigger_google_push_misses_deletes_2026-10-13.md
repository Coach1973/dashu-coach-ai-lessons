---
name: feedback_prefer_event_trigger_google_push_misses_deletes_2026-10-13
description: 教練討厭輪詢；Google 日曆最後採「用到才現看」(ensure_fresh 60 秒)，不用通知通道；通知通道實測不通知刪除、壽命 7 天要換；接手別人輪詢先退一步問最簡單做法
metadata:
  type: feedback
---

教練 10/13 21:15「我很不喜歡這種每15分鐘就輪詢的機制」→ 我先改成 Google events.watch 通知通道＋保險＋續約（越做越複雜，教練問「每個人同步行事曆都這麼麻煩嗎？」「為什麼到現在才想到？浪費我非常多的時間」）→ 最後改成「用到才現看」。

**Why:** 執行細則 N5 事件觸發優先；但「事件」不一定要對方通知我——**使用者要用資料的那一刻**就是最好的事件（預約頁開啟／預約／巴哈報行程）。新增行程通知 <10 秒到，但刪除行程 Google 不通知（3 分鐘以上沒來）、通道只活 7 天要換，維護成本大於好處。
**How to apply:** 接手別人做好的輪詢，先退一步問「用的人需要最新資料的那一刻，我能不能當下去拿」，不要先想外部通知／webhook。實作：`coach_schedule.py ensure_fresh(60)`，`google_synced_epoch` 判斷；Google 讀不到用現有資料。教訓：我在原設計上層層疊加(通知通道→保險→續約)，教練連問三次才退一步，應該在第一次聽到「不喜歡輪詢」時就問最簡單做法。相關：[[reference_google_calendar_private_ical_for_bots_2026-10-13]]
