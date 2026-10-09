---
name: feedback-works-forms-go-to-event-signup-group-2026-10-10
description: 大樹作品頁任何聯絡／索取資料／送出介面，一律打 /api/works/contact，通知進「活動報名即時通知」群；不另開通知管道（教練 2026-10-10 裁示）
metadata:
  type: feedback
---

教練 2026-10-10 裁示：**所有大樹作品頁**只要有聯絡、索取資料、送出之類的介面，資料一律發到 Telegram「活動報名即時通知」群（教練＋佩佩老師＋bot，chat_id 在 `event-signup/app.py` 的 `TELEGRAM_REGISTRATION_GROUP_CHAT_ID`），邏輯跟活動報名一模一樣。

**Why:** 楊博士頁（hnv-cc）原本只放電話，教練要線上表單、不要靠打電話；他要所有作品的訪客留言都在同一個群看到，不想每個作品一個通知管道。

**How to apply:** 新作品要收訪客資料時，前端直接 `fetch('/api/works/contact')`（通用接口，存 `works_contact_leads` 表＋通知群），範例與細節見 `knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md` 的 2026-10-10 段與 `github_repos/hnv-cc/index.html` 的 `#lead`。不要另開 mailto／第三方表單／單一作品專屬通知。測試別對真實網址送出（會真的通知教練與佩佩老師），用 `event-signup/test_works_contact.py`。相關：[[reference_curation_sop_2026-09-06]]。
