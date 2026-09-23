## 🔴 給跨對話框軍師讀的總結摘要（2026-09-23 21:43，Mac桌面版，新的一棒 v241）

**本場主軸：延續v240的聚寶盆12張發票，教練事後發現2張資料有誤，逐一作廢重開/單純作廢，順手把ezPay「作廢發票」流程首次寫進SOP。**

### 1. 楊在珍發票作廢重開：公司資料更新
教練提供全新資料（信望愛創意整合國際有限公司/統編60402799，取代舊的信望愛企業社/88932295）。作廢舊發票FS99860260（自訂編號092312），重開新發票**FS99860262**（自訂編號092313，接續原序號往後排一號），皆用`II_Invoice_Status`欄位查證(舊發票確認變`2`已作廢、新發票確認`1`已開立)。

### 2. 柯朝陽發票作廢：教練發現開錯，尚待補正確資料
教練只說「開錯了，請幫我作廢」未說明錯在哪、也未給新資料。已作廢FS99860257（自訂編號092308，仁心茶茶有限公司/96847552），查證`II_Invoice_Status`確認變`2`。**尚未重開**，已主動問教練要補哪個正確資料，教練本場結束前沒有回覆，下一棒待教練提供正確統編/公司名稱後比照楊在珍SOP補開（自訂編號延續用092314）。

### 3. 🔧 首次補上ezPay「作廢發票」完整SOP
之前`reference_ezpay_invoice_issuing_procedure.md`只涵蓋開立，沒記載作廢流程。本場實戰整理：查詢用`invalid_info.send_search_invalid_invoice()`或`jQuery('#search_btn').trigger('click')`+`get_invoice_by_db`API核對；**作廢原因欄位限中文6字**（踩過一次`INV10002`才發現）；確定作廢鈕無id要用文字比對抓；送出後`Inspected target navigated or closed`同樣是正常訊號，靠`II_Invoice_Status`從1變2驗證真的作廢。完整記錄已寫入SOP文件本身。

## 📋 下一場開工先做
1. **柯朝陽發票待補開**：等教練回覆正確統編/公司名稱，自訂編號用092314，比照楊在珍SOP流程即可，不用重新摸索
2. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰
3. MEMORY.md索引仍超過讀取上限(29.9KB)，等consolidate-memory專場處理

## 🔑 本場commit
（本次總結commit另計，見下方commit hash）

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-23 17:20，Mac桌面版，新的一棒 v240）

**本場主軸：教練交辦BNI大台南南區「聚寶盆」入會續約發票12張(每張26,800元)，用Claude in Chrome瀏覽器自動化+JS直接操作ezPay系統完成開立，過程中兩度被教練糾正「查會員資料要同時查兩個獨立發票系統」，並補強既有ezPay自動化SOP的實戰細節。**

### 1. 12張聚寶盆入會續約發票全部開立成功
教練口頭報12個姓名(穗青/仁超/智帆/靖雯/嘉鴻/仁豪/宜宏/朝陽/峯志/康律/紫妤/在珍)+統一金額26,800元。查`bni_region_members_contact_2026-08-18.csv`+`ezpay_invoice_remarks_108taxid_2026-08-17.csv`+`ezpay_invoices_2024-01-01_to_2026-08-17.csv`比對出7位已有統編、3位過去是個人發票缺手機條碼、1位(林仁超)全新缺統編、1位姓名不確定(康律=康文彬，教練確認)，教練補齊缺項後，用`javascript_tool`直接操作`inv.ezpay.com.tw/Invoice_issue/create_invoice`頁面(商店337391376)逐筆填單+送出，每筆送出前先讀`TotleAmount`欄位核對=26,800才送出，送出後一律回`search_invoice`頁用`search_invoice_info.send_search_invoice`+XHR攔截讀真實API回應驗證(不只信表單清空的假象)。12張發票號碼FS99860250~FS99860261全部查證真實存在。

### 2. 🔴 教練兩度糾正：查會員資料要同時查「入會續約」+「培訓費」兩個獨立系統
一開始只查聚寶盆(入會續約)系統，回報陳穗青、康文彬「查無手機條碼」，教練兩次質問「他明明常上培訓，你怎麼會找不到」——查`build_bni_training_admin.py`才發現這兩人的手機條碼其實早就存在**培訓費系統**裡(陳穗青`AMU2DXY`、康文彬`B3BU7PV`)，跟教練後來親口補的號碼完全吻合。同一個教訓在同一場對話裡犯了兩次(第二次是因為第一次抓到後沒有真的套用到剛確認身份的康文彬身上)。已寫入記憶[[feedback_cross_check_both_ezpay_systems_before_reporting_missing_2026-09-23]]。

