---
name: feedback-register-admin-url-use-houtai-section-2026-11-03
description: 新後台網址登記大樹作品集要用 --section houtai（後臺系統）；預設的 baoliu（活動後台）不在 Stop 鎖稽核的可見分類裡，會被判「新缺漏」
metadata:
  type: feedback
---

11/02 做 /skyteam/admin 時，照執行細則 N10 預設登記到「活動後台」(baoliu)，收尾的 coach888 結構性稽核鎖卻判「新缺漏」——因為稽核只看「大樹常用／後臺系統(houtai)／bymyway自架版」三個教練實際會看的分類（`scripts/audit_coach888_coverage.py` 的 VISIBLE_SECTIONS）。

**Why:** 登記程式預設 baoliu 與稽核可見分類不一致，等於每次新後台都會多跑一輪補救。
**How to apply:** 新後台／管理頁登記時直接 `python3 scripts/coach888_register_admin.py <網址> <名稱> --section houtai`；讀回確認用 `--list`。相關 [[project-skyteam-unlisted-pool-admin-2026-11-02]]
