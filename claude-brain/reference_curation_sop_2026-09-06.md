---
name: reference-curation-sop-2026-09-06
description: 教練親定「策展SOP」——外部AI工具產出的店家/夥伴網站，從打包到大台南策展中心上架的完整流程，跟「網頁推SOP」「自動站」是三套不同目標的SOP
metadata:
  type: reference
---

# 🎯 策展SOP（2026-09-06 教練口述，軍師修正定稿）

> 🔴🔴 **2026-10-07 教練糾正：「下架」只能收起卡片，不能讓網站不見（試金石案例107）**。後台 `/curation/admin` 現在分三個動作：**下架**＝只把大台南策展中心首頁的卡片收起來（卡片原文存進名冊 `card_html`，名冊標 `listed:false`），網址、本機資料夾、GitHub repo、名冊條目全保留，後台仍列出並標「已下架・網站還在」；**重新上架**＝把卡片原文放回首頁最上方；**刪除**＝網址失效、repo 改名關 Pages、資料夾搬進 `_archive_curation_test_folders/`，**只有「重複」或「上錯」才用**。大樹作品（名冊 `no_shop_card:true`）沒有卡片，後台不給下架鈕。程式：`event-signup/app.py` 的 `unlist_curated_site()`／`relist_curated_site()`；迴歸測試：`event-signup/test_curation_unlist.py`（22 項）。過去被舊「下架」搬走的救回腳本：`scripts/curation_restore_archived.py <slug> --card-commit <策展中心的下架 commit>`（複製回來、repo 改回原名、補名冊與卡片，狀態＝已下架，封存區那份保留）。2026-10-07 已救回：shihmin、zhang-teng-wen、ai-application-submission-package-20260923；其餘 10 個封存都是已有現行版的重複（nmda、nmda-2、ai-class-1017、ema1017 舊版、chen-pei-jun-lao-shi、liujingshanfang、qiu-nan-yin-xiao-nan-diao-ke、c-challenge-2、challenge、ai-story 舊版），留在封存區。

> 🔴 **2026-10-04 教練更正：BNI 夥伴的個人品牌頁（不是店家）也走本篇 `kind=shop`**，不是大樹創作。判斷看「誰的網站」：教練自己的作品→創作；夥伴／朋友／客戶的→策展。教練也說：所有上架的網站都要有一份 GitHub（`kind=shop` 流程本來就會建 repo，要確認並回報）；靜態、不碰資料庫的修改，聯想／宏碁都能做，只有程式或資料庫才交 Mac 軍師。聯想沒有策展上傳金鑰，新上架要寫信給小龍蝦（`cross-agent/inbox/xiaolongxia/`，範例 `20261004-1419_lenovo-to-xiaolongxia_hsiuli-curation-shop-upload.md`）。

> 🔴🔴 **2026-09-26教練拍板：`shops.bymyway.com`不再架在VPS(43.245.60.200)上，全部改本機Mac處理**——當初用VPS是為了「24小時不間斷、隨時能接收新店家」，但實測發現`event.bymyway.com`（含上傳網址本身）本來就跑在這台Mac上（透過Cloudflare Tunnel），Mac沒開機的話整條上傳流程一樣會停，VPS並沒有真的多提供獨立於Mac之外的可用性，純粹多一層SSH管理成本、多一種故障模式（09-26鑫瀚昌旅行社事故的custom_slug被覆蓋、SSH寫入偶爾被沙盒攔下等，本質都是這層VPS依賴造成的額外複雜度）。且實際只用到3個真實店家(huitou/ema/鑫瀚昌`hsinhan`)，遷移成本很低。
> **技術細節**：`shops.bymyway.com`的3個既有店家已從VPS下載搬進本機`/Users/bymyway/github_repos/<slug>/`（跟`/curated/<slug>/`共用同一套目錄+`_serve_repo_file()`），`event-signup/app.py`新增`shops_local_page()`/`shops_local_assets()`兩支路由用`request.host`分流只認`shops.bymyway.com`；Cloudflare DNS紀錄從A(43.245.60.200)改CNAME指到跟`event.bymyway.com`同一個tunnel(`739a34e4-9088-42f9-8819-ae1d2667e50e.cfargotunnel.com`)，`~/.cloudflared/event-config.yml`新增一行ingress。`app.py`的`_provision_shop_placeholder()`、`curation_process.py`的`overwrite_shop_placeholder()`/`rename_shop_slug()`全部改成本機檔案操作，不再有任何`sshpass`/`SHOPS_VPS_*`程式碼。VPS上的原始檔案**暫時保留沒刪**（`/var/www/shops/`），當作一段時間的備援，非立即需要不用管它。
> 下面文件裡所有提到「VPS」「SSH」「43.245.60.200」的段落都是**歷史記錄**，保留是為了理解「為什麼會有`_shops_slugs.json`這個既有暫代頁比對機制」的脈絡，**不是現在的實際做法**。

