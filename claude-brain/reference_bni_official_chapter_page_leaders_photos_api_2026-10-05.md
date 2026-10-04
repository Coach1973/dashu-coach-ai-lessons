---
name: reference-bni-official-chapter-page-leaders-photos-api-2026-10-05
description: BNI 官方分會頁（bnitainan.com.tw）的領導幹部名單與大頭照可不登入、不開瀏覽器用指令取得；同步腳本 sync_official_photos 與重跑時機
metadata:
  type: reference
---

BNI 大台南官方「分會資訊」頁 `https://bnitainan.com.tw/zh-TW/chapterdetail?chapterId=<加密代號>&name=BNI+真鑫` 的人員名單不在頁面原始碼裡，是頁面載入後用 `POST /bnicms/v3/frontend/chapterdetail/display` 再抓。參數：`pageMode=Live_Site`、`chapterId`（解碼後的字串）、`languageLocaleCode=zh_TW`、`website_type`、`website_id`、`mappedWidgetSettings`（後三個都在分頁原始碼裡），`planyourvisit=y`；不用登入、不用 cookie。回傳 HTML 裡「分會領導」每個人有姓名、官方職稱、照片網址 `https://bniconnectglobal.com/web/open/networkViewProfileImage/<代號>.jpg`（400×400，公開）。會員分頁（全部會員）是另一個呼叫，尚未做。

**已有分會代號**：真鑫 `fkNPn9jN1gqvY7Ko92g5vQ==`、真鑽 `zDV4rVioLOsObGZl1s4qJw==`（真誠人數少沒有領導名單；其他分會代號從官方「尋找分會」或各分會網站連結的 `ChapterId=` 取得）。

**同步腳本**：`github_repos/bni-chapters/sync_official_photos_2026-10-05.py`——本人自己上傳的照片絕不覆蓋、官方換照片重跑才更新、官方頁偶爾回傳不完整（真鑫曾只回 1 人）會自動重抓。領導換屆或有人換 BNI Connect 大頭照時重跑一次（事件到了才跑，不排輪詢）。

**Why:** 教練 10/05 問「領導幹部加委員會的照片，可不可以移植過去、直接同步」；另外截圖鎖（教練明令未經同意不截圖）擋下時，用 `javascript_tool` 讀 DOM、`read_network_requests` 看介面比截圖省流量也更準。
**How to apply:** 往後要官方分會頁的人員資料（名單、職稱、照片）先走這支腳本或同樣的介面，不要叫教練一張張存照片、不要截圖。
