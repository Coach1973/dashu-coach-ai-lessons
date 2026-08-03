# 軍師接力棒 · 2026-08-02 v89（Mac桌面版 Sonnet 5，ai-talk-tw輪播花絮修復+小龍蝦系統全面健檢：找到並修好兩個真正未被發現的bug）

> 建立時間：2026-08-02 下午～晚間（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v88（Mac桌面版Sonnet5，BNI Connect官方網站後台操作能力驗證+見證頁正式上線）
> 本棒主軸：**教練反映ai-talk-tw.netlify.app活動花絮輪播「一開始沒照片、要等一段時間才出現」，查到根因是輪播切換時才臨時下載下一張、沒有預先載入，已修復上線。教練接著要求「除了解決，也一併檢查小龍蝦是否還有其他問題」，順勢做了一次沒有敷衍的全面健檢——過程中意外挖出兩個之前完全沒被發現、真實存在的系統性問題：①main/kong/peipei三個agent完全沒有「只有教練能下系統指令」的權限鎖 ②沉默計數bug（教練已痛罵三次）的真正根因其實是系統裡藏著兩份互不同步的heartbeat-state.json，之前三次「修復」全部只改到其中一份。過程中還嘗試升級OpenClaw本體，撞上node版本不相容導致gateway短暫真的停機，已回滾恢復。**

## 🎯 本場戰果

### 1. 🎯🎯 ai-talk-tw活動花絮輪播「一開始沒照片」真正根因+修復
教練反映開啟`ai-talk-tw.netlify.app`時，活動花絮輪播一開始都沒照片，要等一段時間才出現，已經不是第一次。查證伺服器端（Content-Type、CDN快取、部署新鮮度）全部正常，排除伺服器bug。真正根因是前端邏輯：輪播每4秒自動切換到下一張，但程式碼是「切換的當下才臨時去下載新照片」，完全沒有預先準備，網路稍慢時切換那一瞬間就會出現空白，且每次自動切換都可能重演，不是只發生一次。修復：頁面載入後在背景用`new Image()`把全部24張照片預先塞進瀏覽器快取，切換時直接顯示。本機驗證通過（24張照片一開頁面就全部開始下載，非切換時才臨時抓）。**這個站其實是手動zip上傳型，GitHub push不會自動部署**（一開始誤判成auto-deploy型，查證後修正認知），照SOP走zip+API手動部署。GitHub commit `c0c860b`，Netlify部署`6a6f03f80217be568d0394b4`，quota扣1次(58→57)。

教練後續指出「這種錯誤讓我又要多消耗一次推送」，要求把教訓寫進SOP——已更新既有的`feedback_netlify_headers_content_type.md`（Netlify圖片部署SOP，累積血淚教訓的同一份檔案），新增第5坑：任何輪播/幻燈片類圖片功能，部署前要檢查是否有preload機制。commit `871dc0196`。

### 2. 🔴🔴🔴 小龍蝦沉默計數bug（教練痛罵三次）真正根因：系統裡藏著兩份互不同步的heartbeat-state.json
教練轉貼小龍蝦對話記錄，問「怎麼又跟我說我7天沒有互動」——這是教練今天第4次被誤報沉默時間（8/1「5.8天」、8/2中午「160h+」、8/2下午三度重申鐵律、8/2晚間「7天」），且是小龍蝦當天下午才宣稱「v3.0修好」之後又發作。

**第一輪查證**（v3.2）：發現小龍蝦寫的`scripts/sync_coach_last_message.sh`本身就是新bug的來源——它只看memory檔案裡「## 對話記錄 HH:MM」段落**標題**時間，沒看**內容**是誰說的，但每30分鐘健康檢查cron、每4小時主動關懷cron都會被memory記成「👤 教練：[cron:xxx]」或「👤 教練：[OpenClaw heartbeat poll]」——只要cron還在跑，就算教練真沉默3天也會被算成剛說過話，跟原本「誤報好幾天」方向相反、一樣是假數字，且更難被發現。改成逐段檢查內容，只採計非中括號開頭的「真正教練訊息」，並加上回溯7天的邏輯。commit `caf2376d6`+學習記錄`e0c515127`。

