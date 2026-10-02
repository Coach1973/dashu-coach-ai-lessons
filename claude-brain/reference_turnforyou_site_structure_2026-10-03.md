---
name: reference-turnforyou-site-structure-2026-10-03
description: 為你轉身(turnforyou)導師席改人的結構坑：資料有三處、inline-data才是真的、觀眾席獨立、席次id綁推薦路徑；瀏覽器會快取舊404圖
metadata:
  node_type: memory
  type: reference
  originSessionId: d0899bc0-b332-4923-84c8-df175ed04000
  modified: 2026-10-02T16:00:59.308Z
---

站在 `~/github_repos/turnforyou`（非 git，直接被 event.bymyway.com/curated/turnforyou/ 供應，改完即上線；改前自己 cp 成 `.bak-日期`）。

改導師席（8 席）要動的地方：
- **`index.html` 內 `<script id="inline-data">window.__C__={data:{...}}`** 才是畫面實際用的資料；`data.json` 只在沒有 inline-data 時才讀，但仍要同步改（開頭是 `{data:` 不是合法 JSON，要先補引號解析）。`FALLBACK`（JS 裡舊示範名）與 `editor.html` 不用動，歷史上也都沒動。
- 席次 `id` 同時決定畫面顯示的「SEAT 0X」、申請表勾選項，以及 `PAIN` 路徑（「選三個條件看路徑」）推薦誰：換人或重排後要順手重配 `seats:[a,b]`。
- **觀眾席 `<script id="audience-data">` 獨立**，同一人不要同時在導師席與觀眾席；升降級時互相搬。
- 文案「八位／八張椅子」散在十多處（meta、hero、各段落）；場景圖 alt 寫的是圖裡真的有八張椅子，不要改。
- 照片：`img/mentors/<拼音>.jpg`，3:4、900×1200；來源優先用 mentor100 DB（`~/github_repos/mentor100/static/uploads/<photo_filename>`）。

**How to apply**：教練說「把某某放進導師席／換掉虛擬的」→ 先查 mentor100 DB 有沒有此人；沒有就用教練貼的文字資料＋公開頁，LinkedIn 要登入、Threads 的 og:image 可抓。瀏覽器曾快取舊的 404 圖，驗證用 `fetch(src,{cache:'reload'})` 排除，伺服器端用 curl 看 200＋content-type。
