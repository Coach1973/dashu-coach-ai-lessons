# 軍師接力棒 · 2026-09-03 v173（Mac終端機 Sonnet 5，ai-art日期修正+四個新活動微站從零建置：leader/1010/DIY/Leadership）

> 建立時間：2026-09-03 12:19 ~ 18:42（台灣時間）
> 上一棒：v172（Mac終端機，發票後台+校友會網站全面完工，coach888誤clear排版搶救成功）
> 本棒主軸：**修正ai-art報名頁截止日錯誤+加即時倒數；接手聯想交接的/leader/報名頁部署；從零建置/1010/（人生四席・一日共鳴）、/DIY/+/Leadership/（結繩工作坊/結繩領導學）三組活動微站，含多輪RWD/文案/講師照片迭代；修好repo-served微站4小時瀏覽器快取誤導教練與自己的坑。**

## 🎯 本場戰果

### 1. ai-art（9/16高雄場）截止日錯誤修正+倒數計時+文案強化
教練回報「報名資訊竟然寫9月13(六)」，查證是8/31新增的「三人同行/裂變行銷」早鳥截止日誤植：9/13實際是星期日不是星期六，正確應為9/12（六），事件本身9/16（三）從未寫錯。已修正日期，並依教練要求加上即時倒數（HH:MM:SS動態時鐘，每秒遞減，截止自動變「⛔已截止」），「立即報名」標題加強為「立即報名 9月16日<br>音樂流水席活動」兩行斷行。commit `186bfcc`+`3a9e134`+`8383d85`+`8582306`+`3828104`（ai-art repo）。

### 2. /leader/ 報名頁部署（接手聯想交接）
聯想在`cross-agent/inbox/mac/`留信，`event-signup`已寫好`/leader/`路由+`/api/leader/join`+`leader_workshop_signups`表但聯想機器沒有Telegram token/launchd服務無法讓正式站生效。Mac這邊`git pull`+重啟`com.coach.event-webapp`，curl驗證200+地址文案「映璇公司一樓會議室」確認已移除，真實表單測試（DB寫入成功+Telegram群組無失敗紀錄）。commit `c02f3efd1`（workspace）。

### 3. /1010/「人生四席・一日共鳴」（淺山綠茶席）從零建置
教練提供design.zip，新建repo`Coach1973/1010`+`event-signup`新增`/1010/`路由+`/api/1010/join`+`event_1010_signups`表，LINE導流佩佩老師官方帳號。教練追問RWD後三項調整：①表頭改`position:fixed`往下滑不跟著捲動②滾動時自動加深底色（`.scrolled`class）③表頭字級調大到32px，桌機/手機/平板寬度皆已測試無跑版。追加匯款資訊（淺山綠植創生活實業社/合作金庫006后里分行/3627-717-007429）。1010 repo commit序列：初版建置→`57be273`（表頭固定+字級）→`c6308cf`（匯款資訊）。

