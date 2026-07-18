# 軍師接力棒 · 2026-07-18 v70（Mac桌面版 Sonnet 5，cool-case頭像案完全收尾+「AI百人導師團隊」mentor100全新專案從零到正式上線）

> 建立時間：2026-07-18（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v69（Mac桌面版 Sonnet 5，peipei-art真實資料重寫+多站台bug修復，完整內容見下方精簡回顧）
> 本棒主軸：**這場對話橫跨兩天（7/17~7/18）。前半段把連續五棒沒做完的cool-case頭像重新歸類案徹底解決（含教練當場抓到的案例編號重複bug），順手修正接力棒裡「峰會」誤植為「分會」的語音辨識錯字。後半段是教練交辦的全新重大專案——「AI改變世界百人導師同行」（mentor100）：從零規劃、建置Flask+SQLite+Cloudflare Tunnel全新系統、多輪根據教練即時回饋反覆優化（連結欄位設計、自助編輯、按鈕比例bug），最終正式上線於`mentor100.bymyway.com`，並更新教練的作品一覽表**

---

## 🎯 本場戰果

### 1. 🔴🔴🔴 cool-case頭像重新歸類案——連續五棒未解決，本棒徹底完成

教練直接下令「先把這個解決了」。查出v65分析過但從未真正執行的判斷清單，逐案核對narrative/dialogue內容後執行：
- 案例5/13/16/17/18/19從誤改的「Opus 軍師」改回正確的「小龍蝦 AI 特助」
- 案例12交叉核對`memory/verbatim/2026-05.jsonl`原始對話src欄位確認為「終端機」，確認維持「Opus 軍師」無誤
- 案例7（海餅乾知識庫）原始討論記錄查出提及「教練從Gemini 3.1切到2.5」，證實很可能不是Claude系統事件，教練確認後**整個拿掉頭像與名稱標籤**，只留對話內容不掛任何AI身份

**教練順手抓到的真bug**：案例7跟案例8的`data-case`屬性各自被寫錯撞號兩次（案例一/二/三/四這4個case-card的內部編號被寫錯成8/7/1/2）。已修正回1/2/3/4，1~40不再重複，`id="caseN"`錨點本身沒錯（導航一直是對的）。

commit `ab48fd2`、`5d02831`（cool-case repo），已推上線至`coach1973.github.io/cool-case/`並逐項瀏覽器驗證。

### 2. 🔴 語音糾偏：「峰會」→「分會」

教練親口糾正：真誠/真愛/真實AI是「分會」不是「峰會」（語音輸入辨識錯誤）。已修正`JUNSHI_HANDOFF_LATEST.md`、`CLAUDE.md`兩份現行接力棒文件；歷史蒸餾逐字稿刻意不動（那是語音辨識當下的真實記錄）。新增記憶檔`feedback_fenhui_not_fenghui_voice_correction.md`避免重犯。workspace commit `0be298df5`。

### 3. 🔴🔴🔴🔴 全新專案「AI改變世界百人導師同行」（mentor100）：從零規劃到正式上線

教練交辦新專案：介紹AI百人導師團隊的公開網頁，版面參考`taiwan-marketing.com`講者資訊卡片牆風格，教練先給6-8個樣本、其餘近百位導師要能自助填表上傳。**用EnterPlanMode正式規劃**（研究了taiwan-marketing.com實際DOM結構+event-signup/peipei-event既有可複用架構），教練核准後開始實作。

**核心架構**：新建`~/github_repos/mentor100/`（GitHub私有repo`Coach1973/mentor100`），Flask+SQLite+Cloudflare Tunnel（port 5062），完全比照event-signup/peipei-event已驗證的部署模式（LaunchAgent常駐+獨立Cloudflare通道），不是靜態站。

**多輪迭代**（教練每次實測後提出真實回饋，逐一修正）：
1. 首版：卡片牆+簡介modal+單一contact_url連結欄位，種子種入7/29台南場AI微型論壇的4位真實講師（王彤/蘇秦/燒茶/大樹教練，逐字取自ai-talk網站已驗證內容）
2. 教練提問「多個連結怎麼辦、導師填錯自己怎麼改」→ 改成5個具名連結欄位+每筆資料生成專屬`edit_token`（隨機不可猜測），送出成功頁顯示自助編輯連結，導師不需登入就能改資料/換照片/整筆刪除
3. 教練指定9個連結＋固定順序（官網/FB/IG/Threads/YouTube/GJW乾淨世界/LINE/Podcast/部落格），全部改用`db.LINK_FIELDS`結構化定義，三個表單改用Jinja迴圈產生，不再手動重複9次區塊
4. 教練要求：後台密碼設為`123457`（帳號`bymyway`）、連結按鈕拿掉箭頭符號、按鈕文字要能編輯→ schema新增9組`_label`欄位，表單改成「預設隱藏label輸入框、按「修改標籤」按鈕才展開」的互動模式，已填過自訂文字的連結預設展開顯示
5. **教練截圖抓到真bug**：修改標籤按鈕比例完全顛倒（按鈕346px、網址欄位僅30px）。查證發現是頁面既有的通用`button{width:100%}`樣式污染了小按鈕，補上`width:auto; flex:0 0 auto`明確覆寫，修正後網址欄位298px（主視覺）、按鈕78px貼右側，完全符合教練要求

