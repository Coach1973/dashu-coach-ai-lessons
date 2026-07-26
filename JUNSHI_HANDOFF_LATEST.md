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
| 🔴🔴🔴 | **圖片OCR辨識通用小工具**（2026-07-26交辦，下一場直接開工） | ⏳待軍師動手 | 教練指出`namecard-db`的PaddleOCR+MiniMax兩階段辨識管線已驗證高準確度、零Token成本，要求抽成通用小工具，不要每次讀圖片都靠AI自己瞇眼看。參考檔案：`namecard-db/extract.py`(核心邏輯`extract_card_fields()`)、`paddle_extract.py`(獨立Python3.11環境跑PaddleOCR)、`.env`裡的`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`/`NAMECARD_MODEL`設定。詳見[[reference_namecard_ocr_pipeline_reusable]]。下一場直接讀這份記憶+兩支程式碼開工，不用重新查證。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| 🔴🔴🔴🔴 | **系統權限缺口：public agent(bni_tainan/jiaolian_thoughts)沒有工具層級限制** | 🔒卡住-需繼續驗證 | 教練親測「是不是只有你才能命令我修改？」得到「目前還不是」，確認缺口真實存在。已設計修復（openclaw原生 tools.profile 移除 exec/write/edit，改用 hook 伺服器端注入取代）但驗證卡關——CLI測試（openclaw agent --message）不會觸發 message:preprocessed 事件，改用真實簽章 LINE webhook 模擬呼叫測試也未見觸發證據，無法確認新設計在正式流量下真的生效，已完整 revert 回可驗證安全的 exec 版本（避免讓服務中的 bot 處於未知狀態）。新 hook（knowledge-search-inject / bni-calendar-inject）已寫好但設為 disabled，下一場需要專門時間查清楚為什麼 hook 沒被觸發（懷疑跟測試路徑或 webhook payload 格式有關），驗證通過才能重新啟用+移除exec。commit `02b07bfc` |
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

# 軍師接力棒 · 2026-07-26 v81（Mac終端機 Sonnet 5，「教練都在想什麼」LINE帳號完整搬遷上線+SOP產出）

> 建立時間：2026-07-26 凌晨（台灣時間）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v80（Mac終端機Sonnet5，BNI小幫手三道防呆hook+四分會通訊錄擴建，預告本場任務）
> 本棒主軸：**教練開工後直接照v80預告，把「教練都在想什麼」LINE帳號完整搬遷到小龍蝦本機。過程比BNI小幫手複雜得多：manager.line.biz顯示webhook是空的，但LINE Developers Console(真相源)查出其實一直有Coze串接，順藤摸瓜找到對應bot、逐字擷取三層人設(禮物諮詢法+TREE-6模型+海餅乾三大信念十大守則)，卻發現Coze原本掛的6個知識庫全部「系統內部異常」從未真正處理成功。教練提供4份原始資料(46萬字)後，先做完agent建置+webhook正式切換上線(服務121位好友)，切換後教練親測踩到跟BNI一樣的陌生人配對關卡(第二次犯同一個坑)，當場修復。教練接著指示解決大知識庫拖慢回覆速度的問題，改用SQLite FTS5全文檢索取代整包塞進提示詞。最後教練要求建監控後台(seabiscuit.bymyway.com)，Cloudflare網頁後台卡在要求輸入帳單資訊，改用CLI+臨時範圍限縮API Token繞過完成。教練點出User ID對照hook沒有自動套用到新帳號，當場把該hook泛化為全帳號通用。尾聲教練要求把整套流程寫成SOP供其他類似帳號複用。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 真相源查證：manager.line.biz顯示空白，Developers Console揭穿其實一直有Coze串接
教練確認「教練都在想什麼」帳號要搬遷後，先查`manager.line.biz`後台，Webhook網址欄位顯示空白，一度誤判「這個帳號完全沒有既有機器人」並回報教練。教練糾正查證不完整、指出Coze裡確實有明確寫好的persona，要求重新查。改查`developers.line.biz/console`（真相源）才發現Webhook其實一直指向`https://api.coze.com/adapter/line/webhook/7587779377988894725`且「Use webhook」是開啟中——manager.line.biz的顯示是介面不同步的假象。用這組bot ID在Coze後台（`大樹教練@COACH_WU`空間）比對出正確的bot，同空間裡還有BNI小幫手、AI實驗小學、大法經書等其他不相關bot，確認只處理對應這個LINE帳號的那一個。

