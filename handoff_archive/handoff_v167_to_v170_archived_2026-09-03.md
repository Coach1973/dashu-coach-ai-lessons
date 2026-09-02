# 軍師接力棒 · 2026-09-02 v167（Mac終端機 Sonnet 5，教練待辦提醒系統正式部署上線）

> 建立時間：2026-09-02 17:12 ~ 17:26（台灣時間）
> 上一棒：v166（Mac終端機，名片系統來賓歷程+帳號審核+coach888批量搬移+RustDesk診斷）
> 本棒主軸：**教練說「動手做todo系統吧」，完成聯想軍師v165交辦的待辦提醒系統部署5步驟，全數真實驗證通過。**

## 🎯 本場戰果

聯想v165已寫好程式碼待Mac部署，本場正式執行：
1. `git pull`確認`todos`表schema/4個路由/`todo.html`/`todo_reminder_check.py`皆為最新。
2. 重啟`com.coach.event-webapp`，`db.init_db()`自動幫`event.db`補上`todos`表。
3. 真實HTTP測試：`GET /todo`回200；新增一筆測試待辦寫入DB成功；切換完成`completed=1`成功；刪除歸零成功。瀏覽器`get_page_text`確認頁面渲染正確（「特助主動提醒版」標題+空清單提示）。測試資料已清乾淨，正式站現為空清單。
4. 起初註冊OpenClaw cron `todo-reminder-check`每15分鐘檢查一次，比照`bni-credit-expiry-reminder`模式建立。**部署完成回報教練後，Stop hook守則#07 deterministic check攔下這個輪詢設計**，查證發現remind_at是已知的未來時間點，可以做到真正事件觸發：改成`/todo/add`當場用`openclaw cron create --at <remind_at>`排一個精確時刻的一次性cron（只查這一筆待辦id），`/todo/<id>/toggle`(完成時)+`/todo/<id>/delete`同步呼叫`cron delete`取消尚未觸發的提醒，`todos`表新增`reminder_cron_id`欄位追蹤。已刪除原本的每15分鐘recurring cron。
5. coach888正式站curl確認`event.bymyway.com/todo`連結存在。

**改事件觸發過程修好一個真bug**：launchd服務(`com.coach.event-webapp`)預設PATH只有`/usr/bin:/bin:/usr/sbin:/sbin`，Flask路由用`subprocess.run(["openclaw",...])`直接找不到指令；補絕對路徑`/opt/homebrew/bin/openclaw`後又因openclaw本身是node script、PATH仍找不到node而失敗；最後在`subprocess.run`額外傳入補齊PATH的`env`參數才成功。已寫入記憶`reference_launchd_subprocess_missing_path_2026-09-02`（其他launchd服務要shell out呼叫homebrew/node工具時可參考）。

**已用真實流程完整驗證事件觸發機制**：①單純測試`openclaw cron create --at`精確時間點觸發(用`touch`驗證檔案準時出現)②新增待辦帶remind_at→`reminder_cron_id`正確寫入資料庫→`openclaw cron show`確認排程存在③標記完成→cron正確被取消(`cron show`查無此job)④讓另一筆真的等到排定時間觸發→`reminder_sent`正確寫回1、Telegram真的收到通知、cron因`deleteAfterRun`自動消失。所有測試資料已清除，正式站`todos`表歸零。

已回信`cross-agent/inbox/lenovo/20260902-1725_mac-to-lenovo_todo-system-deployed-successfully.md`告知完成細節，原始委派信歸檔至`cross-agent/outbox/2026-09/`。

## ⚠️ 下一場開工先做
- 教練若已輸入真實待辦事項，可驗證一次性提醒cron是否有在排定的精確時刻正確送達Telegram。
- v161之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、12月主題培訓內容等）本場未觸及。