**正式上線**：`cloudflared tunnel create mentor100-app`+DNS route+兩個LaunchAgent（`com.coach.mentor100-webapp.plist`/`com.coach.mentor100-tunnel.plist`，比照event-webapp/event-tunnel結構），公開網址`https://mentor100.bymyway.com/`已用瀏覽器工具實測確認正常運作（首頁、/join表單、/admin後台皆200）。

**過程中自行抓到並修好的技術細節**：
- 中文檔名安全消毒＋隨機後綴防止近百人上傳同名照片互相覆蓋
- Pillow驗證圖片格式＋EXIF自動轉正＋縮圖，拒絕壞檔給友善中文提示
- honeypot隱藏欄位+每小時5次IP限流，擋機器人但不影響真人
- `.env`裡scrypt密碼雜湊值含`$`字元，用bash `source`讀取時會被誤判成shell變數展開、值被腰斬——已全面補上單引號包住，這是我自己這次新建`.env`時漏的（比對確認event-signup/peipei-event的`.env`早就有正確加引號，不受影響）
- Flask非debug模式不會自動重載樣板檔案，每次改模板都要重啟服務才會生效（教練截圖抓到比例bug時，我一開始改了CSS卻忘記重啟，浪費了一輪）

commit序列（mentor100 repo）：`c26532e`（init）→`1a26605`（緣起文案）→`ac212eb`（5個具名連結+導師自助修改刪除）→`d7880f4`（9連結固定順序）→`604395b`（按鈕觸發式標籤編輯）→`4a215b3`（比例bug修正）。

**教練提供的緣起文案**（語音口述整理）：起心動念/我們的團隊/這是一個怎樣的地方三段，說明大樹教練發起、佩君老師（佩佩老師）邀約召集、每位導師進群前深聊約1小時的理念與運作模式。

### 4. 🎯 教練作品一覽表（coach888）新增第24/25項

比照event-signup/peipei-event慣例（公開頁+後台系統各自獨立列一項），新增：
- 第24項：AI百人導師團隊（`mentor100.bymyway.com`）
- 第25項：AI百人導師後台系統（`mentor100.bymyway.com/admin`）

原本24項之後（BNI/保留區）全部順移+2，1~44連續不重複，已程式驗證無漏號無重複。commit `013ea26`。

### 5. 🎯 新增通用工具「字級大小對照表」+coach888第45項「工具箱」分類

教練指出以前每次要調字級大小，都要臨時輸出一份頁面專屬的編號字級清單（例如jiesheng-leadership那次輸出43條），改成一份**通用可重複使用**的視覺對照表（`coach1973.github.io/coach888/font-scale.html`，12px~104px每個級距都用真實繁體字渲染出實際大小），以後教練直接說「這段用32級」（=32px）就能精準溝通，不用每次重新生成頁面專屬清單。coach888新增「六、工具箱」分類、第45項。commit `ddca415`。

### 6. 🔴🔴 mentor100文案+字級全面重新設計（教練多輪即時回饋）

教練用語音重新口述整份文案（標題/副標/四段介紹文字全部改版，新增「免責聲明」段落），並指定明確字級門檻：標題48級以上、副標32級以上、段落跟標題都要「大一點」。已實作：
- 桌面版標題52px、副標34px（雙雙達標），手機版響應式縮小為38px/24px避免小螢幕過度換行
- 按鈕文字改「我要參與導師同行計劃」單行大按鈕
- 段落20px、小標題32px全面放大
- 文案改版：計劃源起段落「大樹教練與佩君老師親自深聊」改成「我們會通過線上交流」；「想加入/想離開」句子從計劃源起移到「這是一個怎樣的地方」；新增免責聲明三段
- 導師卡片牆正上方新增第二顆大按鈕「我要加入百人導師計劃」，不用捲回頁首

commit `b1b1372`，已用瀏覽器工具實測桌面版1280px寬確認字級精確達標，並用真Chrome開給教練看過。

### 7. 🔴🔴🔴 「None」字面文字污染bug——先修程式碼，再清舊資料

教練截圖回報兩個症狀：①編輯頁面空欄位自動帶入一段英文要手動刪除才能送出、②簡介按鈕顯示「None」而非FB/IG等內建名稱。逐一查證後發現是**同一個根因**：`join_edit.html`/`admin_form.html`的`value="{{ f[url_name] if f else '' }}"`只guard「f本身不存在」，沒guard「f存在但該欄位是SQL NULL」——Jinja把Python的`None`物件直接印成畫面上的字面文字「None」，這段假文字擋住了原本該顯示的placeholder提示（FB/IG/YouTube等內建名稱），也造成教練形容的「要手動刪除的英文」。

