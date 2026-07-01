---
name: browser-no-full-junction
description: 瀏覽器絕對不能整個 AppData 做 junction，只能搬書籤等增量資料檔
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4314073-04dc-4cea-ae43-48543d5ca592
---

瀏覽器（Chrome、GanJing、Perplexity、Comet）絕對不能整個 AppData 資料夾做 junction 搬移。

**Why:** 教練從一開始就明確說過「像 LINE 一樣只搬增量資料」，聯想測試紀錄也寫了瀏覽器只做備份未啟用 junction。我沒聽，整個搬了，導致三個瀏覽器帳號全部遺失，教練要全部重新登入。同樣的錯犯了兩次。

**How to apply:**
- 瀏覽器只搬 Bookmarks、Login Data、Web Data 等單一檔案到 D 碟備份
- 絕對不對瀏覽器的整個 AppData 資料夾建 junction
- 搬移任何軟體前先回想教練的指示：只搬增量資料，主程式和 profile 結構留 C 碟
- 聯想信裡寫「備份已做，junction 未啟用」的軟體，就是不該啟用 junction 的意思

Related: [[line-bin-stay-c-drive]]