### 4. /DIY/+/Leadership/「結繩工作坊」/「結繩領導學」從零建置，多輪迭代
教練先給DIY.zip，內容重複匯出（index.html與jiesheng-knot-workshop.html實為同一份「結繩工作坊3小時手作體驗」），先照做兩個網址讓教練看效果後才發現重複。教練隨即補給LEADER.zip，才是真正的「結繩領導學兩日實戰工作坊」內容（深藍/橘企業風，講師蔡曜隆）。新建`Coach1973/diy-knot-workshop`+`Coach1973/leadership-knot-workshop`兩個repo，`event-signup`新增`/DIY/`+`/Leadership/`路由（純靜態頁，原稿無表單action不需API）。**多輪迭代**：①Leadership報名連結換PayUNi付款連結（`api.payuni.com.tw/...`），只留台北場，拿掉舊的jiesheng-leadership.netlify.app連結②DIY新增台南10/21+台北10/24雙場次資訊卡+早鳥截止日(開課前1週)、「3人同行」費用卡改為早鳥價NT$600+送限量結繩③Leadership課程價值改16,800元+刪「教材與材料」項+CTA拿掉「刷卡」二字④DIY補「關於老師」講師簡介區塊（移植自Leadership版蔡曜隆老師介紹，教練指出「不能一堂課沒有老師的簡介」）⑤兩頁講師照片換成教練提供的真人照（蔡曜隆帶學員做傘繩手環）⑥**手機版Hero照片顯示問題兩輪修正**：教練回報手機版照片消失/變淡背景，第一輪誤判為bug改成「照片獨立卡片顯示在文字下方」；教練糾正「我其實很喜歡圖片當背景的感覺」，第二輪改回「照片鋪滿整個Hero區當背景」但把原本幾乎看不見的12%透明度提高到合理可見程度（Leadership: opacity 0.4+深色遮罩；DIY: opacity 1.0+米白遮罩），兩頁桌機版全程未受影響。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **repo-served微站（`_serve_repo_file`服務的所有`/ai-art/`、`/1010/`、`/DIY/`、`/Leadership/`等）CSS/JS/HTML都有4小時瀏覽器快取**，同一天AI自己的測試工具跟教練的真實Chrome都各踩坑一次，改完後必須主動提醒教練重新整理（或用`fetch(url,{cache:'no-store'})`/`?_cb=時間戳`繞過驗證）。記憶`reference_repo_served_static_assets_4hr_cache_2026-09-03`。
2. **教練手機版偏好「照片當全版背景」的沉浸式質感，不是「照片獨立卡片」**——回報「照片變成背景/消失」不代表要改成常規排版，先確認他喜不喜歡背景效果本身，重點應放在能見度/遮罩深淺夠不夠。記憶`feedback_coach_likes_mobile_hero_photo_as_background_2026-09-03`。
3. 教練直接在對話中貼圖時，圖片會落地到`~/Downloads/export (N).jpg`（依貼上順序遞增編號），可用`find ~/Downloads -mmin -N`配合時間戳確認是哪一張，不用靠教練另外講檔名。

## 📋 下一場開工先做
1. 四個新微站（leader/1010/DIY/Leadership）目前功能全通，教練若有後續文案/版面調整直接交辦即可。
2. MEMORY.md索引本場已從161行壓縮到140行（移除7條低價值/過時/被新規則取代的舊條目，合併3組主題相近的短條目），詳細內容仍保留在各自檔案未刪除。

## 🔑 本場commit
`ai-art`：`186bfcc`+`3a9e134`+`8383d85`+`8582306`+`3828104`（日期修正+倒數+文案）。`workspace`：`c02f3efd1`（/leader部署）、`6e8d0239b`（/1010+/DIY+/Leadership路由新增）。`1010`：初版+`57be273`+`c6308cf`。`diy-knot-workshop`：初版+`32a0249`+`19abe8e`+`06b9001`+`ee79583`+`1bb9394`。`leadership-knot-workshop`：初版+`855260b`+`ba38d98`+`343d233`+`bef235d`。記憶：`reference_repo_served_static_assets_4hr_cache_2026-09-03`+`feedback_coach_likes_mobile_hero_photo_as_background_2026-09-03`。

---

# 軍師接力棒 · 2026-09-04 v174（Mac終端機 Sonnet 5，DIY3新版落地頁+教練課程教材線上觀看系統從零建置到後台前台分離）

> 建立時間：2026-09-03 19:19 ~ 2026-09-04 05:36（台灣時間）
> 上一棒：v173（Mac終端機，ai-art修正+四個新活動微站leader/1010/DIY/Leadership）
> 本棒主軸：**DIY3「傘繩DIY-3專業研習教室」上線(室內教室+商務人士定位，沿用DIY-2視覺)；教練提出「PPT/PDF雲端線上觀看」構想，從零建置`/materials/`系統(Google Drive embed+OAuth整合+資料夾自動展開+公開/隱藏勾選機制+後台前台分離)，過程含Google Cloud Console手把手設定教學+claude-in-chrome自主排除故障+11份簡報封面圖親眼讀取中文標題。**

## 🎯 本場戰果

### 1. DIY3「傘繩DIY-3專業研習教室」上線
教練要求DIY2(戶外求生風)保留，另做DIY3：場景改室內冷氣專業教室(拿掉戶外/野外強調)、對象改商務人士/自由工作者(休閒商務裝/西裝領帶)，照片沿用DIY2素材。新建repo`Coach1973/diy-studio-workshop`+`event-signup`新增`/DIY3/`路由，報名/日期/費用/講師資訊比照第一版，新增報名區塊LINE官方帳號提醒(教練待補實際連結，先用純文字呈現)。commit`db83c2c`(repo)+`c81e8356a`(路由)。

