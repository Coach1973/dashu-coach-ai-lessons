# 接力棒封存：v157 + v158 + v159（2026-09-01封存）

> 封存原因：主檔超過3棒，依E16瘦身鐵律搬移。原內容完整保留於下方。

---

# 軍師接力棒 · 2026-09-01 v157（Mac終端機 Sonnet 5，team.bymyway.com正式部署+bni-chapters籌備會創始會員表單+BNI信用証提醒擴充兩段式）

> 建立時間：2026-09-01 02:39 ~ 04:05（台灣時間，接續v156，同場對話跨到隔日凌晨）
> 上一棒：v156（Mac終端機，ai-art完整上線接手完成+workspace git衝突查證修復+Hermes進度可見性規則）
> 本棒主軸：**team.bymyway.com（複製bni-chapters去BNI品牌的通用分會系統）教練已在另一對話框讓軍師直接做完程式並推上GitHub，本棒接手正式部署上線；bni-chapters籌備中分會補上「登記成為創始會員」真實表單+Telegram通知；BNI信用証到期提醒擴充成2個月+1個月兩段式。**

## 🎯 本場戰果

### 1. BNI信用証到期提醒擴充：2個月+1個月兩段式通知
教練交辦「當會員只剩2個月及1個月到期時，要記得通知我」。原`scripts/bni_credit_expiry_reminder.py`只有單一30天提醒點（`reminder_sent_at`發過就永久不再提醒同一筆）。新增`reminder_60d_sent_at`欄位（`namecards.db`已手動ALTER TABLE），改寫成兩個獨立里程碑：剩31~60天觸發「2個月提醒」、剩0~30天觸發「1個月提醒」，同一筆證書會各收到一次，互不影響不重複洗版同一里程碑。用合成測試資料驗證45天/20天/90天三種情境分類正確+已發送里程碑不重複觸發。既有cron(`8211e054`，每日08:57)無需異動，直接吃到新邏輯，通知一樣走`notify_coach.sh`→Telegram。commit`757854999`。

### 2. workspace git狀態查證：小龍蝦回報pull失敗，證實非真正落後雲端
小龍蝦轉達「Mac開工git pull失敗，接力棒/守則可能不是雲端最新版」。查證`git fetch`比對HEAD已包含origin/main最新commit（非落後），真因是44個routine狀態檔案長期未commit卡住fast-forward pull。已push一筆本地未上傳的commit+整批commit狀態檔案，重新驗證HEAD與origin/main完全一致。commit`15305e072`。

### 3. ai-art（v156延續）教練實測後追加票種選擇+LINE導流，已完成（詳見v156完整記錄）

### 4. team.bymyway.com通用分會系統：程式由另一場對話框軍師直接完成，本棒接手正式部署上線
**背景**：教練要做`team.bymyway.com`，服務對象是還沒加入BNI的一群朋友，複製`chapters.bymyway.com`架構但拿掉BNI LOGO，分會名稱改通用編號「第一分會、第二分會…」。軍師原本規劃分工：Hermes寫程式、軍師部署，已發信`cross-agent/inbox/hermes/`交辦（commit`5a312c940`）。但教練在**另一個對話框**直接口頭要求軍師（另一個session）動手做完程式（原話：「教練親口指示不要等Hermes」），已完成並推上GitHub（`Coach1973/team-bymyway`，commit`e9d87dc`+`173e035`，5個分會team-01~05）。透過`cross-agent/inbox/mac/`一封「mac寫給下一棒mac」的信發現這個狀況，本棒（同一個對話框的延續）確認教練意向後直接接手部署。

**部署內容**（比照bni-chapters既有模式，DNS+Tunnel+launchd三件套）：
- Cloudflare DNS：`team.bymyway.com` CNAME
- 新建獨立Tunnel `team-bymyway`（id`7bcba233-1544-49bf-b274-e5b818a6000a`），設定檔`~/.cloudflared/team-config.yml`
- 兩支launchd plist：`com.coach.team-webapp.plist`（跑`app.py`，port 5073，借用`bni-chapters/venv/`）+ `com.coach.team-tunnel.plist`
- `.env`寫入`TEAM_SECRET_KEY`（隨機32字）+`TEAM_PORT=5073`
- **部署時發現的真缺口**：`admins`表完全是空的，`/admin/login`頁面存在但沒有任何帳號能登入。已補寫`seed_admins.py`（沿用bni-chapters的Admin/88888慣例）建立總管理員+5個分會各自帳號，用真實curl POST登入流程驗證（302→帶cookie訪問`/admin`回200），commit`fd9dfb8`。
- 已curl驗證首頁200+`team-01`頁面200+5個分會名稱正確顯示+後台登入頁200，並用真實Chrome開啟確認視覺。
- `coach888`作品總覽新增此站（「四、對外公開」區塊第7項，非BNI品牌），commit`34477e4`。

