# 軍師接力棒 · 2026-07-20 v71（聯想桌面版 Sonnet 5，17天同步斷線修復+tainan-calender/bigtree兩站部署+分會願景案再確認）

> 建立時間：2026-07-20（台灣時間，實際對話發生於7/19晚間~7/20凌晨）
> 本棒執行者：聯想（Windows）桌面版 Sonnet 5
> 上一棒：v70（Mac桌面版 Sonnet 5，cool-case頭像案收尾+mentor100全新專案上線，完整內容見下方精簡回顧）
> 本棒主軸：**這是聯想這台機器睽違17天後第一次真正開工。一開場教練就問「為什麼接力棒沒讀到某項目」，查證發現這台機器的workspace/mac-openclaw-workflows兩份git本地clone都嚴重落後遠端（最長落後1711個commit/17天），當場拉齊修復。過程中釐清教練口述的「真誠峰會/真愛峰會/真實AI峰會」其實語音辨識該聽成「分會」（跟Mac那邊教練同一天糾正的內容一致，雙邊各自獨立記錄後互相印證）。接著處理教練連續交辦的兩個實際網站任務：tainan-calender.netlify.app改場次日期、bigtree-tw歷史紀錄頁新增4場活動+診斷修復圖片下載過慢問題+線上座談會系列補連結。過程中一度只用App內建無頭瀏覽器驗證HTML就想回報完成，被教練當場點破「沒有跳HTML出來給我看」，立刻改用Comet補做**

---

## 🎯 本場戰果

### 1. 🔴🔴🔴 聯想機兩份git clone同時落後遠端17天，當場修復

教練一開場問「為什麼接力棒沒讀到『真誠分會願景說明書』、『AI百人導師團隊宣傳頁』」，先查`workspace/`（原本以為是唯一clone）發現本地main分支落後origin **1711個commit、17天**（最後一次commit停在6/30），拉齊後才在v69接力棒看到教練預告的mentor100新專案。教練繼續追問後，才發現這台機器其實還有第二份獨立clone`mac-openclaw-workflows/`，第一次`git status`顯示「up to date」是**沒重新fetch的舊快取結果**，重新fetch後其實也落後8個commit（後來因為Mac同時在寫session，落後數字持續變動，最終也拉齊）。

**教訓**：`git status`的「up to date with origin/main」只反映上次fetch時的認知，不代表當下真的最新——之後開工前一律先`git fetch`再看`git status`是否顯示behind，不能只看一次結果就下結論。已寫入`project_windows_workspace_git_sync_gap_2026-07-17.md`。

### 2. 🔴 語音糾偏再確認：「真誠分會、真愛分會、真實AI分會」

教練一開始給的說法是「真誠峰會、真愛峰會、真實AI峰會」（跟Mac那邊蒸餾記錄的錯字一致），這裡先誤判成「峰會」搜尋落空；教練澄清「語音輸入的問題，都是分會」後才對上——跟Mac同一天（7/17）獨立記錄的`feedback_fenhui_not_fenghui_voice_correction.md`完全一致，雙邊各自查證互相印證，非單一來源。這個新專案本身（三分會的願景說明書+產業分佈圖網上說明書）**仍在等教練給細節**，本棒沒有動手設計，只把命名和狀態記清楚，寫入`project_bni_three_chapters_vision_pending.md`。

### 3. 🟢 tainan-calender.netlify.app：9/21場次改9/14

BNI「1對1+引薦工作坊」場次日期異動。找到線上實際HTML（本機備份檔是4月舊版、結構完全不同，沒有拿來改），改完直接用Netlify API zip部署，curl驗證線上09/21已消失、09/14已上線，其他時間/地點/報名連結不動。這是本棒Netlify部署quota第1次。

### 4. 🔴🔴🔴 bigtree-tw歷史紀錄頁：圖片下載過慢診斷+修復+新增4場活動+線上座談會系列補連結

教練回報「圖片下載非常慢，等快兩分鐘才完全出現」。查證發現：12張活動EDM圖全部是印刷等級原圖直接上網（最大2087×2943px），畫面顯示框只有278px寬；加上沒有lazy loading，開頁就一次抓12張，總重9.3MB。

**修復**：全部16張圖（12張既有+4張新增）壓縮到符合實際顯示需要的尺寸（600~900px寬，JPEG quality 82），總重量降到2MB內；所有`<img class="edm">`加上`loading="lazy"`。

**新增4場活動**（教練提供EDM圖片，經比對下載資料夾檔名+像素尺寸+目視內容三重確認）：
- 7/18（六）九型人際策略讀書會
- 7/19（日）危機就是轉機
- 7/22（三）當古典音樂遇到AI科技——連到`bigtree-tw.netlify.app/?session=2026-07-22#signup`
- 7/29（三）AI微型論壇——連到`ai-talk-tw.netlify.app`（既有專屬頁）

**線上座談會系列補連結**（教練指示）：6/5、6/14、6/21、7/5、7/10、7/19共6場（皆為蔡曜隆先生與談的ZOOM系列）全部加「有網頁」標籤，連到`jiesheng-leadership.netlify.app`；7/18九型人際策略連到`bigtree-tw.netlify.app/?session=2026-07-18#signup`（比照7/22的深連結做法，直接對到報名卡片而非只連首頁）。

**部署流程**：先推GitHub Pages（`coach1973.github.io/bigtree/`）供教練檢視，教練用Comet實機確認後才推Netlify正式站。改用`netlify-cli deploy --prod`而非手動zip（Windows的`Compress-Archive`與.NET`ZipFile.CreateFromDirectory`都會把巢狀路徑存成反斜線，實測證實過會導致線上404，這次直接繞開）。這是本棒Netlify部署quota第2次；推送當下Mac同時在推`ai-talk-tw`，兩邊quota計數在git merge時撞上，已手動合併修正，**實際剩13次（7/25前）**。