## 🔑 本場commit
`workspace`：`58b3f0e46`+`527e907ce`（部署+接力棒）→`0f241ce4f`（改事件觸發，含`event-signup/app.py`+`db.py`+`schema.sql`+`scripts/todo_reminder_check.py`）+cross-agent回信歸檔。記憶：`reference_launchd_subprocess_missing_path_2026-09-02`。

---

# 軍師接力棒 · 2026-09-02 v168（聯想Windows Sonnet 5，9/5+9/16活動FB行銷文案+9/5貼文已發5個粉專，含真實圖片發布首例）

> 建立時間：2026-09-02 18:42 ~ 19:43（台灣時間）
> 上一棒：v167（Mac終端機，教練待辦提醒系統正式部署上線）
> 本棒主軸：**確認ai-talk 9/22台南場確實已上線（先前v165誤判commit遺失，實為本機clone沒fetch）；記錄新RustDesk密碼；回答FB社團發文能力問題；9/5+9/16兩場活動文案+9/16連結更新；首次用Graph API真實發布圖片貼文，5個粉專全數上線並用permalink_url驗證。**

## 🎯 本場戰果

### 1. 澄清v165對ai-talk的誤判：本機clone沒fetch，不是commit遺失
上一棒(v165)發信給Hermes交辦"ai-talk 9/22台南場改版"時，本機`git log`看不到v153記錄的`6dc29dc`等commit，一度懷疑接力棒記錄不實。Mac軍師來信說明：GitHub遠端commit歷史完整，只是聯想這台機器的本機clone沒`git fetch`到最新，不是雲端記錄消失。已`git fetch`+`git pull --ff-only`確認`ai-talk`repo確實已是9/22台南場內容(commit`94ebb66`)，雙方inbox信件歸檔`outbox/2026-09/`。**教訓**：比對`git log`跟`git log origin/main`前一定要先`fetch`，否則本機clone落後也會被誤判成「遠端記錄不存在」。

### 2. 記錄RustDesk連佩佩老師電腦的新密碼
教練交付：RustDesk連佩佩老師電腦密碼`Bymyway7`，跟既有連Mac mini的密碼`Sea123457`分開記錄，寫入`路徑大全_憑證層.md`，commit`59eeb616`。同場也順手查證回答教練「RustDesk固定密碼」查詢(既有`Sea123457`)。

### 3. 回答FB社團(Groups)發文能力問題
教練問粉專發文能力可否延伸到他加入的FB社團。查證回覆：Meta自2018年劍橋分析事件後大幅收緊社團發文API權限(`publish_to_groups`)，一般App幾乎申請不到，這是Meta政策限制非本系統缺陷；唯一可行路徑是比照先前手動貼5個粉專的瀏覽器模擬點擊方式，但教練個人帳號在社團裡跑自動化行為被FB判定機器人的風險比粉專官方API高，已如實告知風險，教練尚未決定要不要嘗試。

### 4. 9/5+9/16兩場活動文案定稿+9/16連結更新+coach888同步
查證兩場活動最新正式資料(非舊草稿)：9/5「零基礎學AI，起步比較快」(KR養生廚房，免費，14:00-16:30)、9/16「當古典音樂遇到AI科技」(高雄郭音樂廳，一日通票600元含午餐下午茶，10:00-17:00，8位老師陣容)。**查`bigtree/archive/大樹小講_歷史講座紀錄.html`確認9/5這場KR養生廚房7/4已經辦過一次同主題同場地**，因此教練指定的「返場款」文案角度屬實非杜撰。9/16教練指定「降門檻款」，主打流水席隨到隨坐降低參與門檻焦慮。教練後續要求9/16連結改用`event.bymyway.com/ai-art/`(比GitHub Pages版更新)，同步更新coach888作品總覽該項目連結，commit`14e4036`(過程與Mac`99dcff3`批量搬移功能merge，div開合317/317驗證平衡無誤)。

