---
name: feedback-ui-change-location-must-confirm
description: 教練要求改UI元件(按鈕/連結)時要問清楚是放在哪一頁，不能自己假設個別頁面vs總覽頁
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3f78a0b4-707b-4ef1-b821-93e5f2584e4f
  modified: 2026-09-01T02:53:43.593Z
---

教練要求「把首頁導覽列的A按鈕改成B」這類UI改動時，不能自己推斷「應該放在哪一頁」——bni-chapters系統裡「認識分會/核心價值」這兩個字串同時出現在首頁(`templates/index.html`)跟每個分會的個別頁面(`templates/chapter.html`)，軍師一開始改到了個別分會頁面(`/sincere`)，導致該分會頁面原本的錨點跳轉功能被誤蓋掉，而教練要的其實是首頁（分會一覽表）。

**Why：** 教練原話「你怎麼就做錯了...你做到真誠分會過去，那真誠分會原本那兩個按鈕不就白費了嗎？而且我從頭到尾都沒有告訴你，應該是去貼在真誠分會的那一頁上面」——同一段文字/UI元件出現在多個頁面時，改動位置不是能從上下文自然推斷的，屬於必須先確認的範疇。

**How to apply：** 收到「把X按鈕改成Y」這類指令時，先搜尋確認X這個字串/元件在系統裡出現在哪些頁面（`grep`），如果不只一處，直接問教練是哪一頁，不要挑一個「看起來合理」的位置動手。跟 [[feedback_url_given_open_it_dont_guess_2026-09-01]] 是同一類「先查證再動手」的教訓，這次是UI定位版本。
