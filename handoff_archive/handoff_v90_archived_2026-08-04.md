# 軍師接力棒 · 2026-08-02 v90（Mac桌面版 Sonnet 5，Mac版Web Search修復+VPS/LINE版全面盤點+bigtree高雄場部署，過程中兩次被教練抓到查證不完整）

> 建立時間：2026-08-02 深夜（台灣時間）
> 本棒執行者：Mac桌面版 Sonnet 5
> 上一棒：v89（Mac桌面版Sonnet5，ai-talk-tw輪播花絮修復+小龍蝦系統全面健檢）
> 本棒主軸：**教練發現Mac版小龍蝦（教練/孔大哥/佩佩老師）用不了Web Search、只能退而求其次用DuckDuckGo，追問原因。查證+修復完成後，教練追問VPS版跟LINE版是否也需要同樣的開關，過程中軍師連續兩次查證不完整被教練當場糾正：①沒先查`路徑大全_憑證層.md`就回報「VPS查不到」②盤點LINE版帳號時漏算沒有名稱標籤的「龍蝦小助教」，只回報兩個。教練藉此機會給出更高層的期許：軍師是整個特助系統的大總管，要自己設計方法確保「用戶說的每句話都記得住、資訊都查得全」，不是每次都靠教練提醒。已將這兩次疏失連同技術修復一併寫入試金石案例55。**

## 🎯 本場戰果

### 1. 🎯🎯 Mac版Web Search真正修復：啟用DuckDuckGo外掛+明確指定為預設provider
教練質疑「Mac本機本來就能上網，為什麼Web Search要綁死MiniMax專屬鑰匙才能用」，查證OpenClaw原始碼確認：`web_search`工具需要一個「已註冊的搜尋provider」，MiniMax原生搜尋走的是獨立於聊天Key之外的「Coding Plan」專屬鑰匙（`MINIMAX_CODE_PLAN_KEY`等），這台Mac從未申請過。但系統內建的`duckduckgo`外掛官方文件寫明「no API key required」，只是裝了沒開。執行`openclaw plugins enable duckduckgo`+`openclaw config set tools.web.search.provider duckduckgo`+`openclaw daemon restart`後，從production log直接看到真實cron任務成功用duckduckgo查到「台南天氣」的真實搜尋結果（標題/網址/摘要齊全），確認修復生效。commit `c9cc8072`。

