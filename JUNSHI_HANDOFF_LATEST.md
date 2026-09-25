## 🔴 給跨對話框軍師讀的總結摘要（2026-09-25 04:15，Mac桌面版，新的一棒 v247）

**本場主軸：教練登出再登入後，赫米斯桌面版自己跳出來，要求「登入時不要啟動」。軍師繞了一大圈（先查Telegram連線、推給macOS重開視窗、開系統設定叫教練自己關、連帶把視窗開到擴充塢副螢幕），教練點出「LINE/Telegram都不會，只有Hermes會」才找到真因。教練收尾痛批：同樣的錯什麼時候才不再犯——已從機制修根源。**

### 1. 赫米斯登入自動跳出：已修
真因`~/Library/LaunchAgents/ai.hermes.desktop.plist`寫`RunAtLoad=false`，但`KeepAlive.SuccessfulExit`在launchd規則裡隱含RunAtLoad，每次登入照跑`open Hermes.app`（`launchctl print`顯示runs=1）。改`KeepAlive=false`，重新載入模擬登入runs=0。原檔備份`~/.hermes/ai.hermes.desktop.plist.bak-2026-09-25`。Telegram線`ai.hermes.gateway`沒動。教練定義：**「赫米斯」＝Mac桌面版Hermes.app**，Telegram線不碰、不當選項問（第3次混淆，已放MEMORY.md索引最上方）。試金石案例82。

### 2. 副螢幕：是軍師造成的，已裝防呆
Wokyis擴充塢附的1280×720螢幕（接953GB SSD和連接埠，**不能叫教練拔**），用Time Machine快照比對，設定自9/21起沒變過；今天是軍師`open`系統設定落在那台。新增`scripts/main_display_guard_hook.sh`（PostToolUse：開App/視窗/改html後自動把副螢幕視窗搬回主螢幕）+`scripts/move_windows_to_main_display.sh`，實測通過。

### 3. 背景項目54項盤點，封存3項沒用的
kong/peipei四月舊版獨立gateway（已改由主gateway bindings服務）＋gateway舊bak，含金鑰，搬到`~/Library/LaunchAgents_archive_2026-09-25/`不進git，說明`_archive/launchagents_retired_20260925/README.md`。其餘52項都在用，教練：「有用就留，沒用的不要留」。

### 4. 根源修法（不加記憶，改機制）
①`pre_task_hook.sh`加「🩺故障診斷法」：教練描述故障就注入「先找對照組→推論先用指令推翻→自己修完才報→3~5行」②`stop_rules_master.py`加A2「叫教練自己動手」擋下（今天三句原話實測全擋；「只有您能」＋密碼/連結等正當情況放行）。

### 5. 🧭 模型分工默契（教練親定）
重大決策、找根因、設計機制用 Opus；庶務用 Sonnet。規則在`knowledges/模型分工規則_Opus與Sonnet.md`，由`scripts/model_tier_advisor.sh`（UserPromptSubmit）自動評估：**v2（教練要求看得見）：每則交辦回覆第一行都標「🟢 Sonnet 就能做／🟣 Opus 等級」**；Sonnet 標🟣先建議切換不動手，Sonnet 卡關停下建議切 Opus；Stop hook A3 沒標示就擋。8 種情況實測通過。教練：本期流量（週三13:00重算）到週五04:13已用50%。

### 6. 教練體驗雲端方案（$100/月），實際搬過一次+踩到本repo分岔陷阱
外層`~/.openclaw`repo卡兩關：①常年背景雜訊要先commit（逐一查證排除533MB漫畫素材大檔，已補`.gitignore`，沒查到機密）②本機分支跟遠端因9/19金鑰清除是真分岔（領先/落後各25），直接push會把舊金鑰歷史推回去——改用`move_to_cloud`的`skip_push:true`，雲端從遠端乾淨版本接手，教練今天的實際工作內容都在`workspace`子repo（沒有分岔問題）已正常commit。雲端對話框連結：https://claude.ai/code/session_018RBKxnNSzFi3t68hTMaR9t 。查證發現：雲端session在本機`list_sessions`/`get_session`完全查不到，是claude.ai端獨立系統，教練要找回雲端對話框目前只能靠瀏覽器開claude.ai/code，桌面版側邊欄會不會顯示AI端看不到自己畫面無法驗證。SOP已寫`reference_move_to_cloud_this_repo_2026-09-25.md`。

