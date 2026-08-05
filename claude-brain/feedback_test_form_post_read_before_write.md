---
name: feedback-test-form-post-read-before-write
description: 用curl測試「整批覆寫」型的表單POST(如update_chapter)前，一定要先讀出該筆資料現有的完整欄位值再送出，漏填的欄位會被覆寫成空白
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a7a813d3-3d3a-47de-831f-20836ed149a6
  modified: 2026-08-05T01:37:55.216Z
---

測試bni-chapters後台「顯示/隱藏傳統區塊」勾選框功能時，直接用`curl -X POST /admin/chapters/1/edit -d "name_zh=...&status=..."`送出一個只填了3、4個欄位的測試表單，忘記這個路由的後端邏輯是`db.update_chapter(conn, chapter_id, fields)`整批覆寫——沒有在POST body裡的欄位，Python層`request.form.get(x, "").strip()`會直接拿到空字串存進資料庫。結果真誠分會的Hero標題/Hero說明/參訪須知標題與說明/頁尾標語全部被我的測試指令清空。

**Why:** Flask的表單處理常見兩種模式：①只更新有送來的欄位(PATCH語意) ②整批覆寫全部欄位(PUT語意)。這個系統是②，但我下意識當成①在測試，沒有先確認後端邏輯就對正式資料庫送出不完整的請求。

**How to apply:** 任何要用curl/腳本測試「編輯表單」的POST路由前，先做兩件事：①查看對應的view function，確認是整批覆寫還是局部更新 ②如果是整批覆寫，先GET現有資料把所有欄位值讀出來，測試POST要帶上全部欄位（只改要測的那一個），不能只填「這次想測的欄位」就送出。發現覆蓋後要立刻查有沒有原始種子腳本(如`seed.py`)或其他來源能救回正確值，不要留著空白不處理。

Related: [[project_bni_chapters_public_launch_2026-08-03]]
