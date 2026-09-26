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

### 5. 插播：小龍蝦LK888額度浪費事故（28張需求出96張），審查其自建防呆機制
小龍蝦(Mac mini/OpenClaw/MiniMax)寫信通報，已自己在`generate_teamwork_manga_v5_anime_mature.py`加上mtime鎖+執行歷史記錄。審查確認擋點在付費API呼叫之前、邏輯正確，回覆其三個問題（軍師端hook做不到跨進程攔截、腳本內建防呆才是對architecture、p14~28要不要繼續是教練的決定不是AI該選），寫進試金石同一案例＋cross-agent信件。

### 6. 教練指名寫信給Opus，交接VPS遷移完整決策過程
放進`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`，含教練給的三條判斷框架、查證過程、技術細節、自己抓到的bug，下次Opus開工六步驟第4步會自動讀到。

### 📋 下一場開工先做
沒有教練待決定的事。VPS上舊檔案沒刪(當備援)、孤兒GitHub repo `hsinhan-2`無害擱置，都列進AI自己的工作清單，不用主動提。小龍蝦LK888事故的p14~28續跑與否，教練會直接跟小龍蝦說，軍師這邊不用追問。

### 🔑 本場commit
workspace：`3e83a3ee1` `62b4206b4` `5edab188e` `67418df3f` `611139f75` `b4d5d1684` `2934338bd` `4e734672c`；tainan-shangquan：3筆改名/清理commit。本次總結commit另計。

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

---

> 📦 v247完整內容已封存：`handoff_archive/handoff_v247_archived_2026-09-26.md`（v247：赫米斯登入自動跳出根因修復+副螢幕防呆+模型分工v2上線+雲端方案分岔陷阱查證）

> 📦 v246完整內容已封存：`handoff_archive/handoff_v246_archived_2026-09-25.md`（v246：執行細則16條E併9條N規則上線+VPS/LINE/大台南小幫手每位朋友單獨記憶查證+龍蝦小助教記憶檔被巡檢指令灌爆bug修復）

---

> 📦 v245完整內容已封存：`handoff_archive/handoff_v245_archived_2026-09-25.md`（v245：VPS/LINE健檢推播404修復+五項修法落地+小龍蝦2.0評估+版本變動通知）

> 📦 v244完整內容已封存：`handoff_archive/handoff_v244_archived_2026-09-25.md`（v244：大樹創作SOP口語別名缺失修復+coach888插入bug修復+coach888分類重組+MEMORY.md清理）


> 📦 v242~v243完整內容已封存：`handoff_archive/handoff_v242_to_v243_archived_2026-09-24.md`（v242產業鏈SOP誤報700+分類資料庫查證+名片系統去識別化技術文件雙版本交付／v243 MEMORY.md索引159筆清零+namecard-db前會員/來賓資訊改造+cloudflared版本過舊發現解決，E16瘦身2026-09-24執行）
> 📦 v238~v241完整內容已封存：`handoff_archive/handoff_v238_to_v241_archived_2026-09-24.md`（含全面體檢/agents人設檔救回/llama-cpp修復/聚寶盆發票/ezPay作廢SOP等v238~v241全紀錄）

---

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
（目前沒有）

### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- VPS升級LTS 2026.7.35（教練09-24：10/1左右月報會自動提醒，時間到再說）
- 367位前會員推薦人補查（BNI Connect帳密沒存在路徑大全，要教練本人登入一次；09-24已問過一次）
- 柯朝陽發票（教練09-24：延後約一年，不用管）
- 試金石商業化計畫書（教練09-24：還沒想到怎麼商品化，暫時不用管）
- 小二(test2)/OpenClaw 2.0評估（暫停，等官方修復）
- 小二Telegram輪詢異常（教練09-21：等小二成熟再處理）
- 聯想C碟WinSxS再瘦身4~5GB（要不要做，教練沒回）
- bni-chapters真誠分會網頁架構問題（教練還沒說明是哪個問題）
- 「教練都在想什麼」補更多素材（等教練提供）
- 其他LINE帳號比照搬遷（等教練指定帳號，SOP已備妥）
- 小龍蝦後台看不到中文名（教練裁示：看到陌生ID問了再回）
- coach888拖拉排序好不好用（等教練回饋）
- 「全世界最優秀的團隊計畫」報名連結（等教練給網址）
- 企業健身房正式建站（等教練交辦）
- 企業健身房4項文案修改（等教練交辦下一步）
- BNI小幫手實戰體驗（等教練親測）
- Coze舊機器人何時停用（等教練裁示）
- ACER 36.3GB備份刪除（需教練在ACER親自開對話）
- 赫米斯Telegram線登出登入時斷約2分鐘（綁使用者登入，要改成開機常駐系統服務才能根治；09-25已告知一次，教練沒要求處理）

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟡 | **團隊協作全面體檢（2026-09-24 Opus 5.5）：五項修法教練13:37說「執行」，已落地** | ⚠️持續追蹤-首次真實使用待觀察 | 完整報告`knowledges/2026-09-24_團隊協作全面體檢報告.md`。①每日08:10全隊點名`scripts/daily_team_rollcall.py`+launchd`ai.openclaw.daily-rollcall`(13:41實跑送達)；VPS/LINE健檢改為只在異常時通知②VPS看守Mac：VPS`/root/watch_mac.sh`每30分，Mac連續兩次連不上才通知(測試訊息message_id 3860送達)③上傳頁`kind`必填，`creation`全自動進coach888最新作品——**09-25首次真實作品實測，發現index.html判斷bug已修復**（個人創作常沒有index.html慣例檔名，改成剩一個html檔就自動採用，見v249），真實上架成功④產業鏈同主題同對話10分鐘防重複⑤VPS健檢拿掉1小時無活動誤報；赫米斯記憶檔金鑰是教練指示保留的寫法，不搬。commit`b076a80fc`+`777c9c7c4`。**VPS升級另見下一列**。VPS健檢缺天原因仍未查明，改由每日點名檢查「今天有沒有跑」。 |
| 🟡 | **雲端工作頁規則同步（2026-09-25 Opus 5.5，教練原則：同一套規則本機雲端一體適用，只有動到Mac本機的事例外）** | ✅已上線，兩條路實測通過 | 機制與SOP見記憶`reference_move_to_cloud_this_repo_2026-09-25.md`：`cloud_sync/`(全域規則+11技能副本，每則回覆結束自動更新)+`workspace/.claude/settings.json`(main)+外層`.claude/settings.json`+`cloud_bootstrap.sh`(master)。commit`1e0bea3ab`+`2db3d1330`(workspace)、`a0975a949`(外層)。**待修小bug**：`model_tier_advisor.sh`剛用/model切換後的第一則仍顯示舊模型(09-25切Opus後仍報sonnet-5)，雲端第一則顯示「未知模型」。外層master分岔已查證安全並合併推送`f517ec524`，v247「791d775d2未push」一句已過時。 |
| 🟡 | **公開交接棒「隨身軍師・一鍵接手」上線（2026-09-25，教練說「推」，後續修好AI相容性問題）** | ✅已上線，每次「總結」自動更新 | **主要網址（貼給任何AI）：`https://coach1973.github.io/ai-go/status.html`**；純文字備用：`status.md`。目的：教練Claude每週額度不夠，思考型問題分流到其他網頁版Opus，貼一個網址對方就知道規則＋目前工作狀態。🔴**真因查證（curl實測，不是猜的）**：一開始只做.md版，教練回報「其他AI說讀不到、被屏蔽」——查證GitHub Pages對.md副檔名回傳`content-type: text/markdown`，index.html回傳`text/html`；人爬蟲UA(GPTBot等)全部200無阻擋，不是robots/WAF——是多數AI內建讀網頁工具只認text/html。已建`scripts/render_public_status_html.py`(python-markdown轉換+bare URL自動連結)，`status.md`仍是唯一手改來源，`scripts/publish_public_status.sh`每次發布自動轉出`status.html`不會分岔。更新流程：`summary_upload_trigger.sh`第5步改寫`~/github_repos/ai-go/status.md`→跑`publish_public_status.sh`(機密掃描→轉HTML→再掃描→commit兩檔→push→確認網站換新版，等5分鐘)。只寫教練自己的事，不寫帳密/主機位址/路徑/他人個資。已收進coach888「工具類」第一項並改指向.html（伺服器狀態+靜態HTML都改，舊狀態備份`state/coach888_state_backup_20260925_110956.json`）。同場順便修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」（教練親口訂正，5個檔案）。🔴**教練追問揪出遺漏**：status.html內文引用的另外兩份`coach-persona.md`/`system-prompt.md`本身也是同一個content-type問題，沒有一起修——已比照建`coach-persona.html`/`system-prompt.html`，三份都納入`publish_public_status.sh`自動轉出，`index.html`的「查看全文」連結也改指向.html（JS一鍵複製到剪貼簿的fetch()維持指向.md不變，複製出來才是純文字不是HTML標籤）。順便修好`publish_public_status.sh`驗證上線的迴圈：GitHub Pages CDN偶爾超過5分鐘才生效，push本身成功卻被誤判成失敗跳exit 1（已實際發生2次），改成push成功就算數，CDN慢只如實回報不當失敗。commit：workspace`445210e92`+`8f953cd14`+`5ea38190d`、ai-go`39b84c7`+`22bbe94`+`5114dc3`+`3f4273e`、coach888`79a7d81`+`03021cb`。 |
| 🟢 | 外層`~/.openclaw`本機git歷史紀錄跟GitHub版本編號對不齊（純本機書面整理，教練2026-09-24裁示：不是外洩、不是公開風險，AI自行找時間處理，不用再提） | ✅無風險-低優先-AI自主處理 | **教練2026-09-24明確裁示**：這不是安全問題（金鑰外洩早在9/19處理完畢，repo本身是私有的、沒有外部協作者，也已決定金鑰不rotate），純粹是這台Mac的git紀錄本子跟GitHub對不上編號的書面瑣事，沒有任何被公開查到的風險，也沒有立即性危害。**教練要求：AI不准再主動提這件事，覺得需要處理就自己找時間安靜做完，不要拿來討論、不要問、不要當成待辦逐場複誦**。哪天AI自己收拾好了，直接做、不用報告；沒收拾好也不影響教練現在用的任何功能，不追蹤、不升級語氣。技術細節（若AI自己要動手）：新版GitHub歷史已把`agent/auth-profiles.json`等金鑰檔從全部commit移除，本機若直接`git reset --hard origin/master`會把本機正在用的同名檔案從磁碟刪掉，須先備份+確認`.gitignore`涵蓋再處理，過去做法可參考`c07544815`的worktree cherry-pick模式。 |
| 🔧 | **AI技術備忘（不准拿去跟教練講）：這個repo的git歷史已被改寫，其他機器的本機clone要先同步才能push** | ⚠️任何機器的AI下次動這個repo前自己看 | 2026-09-19 06:45教練親自裁示後，軍師用`git-filter-repo`把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json(.bak)`4個含明文金鑰的檔案從全部16000+ commit歷史徹底清除+強制推送到GitHub(已用全新clone獨立驗證確認乾淨)。**任何其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟GitHub遠端分岔了**——下次要push前必須先`git fetch origin && git reset --hard origin/main`(或直接砍掉重新clone)，絕對不能在沒同步的狀態下直接push，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。教練同時裁示：外洩的金鑰(MiniMax/Gemini)**不rotate**，「已經曝光不代表會被濫用，換的話動一髮牽全身」。完整過程見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | **shops.bymyway.com已拆除VPS依賴（2026-09-26），VPS上舊檔案+GitHub孤兒repo收尾** | ⏳待處理-低優先 | 3家店(huitou/ema/hsinhan)已遷移到Mac本機+DNS切換完成，VPS(43.245.60.200)上`/var/www/shops/`原始檔案故意沒刪，當一段時間的rollback安全網，穩定觀察期(建議至少2週無異常)過了可以安全刪除。另外測試時意外建立的GitHub孤兒repo`coach1973/hsinhan-2`因手上token沒有`delete_repo`權限刪不掉，已無任何連結指向它、無害，之後若拿到有delete權限的token可順手清掉。詳見`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`。 |
| 🟡 | MEMORY.md超過OpenClaw 2萬字bootstrap上限(20,717字)且有1處UTF-8亂碼，跟HEARTBEAT.md同一類問題(2026-09-25查到，只查不動，優先度低於HEARTBEAT.md因為不影響小龍蝦即時反應) | ⏳待處理 | 用跟HEARTBEAT.md同樣手法瘦身：找出佔比最大的段落搬去handoff_archive或distill、備份原檔、確認新檔UTF-8正常。不用問教練，AI自己找時間做完即可 |
| 🟡 | 軍師自我要求：查證前先查「路徑大全」+盤點類任務要窮舉底層資料結構 | ⚠️永久提醒 | 教練v90當場糾正兩次查證不完整（VPS沒先查路徑大全就回報查不到、LINE帳號盤點漏算沒有名稱標籤的「龍蝦小助教」），教練明確期許「你是所有資訊的大總管，要自己想辦法完善」。已寫入試金石案例55，核心自我檢查：①任何「查不到/做不到」結論前先確認查過該環境萬用索引檔 ②盤點類任務直接數清楚底層資料結構(JSON物件key數)逐一核對，不能只挑印象中顯眼的幾筆 |

---

> 📦 v114完整內容已封存：`handoff_archive/handoff_v114_archived_2026-08-18.md`（Mac桌面版，Chrome搶線根因+ezPay 238筆+coach888連結）

---

> 📦 v115完整內容已封存：`handoff_archive/handoff_v115_archived_2026-08-18.md`（聯想Windows，BNI-Training雙軌系統從零建置+753筆官方報表整合）

---

> 📦 v116完整內容已封存：`handoff_archive/handoff_v116_archived_2026-08-18.md`（聯想Windows，BNI培訓紀錄精準度修正+MSP投票新網站+SOP違規教訓）

---

> 📦 v117完整內容已封存：`handoff_archive/handoff_v117_archived_2026-08-18.md`（聯想Windows，4-8月簽到表開票總清冊交叉比對修正MSP名單）

---

> 📦 v118完整內容已封存：`handoff_archive/handoff_v118_archived_2026-08-18.md`（Mac桌面版，五項任務逐一執行+ezPay 108統編備註查詢完成+find -maxdepth查證失誤自我更正）

---

> 📦 v119完整內容已封存：`handoff_archive/handoff_v119_archived_2026-08-19.md`（Mac桌面版，BNI Connect活動出席勾選任務首次上線，8場活動101人次標記完成）

---

> 📦 v120完整內容已封存：`handoff_archive/handoff_v120_archived_2026-08-19.md`（Mac桌面版，讀跨機信箱接手ezPay培訓費發票，16張全部開立完成，MerchantID假成功陷阱首次發現）

---

> 📦 v121完整內容已封存：`handoff_archive/handoff_v121_archived_2026-08-23.md`（Mac桌面版，教練推翻「34人收齊才開票」規則，24張ezPay培訓費發票先開立）

---

> 📦 v122完整內容已封存：`handoff_archive/handoff_v122_archived_2026-08-24.md`（Mac桌面版，教練糾正「查無Email」誤判＋BNI 94人資料庫永久指引）

---

> 📦 v123完整內容已封存：`handoff_archive/handoff_v123_archived_2026-08-24.md`（Mac桌面版，大樹小講事件密集場：救回雙寫程式碼+場次管理後台+修好2次部署bug）

---

> 📦 v124完整內容已封存：`handoff_archive/handoff_v124_archived_2026-08-24.md`（Mac桌面版，AI助理資料包+8/28攤位頁+報名通知失聯真根因，搬運工失誤試金石案例62）

---

---

> 📦 **v112及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v116_archived_2026-08-18.md`（v116）+ `handoff_archive/handoff_v115_archived_2026-08-18.md`（v115）+ `handoff_archive/handoff_v114_archived_2026-08-18.md`（v114）+ `handoff_archive/handoff_v113_archived_2026-08-17.md`（v113）+ `handoff_archive/handoff_v112_archived_2026-08-17.md`（v112）+ `handoff_archive/handoff_v111_archived_2026-08-16.md`（v111）+ `handoff_archive/handoff_v110_archived_2026-08-16.md`（v110）+ `handoff_archive/handoff_v109_archived_2026-08-16.md`（v109）+ `handoff_archive/handoff_v108_archived_2026-08-15.md`（v108）+ `handoff_archive/handoff_v106_to_v107_archived_2026-08-14.md`（v106+v107）+ `handoff_archive/handoff_v105-lenovo_archived_2026-08-14.md`（聯想Windows 2026-08-10）+ `handoff_archive/handoff_v104_to_v105_archived_2026-08-12.md`（v104+v105 Mac桌面版） + `handoff_archive/handoff_v104-lenovo_archived_2026-08-10.md`（v104聯想Windows） + `handoff_archive/handoff_v101_to_v103_archived_2026-08-09.md`（v101~v103）+ `handoff_archive/handoff_v100_archived_2026-08-08.md`（v100）+ `handoff_archive/handoff_v99_archived_2026-08-08.md`（v99）+ `handoff_archive/handoff_v97_to_v98_archived_2026-08-07.md`（v97~v98）+ `handoff_archive/handoff_v93_to_v96_archived_2026-08-05.md`（v93~v96）+ `handoff_archive/handoff_v92_archived_2026-08-05.md`（v92）+ `handoff_archive/handoff_v91_archived_2026-08-05.md`（v91）+ `handoff_archive/handoff_v90_archived_2026-08-04.md`（v90）+ `handoff_archive/handoff_v89_archived_2026-08-03.md`（v89）+ `handoff_archive/handoff_v88_archived_2026-08-03.md`（v88）+ `handoff_archive/handoff_v87_archived_2026-08-02.md`（v87）+ `handoff_archive/handoff_v85_to_v86_archived_2026-08-02.md`（v85+v86）+ `handoff_archive/handoff_v84_archived_2026-07-31.md`（v84單獨一份）+ `handoff_archive/handoff_v83_archived_2026-07-30.md`（v83單獨一份）+ `handoff_archive/handoff_v82_archived_2026-07-28.md`（v82單獨一份）+ `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`（v72~v81）
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。