### 7. 🔴 攔下一則可疑的英文git指令，沒有照做push
教練切換雲端/本機時，這個對話框收到一句風格明顯不像教練平常口吻的英文指令「commit+push」，研判是操作雲端切換時誤觸/誤送。查證：commit的部分（2個DREAMS.md）安全，已做；push那部分因為就是上一條講的分岔陷阱、會有推回舊金鑰歷史的風險，沒有自己決定做，回頭跟教練確認過。**目前仍是本機commit`791d775d2`，還沒push，教練若之後想通了要不要處理外層repo分岔，再說。**

### 📋 下一場開工先做
沒有要問教練的事。`sfltool dumpbtm`要管理員密碼會跳視窗，**不要再跑**。外層`~/.openclaw`本機commit`791d775d2`還沒push（分岔陷阱，見上第7點），不用主動處理，教練提起再說。

### 🔑 本場commit
`65e4060e8`（試金石82）`bd56c5e3f`（副螢幕防呆）`cceb8ae12`（封存背景項目）`fc3a764af`（模型分工v2）（以上皆workspace repo）；外層`~/.openclaw` repo `791d775d2`（DREAMS.md，本機未push）；本次總結commit另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-25 01:24，Mac桌面版，新的一棒 v246）

**本場主軸：教練要求逐條體檢執行細則，16條E規則併為9條N規則正式上線（含9個技能+8支注入程式+小龍蝦/赫米斯同步）；接著查VPS/LINE/大台南小幫手三系統「每位朋友單獨記憶」是否落實，抓到並修好龍蝦小助教記憶檔被巡檢指令灌爆、9/24起完全停止記錄教練真話的重大bug；過程中兩度被教練當場糾正並修正根源。**

### 1. 🔴 執行細則v2：E01~E17併為N1~N9，全鏈路同步
逐條核對hook/技能/9月違規統計，16條併9條（每條附「撐住它的機制」，N5補上Top10第1名「事件觸發被換成定時檢查」原本沒有的條文，刪掉E05裡08-31後已無人照做的舊步驟）。舊版全文封存`handoff_archive/執行細則_v1_E01-E17_封存_2026-09-24.md`。同步9個技能、8支會注入文字的程式（總結暗號/設定注入/金鑰防護/心法引用/徵詢偵測等）、workspace與全域CLAUDE.md、小龍蝦AGENTS.md+rule-reminder hook、赫米斯SOUL.md（4條精華，未進git）。commit`d882f4cbb`+`3dfa885ea`（Mac）、`788c8e892`+`7bbd5e58d`（小龍蝦）。過程中rule07輪詢偵測誤判「提到偵測器名稱」為提議輪詢，已補白名單commit`97b2c958f`。

### 2. 🔴🔴 三度被教練當場糾正：git分岔重複騷擾、VPS「無權」說法、規則字面過寬
①教練怒「同一件事又拿出來煩我」——外層repo本機git分岔被我用「分岔/外洩」字眼重新包裝問了第5次，教練明講已結案。②我以「不能自己輸密碼」為由把VPS連線丟回教練，教練嚴詞糾正「之前30、50次都怎麼做的」——根因是三關規則①原文「需要教練本人登入帳密」把系統已存好帳密的主機也算進去。已改6處：路徑大全/既有腳本已存帳密的主機（VPS/GitHub/Netlify/ezPay等）AI自己用，只有從未存過帳密的才算教練才能做。commit`fde1eefab`(git分岔降級)、`be1a44af5`(三關①釐清)。