> 🔴 **2026-09-24 起上傳網址 `kind` 必填**：`kind=shop`＝本篇店家流程；`kind=creation`＝大樹作品（原封不動上架＋自動進coach888「最新作品」第一筆＋通知群組，不建repo、不插商圈卡）。沒填或亂填直接HTTP 400，系統不猜。詳見 `knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md` 開頭段、[[project_team_publish_and_daily_report_goal_2026-09-24]]。

> 🔴🔴 **2026-09-26教練根因質問後新增鐵律：上傳後禁止用「等N秒＋猜網址」驗證，一律跑狀態查詢工具**——curl回200只代表「檔案收到排進佇列」，不代表處理完成，也不保證最終網址等於`custom_slug`（命中既有`shops.bymyway.com`暫代頁時網址會被改掉，見下面規則二）。過去Hermes兩次上傳後都靠猜（一次真的失敗、一次成功但猜錯網址），兩次都得寫信給軍師人工查log才知道真相——**這不是AI理解力問題，是SOP從沒提供機器可查的真相來源，只給了人看的Telegram通知**。往後上傳後（不管等多久）一律執行：
> ```bash
> python3 scripts/curation_check_result.py "<zip檔名關鍵字或custom_slug>"
> ```
> 回傳JSON會直接告訴你：處理完了沒(`pending`/`success_shop_new`/`overwritten_existing`/`success_creation`/`failed`)、真正的最終網址(`actual_url`)、這個網址現在活著沒(`live_check_http_status`)。看到`overwritten_existing`代表命中既有暫代頁、`custom_slug`被略過，網址是`shops.bymyway.com/...`不是`event.bymyway.com/curated/...`，這是正常設計不是錯誤，不用再寫信確認。查不到才需要考慮寫信求助。

> 跟另外三套既有SOP的關係（四者目標站不同，不可混用）：
> - **網頁推SOP**（[[feedback_web_push_sop]]）：推送到GitHub測試站 或 Netlify正式站，教練說「網頁推/推」才會觸發
> - **自動站**（[[feedback_coach_deploy_vocabulary]]）：部署到bymyway.com（WP iframe抓GitHub repo新版）
> - **策展SOP**（本篇）：教練用外部AI工具做好的店家/夥伴網站，經GitHub Pages + event.bymyway.com + 大台南策展中心店家名冊三層上架，目的是讓夥伴店家有專屬網址並被策展中心收錄
> - **報名頁上架SOP**（[[reference_event_registration_page_sop_2026-09-17]]，2026-09-17 NEW）：一頁式報名網頁（多為大樹小講/教練演講活動），涉及event.db寫入+即時Telegram通知，跟本篇同屬「上架SOP」觸發詞下的另一條分支——教練說「上架SOP」時，AI依內容是「店家介紹」還是「報名表單」自動判斷走哪一篇

## 完整流程（六步）

**第一步｜教練生成網站**
教練用TAVA AI、Tooo.ai、Lovart.ai、Gemini、ChatGPT等工具產出店家/夥伴的網站原始碼，請AI工具打包（zip/tar.gz，含圖片assets）。