---


> 📦 v125+v126完整內容已封存：`handoff_archive/handoff_v125_to_v126_archived_2026-08-25.md`（Mac桌面版，凌晨全系統稽核+教練覆核追加任務）

---


> 📦 v127+v128+v129完整內容已封存：`handoff_archive/handoff_v127_v128_v129_archived_2026-08-25.md`（Mac桌面版，ezPay發票+台中場上線+賈維斯全系統體檢兩場+頻率覆核）

---

> 📦 v130完整內容已封存：`handoff_archive/handoff_v130_archived_2026-08-25.md`（Mac桌面版，賈維斯體檢延續：頻率覆核+解決通知從沒送達的根因，留下Q1待辦）

---

> 📦 v131完整內容已封存：`handoff_archive/handoff_v131_archived_2026-08-26.md`（Mac桌面版，AI微論壇台中場RWD真根因修復+Netlify額度重新校正）

---


> 📦 v132+v133完整內容已封存：（Mac桌面版，Q1總結功能+context-overflow-guard改版+名片系統CRM擴建）

---

> 📦 v134完整內容已封存：`handoff_archive/handoff_v134_archived_2026-08-26.md`（聯想Windows，Windows當機根因+ezPay記憶更正+跨機Stop hook查證+總結hook缺jq修復）

