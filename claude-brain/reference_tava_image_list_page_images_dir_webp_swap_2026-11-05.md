---
name: reference-tava-image-list-page-images-dir-webp-swap-2026-11-05
description: TAVA 出圖清單版網頁（images.js＋images/ 資料夾，不是 data-slot）回填圖＝把 run_img_list 的網頁小圖 webp 依 IMG-編號 放進 images/ 即可；載圖程式 detached Image 設 lazy 會永遠不載，要拿掉 lazy
metadata:
  node_type: memory
  type: reference
---

business-bni（BNI 冷卻期 SOP，TAVA 做）用 `images.js`＋`app.js fillPh()` 載圖：圖片依 ID 命名放 `~/github_repos/business-bni/images/IMG-001.webp`（jpg/webp/png 皆可）就自動顯示，**不需要 swap_slot_images.py**（那支給 data-slot 版網頁）。出圖用 `run_img_list.py <清單.json> <輸出夾>`，輸出夾的 `IMG-00X.web.webp`（約 30～75KB）複製成 `images/IMG-00X.webp`，commit＋push＝上線（commit `0fa4755`）。

**坑**：`fillPh()` 用 `new Image()` 設 `loading="lazy"`、onload 才 append 進畫面 → 沒在 DOM 的 lazy 圖瀏覽器不載，25 個圖位全空。拿掉 `img.loading="lazy"` 即好（`f602da9`，Chrome 實測 25/25 載入）。這是第二次踩（前一次 [[reference_tava_page_lazy_image_bug_and_prompts_page_to_run_img_list_2026-11-03]]），源頭在 TAVA 的開工指令，不在單頁。

**run_img_list 注意**：一次最多 12 張→27 張分三批；LK888 讀取逾時會失敗不自動重試，重跑同一批會略過已出好的；清單 type「實景感概念」且參考照＝無，程式會跳過，需手動改成「概念」；ratio 非 16:9／4:3／4:5／3:2／3:4／1:1（如 1200×630）要手動換。

**Why:** 教練 11/05 要「出圖清單網頁做好後，我貼網址你就把圖裝回去」。**How to apply:** 看到 images.js＋images/ 結構就走這條；回報前用瀏覽器量圖位 naturalWidth>0，不只 curl。
