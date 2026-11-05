---
name: feedback-skyteam-photo-use-page-first-image-2026-11-05
description: 人才軍火庫補照片＝直接用完成版個人網頁首頁第一張照片（程式已自動），不准翻原始照片、做縮圖總表瞎找；教練 11/05 嫌浪費額度
metadata:
  type: feedback
---

教練 11/05 13:06 罵：江睿翔、薛德民、楊曉熹三位「照片待補」，我去翻原始照片資料夾、做縮圖總表、裁圖、挑半天，「浪費我的錢和額度」。完成版網頁首頁第一張本來就是本人照。

**Why:** 做好的個人網頁第一張內嵌照片＝教練認定的本人照；其他資料夾裡的圖是素材，不是答案。
**How to apply:** `event-signup/skyteam_pool.py` 現在 `add`／`auto`／`set-image <slug>`（不給檔案）都自動取 `~/github_repos/<slug>/index.html` 第一張 `<img src="data:image…">`（函式 `page_first_image`），已上架的要換照片就用該函式讀出來寫回 experts-data。看到「照片待補」第一個動作＝`set-image <slug>`，不要自己找圖。教練口頭點名上架（含排進前 N 位）＝一次做完：照片、`publish --to front`、讀回線上順序，skyteam 倉庫 933e6ed、bd6071b 為首例。相關 [[project-skyteam-unlisted-pool-admin-2026-11-02]]、[[feedback-skyteam-insert-command-front-block-24-2026-10-25]]