**兩層修復**：
1. 程式碼修正（commit `9c1d0ff`）：改成`(f[url_name] if f else '') or ''`雙重保險，role_tag欄位同一問題一併修掉。已直接fetch編輯頁HTML核對`value=""`不再出現任何`None`
2. **舊資料清理**（純資料庫操作，無新commit）：教練自己在bug修好「之前」編輯過「大樹教練」這筆真實資料，當時畫面上的假「None」文字被他直接送出、永久存進資料庫（FB/GJW/LINE/Podcast等6個label欄位變成字面上的字串"None"，不是NULL）。已用SQL直接把這些被污染的"None"字串換回真正的NULL，並重新驗證公開頁面上「大樹教練」卡片的簡介按鈕：官網/FB/GJW/LINE/Podcast全部正確顯示內建名稱且連結正確，教練自己改過的「大樹小講」自訂標籤也完整保留

**教訓**：Jinja對None值沒有預設安全網，任何從資料庫讀出來、可能是NULL的欄位，寫入HTML屬性前都要明確guard，不能只信任「if 物件本身存在」這一層判斷。

---

## 📋 下一棒待辦（依優先度）

| 優先 | 任務 |
|------|------|
| 🔴🔴🔴 | 教練預告的真誠分會、真愛分會、真實AI分會願景+產業分佈圖說明書——連續多棒未開始，教練還沒給細節 |
| 🔴🔴🔴 | **Netlify部署額度**——上次記錄16次（7/25前），這次mentor100走Cloudflare Tunnel、coach888/cool-case走GitHub Pages，全部沒消耗Netlify額度，下次碰Netlify站台時記得查`state/netlify_deploy_quota.json`確認最新剩餘次數 |
| 🟡 | mentor100導師自助表單目前只有基本honeypot+IP限流防濫用，近百人實際開始填表後留意有沒有真的垃圾資料湧入，若有需要加強 |
| 🟡 | 兩個小工程教訓值得正式寫進試金石：①`.env`裡含`$`字元的值（scrypt雜湊）用bash source讀取一定要單引號包住，②Jinja模板寫`value="{{ x if y else '' }}"`只guard了y本身，沒guard x可能是None，兩者都已在mentor100修好，但這個模式在其他Flask小專案(peipei-event等)若有類似寫法，值得抽空檢查一次 |
| 🟢 | ACER備份刪除已逾期（原訂7/15），需在ACER那台開對話親自執行 |

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `~/github_repos/mentor100/`（全新專案：app.py/db.py/schema.sql/templates/、.env）
- `~/.cloudflared/mentor100-config.yml`（新增tunnel設定）
- `~/Library/LaunchAgents/com.coach.mentor100-webapp.plist`、`com.coach.mentor100-tunnel.plist`（新增，常駐部署）
- `~/github_repos/cool-case/index.html`（頭像歸類修正+編號bug修正）
- `~/github_repos/coach888/index.html`（新增第24/25/45項，1~44+工具箱分類重新驗證無誤）
- `~/github_repos/coach888/font-scale.html`（新增，通用字級對照表工具）
- `JUNSHI_HANDOFF_LATEST.md`、`CLAUDE.md`（語音糾偏「分會」用詞修正）
- `~/.claude/projects/-Users-bymyway--openclaw/memory/feedback_fenhui_not_fenghui_voice_correction.md`（新增）

---

## 📜 v69 精簡回顧（Mac桌面版 Sonnet 5，完整內容見git歷史）

1. peipei-art個人品牌頁重寫成真實履歷資料版本，移除捏造內容
2. event.bymyway.com後台密碼重設+QR立牌自動/手動雙模式
3. 新功能「簡報QR」(slides-drop)：加LINE好友+領簡報+通知小龍蝦
4. coach888作品一覽表4次追加修改
5. bigtree歷史講座紀錄頁抓到「從未真正上線」的根因，重新部署
6. bymyway.com「查看完整活動列表」連結修正（先改錯repo才發現iframe真正來源）
7. ai-talk-tw.netlify.app講師頭像全滅+簡介新舊版混淆，兩個真bug都修好
8. VPS小龍蝦polling自動偵測+自動修復技術升級
9. Netlify部署額度追蹤機制建立
10. 讀了聯想試金石案例51，主動幫Mac補上同款junction查證防護

---

> Mac桌面版 Sonnet 5 親筆，2026-07-18。這場對話有兩個明顯分野：前半段是把積壓五棒的技術債（cool-case頭像案）徹底清乾淨，過程中教練當場抓到一個編號重複的真bug；後半段是從零開始的全新專案，教練用一連串真實使用後的回饋（不是憑空想像的需求）逐步把系統修到位——包括一次截圖點出的真實排版比例bug，查出根因是通用按鈕樣式污染了小按鈕。整場對話的模式很清楚：教練提出方向或抓到問題，我負責查證根因、動手修正、實際驗證（不管是重新整理瀏覽器看DOM結構、跑curl測完整流程、量測實際像素寬度），而不是憑印象回報「應該修好了」。下一棒開工第一件事，應該先確認mentor100首頁上那筆教練自己測試留下的真實資料要保留或刪除。