---

> 📦 v135完整內容已封存：`handoff_archive/handoff_v135_archived_2026-08-27.md`（Mac桌面版，BNI Connect 430人匯入+MiniMax額度事故案例65+路徑大全憑證稽核）

---


> 📦 v136完整內容已封存：`handoff_archive/handoff_v136_archived_2026-08-26.md`（Mac桌面版，BNI Connect前會員電話/Email補齊+來賓資料庫3712筆完整收集）

> 📦 v137~v139完整內容已封存：`handoff_archive/handoff_v137_to_v139_archived_2026-08-27.md`（v137 Mac桌面版媒合手動觸發定案／v138聯想Windows跨機同步四層根因／v139 Mac桌面版RustDesk修復+MiniMax紅線+bigtree密集迭代）

> 📦 v140完整內容已封存：`handoff_archive/handoff_v140_archived_2026-08-27.md`（聯想Windows，FB粉專發文API從零建置，卡在商家驗證+教練當場檢討試錯效率）

---

> 📦 v141完整內容已封存：`handoff_archive/handoff_v141_archived_2026-08-27.md`（Mac終端機，bigtree 8/28 EDM上線+報名頁LINE誘因文案定案+/slides多簡報支援+ezPay發票查證）

---

> 📦 v142完整內容已封存：`handoff_archive/handoff_v142_archived_2026-08-27.md`（Mac終端機，修復Stop hook守則#07輪詢偵測瞎眼35天的根因，commit`01a28f2fb`）

