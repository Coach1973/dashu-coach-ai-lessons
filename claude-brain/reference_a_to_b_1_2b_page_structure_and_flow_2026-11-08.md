---
name: reference-a-to-b-1-2b-page-structure-and-flow-2026-11-08
description: 教練說「1-2B」＝a-to-b（從A到B過橋任務）網頁；GitHub Coach1973/a-to-b、本機 ~/github_repos/a-to-b、線上 event.bymyway.com/curated/a-to-b/；單檔 index.html，第2關16張翻牌、第4關11個搭橋方法、第5關三拼圖；TAVA 清單頁≠成品，教練刷新錯頁會以為沒修好
metadata:
  node_type: memory
  type: reference
  originSessionId: c1744500-5b3a-42b0-886c-c829250f3b2f
  modified: 2026-11-08T12:04:42.632Z
---

「1-2B」（教練語音：1 槓 2B＝從 A 到 B）＝`a-to-b`，教練已上架。單檔 `index.html`（JS 資料陣列 PAINS／TRIES／MILES，圖在 `img/`），push 後線上約 7 秒生效。TAVA 清單頁 `tava-ai.com/riccm8f97h/handoff/image-list.html` 只是出圖清單（20 張，已全部回填），**不是成品**。

**11/08 做的**：第2關 PAINS 4→16 張點擊翻牌（`pain_*.jpg`，LK888 出 12 張，翻牌不用 3D 轉換）；第4關 TRIES 4→11 個搭橋方法（約 8 個體力歸零）；第5關三拼圖卡正面改 `puzzle_clients/talent/mentor.jpg`；回頂端按鈕（表頭＋右下浮動，用頁面自己的 `smooth(0)`，原生 smooth 在長頁面會被中斷）；圖片網址加 `?v=`。

**坑**：①教練說 Windows 看不到圖，查伺服器、檔案、快取都正常，最後是他**一直刷新的是 TAVA 的頁面不是我的網頁**——教練說「刷新沒用／看不到」時，先確認他開的是哪個網址。②本機測試用 8791 埠，不要用 8765（8765 是正式站放行來源，會寫進正式資料）。③自檢程式 `page_preflight.js` 對 a-to-b 有舊有紅燈（A/B 圓點、按鈕對比、「表頭沒固定」誤報），「已收進背包」對比是誤報（實算 4.88）。④出圖用 `scripts/run_img_list.py <json> <輸出夾> --no-send`，id/file/type/ratio/prompt；12 張一批約 3 分鐘。

**Why:** 下次教練說改 1-2B／過橋任務，一開始就知道是哪個專案。**How to apply:** 先 `cd ~/github_repos/a-to-b && git pull`，改完本機 8791 實測、push、curl 線上確認。
