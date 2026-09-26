# 封存：v248~v250（2026-09-27 N9瘦身）

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-26 15:55，Mac終端機 Sonnet 5，新的一棒 v250）

**本場主軸：赫米斯鑫瀚昌旅行社上架卡住的表面bug，一路被教練追問揪出系統性根因，最後演變成拆除shops.bymyway.com的VPS依賴、全面遷移到Mac本機處理；過程中自己抓到自己種下的bug並修好；另外插一段小龍蝦LK888額度浪費事故的技術審查。**

### 1. 鑫瀚昌旅行社上架卡關→查證後發現是設計已知行為（custom_slug被既有暫代頁覆蓋規則略過）
赫米斯curl上傳200後猜`/curated/hsinhan/`猜4次都404，其實6秒就處理完成，只是命中`shops.bymyway.com`既有暫代頁、custom_slug被2026-09-06舊規則略過，真正網址是拼音自動轉的`shops.bymyway.com/xin-han-chang-lv-xing-she/`。回信說明+驗證後，教練追問「為什麼保證『分得清楚』卻連續出包」，逼出根因：**執行的AI完全沒有機器可查的真相來源，只能靠猜網址自我驗證**。新增`scripts/curation_check_result.py`（一行查真相：成功/失敗/處理中+真實網址+存活狀態），改寫`SOUL.md`/赫米斯`AGENTS.md`/兩份SOP文件禁止再猜。

### 2. 教練要求「教練指定的網址必須生效」，新增custom_slug覆蓋既有slug的改名機制
新增`rename_shop_slug()`：custom_slug跟既有slug不同時，自動改VPS目錄名+`_shops_slugs.json`+策展中心卡片連結，手動把鑫瀚昌修正到`shops.bymyway.com/hsinhan/`（實測200），寫入試金石案例84。

### 3. 🔴 教練追問「為什麼扯上VPS」，查出shops.bymyway.com實體架在跟「VPS小龍蝦」同一台主機（43.245.60.200）
教練評估後給三條判斷框架（改動成本/不改代價/改了好處），額度不夠切Opus、授權直接在Sonnet上做完整件事：查證VPS沒有真的提供獨立於Mac之外的可用性（`event.bymyway.com`本身就跑在Mac的Cloudflare Tunnel上）→3家真實店家(huitou/ema/鑫瀚昌)全部遷移到本機`github_repos/<slug>/`，複用`/curated/`同一套serving機制，`app.py`新增host分流路由，Cloudflare DNS從A記錄改CNAME指向同一個tunnel，`curation_process.py`/`app.py`移除所有sshpass/VPS程式碼，端到端curl測試通過（含圖片Content-Type）。

### 4. 🔴 自己測試時抓到自己种下的bug：改名機制讓系統「忘記」店家已存在
真實重傳測試發現：改名後`_shops_slugs.json`的拼音key跟着slug一起被換掉，導致下次同店家上傳被誤判成全新店家，重複建了`hsinhan-2`。查出根因（品牌識別key不該跟著網址一起變）、改成`{品牌拼音key: 目前生效slug}`字典格式，清乾淨重複產出（本機目錄搬進`.trash`、tainan-shangquan重複卡片、registry重複條目；GitHub孤兒repo`hsinhan-2`因token無`delete_repo`權限留著但無害無連結），重新測試確認正確。

### 5. 插播：小龍蝦LK888額度浪費事故（28張需求出96張）——我的初步審查不夠嚴謹，被平行的軍師session用真實紀錄糾正
小龍蝦(Mac mini/OpenClaw/MiniMax)寫信通報，自己在`generate_teamwork_manga_v5_anime_mature.py`加了mtime鎖，我審查後只確認「擋點在付費API呼叫前、邏輯正確」就回報可信任——**但沒有拿真實時間間隔資料驗證**。教練同時段人在外用手機（Sonnet）先行處理，查小龍蝦對話資料庫發現：實際重跑次數是21次/15次（不是小龍蝦自報的17/13），而且重跑間隔常常超過60秒（例如84秒），我核可的那道60秒鎖根本擋不住。手機那邊做出真正完整的解法：`scripts/lk888_guard.py`收費閘門（24小時同圖只付一次+5分鐘內不准連續+一天上限+一小時煞車，8支出圖腳本全接上）＋小龍蝦端跟軍師端各一道安全鎖（含防止小龍蝦再次整份覆寫試金石檔案）。過程中小龍蝦自己還把試金石案例庫從3906行寫壞成109行(案例1~84全消失)，已用git`5edab188e`救回。**教訓寫進試金石案例85第2點：「AI的自我檢討要用原始紀錄驗證後才能採信，包括另一個軍師的結論」——這條也是在說我。**

