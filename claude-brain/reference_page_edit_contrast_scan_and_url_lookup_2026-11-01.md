---
name: reference-page-edit-contrast-scan-and-url-lookup-2026-11-01
description: 改網頁深色區塊顏色一次掃全頁(page_contrast_scan.js)、找活動頁連結先查 event.db events.url 與 app.py 路由、公開頁不留講者控制台
metadata:
  type: reference
---

**事件**：11/01 互動頁 ai-impact 同一個深色區塊連被教練抓三次（下拉選單白底白字、已送出提問卡片、熱門／最新按鈕），每次只修他點名的那一個；另外「大樹小講／AI 微論壇」連結我先給官網與 GitHub 的錯網址，教練罵「你連 ByMyWay 網址都找不到」。

**Why:** 深色區塊（`.dark`）會把字色設成淺色，裡面的淺底元件（按鈕、卡片、下拉）繼承到白字就看不見；只修被點名的那一個，同區塊其他元件還是壞的。

**How to apply:**
- 改完網頁先跑 `node ~/.openclaw/workspace/scripts/page_contrast_scan.js <網址>`（全頁對比<3＋左右捲動，電腦／手機各一次）；選中／送出後的狀態要自己點過再掃。
- 找「大樹小講」「AI 微論壇」這類活動頁連結：先查 `event-signup/event.db` 的 `events.url` 與 `app.py` 的 `@app.route`（`/bigtree/`＝大樹小講、`/ai-talk/`＝AI 微論壇回顧、`/ai-forum/`＝台中場延後公告），不要只翻官網。
- 做公開轉發的複製頁：拿掉講者控制台（原頁 `?admin` 會開）、計時器、揭曉鈕。
- 刪伺服器上的資料前先備份該列（本次 seed3 備份在 `state/nmda_ai_seed3_backup_20261101.json`）。

相關：[[feedback-verify-only-changed-element-one-screenshot-2026-10-27]]
