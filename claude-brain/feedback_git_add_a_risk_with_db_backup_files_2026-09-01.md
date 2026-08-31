---
name: git-add-a-risk-with-db-backup-files-2026-09-01
description: git add -A可能繞過.gitignore的*.db規則誤commit含真實個資的.db.bak備份檔，commit前先git status檢查異常檔名
metadata:
  type: feedback
---

在bni-chapters repo用`git add -A`時，誤把一個舊的`chapters.db.bak-before-netlify-link-update-20260830-164330`備份檔commit進去——這個repo的`.gitignore`寫`*.db`排除資料庫，但這個備份檔名是`.db.bak-...`副檔名不完全符合`*.db`的萬用字元規則，繞了過去。檔案含7筆真實會員個資（姓名/電話/Email）。發現後立即`git rm --cached`+補`.gitignore`規則+新commit修復，repo本身是private（`gh repo view --json isPrivate`確認），曝露風險有限，但原則上任何含真實個資的資料庫備份都不該進版控。

**Why**：`git add -A`會抓取工作目錄裡所有變動，包含早於本次任務就存在、跟本次改動無關的遺留檔案；`.gitignore`的萬用字元規則不會自動涵蓋所有變體檔名（`*.db`不擋`.db.bak-xxx`），這種落差不會有任何警告，commit完全靜默成功。

**How to apply**：在含真實使用者資料的repo（bni-chapters/team-bymyway/namecard-db等有姓名電話email的專案）執行`git add -A`前，先`git status --short`肉眼掃一眼新增/修改清單，看到任何`.bak`/`.old`/`.dump`/`.sql`/日期字尾這類非預期的資料檔名就先排除，不要無腦全加。跟[[feedback_data_move_du_sh_verify]]同一種「批次操作前先看內容」的精神，只是這次是git版控情境。
