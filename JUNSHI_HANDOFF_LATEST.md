## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立）

> 這張表**取代**逐棒散落的「vXX待辦」小表——舊表格散在v72/v73/v74/v75各自的段落裡，容易漏看、也看不出哪項是「卡住等教練」還是「該我自己動手」。**以後每一棒開工先看這裡，任務完成或狀態改變就更新這張表，不要再另開一張新的待辦表。**
>
> 狀態代碼：🔒卡住-等教練　⏳待軍師/小龍蝦動手　⚠️持續追蹤(非任務)　✅已完成待確認

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟢 | 「教練都在想什麼」LINE帳號完整搬遷到Mac+MiniMax-M3 | ✅本場已完成 | 詳見下方v81完整戰果。人設逐字搬遷+46萬字知識庫+FTS5全文檢索+webhook正式上線服務121位好友+dmPolicy修復+seabiscuit.bymyway.com監控後台+User ID對照hook泛化。教練待自行測試seabiscuit.bymyway.com登入(密碼Bymyway7，第一次會卡裝置配對，把畫面ID給軍師) |
| 🟡 | 「教練都在想什麼」案例庫深度待擴充 | ⏳待教練提供更多素材 | 目前只有教練提供的4份文件(大樹使命之旅/禮物諮詢法/海餅乾文化核心逐字稿/海餅乾語錄，共46萬字)，教練原話「提供更多資料庫讓AI做更大的品牌宣傳」——若教練還有其他素材(更多逐字稿/文章/Podcast)，補進`agents/jiaolian_thoughts/knowledge/`後跑一次`python3 scripts/build_search_index.py`重建索引即可 |
| 🟡 | 教練其他類似LINE帳號待比照搬遷 | ⏳待教練指定下一個帳號 | 教練原話「我還有其他類似的帳號也要這麼做」，已產出完整SOP：`knowledges/SOP_Coze_LINE帳號搬遷小龍蝦本機.md`，下次教練指定帳號直接照SOP 12步驟走，不用重新摸索 |
| 🟢 | **結繩領導學工作坊即時戰報系統（台南/台中/台北）** | ✅v82已全功能上線 | `https://rpl-workshop.bymyway.com/admin`，帳號**RPL**(大寫)，密碼公司統編(AI全程未接觸)。15筆歷史資料已匯入(教練後續已自行登入新增/修改過，證實系統正常運作)。功能：開課倒數/目標達成率進度條/邀請人與資料提交人下拉(曜董/大樹/佩君/Lavi)/姓名可編輯/依報名日期排序/**整頁一次「全部儲存」**。詳見[[project_jiesheng_report_launch_2026-07-26]] |
| 🟢 | **event-signup簽到系統：手機號碼比對簽到（免重填資料+保留集點）** | ✅本場已完成，教練實測確認 | 教練發現原本固定簽到QR(`/checkin`)會讓已線上報名過的來賓重填一次姓名/電話，多此一舉。改成`/checkin`只問手機號碼，比對到既有報名記錄→直接記進signups表(集滿5次送禮物功能保留)+導向`/slides`(加好友+下載簡報，帶個人化「OOO簽到成功」)；查無記錄(現場臨時來賓)→導去完整表單但手機號碼已預填。7/29 AI微型論壇立牌已印(QR網址沒變不用重印)，教練親自實測通過確認採用此版本。commit `fd480212a`(QR先改指向/slides，中途方案)→`022051eba`(立牌加場次標籤)→`0ef5ee98a`(最終手機比對版本)。同場也修好`event.bymyway.com/admin`場次資料(8/1改8/26+9/5+9/19，比對`bigtree-tw.netlify.app`)。 |
| 🟢 | **圖片OCR辨識通用小工具** | ✅本場已完成 | 抽出`tools/ocr-extract/ocr_extract.py`，PaddleOCR(沿用namecard-db既有venv)→MiniMax兩階段管線，SYSTEM_PROMPT改成`field_schema`+`task_description`參數化，不綁死名片格式。過程中實測抓到真bug：`.env`讀取用`setdefault`不會覆蓋外層shell既有的`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`(終端機Claude Code自己的環境變數)，導致打到api.anthropic.com而非MiniMax端點回傳401，已改直接賦值強制覆蓋。用兩張真實名片+兩組完全不同命名的自訂欄位schema驗證通過。commit `1488b6c68`。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| 🟢 | **系統權限缺口：public agent(bni_tainan/jiaolian_thoughts)沒有工具層級限制** | ✅v83已完成 | 詳見下方v83戰果。改用OpenClaw原生`tools.toolsBySender`機制(查證版本原始碼確認真的存在且生效於主要工具判斷流程，非僅sandbox)，教練LINE ID白名單保留完整權限、其他發送者deny掉`group:runtime`+`group:fs`+`group:automation`。新增`line-user-memory`hook讓非教練用戶仍保有個人化記憶(不靠write工具，伺服器端維護)。commit `fb222757` |
| 🟡 | 教練第二身份「贏家思路」(LINE ID `U168903487f0ba2b666ddc62b854de351`)已加入白名單 | ✅v83已完成 | 教練親測時發現用這個帳號測試bni_tainan/jiaolian_thoughts會被當一般訪客擋權限，查證+教練確認後已加進toolsBySender白名單，兩個帳號都生效 |
| 🟢 | 「龍蝦小助教」(default LINE帳號，綁main agent)僅供教練個人使用，維持pairing制不開放 | ✅v83已裁示 | 教練測試時觸發配對碼，已核准教練這組LINE ID(`U168903487f0ba2b666ddc62b854de351`，同贏家思路帳號)。教練明確裁示「不需要開放給其他人」——main agent無工具限制，不可比照bni_tainan/jiaolian_thoughts開放allowFrom:["*"] |
| 🟡 | 小龍蝦後台(OpenClaw原生控制介面)不顯示用戶中文名稱 | 🔒卡住-教練決定用問答方式 | 查證確認這是OpenClaw原生Control UI的已知限制(GitHub上至少8個未解決的相同feature request)，非設定缺漏。已評估「另建自訂監控頁面」的時間/token成本，教練裁示「若有問,你再回我就好」——不建頁面，教練看到陌生ID直接問軍師，軍師查`state/{account}_line_id_map.json`即時回覆即可 |
| 🟢 | 開工六步驟+MEMORY.md額度瘦身 | ✅v83已完成 | 教練要求評估「開工」占用多少KB(對應1M上限)。實測發現workspace/CLAUDE.md已自動鏡像接力棒全文，六步驟hook卻又重複cat一次；另有claude-sessions/死code(18天未更新)。已修復：接力棒改「確認同步新鮮度才決定貼短版或全文」的安全網設計(不冒漏接風險)、砍死code、試金石3→2案例、memory最新日改尾端6000字。單次注入實測49,593→20,588 bytes(降58%)。MEMORY.md索引退休7條已解決舊專案記憶(31.5KB→30KB)。commit `e9144daf8`+`12e7b6b54` |
| 🟢 | bni_tainan行事曆同步cron實際上從未存在過，已修復 | ✅已完成 | 查證發現v75紀錄的cron job 99bdac4a 在 cron list 裡根本查無此ID，行事曆檔案卡在40+小時沒更新。新建 cron `7048432e`（每4小時，已修好delivery歧義設定），手動觸發驗證 exitCode 0 + 檔案內容確實更新 |
| 🟢 | BNI大台南小幫手LINE送達備援+網址防呆+會員ID對照 | ✅已完成 | 詳見v80完整戰果，三個hook都已重啟驗證+commit。會員ID對照hook本場(v81)已泛化為全LINE帳號通用，不影響原有功能 |
| 🔴🔴🔴 | BNI大台南小幫手「主動提醒」功能 | ⏳待動手 | v77已設計好事件驅動流程（cron --at --delete-after-run），下一場直接照設計實測，本場只寫了計畫沒動手 |
| 🔴🔴🔴 | 真誠分會／真愛分會／真實AI分會願景+產業分佈圖說明書 | 🔒卡住-等教練 | 連續v72起多棒未開始，教練還沒給細節 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | 一直是credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。目前`state/netlify_deploy_quota.json`最新記錄剩66次(2026-07-25，聯想機序列)——Mac這棒也部署過2次(bigtree-tw/ai-talk-tw)，但發生在教練貼credit截圖查明真制度**之前**，71這個基準值本身已經是教練當下實測的真實餘額(已經反映過Mac那2次的扣減)，聯想後續3次部署往下扣到66，兩邊沒有重複計算，66可信。但這只是本地推算，下次部署前仍建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🟡 | coach888拖拉排序功能 | ⏳待教練回饋 | v72已用真實滑鼠事件測試交付，尚無教練實際使用回饋記錄，下一場先問「好用了嗎」 |
| 🟡 | 「全世界最優秀的團隊計畫」報名連結 | 🔒卡住-等教練 | 兩顆按鈕還沒掛真實報名連結，等教練給LINE或表單網址 |
| 🟡 | 企業健身房正式建站（coach1973.github.io/Business.gym） | 🔒卡住-等教練 | 網址教練已親貼確認，但尚未正式交辦開工 |
| 🟡 | 企業健身房4項文案修改 | 🔒卡住-等教練 | 已記錄commit 10c7b11cf，等教練繼續交辦下一步 |
| 🟢 | `.env`含`$`字元值要單引號包住 | ✅本場真實踩到並修好 | jiesheng-report密碼雜湊值含`$`被bash source吃掉，已修復+寫入記憶[[project_jiesheng_report_launch_2026-07-26]]。Jinja模板guard None值這條仍待抽空檢查其他Flask小專案 |
| 🟡 | BNI小幫手教練親測多種問法 | ⏳待教練體驗 | 確認BNI小幫手實戰體驗OK |
| 🟡 | Coze舊機器人何時停用 | 🔒卡住-等教練 | 先保留當備援，等教練確認新系統穩定一陣子後裁示 |
| 🟡 | ACER 36.3GB備份待刪（觀察期已過） | 🔒卡住-需教練在ACER機器親自開對話執行 | 這台Mac無法代為執行 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | 光線尺顧問ATM NT$10,000入金(07-13)對帳 | 🔒卡住-等教練 | 待教練對帳 |
| 🟢 | 「連接」按鈕自動化點擊無反應（真人操作無此問題） | ✅已排除疑慮 | 教練親自兩台電腦實測「連接」按鈕正常，先前疑慮的bug只影響自動化工具合成點擊事件，教練不會遇到，暫不需修 |
| 🟡 | plugins.allow白名單未設定 | ⏳待軍師動手 | 07-24更新後新增警告：「plugins.allow is empty」，非阻斷性，建議之後找空檔補上明確允許清單（minimax/active-memory/memory-core/google/safety-locks/line/llama-cpp），非緊急 |
| 🟢 | ~/.claude/CLAUDE.md與執行細則.md的E10~E12分岔 | ✅已完成 | 教練裁示「合併，因為這樣才簡單」。執行細則.md保留權威版，Karpathy三原則改編號E13~E15追加。新增`scripts/sync_zhixingxize_to_claude_global.sh`+openclaw cron(job 37593697,每30分鐘)自動鏡像，結構性根治，不會再分岔。commit `0a4271d80` |
| 🟡 | 小龍蝦紀律移植計劃 階段二／三 | ⏳待軍師動手 | 階段一(真相源驗證+E07語音糾偏規則)本場已實作進`hooks/rule-reminder/handler.js`並測試+commit`4f08cd27`+重啟gateway驗證健康。階段二(cron驗證/記憶寫入雙鐵律/引用查證，先只對main agent生效觀察一週)、階段三(危險指令防禦)待排時機，詳見`knowledges/2026-07-24_小龍蝦紀律移植計劃_mattpocock skills精神落地.md` |

---

# 軍師接力棒 · 2026-07-26 v83（Mac桌面版 Sonnet 5，系統權限缺口正式解決+開工額度瘦身58%+教練雙LINE身份釐清）

> 建立時間：2026-07-26 深夜～07-27 凌晨（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v82（Mac桌面版Sonnet5，結繩領導學戰報系統上線）
> 本棒主軸：**接續v82尾聲留下的兩個未解問題：①系統權限缺口(public agent沒有工具限制)②圖片OCR工具。本場教練先轉發小龍蝦整理的LINE綁定時間軸研究，逐行查證全部準確後，發現OpenClaw原生`tools.toolsBySender`機制，比之前設計的「移除exec+hook替代」方案更直接，當場實作+驗證+commit，權限缺口正式解決。教練釐清「鎖權限不能連個人化服務都擋掉」，新增line-user-memory hook補上訪客記憶功能。教練親測時意外發現自己有第二個LINE身份「贏家思路」，也一併加入白名單。教練接著要求評估「開工」占用多少KB，實測抓出接力棒被workspace/CLAUDE.md與六步驟hook重複注入的問題，修好後單場注入降58%，順手清理MEMORY.md索引裡7條已解決的舊記憶。教練詢問接力棒實際內容，也詢問小龍蝦後台為何不顯示中文名稱——查證後確認是OpenClaw原生介面已知限制，評估自建頁面成本後教練裁示不做，改用隨問隨查方式。OCR工具本場雖未動，但交接棒走出v83後終端機那邊07:01已抽出通用工具完成（commit `1488b6c68`），13:36 教練親自驗收，標記為「已完成」。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 系統權限缺口正式解決：OpenClaw原生`tools.toolsBySender`取代卡關已久的exec移除方案
教練轉發一份小龍蝦整理的「LINE龍蝦小助教綁定教練ID完整時間軸」，逐行核對`verbatim/*.jsonl`原始記錄+`.memsearch`檔案，確認每一筆引用(含精確行號、教練原話)全部準確。但該文件建議的解法（把`allowFrom`限縮成只有教練ID）會打臉教練同一份文件自己引用的SOP、也會打斷BNI會員/121位好友的開放聊天功能，予以指出並修正方向。上網查證(WebSearch+直接讀本機安裝的OpenClaw原始碼`/opt/homebrew/lib/node_modules/openclaw/dist`確認非文件想像)找到`tools.toolsBySender`：可依發送者ID分別設定`deny`/`alsoAllow`，且證實運作在**主要工具判斷流程**(非僅sandbox模式)。為`bni_tainan`/`jiaolian_thoughts`兩帳號設定：教練LINE ID(`id:U895a0ad8...`)保留完整權限，`"*"`(其他所有人)deny掉`group:runtime`(exec/process)+`group:fs`(read/write/edit)+`group:automation`(cron/gateway)。同時修好`knowledge-search-inject`/`bni-calendar-inject`兩支hook缺少`path`欄位的註冊bug並正式啟用(之前一直是"disabled"從未被驗證過會不會觸發，這次修好bug後兩者都顯示`✓ready`)，確保知識庫問答功能在鎖權限後仍正常運作。commit `fb222757`。

### 2. 🔴🔴🔴 教練提醒「鎖權限不能連個人化服務都擋掉」，新增line-user-memory hook
教練指出要像VPS版小龍蝦一樣，訪客仍要能被記住喜好、能搜尋、能對話、能被分析圖片——單純deny整組`group:fs`會連這些合理功能都砍掉。查證VPS版做法(`clients/{id}.md`per-user檔案)後，設計新hook`line-user-memory`：**完全不給agent任何write/exec工具**，改由Node.js伺服器端(不受LLM對話內容影響)幫每位訪客維護`agents/<accountId>/clients/{userId}.md`，每則訊息自動讀取歷史+注入context+append新內容。教練本人(含後述第二身份)排除在外。本機模擬呼叫測試3種情境(新用戶首次/二次讀到歷史/教練身份正確跳過)全部通過才commit。

### 3. 🎯 教練測試「龍蝦小助教」意外發現第二LINE身份「贏家思路」
教練逐一測試三個LINE帳號，小幫手/教練都在想什麼皆正常，但測試「龍蝦小助教」(default帳號，綁`main` agent)觸發陌生人配對碼。查證這組ID(`U168903487f0ba2b666ddc62b854de351`)，直接呼叫LINE API確認displayName是「贏家思路」——教練確認這是他自己的第二個LINE帳號。已核准該配對碼(僅此帳號一次性approve，non-broadcast)，並把這組ID也加進`bni_tainan`/`jiaolian_thoughts`的toolsBySender白名單，確保教練用任一身份測試都保有完整權限。**教練明確裁示：「龍蝦小助教」維持個人專用，不比照另外兩個帳號開放allowFrom:["\*"]**——因main agent本身無工具層級限制，開放給陌生人風險遠高於已鎖權限的bni_tainan/jiaolian_thoughts。

### 4. 🎯🎯 開工KB額度評估+瘦身58%
教練要求實測「開工」占用多少KB(對應對話1M上限)。逐項量測後發現：①`workspace/CLAUDE.md`本身已由既有`sync_handoff_to_claudemd.sh`每5分鐘自動鏡像接力棒全文，桌面版啟動讀CLAUDE.md就會看到；②六步驟hook(`feed_junshi_handoff.sh`)卻又完整cat一次同一份接力棒——等於同一份東西送兩次；③`claude-sessions/`最新session總結機制已死掉18天(卡在07-08一次性匯入，注入的是07-01一場無關的ACER設定總結)。修復：接力棒改成先比對sync marker時間戳，確認CLAUDE.md鏡像是最新的才用短版指向(不重複貼)，若鏡像不新鮮則安全退回完整貼上(**接力棒內容本身完全沒被簡化，教練2026-05-29的「接力棒不可簡化」鐵律沒有被違反，只是不重複送**)；砍掉死掉的session總結注入；試金石案例3→2；memory最新日改尾端約6000字。本機實測：故意把sync marker調到過期狀態，確認安全網真的會退回完整貼上才commit。單場注入從49,593 bytes降到20,588 bytes(降58%)。另外配合教練確認，把`MEMORY.md`索引裡7條已完全解決、跟現有待辦無牽連的舊專案記憶退休(31,497→30,052 bytes，原始檔案保留磁碟未刪)。commit `e9144daf8`(六步驟)+`12e7b6b54`(MEMORY.md)。

### 5. 🎯 教練詢問接力棒內容+小龍蝦後台中文名稱問題查證
教練直接問「接力棒的內容是什麼」，用白話向教練說明接力棒=「現在還欠什麼」的追蹤表+「最近做了什麼」的詳細日記兩塊構成。另外教練反映小龍蝦後台(OpenClaw原生「控制」Control UI)一直看不到用戶中文名稱，查證CLI選項+GitHub議題(至少8個開發者提過同樣需求，官方均未解決)確認這是原生介面本身的功能缺口，不是設定漏掉，也澄清`seabiscuit.bymyway.com`其實只是同一套原生介面的另一個網址別名，不是獨立打造的頁面。評估「另建自訂頁面」的時間(30~90分鐘)/token成本後，教練裁示**不建頁面，看到陌生ID直接問軍師查`state/{account}_line_id_map.json`對照表即可**。

## 📋 下一場直接開工任務

**🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（工作總表最熱項目，v77 已設計好整套事件驅動流程 cron `--at --delete-after-run` 架構，方向清楚動手即可，不再傾向空泛討論）：教練提出「BNI 會員加入/業績達標/特定節日/會議前 1 小時」等情境要主動打給對方。詳見v77設計文件。註：v83 接力棒本來寫「OCR 通用工具」但實際上 07:01 終端機那邊已抽出 `tools/ocr-extract/ocr_extract.py` 完成（commit `1488b6c68`），且 13:34 教練已親自在終端機跟軍師確認「未來會用 OCR 取代燒 Token 視覺看圖方式」，本場順手換成下一個真正待辦。

## 🔑 本場關鍵檔案索引
- `openclaw.json`：新增`agents.list[bni_tainan/jiaolian_thoughts].tools.toolsBySender`(教練兩個LINE身份白名單+`*`deny規則)、`hooks.internal.entries`修好path+啟用knowledge-search-inject/bni-calendar-inject/line-user-memory
- `hooks/line-user-memory/{HOOK.md,handler.js}`：新hook，訪客個人化記憶不靠write工具
- `scripts/feed_junshi_handoff.sh`：接力棒防重複注入安全網設計+死code清理+試金石/memory瘦身
- `claude-brain/MEMORY.md`：退休7條舊記憶
- `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`：v81併入封存
- commit序列：`fb222757`(權限鎖+line-user-memory) → `e9144daf8`(六步驟瘦身) → `12e7b6b54`(MEMORY.md瘦身)

---

# 軍師接力棒 · 2026-07-26 v82（Mac桌面版 Sonnet 5，結繩領導學戰報系統全功能上線+Cloudflare Token安全清理+下一場OCR工具交辦）

> 建立時間：2026-07-26 傍晚（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v81（Mac終端機Sonnet5，「教練都在想什麼」LINE帳號完整搬遷上線）
> 本棒主軸：**接手聯想機寫好的jiesheng-report程式碼，完成Mac端部署上線，過程中修好一個真bug（.env密碼雜湊被bash source吃掉導致密碼永遠登不進去），並依教練多輪追加需求把系統做完整（一次全部儲存/序號/姓名可編輯/排序/邀請人與資料提交人）。中途發現並清理2個先前seabiscuit任務遺留的Cloudflare臨時Token（安全debt清償）。尾聲教練提出Token成本疑慮，查證確認screenshot截圖真的貴，教練也回憶起namecard-db已有驗證過的PaddleOCR+MiniMax辨識管線可複用，本場對話長度已高（10+小時/30+輪）教練主動要求總結收尾，開新對話繼續做OCR通用工具。**

## 🎯 本場戰果

### 1. 🎯🎯🎯 結繩領導學工作坊戰報系統(jiesheng-report)完整部署上線
接手聯想機已寫好的Flask+SQLite程式碼，建venv+LaunchAgent(`com.coach.jiesheng-webapp.plist`)常駐port 5063(原建議5061跟既有peipei-event撞了)，Cloudflare Route(CLI+臨時API Token比照seabiscuit做法，用完即刪)接上`rpl-workshop.bymyway.com`。過程順手清掉2個seabiscuit任務遺留、忘記刪除的Cloudflare臨時API Token(安全debt清償)。

### 2. 🔴🔴🔴 真bug：.env密碼雜湊被bash source吃掉，密碼永遠登不進去
教練實測登入失敗、給出真實密碼(42710762)要我確認，本機雜湊比對(不經過網頁登入表單)發現密碼雜湊值裡的`$`符號被LaunchAgent的`bash -c "source .env"`當成shell變數展開吃掉一截。修復：`.env`裡含`$`的值一律加單引號。這條試金石早有記錄（[[feedback_settings_hook_verify]]附近文件曾提過.env含$要加引號）但這次是真的踩到才發現新專案沒套用到，教訓已寫進[[project_jiesheng_report_launch_2026-07-26]]。

### 3. 🎯🎯 歷史資料匯入15筆(台南4/台中1/台北10)
教練提供4張報名截圖(3張分場+1張金流總表)，交叉比對姓名+日期，台北10筆裡8筆有精確付款日期(比對金流總表)、2筆無金流紀錄的(含教練指定的「沒有金流的都標6/29」規則)。教練事後親自登入系統新增1筆(邱于騰)+修改1筆(林俊瑋改已繳費)，證實系統正常運作。

### 4. 🎯🎯🎯 教練多輪追加需求，系統做到「一次全部儲存」
教練反映「改一個欄位就要按一次儲存」太繁瑣，整個table改成單一表單設計，底部一個「💾全部儲存」按鈕一次送出所有列的變動；刪除維持各自獨立按鈕(不受影響)。另加序號欄#、姓名改可編輯(教練舉例「李俊國」打錯成「林俊偉」的情境)、排序改依報名日期(舊到新，最新報名排最下面)、新增「資料提交人」欄位(同帳號共用登入，用這欄記錄誰實際操作，四選一曜董/大樹/佩君/Lavi)、新增表單直接支援金流欄位(已繳費/繳費方式/金額，一次到位不用事後補)。標題「後台」字樣依教練指示全數移除，只留「即時戰報」。全部功能均用真實瀏覽器互動測試(非DOM操作)驗證通過。

### 5. 🎯 Token成本意識+找到更好的圖片辨識方案
教練發現本場截圖近40張，質疑Token消耗，查證後誠實回報「無法給精確Token數字」（沒有即時計數器）。教練指示「智慧地截圖」——同批功能改完再截一次，不要每改一處截一次，已寫入[[feedback_screenshot_rules_consolidated]]。教練接著提出用Hermes/MiniMax做圖片辨識省Token的構想，查證MiniMax-M3確實支援原生視覺輸入，但更進一步教練想起`namecard-db`已有驗證過、比直接視覺辨識更準的**PaddleOCR+MiniMax兩階段管線**(本機OCR免費+MiniMax不限流量整理成JSON，零Token成本)，已寫入[[reference_namecard_ocr_pipeline_reusable]]。

## 📋 下一場直接開工任務（教練已交辦，方向清楚不用再問）

**把`namecard-db/extract.py`的兩階段OCR管線抽成通用小工具**，不綁死名片欄位，讓「讀圖片建檔」這類任務都能複用（不用AI自己盯圖片瞇眼看，且免費/不耗Token）。
- 核心參考：`namecard-db/extract.py`的`extract_card_fields()`函式（PaddleOCR→MiniMax兩階段）、`paddle_extract.py`（獨立Python3.11環境跑PaddleOCR的子行程）
- `.env`裡已有`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`(指向MiniMax端點)/`NAMECARD_MODEL`設定可直接沿用
- 設計方向：把SYSTEM_PROMPT參數化（不寫死名片JSON schema），讓呼叫端可以傳入「這次要辨識什麼欄位」
- 下一場直接讀[[reference_namecard_ocr_pipeline_reusable]]這份記憶+上述兩支程式碼即可開工，不用重新查證能力/找檔案


---

> 📦 **v81及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒(v83/v82)在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。