### 3. 🔴🔴 修好龍蝦小助教記憶檔被巡檢指令灌爆+200KB上限停寫bug
教練追問「每位朋友單獨記憶」是否落實，逐一查證LINE三帳號+VPS體驗版：查出`hooks/line-user-memory`把小龍蝦2.0每30分鐘巡檢指令當成教練說的話寫進記憶（9/22起63筆佔96%），且200KB上限寫反成「超過就停寫」，教練檔案9/24 06:20起完全停止記錄真話。已修：巡檢指令雙重判斷不記、超過上限整份封存後續記，沙盒5項測試通過，教練檔案202KB→7KB清乾淨(原檔封存)，重啟gateway 14秒恢復。同時修正VPS新規則誤寫「CLIENT_PROFILE.md」（朋友空間根本沒這檔案，實際是每日記憶+dreaming整理）。commit`e4cc4209c`(Mac)、`856342502`(VPS)、`cd2c85e84`(留底)。

### 4. 🔧 VPS體驗版規則v2上線：12條+工作守則併8條，簡單任務直接做
主帳號+9位朋友空間8條規則全部內嵌SOUL.md（檢查碼一致81e0394f→修正後606ea999）；`auto-goal`/`rule-reminder`改成只對主帳號注入執行合約，朋友的sessionKey(`agent:trial-*`)跳過。VPS本機commit`24fcfde57`（未push，VPS本機09-19後與雲端已分岔，見AI技術備忘列）。

### 📋 下一場開工先做
沒有待教練決定的事。VPS本機/雲端分岔、AI自己的工作清單見接力棒表格區，不用主動提。

### 🔑 本場commit
`d882f4cbb` `3dfa885ea` `97b2c958f` `fde1eefab` `be1a44af5` `e4cc4209c` `cd2c85e84`（workspace repo）；`788c8e892` `7bbd5e58d`（外層`~/.openclaw` repo）；`24fcfde57` `856342502`（VPS本機）。本次總結commit另計。

---

> 📦 v245完整內容已封存：`handoff_archive/handoff_v245_archived_2026-09-25.md`（v245：VPS/LINE健檢推播404修復+五項修法落地+小龍蝦2.0評估+版本變動通知）

> 📦 v244完整內容已封存：`handoff_archive/handoff_v244_archived_2026-09-25.md`（v244：大樹創作SOP口語別名缺失修復+coach888插入bug修復+coach888分類重組+MEMORY.md清理）


> 📦 v242~v243完整內容已封存：`handoff_archive/handoff_v242_to_v243_archived_2026-09-24.md`（v242產業鏈SOP誤報700+分類資料庫查證+名片系統去識別化技術文件雙版本交付／v243 MEMORY.md索引159筆清零+namecard-db前會員/來賓資訊改造+cloudflared版本過舊發現解決，E16瘦身2026-09-24執行）
> 📦 v238~v241完整內容已封存：`handoff_archive/handoff_v238_to_v241_archived_2026-09-24.md`（含全面體檢/agents人設檔救回/llama-cpp修復/聚寶盆發票/ezPay作廢SOP等v238~v241全紀錄）

---

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
（目前沒有）

### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- VPS升級LTS 2026.7.35（教練09-24：10/1左右月報會自動提醒，時間到再說）
- 367位前會員推薦人補查（BNI Connect帳密沒存在路徑大全，要教練本人登入一次；09-24已問過一次）
- 柯朝陽發票（教練09-24：延後約一年，不用管）
- 試金石商業化計畫書（教練09-24：還沒想到怎麼商品化，暫時不用管）
- 小二(test2)/OpenClaw 2.0評估（暫停，等官方修復）
- 小二Telegram輪詢異常（教練09-21：等小二成熟再處理）
- 聯想C碟WinSxS再瘦身4~5GB（要不要做，教練沒回）
- bni-chapters真誠分會網頁架構問題（教練還沒說明是哪個問題）
- 「教練都在想什麼」補更多素材（等教練提供）
- 其他LINE帳號比照搬遷（等教練指定帳號，SOP已備妥）
- 小龍蝦後台看不到中文名（教練裁示：看到陌生ID問了再回）
- coach888拖拉排序好不好用（等教練回饋）
- 「全世界最優秀的團隊計畫」報名連結（等教練給網址）
- 企業健身房正式建站（等教練交辦）
- 企業健身房4項文案修改（等教練交辦下一步）
- BNI小幫手實戰體驗（等教練親測）
- Coze舊機器人何時停用（等教練裁示）
- ACER 36.3GB備份刪除（需教練在ACER親自開對話）
- 赫米斯Telegram線登出登入時斷約2分鐘（綁使用者登入，要改成開機常駐系統服務才能根治；09-25已告知一次，教練沒要求處理）

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟡 | **團隊協作全面體檢（2026-09-24 Opus 5.5）：五項修法教練13:37說「執行」，已落地** | ⚠️持續追蹤-首次真實使用待觀察 | 完整報告`knowledges/2026-09-24_團隊協作全面體檢報告.md`。①每日08:10全隊點名`scripts/daily_team_rollcall.py`+launchd`ai.openclaw.daily-rollcall`(13:41實跑送達)；VPS/LINE健檢改為只在異常時通知②VPS看守Mac：VPS`/root/watch_mac.sh`每30分，Mac連續兩次連不上才通知(測試訊息message_id 3860送達)③上傳頁`kind`必填，`creation`全自動進coach888最新作品(離線+Flask測試全過，**尚未有真實大樹作品走過一次**，下次教練上傳時看`distill/curation_process.log`)④產業鏈同主題同對話10分鐘防重複⑤VPS健檢拿掉1小時無活動誤報；赫米斯記憶檔金鑰是教練指示保留的寫法，不搬。commit`b076a80fc`+`777c9c7c4`。**VPS升級另見下一列**。VPS健檢缺天原因仍未查明，改由每日點名檢查「今天有沒有跑」。 |
| 🟡 | **雲端工作頁規則同步（2026-09-25 Opus 5.5，教練原則：同一套規則本機雲端一體適用，只有動到Mac本機的事例外）** | ✅已上線，兩條路實測通過 | 機制與SOP見記憶`reference_move_to_cloud_this_repo_2026-09-25.md`：`cloud_sync/`(全域規則+11技能副本，每則回覆結束自動更新)+`workspace/.claude/settings.json`(main)+外層`.claude/settings.json`+`cloud_bootstrap.sh`(master)。commit`1e0bea3ab`+`2db3d1330`(workspace)、`a0975a949`(外層)。**待修小bug**：`model_tier_advisor.sh`剛用/model切換後的第一則仍顯示舊模型(09-25切Opus後仍報sonnet-5)，雲端第一則顯示「未知模型」。外層master分岔已查證安全並合併推送`f517ec524`，v247「791d775d2未push」一句已過時。 |
| 🟡 | **公開交接棒「隨身軍師・一鍵接手」上線（2026-09-25，教練說「推」，後續修好AI相容性問題）** | ✅已上線，每次「總結」自動更新 | **主要網址（貼給任何AI）：`https://coach1973.github.io/ai-go/status.html`**；純文字備用：`status.md`。目的：教練Claude每週額度不夠，思考型問題分流到其他網頁版Opus，貼一個網址對方就知道規則＋目前工作狀態。🔴**真因查證（curl實測，不是猜的）**：一開始只做.md版，教練回報「其他AI說讀不到、被屏蔽」——查證GitHub Pages對.md副檔名回傳`content-type: text/markdown`，index.html回傳`text/html`；人爬蟲UA(GPTBot等)全部200無阻擋，不是robots/WAF——是多數AI內建讀網頁工具只認text/html。已建`scripts/render_public_status_html.py`(python-markdown轉換+bare URL自動連結)，`status.md`仍是唯一手改來源，`scripts/publish_public_status.sh`每次發布自動轉出`status.html`不會分岔。更新流程：`summary_upload_trigger.sh`第5步改寫`~/github_repos/ai-go/status.md`→跑`publish_public_status.sh`(機密掃描→轉HTML→再掃描→commit兩檔→push→確認網站換新版，等5分鐘)。只寫教練自己的事，不寫帳密/主機位址/路徑/他人個資。已收進coach888「工具類」第一項並改指向.html（伺服器狀態+靜態HTML都改，舊狀態備份`state/coach888_state_backup_20260925_110956.json`）。同場順便修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」（教練親口訂正，5個檔案）。commit：workspace`445210e92`+`8f953cd14`、ai-go`39b84c7`+`22bbe94`+`5114dc3`、coach888`79a7d81`+`03021cb`。 |
| 🟢 | 外層`~/.openclaw`本機git歷史紀錄跟GitHub版本編號對不齊（純本機書面整理，教練2026-09-24裁示：不是外洩、不是公開風險，AI自行找時間處理，不用再提） | ✅無風險-低優先-AI自主處理 | **教練2026-09-24明確裁示**：這不是安全問題（金鑰外洩早在9/19處理完畢，repo本身是私有的、沒有外部協作者，也已決定金鑰不rotate），純粹是這台Mac的git紀錄本子跟GitHub對不上編號的書面瑣事，沒有任何被公開查到的風險，也沒有立即性危害。**教練要求：AI不准再主動提這件事，覺得需要處理就自己找時間安靜做完，不要拿來討論、不要問、不要當成待辦逐場複誦**。哪天AI自己收拾好了，直接做、不用報告；沒收拾好也不影響教練現在用的任何功能，不追蹤、不升級語氣。技術細節（若AI自己要動手）：新版GitHub歷史已把`agent/auth-profiles.json`等金鑰檔從全部commit移除，本機若直接`git reset --hard origin/master`會把本機正在用的同名檔案從磁碟刪掉，須先備份+確認`.gitignore`涵蓋再處理，過去做法可參考`c07544815`的worktree cherry-pick模式。 |
| 🔧 | **AI技術備忘（不准拿去跟教練講）：這個repo的git歷史已被改寫，其他機器的本機clone要先同步才能push** | ⚠️任何機器的AI下次動這個repo前自己看 | 2026-09-19 06:45教練親自裁示後，軍師用`git-filter-repo`把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json(.bak)`4個含明文金鑰的檔案從全部16000+ commit歷史徹底清除+強制推送到GitHub(已用全新clone獨立驗證確認乾淨)。**任何其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟GitHub遠端分岔了**——下次要push前必須先`git fetch origin && git reset --hard origin/main`(或直接砍掉重新clone)，絕對不能在沒同步的狀態下直接push，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。教練同時裁示：外洩的金鑰(MiniMax/Gemini)**不rotate**，「已經曝光不代表會被濫用，換的話動一髮牽全身」。完整過程見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | 軍師自我要求：查證前先查「路徑大全」+盤點類任務要窮舉底層資料結構 | ⚠️永久提醒 | 教練v90當場糾正兩次查證不完整（VPS沒先查路徑大全就回報查不到、LINE帳號盤點漏算沒有名稱標籤的「龍蝦小助教」），教練明確期許「你是所有資訊的大總管，要自己想辦法完善」。已寫入試金石案例55，核心自我檢查：①任何「查不到/做不到」結論前先確認查過該環境萬用索引檔 ②盤點類任務直接數清楚底層資料結構(JSON物件key數)逐一核對，不能只挑印象中顯眼的幾筆 |

---

> 📦 v114完整內容已封存：`handoff_archive/handoff_v114_archived_2026-08-18.md`（Mac桌面版，Chrome搶線根因+ezPay 238筆+coach888連結）

---

> 📦 v115完整內容已封存：`handoff_archive/handoff_v115_archived_2026-08-18.md`（聯想Windows，BNI-Training雙軌系統從零建置+753筆官方報表整合）

---

> 📦 v116完整內容已封存：`handoff_archive/handoff_v116_archived_2026-08-18.md`（聯想Windows，BNI培訓紀錄精準度修正+MSP投票新網站+SOP違規教訓）

---

> 📦 v117完整內容已封存：`handoff_archive/handoff_v117_archived_2026-08-18.md`（聯想Windows，4-8月簽到表開票總清冊交叉比對修正MSP名單）

---

> 📦 v118完整內容已封存：`handoff_archive/handoff_v118_archived_2026-08-18.md`（Mac桌面版，五項任務逐一執行+ezPay 108統編備註查詢完成+find -maxdepth查證失誤自我更正）

---

> 📦 v119完整內容已封存：`handoff_archive/handoff_v119_archived_2026-08-19.md`（Mac桌面版，BNI Connect活動出席勾選任務首次上線，8場活動101人次標記完成）

---

> 📦 v120完整內容已封存：`handoff_archive/handoff_v120_archived_2026-08-19.md`（Mac桌面版，讀跨機信箱接手ezPay培訓費發票，16張全部開立完成，MerchantID假成功陷阱首次發現）

---

> 📦 v121完整內容已封存：`handoff_archive/handoff_v121_archived_2026-08-23.md`（Mac桌面版，教練推翻「34人收齊才開票」規則，24張ezPay培訓費發票先開立）

---

> 📦 v122完整內容已封存：`handoff_archive/handoff_v122_archived_2026-08-24.md`（Mac桌面版，教練糾正「查無Email」誤判＋BNI 94人資料庫永久指引）

---

> 📦 v123完整內容已封存：`handoff_archive/handoff_v123_archived_2026-08-24.md`（Mac桌面版，大樹小講事件密集場：救回雙寫程式碼+場次管理後台+修好2次部署bug）

---

> 📦 v124完整內容已封存：`handoff_archive/handoff_v124_archived_2026-08-24.md`（Mac桌面版，AI助理資料包+8/28攤位頁+報名通知失聯真根因，搬運工失誤試金石案例62）

---

---

> 📦 **v112及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v116_archived_2026-08-18.md`（v116）+ `handoff_archive/handoff_v115_archived_2026-08-18.md`（v115）+ `handoff_archive/handoff_v114_archived_2026-08-18.md`（v114）+ `handoff_archive/handoff_v113_archived_2026-08-17.md`（v113）+ `handoff_archive/handoff_v112_archived_2026-08-17.md`（v112）+ `handoff_archive/handoff_v111_archived_2026-08-16.md`（v111）+ `handoff_archive/handoff_v110_archived_2026-08-16.md`（v110）+ `handoff_archive/handoff_v109_archived_2026-08-16.md`（v109）+ `handoff_archive/handoff_v108_archived_2026-08-15.md`（v108）+ `handoff_archive/handoff_v106_to_v107_archived_2026-08-14.md`（v106+v107）+ `handoff_archive/handoff_v105-lenovo_archived_2026-08-14.md`（聯想Windows 2026-08-10）+ `handoff_archive/handoff_v104_to_v105_archived_2026-08-12.md`（v104+v105 Mac桌面版） + `handoff_archive/handoff_v104-lenovo_archived_2026-08-10.md`（v104聯想Windows） + `handoff_archive/handoff_v101_to_v103_archived_2026-08-09.md`（v101~v103）+ `handoff_archive/handoff_v100_archived_2026-08-08.md`（v100）+ `handoff_archive/handoff_v99_archived_2026-08-08.md`（v99）+ `handoff_archive/handoff_v97_to_v98_archived_2026-08-07.md`（v97~v98）+ `handoff_archive/handoff_v93_to_v96_archived_2026-08-05.md`（v93~v96）+ `handoff_archive/handoff_v92_archived_2026-08-05.md`（v92）+ `handoff_archive/handoff_v91_archived_2026-08-05.md`（v91）+ `handoff_archive/handoff_v90_archived_2026-08-04.md`（v90）+ `handoff_archive/handoff_v89_archived_2026-08-03.md`（v89）+ `handoff_archive/handoff_v88_archived_2026-08-03.md`（v88）+ `handoff_archive/handoff_v87_archived_2026-08-02.md`（v87）+ `handoff_archive/handoff_v85_to_v86_archived_2026-08-02.md`（v85+v86）+ `handoff_archive/handoff_v84_archived_2026-07-31.md`（v84單獨一份）+ `handoff_archive/handoff_v83_archived_2026-07-30.md`（v83單獨一份）+ `handoff_archive/handoff_v82_archived_2026-07-28.md`（v82單獨一份）+ `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`（v72~v81）
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。

