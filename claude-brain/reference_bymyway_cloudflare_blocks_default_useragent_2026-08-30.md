---
name: reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30
description: event.bymyway.com前面的Cloudflare會擋掉沒有瀏覽器User-Agent的HTTP請求(403)，任何自動化腳本fetch這類bymyway子網域都要注意
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4df163f9-7212-4a42-948a-b7105107ac31
  modified: 2026-08-30T08:46:14.862Z
---

`event.bymyway.com`（以及推測其他走同一組Cloudflare設定的`*.bymyway.com`子網域）會擋掉沒有瀏覽器樣式User-Agent的請求，回傳403 Forbidden。

**發現經過**：把`agents/bni_tainan/scripts/sync_calendar.py`的抓取來源從`tainan-calender.netlify.app`改成`event.bymyway.com/tainan-calender/`後，腳本原本用`urllib.request.urlopen(URL)`（預設送出`Python-urllib/3.x`這個UA）直接403失敗；改用`Mozilla/5.0`當UA的`urllib.request.Request`就正常。curl實測驗證：`curl -A "Python-urllib/3.11" ...` → 403，`curl -A "Mozilla/5.0" ...` → 200，證實是UA字串本身被擋，不是別的原因（兩邊回應內容本身逐位元組相同，排除掉是內容差異的可能）。

**Why**：Netlify預設不擋這類UA，`bymyway.com`系列子網域顯然有Cloudflare WAF/bot防護規則在擋非瀏覽器UA——這是把資料抓取來源從Netlify換成bymyway自架時容易踩到的隱藏差異，只看HTTP狀態碼測試（如只测`curl -sI`不帶UA參數）不會發現，因為那類快速手測往往剛好用的是會被放行的工具（如curl預設UA本身也可能被擋，需視Cloudflare規則細節而定，穩妥做法一律測試時明確指定UA比對兩種結果）。

**How to apply**：任何新寫的Python/腳本要用`urllib.request`／`requests`等程式化方式抓取`*.bymyway.com`底下的頁面（不是透過瀏覽器/claude-in-chrome操作），一律要帶上瀏覽器樣式的`User-Agent`header（如`Mozilla/5.0`），不能依賴函式庫預設值。若之後遇到對bymyway子網域的自動化請求無故403，優先懷疑這個原因，不用重新排查半天。

Related: [[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]（這整批Netlify遷移任務的主記憶）