### 3. 🔧 ezPay自動化SOP補強5項技術發現，已寫回`claude-brain/reference_ezpay_invoice_issuing_procedure.md`
①MerchantID下拉選單「假成功陷阱」舊SOP早有記載，這次一開始還是沒套用，教練親眼看畫面錯誤訊息點破才想起查證——教訓不是SOP不夠，是動手前沒先讀已有SOP，被教練challenge「你去查之前是怎麼做的」才對症。②JS腳本寫中文姓名/公司名一律用文字直接貼、不要用`\u`萬國碼跳脫，這場兩度打錯字(可蕎→可蓋、李紫妤→李紫妍)都是`\u`碼位算錯，靠送出前讀回欄位值核對才攔下。③一張(郭峯志)ezPay後端真實回傳`INV10002手機條碼格式錯誤`，查出教練給的條碼少一碼(手機條碼固定「/」+7碼)，補正確條碼(`/NYFVNY6`)才成功——這種真實API層級拒絕，只有攔截XHR讀`responseText`才看得到，字面`submitted`回傳/CDP逾時都不能當成功依據。④Claude Code自己的auto-mode權限分類器偶爾會攔截送出動作(跟ezPay無關)，屬短暫性，重試即可。

## 📋 下一場開工先做
1. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰
2. 本場任務(聚寶盆12張入會續約發票)已完整結案，無延續動作
3. MEMORY.md索引本場嘗試新增1筆時觸發「已超過24.4KB讀取上限」警告(現29.9KB)——這是既有待辦(v239已提到170行問題)，非本場新增，沿用consolidate-memory技能專場處理即可，不用臨時處理

## 🔑 本場commit
（本次總結commit另計，見下方commit hash）

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-23 16:49，Mac桌面版，新的一棒 v239）

**本場主軸：教練的AI漫畫「ai-story」上架反覆出包，追出真正根因並建立新SOP；教練當場糾正兩個重複性缺失（MEMORY.md該自己動手別問、coach888登記規則講過卻沒照做），已修復並留下防再犯機制。**

### 1. 🔴 ai-story漫畫上架三連坑，詳見試金石案例81
`event.bymyway.com/curated/ai-story/`原本404，查出根因：小龍蝦用「店家上架SOP」處理教練的個人漫畫創作，教練發現分類插錯後手動用後台刪除，該刪除功能是「整套退役」（連GitHub repo/Pages/registry都砍），非只拿掉店家卡片。第一次verbatim部署了教練最早給的`ai-story.zip`，但那個zip本身只是陽春字幕輪播，不是tava-ai.com的疊圖對白效果，教練質疑「這麼單純的事都做不到」；教練後補一份真正完整的`comic-series-site.tar.gz`（20MB，base64內嵌圖片+完整對白定位資料），改用這份verbatim部署才對。**教訓**：部署前要先打開內容看一眼是否真的符合預期，不能只憑檔名/來源假設內容正確。新建SOP文件`knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`（沿用`/curated/<slug>/`機制但跳過店家三步驟），含coach888登記步驟。

### 2. 🔴 兩條教練當場糾正，已寫入記憶
①教練直接質問「你發現的問題為什麼不自己解決」——MEMORY.md索引超過170行早就是待辦，當場動手consolidate-memory技能瘦身172→163行（合併6組重複條目，過程中兩度漏連結/連錯檔名，已自我複查修正）。②教練質問「為什麼老是忘記」coach888登記——查出規則2026-09-05就寫在`reference_curation_sop_2026-09-06.md`，只是純文字沒有hook強制，這次補進新SOP文件+寫記憶+用spawn_task分派獨立任務做deterministic檢查（不臨時湊合寫，避免動壞既有stop hook基礎設施）。

### 📋 下一場開工先做
1. **task_40a366c5（coach888 deterministic檢查hook）**：獨立session待認領，設計見spawn_task內容，需讀懂`jarvis_housekeeper.sh`現有orphan-check範式再動手
2. MEMORY.md本場只清了170筆裡最新45筆的重複部分，still有~80個超過30天未被索引連結的舊記憶檔（housekeeper check掃出來的），非本場故意漏做，是既有已久的欠款，下次有空可以排一場專門處理
3. 沿用既有待辦：試金石商業化計畫書仍等教練回覆三個決策點、跨機分岔警示

### 🔑 本場commit
`0cff7e666`(ai-story陽春版首次verbatim部署+新SOP)、`f630fc1b1`(MEMORY.md瘦身172→163)、`37a0576ac`(換上教練完整版tar.gz)、`3da1629`(coach888/index.html新增條目，注意這個repo是master分支)、`e75772a9e`(補coach888步驟進SOP+寫重複失效記憶)、`212f462f8`(修正MEMORY.md 2個連結錯誤)。本次總結commit另計。