### 5. 首次用Graph API真實發布「圖片+文案」貼文，9/5活動上線5個粉專
教練用9/5文案自製活動海報(`D:\Users\Downloads\export (13).jpg`，AI生成插畫+資訊卡設計，內容跟已核准文案逐字對應)，軍師自行到D槽下載資料夾取圖(未叫教練搬運)。技術做法：`POST /{page-id}/photos`帶`source`(multipart檔案)+`caption`(文案全文)+`access_token`，用既有`fb_automation/page_tokens_2026-09-01.json`裡的粉專權杖，沒有requests套件改用curl `-F`處理multipart上傳。**先發K R養生廚房單一粉專**讓教練驗收效果(教練回饋「效果不錯」)，再追加海餅乾俱樂部/大樹教練/跨界美.術.管/大台南策展中心四個。教練口語報出的「美術館」「大台南會展中心」跟粉專清單正式名稱有落差，軍師對應到清單裡最接近的「跨界美.術.管」「大台南策展中心」後先執行、同時列出對應請教練覆核，教練回「對的」確認無誤。**5則貼文皆用Graph API的`permalink_url`欄位真實查證上線**，不是只看POST回傳的`post_id`就假設成功。

## ⚠️ 下一場開工先做
1. **等教練提供9/16活動圖片**，圖片到位後問清楚要發哪幾個粉專，套用v168同一套流程(curl multipart上傳)即可，不用重新摸索。
2. FB社團發文教練尚未決定要不要用瀏覽器模擬方式嘗試，若教練後續提起，直接引用本棒查證的風險說明，不用重新查證Meta政策。
3. **跨機信箱有2封未讀**：`20260902-1725_mac-to-lenovo_todo-system-deployed-successfully.md`(已在本棒對話中透過CLAUDE.md鏡像讀到內容，todo系統確認部署成功，可歸檔)+`20260831-1858_acer-to-mac-lenovo_status-report-and-workspace-clone-bug.md`(教練未指示處理，繼續掛著)。
4. v161之前已知舊待辦（FB粉專商家驗證後續、`/bni-credit`補公司欄位、12月主題培訓內容等）本場未觸及。

## 🔑 本場commit
`workspace`：`59eeb616`（RustDesk密碼記錄）+跨機信箱歸檔commit。`coach888`：`14e4036`（ai-art連結改bymyway版，含merge）。`fb_automation`：本場僅本機臨時檔案操作(用完即刪)，無新commit(page_tokens沿用既有9/1版本)。

---

# 軍師接力棒 · 2026-09-02 v169（Mac終端機 Sonnet 5，「全部釋放」指令上線+/bni-credit補公司欄位120筆完成+coach888最近刪除功能+BNI信用証查詢）

> 建立時間：2026-09-02 18:52 ~ 20:56（台灣時間）
> 上一棒：v168（聯想Windows，FB行銷文案+9/5貼文首發5粉專）
> 本棒主軸：**教練三個決策一次執行完（GPT/MiniMax路由放棄／「全部釋放」指令範圍定案並上線／9/16部署維持原排程）；`/bni-credit`補公司欄位312筆全數完成(委派3背景Agent平行處理，途中發現並修復多Agent共用瀏覽器分頁的資料污染風險)；coach888新增「最近刪除」回收桶+處理教練本機file://編輯遺失問題(改口述指令直接修正)；BNI Connect單筆信用証到期查詢。**

## 🎯 本場戰果

### 1. 三個教練決策執行：GPT/MiniMax路由放棄／「全部釋放」上線／9/16部署維持排程
教練裁示GPT/MiniMax混合模型路由「不做了」，待辦表結案。**「全部釋放」指令**教練親口定義範圍：「關掉瀏覽器、關掉赫米斯、關掉LINE、關掉語音輸入法(Typeless)、同時重啟連線軟體」。新增`scripts/release_all_memory.sh`：Chrome/LINE/Typeless用osascript偵測是否在跑才關(避免誤開)，赫米斯用`launchctl bootout`四個launchd服務(KeepAlive會自動重啟需bootout才真正停止)，RustDesk沿用既有邏輯重啟。`hooks/rustdesk-free-memory-trigger/handler.js`改兩層觸發(先判「全部釋放」類詞組跑新腳本，否則才判單純「釋放」跑舊腳本，避免文字重疊雙觸發)。**已用真實指令執行驗證**（非模擬）：Chrome/赫米斯/Typeless確實被關閉，RustDesk重啟成功(495M→29M)。commit`d959b039`(hook,外層repo)+`b8e40c824`(腳本,workspace)。9/16高雄場後大樹小講自動部署維持原排程不動。

