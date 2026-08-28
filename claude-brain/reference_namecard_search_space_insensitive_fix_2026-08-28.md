---
name: reference-namecard-search-space-insensitive-fix-2026-08-28
description: 名片系統(namecard-db)姓名搜尋因空格格式不一致大量失效的真根因+修復方法，任何新增搜尋欄位都要比照套用
metadata: 
  node_type: memory
  type: reference
  originSessionId: 47fca155-b2ce-4fdb-a972-20c2d2ab1fe4
  modified: 2026-08-28T02:19:02.970Z
---

教練搜尋「林政志」在`/find`查無結果，一度懷疑是「離會會員沒有進資料庫」，實際查證發現該人早就存在`cards`表(id 154，已標記「前會員‧曾隸屬真誠分會」)，真正原因是**姓名格式不一致**：BNI Connect匯入的姓名慣用「姓 空格 名」格式（如「林 政志」），但教練跟其他資料來源(如`bni_credit_certificates`表)慣用無空格寫法（如「林政志」）。`namecard-db/namecards.db`的`cards`表451筆裡有**422筆(93%)**是帶空格格式，一般SQL `LIKE '%關鍵字%'`逐字比對會被這個空格擋下——這不是單一個案，是系統性搜尋失效，絕大多數姓名搜尋先天上都搜不到。

**教練原話**：「誰知道要空格？」——使用者不可能知道資料庫存的是哪種格式，搜尋不該要求使用者猜對格式。

**修復方法**：`namecard-db/app.py`的`/find`跟`/`(首頁)兩個搜尋路由，把所有文字欄位的比對都從`欄位 LIKE ?`改成`REPLACE(欄位, ' ', '') LIKE ?`，查詢字串也同步用`query.replace(' ', '')`去空格再組`LIKE`樣式，資料庫欄位跟查詢字串雙邊都去空格，不管使用者輸入時打不打空格、資料庫裡存的格式為何，只要文字本身對得上就能命中。已套用到姓名/公司/職稱/分類/電話/Email/地址/關鍵字全部欄位，不只姓名。

**How to apply**：`namecard-db`若未來新增其他搜尋功能或欄位，一律比照`REPLACE(欄位, ' ', '') LIKE REPLACE(?, ' ', '')`寫法，不要用純`LIKE`——這個資料庫的姓名/公司欄位資料來源混雜(名片OCR辨識/BNI Connect官方匯出/教練手動輸入)，格式不統一是常態，空格只是目前發現的其中一種，未來若遇到全形/半形符號、大小寫等類似不一致問題，也該用同樣的「雙邊正規化再比對」思路處理。

Related: [[feedback_dont_reverify_stated_requirements_2026-08-28]]（同一輪對話裡發生的教訓，教練誤以為是資料缺漏而動怒，實際是這個搜尋bug）
