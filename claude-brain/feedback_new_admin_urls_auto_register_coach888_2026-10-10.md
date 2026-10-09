---
name: feedback_new_admin_urls_auto_register_coach888_2026-10-10
description: AI 做出任何新的管理／編輯／刪除網址，當場收進教練的「大樹作品集」(coach888)；教練記不住網址，那是唯一找得到的地方；沒收錄是 bug
metadata:
  type: feedback
---

教練 2026-10-10 兩次講：新做的後台系統要自己去「我的大樹作品」增加；做了後台沒自動寫進去是 bug，AI 要檢討「為什麼還需要我提醒」。任何新的管理、編輯、刪除網址（含簽章的專用連結）都要自動收錄到大樹作品集，並寫進規則。

**Why:** 教練不可能記住那一長串網址，也沒有別處可找；信任遊戲「座位後台」做好後沒收錄，他當場抓到。
**How to apply:** 一行 `python3 scripts/coach888_register_admin.py <網址> <名稱>`（預設「活動後台」，可重複執行，先備份、寫完核對）；已寫成執行細則 N10＋反射 `R-NEW-ADMIN-URL-REGISTER-COACH888`（寫新後台路由時當場跳出）＋大樹作品 SOP＋bni-chapters CLAUDE.md。同類錯再發生＝改反射刺激或升級成擋下，不要只加記憶。相關 [[feedback_event_sites_must_have_github_wired_into_pipeline_2026-10-10]]。

**短網址（教練 10/10 06:38 追加）**：管理／編輯／上傳入口的網址「一律做成短網址」再登記。做法＝用金鑰算一個固定短代碼（信任遊戲後台 `/game/a/<12字>`、策展上傳 `/u/<10字>`），舊長連結照樣有效；`coach888_register_admin.py` 網址超過 60 字會提醒。每位玩家個人的修改連結（`/game/invite/edit/<22字>`）是一人一把、只發給本人，沒動。

**同時要進 /vault（教練 10/10 06:44 抓到）**：教練找後台有兩個地方——大樹作品集（coach888）和 `event.bymyway.com/vault`（憑證總覽，要登入）。`coach888_register_admin.py` 現在預設兩邊一起登記（`/vault` 讀 `event-signup/vault_extra.json`，不用重啟）；有帳密的後台加 `--no-vault`，帳密自己補進 `app.py` 的 VAULT_ENTRIES 與 `路徑大全_憑證層.md`。