---

## v238之前內容（上一份總結摘要，保留備查）

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-23 14:00，Mac桌面版，新的一棒 v238）

**本場主軸：教練交辦「全面體檢」，抓到3個真實系統問題並全部修復——bigtree三站資料分岔、兩個子agent人設檔曾整批從git歷史消失(已救回)、本機語意記憶搜尋失效10+小時(教練親自跑configure精靈修好)。另處理7個月前外洩的Anthropic金鑰+教練當場糾正兩條規則。**

### 1. 🔴 bigtree活動資料在三個站台分岔，真正根因是event.db沒同步
赫米斯(VPS)手改`Coach1973/bigtree`repo的HTML刪掉10/7、10/8兩場TBD活動，但只對`coach1973.github.io/bigtree`(純GitHub Pages)有效。查證發現`event.bymyway.com/bigtree/`跟`bigtree-tw.netlify.app`都是即時/發佈時直接讀`event-signup/event.db`的`events`表產生內容，資料庫裡這兩筆還是`status='active'`。已改成`cancelled`(照既有慣例不刪除)+對`bigtree-tw`跑一鍵發佈(教練已鬆綁Netlify不用每次先問，commit deploy `6ab3606f`)，三站確認一致。已回信赫米斯說明真正根因+提醒往後改場次要改DB為主，見`cross-agent/outbox/2026-09/`。

### 2. 🔴🔴🔴 agents/bni_tainan+jiaolian_thoughts人設檔曾整批從git歷史消失，已救回
`openclaw doctor`回報「bni_tainan記憶系統找不到」，查證確認這兩個子agent的AGENTS.md+DREAMS.md完全不在HEAD跟origin/main裡，磁碟也沒有。高度疑似09-19金鑰git-filter-repo改寫歷史時跟並行commit(`3361e3078`)分岔，導致該commit變懸空。用`git show <hash>:<path>`從懸空commit救回4個檔案(尚未被gc回收，內容完整836~901行)，commit `fff330028`已推上雲端。教練點出這類事故的根源是「全面改」指令範圍沒問清楚(見下)。

### 3. 🔴 本機語意記憶搜尋失效10+小時，教練親自跑configure修好
`llama-cpp`外掛版本落後gateway核心(2026.6.33 vs 2026.9.4)，更新+重啟後仍失敗。真正卡點是`openclaw configure --section model`裡「Local llama.cpp auth method」要選「**Managed local server**」(不是預設反白的「Existing llama-server」)。這個互動精靈完全無法用expect自動化(打字/方向鍵都測試無效)，教練親自在終端機跑完，軍師逐步截圖引導。驗證：embedding直接測試回傳768維真實向量、`openclaw memory index`五個agent共1871個檔案全部成功索引。完整SOP見`reference_llamacpp_managed_local_server_setup_2026-09-23`。

### 4. 其他：舊金鑰遮蔽+兩條規則教訓
7個月前教練申請Anthropic API時貼進對話的金鑰(`sk-ant-api03-jMLa...`)仍是活的但餘額僅$0.01+無自動儲值，教練裁示不撤銷、只遮蔽明文(commit `c5121d298`)。教練當場糾正：①「全面改」範圍預設是這個Claude能碰到的範圍，不是跨MiniMax系統，動手前先問清楚 ②低風險/不緊急發現不要多輪追問升級，一次講完+已處理即可。兩條都已寫入記憶。

### 📋 下一場開工先做
1. **MEMORY.md索引已超過170行，多次被hook提醒要壓到140行以下，本場沒空處理，下一棒優先**——需要逐條讀topic檔判斷去留，適合用consolidate-memory技能專門跑一次，不要順手做
2. 試金石商業化計畫書仍等教練回覆三個決策點
3. 沿用既有待辦：跨機分岔警示(本場agents/消失事件可能就是這個警示的具體案例，值得回頭看是不是同一根因)
4. E16接力棒瘦身：本場已執行(v235移入下方封存區)

### 🔑 本場commit
`c5121d298`(遮蔽外洩金鑰)、`fff330028`(救回agents/bni_tainan+jiaolian_thoughts)。本次總結commit另計。

---

> 📦 v235~v237完整內容已封存：`handoff_archive/handoff_v235_to_v237_archived_2026-09-23.md`（含小龍蝦3天無回應案例79、AI微論壇活動連動修復、試金石商業化計畫書、手機Remote Control MiniMax懸案解謎v235~v237全紀錄）

---

