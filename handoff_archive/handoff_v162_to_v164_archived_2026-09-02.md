# 接力棒封存：v162~v164（2026-09-01）

> 從 JUNSHI_HANDOFF_LATEST.md 封存，原因見主檔「接力棒瘦身鐵律」說明。

# 軍師接力棒 · 2026-09-01 v162（Mac終端機 Sonnet 5，來賓排行榜v1→v3三輪重做+培訓總覽同步加分會篩選+chapters.bymyway.com整合+開工hook誤報修復+真鑽資料備妥發信Hermes）

> 建立時間：2026-09-01 08:14 ~ 10:50（台灣時間，接續v161，教練整夜未睡、本場情緒張力高，連續多次糾正）
> 上一棒：v161（真鑫/真鑽/真貴戰情儀表板從零建置+試金石案例68/69）
> 本棒主軸：**BNI-Training/guests.html來賓排行榜經歷三輪完全重做才做對（警示表→單分會TOP10→PALMS官方資料+全區排名），過程數次被教練point出方向錯誤；chapters.bymyway.com整合培訓/來賓入口一次做錯位置後修正；順手修好開工hook近乎每次誤報的bug；真鑽20週真實資料已備妥發信Hermes。**

## 🎯 本場戰果

### 1. 修復開工hook誤報「git pull失敗」的bug
教練指出通知太頻繁，查`notify_coach.log`證實8/30~9/1至少6次幾乎每場開工都誤報。根因：`git pull --rebase`要求工作區完全乾淨，但這個session自己即時在寫的`terminal-notes/raw_sessions/*.jsonl`等背景檔案幾乎必然造成工作區「髒」，撞到就報失敗。改用`fetch+ff-only merge`優先（不需要乾淨工作區），失敗才退回stash+rebase搶救，且通知前額外比對HEAD跟origin是否一致，只有真正落後才通知。commit`d8b44061c`，已用真實情境（9個髒污檔案同時存在）測試通過。

### 2. BNI-Training/guests.html 三輪重做才做對
- **v1(錯)**：軍師誤解需求，做成「超過門檻未邀約來賓的警示名單」（距今月數排序），教練糾正「邏輯不對，你不知道我要的是排行榜嗎」，連續兩次點名軍師沒有照著`index.html`的實際邏輯走。
- **v2(部分對)**：改用TOP10排行榜邏輯（逐字對照`index.html`的`filterByWindow`+`renderRanking`），但資料源仍是「地區-查看來賓」明細報表，個人數字嚴重偏低（郭政輝106 vs 教練提供官方數字303）。教練提供PALMS摘要報表交叉驗證後，確認明細報表統計口徑跟官方PALMS不同，改用PALMS當唯一資料源。
- **v3(定案)**：`guests_build_data.py`整個重寫，改讀`~/Downloads/__-palms-*.xls`（教練逐一從BNI Connect匯出，讀檔案內容「分會:/從:/至:」參數列自動判斷分會與月數，不用檔名）。三分會（真誠17節點/真鑫6節點/真鑽20節點）月數標籤都以實際成立月封頂（真鑽104→97、真誠85→72、真鑫7→5，教練親口逐一確認成立月份），並用「兩份快照總計相同→證明中間無新資料」的方法交叉驗證，不是單純採信教練口頭數字。教練再指出「跟培訓總覽一樣要有全區總排名，不能只有各分會TOP10」，新增「大台南南區全區」聚合視圖（各分會各自抓「不超過所選月數的最大可用快照」合併）。

已驗證：真鑽104個月TOP2=郭政輝303/康文彬254（逐字對上教練提供的官方數字）；全區近6個月TOP3=陳佩君55(真誠)/林尹渰19(真鑫)/吳志煒15(真鑫)。commit（BNI-Training repo）`be6f272`→`ccd9b09`→`fb4ba5d`→`db17d00`→`dd60308`→`270df6a`。

### 3. index.html（培訓總覽）同步補上分會篩選
教練「同理，培訓也要做各分會的排名」——`region_template.html`新增分會tabs（全區+真誠/真鑫/真鑽），選單一分會時`filterByWindow`額外套用chapter篩選，「分會培訓排名」比較區塊在單一分會模式下自動隱藏（跟自己比較沒意義）。commit`78c9a4d`。