影響範圍：`tools.web.search`是整台Mac唯一一份`openclaw.json`的全域設定，main/kong/peipei（Telegram）+bni_tainan/jiaolian_thoughts/**default（龍蝦小助教）**（LINE）五個agent同一個gateway程序，一次設定全部生效，不需要逐一開。

**過程中一個技術細節記錄**：`openclaw agent --agent main`這個CLI測試指令，即使在plugin確實生效之後，仍持續回報「web_search is disabled or no provider is available」，跟同時間production log裡真實cron任務成功的結果互相矛盾。判斷是這個CLI測試指令本身有獨立於正式gateway之外的runtime快取/隔離問題，不是修復沒生效——最終以production log的真實成功案例為準，不是以這個測試指令為準。下次要驗證web_search功能，直接查`openclaw logs`裡有沒有真實`provider: duckduckgo`成功記錄最準，不要只信`openclaw agent`測試指令。

### 2. 🔴🔴 犯錯記錄：VPS查證沒先讀路徑大全+LINE帳號盤點漏算一個（試金石案例55）
教練追問VPS/LINE版是否也需要開Web Search，軍師連續兩處查證不完整，教練當場兩次糾正，完整過程與教訓已寫入`試金石/試金石_案例庫.md`**案例55**，此處只記結論：

- **VPS真相**：用路徑大全的憑證(`sshpass -p '9kdxvQN2' ssh root@43.245.60.200`，容器名`openclaw`)連進去查證後發現，VPS的Docker容器環境變數裡本來就有`MINIMAX_API_KEY`，這把鑰匙OpenClaw原始碼裡剛好也接受當搜尋功能的備援認證，**VPS的Web Search本來就是通的**（走MiniMax原生搜尋，不是DuckDuckGo）。軍師一開始誤判VPS跟Mac同病，動手開了duckduckgo外掛並設為預設provider，事後查log發現VPS原本就有真實成功搜尋記錄，判斷是多此一舉的改動，**已撤銷（`openclaw config unset tools.web.search.provider`）+重啟容器確認恢復原狀+VPS維持健康**。結論：VPS不需要任何開關，是軍師一開始沒查證就誤判。
- **LINE帳號真相**：`channels.line.accounts`底下其實有3個key，`default`(綁main agent，龍蝦小助教，教練pairing制專屬)、`bni_tainan`(大台南南區小幫手)、`jiaolian_thoughts`(教練都在想什麼)。軍師最初只點名了有名稱標籤的後兩個，教練糾正後補上第三個。三者都在Mac同一gateway程序，Web Search修復已一併覆蓋全部三個。

### 3. 🎯 教練期許：軍師是特助系統大總管，要自行設計「查得全、記得住」的方法
教練在指出兩次疏失後，明確拉高格局：「你是所有資訊的大總管，是我們整個特助系統的軍師，所以你自己要想辦法完善……用你的邏輯跟系統去完成。」這不是單一任務的糾正，而是對「頂級特助如何自我要求」的期許——已寫入試金石案例55的「悟到什麼」段落，核心是兩條可執行的自我檢查動作：①任何「查不到/做不到」結論說出口前，先確認有沒有查過該環境的萬用索引檔（這台Mac是路徑大全）②任何「盤點/列舉」類任務，直接對著底層資料結構（JSON物件的key數量）逐一點名核對，不能只挑印象中顯眼的幾筆。

### 4. 🎯 bigtree-tw（大樹小講）8/26場次補上「高雄場」標籤，已部署
教練指定`github_repos/bigtree/index.html`裡`SESSION_DATES`陣列8/26那筆（主題「當古典音樂遇到AI科技」，跟7/22同系列）補上`location:'高雄場'`。改完先用Node.js把JS陣列eval出來驗證語法正確、14筆場次都能正常解析，再依鐵律用Google Chrome開本機檔案給教練親眼確認，教練回覆「推」後，走完整Netlify部署SOP（zip整個bigtree資料夾當下狀態+API上傳，NETLIFY_DEPLOY_CONFIRMED=1通過部署鎖），部署後直接curl正式網址`bigtree-tw.netlify.app/index.html`確認高雄場字樣真的在線上。bigtree repo commit `a3d9118`，Netlify部署id`6a6f68a82e9e8c51e42e8852`。**注意**：這個部署是整個bigtree資料夾（含子目錄`biz-gym`）一起打包上傳（歷史上此站點一直是這樣部署，`biz-gym`是同一個Netlify站台底下的子路徑），`biz-gym/index.html`目前在git裡有未commit的黑金改版WIP異動（[[project_bizgym_blackgold_redesign_2026-07-04]]），這次部署只commit了`index.html`（大樹小講本體），`biz-gym`的WIP異動未commit但已隨資料夾現況一起上線，如教練之後發現biz-gym頁面跟預期不同，是本場部署的已知副作用，非新bug。

教練接著問「這個月還有幾次可以推」，已更新`state/netlify_deploy_quota.json`（57→56，主要credit pool剩約60次@8/25到期、備用pool剩約4次無到期日），commit `fc74ddf72`（workspace）。

### 5. 🔍 教練詢問信用卡USD $10.49每月扣款來源，查證多輪未能確認商家，待教練回撥銀行進一步調查
教練發現去年11/30起每月被扣USD $10.49（無商店名稱、來源美國，帳單只有授權碼），懷疑是忘記取消的訂閱。**已窮盡目前能查的免密碼管道，皆未命中**：Gmail全信箱歷史搜尋（含seabiscuitclub@gmail.com舊信箱，教練已在瀏覽器登入親自查過）、所有Stripe代收商家收據逐筆核對金額、Google Play訂閱清單（無有效訂閱）、Apple ID訂閱清單（5筆有效訂閱皆核對過金額，無吻合）。教練已回撥銀行一次，客服僅能查到商家在舊金山，無法問出更多細節。**下一步建議教練本人操作**（AI已無更多免密碼查證管道）：①要求銀行做正式交易爭議調查（非單純客服查詢，銀行需往下深挖merchant descriptor）②回想去年11/20~11/29間有無下載試用App/填過免費體驗表單（許多訂閱陷阱是試用到期轉付費，時間點吻合）。**此事本場未解決，若教練下次提起，直接從這兩條建議接續，不用重新查一遍已排除的管道。**

## 📋 下一場直接開工任務
- 沿用v89未完成事項：ai-talk-tw延遲問題需追問教練三個細節、memory自動快照卡住5小時以上待查根因、OpenClaw升級待node版本處理
- 真誠/真愛/真AI分會＋大台南南區網站：仍等教練回覆5項細節，多場未更新
- Email自動發送系統、嘉義場籌備：仍卡在等教練給細節
- 若教練之後測試Telegram/LINE任一帳號問「查資料」類問題，可順手確認Web Search回覆是否正常帶出真實網址（非硬性待辦，僅供驗證參考）
- **USD $10.49訂閱來源**：教練若回撥銀行問出商家全名，或想起11月試用過什麼App，直接接續查證，不用重查已排除的Gmail/Stripe/Google Play/Apple ID四條管道
- **bigtree/biz-gym**：教練若反映biz-gym頁面異常，先確認是否為本場部署帶出的既有WIP異動（見戰果4說明），非新bug

## 🔑 本場關鍵檔案索引
- `openclaw.json`：新增`tools.web.search`區塊（enabled+provider=duckduckgo）、`plugins.entries.duckduckgo.enabled=true`
- `試金石/試金石_案例庫.md`：新增案例55（VPS查證+LINE盤點兩次疏失完整記錄）
- commit（workspace main分支）：`c9cc8072`（Web Search修復）、`fc74ddf72`（Netlify quota更新）
- commit（bigtree repo）：`a3d9118`（8/26補高雄場）
- VPS：已連線查證+誤改後撤銷，VPS本身無任何commit異動（設定已還原）
- 路徑大全位置：`workspace/路徑大全_憑證層.md`（VPS/Hermes SSH密碼、sshpass快速連線指令）
- Netlify部署：`6a6f68a82e9e8c51e42e8852`（bigtree-tw，8/26高雄場），quota 57→56

