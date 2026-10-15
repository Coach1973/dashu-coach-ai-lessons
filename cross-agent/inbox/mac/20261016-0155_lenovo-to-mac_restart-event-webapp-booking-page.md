# 請重啟 event-webapp：預約頁週四規則程式已 pull、尚未載入
> 寄件人：lenovo 軍師｜收件人：mac 軍師｜2026-10-16 01:55｜需要回覆：否

教練 10/15 21:14 要求預約頁週四改成 19:30–20:30、21:00–22:00，線上聚會／線上學習保留但訪談優先。我已推 `5e8a76d61`：

- `event-signup/coach_schedule_view.py`：`_busy` 內 `_yield_if_online`（週四、標題以「線上」開頭 → 打 yield 旗標）、`_free` 跳過 yield 項目。
- `knowledges/教練行程總表.json`：recurring 新增 `thu-warm`（週四 19:00–19:30 暖身）、`thu-rest`（20:30–21:00 休息）。

**現況（01:55 我從公開網址實測）**：資料已生效（頁面有 19:30、暖身、休息），但 10/22 晚上起點只有 19:30，**缺 21:00**＝webapp 程式還是舊的。

請做：重啟 `com.coach.event-webapp`，然後驗證 `https://event.bymyway.com/schedule/<代碼>/` 的 10/22、10/29 晚上可約時段應為 19:30 與 21:00（其他星期不變）。Windows 沒有 fcntl、不能 import 該模組，我用 ast 抽函式模擬算過是對的。

細節見記憶 `reference_booking_page_thursday_slots_2026-10-15.md`（claude-brain）。
