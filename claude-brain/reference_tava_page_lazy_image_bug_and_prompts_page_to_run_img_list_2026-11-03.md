---
name: reference-tava-page-lazy-image-bug-and-prompts-page-to-run-img-list-2026-11-03
description: TAVA 做的網頁若用 new Image()+loading=lazy+onload 才 append 的載圖程式，離畫面的圖永遠不載（只剩第一張）；TAVA「配圖提示詞清單 prompts.html」要轉 JSON 才能餵 run_img_list.py；《重新呼吸》rebreathe 是首例
metadata:
  node_type: memory
  type: reference
  originSessionId: 1209db1c-593d-47bb-89b9-983d2cded11d
  modified: 2026-11-03T14:19:54.316Z
---

11/03 《重新呼吸》（~/github_repos/rebreathe，網址 /curated/rebreathe/）裝好 23 張 LK888 圖後，教練說「沒看到圖片」。

**根因（本機重現、線上 Chrome 實測）**：index.html 的 `figure.pic[data-img]` 載圖迴圈對每格建 `new Image()`、`loading='lazy'`（只有 hero 內的 eager）、onload 才 `fig.appendChild(img)`。沒進頁面的 lazy 圖瀏覽器不載 → onload 不會觸發 → 22 格只有第 1 張顯示。改 `img.loading='eager'`（commit `634db31`）後 22/22。驗證時舊分頁吃快取會誤判「修法無效」，要加 `?v=` 重開。

**TAVA 提示詞清單格式**：prompts.html 的提示詞在 JS 陣列 `const P=[['01','標題','比例文字','prompt',retro旗標],…]`，STYLE／STYLE_RETRO 另存、出圖時接在 prompt 後面；`run_img_list.py` 讀不到（要 `<pre>` JSON）。轉法：Python ast 解析陣列→JSON，欄位 id／file／type（要寫「概念」，寫 concept 會被當實景修飾跳過）／ratio（只認 16:9、4:3、3:2、4:5、3:4、1:1；「1200×630」手動對 16:9）／prompt；超過 12 張要分批（12＋11）。23 張約 2～3 分鐘出完。

**Why:** 教練希望「出圖後自動裝上網址」不要停下問；這個 bug 是 TAVA 範本帶來的，其他 TAVA 頁很可能同症狀。**How to apply:** 裝完圖後在真 Chrome 數 `figure.pic img` naturalWidth>0 的數量再回報；TAVA 範本 playbook 要加「圖片一律 eager 或先 append」（還沒改）。相關：[[reference_swap_slot_images_after_publish_flow_2026-10-30]]、[[reference_img_list_one_command_deliver_first_lock_2026-11-02]]。