### 4. chapters.bymyway.com整合培訓/來賓入口（第一次做錯位置，已修正）
教練要求`chapters.bymyway.com`新增`/training`+`/guests`兩個路由（直接讀`BNI-Training`repo活檔案即時渲染），並把導覽列「認識分會」改「培訓總覽」、「核心價值」改「來賓總覽」。**第一次做錯**：軍師把按鈕改到個別分會頁面(`/sincere`等)的導覽列，教練當場糾正「你怎麼就做錯了，按鈕要做在首頁（分會一覽表），你做到真誠分會過去，那真誠分會原本那兩個按鈕不就白費了嗎」。已修正：`templates/chapter.html`完整復原（認識分會/核心價值錨點功能沒受影響），改在`templates/index.html`首頁導覽列加上培訓總覽/來賓總覽連結。commit`9b1cdb7`（錯誤版）→`5ca9ada`（修正版）。

### 5. 真鑽（不是籌備會）補上20週真實資料，發信Hermes
教練澄清「真傳」是語音誤植「真鑽」，且「真貴才是籌備會」（跟軍師一開始理解相反）。從教練提供的官方「分會訪問報告」解析出真鑽最近20週（2026-04-14~08-25，實際例會週二，非教練口誤沿用的真鑫04-02週四起算）的WEEKS+GUEST_DATA，完整寫進信裡讓Hermes直接複製貼上（不用他自己重新查資料源），並在信裡指出`zhenzuan-guests/seed.py`既有一個編碼壞掉的姓名（洪嘉妘）需要順手修正，否則seed.py會KeyError跑不完。同時交代真貴（籌備會，資料空）只需完成部署（DNS+Tunnel+launchd，比照真鑫`zhenxin.bymyway.com`模式）。commit（workspace）`8fb8c0989`。

## ⚠️ 下一場開工先做
1. **讀Hermes回信**：真鑽`seed.py`跑完的統計數字、`zhenzuan.bymyway.com`+`zhengui.bymyway.com`兩個新網址是否部署成功。
2. **真誠、真鑫的guests.html/index.html排行榜**：本場只驗證了郭政輝303/康文彬254（真鑽），真誠/真鑫的PALMS資料正確性教練尚未親自逐一核對，若教練後續回報數字對不上，優先查PALMS檔案本身有沒有被正確歸類到對的分會/月數。
3. **v161之前已知舊待辦**（FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容、v160交辦的道德規範中英對照複製到其他8分會）本場均未觸及，繼續掛著。
4. **本場教訓**：教練貼出明確網址/檔案/邏輯要求「照著做」時，第一步永遠是先讀懂對方原始碼/資料，逐字對照後再動手，不能憑印象/命名相似度聯想；涉及UI改動位置要問清楚是哪一頁，不能自己假設。

## 🔑 本場commit
`workspace`：`d8b44061c`（開工hook誤報修復）、`8fb8c0989`（Hermes真鑽資料+真貴部署委派信）+本場v162接力棒本身。`BNI-Training`：`be6f272`（排序tie-break+查詢節點調整）→`ccd9b09`（改TOP10排行榜邏輯）→`fb4ba5d`（改用PALMS官方資料源）→`db17d00`（三分會PALMS資料到齊）→`dd60308`（月數成立日封頂）→`270df6a`（全區排名）→`78c9a4d`（培訓總覽同步分會篩選）。`bni-chapters`：`9b1cdb7`（錯誤版，已修正）→`5ca9ada`（修正版：按鈕移到首頁）。

---

# 軍師接力棒 · 2026-09-01 v163（Mac終端機 Sonnet 5，FB粉專API完全打通14個+team01/真鑽/真貴三網址部署+真鑽資料四輪校正+chapters.bymyway.com戰情儀表板改版+claude-in-chrome裝置確認）

