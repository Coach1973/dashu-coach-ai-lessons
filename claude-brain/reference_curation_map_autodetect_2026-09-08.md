---
name: reference-curation-map-autodetect-2026-09-08
description: 策展SOP店家名冊卡片地圖自動化——伺服器端從網站原始碼正則抓地址+教練建議源頭做法（生成網站時就要求AI工具寫清楚地址）
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4a84abf4-a5fc-4064-97eb-aae7b57eeaf6
  modified: 2026-09-08T02:36:48.903Z
---

教練發現策展SOP(zip上傳建站)上架的店家，在大台南策展中心(tainan-shangquan)店家名冊卡片沒有Google地圖，每次都要自己手動開Google地圖搜尋、複製連結貼上。查證發現根因：自助登錄流程(`_provision_shop_placeholder()`，app.py)因表單本身就有地址欄位，一直都有自動地圖；但curation_process.py（zip上傳那條路）從沒抓過地址，卡片天生缺一個`shop-media`欄位（CSS是2欄grid，缺了地圖欄看起來就是版面沒填滿）。

**已修復（commit `065af870a`）**：`scripts/curation_process.py`新增`extract_address()`——用正則掃網站HTML找台灣地址格式(市/縣+路/街+號)，抓到就用跟自助登錄同款的query-based地圖embed(`google.com/maps?q=...&output=embed`，不需要API Key)自動插進卡片；抓不到就不顯示地圖，非致命降級。

**教練當場提出更根源的做法**：與其伺服器端事後用正則猜地址，不如在「生成網站」那一步（教練用TAVA AI/Lovart.ai/ChatGPT等工具做站的當下）就順手要求AI工具把完整地址用清楚文字寫在頁面上——這樣抓取才穩定可靠，一氣呵成。已寫進[[reference_curation_sop_2026-09-06]]第一步的補充說明。

**How to apply**：往後教練或AI幫忙生成店家網站時，提示詞裡加一句「請把完整地址（市+區+路+號）用清楚文字寫在頁面上」。若上架後發現卡片沒地圖，優先懷疑原始網站本身沒寫地址（不是抓取邏輯壞了），回頭跟生成網站的AI工具要求補上再重新上傳即可。

Related: [[reference_curation_sop_2026-09-06]]、[[reference_curation_sop_placeholder_autodetect_and_slug_fix_2026-09-06]]
