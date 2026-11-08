---
name: reference-tava-signup-form-is-mock-wire-to-api-register
description: TAVA 做的報名網頁表單常只跳成功畫面、沒真的送出；上架後要建 events 列＋改成 POST /api/register（11/09 ai-image1202 為例）；run_img_list 檔名帶 images/ 子資料夾曾存檔失敗已修
metadata:
  node_type: memory
  type: reference
  originSessionId: 187f6086-0c4a-4e7a-897e-1310d40b8ecb
  modified: 2026-11-08T18:36:00.552Z
---

11/09 ai-image1202（台灣形象設計發展協會 12/02 講座）：TAVA 網頁 `index.html` 的 submit 只做驗證＋顯示成功畫面，**沒有 fetch**；表單掛 `data-works-form="ai-image-1202"` 但頁面沒載 works-form.js，所以報名資料哪裡都沒去。要接「活動報名即時通知」＝①`events` 表新增一列（slug 跟網頁短網址一樣 `ai-image1202`，TAVA 寫的 `ai-image-1202` 是錯的）②拿掉 data-works-form 屬性（避免之後被上架自動塞的 works-form.js 攔走）③submit 改 `fetch('https://event.bymyway.com/api/register')`，payload slug/name/phone/email/company/note（身分、人數、費用、來源塞進 note），回 `ok:true` 才顯示成功、失敗留在表單④後端用 Flask test client＋假 `_notify_xiaolongxia` 測，測完刪 attendees＋signups 測試列。

**Why:** 教練看不出來表單是假的，客人會以為報名了；通知不會響。**How to apply:** 收到 TAVA 報名頁上架，先 grep submit 有沒有 fetch、`data-works-form` 的 slug 對不對，再接 /api/register。相關 [[reference_tava_prompts_js_items_format_and_reemployment_page_2026-11-07]]。

另：`run_img_list.py` 清單 file 欄位帶子資料夾（images/img-001.webp）原本會 FileNotFoundError（出了圖但存不進去），11/09 已改成先 mkdir（commit 見 workspace git log）。