**🔴 2026-09-08教練交辦：生成網站時順手請AI工具把完整地址寫清楚，源頭一次到位**
起因：教練發現策展上架後大台南策展中心店家名冊卡片沒有Google地圖，每次都要自己手動開Google地圖找、複製連結貼上。查證發現根因是`curation_process.py`原本插卡片時完全沒抓地址（自助登錄那條路`_provision_shop_placeholder()`因為表單本來就有地址欄位，一直都有自動地圖，兩條路徑落差在這裡）。**已修復伺服器端**：新增`extract_address()`用正則掃網站原始碼裡的台灣地址格式(市/縣+路/街+號)，抓到就自動產生跟自助登錄同款的Google地圖embed(query-based，不需要API Key)插進店家卡片；抓不到就照舊不顯示地圖，非致命。**教練同場點出更根源的做法**：與其事後用正則猜地址，不如**請TAVA AI/Lovart.ai/ChatGPT等工具生成網站時，就把完整地址（市+區+路street+號）用清楚的文字寫在頁面上**（例如「門市」「聯絡我們」區塊，牛市町案例本來就這樣做，抓取100%成功）——這樣伺服器端的正則抓取才穩定可靠，一氣呵成不用事後補救。**往後教練/AI請外部工具生成店家網站時，順手加一句「請把完整地址用清楚文字寫在頁面上」**，抓不到地址的網站，教練若發現卡片沒地圖，可判斷是原始網站本身沒寫地址，回頭跟生成網站的AI工具要求補上即可，不用來源不明地猜測。

**🔴🔴 2026-09-06當晚教練追問後大幅修正：誰該走哪條路，兩層規則**

**規則一（🔴2026-09-06凌晨04:06教練拍板定案，取代下面舊版）：不分是誰、有沒有終端機能力，一律用上傳網址**
- 舊版規則（有終端機能力的AI要手動做七步驟）已作廢，理由見下方「規則二」後面的更新說明——暫代頁判斷已自動化，上傳網址對所有情況都安全，手動流程只是白白多花時間跟資源。
- **教練本人 + 任何AI（軍師/Hermes/OpenCode/小龍蝦/任何機器的Claude終端機）→ 一律直接curl上傳到`event.bymyway.com/curation/upload?key=<專屬金鑰>`**，不用自己動手建GitHub repo，也不用先判斷有沒有暫代頁——背景腳本會自動判斷並正確處理。
- 手動七步驟（下方第三步）**只在自動化壞掉、或遇到`huitou`/`kr`這種舊命名撞名的邊界情況時才當備援用**，不是常態路徑。

**規則二（動手前先確認）：這個店家是不是已經走過「自助登錄」流程、已經有shops.bymyway.com暫代頁？**
- 2026-09-06真實案例（迴頭快剪）教訓：這個店家先前透過大台南策展中心「加入我們」表單自助登錄過，系統已經自動建了`shops.bymyway.com/huitou/`暫代頁（`_provision_shop_placeholder()`那條路，見`reference_new_site_collection_policy`）。現在教練拿到TAVA AI做好的正式網站，**不是策展SOP該管的範圍**——正確做法是**直接把完整網站檔案SCP上傳到VPS覆蓋掉暫代頁**，網址完全不變還是`shops.bymyway.com/huitou/`，**不需要建新GitHub repo、不需要`event.bymyway.com/curated/`、不需要`tainan-shangquan`額外插卡片**（原本表單送出時就已經插過一次卡片了）：
  ```bash
  sshpass -p '<VPS密碼，見路徑大全_憑證層.md>' scp -r <解壓縮後的網站資料夾>/* root@43.245.60.200:/var/www/shops/<原有slug>/
  ```
  上傳後curl驗證`shops.bymyway.com/<slug>/`內容已經是正式網站、不再是暫代頁的樣子即完成。
