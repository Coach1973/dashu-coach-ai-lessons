# 軍師接力棒 · 2026-08-31 v153（Mac終端機 Sonnet 5，mentor100通知修復+AI微論壇9/22台南場上線+BNI Connect培訓活動新任務交辦）

> 建立時間：2026-08-30 21:22 ~ 2026-08-31 13:50（台灣時間，接續v152開工，橫跨開工六步驟到教練說「總結」收工）
> 上一棒：v152（Mac終端機，同上一日，逐步脫離Netlify：4個新路由上線）
> 本棒主軸：**教練回報mentor100申請通知漏接，查證修復；AI微論壇9/22台南場網頁從零建置並依教練兩輪回饋修正上線；教練交辦下一場新任務——BNI Connect新增多種培訓活動供會員報名。**

## 🎯 本場戰果

### 1. AI百人導師(mentor100)申請通知改走Telegram，修復8/27靜默漏接
教練回報8/27有人提交申請完全沒收到Telegram通知，還誤以為對方沒提交而重複提醒，結果發現重複。查證`apply_submit()`打的是舊版LINE通道`sme-register-fn`且用`except: pass`吞掉錯誤，跟event-signup試金石案例62（報名通知LINE月配額用完靜默失敗一週）同款坑，只是發生在另一個獨立專案身上。改用event-signup已驗證過的Telegram Bot API直送方案（chat_id 6124913915），失敗必寫`notify_failures.log`。已用真實`/apply`端點提交測試驗證（無失敗log產生），測試資料已清除。commit`1b9b816`（mentor100 repo）。全機掃描`sme-register-fn`/`_notify_coach_line`確認mentor100是唯一還沒遷移的專案，event-signup裡的殘留只是註解提及歷史。記憶`project_mentor100_application_notify_telegram_fix_2026-08-30`。

### 2. 杜亞洛BNI發票查詢（唯讀，教練確認記得曾問過）
查`claude-brain/data/`兩份完成清單json，確認杜亞洛有兩張BNI相關發票皆已開立：BNI入會$39,800（custom_num 082407，宿易智能有限公司，invoice DQ92460811）+ 培訓費$600（custom_num 081925，invoice DQ92662345），皆status=done無作廢紀錄，直接回報教練無需動手。

### 3. AI微論壇9/22台南場網頁從零建置上線（`/ai-talk`repo）
教練確認9/22台南場講師到齊（凌榆舜+李明燦+教練本人），先查證：凌榆舜資料已在mentor100(id=81)，李明燦全機查無資料（mentor100/applications/inbound_echo三方向都查過），回報教練後教練裁示**李明燦取消，只留凌榆舜+教練兩人**，凌榆舜主題「品牌數位轉型與商業應用」、教練主題「零基礎學AI，起步比較快」、教練說明文字「大樹教練的演講就像浪花一樣，每次都精彩，每次都不一樣」。

場地/時間/費用查`event.db`的`bigtree-0922-day`登記資料核對：台南安平維悅酒店、200元、50席，跟教練口頭數字吻合。改寫`/ai-talk`repo的`index.html`：議程/講師陣容從嘉義場5人版換成2人版，凌榆舜簡介照片取自mentor100（複製進`images/speaker-ling.jpg`），og:/canonical改指向`event.bymyway.com/ai-talk/`，7/29台南場「歷屆回顧」封存區塊完全不動。**push時撞上git race**——另一場session同時往同一repo push了4筆嘉義場設攤廠商新增commit（含凌榆舜08/李明燦09兩個設攤卡片），`git pull --no-rebase`乾淨自動合併無衝突，已用javascript_tool直接呼叫`openSpeakerBio()`驗證講師簡介彈窗+照片載入正常，另用`open -a "Google Chrome"`實際打開驗證。commit`6dc29dc`+合併commit`cb69243`。

教練隨後三項修正：①時間改「13:30開始，16:30結束」（原誤寫「13:30進場，17:00轉場」，教練糾正「不是入場」）②取消凌榆舜、李明燦的設攤卡片（兩位仍保留其他身分，只拿掉設攤，剩餘KR廚房重編為08）③強調200元報名費是支付場地費，四處文案補上說明。全頁6處時間文字+`event.db`的`bigtree-0922-day`的`transport`欄位同步更新，已curl+開Chrome驗證。commit`f75d441`。

