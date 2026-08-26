# 軍師接力棒 · 2026-08-25 v132（Mac桌面版 Sonnet 5，Q1「總結」功能上線+context-overflow-guard改版+賈維斯標籤+VPS全面體檢升級）

> 建立時間：2026-08-25 13:06 ~ 22:12（台灣時間，長場）
> 上一棒：v131（同機同日下午）
> 本棒主軸：**教練交辦Q1（小龍蝦總結功能）並全程授權「你是賈維斯，你決定」；下午教練回報Telegram出現一連串矛盾訊息，深入診斷後發現是小龍蝦自己編造假監控機制（非真實hook/cron），改版既有context-overflow-guard根治；教練要求區分「AI講的話」跟「系統自動發的話」，全機加賈維斯標籤；最後教練要求「全面看VPS」，完成一次真正的升級+修復+清理。**

## 🎯 本場戰果

### 1. ✅ Q1：小龍蝦「總結」功能上線（v130交辦，commit `9d1866e7`）
新建`hooks/session-summary-trigger`：教練對小龍蝦說「總結」→蒸餾存檔(`sync-telegram-memory.sh --force`)+標記待清空+直發Telegram確認，不依賴模型配合(inject是fire-and-forget)。同時修好`do_clear_sessions()`對已被sqlite取代的`auth-profiles.json`缺乏容錯的既有小bug。順手處理教練指示：terminal-watchdog確認停用(已在disabled資料夾)、孔大哥/佩佩老師人設備份(kong/peipei獨立git repo，已commit本地，但push卡在遠端分支結構混亂——kong遠端跟workspace共用`mac-openclaw-workflows`同一repo但branch衝突，peipei完全沒設遠端，**尚未解決，留待下一棒**)。

### 2. 🔴🔴🔴 深度診斷：下午context輪數混亂事件，真相是小龍蝦自己編造假機制
教練貼出下午跟小龍蝦的完整對話記錄，問「賈維斯等級的思考，是否全面深入了解問題」。查證`dialog_round_counter.json`後發現**沒有任何hook/cron讀寫這個檔案**——小龍蝦當下只是口頭承諾建機制，實際上是自己心算輪數+編訊息（82%/3MB/4MB三個數字互相矛盾、4MB上限系統裡根本不存在），並非任何真實系統故障。同場也確認：我自己早上建的session-summary-trigger完全沒有觸發這場混亂（log證實13:50教練說「總結」時這支hook完全沒反應——因為真實訊息body有信封包裝`[Telegram coach id:...] coach: 內容`，我的觸發判斷沒剝掉信封，已修復commit`187a0f7b`）。

### 3. 🎯 賈維斯決策：context-overflow-guard改版，取代小龍蝦的假機制（commit `20a63d33`）
教練說「你是賈維斯，你決定」，改版既有hook：門檻從20/30/38改成教練指定的30/50/80/100；新增判斷只計教練本人真人訊息，排除heartbeat輪詢(3166次/天等級雜訊)/排程提醒/其他群組訊息；四個門檻都直發Telegram，統一引導教練說「總結」跟Q1功能形成完整閉環。12案例測試全過。`dialog_round_counter.json`標記停用留存查證。

### 4. 🔧 教練要求：AI講的話跟系統自動發的話要分清楚，全機加「賈維斯」標籤
教練舉報名系統官方通知為例，要求程式自動發的Telegram訊息要標明來源。全機盤點後統一加「🤖【賈維斯自動通知】」：`notify_coach.sh`統一出口(涵蓋7支cron呼叫者)+今日新建/改版的2支hook+既有3支hook(line-url-typo-guard/namecard-inbound/invoice-inbound)+2支現行排程腳本(junshi_task_worker.sh/vps_polling_healthcheck.sh)。commit `d889ac5c`(outer)+`faf4b0f95`(workspace)。

### 5. 🔴 教訓：自己的測試腳本沒mock網路呼叫，重跑測試真的轟炸教練Telegram
教練回報連續收到8則一模一樣的「收到總結」訊息，查log發現是我剛才重跑`test_session_summary_trigger_hook.js`造成的真實發送——這支測試從建立起就沒攔截Telegram API呼叫，今天重跑3次(建功能/修bug/驗證標籤)，只有第一次有提醒教練，後兩次忘記說明。已修復加上跟`test_context_overflow_guard_hook.js`同款的https攔截，commit`9279d6b4`。

