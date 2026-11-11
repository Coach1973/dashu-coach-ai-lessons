---
name: web-emoji-replace-with-lk888-custom-icons-compressed
description: 教練說網頁上的 emoji 太廉價＝全部改 LK888 客製圖（每個意思一張、256px webp 壓縮），不要用同一個印章蓋 25 處；做法與雷點
metadata:
  type: feedback
---

幸福學頁（11/11）教練嫌 emoji「很廉價」，要求網頁上**所有 emoji 都改 LK888 做**，圖要符合頁面風格、像精心客製，且一定要壓縮。他一度提議「用同一個印章／圖騰代替」，但每個 emoji 意思不同（資格、上課資訊、身心靈/AI/ESG 等），用同一張會看不出差別，所以最後每個一張。

**Why:** 教練在乎網頁質感；速度也在乎（所以壓縮）；同一個符號蓋全部會失去資訊。
**How to apply:**
- 先看頁面既有圖與色票，寫 `.image-style.md` 風格卡；先試 1 張定調，再批次。
- 批次用背景＋Monitor 等（24 張約 15 分鐘），走 `lk888_guard`（同一條 prompt 24 小時只付一次，重複圖示共用同一張檔案）。
- 圖背景是奶油色方塊，直接貼會露出方框 → 版面上做成圓形徽章／小圓章（border-radius:50%、object-fit:cover）。
- 輸出 256px webp q82，每張 2～7 KB；`data-success` 這類純文字屬性裡的 emoji 也順手拿掉。
- 保留 ✔ ➜ 這類文字符號（不是 emoji 圖）。
相關：[[feedback-img-list-lk888-no-ask-routine-authorized]]
