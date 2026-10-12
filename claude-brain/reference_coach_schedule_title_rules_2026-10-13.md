---
name: reference_coach_schedule_title_rules_2026-10-13
description: 教練行程總表的名稱簡化規則（週一週四分享會、週二~五早上BNI例會、MSP／LTRT只留代碼等），sync-tainan 已內建
metadata:
  type: reference
---
教練 10/13 要求行事曆名稱簡短明確，看了就知道在忙什麼：
- 週一、週四 17:30 那場＝**分享會**（原「BNI全台交流」「線上學習-成功見証分享會」）；週二~五早上＝**BNI 例會**；諮詢會議、戰報會議、BNI 培訓照寫；週二 21:30＝團隊會議；週三方碩方＝團隊週會；咖啡會議、榮樹下訪談（Podcast）；進階／初階MSP 只寫 MSP，LTRT 只寫 LTRT。
- 程式：`scripts/coach_schedule.py` 的 `simplify_tainan_title`（同步大台南行事曆時自動套用，括號「適逢…」也去掉）。人工加的巴哈行程用 add 時自己下簡短名稱。
- 預約頁公開版只顯示時段、不顯示名稱；名稱在內部清單與群組分身看得到。教練要預約頁也顯示名稱需改 event-signup（尚未做）。