### 2. 教練課程教材線上觀看系統(`/materials/`)從零建置
教練提出構想：PPT/PDF上傳雲端讓學員線上看不用下載。給出兩方案(Google Drive分享 vs 自建觀看頁)建議後，教練選擇「馬上動作」，建成結合版：檔案留Google Drive、`materials`表存ID、頁面embed Drive自己的viewer(單檔`/preview`+資料夾`embeddedfolderview`)。教練隨即要求新增圖片類型+「貼資料夾不用一個個貼檔名」，先用embeddedfolderview零設定達成；教練接著主動提出「我現在就能登入，你自己去抓API」，一步步帶教練完成Google Cloud Console的OAuth設定(建專案/啟用Drive API/OAuth同意畫面/測試使用者/用戶端ID)，教練中途卡在access_denied(測試使用者清單實際是空的)+JavaScript載入失敗(Cloud Console疑似觸發自動化速率限制)，教練情緒明顯升溫："我不想當搬運工"、"浪費我多少時間"——**最終教練自己完成了最後的Google帳號選擇+允許授權點擊**，refresh_token拿到手，串接成功。

### 3. 資料夾展開+42份檔案盤點+11份英文檔名改中文
授權完成後展開教練上傳的「大樹教練精選資料庫」資料夾，實際有42個檔案(教練原以為只有1個，Drive頁面沒載完整我漏看)。教練要求新增「勾選公開」機制(檔案沒篩選過)，加`visible`欄位+管理清單勾選表單，資料夾匯入預設不公開。教練接著交辦「全英文檔名改中文，用簡報首頁怎麼寫當中文檔名」——11份pptx首頁是整張AI生成封面圖(標題畫在圖裡非文字)，抓出`ppt/slides/_rels/slide1.xml.rels`關聯圖片，逐張親眼讀取標題文字(非OCR)後更新DB，11份全數改名成功。

### 4. 後台/前台分離（教練發現漏洞後修復）
教練問「我沒看到我的後台，是哪一個？」才發現`/materials/`把新增表單+勾選清單+刪除按鈕全部跟公開內容混在同一網址——如果照計畫把這個網址給學員，學員會看到管理介面跟未公開檔案清單。已拆分：`/materials/admin`(教練後台，全部管理功能)+`/materials/`(學員乾淨頁，僅visible=1)，用`is_admin` flag控制模板渲染，已用真實請求驗證公開頁面完全無del-form表單元素。commit`5b4126ea2`。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **給外部人看的網頁，管理控制項絕對不能跟公開內容共用同一網址**——一開始設計就要內建這個假設，不要等教練發現才拆分。記憶`feedback_public_admin_separation_default_2026-09-04`。
2. **Google Cloud Console(Google Auth Platform)完整設定步驟+踩坑**：測試使用者要在`/auth/audience`頁單獨加(跟品牌頁是兩回事)；重新導向URI只能填在對應欄位不能填JavaScript來源欄；帳號多重登入要帶`&authuser=N`；頁面卡在「無法載入JS」可能是自動化請求觸發暫時限制，先暫停等待不要狂點重試。記憶`reference_google_drive_oauth_setup_2026-09-04`。
3. **教練情緒升溫時，先解決問題別多解釋，且事後要誠實承認是自己技術判斷卡住不是教練該做的事**——本場教練連續表達不耐煩+熬夜疲憊，優先度是趕快用claude-in-chrome自己排除故障，卡住時老實說「我在嘗試繞過技術限制沒抓對節奏」而非把責任推給流程本身。
4. **pptx投影片標題可能是圖片而非文字**(AI生成封面常見)，XML解析抓不到文字時，改抓slide關聯圖片直接用有圖片能力的工具讀取，比硬上OCR準確(尤其藝術字體)。記憶`reference_google_drive_oauth_setup_2026-09-04`附帶技巧。

## 📋 下一場開工先做
1. **下一場開工先確認**：教練說要把「大品一覽」的後台系統集中帳密——極可能語音誤植「作品一覽」(coach888)，先問清楚再動手，且帳密存放位置(coach888是否公開repo)要先確認再決定放哪裡。記憶`project_backend_credentials_consolidation_pending_2026-09-04`。
2. `/materials/admin`教練待自己勾選要公開哪幾份，目前42份全數未公開。
3. DIY3的「結繩領導學」官方LINE連結教練尚未提供，目前是純文字提醒未做成按鈕，教練給連結後補上。
4. `/materials/admin`是否要加登入保護，教練說先擱著，之後有需要再問。