### 6. 🎯🎯 VPS全面體檢+修正（教練問「有需要修正嗎，例如升級」）
- **OpenClaw升級**：2026.6.11→2026.6.34，用`--tag`明確版本號避開`openclaw@latest`會橫向跳線到不同release line(2026.7.1-2)的陷阱（跟Mac評估6.34時的警告同一個坑，VPS再次驗證）
- apt系統套件更新29項(含3項安全更新)，SSH自動重啟仍正常
- Docker清理：舊image 1.3GB + 孤兒volume 7GB(教練「OK」明確授權後執行，>1GB門檻不自主執行)
- 移除沒在用的防火牆規則(8080)
- **VPS git自主備份修復**：35天沒推送(最後commit 7/20)，根因是Docker更新後觸發git「dubious ownership」安全機制導致所有push靜默失敗。補commit 65個累積異動+merge遠端(SOUL.md衝突，查證遠端版本自己標記deprecated，保留VPS本地活躍版本)+成功推送，commit`1595638fb`
- 清理5月舊備份檔(330MB，教練授權後執行)
- 發現未處理：SSH偏鬆(PermitRootLogin+密碼登入+無fail2ban，教練裁示「不用管」)、VPS repo也缺.gitignore(50MB瀏覽器快取被誤commit，下次補)

## 📋 下一場開工先做
1. **kong/peipei備份仍未真正推上雲端**：kong遠端跟workspace repo共用`mac-openclaw-workflows`但branch衝突(都想用類似main的名字)，peipei完全沒設遠端——需要決定是開新repo還是換分支名，本地commit已安全但未離線備份
2. Q1「總結」功能尚未比照做給佩佩老師的巴哈助理(記憶架構跟小龍蝦不同，需另外評估)
3. VPS repo補`.gitignore`(清掉50MB瀏覽器快取誤commit)
4. 承接v131：等朋友確認AI微論壇台中場RWD修復、Netlify額度下次校正約09-01~09-04
5. 承接舊待辦：3支孤兒hook要不要啟用、bni-chapters「真誠分會」架構問題

## 🔑 本場commit
`9d1866e7`(Q1總結hook)／`187a0f7b`(信封格式bug修復)／`20a63d33`(context-overflow-guard改版)／`d889ac5c`+`faf4b0f95`(賈維斯標籤)／`9279d6b4`(測試腳本mock修復)／VPS `1595638fb`(35天備份救回)

---

# 軍師接力棒 · 2026-08-26 v133（Mac桌面版 Sonnet 5，名片系統從私有工具擴建成完整產業鏈媒合CRM）

> 建立時間：2026-08-25 21:20 ~ 2026-08-26 00:07（台灣時間，長場）
> 上一棒：v132（同機前一日）
> 本棒主軸：**戰報系統小修正後，教練提出名片辨識系統(namecard-db)要做成賈維斯級的產業鏈媒合工具，從「內部私有搜尋頁」一路擴建成公開上傳+AI產業鏈媒合+跟進CRM+BNI會員標記+多名片自動裁切的完整系統，過程多次因教練實測回饋而返工修正，是真正落地可用的成果。**

## 🎯 本場戰果

### 0. 結繩領導學戰報小修正（commit`73d5f902b`）
戰報卡片只留現役台北場，台南場資料保留但改列「歷史記錄」連結不刪除；台北損益平衡13→11人。已用Flask test_client驗證（密碼是公司統編，AI不碰，改注入session測試）。

### 1. 名片系統公開上傳（commit`2a1d0b052`）
既有`namecard-db`只是教練/孔大哥/佩佩老師從Amber私有雲丟照片的內部工具，`namecard.bymyway.com`早有tunnel但無登入保護。新增`/upload`路由複用既有PaddleOCR+MiniMax辨識管線，任何人都能上傳、辨識完直接收錄進同一資料庫。**過程中查出這個正式launchd服務(`com.coach.namecard-webapp`)長期缺少`ANTHROPIC_API_KEY`等環境變數**（plist只設NAMECARD_FOLDER/PORT，之前搜尋頁不呼叫AI才沒被發現），改用`source .env`模式修復。

### 2. 產業鏈動態媒合系統（commit`7eed628ba`）
教練提出完整願景：「大家一起貢獻名片，AI給精準的產業鏈媒合建議」，並給了三份素材——BNI官方533項專業清單(教練用Gemini提取，存於Downloads)、大台南南區AI小幫手既有的「682+產業全生態戰略總庫」(`industry_database.md`)、兩張教練提供的產業鏈範例圖(真誠產業圖九宮格/珠寶業產業鍊同心圓)。整合成905項標準分類詞庫(`build_taxonomy.py`→`taxonomy.json`)取代原本AI自由發揮的category文字。新建`chain_matcher.py`：AI判斷新名片能否補進現有產業鏈缺口，或建議組一條新產業鏈。**教練實測後兩度糾正修正**：①媒合角色太少(只有2-4個)，要求「至少8個」(九宮格規模)，改prompt+加重試機制修復LLM隨機性偶爾漏給角色的bug，重跑全部22張全數達標(commit`f13d50e24`) ②BNI會員狀態標記原本設計錯掛在「AI建議的抽象待招募缺口」上，教練點破「沒有聯絡資料標了也聯絡不到人，沒意義」，改掛在cards表(已有真實姓名電話的名片)身上，登入才能標記(commit`e005b4f41`)。

