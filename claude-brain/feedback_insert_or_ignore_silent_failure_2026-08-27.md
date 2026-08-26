---
name: feedback-insert-or-ignore-silent-failure
description: SQL用INSERT OR IGNORE批次寫入卻不檢查rowcount，撞到既有資料時會靜默漏寫、零錯誤訊息
metadata:
  node_type: memory
  type: feedback
  originSessionId: 454fbcb4-70a8-4a88-832e-8ef2cbc35b65
  modified: 2026-08-26T16:33:32.395Z
---

2026-08-26匯入430位BNI Connect會員時，`parse_and_import.py`對查無既有資料的人用`INSERT OR IGNORE INTO cards (...) VALUES (...)`寫入正確的BNI分類(現任/前會員+分會)。其中4人(田伸強/林尹渰/王聖凱/朱正文)的合成`image_filename`剛好撞到資料庫裡已存在的一筆，`INSERT OR IGNORE`靜默跳過整個寫入——沒有拋錯、沒有log警告、程式輸出的統計數字也完全正常，教練是自己在`/find`搜尋頁上肉眼比對才發現這4人沒有BNI身分標記。無法百分之百還原歷史上撞名的確切成因(git只有一次commit紀錄，不像重跑造成)，重點是抓到「這個寫法本身就是一顆不會報錯的地雷」。

**Why**：`INSERT OR IGNORE`遇到UNIQUE衝突時，`cursor.rowcount`會是0，但沒人去檢查這個值，於是「應該寫入的資料」跟「真的寫入的資料」完全脫節，且外部完全看不出任何異狀（不像丟例外那樣至少會中斷程式）。

**How to apply**：任何用`INSERT OR IGNORE`（或`INSERT OR REPLACE`）處理「先查是否存在、不存在才插入」邏輯的批次寫入腳本，插入後一定要檢查`cursor.rowcount`——如果是0，代表撞到既有資料被跳過，這時要嘛改用同一把識別鍵做UPDATE補寫正確資料，要嘛至少log一筆警告讓人事後查得到，不能讓它悄悄過去。已修復的範例見`namecard-db/bni_connect_import/parse_and_import.py`的`main()`函式。

Related: [[project_namecard_manual_trigger_matching_design_2026-08-27]]