## ⚠️ 本場發現（未寫獨立記憶，順帶記錄）
李明燦查無speaker資料的謎題，在git pull合併後找到答案：他是另一場session加進boothes區塊的**設攤廠商**（台灣模型車博物館），不是mentor100的講師資料——兩種身分（講師 vs 設攤）是完全不同的資料模型（mentor100 DB vs 直接寫死在ai-talk HTML），彼此不互通，下次遇到類似「查無此人」先想清楚問的是哪種身分再查對應資料源。

## 📋 下一場開工先做（教練新交辦，尚未動手）
**教練指示**：進BNI Connect後台，新增大台南南區「初階MSP」「進階MSP」「季度主題培訓」「新領導團隊訓練」「領導團隊期中訓」等活動，讓會員可以在系統裡註冊/報名這些活動。
1. 先讀`reference_bni_connect_cms_structure`記憶，確認BNI Connect CMS後台的活動/培訓管理入口在哪（區域ID`12261`+5分會ID）。
2. 查證這幾種活動類型是否已有既有分類/範本可套用，還是要從零新增。
3. 確認每種活動需要的欄位（日期/時間/地點/講師/名額/費用）教練是否已有具體資料，還是要先問清楚才能建。
4. 這件事本場完全未觸及，是全新任務。

## 🚧 Hermes 接手「9/21 新領導團隊訓練」進度（卡住，已寫信問軍師）
- 教練在場下令接手，帳號「吳 大樹」已登入 BNI Connect
- 用 Hermes preview pane 操作，到表單頁 `appsEventsCreateNewEvent?countryId=7699`
- 教練已確認欄位：日期 2026-09-21、時間 9:00-12:00、形式 ZOOM、免費、不填 RTF、人數上限 100
- 軍師 SOP（`cross-agent/inbox/hermes/20260831-1450_mac-to-hermes_bni-connect-create-new-event-sop.md`）已讀，照做時踩到 3 個 SOP 沒寫的副作用
- ⚠️ 卡住的副作用：
  1. **click 活動類型下拉會清空「地區」select value**（會踩到 SOP 警告的「Select a host region」雷）
  2. **click 地區下拉會自動把「允許線上付款」改成 no 並鎖住**（免費活動剛好對，但 SOP 沒寫）
  3. **誤推論活動類型 value 660 = 領導團隊培訓**（實際是 BNI台灣會員大會，正確 value 待軍師回覆）
- 已寫信給軍師：`cross-agent/inbox/mac/20260831-1500_hermes-to-mac_bni-create-event-3-sop-gaps.md`
- 軍師 15:10 回信、3 個問題都答完（活動類型 value=2、`getDataOnRegion()` 是非同步 AJAX 等 1 秒）

## ❌ Hermes 投降：BNI Connect 後台類任務不適合 Hermes（已寫投降書）
- 照軍師 15:10 修正版順序繼續做，又撞到 4 個更深層問題：
  1. **原生 `<select>` 無法程式化選值**（type 拒絕、press 沒 ref、沒有 js / fill_input）→ 教練必須自己方向鍵選
  2. **「複製活動」型態的隱藏同步機制**（type eventName 會被同步覆蓋成活動類型名）
  3. **`getDataOnRegion()` AJAX race 不只 reset 3 個 select、連文字欄位也被 reset**
  4. **看不到真實頁面**（沒 js evaluate、沒 screenshot、read 拿不到 option 文字）
- 教練 0 按鈕鐵則（2026-06-10）對這個差距 0 容錯——至少要按 4 次方向鍵
- 跟均仕差距是**工具集結構性差距**（均仕用 Browser Use 雲端瀏覽器有 js/fill_input/screenshot，Hermes preview pane 沒有），不是模型差距
- 投降書：`cross-agent/inbox/mac/20260831-1535_hermes-to-mac_bni-task-surrender-report.md`（commit `1642a9762`）
- **教練決定**：以後 BNI Connect 這類後台任務不交給 Hermes，回歸軍師/均仕
- **Hermes 繼續負責**：改 event.db、改文案版面、查報名、寫 SOP、接力棒、讀寫類任務
- 待軍師裁示方案 A/B/C/D（其中 D「分工事」最務實）
- **教練已讓我按 2 次方向鍵**（活動類型、場所）——這條違規記進教訓，等軍師更新 SOP「Hermes 不做後台操作」明文化

