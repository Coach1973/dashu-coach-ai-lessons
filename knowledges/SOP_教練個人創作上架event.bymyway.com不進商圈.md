# SOP：教練個人創作（非店家）上架 event.bymyway.com，不進大台南商圈整合中心

> 🔴 **2026-10-04 教練更正（黃秀麗個人品牌頁，聯想軍師誤走創作）：是不是店家不是分界線，是「誰的網站」才是。** 教練自己的作品 → 本份（`kind=creation`）。BNI 夥伴、朋友、客戶的網站，**包含個人品牌頁、不是店家的也一樣** → 走策展 SOP（`kind=shop`，進大台南策展中心名冊）。教練原話：「我幫夥伴們宣傳非常正常，不一定非得是店家，個人品牌一樣要宣傳。」教練說「策展」「上架到策展中心」就是策展 SOP，不要自己改判成創作。

> 🔴 **判斷依據是概念，不是死背固定句子（教練不會念這份檔名）**：只要教練提到「大樹」+「作品／創作」+「上架／上傳／SOP」這幾個概念的任意組合——例如「走大樹創作SOP」「大樹作品SOP」「大樹作品上傳」「大樹創作」「大樹作品上架SOP」「幫我把作品放上去」——都是指這份文件，**不是**`reference-curation-sop-2026-09-06`（店家策展SOP）。**2026-09-26教練親自測出「大樹作品上架SOP」不在原本的死清單裡，證明死背字串這個做法本身就是錯的**，改成判斷「教練丟的是不是他自己的個人創作」這個概念：是→這份文件；是店家/品牌介紹網站→策展SOP。
>
> **教練實際講過的原話（查小龍蝦對話紀錄逐字調出，2026-09-26補）**：9/23 15:27「這個不是策展的店家網站，所以只需要給我網址就可以了，不用放到策展中心去」；9/23 23:55「走大樹創作的SOP」；9/24 00:10（當場糾正做錯）「你走的不是策展中心的SOP，你走的是**大樹教練作品的SOP**」。「個人創作SOP」這個詞是AI自己取的檔案標籤，教練本人沒講過，不要當成教練的原話引用。
>
> 2026-09-23 教練親自交辦「ai-story」漫畫案建立。跟既有「策展SOP」共用同一套 `/curated/<slug>/` 網址與檔案格式，差別只在**跳過店家專屬的三個步驟**。
>
> ⚠️ **2026-09-23 23:55~00:02（台灣時間）復發記錄**：教練當晚兩度明講「走大樹創作SOP」（送 zhaolin 人像照＋送 ai-application-submission-package zip），小龍蝦仍然跑了店家策展SOP、插了大台南商圈卡片，教練事後手動刪除。根因是這份SOP檔名跟教練嘴巴講的詞完全對不上、也沒有任何路由表指到這裡，AI 在壓力下預設用「最熟的那條路」（已用過很多次的店家策展SOP）。修復：已在 `路徑大全_憑證層.md` 的策展金鑰前+`AGENTS.md`按需讀取路由都補上別名警告，並在本檔加上這段別名清單。

## 🔴 2026-10-02 教練三條新規則（每次上架個人作品都照做，三條都不用再問教練「要不要」）

> 教練口語別名（聽到任一句就是這一段）：「檔案太大要壓縮」「幫我壓縮」「選網址／選檔名／短網址」「上大樹小講」「列入大樹小講」「這場我要講」。
> 起因：教練 10/02 交辦一個個人作品，小龍蝦因為檔案太大停下來問「要不要壓縮」，拖了很久；教練回「要」並裁示列入 SOP。