## 🔑 本場commit
`diy-studio-workshop`：初版`db83c2c`。`workspace`(event-signup)：`c81e8356a`(/DIY3路由)、`2dcd1a9f1`(materials系統+資料夾/圖片支援)、`18529b66a`(圖片類型+資料夾展開)、`a4d967f06`(Drive OAuth整合)、`4a1fd8aa7`(公開/隱藏勾選機制)、`5b4126ea2`(後台前台分離)。記憶：`project_materials_viewer_system_2026-09-04`+`feedback_public_admin_separation_default_2026-09-04`+`reference_google_drive_oauth_setup_2026-09-04`+`project_backend_credentials_consolidation_pending_2026-09-04`。

---

# 軍師接力棒 · 2026-09-03 v175（聯想Windows Sonnet 5，/leader報名頁建置+機器記憶體釋放+能力確認問答，與Mac v173平行作業）

> 建立時間：2026-09-03 13:02 ~ 2026-09-04 06:56（台灣時間）
> 上一棒：v174（Mac終端機，DIY3+教練課程教材線上觀看系統從零建置）
> 本棒主軸：**教練提供design(4).html邀請函稿，聯想完成event.bymyway.com/leader報名頁全套(前端+後端+Telegram/LINE通知)並本機驗證，交接Mac部署——Mac已在v173同日完成部署上線，此項已結案；教練要求「釋放記憶體」，查證聯想這台RustDesk無自動重啟機制後改採保守範圍只關LINE+Typeless；教練確認「做網頁掛GitHub」完全在能力範圍內。本棒與Mac的v173/v174為同時段平行作業，兩邊各自處理不同任務，僅/leader一項有交集（已在Mac v173完整記錄部署細節，此處不重複）。**

## 🎯 本場戰果

### 1. event.bymyway.com/leader「領導人溝通的藝術」9/10報名頁（已由Mac v173完成部署，此項結案）
教練貼`design (4).html`邀請函稿，要求：①移除「（映璇公司一樓會議室）」文案 ②報名成功同時推送Telegram通知+導流佩佩老師LINE官方帳號。比照`/tut`既有模式，新增`templates/leader.html`(邀請函+報名表單)+`/leader/`路由+`/api/leader/join`端點(CORS，寫入新表`leader_workshop_signups`，通知`TELEGRAM_REGISTRATION_GROUP_CHAT_ID`同時導流`PEIPEI_LINE_OA_ID`)。**已在聯想本機8899埠+獨立測試DB完整驗證**：地址文案確認已移除、控制台零錯誤、表單送出200、DB正確寫入一筆、Telegram通知因本機缺`openclaw.json`安全降級(寫入`notify_failures.log`不誤發真訊息)，測試產物已清除。commit`9dc78d09`。**聯想這台沒有`com.coach.event-webapp`服務也無法遠端重啟**，寫信交接`cross-agent/inbox/mac/`(commit`685798e7`)，**Mac已在同日讀信處理，git pull+重啟+curl驗證+真實表單測試全數通過，見接力棒v173第2節**，此項完全結案。已寫入記憶`reference_event_signup_deploy_only_on_mac_2026-09-03`，說明非Mac機器碰這套系統的架構限制，往後可直接查不用重新踩坑。

### 2. 教練要求「釋放記憶體」，查明聯想RustDesk無自動重啟機制
比照Mac既有「釋放記憶體」口令(重啟RustDesk)，查證聯想這台RustDesk沒有Windows Service/排程/Startup自動重啟機制——若直接砍掉會斷線且不會自動恢復，跟Mac靠launchd KeepAlive自動復活完全不同。已問教練要釋放範圍，教練選「無偏好」交由AI判斷，最終**只關閉LINE(~135MB)+Typeless語音輸入(8個process共~633MB)，RustDesk(232MB，數值正常)不動**，釋放約760MB。已寫入記憶`reference_lenovo_rustdesk_no_autostart_2026-09-03`。