---

> 📦 v143完整內容已封存：`handoff_archive/handoff_v143_archived_2026-08-28.md`（Mac終端機，BNI信用証清查4分會171人完成，真鑽231人查了10人中途總結）

---

> 📦 v144+v145完整內容已封存：`handoff_archive/handoff_v144_to_v145_archived_2026-08-28.md`（Mac終端機v144離會會員信用証清查全數完結／聯想Windows v145 AI微論壇+ai-art獨立站建置）

---

> 📦 v146完整內容已封存：`handoff_archive/handoff_v146_archived_2026-08-30.md`（Mac終端機，BNI信用証清查後續建網頁+複查+權限隔離+誤觸事故）

---

> 📦 v147完整內容已封存：`handoff_archive/handoff_v147_archived_2026-08-30.md`（Mac終端機，/bni-credit三項待改+34筆信用証補開+搜尋空格bug修復）

---

> 📦 v148完整內容已封存：`handoff_archive/handoff_v148_archived_2026-08-30.md`（Mac終端機，乾淨世界頻道QR上線+peipei-event斷線5天修復+電腦變慢診斷）

---

> 📦 v149+v151完整內容已封存：`handoff_archive/handoff_v149_v151_archived_2026-08-30.md`（Mac終端機，真誠分會邀約來賓系統從零建置+bni-chapters重複實作/fork根因鑑識，v149與v151是同一起fork事件的兩條分支，內容已在v150結案）

