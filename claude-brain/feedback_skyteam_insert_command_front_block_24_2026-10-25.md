---
name: feedback-skyteam-insert-command-front-block-24
description: 教練說「插入顧問天團」＝把他念的專家插進人才軍火庫前面固定區（現 24 位），其他人往後擠；不夠再把 24 提高到 32
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8d5eaab3-4f7a-480a-bce3-ecd10c62b91a
  modified: 2026-10-24T17:04:56.692Z
---

教練 2026-10-25 01:04 預告口令：之後有高手來，他會說「**插入顧問天團**」，我就把那位插進人才軍火庫（skyteam/index.html 的 experts-data JSON）前面固定區，其他人往後擠。固定區現在是 24 位，不夠就由 24 提高到 32，由教練決定時機，我不自己改。

**Why:** 教練 10/25 先把前 16 位擴成 24 位（6c1ef60：黃國彰、楊仁豪、邱南寅、陳佩君、楊在珍、謝緯翔、許朝竣、傅恩平排 17～24，楊尚儒第 25，當天新增 8 位排 26～33）。他念名字常有諧音錯（江德豪＝楊仁豪、邱乃穎＝邱南寅、沈佩君＝陳佩君、黃國章＝黃國彰、楊再珍＝楊在珍、謝偉祥＝謝緯翔、許朝俊＝許朝竣），照規則先對名單、不確定先問。

**How to apply:**
- 先在 135 位名單與策展名冊對名字；對得上的用既有個人網頁，找不到才問，不要瞎搜。
- 新專家插在固定區最後一位（現為楊尚儒之後）、其餘維持原順序；JSON 用 `json.dumps(ensure_ascii=False)` 整段回寫（讀回與原文一致，已驗證）。
- 改完 commit、push，從線上頁面讀回順序確認。
- 名單沒有的新專家不會自動建卡片（skyteam_link_expert.py 只補連結），要手動加。

相關：[[project-skyteam-identity-labels-chapters-six-columns-2026-10-24]]、[[project-skyteam-auto-link-expert-and-footer-audit-2026-10-24]]
