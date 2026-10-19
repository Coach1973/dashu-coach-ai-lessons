---
name: feedback-interview-30min-buffer-between-sessions-2026-10-19
description: 教練10/19定：訪談每兩場之間留30分鐘緩衝（19:00/20:30/22:00）；週四19:30起；預約頁與 LINE 兩套算法要一起改；順手查到預約頁 JS 語法錯誤（\n）讓點時段沒反應
metadata:
  type: feedback
---

教練 2026-10-19 11:04 原話重點：「7 點訪談到 8 點、8 點又立刻下一場，聊到 8 點 5 分下一位已上線，沒時間喝水、上廁所、暖場，不合理」→ **只要有訪談，每兩場之間必須留半小時**：7:00–8:00／8:30–9:30／10:00–11:00（晚上可約到 23:00）；週四因 17:30–19:00 BNI 線上會議，從 19:30 起（19:30／21:00），其他天 19:00 起。要求「到年底之前所有可預約時段都調好」。接 [[reference_booking_page_thursday_slots_2026-10-15]]。

**做法**（commit 見接力棒）：預約頁每個空檔改「每 90 分鐘一個起點」；已有訪談（kind=interview／guest／標題有訪談，**每週固定行程不算**，不然週四那列「休息（訪談間隔）」會被再加一圈）前後各留 30 分；白天最後一場要在晚上開始前留 30 分；`evening_window.end` 22:00→23:00。規則寫在程式，不是逐日存，所以自動涵蓋到年底（預約頁一次只顯示 28 天）。

**Why**：訪談節目不是排滿的門診，主持人要休息、暖場。**How to apply**：
- 預約頁 `event-signup/coach_schedule_view.py` 與 LINE／小龍蝦用的 `scripts/coach_schedule.py`（`open-slots`、`check`、`daily-report`）是**兩份各自一套算法**，改規則兩邊一起改；`event-signup/test_coach_schedule_buffer.py` 用真實行程總表逐日（到 12/31）比對兩邊必須一致，改完先跑 `cd event-signup && ./venv/bin/python test_coach_schedule_buffer.py`。
- 改 event-signup 程式要 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp` 才生效。
- 已排定但間隔不足 30 分的既有訪談（10/20 的 18:00／19:00（待確認）／20:00；10/27 的 18:00／19:00／20:00）**我沒動**，是否調整由教練決定。
- 🔴 **網頁輸出的 JavaScript 裡的 `\n` 在 Python f-string 要寫 `\\n`**：10/13 加「取消」鈕時沒注意，整支腳本語法錯誤，預約頁點時段完全沒反應，直到 10/19 才被真瀏覽器點擊發現。改這種頁面一定要在真瀏覽器真的點一次，測試檔已加 `node --check`。