- **動手前判斷方法**：先curl `https://shops.bymyway.com/<可能的slug>/` 或查`tainan-shangquan/_shops_slugs.json`這份registry，命中就是這條路（VPS覆蓋暫代頁）；查無記錄才是全新的策展SOP案例（第三~六步）。
- 這條規則被2026-09-06 Hermes實際卡住的案例挖出來——它正確發現了`shops.bymyway.com/huitou/`既有記錄，但被SOP文件誤導去研究不該套用的策展流程，才卡住猶豫。**這不是AI理解力差，是SOP文件本身沒寫這個分支**。

**🔴 2026-09-06凌晨04:00再修正：規則二已寫進`curation_process.py`自動判斷，不用再靠人工判斷**
教練追問「牛市町案例明明比Hermes還快，為什麼不乾脆都走上傳網址」後點破：規則一（有能力的AI要手動做）存在的唯一理由，就是自動上傳路徑原本不會判斷「這家店是不是已經有暫代頁」，會無腦建一個重複新站。**這個判斷邏輯已經內建進`curation_process.py`本身**（新增`find_existing_shop_slug()`+`overwrite_shop_placeholder()`，commit待補）：上傳的zip只要品牌名（`<title>`分隔符號前那段）轉拼音後跟`_shops_slugs.json`裡的既有slug相符，就自動改成SCP覆蓋暫代頁內容（tar打包+遠端解壓，網址不變），完全不建新GitHub repo，也不會重複插店家名冊卡片。**這代表規則二的人工判斷已經自動化，`event.bymyway.com/curation/upload`現在對「全新店家」跟「已有暫代頁的店家」兩種情況都安全**，理論上規則一（有能力的AI要手動做）可以考慮退休——但保留這條規則的一個殘餘理由：`huitou`/`kr`這兩筆最早期手動建立的暫代頁，slug是人工取的沒有跟著`_shop_slug()`演算法走，**新版自動比對用的是「品牌名轉拼音」演算法，這兩筆舊資料算不出來會比對失敗**（純算法限制，非bug），未來若有店家名稱剛好對到`huitou`/`kr`這類舊命名，還是需要人工確認一次。2026-09-06之後新建立的自助登錄暫代頁（`_provision_shop_placeholder()`那條路）都是同一套演算法自動產生，不會有這個落差。

**第三步｜執行的AI完成GitHub Pages上架（僅適用「規則二」判斷為全新案例時）**
依照既有SOP [[reference_zip_to_github_pages_deploy_sop]] 七步驟：解壓縮 → **repo名稱直接取網站`<title>`標題轉拼音，不用再問教練選項**（2026-09-06教練親口拍板：「都跟這個網站的主標題一致就好，就不要再問了。如果要修改的話，會特別跟你說要怎麼修改」——只取品牌主名的拼音，跟`curation_process.py`的`slugify_title()`同一套邏輯，不用列A/B/C選項等教練挑） → 用`git credential fill`取得GitHub token → REST API建repo → push內容 → 開GitHub Pages → 驗證上線(文字+圖片都要curl驗證，不能只看HTTP狀態碼)。

**第四步｜完成後通知軍師**
如果是Hermes/ACER/聯想等非本場軍師執行的，寫信到`cross-agent/inbox/mac/`；如果本來就是軍師自己做的，這步跳過直接進第五步。

**第五步｜軍師接手串接event.bymyway.com + 大台南策展中心**
🔴 **修正教練原本的理解**：這一步**不是連到VPS**——VPS(`shops.bymyway.com`)是另一套完全不同的後端，只服務「大台南策展中心自助登錄表單」送出的店家(`_provision_shop_placeholder()`自動流程)。教練親自拿zip給AI做的這套，走的是：
1. 在`event-signup`（Mac Flask app）新增路由，用`_serve_repo_file()`直接讀該GitHub repo內容，網址是`event.bymyway.com/<repo-slug>/`（repo名稱＝教練或AI取的英文/拼音名）
2. 在`tainan-shangquan`（大台南策展中心）首頁的`SHOP_CARDS_INSERT_POINT`標記下新增一張真實店家卡片（店名/描述/分類食衣住行育樂/連到專屬網站按鈕）
3. curl驗證兩處都正確顯示，並用真實Chrome開一次確認畫面

