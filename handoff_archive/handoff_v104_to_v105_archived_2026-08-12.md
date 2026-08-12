# 軍師接力棒 · 2026-08-10 v105（Mac桌面版 Sonnet 5，event-signup抽獎報到流程重新設計+bymyway.com/coach888多站維護）

> 建立時間：2026-08-09 18:45 ~ 2026-08-10 00:28（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v104（Mac桌面版 Sonnet 5，bni-chapters編輯功能+mentor100頁尾+幕僚長晨報）
> 本棒主軸：**教練密集測試event-signup抽獎報到系統，從「找不到7/29做的QR轉盤頁面」一路挖到重新設計整套現場報到流程。過程中兩次猜錯教練要找的頁面，最後查git log+對話逐字稿才找到真相；教練確認方向後，把簽到+LINE綁定+抽獎登記合併成單一介面。同場也處理了www.bymyway.com首頁活動同步、jiesheng-report數字調整、大樹作品總覽表多次更新、bigtree-tw場次深連結查證。**

## 🎯 本場戰果

### 1. 🎯🎯 event-signup：現場報到+抽獎登記重新設計（本場核心）
教練回報找不到7/29做的「掃QR進轉盤遊戲」頁面。**過程中兩次判斷錯誤**：第一次以為是`/wheel`(需登入，非教練要找的)，第二次補了7/29專屬立牌也不對——最後查`distill/terminal_2026-07-28.md`+`terminal_2026-07-29.md`逐字稿，用教練7/29現場真實提問「請問我的轉盤抽獎的網址是哪個」+「56位加入抽獎但只有16位綁定」當鐵證，確認`/checkin`(掃碼)→`/wheel`(教練操作)本來就是完整正確的一套，沒有遺漏頁面。

教練接著問「綁定是不是一定要加LINE好友」，查`app.py`/`line_webhook`程式碼確認：**綁定條件是「送出訊息」不是「加好友」**(LINE的`follow`事件這支程式完全沒處理，只處理`message`事件)，且比對邏輯是**用姓名比對**、跟手機號碼無關。教練據此提出重新設計：
- 拿掉「簽到成功」中繼畫面，`/checkin`直接以「我要參加抽獎」為主視覺，手機號碼欄位就在同一頁
- 填手機、按送出的同一步，直接轉跳LINE(帶好「我是OOO，剛報名了XXX。我要現場立即參加抽獎（送出才算登記成功）」)，不用再點第二次「加好友」
- 新增可重複使用的通用版「掃碼玩抽獎」QR立牌(`make_qr.py --wheel`)，不押日期，取代單場活動專屬立牌，之後每場都用同一張

全部改動用「插入測試用戶→POST正式站驗證302導向LINE網址→解碼確認文字→清除測試資料」的方式驗證過，非憑程式碼推論；每次改完.html都用`open -a "Google Chrome"`開真實網址給教練看。commit `7227e1812`(核心流程)+`dc90140e3`(新QR立牌)。

### 2. 🎯 event.bymyway.com/admin 場次同步大樹小講
教練要求「後台活動應該跟大樹小講同步」，直接寫入`event.db`補上8/21金門+8/22金門+8/28嘉義三場(8/26已存在)。`routing_mode=auto`本來就會自動抓「日期最近未過期」的場次，已用curl驗證`/checkin`自動切到8/21。資料庫檔案本身`.gitignore`排除，這次沒有commit hash，改動紀錄僅在此接力棒。

### 3. 🎯 www.bymyway.com 首頁「最新消息」同步大樹小講+bigtree-tw查證深連結
教練要求首頁最新消息①取消結繩領導學台中場②拿掉過期活動③跟大樹小講同步。查出`www.bymyway.com`是WordPress iframe嵌`coach1973.github.io/bigtree/speakers-2026/`，直接編輯該頁：移除台中場結繩領導學+7則過期活動，新增8/21~9/23共6場真實現行場次。本機起http.server預覽用`read_page`驗證渲染正確(9場、無殘留)才推送，commit `95273a04b`(bigtree repo)。

另外，教練問「能不能做一個直接跳出8/26報名視窗的連結」，查bigtree-tw原始碼發現**這個功能早就存在**(`?session=YYYY-MM-DD`參數，`openRegisterFromQuery()`)，不用開發，直接用JS實測確認`https://bigtree-tw.netlify.app/?session=2026-08-26`真的會自動彈出預選好場次的報名視窗，交給教練即可用，同時告知教練換日期就能自己生出其他場次的連結。

### 4. 🟢 jiesheng-report：台南場數字調整
教練口頭指示：損益平衡21→13人(commit`03ffbf766`)、目標人數25→20人(commit`6cddd95b4`)。皆重啟服務驗證。

