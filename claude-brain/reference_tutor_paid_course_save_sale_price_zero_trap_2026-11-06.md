---
name: reference-tutor-paid-course-save-sale-price-zero-trap-2026-11-06
description: bymyway.com Tutor 課程前台一直顯示免費＝課程編輯器「已付款」沒存進去；選已付款＋商品後特價欄要清空（填0會讓商品變免費）；課程封面用 REST 設 featured_media
metadata:
  type: reference
---

課程 27448（高價銷售 12 週陪跑課程）前台顯示「免費觀看」時，先到 wp-admin → `admin.php?page=create-course&course_id=27448` 看定價模型：重載後若是「免費」就是沒存進去。做法：選「已付款」→「選擇商品」搜尋商品名點選（原價會自動帶 180000）→ **特價欄清空**（預設 0，存下去商品會變免費）→ 按「更新」→ 重載確認 paid 仍勾著。前台判斷：課程頁出現「加入購物車」與 `name="add-to-cart" value="27543"`；LiteSpeed 有頁面快取，驗證用 `?x=隨機` 加亂數網址。

封面：上傳到 `wp-json/wp/v2/media`（應用程式密碼，直連源站 64.176.38.233），再 POST `wp/v2/courses/<id>` 與 `wp/v2/product/<id>` 的 `featured_media`。WooCommerce 結帳不開放訪客（`enable_guest_checkout=no`），結帳時註冊。

**Why:** 11/06 上午回報「已存已付款」但前台仍免費，下午才查出是沒存成功。
**How to apply:** 之後改 Tutor 課程價格，存完一定重載編輯器＋用亂數網址看前台，兩邊都對才算。相關：[[reference_bymyway_tutor_course_build_via_ajax_htc_video_tunnel_2026-11-06]]
