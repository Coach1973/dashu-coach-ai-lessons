---
name: project-module-kit-new-project-menu-2026-10-14
description: 教練 10/14 要的「開新專案先給預設全勾功能清單＋送出資料自動接到教練」已上線：module_kit.py、模組庫、works-form.js、上架自動接線、兩條反射；模組化下一步 4 項等教練一句話
metadata:
  node_type: memory
  type: project
  originSessionId: a4cae501-0a37-4400-8ff5-f8796bc819ff
  modified: 2026-10-14T01:45:47.442Z
---

教練 2026-10-14 原話：百人導師那套底層邏輯（自助建檔＋專屬連結＋後台）要能套到各分會、校友會、遊戲；「之後任何新建類似底層邏輯的網站，是不是我都不用再提醒，它自動就會套用？」「建立專案時，直接提供清單詢問……預設全部勾選，我不需要再手動取消」「上架作品裡有『送出資料』，是不是也能自動串接，使用者送出我就一定收到」。

**已上線（10/14 上午，commit c4ed811da 等）：**
- 模組目錄（唯一真相源）：`knowledges/模組庫_大樹標準功能.md`，10 個模組各有範本與驗收方式。
- `python3 scripts/module_kit.py menu "專案名"`：開新專案第一個回覆就給這張清單（預設全勾）；`check <slug>` 交付前檢查；`audit` 全站表單稽核（應為 0）；`wire <slug>` 自動接線。
- 共用表單元件 `event-signup/static/works-form.js`：`<form data-works-form="slug">`＋script → /api/works/contact → 活動報名即時通知群；欄位 name/phone/email/item/message，其他有 name 的欄位併進留言；頁內寫 `works-form: skip` 才是刻意不接。
- `curation_process.py` 兩條上架路都呼叫 `wire_forms()`，結果寫進上架通知。
- 反射 `R-NEW-PROJECT-MODULE-MENU`（排第 1 條，避免被每次最多 3 條擠掉）、`R-FORM-USE-WORKS-FORM-MODULE`。

**Why:** 教練一再口頭交代「這個也要後台／要接通知」，同一套邏輯重寫了 6 份名冊、5 支一次性報名接口、3 套短網址；10/03 KR 提問牆因為沒接資料庫，提問全部遺失。

**How to apply:** 教練說做新網站／名冊／活動頁／比照某套 → 先 menu 清單；寫表單一律用 works-form.js；不要再開新的一次性報名接口。模組化下一步（名冊引擎＝tut_team.py 設定檔化、預約引擎、通用短網址、報名接口收斂）在報告 `knowledges/2026-10-14_一週盤點與模組化報告.html` 第六節，等教練說「照做」，建議從名冊引擎開始。相關：[[feedback_works_forms_go_to_event_signup_group_2026-10-10]]、[[feedback_new_admin_urls_auto_register_coach888_2026-10-10]]、[[reference_bni_member_personal_edit_link_two_repos_2026-10-14]]。
