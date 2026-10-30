---
name: project-rongtree-booking-shows-name-two-forms-2026-10-30
description: 榮樹下官網預約 10/30 整個改順：顯示姓名、預約資料帶進來賓資料表、送出即自動確認不再待確認；「預約表單」和「來賓資料表」是兩張
metadata:
  node_type: memory
  type: project
  originSessionId: 2007a746-146d-46f9-a412-c018e0eb3d3f
  modified: 2026-10-30T13:13:20.713Z
---

2026-10-30 教練連續糾正，榮樹下官網預約（/api/rongtree/hold）最終流程：**預約即成立**（自動確認：排開始前 1 小時提醒＋寫 Google 日曆，跑 `coach_schedule.py confirm`）→ 前置作業與來賓卡後台顯示預約人姓名 → 成功畫面帶去填來賓資料表 → 資料表有沒有填才是要看的狀態。

兩張表分清楚：「預約表單」（我要預約，進 works_contact_leads）只問姓名／單位／聯絡／想說的話；「來賓資料表」（/rongtree/guest/<form_token>，rongtree_guest_forms）另外要人生轉折、公益故事。張瓊方 6:21 填的是預約表單，我一度說成「她沒寫」被糾正。預約時填的資料存在行程 `booking_data`，打開資料表自動帶入（姓名、單位→title、聯絡、想說的話→intro）。

教練的邏輯：「對方自選的 7-8 點就是訪談時間，要確認的是有沒有填來賓表，不是確認時間」。官網預約的上限改成「還沒填資料表的最多 6 筆」。來賓卡後台 `/rongtree/a/<代碼>` 有「接下來的訪談」表＋「確認這個時段」鈕（給預約頁進來仍待確認的）。

存檔：workspace d860a3224、87beaacc5、be4a4afd6、5d6d478d2；rongtree 6cbe817、49b178b。

**Why:** 教練要的流程只有兩件事——預約成立、資料表有沒有填；任何多一道「確認時間」都是系統自己加的麻煩。
**How to apply:** 教練說某來賓「填了卻沒出現」，先分清是哪張表再答，用「預約表單」「來賓資料表」兩個名稱；不要為對方自選的時間再設確認關卡。整條「網頁送出→自動確認」尚未用真預約實測，下一位真預約時要核對。相關：[[project-rongtree-booking-hold-and-saturday-930-2026-10-23]]
