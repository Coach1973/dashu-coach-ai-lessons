---
name: project-bni-chapters-member-selfsubmit-2026-08-27
description: bni-chapters新增會員自助送出簡介機制(真誠分會示範)，比照mentor100第一階段(送出即自動上架非人工審核)，9分會共用同一套後端
metadata: 
  node_type: memory
  type: project
  originSessionId: c7607605-ee07-4bef-b9a8-5b81b31cd12d
  modified: 2026-08-27T11:07:40.094Z
---

2026-08-27教練交辦：真誠分會(bni-chapters, slug=`sincere`)要讓會員自己建立資料檔案，比照`mentor100`百人導師計劃的**第一階段**設計——不是mentor100現在的「申請→教練產生連結→人工審核上架」版本，是更早那版`/join`公開表單：填了就直接寫進資料庫、立刻出現在頁面上，不經審核。

**技術實作**：新增`chapter_members`表(欄位含chapter_id/name/company_title/role_tag/bio/photo_filename/9組link+label/edit_token/source)，`/<slug>/join`(GET+POST)、`/<slug>/join/thanks`、`/<slug>/join/edit/<token>`(GET+POST自助修改)、`/<slug>/join/edit/<token>/delete`(自助刪除)。照片處理(EXIF轉正/縮圖1200px/JPEG品質85)+honeypot+IP rate limit(5次/小時)防灌水，直接從`mentor100/app.py`舊commit(`7072acc~1`)的`_process_and_save_photo`等函式移植過來，行為完全一致。後台`admin_edit.html`新增夥伴清單，僅供管理員刪除違規/垃圾內容，非審核關卡。

**Why：** chapter_members表用`chapter_id`分流，路由用`/<slug>/join`模式，代表**這套機制天生就是9個分會共用同一份程式碼**，不像mentor100是單租戶。教練原話「驗證流程沒問題後，同一套機制複製到其他8個BNI分會站台」——不需要為其他8個分會另外寫程式碼，只要對應分會頁面(`chapter.html`)已經包含「分會夥伴」區塊(已經是共用模板，9分會自動都有)，機制就已經對全部分會生效，唯一要做的是**教練驗收真誠分會沒問題**。

**How to apply：** 之後若教練說「其他分會也要這個功能」，先確認chapter.html/join系列模板是否已涵蓋該分會(是，因為都吃同一個`chapters.db`+同一份Flask app)，不用重新開發，只需要跟教練確認驗收通過即可視為全部分會同步完成。若要加「人工審核」關卡(教練提過的下一步)，可比照mentor100 `mentors.status`(draft/published)欄位的做法，加`chapter_members.status`欄位。

commit `44fc3dd`(bni-chapters repo)，已用本機測試port(5099)完整跑過送出/自動上架/自助編輯/自助刪除/跨分會隔離/honeypot/驗證錯誤/後台刪除全部通過，才重啟正式服務(port 5064)並用瀏覽器直連`chapters.bymyway.com`驗證正體中文顯示正確。

Related: [[project_bni_chapters_public_launch_2026-08-03]]（既有bni-chapters系統架構背景）、[[project_mentor100_review_gated_signup_2026-08-08]]（mentor100後來改成人工審核版的脈絡，兩者是同一套自助送出邏輯的前後兩個階段）