### 5. 🟢 語音糾偏規則泛化+大樹作品總覽表多次維護
- 教練親口把「真愛鋒會=真愛分會」的糾正升級為通用規則「真XX鋒會/峰會一律=真XX分會」，已更新記憶檔`feedback_fenhui_not_fenghui_voice_correction`，commit`a4198b2e8`(claude-brain記憶庫)
- `coach888`作品總覽表本場新增第8/9項(抽獎轉盤系統/QR立牌)後又依教練指示改名+改連結共4次，最終定案：第8項「抽獎轉盤系統」(拿掉日期)、第9項「掃 QR Code 玩抽獎」(連向新版`wheel-print.html`)，commit`ef8e6a6`+`7bc25f5`+`0d80f93`

### 6. 🟢 bigtree-tw：報名視窗補地址+費用資訊(2026-08-10上午追加)
教練指示`?session=`深連結彈出的報名視窗要多顯示①地址②費用備註。新增`findSessionMeta()`依sessionLabel反查`SESSION_DATES`拿venue/address/transport，`showRegisterModal()`動態渲染進`modalSessionMeta`區塊，不用逐場硬編。本機http.server預覽+`javascript_tool`實測驗證渲染正確(含無資料時正確隱藏的邊界情況)才推送，commit`bf0cbd6`。**這是`bigtree-tw`站首次在本場對話中真的部署**(先前查`?session=`功能只是測試既有功能沒有變更，不扣點)——教練事後追問「昨天測試連結有沒有扣點」，藉此機會確認清楚跟教練說明「純瀏覽=不扣點，改內容才要部署=扣點」的界線，教練表示理解。教練說「推」後執行：查site ID(`40e580f0-1def-4777-adb8-587ef023ed36`)→打包index.html+photos-carousel+photos-carousel-0729+archive共75檔案→API部署→輪詢確認`state:ready`→curl驗證圖片Content-Type正常→正式網址javascript_tool二次確認渲染正確→Chrome開給教練看。deploy`6a793dc68c5929aa18bea1c3`，額度46→45，已記錄`state/netlify_deploy_quota.json`，commit`6c483ece9`。

## 📋 下一場直接開工任務
- **event-signup新流程**：8/21金門場是第一次實戰，教練現場測試後若有回饋(例如綁定率有沒有真的提升)，下一場先問結果
- bni-chapters「真誠分會」網頁主架構問題：教練仍未說明具體是什麼，見到教練先問清楚
- 企業健身房、BNI分會網站架構(峰會/分會混淆待確認哪個系統)：皆延續v104未解決，教練尚未回覆
- 三機hook同步：ACER仍待處理

## 🔑 本場關鍵檔案索引
- `event-signup/app.py`：`_lottery_greet_url()`新helper、`checkin_submit()`改直接跳LINE、`slides_landing()`複用helper
- `event-signup/templates/checkin.html`：文案改「我要參加抽獎」
- `event-signup/make_qr.py`：新增`make_wheel()`+`--wheel`參數
- `event-signup/qr/wheel-print.html`+`wheel.png`：新版通用QR立牌
- `event-signup/event.db`：場次表新增8/21+8/22+8/28(不進git)
- `github_repos/bigtree/speakers-2026/index.html`：首頁最新消息同步
- `github_repos/bigtree/index.html`：確認`?session=`深連結功能已存在，未改動
- `github_repos/jiesheng-report/app.py`(rpl-workshop)：損益平衡+目標人數
- `github_repos/coach888/index.html`：作品總覽表4次更新
- commit(workspace)：`7227e1812`+`dc90140e3`+`03ffbf766`+`6cddd95b4`
- commit(bigtree)：`95273a04b`
- commit(coach888)：`ef8e6a6`+`7bc25f5`+`0d80f93`
- commit(claude-brain)：`a4198b2e8`

---

# 軍師接力棒 · 2026-08-09 v104（Mac桌面版 Sonnet 5，bni-chapters編輯功能+mentor100頁尾+幕僚長晨報+bymyway.com架構查證）

> 建立時間：2026-08-09 台灣時間 14:00~18:45
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：聯想 Windows 終端機 Sonnet 5（補齊三機hook同步待辦）
> 本棒主軸：**四條主線。①`bni-chapters`後台社群連結補「編輯」功能，教練回報只有新增刪除很麻煩。②`mentor100`首頁補正式頁尾（版權/訪客計數/官網連結/LINE聯絡）。③教練口頭確認三項舊任務結案（Email自動發送/mentor100申請流程/光線尺對帳），並延伸討論一支影片講的AI使用技巧（自我審查邏輯漏洞、個人使用說明書confirm已有ai-go/coach-persona.md不用重做、影片講的第三~六階段AI實踐程度逐項查證評估），落地建立「☕幕僚長晨報」cron統整bni_tainan+jiaolian_thoughts兩個對外AI員工每日動態。④教練問切換聯想電腦做BNI/mentor100任務會不會有落差，查證確認這兩個網站是Mac本機Flask+Cloudflare Tunnel（非教練原本以為的WordPress），過程中教練親自釐清bymyway.com網域下WordPress(根網域+課程)跟Mac本機網站(子網域群)的分流，順手查證VPS真實規格(3.8GB/100GB/1CPU)驗證教練決定網站維持Mac不搬VPS的判斷正確。**

