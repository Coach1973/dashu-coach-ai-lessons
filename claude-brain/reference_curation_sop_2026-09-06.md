---
name: reference-curation-sop-2026-09-06
description: 教練親定「策展SOP」——外部AI工具產出的店家/夥伴網站，從打包到大台南策展中心上架的完整流程，跟「網頁推SOP」「自動站」是三套不同目標的SOP
metadata:
  type: reference
---

# 🎯 策展SOP（2026-09-06 教練口述，軍師修正定稿）

> 跟另外兩套既有SOP的關係（三者目標站不同，不可混用）：
> - **網頁推SOP**（[[feedback_web_push_sop]]）：推送到GitHub測試站 或 Netlify正式站，教練說「網頁推/推」才會觸發
> - **自動站**（[[feedback_coach_deploy_vocabulary]]）：部署到bymyway.com（WP iframe抓GitHub repo新版）
> - **策展SOP**（本篇，NEW）：教練用外部AI工具做好的店家/夥伴網站，經GitHub Pages + event.bymyway.com + 大台南策展中心店家名冊三層上架，目的是讓夥伴店家有專屬網址並被策展中心收錄

## 完整流程（六步）

**第一步｜教練生成網站**
教練用TAVA AI、Tooo.ai、Lovart.ai、Gemini、ChatGPT等工具產出店家/夥伴的網站原始碼，請AI工具打包（zip/tar.gz，含圖片assets）。

**第二步｜教練把打包檔交給任一台AI**
教練可以傳給小龍蝦、Hermes或直接跟軍師（任一台機器的終端機/桌面版）說。
**🔴 修正教練原本的理解**：小龍蝦（OpenClaw main agent）本身**沒有檔案系統/執行指令的工具權限**（`toolsBySender`已鎖exec/fs），收檔案沒問題，但**沒辦法親自完成「解壓縮→上傳GitHub」這個技術動作**。真正能獨立跑完這步的只有：
- **軍師**（任何一台機器的Claude終端機/桌面版）
- **Hermes**（Mac桌面版全功能代理，有終端機能力）
小龍蝦收到打包檔案時，應該做的是「收到後告知教練會請軍師處理」或寫派工單通知軍師，不是自己動手上傳。

**第三步｜執行的AI完成GitHub Pages上架**
依照既有SOP [[reference_zip_to_github_pages_deploy_sop]] 七步驟：解壓縮 → 檢查repo名稱是否為ASCII(中文檔名要先問教練或取英文/拼音名) → 用`git credential fill`取得GitHub token → REST API建repo → push內容 → 開GitHub Pages → 驗證上線(文字+圖片都要curl驗證，不能只看HTTP狀態碼)。

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
- 完成後Telegram通知教練+軍師都看到剛建好的網址

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

## How to apply
下次教練說「策展SOP」或描述類似「AI工具做的店家網站要上架大台南策展中心」的任務，直接照上面六步走。構想一的資料夾監控機制，教練若說「做吧」可直接動手，架構已經想清楚不用重新評估。

Related: [[reference_zip_to_github_pages_deploy_sop]]、[[reference_new_site_collection_policy_2026-09-05]]、[[project_namecard_ocr_pipeline_reusable]]（WatchPaths事件觸發的原始先例）
