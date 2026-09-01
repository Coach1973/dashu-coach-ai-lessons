---
name: verify-all-tables-not-just-main-schema-2026-09-01
description: 用假資料驗證系統畫面時，要窮舉所有資料表(含app.py動態建立、不在schema.sql的)，不能只看主schema，否則測試污染會殘留到正式站
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9b6d5e7c-c63c-44c9-ba78-b15d5ff918bb
  modified: 2026-09-01T00:11:18.944Z
---

真鑫分會戰情儀表板建置時，用真誠分會假資料跑過一次seed.py驗證Chrome畫面，只檢查了members/weekly_data有沒有清乾淨，漏了`app.py`動態建立(`CREATE TABLE IF NOT EXISTS`寫在app.py而非schema.sql)的`guest_list`表——這張表存的是「來賓姓名明細」，赫米斯後續重寫seed.py時完全沒碰到它，於是真誠分會的假來賓姓名(李美花/張育慈等)一路殘留到正式部署的`zhenxin.bymyway.com`，被教練發現「還把真誠分會的名單算在裡面，真的是很糟糕的一個品質」。詳見[[試金石案例69]]。

**Why：** 動態建立的表特別容易被忽略，往往是後來才加的功能，反而是使用者第一眼會看到的內容（這次就是「具體來賓是誰」這個最顯眼的區塊）。

**How to apply：** 用假資料驗證任何系統前，先窮舉這個系統實際用到的所有資料表(讀app.py/db.py找`CREATE TABLE`關鍵字，不能只看schema.sql)；驗證完後要清楚知道「哪些表被測試污染了」，不能只憑印象覺得「反正之後會被蓋掉」；多人協作同一個repo時，委派信要明確交代每一張表誰負責，不能預設對方會處理沒提到的部分。