## 🔑 本場commit
`mentor100`：`1b9b816`（申請通知改Telegram）。`ai-talk`：`6dc29dc`+`cb69243`（9/22台南場上線+merge）+`f75d441`（時間/設攤/場地費三項修正）。記憶：`project_mentor100_application_notify_telegram_fix_2026-08-30`。接力棒瘦身：v150封存至`handoff_archive/handoff_v150_archived_2026-08-31.md`。

---

# 軍師接力棒 · 2026-08-31 v154（Mac終端機 Sonnet 5，BNI Connect 7場培訓活動上線+Hermes任務分工裁示+試金石全面蒸餾重建）

> 建立時間：2026-08-31 13:57 ~ 15:30（台灣時間，接續v153同日開工）
> 上一棒：v153（Mac終端機，同日，mentor100通知修復+AI微論壇9/22台南場上線+BNI Connect培訓新任務交辦）
> 本棒主軸：**BNI Connect新增培訓活動任務執行完畢；Hermes嘗試接手9/21場次卡在工具集限制，裁示分工方案；教練交辦最後一項總結性任務——試金石蒸餾重建，確保系統真正吸收3個月的教訓。**

## 🎯 本場戰果

### 1. BNI Connect大台南南區7場培訓活動上線
詳見上方待辦表已更新項目。核心技術突破：發現「複製活動」表單可用`jQuery('#eventStartDate').datepicker('setDate', new Date(...))`程式化設日期、`CKEDITOR.instances['eventDetls'].setData('')`清空繼承自範本的舊描述、`submitBTN`→復審畫面→`confirmBTN`兩段式送出流程。過程中發現並修正一個內容錯誤：clone自519187的9月主題培訓沿用了舊活動「陳孟專Amber執董」的描述文字，已在送出前清空，避免發布錯誤資訊。教練事後口述9月主題培訓正確內容「領導人的溝通藝術」，已編輯上線；12月「建團隊就是做事業」內容教練尚未提供，留白。「執董與新會員有約」教練最終裁示因無培訓分整個不建。

### 2. Hermes嘗試接手9/21新領導團隊訓練，卡在工具集結構性限制，裁示分工方案D
Hermes（MiniMax-M3桌面版，desktop preview pane）依軍師SOP操作BNI Connect創建新活動表單，連續卡兩輪：第一輪3個副作用（地區/活動類型欄位互相清空、線上付款被鎖、value與顯示文字不同步待軍師回覆），軍師實測驗證後找到根因是`getDataOnRegion()`非同步AJAX會重載活動類型/聯絡人/場所三個select的選項清單，設值時機早於AJAX完成就被蓋掉；第二輪Hermes提出4個更深層問題（原生select無法程式化選值/js evaluate缺失/複製活動隱藏同步機制/AJAX race連文字欄位也重置），寫成完整投降書，誠實分析出跟軍師（Browser Use雲端瀏覽器，有js/fill_input/screenshot）的差距是**工具集結構性差距**非模型能力問題，並自己提出方案A/B/C/D四種選項。軍師裁示採Hermes建議的**方案D**：BNI Connect等需要操作原生select/需要JS的網頁後台任務轉軍師，Hermes專注讀寫類任務（改DB/文案/查詢/接力棒/SOP/蒸餾），不投資給Hermes裝雲端瀏覽器（任務頻率低，ROI不划算）。教練9/21場次最終自己手動建好(eventId 533117)，軍師已驗證資料正確。三封信往返：`cross-agent/inbox/hermes/20260831-1450`(初版SOP)+`1510`(3問題答覆)+`1520`(方案D裁示)，Hermes原信已歸檔`outbox/2026-08/`。已存記憶`project_hermes_bni_connect_task_routing_2026-08-31`。

