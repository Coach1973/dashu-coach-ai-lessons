---
name: reference-rongtree-guest-form-fill-from-personal-page-with-photo-2026-11-05
description: 榮樹下來賓沒填資料表時，教練要我用來賓個人頁面補：event.db 的 rongtree_guest_forms、用 rongtree_guest.save()/直接 UPDATE、一定要連照片一起補、再 build_card；11/05 楊曉熹、鍾俊榮兩位實測
metadata:
  type: reference
---

教練 11/05 定：老人家不習慣寫資料表沒關係，訪談後（或前）由我們從他的個人頁面補。表在 `workspace/event-signup/event.db` 的 `rongtree_guest_forms`（token＝行事曆 `教練行程總表.json` 該場的 `form_token`；已有空殼就沿用同 token）。

做法：①備份 event.db；②資料全取自個人頁面（不編造；電話等頁面沒有的留空，`save()` 會擋空電話所以空殼用 sqlite UPDATE）；③`save(token, ev, payload, ip, None)`（ev＝{id,date,start}）；④**照片一定一起補**：從頁面抽第一張真人像，轉 JPG 放 `rongtree_uploads/<token>.jpg`，UPDATE `photo_file`——11/05 我第一次只存文字，教練問「照片為什麼沒放」；⑤`rongtree_guest.build_card(token)`（約 1 分鐘，狀態變 done）。來賓卡網址要簽章，我沒法直接 curl 驗，只能讀 DB。

**Why:** 教練不要來賓自己填、不要搬運；**How to apply:** 教練貼來賓頁網址或說「補來賓資料」→ 照上面 5 步一次做完含照片。相關：[[feedback_works_forms_go_to_event_signup_group_2026-10-10]]