**第二輪查證**（v3.3，才是真根因）：v3.2部署後幾小時，18:03又發作「7天」，一度以為新版邏輯又壞了。深挖後發現**跟regex/雜訊過濾完全無關**：系統裡同時存在`state/heartbeat-state.json`與`memory/heartbeat-state.json`兩份彼此不同步的檔案。v3.0~v3.2所有修復都只寫入`state/`那份，但`memory/`那份從**7月26日**之後就沒被任何流程碰過，`coachSilentHours`停在166.2小時（=6.9天，四捨五入正是「7天」）。18:03那次agent turn剛好同時撞上main agent 17:38剛經歷context overflow重啟（全新session）、18:00 cron觸發時遇到minimax API 429限流讓turn拖了近4分鐘、桌面版軍師同一時間對gateway做config reload——三者疊加，agent很可能因此讀到了從沒被同步過的舊值。**不追究agent那次turn內部到底走了哪條讀取路徑**（LLM行為層面難以100%重現鎖定），改成結構性防呆：sync腳本現在`state/`與`memory/`兩份都寫，不管未來讀哪一份都是對的。已實測驗證兩份數字一致。commit `365cb7a25`+學習記錄`0578b8dc2`。

### 3. 🔴🔴 全面cron健檢：發現並停用重複跑了近2個月的「場景化升華」cron
查`openclaw cron list`發現兩個「場景化升華」cron都排在每晚23:00執行、內容幾乎一模一樣，其中一個從6/11建立後已經默默重複跑了快2個月，每天多燒一次不必要的處理成本，且查git log證實至少有一次真的因此寫入重複案例、被人工手動清過（7/23的commit可查）。已停用舊的那個（`533cfe54`，用`openclaw cron disable`），保留功能較完整（多了系統健檢步驟）的新版。其餘41個cron逐一檢查consecutiveErrors/timeout/殭屍腳本引用，全部正常，無其他重複。

### 4. 🔴🔴🔴 安全稽核發現：main/kong/peipei完全沒有「只有教練能下系統指令」的權限鎖
教練追問先前健檢報告裡「Telegram groupPolicy=open」這條，指出這是他之前就明確下過的既有指令（查證確認open policy確實從帳號建立時就存在，非近期異動，這條確認結案），但同時追問「你是不是已經把只有教練能發指令、其他人只能當用戶這件事做到？」。跑`openclaw security audit`查出真相：**只有bni_tainan/jiaolian_thoughts兩個對外服務agent有做這道鎖**，main（教練自己）、kong（孔大哥的學弟）、peipei（佩佩老師的學妹）三個完全沒有——系統列為CRITICAL。已比照bni_tainan/jiaolian_thoughts已驗證上線的模式，補上`tools.toolsBySender`：教練Telegram ID(`6124913915`)+LINE ID保留完整權限，其餘（含孔大哥、佩佩老師本人）一律deny掉`group:runtime`/`group:fs`/`group:automation`，一般對話不受影響。**不是只信任設定寫對就交差**——直接呼叫OpenClaw實際的`resolveToolsBySender`原始碼邏輯做測試：教練ID進去→`{}`無限制；陌生ID進去→正確被deny三個危險工具群組。Gateway重啟後確認config生效。commit `2f498962`（注意：這個commit在`~/.openclaw`外層repo的**master分支**，不是workspace的main分支，因為openclaw.json不在workspace裡）。

### 5. 🎯 OpenClaw本體升級評估與嘗試：內容確認有價值，但撞上node版本不相容導致短暫真實斷線
教練要求「認真查升級到底改了什麼」而非空口說風險不明。查官方changelog確認2026.6.33→2026.7.1三個教練關心的面向都有實質改善：**Memory/session**（105個PR修一致性、減少狀態遺失跨session混亂）、**穩定度**（Gateway crash loop不再無限重啟）、**安全性**（憑證/密鑰加固）。判斷值得升級並執行，但升級後doctor檢查發現gateway managed service用的node是25.6.1，卡在新版要求的支援區間外，**導致gateway真的停止服務、LINE/Telegram一度真的斷線**（不是可能，是真的發生）。第一次回滾又踩到系統記憶裡早記載過的「雙node環境」舊坑（npm指令解析到錯的node環境，裝到假地方），改用完整路徑`/opt/homebrew/bin/npm`才真正修好，`openclaw status --deep`確認LINE/Telegram皆OK後才算數。已回滾至2026.6.33穩定運作，升級本身擱置待node環境處理好後再議。記錄進記憶系統`reference_openclaw_node_version_upgrade_blocker`，commit `2fc408054`。

