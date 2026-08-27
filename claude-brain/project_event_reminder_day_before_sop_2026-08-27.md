---
name: project-event-reminder-day-before-sop-2026-08-27
description: 活動前一天AI自動整理報名名單發Telegram給教練，教練再到LINE@後台手動私訊提醒(回覆訊息不扣推播額度)；已建置上線並用真實8/28嘉義場40人資料驗證成功
metadata: 
  node_type: memory
  type: project
  originSessionId: 65db632c-0f23-4fd8-aaf3-3f247ae2fd81
  modified: 2026-08-27T01:40:45.924Z
---

2026-08-27教練交辦並當場完成：學員反映報名後想在活動前收到提醒，但LINE
官方帳號後台主動推播（Push API）每月只有200則免費額度，超過要收費——教練
不想因為提醒功能燒光額度，裁示解法：活動前一天，AI把「誰報名了」的名單
告訴教練，教練自己到LINE@後台用「回覆訊息」逐一私訊提醒（1對1回覆訊息
不算進推播額度，跟主動推播Push API是LINE官方兩種不同計費機制）。

**已完成建置**：`scripts/event_reminder_day_before.py`——檢查event.db裡
「明天」有沒有場次，有就整理報名名單(姓名+電話)發Telegram給教練。刻意
重用`registration_report.py`既有的`roster()`/`_legacy_rows()`/`notify()`
函式，不重新發明比對邏輯（那支腳本已經踩過並修好「同日多場次比對」「MM/DD
格式不一致」等坑，見該檔案內建的詳細註解）。

**已用真實資料驗證**：跑當下(2026-08-27)明天正好是8/28嘉義場AI微論壇，
真實抓到40人完整報名名單(姓名+電話)並成功送達教練Telegram，不是模擬測試。

**排程機制**：`~/Library/LaunchAgents/ai.openclaw.event-reminder-day-before.plist`，
每天09:00執行一次，`launchctl print`已確認`calendarinterval`正確註冊生效。
這是「一天問一次明天有沒有活動」的日曆型檢查，教練若問「這算不算輪詢」——
不算，跟每N分鐘檢查同一個狀態不同，這是每天固定時刻檢查「明天的行事曆」，
沒有天然的事件掛鉤點可用（活動不是使用者操作觸發的，是日期本身）。

**Why**：教練持續要求「LINE官方帳號額度」相關功能都要避免不必要消耗
（見[[reference_telegram_registration_notify_group]]同類額度意識），這次
解法巧妙之處是把「提醒學員」的動作留給教練本人在LINE@後台手動做（利用
LINE官方本身「回覆不扣額度、推播才扣額度」的計費規則），AI只負責「幫教練
省下手動整理名單的時間」，兩者分工清楚。

**How to apply**：
1. 若教練回報某天沒收到提醒但確實有活動，先查`logs/event_reminder_day_before.log`
   確認LaunchAgent當天有沒有真的跑、`event.db`裡`event_date`欄位格式是否
   正確（YYYY-MM-DD），這是最容易出錯的比對點
2. 若教練希望改變提醒時間（例如改成活動前兩天、或當天早上），直接改
   plist的`StartCalendarInterval`即可，不用重寫腳本邏輯
3. 若之後教練希望AI能更進一步（例如直接生成LINE@後台可貼上的訊息草稿，
   而不只是名單），這是同一支腳本上很自然的下一步擴充點

Related: [[reference_telegram_registration_notify_group]]（LINE推播額度
意識的既有先例）、[[project_autonomy_toolkit_2026-08-24]]（報名統計等
既有自動化工具箱，這支屬於同一組工具的新成員）