### 3. 教練確認「做網頁+掛GitHub」完全在AI能力範圍內
教練直接提問確認，已用本場`/leader`頁+近期`tut-alumni`等實例佐證，答覆為肯定，涵蓋純靜態GitHub Pages站+需要後端/資料庫的動態頁面兩種情境。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **非Mac機器改`event-signup`程式碼，推上GitHub不等於上線生效**——這套系統只有Mac在跑活的process，任何機器要加新路由都要記得多一步「交接Mac部署」，不能自己宣稱已上線。
2. **聯想這台的RustDesk跟Mac版「釋放記憶體」不能一視同仁**——沒有自動重啟保護網，動手前務必先查證有沒有等效機制，沒有就先問教練或縮小範圍。
3. **本場親身經歷跟Mac同時段平行工作的接力棒版本號碰撞**（雙方都接在v172後面各自編了一次v173）——這次影響輕微(內容不衝突，只是編號重複)，但再次印證[[project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26]]類似教訓：多機同時活躍時，交接文件的版本號/待辦表狀態都可能在自己還沒收工前就被對方變動，收工時務必重新讀一次最新檔案內容再動筆，不能只憑自己記憶中的版本號往後接。

## 📋 下一場開工先做
1. `/leader`已全通，教練若有後續文案/版面調整直接交辦即可，不用重新查證部署狀態。
2. 沿用v174下一棒待辦：`/materials/admin`教練待自己勾選公開項目、DIY3的LINE連結待補、「大品一覽」語音誤植待確認。
3. FB粉專商家驗證後續、`/bni-credit`頁面顯示效果等舊待辦本場未觸及，繼續掛著。

## 🔑 本場commit
`workspace`：`9dc78d09`(`/leader`報名頁全套：app.py路由+schema.sql新表+templates/leader.html)、`685798e7`(交接信給Mac)。記憶：`reference_event_signup_deploy_only_on_mac_2026-09-03`+`reference_lenovo_rustdesk_no_autostart_2026-09-03`。


---

# 軍師接力棒 · 2026-09-04 v176（聯想Windows Sonnet 5，海餅乾俱樂部20週年官網從零建置到多輪教練親自校對）

> 建立時間：2026-09-04 06:56 ~ 13:44（台灣時間）
> 上一棒：v175（聯想Windows，/leader報名頁建置+機器記憶體釋放+能力確認問答）
> 本棒主軸：**開工第一件事修復卡了兩天的git rebase衝突狀態；教練帶Lovart AI產出的design.html，從零建置`海餅乾俱樂部20週年`官網(Coach1973/seabiscuit20)，logo三輪迭代找到正確去背版、紀念冊從佔位圖全面換成教練提供的38張真實邀請卡照片(過程修好lazy-load卡死+object-fit裁切兩個真bug)、首頁數據列一度誤解教練指令(誤增第5欄，教練糾正後改回直接替換既有格子內容)。**

## 🎯 本場戰果

### 1. 開工修復卡住兩天的git rebase衝突
上一棒(v175)收工時`pull --rebase`失敗留下未完成的rebase狀態，`HEARTBEAT.md`裡殘留兩輪未解的`<<<<<<< HEAD`衝突標記。本場開工第一件事：正確解開衝突(兩輪都是純日誌內容重疊，逐條合併保留無遺漏，不採用`rebase --abort`避免清空已完成工作)，補commit兩則v175遺漏未落地的記憶檔(`reference_event_signup_deploy_only_on_mac_2026-09-03`+`reference_lenovo_rustdesk_no_autostart_2026-09-03`實體檔案)+一則待辦表新增項，完成rebase並push，雲端同步恢復正常。

