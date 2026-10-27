---
name: project-jiang-yilun-booking-tuesday-8pm-and-rongtree-backfill-2026-10-27
description: 江宜倫頁「預約老師」（每週二晚上8:00、works-form 通用接口進活動報名通知，未確認群組收到測試）＋榮樹下「已交資料」手動補來賓的做法（寫 event.db rongtree_guest_forms）
metadata:
  node_type: memory
  type: project
  originSessionId: 05c437a2-c3ff-4db4-808a-dbfaa2f87e47
  modified: 2026-10-27T09:09:45.031Z
---

**江宜倫預約（教練 10/27 00:03 要求「把榮樹下預約系統也複製一份給怡倫老師，只有每週二晚上 8 點，送出進活動報名即時通知」）**：`github_repos/jiang-yilun` 新增 `#book` 區（commit `ad43ec0`）：下拉選未來 8 個週二→姓名／電話或 Email／想聊內容→`data-works-form="jiang-yilun"` 走通用接口 `/api/works/contact`。沒做榮樹下的 `/api/rongtree/hold` 占位（只有一個固定時段）。日期從「明天以後」的第一個週二算起。語音「怡倫」＝江宜倫，頁面統一寫「宜倫」。

**Why:** 教練要求目前不存在的功能；他一貫要「送出就進活動報名群」（見 [[feedback-works-forms-go-to-event-signup-group-2026-10-10]]）。

**How to apply:** 真送出測過一次（資料有存、頁面成功），測試列已刪；**群組是否收到測試通知沒親眼確認**，下次先問。要改時段改 `index.html` 內 `bk-item` 那段 JS。

**榮樹下「已交資料」手動補來賓做法**（教練 10/26 22:17 要補林家旭等 6 位，因為他們沒交過表）：直接寫 `event-signup/event.db` 的 `rongtree_guest_forms`（token＝教練行程總表該場的 `form_token`，public=1，date／start 照教練給的日期，data JSON 十個欄位，photo_file＝`<token>.jpg` 放 `event-signup/rongtree_uploads/`），職稱與一句話取人才軍火庫／本人頁原文、不編造；公開 API `/api/rongtree/prep` 立刻看得到，不用重啟。event.db 不進 git。另見 [[project-rongshuxia-guest-form-card-prep-section-2026-10-14]]。
