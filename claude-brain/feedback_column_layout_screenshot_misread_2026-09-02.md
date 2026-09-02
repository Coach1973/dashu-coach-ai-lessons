---
name: feedback_column_layout_screenshot_misread_2026-09-02
description: CSS column-count多欄排版的頁面，截圖後不能用「由上到下、由左到右」的直覺閱讀順序去判斷DOM歸屬，會誤判項目屬於哪個分類
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b5eadffb-228e-4bea-97d2-aebdae1e4788
  modified: 2026-09-02T12:57:30.461Z
---

coach888 作品總覽表用 `column-count:2` 做 masonry 式多欄排版（`.section-block { break-inside:avoid }`）。教練口頭反映他在本機修改過排序，我用 computer-use 截圖（教練口頭核准）看畫面，把左欄看到的「BNI最近常用」尾端項目跟右欄同一垂直高度的「BNI專用」項目，直覺當成「同一批項目被搬到一起」，據此推論教練把好幾個項目搬進了BNI專用——**這個推論完全錯誤**，右欄那些其實是CSS多欄排版自然分流的結果（瀏覽器把整個 section-block 完整塞進某一欄以維持欄高平衡，不是真的照閱讀順序左右交錯），跟教練實際的編輯內容無關。

**Why**：多欄 CSS 版面的視覺垂直對齊，不代表 DOM 或邏輯上的關聯——同一個螢幕高度上左右兩欄可能來自完全不相干的兩個 section，因為瀏覽器是先把左欄「填滿」到目標高度，才開始排右欄，不是逐列交錯排列。

**How to apply**：
1. 遇到 `column-count`/masonry 排版的頁面要用截圖判讀結構時，先確認截圖工具能不能捲動/能不能看到完整頁面，只看得到局部畫面時要對這類版面的判讀結果打問號，不要直接下結論。
2. 與其花時間截圖猜測，不如直接請教練用一句話講清楚實際改了什麼（這次教練一句「把1移到5那邊，下面都沒動」就徹底講清楚，比我看截圖猜測快且準）——複雜版面的視覺判讀，語言描述往往比圖像判讀更可靠。
3. 這不是「叫教練當搬運工」，是判斷這類任務用哪種輸入管道最準確：教練口述意圖 vs AI 截圖臆測，這次證明前者更可靠。

Related: [[feedback_visual_change_screenshot_not_dom_numbers]]（同樣是視覺驗證的教訓，那次是強調截圖優於DOM數字，這次是提醒截圖本身也有排版陷阱要注意）