### 2. `/bni-credit`補公司欄位：委派3背景Agent，途中發現並修復多Agent共用瀏覽器分頁污染
教練問清楚token消耗後同意先跑10筆校準樣本（9/10成功，1筆確認官方本身空白），過程中意外把Chrome關掉（自己測全部釋放腳本造成），也連帶讓BNI Connect登入態失效，教練親自重新登入後恢復。校準後推算110筆剩餘任務約70~95萬token，教練同意分3批(37/37/36)各自開獨立背景Agent平行處理，**過程中第1批Agent回報讀到「別人的證書」中途停手**——查明3個Agent平行操作時共用了系統預設回傳的同一個瀏覽器分頁，navigate結果互相覆蓋。指示補開專屬分頁(`tabs_create_mcp`)後繼續，全數完成。**最終結果：312筆(active/transferred/redeemed)全部處理完，110筆補上真實公司名稱，2筆(張仕賢/林薔薇)確認官方頁面本身空白**，全程唯讀操作(navigate+讀頁面+寫DB)，未點擊任何BNI Connect按鈕。記憶`reference_parallel_background_agents_shared_browser_contamination_2026-09-02`。

### 3. coach888：「最近刪除」回收桶上線+處理教練file://本機編輯遺失
教練提出「刪除只是為了整理方便，怕手滑刪錯忘記刪了什麼」的痛點，新增「最近刪除」暫存區(仿資源回收桶)：單一項目/整個分類刪除都先移入該區而非直接消失，用既有批量搬移機制勾選送回任何分類，確定不要才按「永久清空」。已用本機瀏覽器JS互動測試「刪除→進最近刪除→勾選搬回原分類」全程正確，commit`817691f`。**教練接著回報之前在`file:///Users/bymyway/github_repos/coach888/index.html`本機編輯的內容沒同步到聯想電腦**——查明是開了本機檔案而非正式GitHub Pages網址，編輯只存在瀏覽器localStorage，不影響檔案本身。嘗試直接讀Chrome LevelDB底層儲存檔案救回內容(UTF-16BE解碼+varint長度解析)，格式解析到JSON中途卡住(疑似LevelDB WAL跨block片段化)未能可靠還原，教練同意截圖查看後也因CSS `column-count`多欄排版誤判內容歸屬(截圖左右對齊看起來像項目被搬動，實為多欄自動平衡排版的視覺巧合)。**教練最終直接口述**：「把1移到5那邊，下面的都沒動」——即「一、BNI最近常用」11項全部併入「五、BNI專用」，其餘7分類不動，直接改正式檔案完成，commit`731ffad`，用Chrome開給教練確認。往後coach888編輯一律提供`https://coach1973.github.io/coach888/`正式網址，不再開本機檔案。記憶`feedback_column_layout_screenshot_misread_2026-09-02`。

