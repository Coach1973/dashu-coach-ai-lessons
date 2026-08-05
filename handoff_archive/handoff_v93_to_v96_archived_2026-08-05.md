# 軍師接力棒 · 2026-08-05 v96（Mac終端機 Opus 5，大樹小講金門場次+歷史紀錄宮格牆改版+健康檢查cron假警報修復）

> 建立時間：2026-08-05 上午（台灣時間）
> 本棒執行者：Mac 終端機 Opus 5
> 上一棒：v95（Mac終端機Opus5，三項待辦清理+AI微論壇嘉義場上線與LINE預覽修復，與本棒同日不同session並行）
> 本棒主軸：**教練口述新增大樹小講(bigtree-tw)金門場兩場次，過程中補了教練口誤的地名（查WebSearch官方資料更正）；接著教練要求把「講座歷史紀錄頁」從一場一張大圖直式捲動改版成一眼看到總場次的宮格牆，做完本機預覽給教練確認後推上正式站。最後教練回報「小龍蝦老是出現奇怪訊息」，查證是每30分鐘健康檢查cron因AI供應商暫時過載連錯5場觸發假警報（送達時其實已自行恢復），教練當場糾正「不影響工作就別吵我」，已重寫該cron的判斷邏輯為三關判定並實跑驗證有效。**

## 🎯 本場戰果

### 1. 🎯 大樹小講(bigtree-tw)新增金門兩場次
教練口述「8月21日週五金門場西浦頭社區晚上7點半到9點」+「8月22日週六下午1點半到4點半」，後續補充「主題都叫零基礎學AI，起步比較快」+糾正第二場地名為「向陽吉第社區」（教練口誤「吉弟」，WebSearch查金門縣政府/金門日報官方資料確認正式用字並告知教練已更正）。順手把站上既有3場同主題但寫法不一致（無逗號無空格）的舊資料統一成教練這次的寫法。GitHub commit `620ca09`+`d567976`+`4262ea8`。

### 2. 🎯🎯 歷史講座紀錄頁改版為4×4宮格牆
教練要求「不需要完整呈現照片，一眼看到這裡面有幾場活動，每一場再點進去看」。改版重點：頂部大字場次計數（資料筆數自動算，不用手改）、EDM海報裁成正方形卡片（桌機4欄/手機2欄，hover上浮+微放大）、點擊彈窗看完整未裁切海報+完整資訊+原始網頁按鈕（無網頁的場次按鈕自動隱藏）。16場資料抽成EVENTS陣列，日後新增一場只要加一筆。本機預覽經教練確認「沒問題可以推了」後，走部署SOP推上正式站(deploy`6a72a1b619a971632cad6833`，額度53→52)，curl驗證文字/圖片Content-Type皆正常。

### 3. 🔴🔴🔴 健康檢查cron假警報根因修復：從「看歷史連錯幾次」改成「三關判定」
教練貼出Telegram收到的健康檢查告警，查證發現`🦞每30分鐘任務健康檢查`(jobId`46e67e2e`)08:00~10:30連錯5場，錯誤全是`FailoverError: AI service temporarily overloaded`(minimax provider暫時過載)，觸發舊規則「連續錯誤≥3必announce教練」——但**送出警報的那一輪執行本身其實已經成功**，等於教練收到一則「早就解決」的假警報。教練當場糾正：「像這種事情就不要跟我報告了，因為根本不影響我的工作。不正常的時候，再來跟我報告。真的是浪費我的注意力。」

用`openclaw cron edit --message`把規則#4改版為v4.0，announce前必須連過三關：①**現在還壞著嗎**（本輪執行成功=已恢復的鐵證，不能只看歷史連錯次數）②**是不是provider暫時過載**（`overloaded`/`FailoverError`字眼→教練無法介入，通知無意義，除非持續超過2小時仍未恢復）③**真的影響工作嗎**（健康檢查機器人檢查自己的meta迴圈不算）。改完用`openclaw cron run --wait`**實際強制執行驗證**（非紙上談兵）：同款「已恢復+provider過載+不影響工作」情境下，新邏輯正確判定「三關全未通過」，系統紀錄確認`delivered:false`，證明不會再對同類情況發假警報。已寫入記憶`feedback_alert_only_when_actually_broken`（監控類通知的通用設計原則，非僅此一個cron適用）。