### 6. 教練指名寫信給Opus，交接VPS遷移完整決策過程——Opus審議抓到我留下的一個真實安全漏洞
放進`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`。Opus 5.5審議後回覆（同一份檔案第八節）：**我新增的`shops_local_page()`/`shops_local_assets()`只檢查「資料夾存在」，等於把`/Users/bymyway/github_repos/`底下80多個資料夾全部掛在shops.bymyway.com公開，實測連來賓名單資料庫(`zhenxin_guests.db`)、schema、log都能被外部下載200**——我當時只測「該通的路徑通不通」，沒測「不該通的路徑會不會被誤放行」。已修：白名單只開放`_shops_slugs.json`登記店家＋`_serve_repo_file()`對敏感副檔名(.db/.log/.sql/.env等)一律404，兩層防禦。另外Opus也糾正我信裡一個事實錯誤：我說「kr這個slug已經死了」——其實Mac檔案系統不分大小寫，`github_repos/KR/`(另一家真實店KR養生廚房)讓`shops.bymyway.com/kr/`一直是活的，我沒注意到大小寫問題。commit`56da56292`。

### 📋 下一場開工先做
沒有教練待決定的事。VPS上舊檔案沒刪(當備援)、孤兒GitHub repo `hsinhan-2`無害擱置，都列進AI自己的工作清單，不用主動提。小龍蝦LK888事故的p14~28續跑與否，教練會直接跟小龍蝦說，軍師這邊不用追問。**本場最大的教訓：兩件事我都做完「看起來對」的驗證就回報過關，實際上一件缺了真實資料比對、一件缺了負向測試（測不該看到的東西），都是被別的session事後抓到——下次交付前要主動想「我漏測了哪個方向」，不能只驗證自己預設的那條路徑。**

### 🔑 本場commit
workspace：`3e83a3ee1` `62b4206b4` `5edab188e` `67418df3f` `611139f75` `b4d5d1684` `2934338bd` `4e734672c` `118daf9d7` `b1677dc05` `d65e25aa6` `53d3e50da` `56da56292`；外層`~/.openclaw`：`2a8594141`；tainan-shangquan：3筆改名/清理commit。本次總結commit另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-26 00:23，Mac桌面版，新的一棒 v249）

**本場主軸：教練發現「軍師調整完之後，小龍蝦說好卻不動、赫米斯上架失敗」，追查發現是軍師自己的自動化在拖垮小龍蝦；後續教練連續兩次查證測試（別名清單漏字、要我交代原話出處），逼出「死背字串」這個方法論本身的錯誤，改成概念判斷。**

### 1. 修好兩個開工hook的小bug（前段）
①`feed_junshi_handoff.sh`身分判斷式用OR，桌面版App因為走OAuth沒有`ANTHROPIC_API_KEY`被誤判成手機，導致跳過第4步(knowledges)、身分報錯成特助——改用AND（兩個變數都清空才算手機），實測驗證。②`render_public_system_prompt.py`：外帶版`system-prompt.md`(21條+N1~N9)改成從`特助心法.md`/`執行細則.md`自動產生不再手動維護，同時發現`publish_public_status.sh`本身`git add`漏了`.md`來源檔，第一次「修好」其實沒真的推上去，補上重推並用GitHub blob API逐字驗證。commit `1cfb71cd9`、`ed0466675`、ai-go`38819c1`。

### 2. 🔴 赫米斯上架「大樹作品」卡住，真因是後端bug不是它不懂SOP
`curation_process.py`要求解壓後一定要有檔名剛好叫`index.html`的檔案，但教練這次的包是「教練照片命名的html+14張jpg」，沒有index.html，背景程式默默失敗，赫米斯的curl回200看起來成功、實際上没上架。修法：只有一個html檔就自動複製當index.html，用教練真實檔案在正式環境測試成功(`c-challenge`)。過程中我自己測試+赫米斯重試共產生3個重複上架，已清乾淨（event後台+coach888伺服器狀態+coach888 git三處都同步，commit`430a881`）。

