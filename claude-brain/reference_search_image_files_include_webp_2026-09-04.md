---
name: reference-search-image-files-include-webp
description: 搜尋教練提供/貼上的圖片檔案時，副檔名清單要涵蓋webp/gif，不能只寫傳統jpg/jpeg/png
metadata: 
  node_type: memory
  type: reference
  originSessionId: 65a4f974-3ac9-474c-8683-dbde5d132d06
  modified: 2026-09-04T08:19:26.769Z
---

搜尋使用者提供或提到的圖片檔案時，`find`/`glob`等副檔名清單預設要寫：`jpg jpeg png webp gif`（視情境可再加`bmp/svg/avif`），不要只寫傳統三種（jpg/jpeg/png）。

**Why:** 教練在對話中貼圖，瀏覽器/社群平台（尤其Facebook等分享下載的圖片）大量使用WebP做預設輸出格式，比傳統JPG更常見。2026-09-04踩過一次：教練貼一張海報要加進seabiscuit20的「時光足跡」照片牆，`find D:/Users/Downloads -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png"`查無結果，於是又花好幾輪工具呼叫去Desktop/Pictures/AppData繞了一圈（還誤抓到一張無關的舊海報檔案），教練澄清「就在下載資料夾」後重新查證才發現檔案是`.webp`格式，自始至終就在對的資料夾裡，只是被副檔名清單篩掉。詳見試金石案例70。

**How to apply:** 任何時候要搜尋使用者提供或提到的圖片檔案，副檔名清單一律先寫全（jpg/jpeg/png/webp/gif），搜不到時第一個該懷疑的是「搜尋條件本身」，不要急著跑去其他資料夾亂找——教練明確指出的位置優先相信是對的。