---


> 📦 v125+v126完整內容已封存：`handoff_archive/handoff_v125_to_v126_archived_2026-08-25.md`（Mac桌面版，凌晨全系統稽核+教練覆核追加任務）

---


> 📦 v127+v128+v129完整內容已封存：`handoff_archive/handoff_v127_v128_v129_archived_2026-08-25.md`（Mac桌面版，ezPay發票+台中場上線+賈維斯全系統體檢兩場+頻率覆核）

---

> 📦 v130完整內容已封存：`handoff_archive/handoff_v130_archived_2026-08-25.md`（Mac桌面版，賈維斯體檢延續：頻率覆核+解決通知從沒送達的根因，留下Q1待辦）

---

> 📦 v131完整內容已封存：`handoff_archive/handoff_v131_archived_2026-08-26.md`（Mac桌面版，AI微論壇台中場RWD真根因修復+Netlify額度重新校正）

---


> 📦 v132+v133完整內容已封存：（Mac桌面版，Q1總結功能+context-overflow-guard改版+名片系統CRM擴建）

---

> 📦 v134完整內容已封存：`handoff_archive/handoff_v134_archived_2026-08-26.md`（聯想Windows，Windows當機根因+ezPay記憶更正+跨機Stop hook查證+總結hook缺jq修復）