**教訓**：多對話框並行時，同一個教練可能在不同視窗給不同AI實例下達會互相影響的指令（這次是「Hermes寫程式」vs「軍師直接寫程式」兩個決定疊在一起），跨機`cross-agent/inbox/mac/`信箱這次意外成為發現這個狀況的關鍵管道——下次類似情境，先查inbox有沒有「自己寫給自己下一棒」的信，可能代表另一個對話框已經動過手。

### 5. bni-chapters籌備中分會新增「登記成為創始會員」真實表單
教練指出真AI/真貴/真功夫/真樂齡等4個籌備中分會（`status='forming'`）的「登記成為創始會員」按鈕原本是死連結(`href="#"`)。新增：
- `founder_signups`資料表（schema.sql+db.py，已對live DB跑`init_db()`套用，IF NOT EXISTS安全）
- `/<slug>/founder-signup`（GET表單+POST送出）+`/<slug>/founder-signup/thanks`路由，欄位姓名/電話/Email/公司，沿用既有的honeypot+IP rate limit防灌水機制
- 送出成功即時呼叫`workspace/scripts/notify_coach.sh`推播Telegram
- `chapter.html`兩顆CTA按鈕改成：`status=='forming'`才連到新表單，正式營運分會維持原本`#`不受影響
- 用`test_client()`驗證GET表單/POST驗證錯誤(400)/POST完整送出全流程(mock通知避免真的打教練Telegram)，4個籌備會slug皆curl驗證200，測試資料已從DB清除
- commit`69670de`（bni-chapters repo）

## ⚠️ 下一場開工先做
1. **team.bymyway.com後台密碼**：跟bni-chapters一樣是預設Admin/88888，教練尚未裁示是否/何時要求改密碼，兩套系統可以一起處理。
2. **team.bymyway.com示範內容**：5個分會目前是佔位文字（第一分會~第五分會），教練可能需要進一步調整視覺風格/文案，屬於後續內容維運，可以交給Hermes做（部署已完成，接下來就是內容層面）。
3. Hermes那封「team-bymyway-new-site」交辦信（commit`5a312c940`）已經過時（程式已由軍師做完），若Hermes後續有動作或詢問，告知現況即可，不用真的做重複的事。
4. v151之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容）本場均未觸及，繼續掛著。

## 🔑 本場commit
`workspace`：`757854999`（信用証提醒兩段式）、`15305e072`（git衝突查證）、`5a312c940`（發信Hermes team交辦，已過時）、本場v157接力棒本身。`team-bymyway`：`fd9dfb8`（seed_admins.py，部署時新增）；程式本體`e9d87dc`+`173e035`為另一場對話框軍師所做，非本棒commit。`bni-chapters`：`69670de`（籌備會創始會員表單）。`coach888`：`34477e4`（作品總覽新增team.bymyway.com）。部署基礎設施：`~/.cloudflared/team-config.yml`+兩支launchd plist（非git追蹤，本機設定檔）。

---

# 軍師接力棒 · 2026-09-01 v158（Mac終端機 Sonnet 5，team.bymyway.com核心價值複製+預約參訪表單+bni-chapters分會精神新功能+PII誤commit修復）

> 建立時間：2026-09-01 04:33 ~ 05:00（台灣時間，接續v157同場對話）
> 上一棒：v157（team.bymyway.com部署上線+bni-chapters創始會員表單+信用証提醒兩段式）
> 本棒主軸：**教練親自在team.bymyway.com後台寫好第一分會9個核心價值，交辦複製到其餘4分會+「預約參訪」按鈕接上表單通知；接著要求bni-chapters真誠分會新增「分會精神」區塊（教練同一批核心價值內容）取代「分會之光」示範；過程中發現並修復一次git add -A誤commit含真實個資db備份檔的事故。**

## 🎯 本場戰果

### 1. team.bymyway.com：第一分會9個核心價值複製到第二~第五分會
教練在後台（v157修好的CRUD功能）親自寫完第一分會9個核心價值，直接SQL複製到chapter_id 2~5，5個分會皆curl驗證顯示一致。

### 2. team.bymyway.com：「預約參訪」按鈕接上真實表單+Telegram通知
不分分會狀態(forming/active)，新增`visit_signups`表+`/<slug>/visit-signup`路由(姓名/電話/Email/公司)+沿用honeypot/rate limit機制，送出即時notify_coach.sh→Telegram。5個分會按鈕皆已連上並curl驗證，test_client()全流程驗證含mock通知。commit`e477260`。

### 3. bni-chapters：新增「分會精神」區塊，先在真誠分會示範
教練要求把「分會之光」改名「分會精神」，核心價值(BNI官方9大)維持不動，分會精神放教練新寫的那9個(跟team.bymyway.com第一分會同一批內容)。設計成漸進式：新增`chapter_spirit`表，chapter.html改用「有spirit內容才顯示分會精神，否則顯示舊分會之光(chapter_stats)」的條件式渲染——真誠分會已寫入9筆自動切換，其餘8分會spirit為空維持顯示舊內容不受影響，教練確認滿意後可自行在後台複製到其他分會(已補CRUD介面)或請軍師代勞。舊chapter_stats資料完整保留未刪除。commit`a7773a7`。