**第六步｜歸類原則 + 通知教練**
- 「教練朋友/客戶一次性網站」→ 只收錄`tainan-shangquan`店家名冊，**不收coach888**（2026-09-05教練親定，見[[reference_new_site_collection_policy_2026-09-05]]）
- 「教練自己的作品」→ 收coach888
- 🔴 **2026-09-06教練發現真漏洞已修復**：「黑糖農莊」「立馬吃一鍋」兩家手動照SOP上架後完全沒收到通知——通知程式碼原本只寫在`/curation/upload`（給沒能力的人用）跟`/api/tainan-shangquan/join`（自助登錄表單）兩支自動化端點，**手動流程從沒呼叫過，不是bug是SOP空白**。已改成`tainan-shangquan` repo的`.git/hooks/post-commit`：只要commit新增了一張`<article class="shop-row">`卡片，不管是誰、用哪種方式做的，一律自動發Telegram到活動報名即時通知群組，不再依賴任何人「記得」這一步。事件驅動（掛在commit動作本身），非輪詢。**這一步現在不用手動做，寫完卡片commit下去就會自動通知。**

## 兩件教練提出的天馬行空構想，評估結果

### 構想一：直接登入教練的AI創作中心，收到通知自動下載上傳部署

**評估：不建議直接登入各家AI工具帳號自動化，改用「共用資料夾+事件觸發」更務實。**

原因：
1. TAVA AI/Tooo.ai/Lovart.ai/Gemini/ChatGPT每家介面、匯出流程都不同，要對每一家分別寫瀏覽器自動化腳本，工程量大且脆弱（介面一改版就失效）
2. 這些工具幾乎都沒有「產生完成」的webhook/API通知機制——真的要做，只能定時去每個工具的後台檢查有沒有新專案，這正好踩到守則#07「事件驅動優於輪詢」的紅線，教練已經糾正過至少6次同類坑
3. 帳密風險分散到很多第三方網站，不如集中在教練自己能完全控制的地方

**替代方案（真正的事件驅動，且已有成熟先例可以直接複製）**：
比照名片系統的`namecard-inbound`機制——設一個共用資料夾（可以是iCloud雲端硬碟、Google Drive本機同步資料夾，或Amber私有雲的一個子目錄），教練把AI工具匯出的打包檔案拖進這個資料夾即可，**不用再手動傳給小龍蝦/Hermes**。技術上用macOS launchd的`WatchPaths`（跟名片系統`com.coach.namecard-amber-watch.plist`同一種機制，已驗證是真事件觸發非輪詢），資料夾內容一有變化就自動觸發第三步的GitHub Pages上架流程。教練唯一要做的動作，從「下載完傳給某個AI」簡化成「下載完丟進資料夾」，兩者都是手動一步，但後者完全自動接續。

如果教練想要，下次可以直接建置這個資料夾監控機制，不需要額外詢問，方向清楚。

### 構想二：每個店家上線後單獨在大台南策展中心FB發一則貼文宣布

**評估：可行，已用現有FB自動化架構（`fb_automation/page_tokens_2026-09-01.json`，大台南策展中心 page_id `612941615239114`）驗證，非新建機制。**

已完成教練交辦的即時任務：現有5個已上線店家（林貝羿・逸心生技、66街道咖啡、臺南匹克藝術扶輪社、KingMauii金茂宜咖啡、中華網紅協會CICA）逐一寫行銷文案並用Graph API `/photos`端點帶圖發布，全部已用`permalink_url`驗證真實上線，非僅API回傳成功假設：
- https://www.facebook.com/122198437562837553/posts/122198810750837553（林貝羿）
- https://www.facebook.com/122198437562837553/posts/122198810852837553（66街道咖啡）
- https://www.facebook.com/122198437562837553/posts/122198810912837553（臺南匹克藝術扶輪社）
- https://www.facebook.com/122198437562837553/posts/122198811014837553（KingMauii金茂宜咖啡）
- https://www.facebook.com/122198437562837553/posts/122198811080837553（中華網紅協會CICA）

