---
name: reference-bni-member-personal-edit-link-two-repos-2026-10-14
description: BNI 分會夥伴的「專屬修改連結」≠ 後台編輯網址；後台已加一鍵複製，但 bni-chapters 與 team-bymyway 各有一份後台模板，改一處要同步改另一處
metadata:
  node_type: memory
  type: reference
  originSessionId: 1120f135-e197-43d6-997f-bdcf7a93f84a
  modified: 2026-10-14T01:17:56.608Z
---

- 教練問「後台編輯網址（`/admin/chapters/9/members/94/edit`）跟夥伴送出頁面的連結是同一條嗎」→ **不是**。後台那條要登入，沒登入會 302 到登入頁；夥伴自己的是 `/<slug>/join/edit/<edit_token>`（不用登入），token 在 `chapter_members.edit_token`。
- 原本 BNI 後台沒顯示專屬連結（AI 百人導師有），2026-10-14 補上：夥伴編輯頁頂端有「傳給○○的專屬修改連結」框＋複製鈕，分會後台夥伴列表每位有「複製他的專屬連結」。用 `_public_url` 補成 https。
- **兩份各自獨立的模板，要一起改**：`github_repos/bni-chapters`（chapters.bymyway.com，13 個分會共用一份模板，commit `fa36f74`）與 `github_repos/team-bymyway`（team.bymyway.com 第一、第二分會，`02af90d`）。教練原則：「這個網站有，其他的網站都得有」——改後台頁時先 `grep` 另一個 repo 有沒有同名模板。
- 測試方式：兩個專案都沒裝 pytest；用 `BNI_CHAPTERS_SECRET_KEY=test-secret BNI_CHAPTERS_DB=<複製的db>` 起 Flask 測試用戶端，`session_transaction` 設 `admin_scope="super"`（team-bymyway 用 `TEAM_SECRET_KEY` 與 `db.DB_PATH`）。

**Why:** 教練新增夥伴後找不到要傳給本人的連結，差點把後台網址傳出去。
**How to apply:** 教練問某夥伴的連結時，直接查 `edit_token` 組 `/<slug>/join/edit/<token>`，不要叫他去後台翻。
