---
name: repo-served-static-assets-4hr-cache
description: event.bymyway.com透過_serve_repo_file(send_from_directory)服務的靜態微站，CSS/JS/HTML都有cache-control:max-age=14400(4小時)，快速迭代時教練跟AI自己的瀏覽器都會看到舊版
metadata: 
  node_type: memory
  type: reference
  originSessionId: de296bea-ce9f-4876-9810-0444b5860bbd
  modified: 2026-09-03T10:43:09.682Z
---

`event-signup/app.py`的`_serve_repo_file()`（`send_from_directory`底層行為）對所有透過它服務的檔案（`/ai-art/`、`/1010/`、`/DIY/`、`/Leadership/`、`/leader/`、`/tut/`等micro-site）都會回傳`cache-control: max-age=14400`（4小時），這是Flask+Cloudflare疊加的預設行為，不是特別針對某一頁設定的。

**實測踩坑（2026-09-03，`/1010/`頁面RWD調整場）**：改完CSS後在自己的測試瀏覽器分頁裡看，即使開「全新分頁」也還是讀到改動前的舊版——因為瀏覽器磁碟快取是跨分頁共用的，不是分頁各自獨立。同一天教練自己在真實Chrome裡也踩到同一個坑（`/1010/`表頭固定的CSS明明已經改好，教練說「沒有固定呀」，最後教練自己抓到是沒重新整理）。

**驗證修改是否真的生效的正確做法**：
- 不要相信「開新分頁」就代表沒快取——用`fetch(url, {cache:'no-store'})`直接讀取最新內容比對，或在URL後面加`?_cb=時間戳`強制繞過快取
- 給教練看之前，若這個網址他可能之前開過，主動提醒他重新整理（或Cmd+Shift+R強制重新整理），不要預設他會自己想到

**如果未來同類micro-site迭代變得更頻繁**，可以考慮把`_serve_repo_file`改成對開發中頁面設較短快取或`no-cache`，但目前教練沒有明確要求改動這個全域行為，先用「主動提醒重新整理」處理即可，不要自作主張改動共用的快取設定（會影響所有已上線頁面的CDN效能）。