**往後常態化**：策展SOP第六步「通知教練」時，同一輪順便完成這則個別FB貼文（用該店家網站的og:image或代表圖+行銷文案+連到`event.bymyway.com/<slug>/`+連到`tainan-shangquan`首頁），不用教練每次額外交辦。

## 🎯 2026-09-06當場加碼：上傳網址上線 + 策展一鍵注入頁面

教練當場要求把構想一（共用資料夾+事件觸發）落地成一個**真正的上傳網址**，而不只是本機Mac資料夾（因為教練常在外面用其他機器）。已完整建置並端到端實測：

- **上傳網址**：`https://event.bymyway.com/curation/upload`（兩種登入方式：既有admin帳密`bymyway`/`88888`，或帶專屬金鑰`?key=<CURATION_UPLOAD_KEY>`）
- **背景自動處理**：`scripts/curation_process.py`，由`com.coach.curation-watch.plist`（launchd WatchPaths監控`event-signup/curation_uploads/incoming/`，事件觸發非輪詢）觸發，流程：解壓縮→拼音轉slug→建GitHub repo+push+開Pages→登記`curated_sites_registry.json`（`event.bymyway.com/curated/<slug>/`路由讀這份registry當白名單，避免曝光`github_repos/`底下其他含個資的內部repo）→插入`tainan-shangquan`店家卡片→Telegram通知
- **策展一鍵注入頁面**：`https://coach1973.github.io/ai-go/curation-inject.html`（比照既有「特助心法一鍵注入」樣式），複製`curation-prompt.md`內容貼給任何AI，AI只要問清楚檔案路徑、跑一行curl上傳即可，不需要自己動手做GitHub部署
- **為什麼用獨立金鑰而非後台密碼**：這個一鍵注入頁面是公開網頁，任何人都可能複製到提示詞內容，如果直接放後台主密碼等於後台密碼公開外流。改用`CURATION_UPLOAD_KEY`（跟`.env`裡的`EVENT_ADMIN_PASSWORD_HASH`完全獨立），外流最多只能觸發「上傳zip建網站」這個單一動作，不能登入後台改任何既有資料，且隨時可換掉不影響教練登入
- **已知殘留風險**：`curation-inject.html`設了`noindex`但URL本身仍是公開可存取的靜態頁面，任何拿到連結的人理論上都能看到這把鑰匙——這是「方便任何AI都能用」跟「完全保密」的必然取捨，教練已知情此設計方向

## 🔴 2026-09-06深夜修復：改短網址一律用`curated_site_rename.py`，禁止再手動改

教練當晚連續4次要求把自動產生的過長網址改短（百聖/楊尚儒/張騰文/Esther楊在真），
每次都是不同AI各憑印象手動做4件事（GitHub repo改名/本機資料夾改名/registry換
slug/策展中心卡片連結換新），**沒有任何一次留下「舊網址→新網址」的轉址**，
導致教練事後回報：改名前已經自動發到FB的貼文連結、店家自己留存轉發的舊連結，
全部變成404。

**根因**：`curation_process.py`的`slugify_title()`遇到「沒有清楚分隔符號的完整
公司全名」（如「百聖廣告設計工程有限公司」整句無分隔符號）或用純「-」(無空格)
分隔的標題（如「張騰文-騰文昌」），原本只認｜/—/：這類符號，抓不到，slug還是
會很長。已修復：分隔符號補上純「-」+ 抓到品牌名後順手砍掉常見公司尾綴
（有限公司/工作室/企業社/廣告設計/設計工程等）。**但業務名稱千變萬化，這個
規則式做法不可能每次都猜出教練真正想要的最短品牌名（如「百聖廣告設計工程
有限公司」教練想要的其實是「百聖」兩字），所以不能只靠改善猜測演算法收尾**。

**真正的修復是加上「改名不死連結」機制**：`event-signup/curated_sites_registry.json`
新增`redirects`欄位（`{"舊slug": "新slug"}`），Flask的`/curated/<slug>/`路由
改名後找不到slug時，會先查這張表，命中就301轉址到新網址——**不管未來被誰用
什麼方式改短幾次，只要走這個機制，舊連結永遠活著，FB貼文/名片/QR code都不會
因為改名而死掉**。已補回這次4個案例的redirects記錄，4個舊網址現在都curl驗證
會自動跳轉到新網址且200。