## 📋 下一場直接開工任務
- bigtree-tw金門兩場已上線，若教練後續有更明確的主題（目前沿用「零基礎學AI，起步比較快」），可再更新
- v95遺留：紀律移植計劃階段二觀察期到2026-08-12；AI微論壇嘉義場行銷網址記得用`?v=2`
- BNI真誠/真愛/真AI分會網站、Email自動發送系統：仍卡在等教練給細節
- bni-chapters 10組帳號仍是預設密碼Admin/88888，教練尚未裁示是否/何時要求改密碼

## 🔑 本場關鍵檔案索引
- `github_repos/bigtree/index.html`：SESSION_DATES新增金門2場+SLOTS新增「夜」「下午」時段+場地顯示條件放寬
- `github_repos/bigtree/archive/大樹小講_歷史講座紀錄.html`：整頁重寫為EVENTS陣列驅動的宮格牆
- `state/netlify_deploy_quota.json`：額度記錄至剩52次
- openclaw cron `46e67e2e-6332-4589-aae2-ee7e10dd7279`（🦞每30分鐘任務健康檢查）：payload.message改版v4.0
- 記憶新增：`feedback_alert_only_when_actually_broken`
- commit（bigtree獨立repo）：`620ca09`→`d567976`→`4262ea8`
- commit（workspace main）：本場收工時產生（見下方commit hash）

---

# 軍師接力棒 · 2026-08-05 v95（Mac終端機 Opus 5，三項待辦清理+AI微論壇嘉義場上線與LINE預覽修復）

> 建立時間：2026-08-05 上午（台灣時間）
> 本棒執行者：Mac 終端機 Opus 5
> 上一棒：v94（Mac終端機Sonnet5，BNI大台南南區bni-chapters系統對外開通+一整場密集功能迭代）
> 本棒主軸：**開工時教練直接點名三項上一棒留下的待辦（ai-go雙入口/plugins.allow白名單/紀律移植階段二），全部查證後才動手——其中兩項發現實際狀況比接力棒記錄的更嚴重或方向錯誤，沒有照抄舊建議直接做。三項做完後教練把焦點轉到AI微論壇嘉義場：先問「推了嗎」發現還卡在GitHub預覽沒推正式站，教練說「推」後照SOP走完部署上線；隨後教練實測發現LINE分享預覽仍顯示台南場舊內容，查出真根因是全站從未設過og:標籤；教練接著要求比照AI百人導師mentor100幫講師補外部連結，一次性做完三件事二次部署；最後教練問有沒有更快的方法繞過LINE快取，查證確認官方工具已停用、`?v=`參數是唯一解法。整場貫穿「教練點頭前先查證，不照舊記錄或直覺動手」的節奏。**

## 🎯 本場戰果

### 1. 🔴🔴 ai-go bymyway.com空白頁修復 + plugins.allow白名單——兩項都推翻了接力棒原本的說法/建議
教練指名三項待辦「直接動手」。**ai-go**：接力棒記錄是「雙入口不同步」，實際查WordPress修訂紀錄發現是**整頁被清空、空白了6週**（revision 27392 於2026-06-25內容變成0字元）。新增`sync_ai_go_to_bymyway.py`就地修復（原有部署腳本是新建draft，會產生重複頁面）。**plugins.allow**：接力棒建議只列7個外掛，查原始碼發現這是「全域嚴格白名單」不是「只管非內建外掛」——照做會把另外41個（telegram/browser/duckduckgo等）全部關掉，跟案例56 toolsBySender誤傷cron同一種形狀的坑。改用程式化取自`plugins list`的48個實際載入外掛ID，重啟驗證數量一致、六個通道（3 LINE+3 Telegram）全部正常。已寫入記憶`reference_openclaw_plugins_allow_strict_whitelist`避免其他機器重蹈覆轍。

