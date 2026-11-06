---
name: reference-tava-prompts-js-items-format-and-reemployment-page
description: "TAVA prompts.html 第二種格式 `const items=[{id,file,ratio,p}]` 已寫進 run_img_list.py 可直接吃網址；婦女再就業 reemployment 網頁（slug、event.db id35、佩佩老師洽詢列）怎麼接的 (2026-11-07)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 33cd87cf-0149-4c01-a99d-1a1356e0efc7
  modified: 2026-11-06T18:29:40.329Z
---

11/07 教練給 `tava-ai.com/n2af7xksk3/prompts.html`（女性個人 IP 課程）要我「先出圖」，頁面清單是 `<script>` 的 `const items=[{id,file,where,ratio,ref,p}]`（11/03 康牧師那種是 `const P=[[…]]`，更早是 `<pre>` JSON）。同類錯第 3 次，按 N8 改源頭：`scripts/run_img_list.py` 的 `load_items` 補上讀 `const items=[…]`（用 node 轉 JSON），現在**網址直接一行跑**，不用再手動轉 JSON。

網頁 `~/github_repos/reemployment`（/curated/reemployment/）：報名表單 SLUG 必須等於 event.db 的場次 slug——TAVA 原頁寫 `women-ip-ai-1230` 資料庫查無，通知會變成「資料沒入庫」警告；已建 events id=35 `reemployment` 並改頁面。佩佩老師：電話 0988-004-118（教練 7/9 指定）、LINE `https://lin.ee/vyFqWVB`（教練 7/9 稱它為 LINE ID，是連結）。頁尾 TAVA 慣例寫法 `<a href="https://www.tava-ai.com/">本網頁由 TAVA AI 製作</a>`。

**Why:** TAVA 每頁的清單格式不固定；網頁 `<img width height>` 屬性會蓋掉 CSS `aspect-ratio`（要補 `height:auto`）。**How to apply:** 收到 TAVA prompts 網址先 `--dry-run` 看讀得到幾張；插圖類 CSS 一律加 `height:auto`；驗證報名用 Flask test client＋假 `_notify_xiaolongxia`，驗完刪測試 attendees／signups。相關 [[reference_tava_page_lazy_image_bug_and_prompts_page_to_run_img_list_2026-11-03]]