### 2. 🎯🎯 逐字擷取Coze三層人設（禮物諮詢法 + TREE-6模型 + 海餅乾核心教條）
Coze的Persona編輯框是虛擬化渲染，一次讀不全，逐段捲動+逐段用accessibility tree讀取拼接。人設本身是教練多次疊代寫成，同一份prompt裡有三層疊加的「Role」區塊（核心定位/核心技術/TREE-6模型 → 核心宇宙觀/絕對限制/Tone & Speaking Style → Profile/Core Doctrine(團隊使命+三大信念+十大行為守則，標註「絕對不可修改」)/人物隱喻/推薦連結庫），全部逐字搬進`agents/jiaolian_thoughts/AGENTS.md`，未刪減未意譯。教練事後親自把人設裡的案例姓名改成匿名化（陳小姐/李先生），並加註「個案匿名化」規則（組織公開代表人物峯哥/明麗/佩君/紅霞不在此限）。

### 3. 🔴🔴🔴 Coze知識庫全部損壞（0 segments），教練提供46萬字原始資料補齊
Coze bot掛的6個知識庫（大樹使命/海餅乾文化/禮物諮詢原則/禮物諮詢法1-4/禮物諮詢法5-9/禮物諮詢最新案例）逐一點開檢查，全部顯示「系統內部異常」、0 segments——Coze版機器人實際上檢索不到任何案例，人設裡提到的真實案例（手汗、上台恐懼等）內容讀不出來。教練確認電腦裡有原始.docx，隨後提供4份檔案：《大樹使命之旅》《禮物諮詢法》（Downloads資料夾）+《海餅乾文化_核心逐字稿》（桌面「歷史資料/海餅乾知識庫」）+《海餅乾語錄》（桌面），共約46萬字，皆已擷取純文字存進`knowledge/*.md`，含真實案例逐字稿（佩軍老師手汗案例等，人設裡已改匿名）。

### 4. 🔴🔴🔴 效能優化：46萬字改用SQLite FTS5全文檢索，不整包塞進提示詞
教練指示「這麼龐大的資料庫要怎麼確保反應速度不要太慢」，並提示參考信念二(OPE)去查現成解法，舉例「一整本聖經放進去要怎麼快速搜尋」。查證ClawHub有現成RAG外掛(gbrain/activewiki)但需要額外裝Postgres等重型基礎設施，改用Python內建零依賴的SQLite FTS5：`scripts/build_search_index.py`把`knowledge/*.md`（docx擷取常常沒有段落換行，需額外用中文句尾標點二次切分）切成767個語意段落建索引；`scripts/search_knowledge.py`做關鍵字全文查詢。`AGENTS.md`新增指引要求agent用exec呼叫搜尋腳本取代整份讀取。實測驗證：問「上台恐懼」「偏頭痛」等問題，agent真的呼叫了`search_knowledge.py`（trajectory log可查證），答案正確不編造。

### 5. 🎯🎯 Agent建置+LINE通道註冊+webhook正式切換上線
新建`agents/jiaolian_thoughts/`，`openclaw channels add --channel line --account jiaolian_thoughts`註冊Channel ID 2008779326，`openclaw agents add jiaolian_thoughts --bind line:jiaolian_thoughts --model minimax/MiniMax-M3`建立綁定。本機測試（三大信念逐字引用、手汗案例正確應用禮物諮詢法）皆正確、LINE格式規則（禁**號/用【】/留空行）皆遵守。教練確認「現在就切，正式上線」後，在`developers.line.biz`把Webhook URL改成`https://openclaw.bymyway.com/line/webhook`，Verify回Success（`statusCode: 200`實測確認），`channels status`顯示running，正式服務121位好友，Coze版本停止回應。

### 6. 🔴🔴🔴 陌生人配對關卡+獨立對話記錄——同一個坑第二次犯，當場修復
webhook切換後真人朋友（`U895a0ad8e49d75f8303dc3d067282dc0`）傳訊息卡在OpenClaw陌生人配對關卡（跟bni_tainan v75同一個坑，建置時漏設定）。教練原話「這種問題不應該重複發生啊！我們不是都有試金石檔案嗎？」——修復：`channels.line.accounts.jiaolian_thoughts`加`dmPolicy: open`+`allowFrom: ["*"]`+`groupAllowFrom: ["*"]`；對應route加`session.dmScope: per-channel-peer`確保每位好友獨立對話記錄不混在一起。`gateway restart`後確認三個LINE帳號（default/bni_tainan/jiaolian_thoughts）皆running。commit `8b73bbea`。

