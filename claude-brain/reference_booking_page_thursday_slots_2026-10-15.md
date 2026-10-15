---
name: reference_booking_page_thursday_slots_2026-10-15
description: 預約頁（event.bymyway.com/schedule/<代碼>/）週四規則：19:30–20:30、21:00–22:00 可約；暖身/休息緩衝、線上聚會/學習訪談優先（程式用名稱判斷）；改程式要重啟 event-webapp 才生效（10/16 02:32 已重啟驗證）
metadata:
  node_type: memory
  type: reference
  originSessionId: 4aac7f25-d657-43c8-a422-e28fd94a634d
  modified: 2026-10-15T18:36:11.261Z
---

2026-10-15 教練要求週四時段改 7:30–8:30、9:00–10:00（原因：週四分享會 19:00 結束要暖身；中間休息30分），線上聚會／線上學習保留但「有訪談就以訪談優先」。commit `5e8a76d61`。

- 預約頁空檔＝行程總表忙碌時段推算，每個空檔每小時一個起點（`coach_schedule_view._free/_starts`）。要在 19:30 起算，只能加「緩衝」行程：總表 recurring 新增 `thu-warm`（週四 19:00–19:30 暖身）、`thu-rest`（20:30–21:00 休息），自 10/22 起到 12/31。
- 週四「線上」開頭的行程（線上學習／線上聚）不擋預約：`_yield_if_online(item, d)` 在 `_busy` 裡依「週四＋標題以線上開頭」打 `yield` 旗標。**不能把旗標寫進總表資料**：Google 同步（`sync_google`）每次整批重建「來源＝Google日曆」的一次性行程，旗標會被蓋掉；固定規則（recurring）倒是不會被重建，但 Google 版是一次性行程，所以只有程式判斷最穩。
- 生效條件：資料（JSON）每次請求都重讀，Mac 拉到就生效；**程式要重啟 launchd 的 `com.coach.event-webapp`** 才會載入新版。10/16 01:55 實測：線上已有 19:30、暖身、休息，但 10/22 沒有 21:00＝程式還沒重啟（已寫信給 Mac 軍師）。
- ✅ **10/16 02:32 Mac 已重啟並驗證完成**（`launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`，新 PID 5382）：本機與公開網址 10/22、10/29 晚上＝19:30＋21:00；10/21 晚上仍只有 18:00、10/23 仍 19:00＋18:00（其他星期不變）。**Mac 端驗證法**：代碼存 `workspace/state/coach_schedule_token.txt`（別貼進對話／commit）；`curl http://localhost:5060/schedule/<代碼>/` 存檔，用 regex `data-d="2026-10-22" data-t="(\d\d:\d\d)"` 抽時段。重啟前先量一次基準，才能證明是重啟造成的差異。
- 預約頁網站跑在 Mac（port 5060），Windows 不能遠端重啟；改 `event-signup/*.py` 都要請 Mac 重啟。
- 測試法：Windows 沒有 fcntl，無法 import 該模組；用 ast 抽出 `_hm/_fmt/_busy/_free/_starts/_yield_if_online` 函式 exec 後套真資料算。
