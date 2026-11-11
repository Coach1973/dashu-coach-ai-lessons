---
name: feedback-live-page-change-request-means-push-no-ask
description: 教練給 event.bymyway.com 線上網址並說改／換＝要上線，改完驗證就直接 push，不准再問「要不要推」
metadata:
  node_type: memory
  type: feedback
  originSessionId: 902ac299-059b-4567-a781-4b0634de8147
  modified: 2026-11-11T12:07:50.414Z
---

教練貼線上網址叫我改（費用、換照片、修 bug），改完直接 git push 上線並驗證線上版，不問「要不要推」。

**Why:** 2026-11-11 金門私廚頁改費用＋換主廚照，我 commit 後停下問「回覆『推』才 push」，教練罵「推什麼推？不推幹嘛叫你做？」。交辦線上網址的修改本身就是上線授權；之前 bni-story 的「推」門檻是教練當場要先看過才推的特例。

**How to apply:** 交辦對象是已上架的線上網址（event.bymyway.com/curated/...）→ 改完、親眼驗證（看圖／量 DOM）→ 同輪 push → 查線上 Content-Type／內容，回報憑證。只有「新作品首次公開」或教練明講要先看，才先給本機預覽。見 [[feedback-no-pre-ask-routine-authorized]] 類規則（N2）。