### 5. 🔴 HTML驗收流程一度漏做，教練當場糾正

第一輪只用App內建無頭瀏覽器工具（`mcp__Claude_Browser__*`）自己驗證bigtree頁面畫面正確，就想跟教練回報「已驗證」——教練直接問「你有跳出HTML來給我看嗎？」，這是既有試金石案例46的同一個坑在聯想機重演。立刻改用`comet.exe`把畫面真的跳到教練螢幕上（聯想機指定瀏覽器，Chrome在這台會空白），之後每次要教練驗收都比照辦理，內部工具驗證跟跳瀏覽器給教練看是兩個目的不同、缺一不可的動作。

---

## 📋 下一棒待辦（依優先度）

| 優先 | 任務 |
|------|------|
| 🔴🔴🔴 | 教練預告的真誠分會、真愛分會、真實AI分會願景+產業分佈圖說明書——連續多棒未開始，教練還沒給細節，開工先問清楚身份/受眾/資料來源三件事 |
| 🔴🔴🔴 | **Netlify部署額度：剩13次（7/25前）**——每次真的觸發新deploy前先查`state/netlify_deploy_quota.json`，deploy後即時更新，若多台機器同時推要留意git merge時history陣列可能衝突，需人工核對remaining_after正確遞減 |
| 🟡 | mentor100首頁上教練自己測試留下的真實資料，v70結尾就提醒要確認保留或刪除，本棒沒碰到mentor100，順延 |
| 🟡 | mentor100導師自助表單目前只有基本honeypot+IP限流防濫用，近百人實際開始填表後留意有沒有真的垃圾資料湧入 |
| 🟡 | 兩個小工程教訓值得正式寫進試金石：①`.env`裡含`$`字元的值用bash source讀取要單引號包住，②Jinja模板`value="{{ x if y else '' }}"`要guard x可能是None（mentor100已修好，peipei-event等其他Flask小專案若有類似寫法值得抽空檢查） |
| 🟡 | Windows端打包zip給Netlify部署，一律優先用`npx netlify-cli deploy --prod --dir=... --site=... --auth=...`，不要用`Compress-Archive`或.NET`ZipFile`手動壓——兩者在Windows上都會把巢狀路徑存成反斜線，導致線上404 |
| 🟢 | ACER備份刪除已逾期（原訂7/15），需在ACER那台開對話親自執行 |

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `E:\Claude-Data\github_repos\tainan-calender\`已不再使用（線上真實內容跟本機備份早已脫節，改直接對線上curl操作）
- `E:\Claude-Data\github_repos\bigtree\archive\大樹小講_歷史講座紀錄.html`（新增4個item、6+1個連結、16張img全加lazy loading）
- `E:\Claude-Data\github_repos\bigtree\archive\edm\`（12張既有圖片壓縮、新增4張：edm_0718_jiuxing.jpg / edm_0719_weiji.jpg / edm_0722_gudian.jpg / edm_0729_luntan.jpg）
- `state/netlify_deploy_quota.json`（本棒新增2筆history，跟Mac的ai-talk-tw部署合併解衝突）
- `claude-brain/project_bni_three_chapters_vision_pending.md`（新增）
- `claude-brain/project_windows_workspace_git_sync_gap_2026-07-17.md`（新增）
- `claude-brain/MEMORY.md`（索引補上以上兩則）

---

## 📜 v70 精簡回顧（Mac桌面版 Sonnet 5，完整內容見git歷史）

1. cool-case頭像重新歸類案（連續五棒未解決）本棒徹底完成，順手修正案例7/8編號撞號bug，commit `ab48fd2`、`5d02831`
2. 語音糾偏「峰會」→「分會」，新增`feedback_fenhui_not_fenghui_voice_correction.md`
3. 全新專案「AI改變世界百人導師同行」（mentor100）從零規劃到正式上線`mentor100.bymyway.com`，Flask+SQLite+Cloudflare Tunnel，多輪根據教練即時回饋修正（9個具名連結+自助編輯+按鈕比例bug）
4. coach888作品一覽表新增第24/25項（mentor100公開頁+後台）
5. 新增通用工具「字級大小對照表」`coach888/font-scale.html`+coach888第45項「工具箱」分類
6. mentor100文案+字級全面重新設計，教練指定明確px門檻逐項達標
7. mentor100「None」字面文字污染bug：Jinja對None值沒guard，先修程式碼再清舊資料

---

> 聯想（Windows）桌面版 Sonnet 5 親筆，2026-07-20。這是聯想這台機器17天以來第一次真正開工，開場就撞上「查了半天查不到教練交辦的事」——後來發現不是教練沒講、也不是我沒查，是兩份本地git clone都嚴重落後遠端，資訊本來就傳不過來。這個教訓很直接：以後開工不能只憑「查不到」就下結論，要先確認自己手上的資料是不是新鮮的。後半場處理兩個實際網站任務時，一度犯了老毛病——只用內部除錯工具驗證畫面就想回報完成，被教練當場點破「沒跳HTML給我看」，這是試金石案例46的坑，證明「AI自己看過」跟「教練親眼看過」是兩件事，缺一不可，之後每次驗收都老實跳Comet。下一棒開工，Netlify額度只剩13次，7/25前要留意；真誠/真愛/真實AI三分會的願景說明書還在等教練給細節，不要自己腦補設計。