### 2. 海餅乾俱樂部20週年官網從零建置(Coach1973/seabiscuit20)
教練提供`design.html`(Lovart AI產出，多處使用外部佔位圖URL)，新建repo並推GitHub Pages上線`https://coach1973.github.io/seabiscuit20/`。**Logo三輪迭代**：①教練第一次要求「換成無外框圓形去背版」，AI用背景移除工具處理教練上傳的一張圖，結果那張其實是checkerboard棋盤格假透明截圖(JPG格式本身不可能有alpha)，誤把棋盤格當成透明處理②教練澄清後找到真正正確的、教練自己已裁切好的透明PNG直接套用成功③頁尾logo再要求放大到「跟培育人才那行字一樣寬」，用JS量出該行文字實際渲染寬度(418px)精確設定logo寬度並置中對齊，程式驗證像素誤差0px。**紀念冊(歷年紀念冊)重建**：原本是佔位圖，教練提供`20週年`資料夾內38張真實邀請卡+花絮照片(分兩批提供，第二批補齊1-3週年+4/5/6/16/19週年主卡+16.5/17.5花絮)，逐一核對年份日期(均符合2007創立+N年公式，如7週年=2014/5/14)後建表插入，過程修好兩個真bug：①`loading="lazy"`+flex置中+無固定尺寸img標籤會讓瀏覽器判定初始版面框0×0、IntersectionObserver永不觸發，圖片卡死不載入，已移除該屬性②原設計`object-fit:cover`裁切非標準比例照片(教練照片寬高比0.56~2.83都有)，改`object-fit:contain`符合教練「絕對不要裁切到」要求。**1940歷史照片+17週年照片**依教練指示更新兩次。**首頁數據列一度誤解指令**：教練說「在1938後面接1940，寫累積獎金世界第一」，AI誤判成新增第5欄位(破壞原本4欄有意境排版)，教練糾正「我只是請你把數字改成1940...把89/33這個拿掉」——正解是直接把89/33那格內容換成1940，已改回4欄原版面。教練詢問GitHub能否放影片，已建議改YouTube上傳+embed連結(GitHub不適合存放大型媒體拖慢repo)。

## ⚠️ 本場教訓/發現（待寫入記憶）
1. **教練連續上傳多張圖檔時，先問清楚指的是哪一張，不要憑檔名相似度或上傳順序猜**——logo第一輪誤用了checkerboard假透明截圖，浪費一輪來回。
2. **教練給的「在A後面接B」這類指令有歧義**：可能是「新增一個項目插在A後面」，也可能是「把緊接在A後面的既有項目內容換成B」——本場首頁數據列誤判成前者，教練實際要的是後者，且教練特別強調「原本數字的呈現方式」不能被破壞（4欄有意境版面、不是隨意加減欄位）。日後遇到類似「接在...後面」的修改指令，先反問一句確認插入vs替換，比事後改兩次更省教練時間。
3. **`loading="lazy"`在flex置中容器+無固定width/height的img標籤上會失效**：瀏覽器初始判定該元素版面框是0×0，IntersectionObserver可能永遠不判定它進入可視範圍，圖片卡死不載入且無錯誤訊息，肉眼難以察覺。這類「圖片自然置中、無固定框」的排版設計要移除lazy-load屬性，改用eager載入。
4. **`object-fit:cover`只適合統一比例素材，教練實際提供的照片素材(邀請卡/EDM/截圖)寬高比落差可能很大**——設計稿階段假設的裁切方式在真實素材灌入後常常不成立，改用`object-fit:contain`+動態容器高度較保險，尤其教練明確表達過「不要裁切」的偏好時。

## 📋 下一場開工先做
1. seabiscuit20官網logo/紀念冊/數據列目前教練驗收中，若有後續文案/版面微調直接交辦即可。
2. 沿用v174/v175下一棒待辦：`/materials/admin`教練待自己勾選公開項目、DIY3的LINE連結待補、「大品一覽」語音誤植待確認——本場皆未觸及，繼續掛著。
3. FB粉專商家驗證後續、`/bni-credit`頁面顯示效果等更早期舊待辦本場未觸及。

## 🔑 本場commit
`seabiscuit20`(新repo)：初版建置→多輪logo/紀念冊/1940+17週年照片/數據列迭代，最新`d8fe469`。`workspace`：HEARTBEAT.md衝突解決+補commit v175遺漏記憶檔（git log可查今日聯想commit序列）。

---

# 軍師接力棒 · 2026-09-04 v177（聯想Windows Sonnet 5，記憶體98%洩漏安全排查：確診核心層驅動洩漏非中毒，Nahimic嫌疑+新裝顯示卡驅動後更快復發）

> 建立時間：2026-09-04 10:09 ~ 13:49（台灣時間）
> 上一棒：v176（聯想Windows，海餅乾俱樂部20週年官網從零建置到多輪教練親自校對）
> 本棒主軸：**教練半夜發現這台聯想Windows開機記憶體飆到98%，懷疑中毒要求安全排查+網路流量檢查，甚至準備動用「一鍵還原」重灌。全面排查後排除中毒，確診是核心層Nonpaged Pool驅動洩漏（非病毒），重開機驗證有效但約2小時內更快復發，鎖定Nahimic音效驅動最可疑並教會教練手動移除步驟，過程順手修正教練誤判「Claude開Chrome造成」的錯誤歸因，另回答BIOS更新風險問題。**