> 建立時間：2026-09-01 16:27 ~ 19:10（台灣時間，接續v162，教練整天未睡到晚上，本場橫跨FB行銷+BNI戰情儀表板兩條主線）
> 上一棒：v162（來賓排行榜三輪重做定案+chapters.bymyway.com整合培訓/來賓入口）
> 本棒主軸：**FB粉專自動發文API從卡住5天到14個粉專全部打通；接手赫米斯Team01骨架完成team01/真鑽/真貴三網址部署，過程中真鑽資料被教練四輪校正（品牌文字殘留/命名錯誤/名單錯誤/週次認知落差）；chapters.bymyway.com首頁改版「戰情儀表板」+培訓來賓總覽互連；真誠/真鑫/真鑽三站視覺同步改版；發現並修復zhenxin-guests從未推上GitHub的真空窗；查出claude-in-chrome誤連聯想電腦Chrome的裝置混淆問題。**

## 🎯 本場戰果

### 1. FB粉專行銷自動化：14個粉專(含大樹教練本人)API完全打通
教練要求發FB貼文，先用瀏覽器手動貼5個粉專（大樹教練/大台南策展中心/K R養生廚房/海餅乾俱樂部/跨界美.術.管）全部成功。教練追問API卡住原因，查出真因不是商家驗證（那個已經過了），是這個Graph API App的使用案例清單從未加過`pages_read_engagement`權限。已在App後台補上權限，教練親自到Graph API Explorer重新勾選6個權限點擊「Generate Access Token」授權，14個粉專（含原卡5天的「大樹教練」+「大樹教練之『BNi』奇妙旅程」）全部驗證可正常GET/POST，權杖`expires_at:0`永不過期，存於`fb_automation/page_tokens_2026-09-01.json`。教練確認往後改粉專名字不用重新授權，只有新建粉專才要重跑`/me/accounts`。

### 2. 接手赫米斯Team01骨架，完成team01/真鑽/真貴三網址部署
赫米斯建好Team01戰情儀表板骨架（`Coach1973/team01-guests`）後寫信交接部署，軍師比照`zhenxin.bymyway.com`模式，一次幫team01+真鑽+真貴三個都建好Cloudflare Tunnel+DNS+launchd（webapp+tunnel各一支plist）。過程中抓到並修好一個真bug：`zhenzuan-guests/app.py`硬編碼port=5092跟真鑫（zhenxin）撞埠，改5093並連鎖調整真貴為5094避免二次撞埠。

### 3. 真鑽資料經教練四輪校正才定案
- **第1輪**：教練發現網址命名錯誤——`zhenzuan.bymyway.com`/`zhengui.bymyway.com`是軍師自己音譯的，跟`chapters.bymyway.com`既有的英文代號（`real-diamonds`/`real-wealth`）不一致。已改DNS+Cloudflare Tunnel為正確網址，舊錯誤網址的DNS紀錄已刪除。
- **第2輪**：教練發現網站內文（h1標題/大事紀/規則說明）殘留「真鑫分會」字樣，只有`<title>`標籤是對的——複製模板只改了title不夠。已全部改正，並補上真鑽/真貴原本缺的`early_bird`欄位。
- **第3輪**：教練指出「洪嘉妘沒有離會，你打錯字了」+「蘇志揚8/31離會，先不列入計算」。查證後確認「洪嘉紜」是「洪嘉妘」的姓名誤植（不是不同的離會會員），已合併其邀約/早鳥紀錄；蘇志揚已從48人在籍名單移除。標籤文字「教練提供」全改「委員會提供」。
- **第4輪（澄清非錯誤）**：教練質疑「我明明給30場會議，你算成27場」——查證後說明：教練貼了30則報告，但04/21・07/14・08/25三個日期各重複貼了2次（同一場例會的補充/修正版），不是3場不同會議，取內容較完整版本後仍是27場真實例會，非漏算。

用Python程式化解析教練提供的27場BNI例會出席報告文字，交叉比對在籍名單過濾離會會員，寫入`GUEST_DATA`/`GUEST_LIST_DATA`。commit（zhenzuan-guests）`de30793`→`a02249f`→`d5585ac`→`ebae7f3`。

