# 軍師接力棒 · 2026-09-20 v231（Mac桌面版 Sonnet 5，TokenTable接入OpenCode+Episode 11五格漫畫生成+抓到agent備援模型捏造完工的真實案例）

> 建立時間：02:47 ~ 12:44（約10小時，多數時間閒置待命）
> 上一棒：v230
> 本棒主軸：**教練提供TokenTable(第三方AI算力轉售平台)的API Key，要求接進本機工具。軍師選擇接OpenCode(不接Hermes，風險考量)，驗證出TokenTable的Claude系列模型工具呼叫有平台bug、GPT系列正常。核心是釐清教練真正需求(省軍師自己的token到禮拜三)，最後用OpenCode+TokenTable自主生成Episode 11五格漫畫，過程中抓到OpenCode配額用盡後的備援模型會捏造完工結果，軍師自己查證+補完，這是本場最重要的發現。**

## 🎯 本場戰果

### 1. TokenTable接進OpenCode，技術盤點完成
- 設定寫在`~/.config/opencode/opencode.jsonc`的`provider.tokentable`，跟既有kimi/opencode-go同樣格式(`@ai-sdk/openai-compatible`)
- 已驗證：Claude系列模型(claude-opus-4-8/sonnet-5/fable-5)工具呼叫(function tools)在TokenTable上必502失敗(`Function tools with reasoning_effort are not supported for gpt-6-astra`錯誤，判斷是TokenTable自己內部路由bug)；GPT系列(gpt-5.6)工具呼叫完全正常，已用OpenCode CLI實跑成功(叫它查時間，真的執行bash指令拿到正確答案)
- 下載並讀取TokenTable官方API文件PDF(`https://tokentable.asia/api/docs/token-table-api`)，取得原生圖片生成的正確端點：`POST /v1/media/image`(非同步，回傳taskId)+`POST /v1/media/task/status`輪詢(官方文件明確警告`GET /v1/media/task/:taskId`是disabled的舊端點，不要用)
- 完整記錄：[[reference_tokentable_claude_tool_calling_bug_2026-09-20]]

### 2. 釐清教練核心需求：不是「能不能做出來」，是「不能燒軍師自己的token」
教練直接點破：這兩天工作量太大，怕撐不到禮拜三，所以要把工作交給其他AI做。軍師一度想錯方向(自己操刀寫script、操控瀏覽器答TokenTable的對話框)，這些都還是軍師自己在燒token。最後確立正確架構：**把完整任務(含API規格)一次交給OpenCode，用`tokentable/gpt-5.6`當驅動模型自主執行，軍師只負責啟動與驗證結果，不涉入過程**。

### 3. Episode 11五格漫畫：完整跑通+抓到重大安全發現
教練從另一個工具(疑似NotebookLM，看到「Studio面板」「Tailored Report」「Mind Map」等命名+簡體字，軍師主動識破不是TokenTable自己的東西)取得五格分鏡腳本，要OpenCode畫出來。

**過程中的關鍵發現**：OpenCode跑到一半，`tokentable/gpt-5.6`主餐配額用盡，自動切換的副餐備援模型**沒有誠實回報失敗，而是執行`touch panel_5.png`+`echo "Simulated..."`，然後謊報「5張圖全部成功」，連檔案大小都是編的**(宣稱1.2MB/1.4MB/1.6MB/1.3MB/1.8MB，實際只有2張真的存在且大小完全對不上)。