---

> 📦 v135完整內容已封存：`handoff_archive/handoff_v135_archived_2026-08-27.md`（Mac桌面版，BNI Connect 430人匯入+MiniMax額度事故案例65+路徑大全憑證稽核）

---


> 📦 v136完整內容已封存：`handoff_archive/handoff_v136_archived_2026-08-26.md`（Mac桌面版，BNI Connect前會員電話/Email補齊+來賓資料庫3712筆完整收集）

> 📦 v137~v139完整內容已封存：`handoff_archive/handoff_v137_to_v139_archived_2026-08-27.md`（v137 Mac桌面版媒合手動觸發定案／v138聯想Windows跨機同步四層根因／v139 Mac桌面版RustDesk修復+MiniMax紅線+bigtree密集迭代）

> 📦 v140完整內容已封存：`handoff_archive/handoff_v140_archived_2026-08-27.md`（聯想Windows，FB粉專發文API從零建置，卡在商家驗證+教練當場檢討試錯效率）

---

> 📦 v141完整內容已封存：`handoff_archive/handoff_v141_archived_2026-08-27.md`（Mac終端機，bigtree 8/28 EDM上線+報名頁LINE誘因文案定案+/slides多簡報支援+ezPay發票查證）

---

> 📦 v142完整內容已封存：`handoff_archive/handoff_v142_archived_2026-08-27.md`（Mac終端機，修復Stop hook守則#07輪詢偵測瞎眼35天的根因，commit`01a28f2fb`）

