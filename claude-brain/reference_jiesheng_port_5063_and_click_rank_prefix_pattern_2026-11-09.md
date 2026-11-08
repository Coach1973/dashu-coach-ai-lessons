---
name: jiesheng-port-5063-and-click-rank-prefix-pattern
description: "結繩戰報真正埠是 5063（app.py 預設/README 寫 5061 是錯的，5061 是 peipei-event）；網頁要加「最常點排行」就照 worksmap:: 前綴抄 coach888 計次接口"
metadata:
  node_type: memory
  type: reference
  originSessionId: 79fb7143-ff53-42af-bf83-e2956a38e953
  modified: 2026-11-08T19:48:25.027Z
---

結繩戰報（rpl-workshop.bymyway.com/admin，程式 `workspace/jiesheng-report`）實際跑在 **5063**（`.env` 的 JIESHENG_PORT）；app.py 預設值與 README 寫 5061，但 5061 是 peipei-event，別去 curl 5061 驗證。改完用 `launchctl kickstart -k gui/$(id -u)/com.coach.jiesheng-webapp` 重啟；公開網址帶中文參數要 URL 編碼，否則回 400。

「分類收合＋我最常點排行」做法（大樹作品分類表 works-map 已實作，技法庫 R）：沿用 coach888 伺服器的 `/api/coach888/click` 與 `/api/coach888/click-counts?prefix=`，網址前加專屬前綴（works-map 用 `worksmap::`，my-tools 用 `mytools::`），並在 `event-signup/app.py` 的 click-counts 不帶 prefix 分支把新前綴排除，否則會擠掉大樹作品集自己的前 10 名。收合狀態只存瀏覽器 localStorage。

**Why:** 5061 撞埠的錯誤寫在 README 與預設值，下一個人驗證會打到別的服務；前綴排除漏掉會讓兩邊排行互相污染。
**How to apply:** 驗證戰報用 5063 或公開網址；新頁要排行就加新前綴＋改排除清單，產頁程式見 `scripts/build_works_map.py`。