### 規則一：圖片／影片一律壓縮，AI 不再問「要不要壓縮」
- 教練原話：無論檔案大小，只要在網頁上能清楚呈現，都一律壓縮為較小檔案的格式（檔案愈大，網頁呈現愈慢——教練理解正確）。
- **機制（不靠記得）**：`scripts/optimize_site_assets.py` 已接進上傳流程（`curation_process.py` 的 `kind=creation`，解壓後、上架前自動跑，通知訊息會多一行「🗜 壓縮 N 個檔案：A → B」）；壓縮失敗時照原檔上架，不擋上架。
- 做法：圖片（png/jpg）超過 100KB 才處理，最長邊縮到 2000px（手機與視網膜螢幕夠清楚），存成 webp，色彩少的圖表／文字圖用無損 webp（字不會糊），省不到 25% 就保留原檔；mp4 超過 10MB 才重新編碼（H.264，最長邊 1280）。只有在網頁文字裡真的找得到檔名才轉換並改引用，找不到（可能是程式動態組檔名）就不動；外部網址裡的同名檔不改。
- 手動用法（自己打包 zip 的流程也一樣，伺服器端會自動壓，**不必先壓**）：`python3 scripts/optimize_site_assets.py <網站資料夾> [--dry-run]`。
- 這跟「原汁原味、版面不動」不衝突：壓縮只換圖片檔的格式與大小，網頁的版面與文字一個字都不動。
- 驗證：圖片網址要 200 且 `Content-Type: image/webp`；用真瀏覽器開頁確認每張圖 `naturalWidth>0`。
- 首次實測（ema1017，10/02）：4 張圖 13.2MB → 1.1MB，解析度 1600~2000px，與原圖比對 PSNR 45~48 dB（肉眼看不出差別）；原圖備份不進網站。

### 規則二：短網址（檔名）怎麼決定
1. 教練**一開始就指定**了網址／檔名 → 直接用，**不要再問**。
2. 沒指定 → AI 提**三個**候選＋第**四個「由您自己指定」**，一次問完：
   - 每個 **10 個字以內**，只用小寫英文、數字、連字號；
   - 先查不跟 `curated_sites_registry.json` 已有的撞名；
   - 風格參考既有：`ema1017`（簡稱＋月日）、`bigtree-1003`、`tut-memory`；
   - 三個要各有差別（例如：主辦簡稱＋日期／主題英文短詞／主題縮寫），並標示推薦哪一個；
   - 每個網址完整寫出來，**獨立一行**，後面不黏任何字。
3. 教練選一個或自己指定 → 照這個上傳（`custom_slug`）。這是上架過程中**唯一**會停下來等教練的點。

### 規則三：教練是講師＋有報名機制 → 同時列入「大樹小講」
- 判斷（兩個都成立才自動做，不用問教練）：① 頁面上看得到教練（大樹／吳大樹）擔任講師或主講；② 頁面有報名機制（已走「線上報名 SOP」，`event.db` 的 `events` 表有這一場）。
- 成立 → 上架同一輪：把該場 `events.site` 由 `curated` 改成 `bigtree`（**slug 不變**，報名不受影響）。大樹小講清單（`event.bymyway.com/bigtree/`）讀的就是 `site='bigtree'`、狀態進行中、日期未過的場次（讀碼確認：`bigtree_publish.read_sessions`／`render_session_dates`，會帶出場次名稱、日期、地點與這一頁的網址）。後台 `/admin/sessions` 管的是同一張表。
- 上架當下不知道教練是不是講師（頁面沒有教練名字）→ 先只上架為個人作品，**不問、不猜**；之後教練只要說一聲「這場我要講／上大樹小講」→ 當場把 `site` 改成 `bigtree`，並用真瀏覽器確認 `event.bymyway.com/bigtree/` 上有這一場、點進去能到活動頁。
- 不成立（教練不是講師，或沒有報名機制）→ 不列入。大樹小講是教練自己的品牌清單，掛錯別人的場次等於替教練背書。
- 注意：只改 `event.db`＋（教練要同步時）GitHub Pages；**Netlify 正式站（bigtree-tw）要教練說「推」才部署**（`netlify_deploy_guard.sh` 會擋）。`event.bymyway.com/bigtree/` 是即時從資料庫渲染，改完就看得到。