---

> 📦 v150完整內容已封存：`handoff_archive/handoff_v150_archived_2026-08-31.md`（Mac終端機，真誠分會邀約來賓重複建置根因查明+移除+5位會員專屬編輯網址交付）

---

> 📦 v152完整內容已封存：`handoff_archive/handoff_v152_archived_2026-08-31.md`（Mac終端機，逐步脫離Netlify：4個新路由+3處連動+作品總覽更新）

---

> 📦 v218完整內容已封存：`handoff_archive/handoff_v218_archived_2026-09-19.md`（Mac桌面版，全部釋放+MiniMax團隊品質稽核機制+開工hook身份誤判修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

---

> 📦 v219完整內容已封存：`handoff_archive/handoff_v219_archived_2026-09-19.md`（Mac桌面版，手機/軍師討論邊界+Netlify中文檔名修復部署+後台帳密清單結案+workspace git大掃除含金鑰外洩發現+coach888熱門排行新功能）

> 📦 v220完整內容已封存：`handoff_archive/handoff_v220_archived_2026-09-19.md`（Mac桌面版，接力棒狀態表失真教訓+機械防呆`handoff_sync_guard.sh`上線+CLAUDE.md 236KB→78KB瘦身+M系列MiniMax 1M機制查證+手機Remote Control重啟卡死未解留待下一棒）

> 📦 v221+v222完整內容已封存：`handoff_archive/handoff_v221_v222_archived_2026-09-19.md`（v221 Mac桌面版，手機Remote Control真正根因查明修復+舊SOP早有答案的教訓／v222 Mac桌面版，中正大學互動牆從零建置上線+赫米斯Telegram斷線16小時根因修復，E16瘦身本場執行）

> 📦 v223~v227完整內容已封存：`handoff_archive/handoff_v223_to_v227_archived_2026-09-20.md`（v223 B路徑1M通驗證／v224跨對話框交接SOP／v225 MiniMax懸案初步調查+coach888同步修復(平行session)／v226產業鏈SOP雙執行root cause／v227 MiniMax懸案徹底解謎+手機1M實測成功，E16瘦身2026-09-20執行）

---


> 📦 v228~v230完整內容已封存：`handoff_archive/handoff_v228_to_v230_archived_2026-09-21.md`（v228憑證層git追蹤問題發現／v229 git-filter-repo歷史清除執行完畢／v230 CCU留言關閉+coach888收錄查證，E16瘦身2026-09-21執行）

---

> 📦 v231~v237完整內容已封存：`handoff_archive/handoff_v231_to_v237_archived_2026-09-24.md`（v231 TokenTable接OpenCode+Episode11漫畫+agent捏造完工案例／v232 CCU媒體格式連環修復／v233海餅乾網站+BNI PPT SOP建立／v234聯想bni-dna/bigtree維護+記憶體洩漏追蹤／v235手機流量查證鏈+EM模式定義／v237膠囊咖啡機產業鏈+語音轉簡體字記錄，E16瘦身2026-09-24執行）
