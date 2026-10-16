---
name: bigtree-event-signup
description: 教練要活動頁能報名、或要做新場次時使用——「線上報名 SOP」「加上報名」「加一個立即報名」「網路報名」「做一場新的」「照上次那場複製」「新增場次」。建場次資料、放報名表、測試（不吵到群組）、清測試資料、交付。
---

# 活動報名頁（完整規則在 `knowledges/SOP_線上報名.md`；複製舊場次看記憶 reference_clone_event_page_and_keynote_export_2026-10-04）

## 新場次要不要複製舊頁
教練說「內容一樣、要留歷史頁」→ 複製 `~/github_repos/<舊slug>/` 到 `~/github_repos/<新slug>/`，用程式一次取代日期、slug、場次序數，取代後 grep 確認沒有殘留舊日期。**QR 碼、海報都要重做**（舊的會指向舊網址），換圖要換檔名。

## 步驟
1. **建場次**（先備份 `event-signup/event.db`）：`events` 表新增一列，`slug` 跟網頁短網址一樣，填 `name`、`event_date`、`start_time`、`location`、`venue`、`address`、`event_url`、`status='active'`；教練是講師的場次 `site='bigtree'`（結束後會自動進大樹小講歷史頁）。沒建這列，報名會變成「場次代碼對不上」。
2. **改網頁**：所有「立即報名」按鈕 `href="#signup"`；報名區照抄 `knowledges/templates/線上報名_範本片段.html`（表單 `#regForm`、成功視窗 `#okModal`），改 `SLUG` 與 `SESSION` 兩個值，顏色用該頁自己的變數。送出打 `POST https://event.bymyway.com/api/register`。
3. **測試，不准吵到群組**：
   - 後端：`event-signup/venv/bin/python3` 開 Flask test client，把 `_notify_xiaolongxia` 換成假函式，打一次 `/api/register` 確認 `ok:true`，**刪掉測試的 attendees＋signups**。
   - 前端：瀏覽器裡先把 `window.fetch` 換成假的再點「立即報名」：空白送出要出紅字、填好送出要跳成功視窗且 slug 正確；手機 375 寬沒有左右捲動。
   - 真的送一筆＝群組會收到通知，教練說可以才做；做了要當場清掉測試資料。
4. **字 ≥20px、上線確認、交付**：照 `bigtree-web-edit` 技能第 4～7 步。網址獨立一行。
