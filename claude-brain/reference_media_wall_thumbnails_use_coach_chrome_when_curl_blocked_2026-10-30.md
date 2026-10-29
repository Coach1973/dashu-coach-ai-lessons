---
name: reference-media-wall-thumbnails-use-coach-chrome-when-curl-blocked-2026-10-30
description: 媒體牆／連結卡要補縮圖：curl 被 Cloudflare 擋（403「Just a moment」）時改用教練自己的 Chrome（claude-in-chrome）正常開頁抓 og:image；下載放獨立空資料夾、python -I 解析；Apple Podcast 封面用 itunes lookup API
metadata:
  type: reference
---

coachwu 頁媒體牆（event.bymyway.com/curated/coachwu/ ，倉庫 ~/github_repos/coachwu）10/30 補 7 張純文字卡縮圖（`a1711e5`）的做法，下次新增媒體卡照走：
1. 先 curl 抓原網頁找 og:image；**看雜誌（watchinese.com）與 Dcard 對 curl 回 403 驗證頁（Cloudflare）——不繞過**，改用教練的 Chrome（`mcp__claude-in-chrome__*`，先 list_connected_browsers 確認 Mac 本機、用完關分頁）正常開頁，在頁面裡讀 og:image，再 curl 帶 Referer 下載圖檔本身（圖檔沒擋）。內建瀏覽器窗格只給 localhost 預覽（有反射擋）。
2. Apple Podcast 封面：`https://itunes.apple.com/lookup?id=<節目id>&entity=podcast` 的 artworkUrl600。正方形封面放進 16:9 縮圖＝模糊放大當底＋正方形置中圓角（PIL）。海報類直角裁切到標題＋人像（16:9）。
3. 下載的圖各放獨立空資料夾、處理程式放另一個資料夾、`python3 -I` 執行；轉 webp 640x360 內嵌（`<div class="mth"><img src="data:image/webp;base64,..." alt=標題></div>`，取代 `<div class="mth type"><span>…`）。
4. 成品拼成一張聯絡表親眼看（截圖鎖：教練未同意不截圖，用數字量版面＋看圖檔本身）。

相關：[[reference_delegate_to_xiaolongxia_openclaw_agent_and_run_img_list_2026-10-30]]（同頁 4 張 AI 示意圖）。
