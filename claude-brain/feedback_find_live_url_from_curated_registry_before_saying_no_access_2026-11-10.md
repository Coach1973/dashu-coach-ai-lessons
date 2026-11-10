---
name: feedback-find-live-url-from-curated-registry-before-saying-no-access
description: 教練丟 TAVA 出圖清單網址＋要換圖＝網頁早已自動上架在 event.bymyway.com/curated/<slug>/，倉庫 ~/github_repos/<slug>/；先查 curated_sites_registry.json 與 curation_uploads/processed，不准改本機副本還說「沒權限上傳」
metadata:
  type: feedback
---

2026-11-10 朱志成頁：教練丟 tava-ai.com 出圖清單網址，我出完圖卻把圖換在本機副本，還對教練說「沒有上傳權限」；其實 16:04 上架程式已把網頁自動發布到 https://event.bymyway.com/curated/zhu-zhicheng/（倉庫 ~/github_repos/zhu-zhicheng，registry 有記錄），我第一次搜尋就看到 processed 裡的 zip 卻沒連起來。教練罵「雞同鴨講」。

**Why:** 把教練給的網址（TAVA 出圖清單頁）當成網站本體；沒走 bigtree-web-edit 的「找到檔案，不猜」第一步。

**How to apply:** 教練說換圖／改字＝先查 `event-signup/curated_sites_registry.json`（用人名 slug）與 `curation_uploads/processed/` 找已上架網址與倉庫，直接改 `~/github_repos/<slug>/` 並 push，不等教練給網址；絕不說「沒權限」。改頁面文字時用正則只動 HTML 文字節點、跳過 `<script>`/`<style>`，否則會弄壞 JS 內的字串（這次證書照因此一度壞掉）。出圖清單 TAVA 頁的圖位用 data-slot，換成內嵌 base64 webp 即可。見 [[reference_swap_slot_images_after_publish_flow_2026-10-30]]。
