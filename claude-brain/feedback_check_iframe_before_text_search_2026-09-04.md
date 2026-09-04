---
name: feedback_check_iframe_before_text_search_2026-09-04
description: bymyway.com找不到內容時要先查iframe嵌入技術，不能只靠curl/grep文字搜尋，教練親口指出浪費時間token
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 786ed7db-2ca8-4ff8-9a7e-eebbebaafb36
  modified: 2026-09-04T13:54:17.048Z
---

查bymyway.com任何頁面，若curl抓到的HTML大小正常但關鍵字全部搜不到，先查該頁原始碼有沒有`<iframe`標籤——這個網站至少兩頁是先在GitHub Pages建好、再用iframe嵌回bymyway.com（`/ai-go/`嵌`coach1973.github.io/ai-go/`，`/coach/`嵌`coach1973.github.io/bymyway-website/`）。iframe內容是完全獨立的文件，父頁面純文字搜尋永遠找不到。

**Why**：2026-09-04教練要求把bymyway.com「關於教練」頁搬到seabiscuit20，Sonnet 5用curl查了`/`、`/about/`、`/coach/`、`/ai/`、`/old/`共5個頁面全部搜不到內容，甚至懷疑教練瀏覽器快取問題，繞了一大圈才靠翻舊對話逐字稿發現iframe架構。教練點破：這是不查歷史建置方式、瞎猜的代價，浪費時間跟token。真正的答案其實早就在同一天稍早讀過的[[feedback_verify_online_before_answering]]記憶檔裡（該檔案已明確記錄`/coach/`嵌入`bymyway-website`），只是沒有回頭連結使用。試金石案例71完整記錄。

**How to apply**：往後在bymyway.com找不到教練描述的內容時，第一步就是`grep -o '<iframe[^>]*'`該頁原始碼，而不是不斷更換關鍵字重試同一種文字搜尋方法；教練給出的技術架構描述（如「先GitHub做，再指到官網」）要當作查證起點直接驗證，不要在已經失敗的方法上反覆確認。