---

> 📦 v143完整內容已封存：`handoff_archive/handoff_v143_archived_2026-08-28.md`（Mac終端機，BNI信用証清查4分會171人完成，真鑽231人查了10人中途總結）

---

> 📦 v144+v145完整內容已封存：`handoff_archive/handoff_v144_to_v145_archived_2026-08-28.md`（Mac終端機v144離會會員信用証清查全數完結／聯想Windows v145 AI微論壇+ai-art獨立站建置）

---

> 📦 v146完整內容已封存：`handoff_archive/handoff_v146_archived_2026-08-30.md`（Mac終端機，BNI信用証清查後續建網頁+複查+權限隔離+誤觸事故）

---

> 📦 v147完整內容已封存：`handoff_archive/handoff_v147_archived_2026-08-30.md`（Mac終端機，/bni-credit三項待改+34筆信用証補開+搜尋空格bug修復）

---

> 📦 v148完整內容已封存：`handoff_archive/handoff_v148_archived_2026-08-30.md`（Mac終端機，乾淨世界頻道QR上線+peipei-event斷線5天修復+電腦變慢診斷）

---

> 📦 v149+v151完整內容已封存：`handoff_archive/handoff_v149_v151_archived_2026-08-30.md`（Mac終端機，真誠分會邀約來賓系統從零建置+bni-chapters重複實作/fork根因鑑識，v149與v151是同一起fork事件的兩條分支，內容已在v150結案）

