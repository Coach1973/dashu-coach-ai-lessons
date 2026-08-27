# 軍師接力棒 · 2026-08-27 v141（Mac終端機 Sonnet 5，bigtree 8/28 EDM上線+報名頁LINE誘因文案定案+/slides多簡報支援+ezPay發票查證）

> 建立時間：2026-08-27 10:40 ~ 18:33（台灣時間，教練「總結」觸發收工）
> 上一棒：v140（聯想Windows，同日）— 與本棒在不同機器並行進行，互不衝突
> 本棒主軸：**教練提供8/28嘉義場正式EDM，補進歷史紀錄+報名頁上線；報名成功頁LINE加入誘因文案經三輪迭代定案並上線；event-signup簡報下載功能擴充為支援多份；查證林仁超/林智帆兩人ezPay發票紀錄；收工時教練交辦兩項新任務。**

## 🎯 本場戰果

### 1. bigtree-tw：8/28嘉義AI微論壇正式EDM上線（deploy `6a8fa70b`）
教練下載正式EDM(`export (3).jpg`)後，補進`archive/大樹小講_歷史講座紀錄.html`第21場+報名頁`index.html`場次資訊(原本只有停車場資訊，補上報名費100元園遊券制說明)，同步更新`event.db`。本機http.server+真實Chrome預覽驗證後，教練親口「就可以推了」，已推GitHub+Netlify並curl驗證正式站三處(EDM圖片/歷史紀錄頁/報名頁文字)皆生效。

### 2. Netlify額度校正+bigtree報名頁LINE誘因文案三輪迭代（deploy `6a8fb206c38ae66c7d2a843c`）
教練親自查真實帳單頁回報903.3/1000（換算約60次部署），已寫回`state/netlify_deploy_quota.json`供三機同步基準，commit `17e477920`。順勢處理教練提出的「明天40位嘉賓沒綁LINE，如何通知」問題：查證LINE/Telegram皆需對方先加好友/啟動bot才能觸達，電話號碼本身無法直接推播；三竹簡訊申請牽涉MID身分識別驗證+帳號建立，屬於軍師規矩上不可代辦的動作（帳號/身分驗證類），已誠實告知並提供替代思路。接著把這個洞察落地成**報名成功頁的LINE加入誘因文案**，教練逐輪修改定案：加LINE→活動前提醒→經確認出席後優先入場+免填資料通過抽獎資格審核（開場前10分鐘到場，逾時不保留）。bigtree_publish.py因只比對SESSION_DATES內容而誤判「已是最新」拒絕部署，改用手動`git archive HEAD`+zip+curl流程成功部署，此坑已寫入記憶`reference_bigtree_publish_hash_scope_2026-08-27`。

### 3. event-signup：/slides簡報下載功能擴充支援多份檔案（commit `8f65585ab`）
教練昨天(8/26)高雄場有兩份簡報要分享，查證發現`/slides`原設計一次只能提供一份檔案（自動模式抓今日日期、手動模式僅能指定一個檔名）。已改造`_resolve_current_slides()`回傳list、manual_file改存逗號分隔清單、`/slides/download`改成`/slides/download/<filename>`並驗證檔名在目前開放清單內才給下載（擋路徑穿越）、後台manual_file下拉選單改multiple可複選。用test_client+直接render_template雙重驗證通過（兩檔案各自200下載、路徑穿越404、不存在檔名404），測試後已還原DB原始設定，服務已重啟上線。教練選擇自己上後台操作(選項B)，已給操作步驟。

### 4. ezPay發票查證：林仁超(真鑽/旅行者企業社29412451)、林智帆(真鑽/鴻羽網路54082268)
先查本機3份離線發票資料庫皆查無結果，但**沒有先報告查證過程就直接問教練登入ezPay**，教練當場糾正「你的資料庫裡面應該要有啊」——已寫入記憶`feedback_report_offline_check_before_pivoting_2026-08-27`。教練給出正確統編後，本機CSV改用統編查到兩人完整歷史：林智帆備註明確寫「真鑽-智帆續約」確認身分，2026年至今皆無新發票；林仁超2026-01-03有一筆$26,000（教練說明是接任職務提前續約，非重複）。兩人皆確認可正常開立，教練尚未下令開立。

### 5. Trello connector澄清
教練透過`claude.ai/directory/trello`連接了Trello，詢問能做什麼。查證本session（Claude Code終端機/桌面版）的工具清單無Trello相關工具，已誠實告知claude.ai與Claude Code是不同產品、外掛連接不互通，若要用需回claude.ai對話框操作。

## ⚠️ 本場教訓

1. **查證沒找到結果時，要先口頭報告「已查過什麼、結果是什麼」，再問是否要換管道**——省略報告直接問教練做動作(如登入)，會讓教練誤以為AI沒做功課，即使AI其實已經查過。
2. **bigtree_publish.py的去重檢查只看SESSION_DATES內容，改其他區塊文案不會被偵測到**，遇到「明明改了卻說已是最新」要想到這個範圍限制，改走手動zip+curl流程。

## 📋 下一場開工先做

1. **真誠分會自助送出簡介機制**——本棒新任務，優先度最高，見待辦表詳細規格
2. **BNI Connect離會會員信用証查詢**——先問教練「信用証」確切定義再動手，不要瞎猜
3. MEMORY.md索引檔20.1KB逼近讀取上限，已拆背景任務`task_5332e76c`處理中，下次開工檢查是否完成
4. 承接v140待辦：教練商家驗證完成後的FB粉專pages_manage_posts授權後續
5. event-signup `/slides`多檔案功能上線後，教練若已自行上傳8/26高雄場兩份簡報，可主動確認是否運作正常

## 🔑 本場commit
`7dc3704`(8/28 EDM歷史紀錄+報名頁)／`17e477920`(Netlify額度校正903.3)／`fb127e5`(bigtree LINE誘因文案定案)／`8f65585ab`(/slides多檔案支援)／記憶`feedback_report_offline_check_before_pivoting_2026-08-27`+`reference_bigtree_publish_hash_scope_2026-08-27`(本次總結一併commit)

