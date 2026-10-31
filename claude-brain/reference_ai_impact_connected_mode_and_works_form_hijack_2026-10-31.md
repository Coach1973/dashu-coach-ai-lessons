---
name: reference-ai-impact-connected-mode-and-works-form-hijack-2026-10-31
description: 互動頁「送出沒反應」＝API_BASE=null 單機模式＋上架自動塞的 works-form.js 攔截 submit；修法與以後要先查什麼
metadata:
  type: reference
---

零基礎學 AI 啟動大會互動頁（github_repos/ai-impact，網址 event.bymyway.com/curated/ai-impact/）：①頁面內建「連線模式」`API_BASE='/api/nmda-ai'`，原本寫 null＝每人資料只在自己手機；後端現為 event-signup/nmda_ai.py（nmda_ai.db，commit d3213f0dd，頁面 09e687b）。②上架流程自動給表單加 `data-works-form` ＋載入 `/static/works-form.js`，它用 `stopImmediatePropagation` 攔掉頁面自己的 submit，還要求姓名＋電話／Email；互動頁表單沒這些欄位，來賓只看到紅字。

**Why:** 教練現場「送出了、螢幕沒反應」。證據：works_contact_leads 該站 0 筆、真 Chrome 兩個獨立訪客復測才通。
**How to apply:** 任何「互動／即時」類作品頁（票選、提問牆）交付前：先看 API_BASE 是不是 null、表單有沒有 data-works-form；用兩個獨立瀏覽器環境實測「一個送、一個看」。重新打包上架可能又被自動塞回 works-form，要再拿掉。相關 [[reference_event_lottery_join_url_setting_2026-10-31]]。