### 3. 🔴 跨機指令鎖被教練糾正：回覆對方主動來信不該再問
我回信赫米斯前先問教練「可以發嗎」，教練：「你本來就應該回信給赫米斯，幹嘛還要問過我？」——`cross_machine_dispatch_guard.sh`原本不分方向，07-02原始案例是軍師「主動」發號施令、這次是「回覆」對方主動求助的來信，性質不同。已修：鎖會檢查`inbox/mac/`有沒有一封`{對方}-to-mac`格式待處理來信，有就直接放行；沒有(=軍師主動發起)才維持要教練拍板。dry-run驗證兩種情況都對。commit`fbdc00ace`（此commit同時含赫米斯回信+index.html bug修復）。

### 4. 🔴🔴 深度根因分析：為什麼小龍蝦說好卻不動、赫米斯上架又失敗（Opus 5.5）
教練質問「調整完表現還不如調整前」，查小龍蝦對話資料庫（不是猜的）：
①**心跳bug復活**：9/14用`system heartbeat disable`關過，但那只存在記憶體，9/22 23:20 gateway重開後心跳復活，每30分鐘插進教練Telegram主對話（一天70~110次），帶「不要接續舊任務/回NO_REPLY」指令。9/17記憶檔早記下這個坑卻沒人改永久設定。**已改`openclaw.json`寫`heartbeat.every=0m`，cron list實測系統排程1筆→0筆**，並更新舊記憶檔補上正確方法。
②**軍師自己的日誌灌爆小龍蝦開機必讀檔**：`HEARTBEAT.md`78%(155/167段)是軍師hook自動寫入的日誌，撐到25,769字超過OpenClaw每檔2萬字上限被截斷、寫出亂碼。5支程式(含2支Windows .ps1)全改寫`state/junshi_automation.log`，實跑確認HEARTBEAT.md md5不變；檔案瘦到4,422字，搬走內容+原檔都封存在`handoff_archive/`。
③生圖技能觸發詞沒有「分鏡」，小龍蝦自己另寫不帶照片的腳本，臉不像教練——技能踩雷表早寫著這個坑，已補觸發詞+明令用現成腳本。
④赫米斯自己的`AGENTS.md`從沒收到09-24「大樹創作SOP」別名補丁（只補進小龍蝦那份），已補上。
試金石案例83；commit：workspace`25f2c861e`、外層`openclaw.json``8f5f9a45e`、赫米斯`aecc0e1`。

### 5. 🔴🔴 教練連續測出「死背別名清單」這個方法本身是錯的
教練問「大樹作品上架SOP不是正確指令，那正確指令是哪個」——grep查證：這6個字在我剛寫的3份清單裡0命中。**體悟：清單永遠列不完，教練永遠可以換講法**，改成三處都寫「判斷概念（大樹+作品/創作+上架/上傳/SOP的任意組合），不是死背字串」。commit`4c57cfe92`、`de4a491`。
教練接著問「我當時到底怎麼講的，是『個人創作SOP』嗎」——查小龍蝦對話資料庫找到教練三段原話：9/23「這個不是策展的店家網站」、「走大樹創作的SOP」、9/24當場糾正「你走的不是策展中心的SOP，你走的是大樹教練作品的SOP」。**「個人創作SOP」是AI自己取的檔案標籤，教練沒講過**，已在SOP文件補上這段查證與教練原話，避免以後被誤當教練原話引用。commit`60f8d9a21`。

### 6. 待回答：CoWork分頁去哪了
教練問Claude桌面版App的「CoWork」分頁現在變成「Chat & CoWork」，以及現在的工作算Code還是CoWork。**誠實回報做不到**：試著用computer-use截圖被系統擋下（不能操作/截圖自己所在的App本身，是寫死的安全限制），無法親眼查證。已請教練直接截圖或描述畫面，答案未完成，下一棒若教練提供畫面請接續回答。