### 2. 🎯🎯 小龍蝦紀律移植計劃階段二上線 + 教練當場追加E08官方文本版
三條規則（E09 cron驗證/E12記憶寫入/E08引用查證）進`hooks/rule-reminder/handler.js`，全部`scope:['main']`只對教練自己的小龍蝦生效，新增`test_scope.js`18項測試全過。教練接著問「開放給BNI小幫手什麼功能」，查證小幫手權限後回報：E09/E12在那邊沒有對象（會員身分被擋掉exec/fs/cron），只有E08有意義。教練當場糾正「這不用問，我的原始設定本來就要求官方條文一字不差回答，這是必須的」——查證`agents/bni_tainan/AGENTS.md`確認教練說的規範真的寫死在裡面（模式B Official Text Mode、總政策19條「不得節錄」），立刻新增「E08官方文本版」開放給`bni_tainan`+`jiaolian_thoughts`，不等原訂的一週觀察期。

### 3. 🎯🎯🎯 AI微論壇嘉義場推上Netlify正式站，過程中修好LINE分享預覽卡台南場舊內容的根因
教練問「AI微論壇推上去了嗎」，查證發現只推了GitHub Pages供講師預覽，正式站`ai-talk-tw.netlify.app`還是台南場舊版。走完部署SOP（本機預覽+開Chrome給教練看+教練說「推」）後第一次部署上線。教練隨即實測貼到LINE，發現預覽仍顯示「台南場」——查了20個歷史commit確認這頁**從來沒有過`og:`標籤**，LINE只能退而求其次去猜`<title>`且會把結果快取住，換內容不換網址不會重讀。同時教練要求比照AI百人導師（mentor100）幫四位講師簡介補上FB/IG/官網等外部連結，從`mentor100.db`撈出四位講師既有填寫的連結（季哥2條/洪詠清6條/林韋銘4條/大樹教練7條，大樹教練填的IG欄位其實是這個網站自己、屬自我指涉未收錄已告知教練），比照mentor100的`openBio`模式做成彈窗按鈕。三件事（og標籤16條+活動正名「AI微型論壇」→「AI微論壇」12處+講師連結）合併成第二次部署一次推上去。教練問有沒有更快的方法清LINE快取，查證LINE官方除錯工具Page Poker已停用（DNS查無此網域），確認`?v=`參數是唯一可行的繞過法，教練往後行銷網址統一改貼`ai-talk-tw.netlify.app/?v=2`。

## 📋 下一場直接開工任務
- 紀律移植計劃階段二（E09/E12僅main）觀察期到2026-08-12，期間看`rule-reminder-probe.log`確認無誤觸發
- AI微論壇嘉義場已上線，教練近期要開始行銷，網址記得用`?v=2`版本；已分享出去的舊訊息（若有）需教練自行刪除重貼才會更新預覽
- BNI真誠/真愛/真AI分會網站、Email自動發送系統：仍卡在等教練，多場未更新

## 🔑 本場關鍵檔案索引
- `projects/bymyway-bridge/examples/sync_ai_go_to_bymyway.py`：新增，ai-go就地同步腳本
- `openclaw.json`（外層master）：新增`plugins.allow`48個外掛ID
- `hooks/rule-reminder/handler.js`＋`test_scope.js`：新增scope機制+E09/E12/E08(軍師版)+E08官方文本版
- `github_repos/ai-talk/index.html`：og:標籤16條+活動正名12處+四位講師`data-links`
- `state/netlify_deploy_quota.json`：額度記錄至剩52次
- commit（workspace main）：`92eaaaa0e`→`8b7e7dde`（外層master）→`fe86890a`（外層master）→`d04241a4`（外層master）→`839748623`→`1c10d92bf`
- commit（ai-talk獨立repo）：`45090d8`

---

# 軍師接力棒 · 2026-08-04 v94（Mac終端機 Sonnet 5，BNI大台南南區bni-chapters系統對外開通+一整場密集功能迭代）

> 建立時間：2026-08-03 深夜～2026-08-05 凌晨（台灣時間，跨整場對話）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v93（Mac桌面版Sonnet5，AI微型論壇嘉義場網站build完成）
> 本棒主軸：**教練要求把「大台南南區的總表」跟「後台系統」網址列出來加進coach888，查證後發現這套`bni-chapters`系統（教練另一個對話框8/1建置，這場對話之前完全不知道它存在）從未對外開通過，只能本機存取。開通網址只是起點，接下來教練一路密集加需求：BNI官方9大核心價值、常用連結彈窗、六項傳統與道德規範、響應式設計、參訪須知線上/實體分流——幾乎每一輪都是教練看完成果後立刻提出下一個優化方向，屬於「邊做邊定案」的密集迭代型任務。過程中犯了兩個值得記住的錯：①測試表單時漏填欄位誤清空真誠分會的Hero文字（當場查seed.py救回）②用`status`(正式營運/籌備中)欄位去猜「線上/實體」分類，猜錯了，教練糾正2次才拿到正確名單，兩條教訓都已寫入記憶。**