## 🎯 本場戰果

### 1. 記憶體98%安全排查：確診非中毒，鎖定Nahimic驅動洩漏
教練回報記憶體飆98%懷疑中毒，用PowerShell全面排查：Defender即時防護開啟/病毒碼最新/零威脅紀錄、前25大耗記憶體程式全是教練平常在用的Comet/LINE/Claude/Typeless/Signal、對外連線埠全是443+高位隨機埠共31個不重複IP(對應教練實際開的App數)、無Temp/Public資料夾藏匿程式，排除中毒可能。真正根因：全部process記憶體加總只有10GB，卻對不上系統回報用掉38GB，用`Get-Counter "\Memory\Pool Nonpaged Bytes"`查到核心層驅動記憶體區（正常僅幾百MB）暴增到**29GB**，落差全在這裡。鎖定嫌疑Nahimic音效驅動（NahimicBTLink.sys+Nahimic_Mirroring.sys，檔案日期2022/8/18已4年沒更新，只存在裝置管理員不在新增/移除程式清單），教會教練手動解除安裝步驟（裝置管理員→3個Nahimic裝置→解除安裝＋勾選刪除驅動程式軟體→重開機）。**重開機驗證**：記憶體從97.76%瞬間降到33.1%，Nonpaged Pool歸零，證實診斷方向正確，非病毒。

### 2. 新裝驅動後2小時內更快復發，澄清教練誤判「Claude開Chrome造成」
教練同時段新裝Intel顯示卡驅動31.0.101.4255/NVIDIA GeForce Experience 3.27.0.114/聯想電競功能修補程式後，Nonpaged Pool約1h56m內又衝到22GB，比第一次21.5小時才洩漏到29GB快了近10倍。教練當下猜測是「Claude Code開Chrome瀏覽器做網頁」造成——查證系統當時**根本沒有chrome.exe在跑**，Comet+Claude合法用量僅約4GB，跟22GB缺口完全對不上，已澄清仍是驅動層洩漏、非瀏覽器/AI工具行為造成。**尚未確認教練是否已執行Nahimic移除步驟**，此為下一場開工首要確認事項——若已移除仍快速復發，嫌疑轉移到新裝的Intel/NVIDIA/聯想電競驅動。

### 3. BIOS更新風險問題（一般性回答，非本機操作）
教練另外問「BIOS Update Utility - 11」更新風險，已說明官方聯想工具風險相對低但仍需注意（全程接電源+不可中斷+更新後部分設定會重置），此為一般性建議未實際操作。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **PowerShell核心層Nonpaged Pool診斷法可複用**：正常應僅幾百MB，超過1-2GB即視為異常驅動洩漏，比逐一排查process更快定位「記憶體帳目對不上」的元凶。記憶`project_lenovo_nonpaged_pool_leak_2026-09-04`。
2. **這台機器用Bash工具(Git Bash)呼叫PowerShell時，`-Command`參數若用雙引號包裹，Bash會把PowerShell的`$_`管線變數當自己的參數展開吃掉**，導致語法錯誤、看起來像PowerShell壞掉其實是shell引號層級問題——本場前3次查詢指令因此全部失敗，改用單引號包外層才修復。記憶`reference_gitbash_powershell_dollar_underscore_quoting_2026-09-04`。

## 📋 下一場開工先做
1. **優先確認**：教練是否已執行Nahimic驅動移除步驟？若已移除但記憶體仍快速復發，改排查新裝的Intel顯示卡/NVIDIA/聯想電競驅動，可建議逐一解除安裝排除測試。
2. 沿用v174/v175/v176下一棒待辦：`/materials/admin`教練待自己勾選公開項目、DIY3的LINE連結待補、「大品一覽」語音誤植待確認、seabiscuit20官網教練驗收中——本場皆未觸及，繼續掛著。
3. FB粉專商家驗證後續、`/bni-credit`頁面顯示效果等更早期舊待辦本場未觸及。

## 🔑 本場commit
`.claude/projects`記憶庫：`project_lenovo_nonpaged_pool_leak_2026-09-04.md`+`reference_gitbash_powershell_dollar_underscore_quoting_2026-09-04.md`（新增）+MEMORY.md索引更新（含瘦身壓縮，回應hook額度提醒）。`workspace`：本篇接力棒v177新增（純診斷/衛教任務，未觸及任何程式碼repo）。