### 📋 下一場開工先做
沒有教練待決定的事（三關都沒過）。CoWork問題等教練提供畫面才能回答，不用主動問。20張分鏡圖批次停在第2張（第3張被教練叫停，因為人不像教練），已用帶照片的舊方法修好根因，但**沒有教練明確說「繼續」之前不要自己重啟**，這批20張教練自己會再交代。MEMORY.md也超過2萬字上限且有1處亂碼（跟HEARTBEAT.md同一類問題，只是還沒瘦身），列進下面AI工作清單自己找時間處理。

### 🔑 本場commit
workspace：`1cfb71cd9` `ed0466675` `fbdc00ace` `25f2c861e` `4c57cfe92` `60f8d9a21`；外層`~/.openclaw`：`8f5f9a45e`；ai-go：`38819c1`；coach888：`430a881`；赫米斯：`aecc0e1` `de4a491`。本次總結commit另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-25 14:16，Mac桌面版，新的一棒 v248）

**本場主軸：建立公開交接棒「隨身軍師」解決教練Claude Opus每週額度不夠的問題，過程中教練連續問了三個精準問題，抓出兩個我自己沒查全的技術漏洞，逐一修好。**

### 1. 公開交接棒「隨身軍師・一鍵接手」上線：https://coach1973.github.io/ai-go/status.html
目的：教練Opus週額度兩天燒掉56%，週末會斷炊，想把思考型問題分流到其他網頁版AI。做法：`ai-go/status.md`當唯一手改來源，每次教練說「總結」自動改寫+發布。教練直接拿去實測，牽出下面兩個真問題。

### 2. 🔴 真因查證：GitHub Pages對.md回傳text/markdown，多數AI讀不到
教練回報其他AI說「被屏蔽」。curl實測(不是猜)：五種AI爬蟲UA全部200無阻擋，不是robots/WAF；真因是`.md`檔content-type是`text/markdown`，`.html`是`text/html`，多數AI內建讀網頁工具只認後者。建`scripts/render_public_status_html.py`(python-markdown)自動轉換，`.md`仍是唯一來源不分岔。已記進記憶`reference_github_pages_md_content_type_ai_compat_2026-09-25.md`。

### 3. 🔴 教練追問揪出第二個漏洞：頁面裡引用的另外兩份文件沒有一起修
`status.html`內文引用`coach-persona.md`/`system-prompt.md`，這兩份本身也是同一個content-type問題，我只修了入口沒查全部。已比照建`coach-persona.html`/`system-prompt.html`，三份都納入發布腳本自動轉出，`index.html`「查看全文」連結也改指向`.html`。**教訓：修好一個技術問題時，要順手檢查同一頁面引用出去的其他資源是不是同一個病，不能只治入口。**

### 4. 誠實澄清「總結」自動更新的邊界
教練問「其他網頁版AI有能力寫入.md嗎」——如實回答：沒有。這套自動化是Claude Code系統本身的hook功能，只在教練跟軍師（這台Mac / 雲端工作頁）對話時生效；ChatGPT/Gemini/Grok等網頁版完全碰不到這台電腦的檔案系統，沒有寫入能力，只能讀。

### 5. 順便修好的小事
①修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」(教練親口訂正，5個檔案)，同時補記到`user_coach_brand_data.md`避免第三次犯②`publish_public_status.sh`驗證迴圈：GitHub Pages CDN偶爾超過5分鐘才生效，push成功卻被誤判失敗(發生2次)，改成push成功就算數，CDN慢只如實回報不當失敗③外層`~/.openclaw`repo的git分岔查證後確認安全並合併推送(`f517ec524`)，雲端工作頁(claude.ai/code)現在能吃到跟Mac一致的全套規則，main/master兩分支都實測過④已收進coach888工具類第一項。

### 📋 下一場開工先做
沒有待教練決定的事。公開交接棒機制已上線，教練以後說「總結」會自動維護，不用主動提。

### 🔑 本場commit
workspace：`445210e92` `8f953cd14` `5ea38190d` `9543c6ec6` `614db2def`；ai-go：`39b84c7` `22bbe94` `5114dc3` `3f4273e`；coach888：`79a7d81` `03021cb`；外層`~/.openclaw`repo：`f517ec524`(merge)。本次總結commit另計。

