---
name: reference-sticky-header-broken-by-body-overflow-x-hidden-audit-method
description: 網頁表頭滑掉不固定的根因（body overflow-x:hidden 讓 sticky 失效）＋全站 84 頁用同網域 iframe 往下捲量表頭的檢查法（2026-10-25）
metadata:
  type: reference
---

教練 10/25 指出寶華姐頁（linbaohua）往下滾表頭不見，楊千嬅（adia）頁卻固定。

**根因（查到）**：`body{overflow-x:hidden}` 會讓 body 變成捲動容器，nav 的 `position:sticky` 就貼不住視窗。修法：拿掉 body 的 overflow-x:hidden（html 已有 `overflow-x:clip` 即可）。另一種常見原因是手機版媒體查詢刻意寫 `position:static`（百聖、朱元中）。

**全站檢查法**：開 Claude in Chrome 到 event.bymyway.com 任一頁，用 JS 對每個 `/curated/<slug>/` 建同網域隱形 iframe（寬 1280 與 390），找頁面頂端橫跨 60% 以上寬度的 header／nav，往下捲 1500px 後量 `getBoundingClientRect().top` 是否約 0。10/25 結果：84 頁中修 4 處，12 頁無導覽列（長文／簡報型）不動。注意：手機版固定表頭高度要量（朱元中曾 220px，縮到 92px）；內建瀏覽器截圖被截圖鎖擋，外部網站一律用 Chrome 不用內建窗格。

**Why:** 教練希望每個網頁表頭都固定，不會滑掉。
**How to apply:** 新做或改網頁時，body 不要加 overflow-x:hidden；上架後可跑上述 iframe 量測。關聯 [[feedback-web-font-min-20px]]（同樣是全站網頁品質規則）。