## 🎯 本場戰果

### 1. 🎯 bni-chapters：後台社群／外部連結新增「編輯」功能
教練回報FB/LINE/聯絡我們只有新增刪除、缺編輯，得先刪再建很麻煩。補`db.update_link()`+`/links/<id>/edit`路由+模板改成可直接編輯label/url，重啟服務+登入實測更新真的存進資料庫（改完再改回原值，沒留測試假資料）。commit `3a5ae8e4`。

### 2. 🎯 mentor100：首頁補正式頁尾
教練要求頁面最下面要有正式頁尾：版權標示+正式計算訪客次數(沿用既有`total_views`)+連結大樹教練官網(bigtree-tw.netlify.app)+LINE官方帳號直接聯絡(沿用bigtree既有`lin.ee/o5pODV8`)。重啟服務+curl正式站驗證通過。commit `63f967a9`。

### 3. 🎯🎯 影片技巧討論+第六階段落地：☕幕僚長晨報cron
教練分享影片兩段指令（①自我審查邏輯漏洞②個人使用說明書），評估後confirm教練現有`coach1973.github.io/ai-go/`的`coach-persona.md`已經是完善的「個人使用說明書」，不用重做（過程中我一度誤判「系統還沒有這個東西」，查證後自行更正，避免重蹈試金石案例55「沒查證就下結論」）。接著逐項查證教練實踐影片講的第三~六階段(高級玩家/數位工頭/數位建構者/終極指揮官)程度，發現對外服務的兩個AI員工(bni_tainan/jiaolian_thoughts)動態教練完全看不到，是第六階段唯一缺口。教練核准後新建cron `b73845c9-f653-4f9a-8869-0e2f2c0bd9b1`，每天07:00讀這兩個agent的每日記憶檔，用「三關」過濾挑出值得教練知道的事，沒事就說沒事不硬編內容。已手動觸發測試：16.4秒完成、真的送達Telegram、正確判斷「今天無notable互動」。

### 4. 🔧🔧 bymyway.com網域架構查證+VPS真實規格
教練誤以為chapters.bymyway.com/mentor100.bymyway.com是WordPress，直接curl驗證wp-json/wp-content特徵，確認實際跑在Mac本機Flask+LaunchAgent+Cloudflare Tunnel（教練稱「傳送門」，帳號最早的tunnel `openclaw-macmini` 2026-03-15建立，吻合教練「當初為了串聯小龍蝦申請」的說法）。同時驗證`www.bymyway.com`根網域+課程頁才是真WordPress。教練決定BNI/mentor100等網站維持Mac架構不搬VPS，理由包括VPS規格偏低——已SSH直接查證VPS真實規格：3.8GB RAM(教練原本印象「4G」正確)、100GB硬碟、僅1顆CPU，驗證教練判斷正確。記憶已寫入`reference_bymyway_domain_architecture`，commit `5af35c96e`（claude-brain記憶庫）。

### 5. 🟢 教練口頭確認三項結案
Email自動發送系統(教練自己執行完成)、mentor100申請流程(已有申請者實測無問題)、光線尺顧問對帳(已解決)——三項寫入接力棒結案，commit `4b055995e`。

## 📋 下一場直接開工任務
- **bni-chapters「真誠分會」網頁主架構問題**：教練仍未說明具體是什麼，見到教練先問清楚
- **企業健身房**：教練表示需要繼續，但尚未給出具體下一步指示，下一場先問清楚要繼續哪個部分（正式建站？4項文案修改？）
- **BNI分會網站架構**：教練表示需要繼續，但用詞疑似「峰會/分會」語音混淆，上一場已提醒待確認是指bni-chapters系統內問題還是真誠/真愛/真AI分會+大台南南區網站草稿，教練尚未回覆，下一場先確認
- **☕幕僚長晨報**：觀察一週，教練回饋內容準不準再決定要不要調整判斷標準
- 三機hook同步：聯想已完成，ACER仍待處理

## 🔑 本場關鍵檔案索引
- `github_repos/bni-chapters/db.py`+`app.py`+`templates/admin_edit.html`：連結編輯功能
- `github_repos/mentor100/templates/index.html`：首頁頁尾
- openclaw cron `b73845c9-f653-4f9a-8869-0e2f2c0bd9b1`：幕僚長晨報
- `~/.claude/projects/-Users-bymyway--openclaw/memory/reference_bymyway_domain_architecture.md`：新建
- commit(bni-chapters獨立repo)：`3a5ae8e4`
- commit(mentor100獨立repo)：`63f967a9`
- commit(workspace)：`4b055995e`（三項結案）→`215b0f623`（幕僚長晨報記錄）
- commit(claude-brain記憶庫)：`5af35c96e`