**新建`scripts/curated_site_rename.py`**：把改名要做的5件事（GitHub repo改名/
本機資料夾+remote同步/registry換slug/寫入redirects/tainan-shangquan卡片連結
同步）合併成一支腳本，用法：`python3 scripts/curated_site_rename.py <舊slug> <新slug>`。
**往後教練要求「這個網址改短」，一律跑這支腳本，不要再手動逐一操作**——手動做
最容易漏掉的就是redirects這一步（因為它不影響「看起來改名成功了」的當下驗收，
只有等舊連結被外部引用後才會發現死掉，教訓成本很高）。

## 🔴 2026-09-06深夜再修正：教練否決redirect補救方案，改成源頭強制輸入短網址

教練看到上面的redirect機制後明確表態不喜歡：「明明就是一個錯的網址，還要把它轉址到正確的，我覺得很費勁，我比較喜歡從源頭解決」。教練提出兩件事並已落地：

1. **源頭解決（已完成）**：`event.bymyway.com/curation/upload`上傳表單新增**必填**的「自訂短網址」欄位（`custom_slug`），送出前教練或夥伴自己決定短名稱，伺服器端驗證格式(小寫英文/數字/短橫線)+是否重複，沒帶這個欄位會直接400拒絕上傳。`curation_process.py`的`process_one()`優先採用這個值(`read_custom_slug()`)，不再依賴`slugify_title()`的拼音猜測(拼音邏輯保留當ai-go一鍵注入等其他呼叫端的備援，但主要上傳頁面已不會走到它)。`curation-prompt.md`(策展一鍵注入給其他AI用的指令文字)+`SOUL.md`(小龍蝦指示)+`H_HANDOFF_LATEST.md`(Hermes指示)三處同步更新，都改成「先問短網址，curl帶`-F custom_slug=`」。
2. **既有4~5個已發布錯誤網址的清理（已完成）**：教練原意是「FB刪掉重貼」，查證後改用**編輯貼文文字**(Graph API `POST /{post_id}` 帶`message`參數可直接改文案，含連結)達成同樣效果但保留原貼文的按讚/留言/發布時間，不需要真的砍掉重發。已修正bai-sheng/yang-shang-ru/zhang-teng-wen/yang-zai-zhen/niu-shi-ting共5則FB貼文的連結，逐一用Graph API GET驗證新網址已生效。Telegram「活動報名即時通知」群組裡的舊網址訊息**沒有清除**——嘗試過Telegram Bot API沒有瀏覽群組歷史訊息的能力、桌面版App在背景操控點擊沒有反應，冒然用message_id範圍猜測有刪到別人訊息的風險，已如實告知教練這個限制，改成**這個redirect機制本身仍保留**當安全網——即使Telegram舊訊息裡的舊網址沒清掉，點下去也會自動轉址到對的地方，不是死連結。
3. **notify()已補上message_id記錄**：`curation_process.py`的Telegram通知函式原本送出後完全不記錄回傳的`message_id`，這次想清舊訊息時才發現完全查不到——已修復，往後每則通知的message_id都會寫進`distill/curation_process.log`，之後真的要清特定訊息可以直接查log呼叫`deleteMessage`，不用再靠人眼翻聊天記錄。

**redirect機制維持不動**——教練沒有要求移除，只是不想再依賴它當「主要」解法，改成source-fix為主、redirect當zero-cost安全網，兩者不衝突。

## 🔴 2026-09-06下午追加：「改短網址」完整SOP，教練/軍師/Hermes/小龍蝦皆可直接執行

教練當面問「這件事只是簡單的文書作業，Hermes跟小龍蝦是不是也能做」——查證屬實：這整套流程就是幾個curl打公開網址，不需要判斷力，Hermes(這台Mac上的獨立agent，workspace跟軍師symlink共用)+小龍蝦(main agent，已實測`ls -la`成功，`openclaw.json`無工具限制)都有終端機能力可以做。**下面三步都不需要教練自己登入任何後台或FB**：

