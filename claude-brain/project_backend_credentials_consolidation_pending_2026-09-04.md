---
name: project-backend-credentials-consolidation-pending
description: coach888「後台系統帳密集中」任務的存放位置決策——教練裁示存Mac本機、直接問小龍蝦
metadata: 
  node_type: memory
  type: project
  originSessionId: 89e4937c-c840-4c0c-bc46-68785a6d6bbf
  modified: 2026-09-04T14:30:44.898Z
---

教練確認「後台系統帳密集中」任務對應的是coach888作品一覽（非其他系統），已盤點11個帶登入的後台系統。存放位置教練2026-09-04裁示：**存放在Mac本機（不是coach888公開repo，也不是獨立網頁），教練需要密碼時直接問小龍蝦就好**。

**Why**：coach888是公開GitHub repo，帳密不能直接寫進頁面（先前AskUserQuestion提過三案：只列帳號+密碼另存私密憑證檔／整個repo改私有／帳密清單另建獨立私密頁面），教練選的其實是第一案的精神——密碼不上網頁，改成口語化查詢入口。

**How to apply**：
1. 實際的11個系統帳密清單尚未彙整成單一檔案（先前只完成「盤點哪些系統有登入」，密碼明碼本身多數要另外查證，部分系統只存加密雜湊AI讀不出明碼）。下次有時間應建立`路徑大全_憑證層.md`底下的「coach888後台系統帳密」小節，逐一補齊帳號/密碼（讀不出明碼的要重設或標記）。
2. 這份清單只能寫在Mac本機的`路徑大全_憑證層.md`（本來就是權限受限、不進公開repo的檔案），不可外流到coach888或任何公開頁面。
3. **小龍蝦（main agent）需要知道**：教練若在LINE/Telegram問「XX後台密碼是多少」，答案來源是Mac本機的`路徑大全_憑證層.md`，小龍蝦本身工具權限受限（no fs/exec，見`hooks/rule-reminder`的scope設計），實際上要嘛這份清單要用某種方式讓小龍蝦讀得到（例如放進小龍蝦有讀取權限的知識庫路徑），要嘛教練問的時候由軍師代答。**這個技術細節本場尚未落實**，只是決策已拍板，下次建置清單時要一併確認小龍蝦讀不讀得到這份檔案。

相關：[[feedback_public_admin_separation_default_2026-09-04]]