## 🎯 本場戰果

### 1. 🎯🎯 bni-chapters系統對外開通：申請chapters.bymyway.com，途中修好過期的cloudflared憑證
查證發現系統本身運作正常（Flask+SQLite，9個分會：真誠/真AI籌備會/真富/真愛/真鑫/真鑽/真功夫籌備會/真樂齡籌備會/真貴籌備會），但從未申請公開網址。比照mentor100/namecard既有模式建立新tunnel時，發現這台Mac的cloudflared憑證(cert.pem)已過期，連`tunnel list`都被拒。教練提醒「你可以操控我的瀏覽器，為什麼要我來點」，改用`claude-in-chrome`直接在教練真實登入的Chrome裡完成Cloudflare的網域選擇+Authorize按鈕點擊，不再請教練自己操作（見[[feedback_use_chrome_control_for_oauth_flows]]）。成功後建立`bni-chapters-app`tunnel+DNS route+`com.coach.bni-chapters-tunnel`launchd常駐，coach888新增第13/14項連結，commit `a3c7cad`。

### 2. 🎯🎯 核心價值卡片：從零散佔位文字→BNI官方9大價值(中英對照+2條隱藏版)+懸浮質感
先用bnidahan.com.tw官網逐字抓7大核心價值灌入9分會（取代每分會原本1~2條零散佔位文字），教練接著要求視覺升級（立體懸浮hover效果，滑鼠移過去上浮+陰影加深），並提供BNI官方定義全文+英文對照+2條「隱藏版」（感恩Gratitude、謙遜Humility，共9條）。`db.py`的`MAX_VALUES`從3一路調整到9。教練後來發現後台仍顯示過期的「已達上限3項」提示文字（我改常數但漏改寫死的UI文字），順勢做了更根本的決定：核心價值是官方固定內容，後台不該讓分會自行增刪，改成唯讀顯示，並移除對應的新增/刪除後端路由（不只藏按鈕，連API都關閉）。commit序列：`98277ac`→`5e64b84`→`62fd1f1`。

### 3. 🎯🎯 常用連結彈窗+六項傳統與道德規範：三次改版才定案
教練要求新增「常用連結」功能，歷經多輪調整：①一開始是導覽列文字連結→教練要求改成漢堡圖示按鈕(☰)②內容從3項(紅綠燈看板/LINE AI小幫手/培訓行事曆)擴充到教練陸續提供的11項(加6個BNI教育資源：1則FB貼文+4支YouTube+1集Podcast，YouTube標題用oEmbed API自動抓取真實標題，不用教練自己打字)。「六項傳統與道德規範」則獨立經歷3次改版：常用連結彈窗裡的文字區塊→教練嫌不夠正式改成獨立雙欄彈窗→最終定案為「分會之光」下方的**永久展示區塊**（不用點擊），並加上`chapters.show_traditions`欄位讓每個分會自己勾選顯示/隱藏（跟既有「分會之光」的條件式顯示邏輯一致）。同場也把整站做成**響應式**：手機版隱藏文字導覽只留Logo(可點回首頁)+漢堡圖示常用連結按鈕+CTA。commit序列：`66819cf`→`18296cc`→`b7fe3e9`。

### 4. 🔴🔴 差點犯的錯：測試表單POST漏填欄位，誤清空真誠分會Hero文字
測試「顯示/隱藏傳統區塊」勾選框功能時，用curl送出一個只填3、4個欄位的POST，忘記`update_chapter()`是整批覆寫語意——沒送的欄位被存成空字串，真誠分會的Hero標題/說明/參訪須知標題說明/頁尾標語全部被清空。當場發現+從`seed.py`原始種子資料查回正確內容補救，沒有造成永久損失，但已寫入教訓：測試「整批覆寫」型表單前一定要先讀出完整既有資料再送出，見[[feedback_test_form_post_read_before_write]]。