### 6. 🔴 ai-talk-tw輪播修復後教練回報「還是延遲」，尚未真正解決＋順手發現memory自動快照卡住超過5小時
戰果1修復並部署後，教練晚間10:27再次打開網頁回報「照片還是延遲」。查證部署本身確認是修復後的版本（`preloadCarouselImages`確實在線上），但這次photo-01.jpg實測下載花了1.14秒（比之前測的0.4秒慢），意識到**戰果1的修復（预载後續22張）跟教練這次講的「還是延遲」可能是兩個不同層面的問題**——如果教練是指「打開網頁那一刻連第一張都要等」，那是CDN/網路延遲層面，不是我修的「切換時才臨時下載」那個問題。已詢問教練三個關鍵細節（開頁瞬間或切換瞬間延遲／手機或電腦／延遲多久），**教練只簡短回「好，我已經用上了」沒有給出具體細節**，接著就說要開新對話收工。**這件事尚未真正解決，下一場開工第一件事必須先追問這三個細節才能繼續診斷，不要假設已經修好。**

過程中意外發現一個獨立但重要的系統問題：小龍蝦的`memory/YYYY-MM-DD.md`自動快照機制，從**下午17:53之後就完全沒有再更新**（查到22:43仍是舊的），已超過5小時無新內容——這呼應了本場戰果2查證時就已經看到的「⚠️ Pull 警告：本地有衝突或網路失敗」線索，但當時判斷git本身無真正衝突（fetch後領先/落後都是0）就沒有深究，事後看這個snapshot卡住的問題其實一直持續到收工都沒解決。這會持續影響任何依賴memory檔案判斷「教練最後說話時間」的邏輯（包含本場才修好的`sync_coach_last_message.sh`），下一場應該優先查清楚是哪個流程負責定期把對話寫進`memory/YYYY-MM-DD.md`、為什麼卡住。

## 📋 下一場直接開工任務
- **🔴 優先：ai-talk-tw延遲問題追問**：教練10:27回報「還是延遲」但沒給出具體細節，開工第一件事先問清楚——是打開網頁那一刻還是切換照片時延遲？手機還是電腦？大概延遲多久？才能判斷這是CDN/網路層面問題還是還有程式碼漏洞，不要假設已經修好
- **🔴 memory自動快照卡住**：`memory/YYYY-MM-DD.md`從8/2 17:53後沒再更新，超過5小時，需查清楚是哪個流程負責定期snapshot、為什麼停了——這會持續影響sync_coach_last_message.sh等依賴memory時間戳的邏輯
- **OpenClaw升級**：內容已確認值得（v89已查證），卡在node版本不相容，若教練希望完成升級，下一場先處理node版本（`brew upgrade node@22`或裝`node@24`，目前裝的22.22.0差一點點不夠新），確認gateway用的node符合支援區間後再重跑`openclaw update`
- **真誠/真愛/真AI分會＋大台南南區網站**：仍等教練回覆5項細節（v87已產出兩份HTML草稿），多場未更新
- Email自動發送系統、嘉義場籌備：仍卡在等教練給細節，多場未更新
- **BNI大台南小幫手「主動提醒」功能**：v87已完成上線，本場未變動，若教練近期實際使用有問題請回報

## 🔑 本場關鍵檔案索引
- `github_repos/ai-talk/index.html`：輪播preload修復
- `scripts/sync_coach_last_message.sh`：v3.2(過濾cron雜訊)→v3.3(雙檔案同步寫入)
- `openclaw.json`（`~/.openclaw`外層master分支）：main/kong/peipei補上toolsBySender
- `claude-brain/feedback_netlify_headers_content_type.md`：Netlify圖片部署SOP第5坑
- `claude-brain/reference_openclaw_node_version_upgrade_blocker.md`：升級前置檢查清單
- `.learnings/feedback_silence_count_must_be_real_time.md`：沉默計數bug完整5次錯誤時間軸
- commit序列（workspace main分支）：`c0c860b`(github_repos/ai-talk獨立repo，輪播修復) →
  `871dc0196`(SOP記錄) → `e8ba43b2a`(quota記錄) → `caf2376d6`(sync腳本v3.2) →
  `e0c515127`(v3.2學習記錄) → `2fc408054`(node blocker記錄) → `365cb7a25`(sync腳本v3.3真根因) →
  `0578b8dc2`(v3.3學習記錄)
- commit（`~/.openclaw`外層master分支）：`2f498962`(main/kong/peipei權限鎖)
- Netlify部署：`6a6f03f80217be568d0394b4`（ai-talk-tw輪播修復，quota 58→57）
- Cron變更：`533cfe54`（重複的場景化升華）已用`openclaw cron disable`停用

