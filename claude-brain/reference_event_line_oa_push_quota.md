---
name: reference-event-line-oa-push-quota
description: event-signup系統用的LINE官方帳號@qaw8118h每月推播額度200則(免費方案)，用完不是bug；/admin/notify頁已內建即時額度顯示，不用再查API
metadata: 
  node_type: memory
  type: reference
  originSessionId: 586e8d1b-6f90-4d2f-a3fc-7b66a47f227c
  modified: 2026-08-23T14:37:26.921Z
---

2026-08-23教練回報`/admin/notify`群發訊息「發送失敗」，查證後確認：不是後台程式壞掉，是LINE官方帳號「大樹教育顧問」(@qaw8118h，event-signup系統專用，跟龍蝦小助教是不同帳號)本月推播額度用完（免費方案200則/月，`GET /v2/bot/message/quota/consumption`查到`totalUsage:200`打平`limit:200`）。免費方案每月初重置。

**Why**：這個帳號的push quota跟教練其他LINE帳號（龍蝦小助教@268dptjc）完全獨立，互不影響；`/line/webhook`收綁定訊息、`/checkin`簽到、`/api/register`報名寫入這些功能都不消耗push額度（只有`_line_push()`真正發送出去的訊息才算），所以額度用完只會讓「主動群發通知」失效，其餘功能正常。

**How to apply**：
1. 下次再看到LINE群發「失敗」，**先查額度再查程式碼**：`/admin/notify`頁面已經內建即時額度顯示（2026-08-23新增，commit`b3a6900d9`），登入直接看得到目前用了幾則，不用再手動打API
2. 免費方案要拉高額度只能教練本人登入LINE Official Account Manager付費升級，AI不能代為購買
3. 額度用完期間，需要接觸「已報名但尚未綁定LINE」的人，`/admin/notify`頁同一次更新也加了「未綁定名單一鍵複製連結」功能，教練可用簡訊/電話等其他管道把個人化連結送出去，繞過push額度限制
