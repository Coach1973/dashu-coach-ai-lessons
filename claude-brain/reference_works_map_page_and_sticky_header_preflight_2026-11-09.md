---
name: works-map-page-and-sticky-header-preflight
description: 大樹作品分類表（event.bymyway.com/curated/works-map/）的產生方式；page_preflight 對比誤報＝固定表頭太高（要壓在約 110px 內）
metadata:
  node_type: memory
  type: reference
  originSessionId: 8f79eed0-bd78-4fce-91c0-2072dc04862f
  modified: 2026-11-08T19:37:56.886Z
---

**作品分類表**：網址 https://event.bymyway.com/curated/works-map/ ，256 個作品分 9 類（教練 11/09 指定前四類：課程報名／顧問師天團＋人才軍火庫／工具技能／沒上架；其餘五類我補）。資料來源 `~/github_repos/all-works/data.json` ＋ skyteam `index.html` 的 experts-data；分類規則在 `workspace/scripts/works_map_classify.py`（明確名單優先→關鍵字→有沒有上架），產頁 `scripts/build_works_map.py <資料夾>`，再 zip 用 curation/upload（slug=works-map、kind=creation）。是快照，新作品要重跑才會出現；已收進大樹作品集 changyong（常用）。

**Why:** 教練睡前交辦，要一張看全部作品的分類表。

**How to apply:** 教練說「某作品放錯類」→ 改 classify 的名單重跑重傳。人才軍火庫連結（陳佩君換成 peipei1983）同日已改。

**踩到的坑（N8「更好的方法」）：** `page_preflight.js` 報「字看不清、對比 1.98」不一定是顏色真的淡——固定表頭（sticky header）高過約 110px 時，卡片字剛好捲到表頭底下，截圖取像素算成深色底，38～49 處誤報。解法：表頭壓矮（標題＋選單同一排、搜尋框移出表頭），不是亂改字色。
