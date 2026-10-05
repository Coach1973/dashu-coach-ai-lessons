---
name: reference-pdf-portrait-extract-use-displayed-aspect-2026-10-05
description: 從 PPT 轉的 PDF 抽人像，原圖寬高比常跟投影片上顯示的不同（差到 37%），要照 bbox 顯示比例重縮放＋頭頂位置一致，否則人變胖變瘦（教練 10-05 抓到）
metadata:
  type: reference
---

2026-10-05 真誠分會 15 位夥伴照片從《真誠分會夥伴PPT.pdf》抽：用 PyMuPDF `doc.extract_image(xref)`＋`smask` 貼白底，取到的是「原始像素」，但 PowerPoint 轉 PDF 時投影片上的顯示框（`page.get_image_info()` 的 bbox）寬高比不一樣——鄭禮昂差 37%、陳佩君 33%、鄭綉美 30%、郭展鴻 23%，教練一看就說「變形、位置不恰當」。

**How to apply:**
- 抽人像後一律 `resize((round(h*bbox_w/bbox_h), h))` 照投影片顯示比例；`pdfimages -list` 的 x-ppi ≠ y-ppi 就是這個訊號。
- 卡片是 5:4、從上方裁：左右裁到人＋8% 邊、頭頂上方留卡片高度 7%，人的大小位置才一致（`bni-chapters/extract_sincere_ppt_2026-10-05.py` 的 `frame_for_card`）。
- 整頁壓平成一張圖的投影片（真誠第 13～15 頁）沒有獨立人像，只能從頁面裁。
- 交付前做「原本／修正後／投影片上」三欄並排圖自己看過再上線。
- 相關：[[feedback-elite-list-is-master-no-reentry-2026-10-04]]