### 4. chapters.bymyway.com首頁「分會之光」改「戰情儀表板」+新增/dashboards頁
教練要求分會列表首頁的導覽列項目改名，點進去列出真誠/真鑫/真鑽三個分會的戰情儀表板外部連結（各自獨立子網域）。新增`/dashboards`路由+`dashboards.html`模板，commit（bni-chapters）`3023af3`。同場也修復`chapters.bymyway.com/admin`一個真bug：分會帳號(非super)誤訪問通用`/admin`會被403擋下（教練誤以為「當掉」），查`webapp.error.log`確認process從未crash，真因是`login_required`裝飾器對無`chapter_id`的路由必定abort，已改成導向自己分會編輯頁，commit`40448f4`。

### 5. 培訓總覽⇄來賓總覽互相加上頂部+底部切換按鈕
教練指出來賓總覽底下已有「培訓總覽」+「MSP進階培訓記錄」連結，但培訓總覽底下沒有來賓總覽，兩邊都要能互相跳轉。已在`BNI-Training/index.html`+`guests.html`的header下方跟footer各自加上對方連結，commit`2f22ad2`。

### 6. 真誠/真鑫/真鑽三站視覺同步改版：姓名下方顯示四項指標摘要
教練要求姓名格下方直接顯示「來賓X人・早鳥X次・121X次・咖啡X場」摘要，不用捲到最右邊看總計，並移除「新進會員（待教練指派小組）」文字。先在真誠分會(`sincere.bymyway.com`)做prototype給教練看，教練確認「視覺效果不錯」後追加121/咖啡兩項，並詢問即時更新是否有效——已用真實瀏覽器dispatch change事件實測驗證（填3次121，姓名下方摘要當場從0變3，不用重新整理），測試後還原資料庫。教練確認後套用到真鑫/真鑽。commit（zhencheng-guests）`ec8c780`→`dac7005`；（zhenxin-guests）`d5585ac`→`e6ebae9`；（zhenzuan-guests同批次）`4b5d3a1`→`ebae7f3`。

### 7. 發現並修復zhenxin-guests從未推上GitHub的真空窗
套用視覺改版時push失敗才發現：`zhenxin-guests`這個repo從v161建立以來從未設定git remote，所有先前接力棒記錄的commit（`4be45ad`/`9b36d4a`等）都只存在本機，正式站`zhenxin.bymyway.com`程式碼曾經零雲端備份。已用`gh repo create`補建私有repo `Coach1973/zhenxin-guests`並推送全部歷史commit，跟其他姊妹repo一樣有雲端備份了。

### 8. claude-in-chrome裝置混淆：教練發現連到聯想電腦而非這台Mac
教練點出用瀏覽器驗證時可能連錯裝置。查`list_connected_browsers`確認當下同時有Windows(聯想)+macOS(這台Mac)兩台已連線，系統規定必須讓教練親自選才能繼續，已請教練選定macOS這台後`select_browser`鎖定，重新驗證過`sincere.bymyway.com`畫面無誤。**釐清**：`open -a "Google Chrome"`這個Bash指令一直都是在Mac本機執行沒有問題，會混淆裝置的只有claude-in-chrome瀏覽器擴充功能連線對象。