### 3. 團隊登入+跟進紀錄簿+編輯/刪除
簡單帳密登入(`/team/login`)：**教練帳號`bymyway`/`123457`**、佩君老師`0988004118`/`88888`，教練明訂「其他成員一律用手機號碼當帳號、預設密碼88888」，下次教練給名單直接照此模式建(`create_team_member.py`)。跟進紀錄簿(`/card/<id>/follow`)：階段(待邀約/已邀約/跟進中/已合作/婉拒/暫緩)+聯絡歷程。編輯(`/card/<id>/edit`)讓教練手動修正AI認錯的字(同音異字問題，如邱莉儒/邱立儒、鄧力瑋/鄧立偉)；「未辨識」(status=failed)名片可一鍵刪除。教練規則：上傳/查詢媒合完全公開不設限，但跟進/編輯/刪除/BNI標記需要登入。

### 4. 上傳體驗優化：非同步+多名片自動裁切+圖片本機化
- **非同步上傳**(commit`20048ed43`)：教練要求「不追求立即辨識，後台慢慢消化」，拿掉5張上限，`/upload`存檔即回應，`subprocess`非阻塞觸發`process_pending.py`背景worker逐張處理（事件觸發不是輪詢）
- **一張照片拍多張名片自動裁切**(commit`d7cde90a0`，本場壓軸)：教練要求一次拍6~8張名片提升效率。實測確認MiniMax-M3有vision能力且邊界框判斷準確，新建`card_splitter.py`：AI視覺分析一張照片裡有幾張名片+各自邊界框，2張以上自動裁切成獨立圖片各自辨識+媒合。整合進`/upload`背景worker跟`watch_and_extract.py`(Amber監看)兩個入口，原始合照留`status='split'`佔位記錄避免重複偵測、但不算真實名片不會顯示在首頁。用真實4合1名片合照端到端驗證：自動偵測4張、裁切、逐一辨識全部正確，`watch_and_extract.py`版本還額外驗證了dedup機制正確合併重複名片。
- **圖片本機化+HEIC顯示修復+救回遺失圖片**(commit`82a099280`)：Amber私有雲SMB沒掛載時舊照片完全看不到，19張既有照片複製進`team_uploads/`不再依賴即時掛載。教練回報首頁多筆名片顯示不出來，查證是兩個根因：HEIC格式瀏覽器無法原生顯示(改即時轉JPEG+快取)；4筆記錄的圖檔案從未真正存在(在Amber資料夾找到同編號的原始合照，確認是4張名片拼貼照片，重新照內容裁切救回)。

### 5. 架構認知釐清
教練問「上傳的名片存在bymyway.com官網還是Mac裡」——誠實說明`namecard.bymyway.com`只是Cloudflare Tunnel把網域導向Mac mini本機，資料(照片+SQLite)完全存在本機`namecard-db/`目錄，沒有雲端備份。教練同時表態**以後不再透過Amber私有雲上傳，改用`/upload`網頁直接丟照片**（更有效率），Amber路徑保留但預期使用頻率會降低。

## ⚠️ 本場教訓
1. **不要把用戶標記類功能設計掛在AI生成的抽象概念上**——BNI會員狀態一開始掛在「AI建議但沒有真人對應的待招募角色」，教練一句「沒有聯絡資料你聯絡不到人，標了也沒意義」點破設計錯誤。任何「人工標記/跟進」類功能，都要先確認掛載對象是「有實體資料可用」的東西，不是AI憑空想像的佔位符。
2. **AI視覺(vision)能做的事比想像中更多**——測試前以為要用OpenCV等傳統CV演算法做多名片邊界偵測，一測發現MiniMax-M3直接餵圖片就能準確回傳邊界框比例座標，比手動裁切還精準。遇到「偵測物件位置」類需求，先測試現有多模態模型能不能直接做，不用急著上傳統CV方案。
3. **正式launchd服務環境變數要跟.env來源一致**——namecard-webapp長期缺少API金鑰環境變數卻沒被發現，因為舊功能(純搜尋)不需要呼叫AI。新增會呼叫AI的路由前，先確認正式服務process的環境變數是否完整，不能只在自己的bash session裡source .env測試就當作正式環境也正常。

## 📋 下一場開工先做
1. 5筆name/company為None的needs_review名片，教練可能會陸續用`/edit`修正或詢問進度
2. 教練說會陸續提供其他團隊成員手機號碼，直接用`create_team_member.py`建帳號(手機號碼當username+預設密碼88888)
3. 承接v132：kong/peipei備份未推上雲端、Q1功能未比照給佩佩老師、VPS repo補.gitignore
4. 承接舊待辦：3支孤兒hook要不要啟用、bni-chapters「真誠分會」架構問題

## 🔑 本場commit（namecard-db，依時間序）
`73d5f902b`(戰報系統)／`2a1d0b052`(公開上傳)／`7eed628ba`(產業鏈媒合初版)／`20048ed43`(非同步上傳+媒合按鈕+照片本機化)／`f13d50e24`(產業鏈至少8角色+編輯刪除)／`e005b4f41`(BNI標記改掛名片本身)／`82a099280`(HEIC轉檔+救回遺失圖片)／`d7cde90a0`(多名片自動裁切)

---