### 規則四（2026-10-04 追加）：列入「大樹小講」的活動，結束後一定自動進「過往講座歷史紀錄」
> 教練口語別名：「歷史頁面」「歷史紀錄」「過往講座」「辦過的活動要留歷史」。
> 教練原話（2026-10-04）：「任何我們在『大樹小講』上架的活動，結束之後一定要自動納入歷史頁面。」
> 起因：9/19 中正大學社團幹部專場辦完，沒有進歷史頁（歷史頁是手動維護的清單，沒人補），教練 10/04 發現。
- **機制（不靠記得）**：`scripts/bigtree_history_sync.py`，launchd `ai.openclaw.bigtree-history-sync` 每天 00:20 自動跑（日期一過就是「結束之後」）。它掃 `event.db` 裡 `site='bigtree'`、`status='active'`、日期已過的場次，歷史頁（`github_repos/bigtree/archive/lecture-history.html` 的 `EVENTS`）還沒有那一天的就自動補一張卡片，commit + push 到 GitHub；`event.bymyway.com/bigtree/archive/lecture-history.html` 直接讀本機檔案，補完立刻看得到。
- **海報**：優先抓該場 `event_url` 活動網頁的 `og:image`（沒有就找 `edm.jpg`）；抓不到就自動產生一張文字卡（日期＋活動名稱＋地點），不會因為缺圖就漏掉。
- **AI 上架時要做的只有兩件事**：① 該場 `events` 列 `site='bigtree'`、`status='active'`；② `event_url` 填活動網頁網址（海報才抓得到）。**不用手動加歷史**；取消的場次要把 `status` 改成 `cancelled`（才不會被補進歷史）；名稱含「待定」的佔位場次不會被補。
- **驗證**：`python3 scripts/bigtree_history_sync.py --dry-run` 會列出「還沒進歷史、將被補登」的場次；空的就是都涵蓋了。紀錄檔 `distill/bigtree_history_sync.log`。
- **不碰 Netlify**：只改 GitHub 與本機檔案；Netlify 的 bigtree-tw 版要教練說「推」才更新（`netlify_deploy_guard.sh` 規定）。
- 首次實跑（2026-10-04）：補進 9/19 中正大學（歷史頁 24→25 場），其餘場次本來就都在。

## 🔴 2026-10-10 教練裁示：大樹作品頁的「聯絡／索取資料／送出」一律進「活動報名即時通知」群

> 教練原話：「我們以後任何大樹作品的頁面，只要有送出通知，只要有這種聯絡或送出通知的介面，一律都發到『活動報名即時通知』。」起因：楊博士頁面（hnv-cc）的「了解訂閱／索取加盟說明／洽詢代工」只留電話，教練要改成線上表單，資料進通知群，邏輯跟活動報名一模一樣。

- **不要為單一作品另開通知管道、不要用 mailto／Tooo.ai／第三方表單**。一律打通用接口 `POST /api/works/contact`（程式在 `event-signup/app.py` 的 `api_works_contact`，資料表 `works_contact_leads`，通知發到 `TELEGRAM_REGISTRATION_GROUP_CHAT_ID`＝「活動報名即時通知」群）。
- 前端做法（同源，頁面在 event.bymyway.com 底下就直接打相對路徑）：`fetch('/api/works/contact', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({site:'<作品網址代號>', name, phone, item, email, message, website})})`；`website` 是隱藏的防機器人欄位，要留著不給人看到。`site` 必須是已在 `curated_sites_registry.json` 登記的 slug。範例：`github_repos/hnv-cc/index.html` 的 `#lead` 表單與最後那段 script。
- 後端已有：姓名／電話驗證（電話至少 8 位數字）、每個 IP 每小時最多 10 次、輸入截斷、資料庫寫入失敗也會通知人工補登。測試：`cd event-signup && python3 test_works_contact.py`（用暫時資料庫＋假通知，不會真的發 Telegram）。
- **測試鐵律**：打真實網址送出＝真的通知教練與佩佩老師，半夜別打；驗證用假通知的測試，或只打會被擋下的請求（缺姓名→400）。
- 接力：已有的非作品頁表單（`/api/KR/contact` 等）是策展店家用的，維持原狀不動。

## ✅ 2026-09-24 起的做法：一步到位，全自動（下方手動7步驟改為備援／歷史參考）

教練以Opus 5.5做團隊體檢後拍板執行：大樹作品跟店家策展共用同一個上傳網址，**只差 `kind` 一個欄位**，系統自己完成全部步驟，不再讓AI手動改coach888網頁。