### 5. 🔴🔴🔴 參訪須知線上/實體分流：用status欄位猜分類，猜錯2次
教練要求「參訪須知」依線上分會/實體分會顯示不同內容（線上免出席費，實體650元+永康桂田酒店地址+Google地圖連結）。第一版偷懶用系統既有的`status`欄位(active正式營運/forming籌備中)去猜對應關係，結果**真誠分會、真愛分會雖是active但其實是線上分會，真功夫/真樂齡籌備會雖是forming但其實是實體分會**，教練逐一糾正2次才拿到正確名單：**線上**=真誠/真AI籌備會/真愛/真貴籌備會，**實體**=真富/真鑫/真鑽/真功夫籌備會/真樂齡籌備會。教訓：不能拿「看起來相關」的既有欄位去推論教練沒明講的新分類，見[[feedback_dont_infer_unrelated_attribute]]。最終版：實體分會5張卡(服裝/名片/自我介紹/650元/地址+Google地圖)，線上分會4張卡(ZOOM下載連結/服裝/開鏡頭/自我介紹)。commit `bc050ba`+後續資料修正(DB內容，無新commit)。

## 📋 下一場直接開工任務
- **10組bni-chapters帳號仍是預設密碼Admin/88888**：系統已對外公開，教練尚未裁示是否/何時要求各分會改密碼，下次提到這套系統應主動提醒
- 7/29的靜態mockup草稿(`knowledges/2026-07-29_bni-nantai-mockup/`)已完全過時，真正系統是`chapters.bymyway.com`，別再對著舊草稿改
- 真誠/真愛/真AI分會＋大台南南區網站(BNI Connect CMS官方版，跟bni-chapters是兩個獨立系統)、Email自動發送系統：仍卡在等教練給細節
- AI微型論壇嘉義場：仍在等講師確認後才推Netlify正式站（v93遺留）

## 🔑 本場關鍵檔案索引
- `github_repos/bni-chapters/`：app.py(移除values增刪路由)、db.py(MAX_VALUES 3→9)、schema.sql(新增show_traditions欄位)、templates/{base,chapter,admin_edit}.html、seed_bni_values_links.py(新增，可重跑的核心價值+連結種子腳本)
- `~/.cloudflared/bni-chapters-config.yml`+`~/Library/LaunchAgents/com.coach.bni-chapters-tunnel.plist`：新增
- commit序列（bni-chapters獨立repo，時間序）：`a3c7cad`(coach888新增連結，非此repo)→`98277ac`→`5e64b84`→`8022846`→`32778a0`→`66819cf`→`18296cc`→`b7fe3e9`→`62fd1f1`→`bc050ba`
- 記憶更新：[[project_bni_chapters_public_launch_2026-08-03]]（主檔，已更新到本場）、[[feedback_use_chrome_control_for_oauth_flows]]、[[feedback_test_form_post_read_before_write]]（新增）、[[feedback_dont_infer_unrelated_attribute]]（新增）

---

# 軍師接力棒 · 2026-08-04 v93（Mac桌面版 Sonnet 5，AI微型論壇嘉義場網站從零build完成，含台南場northern-tw式完整封存）

> 建立時間：2026-08-03 下午～2026-08-04 凌晨（台灣時間，跨整場對話）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v92（Mac終端機Sonnet5，龍蝦小助教LINE群組失效修復+cron權限修復+提醒功能推廣三帳號）
> 本棒主軸：**教練指示嘉義場（8/28）AI微型論壇網站籌備，這是一場從「嘉義場資料設置」到「網站正式可分享給講師預覽」的完整迭代過程，前後經歷5輪教練回饋修正。核心工作是把`github_repos/ai-talk`這個單頁網站從台南場（已結束）轉型為嘉義場（即將舉辦）為主場，同時忠實保留台南場當天的完整版面設計。過程中兩次直接查證教練提供的參考網站（northern-tw.netlify.app）的真實結構，而不是憑印象猜測，第二次查證後才發現第一版「歷屆回顧」做得太簡化，重做成忠實封存整頁設計，這是本場最大的方法論教訓。**

## 🎯 本場戰果