**第一步｜下架舊的長網址**（先取得admin session cookie，再打刪除路由）
```bash
curl -s -c /tmp/curation_cookie.txt -d "username=0901056777" -d "password=88888" \
  https://event.bymyway.com/admin/login -o /dev/null
curl -s -b /tmp/curation_cookie.txt -X POST \
  https://event.bymyway.com/curation/admin/delete/<舊的slug> -o /tmp/curation_delete_resp.html
grep -o "已下架「[^」]*」" /tmp/curation_delete_resp.html
```
（`<舊的slug>`從舊網址`event.bymyway.com/curated/<slug>/`裡取；下架不是真刪除，本機資料夾搬去封存區、GitHub repo改名關Pages，資料不會消失）

**第二步｜用新短網址重新上傳**（同一份zip，走既有上傳SOP，見上面SOUL.md/curation-prompt.md已有的步驟，帶`custom_slug=<教練指定的新短網址>`）

**第三步｜修正FB舊貼文文字**（若這家店之前發過FB貼文才需要這步，用編輯不用砍重發，保留讚/留言）
```bash
# 先查這家店對應的FB post_id：grep distill/curation_process.log找店名附近的「FB貼文成功」那行，裡面的JSON含id欄位
grep -B2 -A2 "<店名關鍵字>" /Users/bymyway/.openclaw/workspace/distill/curation_process.log
# 讀取粉專access_token
cat /Users/bymyway/.openclaw/workspace/fb_automation/page_tokens_2026-09-01.json
# 用access_token+post_id編輯貼文文字(把舊網址換成新網址)
curl -s -X POST "https://graph.facebook.com/v20.0/<post_id>" \
  -F "message=<修正後的完整文案，含新網址>" \
  -F "access_token=<page的access_token>"
```
查不到對應post_id（沒發過FB貼文，或log裡找不到）就跳過這步，只做前兩步即可，網址本身已經是對的。

**⚠️ 2026-09-06下午更正**：本文件先前(深夜段落)寫「一律用`scripts/curated_site_rename.py`不要手動操作」，教練事後追問zhang-teng-wen案例時，實際確認的正確做法是「先下架、再用新短網址重新上傳」（即本節三步驟），不是跑改名腳本——那支腳本是redirect年代的產物，教練已否決redirect當主要解法，**下面這行「How to apply」以本節為準**。

## How to apply
下次教練說「策展SOP」或描述類似「AI工具做的店家網站要上架大台南策展中心」的任務，直接照上面六步走。構想一的資料夾監控機制，教練若說「做吧」可直接動手，架構已經想清楚不用重新評估。**教練要求改短既有網址時，照上面「改短網址完整SOP」三步驟走（下架→重新上傳→視情況修FB貼文），不要用`curated_site_rename.py`**。上傳頁面現在會強制要求短網址欄位，不用再擔心系統猜出過長網址。這整套流程軍師/Hermes/小龍蝦皆可直接執行，不需要教練親自操作任何後台。

Related: [[reference_zip_to_github_pages_deploy_sop]]、[[reference_new_site_collection_policy_2026-09-05]]、[[project_namecard_ocr_pipeline_reusable]]（WatchPaths事件觸發的原始先例）


## 🔴 2026-09-27 教練拍板：全站店家網址統一 event.bymyway.com/curated/<slug>/
- shops.bymyway.com 只剩舊連結永久轉址（301），本身不供應任何檔案；kr 轉到 event.bymyway.com/KR/。
- 自助登錄表單的暫代頁也直接建在 /curated/<slug>/ 並登記進 curated_sites_registry.json；覆蓋成完整網站時同步更新名單、改名時舊 slug 寫進 redirects。
- 原因：兩種開頭訪客分不出差別，且 09-26 的三個事故（custom_slug 被蓋、卡片漏換照片、github_repos 外洩）全出在 shops 這條少用的路。
