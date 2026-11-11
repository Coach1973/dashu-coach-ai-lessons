---
name: event-poster-pillow-jpg-font-no-middle-dot
description: 活動頁 EDM 海報要 JPG＋下載鈕：用 Pillow 疊字出直式1080x1350／橫式1600x900；macOS 的 STHeiti 沒有「・」會印成方框
metadata:
  type: reference
---

金門私廚頁（kinmen-kitchen-1205）11/11：EDM 只有佔位圖、沒下載鈕，教練要 JPG 可下載、海報上要有時間地點費用與匯款資訊。
- 程式：`workspace/scripts/kinmen_poster_jpg.py`（Pillow，照片取頁面 ph-IMG-001.webp，字型 `/System/Library/Fonts/STHeiti Medium.ttc`；改文字重跑即可）。
- 頁面：兩個 `<figure>` 換成 `images/edm-portrait.jpg`／`edm-landscape.jpg`，下面加 `<a download="…jpg">` 兩顆鈕，og:image 改橫式。
- 雷：STHeiti 沒有中點「・」，印出來是方框 → 一律改用「，」；字體量大小要看圖確認沒有被切到底（直式要先預留文字區高度）。
- 這台沒有 playwright，無頭 Chrome 截圖也失敗；截圖又被截圖鎖擋 → 用內建瀏覽器 JS 量 DOM（img.decode、emoji 殘留）驗證。