```bash
curl -s -F "kind=creation" -F "package=@<檔案路徑>" -F "custom_slug=<教練確認的短網址>" \
  "https://event.bymyway.com/curation/upload?key=<見路徑大全_憑證層.md策展金鑰>" \
  -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
```
- 教練自己用手機：打開coach888「大樹常用」裡的作品上傳頁，選「🎨 大樹教練個人作品」→選檔→填短網址→上傳。沒有Telegram的20MB限制。
- 系統自動做：原封不動解壓上架 `event.bymyway.com/curated/<slug>/` → 登記 `curated_sites_registry.json`（category=教練個人創作、no_shop_card）→ 放進coach888「最新作品」第一筆（伺服器同步狀態＋靜態HTML備援，錨點用grid開頭標籤並檢查標籤配對）→ 通知「活動報名即時通知」群組附網址。
- 🔴 **一定要做：建私有GitHub repo**（2026-09-30教練定、10-10教練再次提醒：event.bymyway.com 的靜態網站背後都必須有 GitHub，這樣他在小龍蝦／聯想／宏碁改 GitHub 就好，只有涉及資料庫／程式才回 Mac）。上架程式 `publish_creation()` 已自動呼叫 `scripts/curated_git.py ensure <slug>`；每天 00:40 launchd 會再補一次 `ensure-all`。
- 不做：插大台南商圈卡、發FB。
- `kind` 沒填或亂填 → 上傳直接被擋下（HTTP 400），系統不猜。
- 程式：`event-signup/app.py` `curation_upload()` ＋ `scripts/curation_process.py` `publish_creation()`。

🔴🔴 **2026-09-26新增鐵律：上傳後禁止用「等N秒＋猜/curated/<slug>/」驗證，一律跑狀態查詢工具**——curl回200只代表排進背景佇列，不代表處理完成。2026-09-25赫米斯上傳「證明給機器看」系列連續2次因為包裡沒有剛好叫`index.html`的檔案而背景默默失敗（現已修復：只剩一個html檔會自動採用），赫米斯兩次都是等了一段時間猜網址404才發現不對、寫信給軍師才查出真相。往後上傳後執行：
```bash
python3 scripts/curation_check_result.py "<zip檔名關鍵字或custom_slug>"
```
回傳JSON直接告訴你成功/失敗/還在處理中、真正的最終網址、網址現在活著沒。查不到才需要考慮寫信求助，不要自己猜或等。

## 適用情境
教練自己用外部 AI 工具（TAVA AI／Lovart／ChatGPT 等）做的個人創作（漫畫、故事、作品集……），只想放上 `event.bymyway.com` 有個網址可以分享，**不是店家/夥伴介紹網站**，不該出現在大台南商圈整合中心的店家名冊。

## 跟「策展SOP」的關鍵差異
既有 [[reference_curation_sop_2026-09-06]] 是為店家設計的，會自動做三件事，這三件事對個人創作都是不必要甚至錯誤的：
1. 抓地址、猜分類，插入大台南商圈整合中心店家名冊卡片
2. 自動發大台南商圈整合中心 FB 貼文宣布
3. 開 GitHub Pages（個人創作不用；但**私有 GitHub repo 一定要建**，見上方 2026-09-30 規則，建 repo ≠ 開 Pages）

**教訓案例**：2026-09-23 教練把「ai-story」漫畫包丟給小龍蝦，小龍蝦直接照策展SOP整套跑，被誤判成店家上架，後續處理（很可能是用 `/curation/admin/delete` 下架）連帶把 GitHub repo、Pages、registry 全部砍掉，導致 `event.bymyway.com/curated/ai-story/` 變 404、`log` 卻仍顯示「✅完成」——log 只代表當初上架流程本身沒有丟例外，不代表後來沒被整組刪除，兩者是不同時間點的事，查證時不能只看 log 就下結論。

## ⚠️ 備援：只有上面的一鍵上傳失敗、而且軍師確認要手動補救時才用（平常不要照這段做）