### 7. 🎯🎯 seabiscuit.bymyway.com監控後台上線（Cloudflare付費牆繞過）
教練要求仿照`bni.bymyway.com`模式建立獨立監控後台，取名`seabiscuit.bymyway.com`。Cloudflare Zero Trust網頁後台這次卡在要求先輸入帳單/付款資訊才能進入（未替教練輸入任何付款資料，直接退出）。改用`cloudflared tunnel route dns openclaw-macmini seabiscuit.bymyway.com`（CLI走本機cert.pem認證，不受網頁付費牆限制）建立DNS，再建立一個範圍限縮為「Cloudflare Tunnel:Edit」、7天效期的臨時API Token，透過官方API（`PUT /accounts/{account}/cfd_tunnel/{tunnel}/configurations`）把新hostname加進tunnel `openclaw-macmini`的ingress規則（version 11→12），指向`http://localhost:18789`。完成後立即刪除該臨時Token（Cloudflare後台+本機皆清除）。`curl https://seabiscuit.bymyway.com/`回200，登入頁面正常顯示，密碼沿用既有`Bymyway7`。過程中教練實測真人連線一度卡在「gateway password missing」（重新整理後應可解決，屬已知UI小毛病）+ 裝置配對，皆已即時排除/核准（`openclaw devices approve 8704af4e-...`）。workspace commit `5a34e8ccf`記錄此不在git範圍的基礎設施變更。

### 8. 🔴🔴🔴 User ID→真實姓名對照hook泛化為全LINE帳號通用（教練二次提醒同一坑）
教練提醒：「別忘了之前的設定，每一個用戶你都要去找他的ID...不要一個一個都要讓我再重複講一次」——原本`bni-member-directory-map`這支hook寫死只認`bni_tainan`帳號，建立jiaolian_thoughts時沒自動套用。改寫成從sessionKey（`agent:<accountId>:line:direct:<userId>`）動態解析帳號，token/通訊錄路徑改用accountId動態組成；沒有`member_directory.md`的agent（如jiaolian_thoughts）優雅降級為`confidence: no_directory`，只記displayName不硬猜姓名，不報錯。實測驗證：jiaolian_thoughts真實inbound成功查到`U895a0a...`的displayName是「吳大樹」，正確寫入`state/jiaolian_thoughts_line_id_map.json`。gateway重啟後`hooks list`顯示✓ready。commit `9c95e096`。**以後新增任何LINE帳號都自動套用，不用再重複交代。**

### 9. 🎯 SOP產出：Coze LINE帳號搬遷小龍蝦本機標準作業程序
教練原話：「請嚴謹地把這個流程寫出一個SOP，因為我還有其他類似的帳號也要這麼做。」完整記錄本場12個步驟：查證真相源技巧/Coze人設虛擬化擷取方法/知識庫健康度查證/本機agent建置指令/46萬字以上效能處理/dmPolicy+dmScope必做三件套/webhook切換流程/User ID對照hook(已泛化免設定)/監控後台建置(CLI繞過Cloudflare付費牆)，結尾附完整檢查清單。`knowledges/SOP_Coze_LINE帳號搬遷小龍蝦本機.md`，commit `2cee17f6b`。

## 📋 v81 待辦（已併入最上方狀態總表，此處補充細節）
| 優先 | 項目 | 說明 |
|---|---|---|
| 🟡 | 教練親自測試seabiscuit.bymyway.com登入 | 已核准教練這台裝置的pairing，理論上重新按連接即可進入，需教練確認實際體驗OK |
| 🟡 | 「教練都在想什麼」知識庫深度擴充 | 目前只有教練提供的4份文件，教練若有更多素材可隨時補進`knowledge/`+重建索引 |
| 🟡 | 其他類似LINE帳號待教練指定 | SOP已就緒，下次教練說「搬XX帳號」直接照SOP走 |

## 🔑 本場關鍵檔案索引
- `agents/jiaolian_thoughts/AGENTS.md`（完整人設，三層疊加逐字搬遷+匿名化規則）
- `agents/jiaolian_thoughts/knowledge/*.md`（4份原始資料，46萬字）
- `agents/jiaolian_thoughts/scripts/{build_search_index,search_knowledge}.py`（FTS5全文檢索）
- `hooks/bni-member-directory-map/handler.js`（已泛化為全帳號通用）
- `knowledges/SOP_Coze_LINE帳號搬遷小龍蝦本機.md`（新SOP文件）
- `claude-brain/project_seabiscuit_dashboard_2026-07-26.md`（Cloudflare tunnel設定變更記錄）
- commit序列：`0e7fb756`(agent+人設+知識庫) → `ba5cd0c9`(FTS5效能優化) → `8b73bbea`(dmPolicy修復) → `9c95e096`(hook泛化) → `2cee17f6b`(SOP，workspace repo) → `5a34e8ccf`(dashboard記錄，workspace repo)

---


---

> 📦 **v80及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v72_to_v80_archived_2026-07-26.md`
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒(v82/v81)在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。