### 4. 【事故修復】git add -A誤commit含真實會員個資的.db備份檔
上一個commit(`a7773a7`)用`git add -A`時，一個遺留的`chapters.db.bak-before-netlify-link-update-20260830-164330`（含7筆真實會員姓名/電話/Email）被誤commit——`.gitignore`的`*.db`規則擋不住`.db.bak-xxx`這種變體檔名。查證repo為private（`gh repo view`確認`isPrivate:true`），曝露風險有限，但立即`git rm --cached`+補`.gitignore`規則+新commit修復(`b33c327`)，本機檔案保留未刪除。已寫入記憶`feedback_git_add_a_risk_with_db_backup_files_2026-09-01`，往後在含真實個資的repo執行`git add -A`前先`git status --short`肉眼掃一眼。

## ⚠️ 下一場開工先做
1. 教練若確認真誠分會「分會精神」效果不錯，下一步是複製到其他8個分會（現在只有真誠分會有spirit資料）。
2. team.bymyway.com/bni-chapters兩套系統後台密碼仍是預設Admin/88888，教練尚未裁示改密碼時程。
3. v151之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容）本場均未觸及，繼續掛著。

## 🔑 本場commit
`team-bymyway`：`e477260`（預約參訪表單+通知）+核心價值SQL直接複製(無獨立commit，資料庫操作)。`bni-chapters`：`a7773a7`（分會精神新功能）+`b33c327`（PII誤commit修復）。`workspace`：`1c261394a`（git add -A教訓記憶）。

---

# 軍師接力棒 · 2026-09-01 v159（Mac終端機 Sonnet 5，真誠分會視覺微調兩輪+跨系統錯字修正，教練說「總結」收工）

> 建立時間：2026-09-01 05:00 ~ 05:10（台灣時間，接續v158同場對話，教練驗收後兩輪微調，最後說「總結」）
> 上一棒：v158（team.bymyway.com核心價值複製+預約參訪表單+bni-chapters分會精神+PII事故修復）
> 本棒主軸：**教練驗收v158做的「分會精神」demo後，連續給兩輪視覺微調意見；過程中教練發現一個錯字，要求橫跨兩個系統共6處內容全部修正。**

## 🎯 本場戰果

### 1. 真誠分會視覺微調第一輪
教練反饋：①核心價值區塊標題「核心價值與分會精神」是舊版遺留文案，教練覺得多餘，改回單純「BNI 核心價值」②分會精神卡片配色（紅底半透明白卡）太紅，改成整段白底、9個框框滿版紅色實心色塊、文字白色放大到16px。技術上把「分會精神」獨立拆成新的`.spirit-section`/`.spirit-card` CSS class（不再共用`.glory`），確保只影響真誠分會，不動到其他8個分會現在還在用的舊版「分會之光」樣式。commit`16920d0`（bni-chapters）。

### 2. 真誠分會視覺微調第二輪+跨系統錯字修正
教練反饋白字配紅底還是反差太大不舒服，改成金色(#D4AF37)+字級再放大(16→18px，標題18→20px)。commit`bf1ea22`（bni-chapters）。

**同時教練發現錯字**：第九條「你可以擁有的一切」內文「但別懟了」應為「但別忘了」。教練指出這份內容同一批文字被複製到多處（team-bymyway五個分會的chapter_values + bni-chapters真誠分會的chapter_spirit），要求「連同第一分會的那五個，全部都得改，因為如果這個字錯，就代表所有都錯了」——已用SQL UPDATE一次性修正全部6處（team-01~05各一筆+真誠分會chapter_spirit一筆），逐一curl驗證錯字歸零、正確文字「但別忘了」都已生效。資料庫內容修正無獨立commit（純DB操作，不進git）。

## ⚠️ 下一場開工先做
1. 真誠分會「分會精神」若教練最終確認滿意，複製到其他8個分會（bni-chapters）+若team.bymyway.com之後再有類似批次文字複製需求，記得先檢查有沒有錯字，不要複製完才發現要跑第二輪修正。
2. v151之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容）本場均未觸及，繼續掛著。
3. **教練本場提醒Context已到53%，準備換新對話框**——下一場開工先讀本棒+v157/v158，了解team.bymyway.com/bni-chapters分會精神這兩條主線的最新狀態。

## 🔑 本場commit
`bni-chapters`：`16920d0`（標題簡化+分會精神白底紅卡片）、`bf1ea22`（金色字+放大+錯字修正）。資料庫內容修正（team-bymyway 5筆+bni-chapters真誠分會1筆錯字）為直接SQL操作，無git commit（.db檔本不進版控）。

---