> 2026-09-25：赫米斯看到上面寫「一鍵curl」、這裡又寫「正確做法：手動7步驟」，以為是兩套互相矛盾的SOP。平常一律走上面的 `kind=creation` 一鍵上傳，這段只是歷史備援。
1. **找到原始包**：教練說「打包給小龍蝦」，通常會落在
   `event-signup/curation_uploads/processed/<時間戳>__<檔名>.zip`（已處理過）或
   `event-signup/curation_uploads/incoming/`（還沒處理）。教練若同時貼過對話記錄或截圖，也可以在 `claude-brain/data/` 底下找到對應日期的資料夾。
2. **直接解壓縮到 `/Users/bymyway/github_repos/<slug>/`**（跟策展SOP用同一個根目錄，Flask 就是從這裡讀），保持檔案內容**完全不動**——教練要的是「原汁原味」，不要重新設計版面、不要換字型大小、不要加自己的排版巧思。
   ```bash
   unzip -q <zip路徑> -d /tmp/extract
   rsync -a /tmp/extract/<zip內的子資料夾>/ /Users/bymyway/github_repos/<slug>/
   diff -rq /tmp/extract/<子資料夾> /Users/bymyway/github_repos/<slug>/  # 逐檔比對確認一模一樣
   ```
3. **手動登記進 `event-signup/curated_sites_registry.json`**，不要跑 `scripts/curation_process.py`（那支腳本會執行上面三個店家專屬步驟）。用 Python 直接在 `sites`陣列補一筆：
   ```python
   {
     "slug": "<slug>",
     "title": "...",
     "description": "...",
     "category": "教練個人創作",
     "event_url": "https://event.bymyway.com/curated/<slug>/",
     "github_pages_url": "",
     "uploaded_at": "YYYY-MM-DD HH:MM",
     "status": "live",
     "source_package": "<原始zip檔名>",
     "no_shop_card": true
   }
   ```
   `no_shop_card: true`這個欄位是延用 2026-09-17 bigtree-1003 事故修復時就有的既有慣例（見接力棒 v220 前後），意思是「這筆有效但不是店家，不進名冊」。
4. **不用重啟 Flask**——`app.py` 的 `_load_curated_registry()` 每次請求都重讀 JSON，寫檔案存檔當下就生效。
5. **驗證**：`curl -sI https://event.bymyway.com/curated/<slug>/` 確認 200，再抓一段內容文字比對確認真的是原始版本（不是被哪個環節動過手腳）。
6. **🔴 登記進 coach888「AI作品一覽」，跟上架動作同一輪完成，不要等教練問才補**——這條規則其實[[reference_curation_sop_2026-09-06]]第56~57行早就寫了（「教練自己的作品→收coach888」，2026-09-05教練親定），2026-09-23第一次做這個SOP時漏做，教練事後問「為什麼老是忘記」才發現。做法：
   - `cd /Users/bymyway/github_repos/coach888 && git pull`
   - 在 `index.html` 找 `data-section="gongkai"`（對外公開分類）的 `<div class="grid" data-section="gongkai">` 這個**開頭標籤本身**，新項目直接插在這個開頭標籤**後面**（不是插在「第一個看到的 `<div class="item"` 之前」——這個 grid 裡混雜兩種項目模板：舊版`<div class="item" data-cat="gongkai"><a...><div class="thumb">...</div><div class="meta">...</div></a></div>`跟新版單行`<div class="item" data-url="...">...</div>`，用字串比對找「第一個`<div class="item"`」很可能真的落在舊版項目的`<a>`標籤內部、切在`<div class="thumb">`跟`<div class="meta">`中間，2026-09-24《造林》上架時Hermes就是這樣切壞了「AI人才檢索提案」項目的結構，教練回報「看不到最新作品」，commit `31739ac`修復），其餘項目的 `<div class="num">` 依序遞增（含所有`.item`不管新舊模板都要遞增，避免重複），`<span class="count">N項</span>` 的 N 一併更新
   - **插入後務必檢查HTML標籤配對**：`<div class="grid" data-section="gongkai">`到對應`</div>`之間，`<div`計數要等於`</div>`計數、`<a `計數要等於`</a>`計數，不平衡代表插入位置切壞了既有項目，要重新定位
   - `git add index.html && git commit ... && git push origin master`（**注意這個 repo 預設分支是 `master` 不是 `main`**）
   - 驗證：GitHub Pages 部署有延遲（實測約15秒），`curl https://coach1973.github.io/coach888/` 確認新項目字樣出現才算完成，不要 push 完就回報完成
