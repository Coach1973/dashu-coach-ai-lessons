## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立）

> 這張表**取代**逐棒散落的「vXX待辦」小表——舊表格散在v72/v73/v74/v75各自的段落裡，容易漏看、也看不出哪項是「卡住等教練」還是「該我自己動手」。**以後每一棒開工先看這裡，任務完成或狀態改變就更新這張表，不要再另開一張新的待辦表。**
>
> 狀態代碼：🔒卡住-等教練　⏳待軍師/小龍蝦動手　⚠️持續追蹤(非任務)　✅已完成待確認

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟡 | **Email自動發送系統** | 🔒卡住-等教練給細節 | 2026-07-28教練提出下一個任務方向，僅先記錄，教練尚未說明要發什麼內容/給誰/觸發時機(定期報表？表單提交後自動回信？行銷群發？)，下一場先問清楚用途再評估技術方案(SMTP/SendGrid/Gmail API等) |
| 🟢 | **event-signup抽獎轉盤(/wheel)：簽到名單自動帶入+獎品庫存追蹤** | ✅v85完成，7/29現場正式使用 | 詳見v85完整戰果。名單直接查簽到記錄不用手動輸入、獎品清單+抽中自動扣庫存+中獎彈窗+15句趣味台詞。7/29教練現場異地登入密碼重設(改成教練指定的新密碼)+實測登入成功，詳見v86 |
| 🟢 | **LINE綁定率低(56簽到僅12綁定)真正原因+修復** | ✅v86已完成 | `/checkin`簽到路徑的`/slides`頁面沒有像線上報名`/thanks`頁面一樣幫來賓預填「我是OOO，剛報名了XXX」問候語，來賓要自己手動輸入才會綁定，多數人卡在這步放棄。已修復`slides_landing()`補上同一套`greet_url`邏輯，測試通過並部署，未來場次現場簽到綁定率應明顯改善 |
| 🟢 | **AI微型論壇台南場轉型為活動回顧頁** | ✅v86已完成 | 仿照全球健康發展協會(northern-tw.netlify.app)做法，`ai-talk-tw.netlify.app`從報名頁轉成歷史紀錄：花絮換成教練提供的24張現場真實照片、拿掉倒數計時器/報名區塊、CTA全改「加入LINE」、新增下一場嘉義場預告。GitHub commit `78213ed`，Netlify部署`6a6a1a24` |
| 🟡 | **下一場：嘉義場** | 🔒卡住-等教練給細節 | 教練7/29晚間提到下一場預計辦在嘉義，尚未給時間/地點/講師等任何細節，教練給了之後可直接比照台南場經驗開工 |
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
| 🟢 | BNI大台南小幫手「主動提醒」功能 | ✅v87已完成，教練實測LINE推播成功 | v77原設計要agent自己exec呼叫cron，但v83鎖了非教練發送者的exec/cron權限，此設計已失效。改用`hooks/bni-reminder-schedule/`伺服器端hook解析中文時間(相對/絕對，含中文數字)+提醒內容直接排一次性cron，不需要任何會員拿到工具權限，架構上對所有會員一視同仁(非教練專屬)。教練真實傳LINE訊息測試收到推播確認成功。commit `e3608229` |
| 🟡 | 「教練都在想什麼」LINE語音訊息無法辨識 | ⏳v87已修復待驗證 | 查production log證實2026-07-29有真實會員傳語音、transcribe失敗(reason=Command failed)。已改`tools.media.audio`明確指定完整路徑`/opt/homebrew/bin/whisper`+已快取的base模型(避開PATH解析與模型下載逾時兩個嫌疑根因)+120秒逾時。無法自己模擬真實LINE語音webhook，待教練或任一會員實際傳一句語音給「教練都在想什麼」驗證是否真的修好。commit `e3608229` |
| 🟡 | **真誠分會／真愛分會／真AI分會＋大台南南區網站**（⚠️2026-07-31名稱更正：原記錄「真實AI分會」錯誤，教練親口澄清正式名稱是「真AI分會」，該分會尚未在BNI Connect登記） | ⏳待教練回覆5項細節 | 連續v72起多棒未開始，2026-07-29(v87)教練終於給細節：兩個參考網址(bnidahan.com.tw／bni-tainan.com/Training-Program)+要求BNI標準色系。已產出**兩份完整HTML版型草稿**(色系實測抓自兩參考站真實CSS`#A22026`)：真誠分會(比照bnidahan結構：參訪須知/核心價值/分會之光)、大台南南區(比照bni-tainan結構：轄下分會/培訓計畫/最新消息)，三分會共用同一套版型套版。教練Comet預覽後確認「方向正確」，交棒給Mac接手，詳見v87。**卡住點**：等教練回覆5項細節——①參訪須知實際數字(名片張數/早餐費用/自介秒數，教練說「部分不同」但尚未給確切值) ②真愛/真AI分會各自slogan ③分會之光要不要放真實數據 ④大台南南區是否僅此三分會 ⑤各分會FB/Line連結。檔案：`knowledges/2026-07-29_bni-nantai-mockup/真誠分會_index.html`、`knowledges/2026-07-29_bni-nantai-mockup/大台南南區_index.html`(暫放knowledges，尚未建立實體GitHub repo，等內容定案後再轉正式repo)。部署位置教練已選定GitHub Pages測試稿(非Netlify正式站)。**2026-07-31查證BNI Connect CMS真實分會清單只有5個：真富/真愛/真誠/真鑫/真鑽(無真AI，因尚未登記)**，詳見下方新增項目 |
| 🟢 | **BNI Connect官方網站CMS後台操作能力驗證** | ✅2026-07-31本場完成，教練親口確認「非常棒」 | 教練登入BNI Connect後台(bniconnectglobal.com/bnicms/v3)，用`claude-in-chrome`連上教練本機真實已登入Chrome(不是Claude自己的隔離分頁，這個坑先踩過一次教練當場糾正)，確認有編輯權限：大台南南區(區域ID`12261`)+5個分會(真富25503/真愛26706/真誠18487舊&18640新/真鑫28446/真鑽12262)，可改地址/電話/聯絡人/分會頁面內容。全程DOM純文字讀取不截圖，Token消耗低。教練明確授權「以後我口頭講要改什麼，你直接去改」，發布上線前口頭提醒一聲即可，不用每欄都確認。**完整存取方法+網站ID索引已寫入記憶系統**`reference_bni_connect_cms_structure`+`project_bni_connect_backend_access_verified_2026-07-31`(commit `6acef6316`，透過`.claude/projects`記憶庫git同步三機)。**⚠️三機注意**：操作方法/網站ID三機共用，但**登入狀態是per機器**——聯想/宏碁要操作BNI網站前，教練需在那台機器的Chrome親自重新登入BNI Connect(帳密僅教練本人輸入)+確認該機器claude-in-chrome擴充功能已連線，登入後直接套用同一套方法即可，不用重新摸索。**待處理**：真誠分會有2筆重複CMS記錄(舊18487/新18640)，該CMS對分會層級無Delete/Unpublish功能，教練決定先不動，待確認正式處理管道(BNI客服或Outback Global代理商帳號) |
| 🟡 | **大台南南區「見證」頁中文化+教練親自見證** | ⏳草稿完成待教練確認發布 | 原頁面兩則英文見證(Marim/Amanda)已翻譯成中文(瑪琳/安曼達)+清空會跳到bni.com國際網站的連結。新增第三則教練親自口述的見證(BNI信任感引薦新加坡馬來西亞商機+上市公司培訓演講)，用表格排版做出「圖右文左」跟前兩則交錯呼應。**過程三次返工**：①Base64內嵌照片被CMS存檔時整個過濾掉(安全機制) ②改用CMS圖片庫網址但只有200×300小尺寸還被我拉大顯示糊掉 ③教練親自透過「瀏覽伺服器」選圖流程確認可以拿到真正原始解析度(6336×9504)網址，但同時給了寬高兩個固定數字，被BNI全站CSS只限制寬不限制高，拉變形，教練當場抓到糾正，已改成只給寬度讓高度自動跟隨比例，數據驗證比例0.667完全吻合原始檔案。**目前狀態**：三則見證都在草稿，尚未按Publish正式上線，等教練最終確認。Preview網址：`bnicms/v3/preview/bnitainan.com.tw/zh-TW/testimonials`(需教練登入態) |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩58次(2026-07-29，ai-talk-tw活動回顧頁部署後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
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

# 軍師接力棒 · 2026-07-29 v87（聯想Windows Sonnet 5，BNI大台南南區＋真誠分會網站版型規劃，教練交棒給Mac）

> 建立時間：2026-07-29（台灣時間）
> 本棒執行者：聯想Windows桌面版 Sonnet 5
> 上一棒：v86（Mac桌面版Sonnet5，AI微型論壇台南場正式登場：現場緊急支援+LINE綁定bug修復+活動轉型回顧頁）
> 本棒主軸：**開工六步驟後，教練交辦卡了多棒的「真誠/真愛/真實AI分會願景說明書」——這次終於給了具體參考：bnidahan.com.tw（教練心目中理想範例）+bni-tainan.com/Training-Program（區域參考頁），要求BNI標準色系。實際瀏覽兩站抓出真實CSS色碼後，產出真誠分會＋大台南南區兩份完整HTML版型草稿，教練用Comet看過確認「方向正確」。教練接著問要不要親自逐步交代細節，軍師表態自己先動手做，但教練提醒公開網路查得到的分會資料很少，上網查詢是浪費token，直接問比較快——已改口直接列5項關鍵事實請教練回覆。教練最後決定切換到Mac電腦接手，本棒任務是把目前進度完整交棒。**

## 🎯 本場戰果

### 1. 開工六步驟＋一個當場未解的小疑點
執行六步驟時查`state/recall_index.jsonl`發現：v85接力棒寫完(7/28 19:06)後教練同晚又開新對話(20:03-20:32)，已把AI微論壇60位報名者Email整理進Gmail草稿匣(BCC保護隱私)準備寄提醒信，教練最後一句是「一會兒我就來寄信了」。開工回報時主動提出詢問是否已送出，教練當下沒回答就轉向其他任務。**事後對照Mac的v86才確認：AI微論壇7/29台南場當天已經正式辦過(見v86完整戰果)，代表這封提醒信的時效已經過去，不再是急件，純粹是個可以順口收個尾的小疑點，不影響任何現況任務。**

### 2. 🎯🎯 BNI真誠分會＋大台南南區網站版型規劃（本場主軸）
教練給定兩個參考網址，先用Browser工具實際瀏覽並用`javascript_tool`抓取頁面真實computed style，取得BNI品牌色實測值：bnidahan.com.tw主色`rgb(162,32,38)`≈`#A22026`、bni-tainan.com主色`rgb(145,14,20)`≈`#910E14`，確認BNI標準色系是深酒紅色系，非憑印象猜測。

**版型設計邏輯**：
- **真誠分會**（單一分會品牌站，比照bnidahan.com.tw結構）：Header導覽(認識分會/特色團隊/會員名錄/分會之光/活動)→Hero+「預約參訪」CTA→參訪須知4卡(正式服裝/50張名片/20秒自介/早餐Buffet，文字沿用bnidahan原文，教練已表示部分數字要改但尚未給確切值)→核心價值(Givers Gain)→分會之光(示意數據待填)→Footer社群連結
- **大台南南區**（區域總站，比照bni-tainan.com/Training-Program結構）：Header導覽(認識BNI/轄下分會/培訓計畫/最新消息)→滿版酒紅色Hero→轄下分會卡片(真誠/真愛/真實AI，此區為延伸設計，原站沒有因為它是單分會頁)→培訓計畫卡片(MSP/成功藍圖/引薦/帶來賓)→最新消息列表→Footer

先用`mcp__visualize__show_widget`做過一版精簡wireframe給教練看方向，教練確認「方向正確」後，因教練說「你至少要跳HTML出來給我看吧」，改用這台機器既有SOP（`feedback_html_preview_chrome_only`：聯想這台Chrome會跳空白頁，改用Comet）——寫出兩份**完整靜態HTML**(非簡化widget版，含真實CSS排版/hover效果/Noto Sans TC字型)存到`D:\Users\Desktop\`，用`comet.exe`跳出兩個視窗給教練看，教練確認滿意。

**教練釐清協作模式**：教練問「你要自己先動手做，還是我一步一步跟你說？」，軍師表態自己先動手做（守則#12拒絕當資訊搬運工），原打算上網查真誠/真愛/真實AI分會有沒有公開資料可引用，**教練當場糾正**：「網路上可以公開查詢的資訊不多，直接問我比較快」——BNI分會資料屬於內部/私有性質，本來就不是WebSearch查得到的範疇，已改為直接列出5項需要教練親自提供的關鍵事實(參訪須知數字/真愛與真實AI分會slogan/分會之光是否放真實數據/大台南南區轄下分會範圍/各分會FB與Line連結)。

**部署位置**：教練確認先放GitHub Pages測試稿(非Netlify正式站)，已放進`knowledges/2026-07-29_bni-nantai-mockup/`(注意：github_repos/整個資料夾被.gitignore排除，每個子資料夾其實是獨立GitHub repo，不能直接放草稿進去，這是本場才發現的真規則，暫放knowledges等內容定案後再由Mac建立實體GitHub repo)。

### 3. 🎯 Chrome新使用者資料夾位置（快速問答）
教練問Chrome新增使用者的User Data會落在C槽還是E槽，查證這台機器`C:\Users\bymyw\AppData\Local\Google\Chrome\User Data`本身是Junction指向`E:\Claude-Data\AppData\Chrome-User-Data`，回答新增的Profile會落在E槽（因為整個User Data資料夾早就搬家了）。

## 📋 下一場（Mac）直接開工任務

- **🟡 主線**：等教練回覆5項BNI網站細節後，把`knowledges/2026-07-29_bni-nantai-mockup/`兩份草稿的佔位內容(黃色提示條標記處)換成真實資料，並產出真愛分會/真實AI分會兩個套版版本，之後視教練指示建立實體GitHub repo+開Pages
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，已多場未動手，優先度持續最高）
- 順手可問一句：AI微論壇那封60位BCC提醒信Gmail草稿後來寄了嗎（非急件，見上方戰果1說明）
- 嘉義場籌備（見v86，教練尚未給細節）

## 🔑 本場關鍵檔案索引
- `knowledges/2026-07-29_bni-nantai-mockup/真誠分會_index.html`：真誠分會版型草稿(比照bnidahan.com.tw)
- `knowledges/2026-07-29_bni-nantai-mockup/大台南南區_index.html`：大台南南區版型草稿(比照bni-tainan.com/Training-Program)
- `D:\Users\Desktop\bni_真誠分會_mockup.html`、`D:\Users\Desktop\bni_大台南南區_mockup.html`：教練Comet驗收用的桌面副本(與repo版內容相同)
- 本場無commit（版型草稿存於knowledges，尚未有正式commit對應的獨立repo）

---

# 軍師接力棒 · 2026-07-29 v86（Mac桌面版 Sonnet 5，AI微型論壇台南場正式登場：現場緊急支援+LINE綁定bug修復+活動轉型回顧頁）

> 建立時間：2026-07-29 下午～深夜（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v85（Mac桌面版Sonnet5，抽獎轉盤上線+付款連結批次更新）
> 本棒主軸：**v85做好的抽獎轉盤在7/29當天正式上場，本場處理三件事：①教練人在別台電腦要現場登入/wheel，密碼是雜湊值無法提供明文，改幫教練重設成他指定的新密碼並實測登入成功②活動結束後教練發現56位簽到只有12位完成LINE綁定，查證抓到真正原因是/checkin這條路徑沒有像線上報名表單那樣幫來賓「打好問候語草稿」，當場修復③教練提出要仿照全球健康發展協會(northern-tw.netlify.app)的做法，把已結束的活動頁轉型成歷史紀錄，用教練提供的24張現場真實照片做成活動花絮，同時記錄下一場預計辦在嘉義。**

## 🎯 本場戰果

### 1. 🔴🔴 現場緊急支援：教練異地登入密碼重設
教練在別台電腦要用`/wheel`轉盤功能，但登入密碼只存了scrypt雜湊值，技術上無法逆推明文。教練直接指定新密碼`123457`，用`werkzeug.security.generate_password_hash`生成新雜湊值寫入`.env`，重啟`com.coach.event-webapp`服務，並用真實的`POST /admin/login`+session cookie完整測試登入到`/wheel`成功(非test client模擬)，才回報教練帳密可用。全程沒有經手明文密碼被輸入到任何第三方系統，只是更新自己維護系統的密碼設定。

### 2. 🔴🔴🔴 抓到LINE綁定率低的真正原因並修復：`/checkin`少了「幫來賓打好問候語草稿」這一步
教練回報：56位透過現場手機號碼簽到、參與抽獎的來賓，只有12位完成LINE綁定(後續無法收到通知)。查證發現LINE綁定機制要求來賓在LINE手動輸入固定格式文字「我是OOO，剛報名了XXX」，webhook才會寫入`line_user_id`。比對兩條路徑：`/e/<slug>/thanks`(線上事先填表單的人看到的頁面)早就有`greet_url`自動把這句問候語預填好，來賓只要按「加好友」就一鍵送出；但`/checkin`(手機比對簽到)導向的`/slides`頁面，只給了一個普通的「加好友」按鈕，來賓要自己手動輸入正確格式才能綁定——這才是今天現場56人只有12人綁定的真正原因，不是來賓不想綁，是系統少做了這一步引導。修復：`slides_landing()`在有`name`參數時比照`thanks()`同樣邏輯生成`greet_url`，測試通過(有name→智慧連結、無name→維持原本通用連結)後部署。commit在`event-signup`獨立repo內(該repo不透過workspace追蹤，改動已上線生效，未來場次現場簽到綁定率應該會明顯改善)。

### 3. 🎯🎯 AI微型論壇台南場正式轉型為活動回顧頁，仿照全球健康發展協會做法
教練參考`northern-tw.netlify.app`(全球健康發展協會論壇官網，帶「歷屆回顧」板塊)的呈現方式，要求把已結束的`ai-talk-tw.netlify.app`報名頁變成歷史紀錄，教練提供的24張現場照片(下載資料夾裡的LINE傳圖，設攤+滿場講座畫面)做成花絮。動手內容：
- 24張照片壓縮到900px寬(10MB→3.4MB)，取代原本首頁「精彩花絮」輪播的12張示意照(舊照片備份在`images/carousel_archive_previous/`不刪除)，`CAROUSEL_TOTAL`12→24
- Hero區拿掉倒數計時器+報名進度條，改成「圓滿落幕，感謝每一位到場的朋友」，對應JS(`updateCountdown`/`updateLiveCount`兩個IIFE)一併移除，避免抓不到已刪除DOM元素而報錯
- 整個「選擇你的報名方式」區塊(個人報名/企業合作兩張大卡片)直接移除
- navbar桌面版/手機版、sticky底部欄、agenda區「手刀搶免費名額」按鈕，全部從「立即報名」(`onclick="showTypeModal()"`)改成「加入LINE」(直接連`line.me`)，不再觸發已經不合時宜的報名彈窗
- signup區塊改寫成「下一場預告：嘉義場籌備中」
- 本機Chrome預覽經教練確認後部署，curl驗證文字/圖片Content-Type/舊CTA清除，全部通過。GitHub commit `78213ed`，Netlify部署`6a6a1a24`，quota扣1次(59→58)

## 📋 下一場直接開工任務
- **嘉義場籌備**：教練已提到下一場預計辦在嘉義，尚未給任何細節(時間/地點/講師)，下一場教練給了細節後可以直接比照台南場經驗開工，不用重新摸索
- **Email自動發送系統**：v85記錄的方向，教練仍未給細節，下一場先問清楚用途(報表/自動回信/行銷群發)再評估技術方案
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，已多場未動手，優先度持續最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）

## 🔑 本場關鍵檔案索引
- `event-signup/.env`：`EVENT_ADMIN_PASSWORD_HASH`更新為教練指定新密碼的雜湊值
- `event-signup/app.py`：`slides_landing()`新增`greet_url`智慧預填問候語邏輯
- `github_repos/ai-talk/index.html`：Hero區/gallery/signup/navbar全面改寫成回顧版語氣，移除報名相關區塊與JS
- `github_repos/ai-talk/images/carousel/`：24張真實花絮照(取代舊12張，舊版存於`carousel_archive_previous/`)
- `state/netlify_deploy_quota.json`：本場2次部署紀錄(贊助人清單+活動回顧頁)
- commit序列（workspace repo）：`f268d7039`起延續v85抽獎轉盤 → `86ace9420`(quota記錄回顧頁部署)
- commit序列（github_repos/ai-talk獨立repo）：`cdcdf0c`(贊助人12/13) → `78213ed`(活動回顧頁轉型)

---

# 軍師接力棒 · 2026-07-28 v85（Mac桌面版 Sonnet 5，抽獎轉盤上線+付款連結批次更新+新任務登記）

> 建立時間：2026-07-28 下午～晚間（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v84（Mac桌面版Sonnet5，AI微型論壇籌備衝刺：簽到系統重構+多站更新）
> 本棒主軸：**教練開場交辦結繩領導學工作坊4站付款連結批次更新(從Google表單/pse.is短網址統一換成PayUNi直連)，接著教練提出想法：看到一個現成轉盤小程式，希望串接event-signup簽到系統做成現場抽獎工具，省去人工輸入名單。當場評估可行性後動手做，過程中連續處理教練多輪細節回饋(HTML預覽跳出方式/瀏覽器ERR_UNSAFE_PORT/獎品庫存追蹤/中獎彈窗戲劇效果/趣味台詞)，其中最重要的一次糾正是「15秒輪詢查簽到名單」又踩到教練已經講過4次的「事件驅動優於輪詢」同一個坑，這是第5次發作，已修正為「按旋轉鍵當下才查詢」並更新對應記憶檔強化教訓。收工前教練提出下一個任務方向「Email自動發送系統」，先記錄不動手。**

## 🎯 本場戰果

### 1. 🎯🎯 結繩領導學工作坊4站付款連結批次換成PayUNi直連
教練給定台南/台中/台北3組新付款連結，起初是Netlify轉址短網址(pse.is)，過程中教練發現pse.is
轉址頁顯示的「讀者優惠日期」是舊資訊，要求改用PayUNi的`receive_info`直連網址(3組長網址)。
範圍先問清楚(教練指定workshop-richard/workshop-lavi/workshop-peipei三站要換，加上原本
已上線pse.is版本的workshop-invite一併更新成PayUNi版，bni-invite/bni-peipei兩站不動)，
再問清楚3個新連結對應台南/台中/台北的順序(照原順序)。本機Chrome預覽經教練確認後4站分次
部署(間隔40秒避免token鎖定)，部署後curl驗證新連結生效+舊連結清除+圖片Content-Type正常。
順手更新`ai-talk-tw.netlify.app`贊助人清單新增第12/13位(教練指定)並補上1-13編號。
Netlify quota同步扣5次部署(64→59)。commit `f03d356cf`(4站PayUNi連結)、`7f7225a5d`
(贊助人清單)。

### 2. 🔴🔴🔴 event-signup新增抽獎轉盤(/wheel)：簽到名單自動帶入+獎品庫存追蹤
教練提出構想：有一個現成轉盤小程式(`tourmaline-panda-82be5e.netlify.app`，GitHub自動部署型，
直接clone原始碼比教練貼過來省token)，想串接既有數位簽到系統，簽到的人自動成為轉盤名單，
省去人工輸入。評估可行性後直接動手：
- `schema.sql`新增`wheel_winners`(記錄本場中獎者防重複抽中)、`wheel_prizes`(獎品清單+
  總數/剩餘數)兩張表
- `app.py`新增`/wheel`(頁面)、`/wheel/data`、`/wheel/winner`、`/wheel/reset`、
  `/wheel/prizes/set`路由，沿用`/admin`既有session登入保護
- `wheel.html`：canvas手繪轉盤(邏輯取自tourmaline-panda)，名單改為即時查詢簽到記錄
  (不用手動輸入)；「本輪獎項」從自由輸入文字改成下拉選單(顯示剩餘數量)，抽中自動扣庫存，
  發完自動從選單消失；新增「設定獎品清單」小工具(教練自己隨時用文字框增減獎項，不用碰程式碼)；
  中獎彈窗放大到72px字體+彈跳動畫，戲劇效果更強；15句趣味中獎台詞(教練給4個梗：樂透/閃電/
  相親一次中/驗孕棒兩條槓，延伸創作到15句隨機播放)
- 已幫教練把明天正式獎品清單建進資料庫：雲朵包1、下午茶組3、迷你水杯5、杯套3、洗髮組1、
  手工皂1，共14份
- 用Flask test_client完整測試全流程(抓名單/標記中獎/防重複中獎/扣庫存/庫存0時擋掉/
  重置復原庫存+名單)，全部通過，測試資料已清空不影響明天正式使用

**過程中的教訓**：
- **教練要求「你要直接跳出來給我」**——不要叫教練自己切視窗/自己打網址驗證，AI能自我驗證的
  就自己做完再回報，這次改用Flask test_client模擬登入session產生真實資料的靜態快照，
  用真正Google Chrome開給教練看(內建無頭瀏覽器截圖只能自己除錯用，不能取代教練親眼看)
- **ERR_UNSAFE_PORT**：教練連`127.0.0.1:5060`出現「無法連上」，一開始誤判是網路問題，
  查證後發現是瀏覽器對SIP協議常用埠(5060等)內建安全黑名單直接擋掉，跟服務本身是否正常
  無關。已寫入`reference_browser_unsafe_port_5060`記憶檔，以後架本機測試服務要避開這類埠號
- **🔴🔴🔴 15秒輪詢，第5次踩「事件驅動優於輪詢」同一個坑**：第一版設計成前端JS每15秒
  `setInterval`自動查詢有沒有新簽到，教練直接點破「一場活動四五個小時要掃描多少次，浪費
  資源」，並指出這是重複提醒很多次的問題。改法是教練親自提出的：把查詢動作掛在「按下開始
  旋轉」這個使用者操作的當下才做一次，完全不需要背景計時器。已更新
  `feedback_event_driven_not_polling_pattern`記憶檔，明確記錄「前端UI的setInterval跟後端
  排程輪詢是同一個坑，不分前後端」，避免下次又用「這是前端dashboard常見寫法」自我說服

commit序列：`aae07796f`(新增/wheel功能主體) → 中獎彈窗放大+移除輪詢改按需查詢(尚未commit，
下一動作立即補上) → `543ca4ec3`(15句趣味台詞)。

### 3. 🔴🔒 瀏覽器不安全埠攔截升級成確定性Hook(不只是記憶)
教練要求：「不要每次都要我說『記得跳HTML』然後結果無法顯示網頁，把它寫進SOP。」新增
PreToolUse hook `scripts/unsafe_port_check.sh`：偵測`open -a "Google Chrome"`/`start chrome`
真的執行指向本機黑名單埠(如5060)時直接攔截，提醒改用對外網址或換安全埠。第一版寫完立刻
自打臉——commit訊息描述這支hook自己時同時含有觸發文字，被自己誤判攔下2次，修正後仿照
`netlify_deploy_guard.sh`加白名單+要求真實指令位置才算數，6種情境測試通過。已註冊進
`~/.claude/settings.json`。commit `cb3ff2c12`。

### 4. 🎯 下一個任務登記：Email自動發送系統
教練收工前提出「我有下一個任務，是想要做一個email自動發送系統，你先記錄下來」——僅先記錄
方向，教練尚未說明具體用途(报表？表單提交自動回信？行銷群發？)，下一場開工先問清楚場景
再評估技術方案，不預先假設架構。

## 📋 下一場直接開工任務

- **Email自動發送系統**：教練只給了方向，還沒給細節，下一場先問清楚「要發什麼、給誰、
  什麼時候發」，用守則#16好問句工具箱釐清後再評估技術方案
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，
  已多場未動手，優先度持續最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）
- 明天(7/29) AI微型論壇現場實際使用抽獎轉盤，若教練現場回報任何問題，優先處理

## 🔑 本場關鍵檔案索引
- `event-signup/schema.sql`：新增`wheel_winners`/`wheel_prizes`兩張表
- `event-signup/db.py`：新增`get_wheel_roster`/`add_wheel_winner`/`get_wheel_prizes`/
  `set_wheel_prizes`/`decrement_wheel_prize`/`clear_wheel_winners`(含復原庫存)
- `event-signup/app.py`：新增`/wheel`、`/wheel/data`、`/wheel/winner`、`/wheel/reset`、
  `/wheel/prizes/set`
- `event-signup/templates/wheel.html`：轉盤主頁面，獎品下拉選單+設定小工具+中獎動畫+
  15句趣味台詞
- `github_repos/ai-talk/index.html`：贊助人清單12/13編號
- `state/netlify_deploy_quota.json`：本場5次部署紀錄
- commit序列：`f03d356cf`(PayUNi連結) → `7f7225a5d`(贊助人清單) → `aae07796f`(轉盤獎品庫存) →
  `543ca4ec3`(趣味台詞)

---

# 軍師接力棒 · 2026-07-28 v84（Mac桌面版 Sonnet 5，AI微型論壇7/29籌備衝刺：簽到系統重構+多站內容更新）

> 建立時間：2026-07-27 深夜～07-28 上午（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v83（Mac桌面版Sonnet5，系統權限缺口解決+開工額度瘦身）
> 本棒主軸：**教練密集為7/29「AI微型論壇」籌備做最後衝刺，本場處理6件獨立任務，多數當場教練實測/確認後結案。核心戰果是event-signup簽到系統重構——教練發現來賓線上報名後現場掃碼還要重填資料，設計出「手機號碼比對」新流程，免重填又保留集點功能，教練親自實測通過。另完成bymyway.com/ai/品牌頁三輪內容改版、event.bymyway.com場次資料校正、ai-talk-tw.netlify.app兩次數據更新(甜點份額、報名人數)、OCR通用工具教練驗收確認採用。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 event-signup簽到系統重構：手機號碼比對，免重填資料又保留集點功能
教練指出`event.bymyway.com/qr/checkin-print.html`(現場簽到QR立牌)的問題：來賓在`bigtree-tw`/`ai-talk-tw`網站報名時已留過姓名/電話，現場掃碼進`/checkin`卻要整份表單重填一次，多此一舉。過程分三階段收斂：
1. 第一版直接把QR改指向`/slides`(加好友+下載簡報，零輸入)，但教練指出這樣會失去「集滿5次活動送禮物」的簽到紀錄功能
2. 教練提出「我的紙本簽到表本來就有手機號碼」的思路，追問是否還需要數位輸入
3. 最終定案：`/checkin`拆成GET(手機輸入頁)+POST(比對邏輯)——輸入手機號碼比對`attendees`表，比對成功記進`signups`表(集點功能保留)+導向`/slides`顯示個人化「OOO，簽到成功」；查無資料的現場臨時來賓才導去完整表單(手機號碼已預填，只需補姓名)。用真實資料(已知電話/未知電話/格式錯誤)三種情境本機測試通過，教練實測確認採用。commit序列：`fd480212a`→`022051eba`→`0ef5ee98a`。7/29立牌已印好，QR網址沒變不用重印。

### 2. 🎯🎯 bymyway.com/ai/ 品牌頁三輪內容改版
GitHub Pages(`coach1973.github.io/bymyway-website/ai.html`)透過iframe嵌入`bymyway.com/ai/`。教練分三輪交辦：①案例清單新增「大樹小講．無話不談」、移除「AI特助案例集」「特助心法專屬頁面」兩項舊連結 ②CTA區塊文字簡化為「真實案例公開上線」，按鈕改連`coach1973.github.io/coach-case4/` ③新增「近期活動」按鈕連到大樹小講。每次改動都先用Chrome本機預覽給教練看過才推，commit `f8a7a89`，GitHub Pages約1分鐘內自動生效。

### 3. 🎯 event.bymyway.com/admin 場次資料校正
教練告知8/1場次已取消，改為8/26、9/5、9/19三場，比對`bigtree-tw.netlify.app`線上場次資料(topic/時段/地點)校正到`event.db`。確認8/1場次0人報名可安全刪除，三個新場次的`/e/<slug>`報名頁curl驗證正常顯示。同時回答教練「綁定/未綁定」判斷邏輯的疑問——查證LINE webhook原始碼確認：綁定要求來賓傳送固定格式文字「我是OOO，剛報名了」，webhook只處理`message.type=="text"`，**單純傳貼圖/表情符號不會觸發綁定**(教練原本以為表情符號算數，已當場更正)。

### 4. 🎯 ai-talk-tw.netlify.app 兩次數據更新
①甜點下午茶限量份數60→50份(兩處：入門禮段落+煦多午茶設攤卡片同步)，commit `52ff47a`；②已報名人數重新校準為88、遞增速率從「每6小時+1人」改「每3小時+2人」(教練回報現場報名超過88位)，commit `16d72b4`。部署前發現本機GitHub工作稿落後聯想機4個commit(缺現場設攤廠商卡片)，先`git pull`同步再改，避免蓋掉別台機器的成果。兩次都用Chrome本機預覽+curl驗證文字/圖片Content-Type後才推，Netlify quota紀錄同步更新(`state/netlify_deploy_quota.json`)，目前剩64次。

### 5. 🎯 OCR通用工具教練驗收+使用範圍界定
教練詢問建置OCR工具的原始動機，查證`reference_namecard_ocr_pipeline_reusable`記憶檔確認源頭(教練親自讀截圖時看錯陳慧雯→陳薏雯的真實案例)後準確回答。教練確認「之後讀圖片文字改用OCR」的方向，本場也順手釐清使用界線：**讀字→用OCR；看畫面(排版/設計判斷)→AI還是要自己看**，避免教練誤以為所有圖片任務都能靠OCR繞過。

## 📋 下一場直接開工任務

教練本場結束時表示「有新的Netlify的更新要做」，**但尚未說明具體內容**——會開新對話框交辦，下一場先問教練這次要更新哪個站、改什麼，不用預先假設。另外仍有queue中的舊任務：
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，多場未動手，優先度最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）

## 🔑 本場關鍵檔案索引
- `event-signup/app.py`：`/checkin`拆GET+POST、`/slides`新增`name`參數個人化、`/e/<slug>`支援`phone`預填
- `event-signup/templates/checkin.html`：新模板，單一手機號碼欄位
- `event-signup/make_qr.py`：`make_checkin()`新增`event_label`參數
- `github_repos/bymyway-website/ai.html`：案例清單+CTA三輪改版
- `github_repos/ai-talk/index.html`：甜點份數+報名人數公式
- `state/netlify_deploy_quota.json`：本場3次部署紀錄(ai-talk-tw×3)
- commit序列：`f8a7a89`(bymyway.com/ai) → `52ff47a`(甜點份數) → `fd480212a`→`022051eba`→`0ef5ee98a`(簽到系統) → `16d72b4`(報名人數)

---

> 📦 **v83及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v83_archived_2026-07-30.md`（v83單獨一份）+ `handoff_archive/handoff_v82_archived_2026-07-28.md`（v82單獨一份）+ `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`（v72~v81）
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新3棒(v86/v85/v84)在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。