### 1. 🎯🎯 嘉義場完整build：從4位講師資料抓取到全站文案改寫
從mentor100資料庫（教練另一個「AI百人導師」專案）撈取洪詠清/林韋銘/季哥Eric Chi三位講師的真實簡介+照片，加上教練既有的吳大樹（大樹教練）簡介，組成4位講師陣容；議程從5大主題精簡再依教練指示加回「神秘嘉賓：中小微企業補助貸款」變回5項；hero/navbar/報名彈窗/FAQ等全站文案改為嘉義場8/28（五）14:00-17:00、再耕園404演講廳。

### 2. 🎯🎯 台南場改為northern-tw.netlify.app真實查證後的「完整封存」（非簡化摘要）
第一輪教練只說「歷屆回顧」，做了一個精簡摘要卡+輪播的版本。教練接著明確指出「我希望像northern-tw.netlify.app/#session-411一樣，完整保留7/29那天的頁面」，這次**先實際打開該網址查看真實結構**（而非猜測），確認它是把每場活動的完整版面（hero/議程/講師/花絮/贊助/FAQ）原封不動接續放在同一頁下方，不是簡化卡片。重做成完整封存區塊：所有id加`tn-`前綴避免與現役嘉義場衝突，寫python腳本驗證整份文件id全部唯一、無重複、無斷鏈錨點。

### 3. 🎯 講師卡片改點擊彈窗（比照mentor100「AI百人導師」）
教練用「AI百人導師」類比要求講師卡片點擊直接彈窗顯示完整簡介，不要下方重複介紹。查證`mentor100/templates/index.html`的`openBio(btn)`模式（data屬性+共用modal），在嘉義場現役區塊套用同款互動，台南封存區塊依教練指示保持原樣不動。

### 4. 🎯 多輪細節微調：100元園遊券制收費、100席+每天3人倒數、統一編號欄位、設攤方案定價
陸續完成：收費模式從免費改100元（可全額折抵現場攤位消費，園遊券概念）；報名人數改100席上限、以2026-08-03為基準每天+3人；報名表加「公司統一編號」選填欄位；現場設攤方案補上2000元+專屬桌+1000元園遊券贈品；洪詠清照片教練換了兩次都即時更新。

### 5. 🎯 已推GitHub Pages供講師預覽，Netlify按兵不動
教練刻意分兩階段：先只推GitHub讓講師看過確認，之後才推Netlify正式上線。查證`coach1973.github.io/ai-talk`本來就有設好的GitHub Pages（教練記得但不確定網址），curl驗證確認自動跟main分支同步。全程每次修改都用python http.server本機起服務+claude-in-chrome做真實瀏覽器驗證（DOM文字內容/圖片200載入/console無錯誤/互動功能測試），另用`open -a "Google Chrome"`開真實Chrome供教練親眼查驗，符合`web_preview_verify_guard.sh`的查證鎖要求。

## 📋 下一場直接開工任務
- **等教練確認講師看過嘉義場網站沒問題**，之後才推`ai-talk-tw.netlify.app`正式上線（目前線上還是台南場舊版）
- v92記錄的「教練15:18訊息遺失」已釐清是誤判，本場桌面版session完整收到並執行，詳見待辦表修正說明
- 其餘卡住項目（BNI真誠/真愛/真AI分會、Email自動發送系統等）本場未觸碰，狀態不變

## 🔑 本場關鍵檔案索引
- `github_repos/ai-talk/index.html`：本場唯一異動檔案，996行→1300+行
- `github_repos/ai-talk/images/speaker-{jige,hong,lin}.jpg`：新增/替換的講師照片
- commit序列（ai-talk獨立repo，時間序）：`9ea596a`（嘉義場主場轉型）→`14456e1`（地址時間+100元+神秘嘉賓+歷屆回顧初版）→`4742cff`（教練三點微調）→`d32b0dd`（設攤方案定價）→`8b0d33a`（台南場northern-tw式完整封存重做+報名倒數+統編欄位）→`04c45d7`（講師彈窗）→`1170729`（洪詠清照片第三版）
- GitHub Pages預覽：`https://coach1973.github.io/ai-talk/`
- 待推正式站：`https://ai-talk-tw.netlify.app/`（教練確認後才動作）