### 3. 試金石全面蒸餾重建（教練交辦本場最後任務）
教練指示：把試金石這段時間所有犯的錯、繞的彎、讓教練生氣的地方總結，寫進系統檔案，確保永遠不會再犯，同時保留歷史存檔。查證發現真正的問題：`distill/top10_dynamic.md`與`top10_errors_index.md`自2026-05-27（案例O）後就沒再更新，但`試金石/試金石_案例庫.md`已默默長到case 67（2026-08-27），3個月、40+個案例的教訓從未被蒸餾進「快速比對層」，開工六步驟第3步也只注入「最新2案例全文」，3個月前但還沒真正解決的舊模式（例如輪詢反覆犯6次）平常不會被提醒到，只有剛好是「最新2案例」才會露出。

修復三件事：①重建`top10_errors_index.md` v2，讀完全部49案例歸納出10大高頻失敗模式（輪詢取代事件觸發累計6+次最高頻／機制看似存在實已失效／查證優先於試錯／部署SOP被跳過／危險指令防護／環境裝置確認／一字不差查證／讓教練當搬運工／交接心跳斷點／只信數字不看畫面），每個模式標註涉及案例編號+是否已有自動化防護(hook/測試)+觸發詞，改採「新案例只需在對應模式加一行索引」的低維護成本設計，避免重演v1「每案例要重寫整段觸發清單」導致3個月沒人維護的失敗模式本身。②`top10_dynamic.md`標記封存不刪除（資料處置原則：預設歷史存檔），內容完整保留供查閱舊格式紀錄。③`feed_junshi_handoff.sh`新增第3a步：開工時額外注入10大模式一句話+觸發詞摘要（awk擷取，不重複全文），跟原有3b「最新2案例全文」並存，**已用合成session_id實測跑通**（exit 0，10個模式全數正確出現，總注入量23KB仍在合理範圍，非空談）。`feed_junshi_handoff.ps1`（Windows）鏡像同步相同改動，但這台Mac無pwsh無法實測，**下次聯想/ACER開工時需驗證**（呼應案例66教訓：新機關必須用真實資料驗證過才算數）。commit`4432abb93`。

### 4. 大樹小講／近期活動類任務預設分工正式定案（教練15:26親口拍板）
教練緊接著上面的Hermes/BNI Connect分工裁示，進一步拍板：往後只要是大樹小講/近期活動這類任務，**盡可能丟給Hermes運作**，兩邊透過既有`cross-agent`信箱通訊，軍師持續給指導直到Hermes能完全接手網站活動建置。已把「這是常態預設、不只是額度用完前的備援」寫成永久協議：`cross-agent/README.md`新增「任務分工鐵律」章節（含分工範圍表+教學迴圈說明）；`projects/cards/bigtree.md`/`ai-talk.md`/`ai-forum-taichung.md`/`tainan-calender.md`加`owner:Hermes`標記，`bni-connect.md`加`owner:軍師`標記；正式發信到`cross-agent/inbox/hermes/`告知Hermes新政策+已具備的SOP手冊位置。記憶`project_hermes_default_owner_event_tasks_2026-08-31`。**教學迴圈的實際機制**：Hermes卡住寫信到`inbox/mac/`→軍師開工讀信給答案→答案同步補進SOP文件（不只回信了事）→SOP越補越完整、Hermes卡住頻率隨時間下降，這才是「教到完全能接手」的真正落地方式，不是一次性文件而已。

## ⚠️ 下一場開工先做
1. **Windows端`feed_junshi_handoff.ps1`第3a步尚未實測**，聯想或ACER下次開工時確認有無報錯、10個模式是否正確出現，有問題直接修，不要假設「跟Mac版同邏輯應該沒事」。
2. 12月「建團隊就是做事業」主題培訓內容教練尚未提供，補齊後編輯eventId 533111上線。
3. FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍——三項舊待辦本場均未觸及。
4. **下次Hermes來信到`inbox/mac/`時**，除了回答問題，記得同步把答案補進`knowledges/2026-08-31_大樹小講四場活動維運SOP_備援指令給Hermes.md`或對應專案卡，這是分工政策能否真正生效的關鍵動作。

## 🔑 本場commit
`cross-agent/inbox/hermes/`四封信：`7c8f5e6ff`+`a62b91fd5`+`e1b8a343d`+（本次任務分工政策信，下方補齊hash）。試金石蒸餾重建：`4432abb93`。記憶：`project_hermes_bni_connect_task_routing_2026-08-31`+`project_hermes_default_owner_event_tasks_2026-08-31`。

---