7. **🔴 發 Telegram 通知到「活動報名即時通知」群組，跟店家策展SOP待遇一致**——2026-09-24教練親自問「即便是大樹個人作品的上架，也一樣要在活動報到通知那邊給我發通知，讓我找得到網址吧？」才發現這條SOP從頭到尾沒有這一步，教練只能自己翻聊天記錄找URL。**這是合理要求，往後每次上架完成都要做**，直接重用店家策展SOP同一套`notify()`（同一個群組、同一個bot_token，只是文案不同，不要另外寫新的Telegram呼叫）：
   ```bash
   cd /Users/bymyway/.openclaw/workspace/event-signup && PYTHONPATH=/Users/bymyway/.openclaw/workspace/scripts python3 -c "
   from curation_process import notify
   notify(
       '🎨【大樹創作・個人作品已上架】\n'
       '標題：<標題>\n'
       '網址：https://event.bymyway.com/curated/<slug>/\n'
       '📌 教練個人創作，不進大台南商圈整合中心店家名冊'
   )
   "
   ```
   已於2026-09-24 00:18實測發送成功（`message_id=11316`），確認`notify()`匯入與呼叫都正常，往後可直接照抄。

## 明確不要做的事
- 不要跑 `python3 scripts/curation_process.py`（會觸發店家三步驟）
- 不要呼叫 `insert_tainan_shangquan_card()`
- 不要呼叫 `post_to_facebook()`
- 不要自己重新設計版面/改字型大小/加自己的詮釋——教練要「一模一樣」就是像素級不動，有意見用視覺重新設計時，先問清楚教練是要「完全模仿」還是「做得更好」，不要自己預設立場硬改

## 🔴 2026-10-02 新增：教練只給「單一 HTML 檔」（沒有 zip）時怎麼辦——自己下載圖片、打包 zip 再上傳

> 起因：教練丟 `design (1).html` 給赫米斯，赫米斯回「HTML 我不會，一定要壓縮檔」，教練裁示：**單檔網頁你也一樣做得到，不准叫教練去壓縮**。聯想軍師照下列流程完成：https://event.bymyway.com/curated/ema1017/
1. 上傳端點只收 `.zip`／`.tar.gz`（送 .html 會 HTTP 400「只接受 zip」）→ **自己打包**。
2. **外連圖片一律下載**（教練明講「不下載怎麼行」）：抓出 HTML 內所有外連圖（`<img src>`、CSS `url()`、srcset；這次是 a.lovart.ai 共 4 張約 13.8MB）→ 下載到 `images/` → HTML 內網址改成相對路徑 → 主檔命名 `index.html` → zip（路徑用正斜線）。打包後確認不再有外連圖網址（Google Fonts 可保留）。
3. `curl -F kind=creation -F package=@x.zip -F custom_slug=<教練指定>`（網名由教練指定，沒指定才提議）。
4. **驗證**：首頁 200＋每張圖片網址都 curl 200。🔴 首頁會先換新、**圖片約 1~2 分鐘後才陸續可讀**，剛傳完圖片 404 是正常，等 2 分鐘再驗，不要誤判重傳。
5. `curation_check_result.py` 只能在 Mac 跑（讀 Mac 本機 log），聯想/宏碁驗證請用上面 curl。
6. 短網址被自己先前的上傳佔用（HTTP 400「已被其他店家用過」）：用 `/curation/admin/delete/<slug>` 下架**自己剛傳的舊版**再重傳（登入步驟見策展SOP「改短網址」段）。別動別人的站。
7. 完整可複製的 Python 打包腳本見信 `cross-agent/inbox/hermes/20261002-0020_lenovo-to-hermes_html-file-you-can-do-it-download-images-and-zip.md`。
8. 用詞：個人作品不叫「上架到名冊」，也不進店家名冊；教練聽到「上架」會困惑，講「放到網址上」。
