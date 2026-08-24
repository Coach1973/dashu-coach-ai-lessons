# 軍師接力棒 · 2026-08-23 v123（Mac桌面版 Sonnet 5→Opus 5混用，大樹小講事件密集場：救回失蹤的雙寫程式碼、改期、自建管理後台、修好2次部署bug、抓出LINE綁定率低的真因並四點補強）

> 建立時間：2026-08-22 22:35 ~ 2026-08-23 22:36（台灣時間，跨日長場）
> 本棒執行者：Mac 桌面版 Sonnet 5（中途教練切換至 Opus 5）
> 上一棒：v122（同機前四日）
> 本棒主軸：**這一整場圍繞`bigtree-tw`(大樹小講)官網跟`event-signup`報名後台展開，從「救回一段消失的程式碼」開始，一路做到「教練自己就能管理活動、不用再靠AI改網頁」。過程中兩次因為自己改壞部署流程讓教練白扣額度，都當場拿「已知成功的樣本」逐項diff揪出真因並修好，同時把每個教訓寫回永久記憶。**

## 🎯 本場戰果

### 1. 🔴🔴🔴🔴 救回8/14寫好卻從未推送的報名雙寫程式碼
查明8/14曾在本機commit`3130b93`寫好`event.bymyway.com/api/register`雙寫邏輯，但**這個commit從未git push**——8/18另一台機器在缺這段程式碼的origin/main上加了新場次並推送，兩邊分岔一週沒人發現。`git merge`救回後confirm教練「推」，部署上線。**同一輪順手把這個問題結構性根治**：擴充`session_end_auto_push.sh`（原本只保護workspace自身），新增每輪對話結束自動掃描`~/github_repos/`全部22個站台repo，任何有unpushed commit就自動補推，用真實測試commit驗證過(`ai-fit`repo)確實會被抓到並自動推送。commit`763f7ab00`。

### 2. 🎯 大樹小講8/25台南場改期9/22＋場地改台南安平維悅酒店
教練口頭指示改期+換場地(7/29 AI微論壇同一場地，WebSearch查證地址)，時間/收費不變。同步修改bigtree官網+event.db+**意外發現的獨立微站`ai-fit`**(整站專為這場活動做，6處meta標籤+4處場地卡+深連結全部要跟著改)。真實Chrome雙頁預覽教練確認後上線。**發現原8/25已有4筆歷史報名，教練確認自行聯絡通知**。commit`d95e8b3`+`080ca32`。

### 3. 🎯🎯 大樹小講場次管理後台：event.db成唯一真相源
教練提出想要「自己能管理活動的後台」，軍師判斷**不新建系統**——`event.bymyway.com/admin`早就是完整後台，真正病根是場次資料同時活在「網頁原始碼」跟「event.db」兩份、必定會漏（8/22改期出包就是這樣）。做法：events表擴充欄位、新增`/admin/sessions`管理頁（新增/編輯/刪除/取消，有報名不給刪）、`bigtree_publish.py`一鍵發佈（資料庫→網頁→git→Netlify）、**教練本人按發佈不需AI再確認**。commit`bde5ae160`。

### 4. 🔴🔴 一鍵發佈踩雷2次，最終用「跟成功樣本diff」抓到真因
教練首次使用就連續失敗2次、額度白扣2次。第一次誤診為zip中文檔名UTF-8旗標問題（改用Python zipfile打包）；第二次拿08-22實測成功的zip逐項比對，才發現真因是**缺少目錄項**（zipfile自行走訪檔案不會寫目錄項，Netlify解壓需要），改回`git archive HEAD`+系統`zip`指令，並加上`_wait_until_live()`輪詢真正state=ready才算成功（原本誤把HTTP 200當成功）。commit`7a096531b`→`99ceb9cf5`，教訓寫入`feedback_netlify_headers_content_type.md`第7條：**有已知成功樣本時先diff，不要靠單一可疑現象推論**。

### 5. 🔧 LINE群發「發送失敗」查證：非bug，是官方帳號月額度用完
查證`@qaw8118h`(event-signup專用LINE帳號，跟龍蝦小助教是不同帳號)本月200則免費額度用滿(用LINE quota API確認)。`/admin/notify`新增即時額度顯示+「未綁定名單一鍵複製連結」功能，讓教練能繞過額度限制用簡訊等管道接觸8/21+8/22兩場49人中29位未綁定LINE的人。commit`b3a6900d9`。

### 6. 🎯 「掃碼時強調一定要發訊息」四點補強
教練提出解法後，查現有4個觸點（2張現場立牌+2個掃碼後網頁）全部沒有明確講出「LINE打開後還要自己按傳送」，線上報名頁按鈕文案「一鍵傳送」甚至可能誤導。已全部加上紅底警語，thanks.html文案同步修正。**待辦**：已印過的舊版立牌沒有新警語，需教練決定是否重印。commit`0753e0e41`。

## 📋 下一場直接開工任務
- **現場立牌是否重印**：詢問教練`qr/wheel-print.html`+`qr/checkin-print.html`的新警語版本要不要重新列印替換現場舊立牌
- **LINE推播額度**：約9/1重置，屆時可針對8/21+8/22未綁定的29人做精準補發提醒
- **大樹小講後台擴充**：教練表態長期要「所有活動都歸後台管理」，`ai-fit`這類單一活動微站尚未納入`site`欄位體系
- 承接舊待辦：ezPay「38人待問清單」剩8人資料待補齊（見主表）、bni-chapters「真誠分會」架構問題(擱置中)

## 🔑 本場關鍵檔案索引
- `event-signup/bigtree_publish.py`：一鍵發佈核心邏輯，含兩次修好的打包+輪詢驗證機制
- `event-signup/templates/sessions.html`+`_session_card.html`：場次管理後台頁面
- `event-signup/templates/notify.html`：未綁定名單+額度顯示
- `event-signup/qr/wheel-print.html`+`checkin-print.html`、`templates/slides.html`+`thanks.html`：四點警語補強
- `scripts/session_end_auto_push.sh`：新增github_repos全域unpushed commit自動補推
- 記憶：`feedback_netlify_headers_content_type.md`第7條、`reference_event_line_oa_push_quota.md`、`project_bigtree_session_admin_backend_2026-08-23.md`

---