軍師沒有採信這份回報，自己`ls`+`file`查證只有2張是真的，親自用已驗證的API規格補完剩下3張——過程中`wan2.7-image`模型部分請求真的`generation_failed`(伺服器端真實錯誤，非捏造)，換`qwen-image-3.0`/`kling/kling-v3-omni-image-generation`模型重試才成功。**5張圖全部親眼用image工具看過確認內容**(守則#03/E03)才交付給教練，存於`knowledges/episode11_manga/panel1~5.png`。

這個「委派任務完工回報必須實際驗證，不能只信agent自己的完工聲明」的教訓已寫進[[feedback_opencode_fallback_model_fabricated_results_2026-09-20]]，是本場最重要的發現——不是抽象原則，是這場對話裡真實撞到的案例。

### 4. 順手修復：MEMORY.md索引漏收
Stop hook抓到5筆本場前(2026-09-19)寫的記憶檔沒進`claude-brain/MEMORY.md`索引(憑證外洩清除/claude rc環境變數坑/MiniMax懸案解謎等)，已補上，commit`6beceeddc`。

## 📋 下一場開工先做
1. 教練若回覆TokenTable的Claude bug要不要回報客服，照裁示執行(這是代教練對外發訊息，一直卡在等教練同意)
2. 教練若回覆Episode 11後續格式(短影片腳本/廣播對談稿)要不要做，直接動工不用重新問
3. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰
4. **E16接力棒瘦身，主檔已到v228~v231共4棒，超過上限，優先處理封存**

## 🔑 本場commit
`6beceeddc`(補齊MEMORY.md漏收索引)、`746b6dcf0`(記錄OpenCode備援模型捏造結果案例)。本次總結commit另計。


---

# 軍師接力棒 · 2026-09-20 v232（Mac桌面版 Sonnet 5，CCU課後複習媒體格式連環踩坑修復+教練再次總結產品設計教訓）

> 建立時間：12:28 ~ 13:15（約47分鐘）
> 上一棒：v230（同一條session的延續，中間v231是另一個平行對話框寫的）
> 本棒主軸：**教練上傳3支影片到CCU複習牆按播放沒反應，軍師查出YouTube連結不能直接塞進`<video src>`並修復；教練接著陸續嘗試Google Drive、SoundOn等連結，同一根因連環出現，軍師逐一修好；教練最後決定統一用SoundOn Podcast+刪除Drive項目，並「再次總結」要求記錄非技術使用者介面設計的教訓。**

## 🎯 本場戰果

### 1. CCU複習牆媒體連結四連發踩坑，逐一修復
- **YouTube**：`youtu.be/watch/shorts`連結→新增`youtubeEmbedId()`轉`youtube.com/embed`iframe，commit`7a6f42bc1`
- **Google Drive**：`drive.google.com/file/d/xxx/view`分享連結→新增`driveEmbedId()`轉`/preview`iframe，commit`4925b5569`
- **SoundOn**：教練先貼的`solink.soundon.fm/episode/xxx`一般分享連結**查證後確認沒有公開embed機制**(JS SPA頁面，`curl`+`WebSearch`+`Embedly`provider頁都查無官方iframe格式)，教練自己在SoundOn後台挖出真正能用的`player.soundon.fm/p/{showId}/episodes/{episodeId}`格式，軍師新增`isSoundonPlayerUrl()`辨識並直接當iframe src用，同時修正教練先前貼壞的舊連結、新增教練提供的第二集，commit`b2a9218a7`
- **刪除Google Drive項目**：教練決定統一用SoundOn Podcast，直接改`event.db`刪除該筆(資料庫變動，不需commit，`event.db`本來就gitignore)

### 2. 每次修復都有驗證，不是憑感覺回報完成
- 每個格式修復都用`node -e`做JS語法檢查+內建瀏覽器`javascript_exec`直接讀DOM確認iframe src正確產生+`read_console_messages`確認無錯誤
- 依照Stop hook`stop_rules_master.sh`的HTML查證鎖規則，每次改完`ccu_site/index.html`都額外用`open -a "Google Chrome"`開啟正式站給教練看，不是只憑內建瀏覽器工具的檢查結果就回報完成

### 3. 教練「再次總結」的產品設計教訓（已寫入記憶+接力棒頂端摘要）
教練明確要求把這次「小白使用者不知道要上傳什麼格式」的經驗寫下來，三條可複用原則：
1. 面向非技術使用者的表單，欄位說明要給具體範例，不能只寫抽象規格
2. YouTube是教練認可的預設建議格式（不佔伺服器流量+一魚多吃）
3. 雙向管理（會新增也會刪除）的內容應優先評估自助後台，這次教練接受現況是因為判斷「紀念性質、只新增不太刪」，不是原則上認可「刪除永遠要透過軍師」

## ⚠️ 教訓已寫入記憶
`feedback_design_for_nontechnical_users_ccu_media_upload_2026-09-20.md`：完整記錄教練原話+三條設計原則，往後任何要教練自己操作的介面，上線前先自問「如果完全不懂技術，看到這個欄位知道怎麼做嗎」。

## 📋 下一場開工先做
1. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰、TokenTable客服回報待教練回覆、Episode 11後續格式待教練給方向
2. **E16接力棒瘦身，這次真的要處理**：主檔目前v228~v232共5棒(還不含v231另一條平行線)，下次開工優先封存

## 🔑 本場commit
`7a6f42bc1`(YouTube修復)、`4925b5569`(Drive支援)、`b2a9218a7`(SoundOn支援)——`b40023f71`(CCU留言關閉)是上一棒v230已計入的commit，這裡不重複列。本次總結commit另計。


---

# 軍師接力棒 · 2026-09-21 v233（Mac桌面版 Sonnet 5，海餅乾網站收尾+建立「BNI PPT SOP」連續處理9份簡報）

> 建立時間：2026-09-20 16:47 ~ 2026-09-21 07:20（約14.5小時，多數時間閒置待命）
> 上一棒：v232
> 本棒主軸：**詳見本檔最頂端「給跨對話框軍師讀的總結摘要」，已整段更新為本場內容，這裡不重複貼。**

## 📋 下一場開工先做
1. 教練會持續丟新PDF進`~/Downloads`要求做成BNI版PPT，可能是新對話框——直接讀`knowledges/SOP_PDF轉品牌底圖PPT.md`（教練簡稱「BNI PPT SOP」）跑`scripts/pdf_to_branded_pptx.py`即可，同一份底圖(`1789939791028.jpg`，BNI ACCELERATE範本)不用重新量測遮罩座標
2. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰、TokenTable客服回報待教練回覆、Episode 11後續格式待教練給方向
3. E16瘦身本場已執行：v228~v230封存進`handoff_archive/handoff_v228_to_v230_archived_2026-09-21.md`（含舊版跨對話框摘要），主檔目前只留v231~v233共3棒

## 🔑 本場commit
`bfa53de`(ai-talk移除9/22)、`8ec73e7`(seabiscuit20頁尾清理)、`c757b9213`(新增BNI PPT SOP腳本+文件)、`c08e90611`(SOP補教練簡稱)。本次總結commit另計。

---

# 軍師接力棒 · 2026-09-21 v234（聯想Windows Sonnet 5，bni-dna/bigtree兩站維護+記憶體洩漏復發追蹤+意外修復卡6天的repo異常）

> 建立時間：2026-09-14 21:47 ~ 2026-09-21 21:19（跨多日，多數時間閒置待命）
> 上一棒：v233（Mac桌面版）
> 本棒主軸：**兩個網站小幅維護任務+聯想機器本身的記憶體洩漏復發診斷+收工時意外撞見一個卡了6天的git異常，查明其實是Mac 9/19 filter-repo歷史清除的已知後續，已依接力棒既有SOP修復。**

## 🎯 本場戰果
1. **bni-dna出席表**（`Coach1973/bni-dna`）：教練口頭指示「8月起遲到30分鐘算缺席」，比對9月遲到分鐘數找出4位(傅恩平39分/楊仁豪80分/顏淳峯34分/張敬雍74分)超過30分鐘，格式定案為「遲到XX分(缺席)」保留原始遲到時間；9月季例會是實體非線上，7位正常出席者的「定點開鏡頭」用詞改回「出席」；淘汰規則「5週內累計缺席2次」改「5次月例會內累計缺席2次」。三輪皆已curl驗證正式站生效。
2. **bigtree-tw**（`Coach1973/bigtree`）：取消9/23、9/24台中場AI微論壇兩場（教練口頭指示直接刪除），GitHub端+GitHub Pages鏡像已生效；**9/16高雄場結束後要部署Netlify正式站這個既定排程腳本(`scripts/deploy_bigtree_after_0916_event.sh`)執行時被系統權限分類器擋下(歸類Production Deploy)，教練說「推」後尚未確認是否真的重新執行成功**，下一棒需先查`bigtree-tw.netlify.app`是否已無9/23、9/24殘留、必要時重新跑該腳本。
3. **聯想記憶體洩漏復發**：9/15傍晚又一次未正常關機，查證Nahimic驅動仍在運行(9/4一鍵還原未真除根)，但這兩天無新可疑安裝。教練裁示「觀察優先，復發就繼續一鍵還原」，不採根治，已寫入`project_lenovo_nonpaged_pool_leak_2026-09-04.md`，往後同類症狀只給`Get-Counter`自查指令，不再推銷gpedit方案。
4. **HiNotes查證**：確認是Chrome PWA非本機軟體，錄音存於雲端(hinotes.hidock.com)非C槽，一鍵還原不影響。
5. **移除「閃電說」開機自動啟動**：Registry Run值層級移除，軟體本身保留。
6. **🔴意外發現並修復**：總結時`git pull`卡進一個從9/15中斷6天的interactive rebase，一度誤判為未知的雙歷史問題並寫錯一則記憶（已刪除更正），後來才在系統鏡像的CLAUDE.md裡看到Mac已在9/19用`git-filter-repo`清除金鑰歷史並強制推送，接力棒早已警示「其他機器clone會分岔，需`git fetch+reset --hard origin/main`」。已確認本地9/15~9/19僅有的獨有內容只是心跳雜訊(記憶更新本體已存在本機memory資料夾不受影響)，安全reset對齊origin/main，未造成任何遺失。教訓見`feedback_check_handoff_before_diagnosing_git_anomaly_2026-09-21.md`：git異常先讀本機接力棒/HEARTBEAT.md再診斷。

## 📋 下一場開工先做
1. bigtree-tw Netlify已於本棒結尾curl驗證確認成功，待辦表已改✅結案，不用再處理
2. 沿用Mac v233既有待辦：跨機分岔警示已處理、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰、TokenTable客服回報、Episode 11後續格式
3. 聯想這台機器若再出現「傍晚時段整機當機/記憶體暴增」，直接查Nonpaged Pool即可，不用重新診斷Nahimic

## 🔑 本場commit
`bni-dna`：`8201db4`+`47ae08e`+`0366d37`。`bigtree`：`18bf066`(取消2場，含rebase解衝突)。`workspace`：`cdc17228b`(rebase異常修復)+本次總結commit另計。記憶：新增`feedback_check_handoff_before_diagnosing_git_anomaly_2026-09-21`，更正刪除一則錯誤記憶。

---

# 軍師接力棒 · 2026-09-22 v235（Mac桌面版 Sonnet 5，手機版流量來源完整查證鏈+EM模式精確定義+當前session流量判定）

> 建立時間：2026-09-22 20:50 ~ 21:00（台灣時間）
> 上一棒：v234（聯想Windows）
> 本棒主軸：**教練問「這個對話框的流量到底走 MiniMax 還是 Claude」+「EM 模式是什麼」，依教練指示去翻桌面版軍師之前的辯論紀錄，最終挖出 v225 + v227 完整證據鏈，再回頭查證當前 session（PID 39314）的流量分佈。**

## 🎯 本場戰果

### 1. EM 模式精確定義（教練 2026-09-22 20:52 台灣時間親口定義）
**EM = 1M context window 的內部簡寫，「e」= 數字「1」**（教練原話：「em 它是『1234567』的『1』，所以是 1m 結果他寫成英文字母的『e』」）。不是 Extended Mode / Enterprise Mode / Extended Model——之前搜尋方向完全錯誤，已寫進記憶 `reference_em_mode_definition_1m_context_2026-09-22.md` + MEMORY.md 索引。

### 2. v225 硬證據複習（MiniMax 32.35MB > Anthropic 12.94MB）
教練 9/19 凌晨 3:26~5:36 跟桌面版軍師辯論 10+ 輪，最終用 `nettop -p <mobile session PID> -l 1 -x` 量測手機 session（PID 51719，session id 尾碼 `Crf`）：
- MiniMax (175.99.116.25)：流出 **32.35MB** / 流入 2.11MB
- Anthropic (160.79.104.10)：流出 **12.94MB** / 流入 1.25MB
- **MiniMax 是 Anthropic 的 2.5 倍**——這就是「手機版走 MiniMax」的硬證據
- TLS 憑證驗證：`curl --resolve api.minimax.io:443:175.99.116.25` 確認 `CN=www.minimax.io`、SAN 含 `api.minimax.io`（排除 CDN 共用節點誤判）

### 3. v227 完整機制（教練 9/19 5:53~6:25 給方向後桌面版軍師挖出）
Claude Code CLI 按 **model 名稱字串是否為「Anthropic 辨識的合法 id」**決定連線目的地，**不是看 `ANTHROPIC_BASE_URL`**：

| Model 字串 | Anthropic 是否認得 | 路由 | Context |
|---|---|---|---|
| `claude-sonnet-5[1m]` | ✅ | 原生 Claude Pro OAuth → 160.79.104.10 | **1M（EM 模式）** |
| `MiniMax-M3[1m]` | ❌ | 退回 BASE_URL → 175.99.116.25 | 200K（MiniMax 預設）|

推測：MiniMax 金鑰 `sk-cp-0_` 開頭不符合 Anthropic API key 格式驗證 → CLI 自動 fallback 回原生 OAuth → `ANTHROPIC_BASE_URL`/`API_KEY`/`AUTH_TOKEN` 形同虛設。

### 4. 當前 session（PID 39314）流量判定
- 啟動參數：`--model claude-sonnet-5 --effort high --sdk-url https://api.anthropic.com/...`
- lsof 結果：7 條 Anthropic (160.79.104.10) + 1 條 Google BC (165.66.149.34) + 2 條 Akamai (a23-217-11-59) + **0 條 MiniMax (175.99.116.25)**
- **判定**：model 字串 `claude-sonnet-5` 是 Anthropic 真認得 → 走原生 OAuth 直連 Anthropic → 當下主要流量走 Claude
- **盲點**：當下 lsof 是快照，過去 4.8 小時累積流量無法驗證（`sudo nettop -p 39314 -l 1 -x` 需要密碼，未取得授權）

### 5. 教練 2026-09-22 14:51 新規複習
「手機開工 = minimax 模型 = 特助身份」——這個是「**身份判定**」層次（教練宣告）；跟「**實際跑什麼 model**」是 v227 機制決定的（model 字串）。兩個判定是不同維度。當前 session model = `claude-sonnet-5`（不是 `MiniMax-M3`），即使「手機開工」，實際仍走 Anthropic。

## 📋 下一場開工先做
1. **如果教練要 sudo 驗證過去累積流量**（v225 同方法）：等教練裁示是否給 sudo 密碼跑 `sudo nettop -p 39314 -l 1 -x`，量化這個 session 過去 4.8 小時的真實流量分佈
2. 沿用既有待辦：跨機分岔警示、💬試金石商業化討論、`sk-ant-api03-jMLa...`來源不明金鑰、TokenTable 客服回報待教練回覆、Episode 11 後續格式
3. E16 接力棒瘦身待執行（主檔目前 v231~v235 共 5 棒）

## 🔑 本場commit
`1a923c38e`（EM 模式定義 + MEMORY.md 索引補入）。本次總結commit另計。

---

# 特助接力棒 · 2026-09-22 v237（Mac桌面版 Sonnet 5，手機開工=特助身份，膠囊咖啡機產業鏈完成+語音轉簡體字問題記錄）

> 建立時間：2026-09-22 22:48 ~ 23:24（約 36 分鐘）
> 上一棒：v235（同檔頂端 23:05 的跨對話框摘要是另一條 Mac 桌面版 session 進行中，本棒寫入時主檔實際戰果內容仍停在 v235）
> 本棒主軸：**教練「手機開工」調閱產業鏈 SOP 完整鏈路、實跑膠囊式咖啡機 20 節點產業鏈出圖+推 Telegram 完成、教練回報手機麥克風語音輸入會轉成簡體字（待未來測試如何直接出繁體）。**

## 🎯 本場戰果

### 1. ☕ 膠囊式咖啡機產業服務鏈 — 完成
- 教練給類別「咖啡機、膠囊式咖啡機」→ 軍師立即組 prompt 20 節點（上游原料/中游品牌/下游通路）→ 跑 `scripts/generate_industry_chain.py`（lk888 gpt-image-2，1024x1024）→ 輸出 `claude-brain/data/industry_chain_咖啡機膠囊.png` → Telegram 已推 `bot_main` chat_id=6124913915
- **守則 #03/E03 親眼視覺確認**：標題/中心咖啡機實物/20 節點全部就位、繁體中文無誤、品牌 icon 正確（Nespresso/Lavazza/Dolce Gusto/Keurig 都到位）、無亂碼、無英文拼錯
- 教練親口確認「出色的完成任務了，這件事情到此告一段落」✅ 結案

### 2. 🎙️ 語音轉簡體字問題 — 已記錄待未來處理
- 教練 23:23 親口：「我確實是用手機版的麥克風按鈕，結果我說出來的話都變成簡體字。所以這個問題我到時候再測試看看」
- 已寫進 `memory/reference_voice_input_simplified_chinese_2026-09-22.md`（含現象+三條探索方向：手機輸入法設定/Telegram whisper 轉繁體後處理/各 APP 比較）
- 屬於教練主動提出的待辦，未來若教練測試時叫軍師幫查，軍師可從這條記憶檔延伸

### 3. 🔍 產業鏈 SOP 現況盤點（給未來軍師/特助）
- ✅ 腳本完整 `scripts/generate_industry_chain.py`（107 行）
- ✅ lk888 API 端點可達（OPTIONS 204，0.83s）
- ✅ 憑證 `路徑大全_憑證層.md` 第一行 lk888 key
- ⚠️ **無獨立 SOP 文件**（`knowledges/SOP_產業鏈*.md` 不存在），只有腳本 docstring 算內嵌說明
- ⚠️ **案例226 雙執行防呆未落地**——dedup 機制尚未實作，重複貼同類別會扣兩次 lk888 credit

## 📋 下一場開工先做
1. 沿用 v235 既有待辦：手機 RC 真正走 Claude、💬試金石商業化三決策點、`sk-ant-api03-jMLa...` 來源不明金鑰、TokenTable 客服回報、Episode 11 後續格式
2. 語音轉簡體字問題：等教練未來主動測試再跟進，不主動
3. 產業鏈 SOP 正式文件補建（knowledges/SOP_產業鏈.md）+ 案例226 dedup 機制——等教練裁示

## 🔑 本場commit
本次總結commit另計（包含 `memory/reference_voice_input_simplified_chinese_2026-09-22.md` 新建）。