### 4. BNI Connect單筆信用証查詢
教練貼memberId 2547603查詢是否過期，查頁面「信用證」連結(href=#)比對資料庫既有記錄(2026-08-27已查證同款「Please contact support」過期訊號)，確認陳宏恩(真誠分會)信用証已過期，未重複點擊測試。

## ⚠️ 下一場開工先做
1. FB粉專商家驗證後續、12月主題培訓內容等舊待辦本場未觸及，繼續掛著。
2. 教練若反映`/bni-credit`頁面顯示效果或其他分會問題，優先處理。
3. `/bni-credit`120筆補公司欄位的commit待查——資料庫是SQLite直改，非git追蹤範圍，若需要留存快照可考慮備份`namecards.db`。

## 🔑 本場commit
外層repo：`d959b039`（全部釋放hook）。`workspace`：`b8e40c824`（全部釋放腳本+接力棒更新）。`coach888`：`817691f`（最近刪除功能）+`731ffad`（BNI最近常用併入BNI專用）。記憶：`reference_parallel_background_agents_shared_browser_contamination_2026-09-02`+`feedback_column_layout_screenshot_misread_2026-09-02`。

---

# 軍師接力棒 · 2026-09-02 v170（聯想Windows Sonnet 5，9/16活動FB貼文發滿5個粉專，9/5+9/16行銷任務全數結案）

> 建立時間：2026-09-02 22:14 ~ 23:41（台灣時間）
> 上一棒：v169（Mac終端機，全部釋放上線+/bni-credit補公司欄位312筆完成+coach888最近刪除功能）
> 本棒主軸：**教練9/16活動圖片做好，延續v168同一套curl multipart流程發到5個粉專，教練確認KR養生廚房要不要一起發後回覆「都發」，兩場活動行銷任務至此全數結案；教練順口問發文token消耗，已說明清楚。**

## 🎯 本場戰果

### 1. 9/16活動圖片確認+發文範圍二次確認
教練回報9/16圖片(`export (14).jpg`)也在下載資料夾，軍師自行到D槽抓取讀取確認：內容跟核准文案逐字對應(降門檻款/流水席/日期時間地點/票價/CTA連結皆為`event.bymyway.com/ai-art/`最新版)。發文前主動提出一個確認點：KR養生廚房是9/5台南場地的專屬粉專，跟9/16高雄場沒有直接地緣關係，先問教練是否要排除，教練回覆「都發」——即5個粉專(含KR養生廚房)全數發布，不因活動地點跟粉專屬性不完全對應而自行排除。

### 2. 9/16貼文發滿5個粉專，全數permalink_url驗證上線
沿用v168同一套技術流程(`POST /{page-id}/photos`帶`source`+`caption`+`access_token`)，一次性發送大台南策展中心/K R養生廚房/海餅乾俱樂部/跨界美.術.管/大樹教練共5個粉專，逐一用`permalink_url`欄位查證真實上線非僅信任API回傳的`post_id`。**兩場活動(9/5+9/16)合計10則貼文全部驗證成功**，教練待辦表該項目已改標✅結案。

### 3. 回答教練發文token消耗疑問
教練問這樣發文會不會很耗token。已說明：發文動作本身是用curl直接呼叫Facebook Graph API(等同執行一行指令)，不是叫AI模型生成內容，幾乎不耗token；真正耗token的是讀圖確認內容+對話討論文案的過程，跟粉專數量多寡無關——同一張圖不管發5個還是50個粉專，token消耗差異都很小。

## ⚠️ 下一場開工先做
1. **跨機信箱仍有1封未讀**：`20260831-1858_acer-to-mac-lenovo_status-report-and-workspace-clone-bug.md`，教練未指示處理，繼續掛著等教練說「讀信」。
2. 9/5+9/16FB行銷任務已完整結案，教練若後續有其他場次要推廣，直接套用v168/v170建立的流程(自行取圖→確認文案內容對應→問清楚發文範圍有無需要排除的粉專→curl multipart發布→permalink_url逐一驗證)。
3. v161之前已知舊待辦（FB粉專商家驗證後續、`/bni-credit`頁面顯示效果、12月主題培訓內容等）本場未觸及，繼續掛著。
4. **本場無新教訓寫入試金石/memory**——流程順暢複用既有SOP，教練發文範圍的確認屬於當場澄清、非AI犯錯。

## 🔑 本場commit
`workspace`：本場v170接力棒本身。`fb_automation`：本場僅本機臨時檔案操作(用完即刪)，無新commit，沿用既有`page_tokens_2026-09-01.json`。