## ⚠️ 下一場開工先做
1. **真鑽/真貴資料仍待補**：真貴目前完全空骨架，等教練提供會員名單；真鑽的121/咖啡會議兩項尚未有真實資料，早鳥次數教練說「會請人統計後填上」。
2. **真誠/真鑫還沒做的細節**：教練確認真誠視覺改版後套用到真鑫/真鑽已完成，但真誠本身早鳥資料是空的(0)，等教練後續補資料。
3. **v161之前已知舊待辦**（`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容、v160交辦的道德規範中英對照複製到其他8分會）本場均未觸及，繼續掛著。
4. **本場教訓（已寫入試金石/記憶）**：①複製模板建新網站要先查既有命名規則，不能自己音譯②複製模板只查title不夠要grep全檔確認品牌文字沒殘留③新repo建立時要確認git remote有設定，不能假設commit成功=已備份④claude-in-chrome多裝置連線時系統會強制要求詢問教練，不可自己選。

## 🔑 本場commit
`fb_automation`+`路徑大全_憑證層.md`：`0c3bc8cb5`（FB粉專14個打通）。`coach888`：`0a06345`→`b4660c0`（新網址連結更新）。`zhenzuan-guests`：`de30793`→`a02249f`→`4b5d3a1`→`ebae7f3`。`zhengui-guests`：`9639052`。`zhenxin-guests`：`d5585ac`→`e6ebae9`（含補remote推送全部歷史）。`zhencheng-guests`：`ec8c780`→`dac7005`。`bni-chapters`：`40448f4`（403 bug修復）→`3023af3`（戰情儀表板頁）。`BNI-Training`：`2f22ad2`（互連按鈕）。`workspace`：`97b886023`（Hermes部署完成回信）+本場v163接力棒本身。

---

# 軍師接力棒 · 2026-09-01 v164（聯想Windows Sonnet 5，coach888作品總覽表重整：新增BNI最近常用置頂+補漏路由+排版改2欄流式）

> 建立時間：2026-09-01 18:31 ~ 19:16（台灣時間）
> 上一棒：v163（Mac終端機，FB粉專API打通+三個戰情儀表板部署+claude-in-chrome裝置確認）
> 本棒主軸：**教練口述整理coach888作品總覽表分類，把BNI專用裡最常用的9項獨立成置頂新區「BNI最近常用」，其餘三個冷門區塊移到最後；隨後教練發現chapters.bymyway.com/guests沒列進去、且排版壓縮凌亂，一併修復。**

## 🎯 本場戰果

### 1. 「BNI最近常用」置頂新區上線
教練唸序號指定：BNI專用第1項(出席戰情儀表板)+第13~20項(chapters總表/後台/信用証追蹤/真誠/真鑫/真鑽/真貴/team01共8個戰情儀表板)獨立成新區塊放最上面；對外公開/不公開/保留三區移到最後。逐筆核對68項全數保留無漏無重複，commit`c65712d`。

### 2. 教練回報`chapters.bymyway.com/guests`沒列進總覽表+排版壓縮凌亂
查證發現同一批上線的`/training`(培訓總覽)也一併漏掉（v162接力棒早有記載這兩個路由，本場整理時卻沒對照舊接力棒逐一核對，是本場疏漏）。排版問題：原本用手動`.row`+兩個`.col`把8個分區強制兩兩配對成4排，教練覺得「3、5、6放在一起」「5跟6都是壓縮的，7、8也是壓縮的」——診斷後判斷根因是短區塊(如bymyway 5項)跟長區塊(如後臺10項)硬配成一排時視覺不平衡。改用CSS `column-count:2`整頁流式兩欄排版（8個分區當作連續內容依序往下流動，各自`break-inside:avoid`不被欄位截斷），不再手動配對，徹底解決任何項目數變動造成的排版落差問題。

### 3. 過程中一次技術教訓：大幅結構重排優先整檔案重寫，不要用regex片段替換
第一輪用node正則替換`.row`/`.col`標籤改成`.section-block`時，因原始HTML巢狀結構（grid關閉+col關閉+col開啟三行連續）跟正則預期的兩行模式不一致，加上CRLF行尾一開始沒考慮到，導致替換後div開合數量不平衡（299開/298合）。沒有直接肉眼抓不平衡點在哪，改用node計算div opens/closes數量做為快速健檢，確認有問題後放棄regex修補，直接用完整內容重寫整個檔案，重寫後驗證307/307配平+70項逐筆核對正確才commit。

## ⚠️ 下一場開工先做
本任務已完整結案，coach888正式站已curl驗證上線（`column-count:2`+`來賓總覽`+`培訓總覽`皆確認存在）。無延續待辦。承接v163留下的舊待辦：真鑽/真貴資料待教練補、真誠早鳥資料是空的、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容、道德規範中英對照複製到其他8分會。**跨機信箱有1封ACER→Mac/聯想未讀信**（`20260831-1858_acer-to-mac-lenovo_status-report-and-workspace-clone-bug.md`），本場教練沒有要求處理，下一場若教練說「讀信」再處理。

## 🔑 本場commit
`coach888`：`c65712d`（BNI最近常用置頂+分區順序調整）→`a8e93cd`（補guests/training路由+排版改column-count:2）。`workspace`：本場v164接力棒本身。