---

> 📦 v150完整內容已封存：`handoff_archive/handoff_v150_archived_2026-08-31.md`（Mac終端機，真誠分會邀約來賓重複建置根因查明+移除+5位會員專屬編輯網址交付）

---

> 📦 v152完整內容已封存：`handoff_archive/handoff_v152_archived_2026-08-31.md`（Mac終端機，逐步脫離Netlify：4個新路由+3處連動+作品總覽更新）

---

> 📦 v218完整內容已封存：`handoff_archive/handoff_v218_archived_2026-09-19.md`（Mac桌面版，全部釋放+MiniMax團隊品質稽核機制+開工hook身份誤判修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

---

> 📦 v219完整內容已封存：`handoff_archive/handoff_v219_archived_2026-09-19.md`（Mac桌面版，手機/軍師討論邊界+Netlify中文檔名修復部署+後台帳密清單結案+workspace git大掃除含金鑰外洩發現+coach888熱門排行新功能）

> 📦 v220完整內容已封存：`handoff_archive/handoff_v220_archived_2026-09-19.md`（Mac桌面版，接力棒狀態表失真教訓+機械防呆`handoff_sync_guard.sh`上線+CLAUDE.md 236KB→78KB瘦身+M系列MiniMax 1M機制查證+手機Remote Control重啟卡死未解留待下一棒）

> 📦 v221+v222完整內容已封存：`handoff_archive/handoff_v221_v222_archived_2026-09-19.md`（v221 Mac桌面版，手機Remote Control真正根因查明修復+舊SOP早有答案的教訓／v222 Mac桌面版，中正大學互動牆從零建置上線+赫米斯Telegram斷線16小時根因修復，E16瘦身本場執行）

> 📦 v223~v227完整內容已封存：`handoff_archive/handoff_v223_to_v227_archived_2026-09-20.md`（v223 B路徑1M通驗證／v224跨對話框交接SOP／v225 MiniMax懸案初步調查+coach888同步修復(平行session)／v226產業鏈SOP雙執行root cause／v227 MiniMax懸案徹底解謎+手機1M實測成功，E16瘦身2026-09-20執行）

---


> 📦 v228~v230完整內容已封存：`handoff_archive/handoff_v228_to_v230_archived_2026-09-21.md`（v228憑證層git追蹤問題發現／v229 git-filter-repo歷史清除執行完畢／v230 CCU留言關閉+coach888收錄查證，E16瘦身2026-09-21執行）

---

> 📦 v231~v237完整內容已封存：`handoff_archive/handoff_v231_to_v237_archived_2026-09-24.md`（v231 TokenTable接OpenCode+Episode11漫畫+agent捏造完工案例／v232 CCU媒體格式連環修復／v233海餅乾網站+BNI PPT SOP建立／v234聯想bni-dna/bigtree維護+記憶體洩漏追蹤／v235手機流量查證鏈+EM模式定義／v237膠囊咖啡機產業鏈+語音轉簡體字記錄，E16瘦身2026-09-24執行）
