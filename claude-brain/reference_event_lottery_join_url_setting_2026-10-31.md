---
name: reference-event-lottery-join-url-setting-2026-10-31
description: 掃碼抽獎簽到後跳去哪，由 event.db app_settings.lottery_join_url 決定；10/31 設成零基礎學AI LINE群邀請連結，回退只要刪該列
metadata:
  type: reference
---

event-signup 的 `_lottery_greet_url`（app.py）先讀 `app_settings.lottery_join_url`：有值（須 https://line.me/ 開頭）就導去該連結，沒值才用官方 LINE 問候語（綁定 line_user_id）。10/31 教練改成「加入零基礎學 AI 群才能抽獎」，已設為群邀請連結（commit f74db3b97）。

**Why:** 教練給的是 LINE 群邀請 QR，掃了直接進 LINE、不經過我們網站，所以只能改簽到後的跳轉，不能換他的 QR。抽獎名單來自簽到紀錄，不看是否進群；官方 LINE 綁定因此不再發生。
**How to apply:** 要換群或改回官方 LINE：改／刪該設定列（不用改程式，但程式改動後要重啟 com.coach.event-webapp）。教練問「掃了就能加入嗎」要講清楚：掃 QR→輸入手機→跳群頁按加入。現場「目前活動」要先在後台確認。相關 [[reference_dashu_common_urls_my_tools_vs_coach888_2026-10-19]]。
