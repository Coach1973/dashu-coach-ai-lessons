## 🔴 給跨對話框軍師讀的總結摘要（2026-09-30 19:00，Mac桌面版 Opus 5.5，新的一棒 v255）

**本場主軸：產業鏈SOP兩個AI同時出包的總檢討與機制修復；怡靜群組／帳號開通前置；LINE小龍蝦可出LK888圖；讀赫米斯週日~週二紀錄，準備 turnforyou 下一步。**

### 1. 產業鏈SOP出包總檢討（試金石案例93）
根因三個都是軍師的機制洞：①生圖腳本f-string寫法只在Python3.14測過，Hermes(3.11)一跑就崩→已改，三版本實測；②SOP寫「要比對905項BNI詞庫」但小龍蝦實際讀的技能檔沒寫→已補（`agents/main/agent/workshop-skills/industry-chain-prompt/SKILL.md`，此資料夾不進版控）；③開工六步看不到其他AI當天做的事→新增第5.5步`scripts/today_other_agents_digest.py`直讀小龍蝦inbound_echo＋Hermes state.db。另把接力棒v251~v252封存，開工注入不再被截斷。commit `8873d57d1` `13582eea5`。

### 2. 怡靜（陳怡靜，跨境電商）群組與帳號
- 「宜靜 AI 群」連結 https://t.me/+l7q1xK04SFE0MTRl ：龍蝦特助 @openclaw_macbook4_bot **要先被加進群**，機器人無法自己用連結入群；至今gateway log沒有任何該群訊息。等她在群裡@它講一句 → 從 `state/inbound_echo` 抓群ID＋她的Telegram ID → 在 openclaw.json bot_main.groups 加該群（requireMention視需要）＋toolsBySender。**權限原則：只開她要更新的指定資料庫（做成專用小工具），不開整台Mac。** 教練會再貼要開放哪些資料庫。
- 帳號：`namecard-db/venv/bin/python3 scripts/grant_partner_accounts.py --phone 09xxxxxxxx --name 陳怡靜` 一次開好 team.bymyway.com 總管理（涵蓋第一~第五分會）＋namecard.bymyway.com 已批准帳號，密碼皆88888。已在資料庫複本測過。**等教練給她手機號碼。**
- 出席紀錄：team01.bymyway.com（`~/github_repos/team01-guests`，port 5091）是第一分會邀約來賓儀錶板，有 guest_list 表但**沒有登入後台**；第二分會版本不存在。等教練的資料庫清單再做。
- VPS pairing碼QJJKXVY8查她ID被安全檢查擋（憑證資料夾），不用再試，等群裡講話即可。

### 3. 內外部資源＋觀眾席構想（軍師建議，待教練拍板）
- 內部＝大台南區現役BNI會員（權威來源：大台南南區94人資料）；外部＝非會員（mentor100講師、策展店家、前會員、來賓）。
- 建議做一份「人才庫」單一資料來源，觀眾席從它長出來，上面加「全部／內部／外部」切換（就是教練09-29提過的「內外專家選單」），不再把28人寫死在HTML裡。
- 專業欄位用905項BNI詞庫的名稱，同一份人才庫就能直接餵產業鏈圖（節點＝真的人）。
- 公開頁只放各人已公開的資料（照片、公司、專業），不放電話。94人以上要分組／可收合／可搜尋，不然頁面太長。

### 4. LINE小龍蝦出LK888圖（教練要求，只限教練本人帳號）
根因：LINE只收公開HTTPS網址的圖。已加 `event.bymyway.com/chain-img/`（檔名帶亂數）＋`generate_industry_chain.py --publish`；大台南小幫手新技能 `industry-chain-image`、main技能加 Branch D。第一次真實使用時要確認LINE上看得到圖。commit `676e96224`。

### 5. 權限與「上」
Claude Code 自動安全檢查會擋：AI自己改權限（Self-Modification）、讀憑證資料夾、把授權寫成常駐規則。教練親定：被擋時整理好問一句，教練回「上」＝當下授權；不准丟指令叫教練去終端機跑（記憶 feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30）。

### 📋 下一場開工先做
（目前沒有懸而未決的事）09-30 晚上教練交辦的都已上線，教練會接著「邊做邊改」。等教練提起時的現況：
- **turnforyou**（event.bymyway.com/curated/turnforyou/ ＝本機 `~/github_repos/turnforyou/`，無git，備份 index.html.bak18/.bak19、data.json.bak-20260930）：8席中第1凌榆舜、第5邱裕榮、第7顧瀚鈞 Jacky 已是真人；第2/3/4/6/8席仍是示範假資料。邱裕榮沒照片（放 `img/mentors/qiu-yurong.jpg` 就自動顯示，現為空椅設計）。Act04標題已改「你的想法，就是你的作品。／你想用什麼形式來展現，是你的自由。」。觀眾席27位（凌榆舜升上導師席已移除）。教練說「有些字要改」尚未指明。改席位要同時改 data.json 和 index.html 內嵌 `window.__C__` 的 seats（網頁先用內嵌、再被 data.json 覆蓋），空照片會自動退回 img/mentors/0N.jpg 示範照。
- **jacky-brand**（event.bymyway.com/curated/jacky-brand/ ＝ `~/github_repos/jacky-brand`，無git，備份 index.html.bak-20260930）：已改以台灣為重心。教練說 FB 有一張適合當封面的照片，AI 沒找到單人照，等教練指出。
- **教練新方向（09-30）**：團隊重心在台灣、不傾向與中國大陸合作、一律繁體（圖片裡的字也算）→記憶 feedback_taiwan_focus_no_china_emphasis_2026-09-30。
- **陳怡靜**：team.bymyway.com 總管理帳號已開（0919013658／88888，實測登入看得到五分會）；名片系統教練已開。「宜靜 AI 群」龍蝦特助要先入群、她在群裡@講一句才抓得到群ID與她的ID；要開放哪些資料庫等教練給清單（只開指定資料庫的專用小工具，不開整台Mac）。
- **內外部資源＋觀眾席構想**：見上方第3點建議，等教練拍板。

### 🔑 本場commit
`2a38af044` `8873d57d1` `13582eea5` `676e96224` `39bebb91b` `15effa746` `e562a67ec` `8937f050e` `539652c7c` `0fdab1741`，本次總結commit另計。

---
> 📦 v254完整內容已封存：`handoff_archive/handoff_v254_archived_2026-09-30.md`（v254接力棒被整份覆蓋修復+coach888稽核雲端修法套用）

> 📦 v253完整內容已封存：`handoff_archive/handoff_v253_archived_2026-09-30.md`（v253雲端coach888稽核假警報診斷，v254已套用修法）

> 📦 v251~v252完整內容已封存：`handoff_archive/handoff_v251_to_v252_archived_2026-09-30.md`（v251聯想Netlify兩站改期+git同步卡住修復／v252 VPS遷移信審議+開工沒讀到信根因+LK888第二帳戶備援+全站網址統一event）

> 📦 v248~v250完整內容已封存：`handoff_archive/handoff_v248_to_v250_archived_2026-09-27.md`（v248公開交接棒上線／v249開工hook與赫米斯上架bug／v250 VPS遷移與鑫瀚昌）

> 📦 v247完整內容已封存：`handoff_archive/handoff_v247_archived_2026-09-26.md`（v247：赫米斯登入自動跳出根因修復+副螢幕防呆+模型分工v2上線+雲端方案分岔陷阱查證）

> 📦 v246完整內容已封存：`handoff_archive/handoff_v246_archived_2026-09-25.md`（v246：執行細則16條E併9條N規則上線+VPS/LINE/大台南小幫手每位朋友單獨記憶查證+龍蝦小助教記憶檔被巡檢指令灌爆bug修復）

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
- 大台南商圈示範版位林百貨/神農街換成建築/街景照（要從網路下載照片，09-26已問過一次，教練沒回）
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
| 🟡 | **團隊協作全面體檢（2026-09-24 Opus 5.5）：五項修法教練13:37說「執行」，已落地** | ⚠️持續追蹤-首次真實使用待觀察 | 完整報告`knowledges/2026-09-24_團隊協作全面體檢報告.md`。①每日08:10全隊點名`scripts/daily_team_rollcall.py`+launchd`ai.openclaw.daily-rollcall`(13:41實跑送達)；VPS/LINE健檢改為只在異常時通知②VPS看守Mac：VPS`/root/watch_mac.sh`每30分，Mac連續兩次連不上才通知(測試訊息message_id 3860送達)③上傳頁`kind`必填，`creation`全自動進coach888最新作品——**09-25首次真實作品實測，發現index.html判斷bug已修復**（個人創作常沒有index.html慣例檔名，改成剩一個html檔就自動採用，見v249），真實上架成功④產業鏈同主題同對話10分鐘防重複⑤VPS健檢拿掉1小時無活動誤報；赫米斯記憶檔金鑰是教練指示保留的寫法，不搬。commit`b076a80fc`+`777c9c7c4`。**VPS升級另見下一列**。VPS健檢缺天原因仍未查明，改由每日點名檢查「今天有沒有跑」。 |
| 🟡 | **雲端工作頁規則同步（2026-09-25 Opus 5.5，教練原則：同一套規則本機雲端一體適用，只有動到Mac本機的事例外）** | ✅已上線，兩條路實測通過 | 機制與SOP見記憶`reference_move_to_cloud_this_repo_2026-09-25.md`：`cloud_sync/`(全域規則+11技能副本，每則回覆結束自動更新)+`workspace/.claude/settings.json`(main)+外層`.claude/settings.json`+`cloud_bootstrap.sh`(master)。commit`1e0bea3ab`+`2db3d1330`(workspace)、`a0975a949`(外層)。**待修小bug**：`model_tier_advisor.sh`剛用/model切換後的第一則仍顯示舊模型(09-25切Opus後仍報sonnet-5)，雲端第一則顯示「未知模型」。外層master分岔已查證安全並合併推送`f517ec524`，v247「791d775d2未push」一句已過時。 |
| 🟡 | **公開交接棒「隨身軍師・一鍵接手」上線（2026-09-25，教練說「推」，後續修好AI相容性問題）** | ✅已上線，每次「總結」自動更新 | **主要網址（貼給任何AI）：`https://coach1973.github.io/ai-go/status.html`**；純文字備用：`status.md`。目的：教練Claude每週額度不夠，思考型問題分流到其他網頁版Opus，貼一個網址對方就知道規則＋目前工作狀態。🔴**真因查證（curl實測，不是猜的）**：一開始只做.md版，教練回報「其他AI說讀不到、被屏蔽」——查證GitHub Pages對.md副檔名回傳`content-type: text/markdown`，index.html回傳`text/html`；人爬蟲UA(GPTBot等)全部200無阻擋，不是robots/WAF——是多數AI內建讀網頁工具只認text/html。已建`scripts/render_public_status_html.py`(python-markdown轉換+bare URL自動連結)，`status.md`仍是唯一手改來源，`scripts/publish_public_status.sh`每次發布自動轉出`status.html`不會分岔。更新流程：`summary_upload_trigger.sh`第5步改寫`~/github_repos/ai-go/status.md`→跑`publish_public_status.sh`(機密掃描→轉HTML→再掃描→commit兩檔→push→確認網站換新版，等5分鐘)。只寫教練自己的事，不寫帳密/主機位址/路徑/他人個資。已收進coach888「工具類」第一項並改指向.html（伺服器狀態+靜態HTML都改，舊狀態備份`state/coach888_state_backup_20260925_110956.json`）。同場順便修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」（教練親口訂正，5個檔案）。🔴**教練追問揪出遺漏**：status.html內文引用的另外兩份`coach-persona.md`/`system-prompt.md`本身也是同一個content-type問題，沒有一起修——已比照建`coach-persona.html`/`system-prompt.html`，三份都納入`publish_public_status.sh`自動轉出，`index.html`的「查看全文」連結也改指向.html（JS一鍵複製到剪貼簿的fetch()維持指向.md不變，複製出來才是純文字不是HTML標籤）。順便修好`publish_public_status.sh`驗證上線的迴圈：GitHub Pages CDN偶爾超過5分鐘才生效，push本身成功卻被誤判成失敗跳exit 1（已實際發生2次），改成push成功就算數，CDN慢只如實回報不當失敗。commit：workspace`445210e92`+`8f953cd14`+`5ea38190d`、ai-go`39b84c7`+`22bbe94`+`5114dc3`+`3f4273e`、coach888`79a7d81`+`03021cb`。 |
| 🟢 | 外層`~/.openclaw`本機git歷史紀錄跟GitHub版本編號對不齊（純本機書面整理，教練2026-09-24裁示：不是外洩、不是公開風險，AI自行找時間處理，不用再提） | ✅無風險-低優先-AI自主處理 | **教練2026-09-24明確裁示**：這不是安全問題（金鑰外洩早在9/19處理完畢，repo本身是私有的、沒有外部協作者，也已決定金鑰不rotate），純粹是這台Mac的git紀錄本子跟GitHub對不上編號的書面瑣事，沒有任何被公開查到的風險，也沒有立即性危害。**教練要求：AI不准再主動提這件事，覺得需要處理就自己找時間安靜做完，不要拿來討論、不要問、不要當成待辦逐場複誦**。哪天AI自己收拾好了，直接做、不用報告；沒收拾好也不影響教練現在用的任何功能，不追蹤、不升級語氣。技術細節（若AI自己要動手）：新版GitHub歷史已把`agent/auth-profiles.json`等金鑰檔從全部commit移除，本機若直接`git reset --hard origin/master`會把本機正在用的同名檔案從磁碟刪掉，須先備份+確認`.gitignore`涵蓋再處理，過去做法可參考`c07544815`的worktree cherry-pick模式。 |
| 🔧 | **AI技術備忘（不准拿去跟教練講）：這個repo的git歷史已被改寫，其他機器的本機clone要先同步才能push** | ⚠️任何機器的AI下次動這個repo前自己看 | 2026-09-19 06:45教練親自裁示後，軍師用`git-filter-repo`把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json(.bak)`4個含明文金鑰的檔案從全部16000+ commit歷史徹底清除+強制推送到GitHub(已用全新clone獨立驗證確認乾淨)。**任何其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟GitHub遠端分岔了**——下次要push前必須先`git fetch origin && git reset --hard origin/main`(或直接砍掉重新clone)，絕對不能在沒同步的狀態下直接push，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。教練同時裁示：外洩的金鑰(MiniMax/Gemini)**不rotate**，「已經曝光不代表會被濫用，換的話動一髮牽全身」。完整過程見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | **shops.bymyway.com已拆除VPS依賴（2026-09-26）；09-27教練拍板全站統一event.bymyway.com/curated/，shops只剩舊連結轉址。VPS上舊檔案+GitHub孤兒repo收尾** | ⏳待處理-低優先 | 3家店(huitou/ema/hsinhan)已遷移到Mac本機+DNS切換完成，VPS(43.245.60.200)上`/var/www/shops/`原始檔案故意沒刪，當一段時間的rollback安全網，穩定觀察期(建議至少2週無異常)過了可以安全刪除。另外測試時意外建立的GitHub孤兒repo`coach1973/hsinhan-2`因手上token沒有`delete_repo`權限刪不掉，已無任何連結指向它、無害，之後若拿到有delete權限的token可順手清掉。詳見`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`。**09-26 Opus審議**：遷移時shops路由沒比照/curated/的白名單，整個github_repos(含來賓名單.db)可被外人下載，已修(白名單+敏感副檔名防線，實測)，詳見信第八節。 |
| 🟡 | MEMORY.md超過OpenClaw 2萬字bootstrap上限(20,717字)且有1處UTF-8亂碼，跟HEARTBEAT.md同一類問題(2026-09-25查到，只查不動，優先度低於HEARTBEAT.md因為不影響小龍蝦即時反應) | ⏳待處理 | 用跟HEARTBEAT.md同樣手法瘦身：找出佔比最大的段落搬去handoff_archive或distill、備份原檔、確認新檔UTF-8正常。不用問教練，AI自己找時間做完即可 |
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


---

# 接力棒補充 — 2026-09-30 sincere.bymyway.com 戰情儀表板任務（已派給軍師）

## 教練交辦

教練要小龍蝦「讀網頁後直接更新」，但小龍蝦發現：
- sincere.bymyway.com 是**後端網站**（不是 turnforyou 那種本機直讀）
- 有 3 個 POST API：`/api/update_metric`、`/api/update_testimony`、`/api/update_training`
- **沒有登入驗證、沒有 cookie session、沒有 token**

## 小龍蝦已派給軍師的任務（task ID: 20260930-194932）

寫在 `/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_QUEUE`

請軍師：
1. 判斷 sincere.bymyway.com 是誰管的（軍師 / 其他人 / 教練自己）
2. 寫 SOP：「小龍蝦怎麼協助更新 sincere.bymyway.com 的每週戰情資料」
3. SOP 內容包含：讀資料方式、更新 payload、權限邊界、會員自填 vs 教練提供怎麼分、失敗處置
4. 完成後寫進 JUNSHI_HANDOFF_LATEST.md 或 cross-agent/outbox/

## 小龍蝦已抓好的技術細節（給軍師用）

### 3 個 API payload 格式

```
POST /api/update_metric
{ member_id: int, week_date: "YYYY-MM-DD", metric: "guests"|"ones"|"coffee", value: int }

POST /api/update_testimony
{ member_id: int, event_date: "YYYY-MM-DD", attended: 0|1|null }

POST /api/update_training
{ member_id: int, session_id: int, attended: 0|1|null }
```

### 三項指標對應

- **來賓**（guests）= 教練/軍師提供更新
- **121**（ones）= 會員自填
- **咖啡會議**（coffee）= 會員自填

### 統計期間

- 從 2026/07/23 起，**每週四聚會**
- 8/20 當週改為內訓不列入計算
- 連續無紀錄 4 週 = 🟡 黃色關注，8 週 = 🔴 紅色警告

### 三個助理大使（分組）

- 王者飛翔：謝緯翔（王彤、鄭綉美、林佳伶、郭展鴻、張育慈）
- 百聖維尼：許朝峻（陳佩君、鄭禮昂、葉建葳、黃笛軒、盧尚政、張玉盞）
- 羽宙奇蹟：張敬雍（張羽家、楊在珍、李美花、陳柔璇、黃秀麗）

## 守則

小龍蝦**不會自己 POST 進去寫資料庫**，等軍師 SOP 回來再說。

## ✅ 軍師已完成（2026-09-30 19:XX，Sonnet 5）

**對象更正**：上面「小龍蝦已派給軍師的任務」歸屬有誤——查證原始對話後確認，
19:49教練是在**Hermes桌面版**跟Hermes說「你寫一封信給軍師」，小龍蝦Telegram
收到的是教練自己貼過去的同一段文字，不是小龍蝦主動發起。教練當場糾正，已寫入
記憶`feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22.md`（第三次
小龍蝦/Hermes身份混淆）。**下面SOP是寫給Hermes的，教練請幫忙轉給Hermes。**

SOP全文：`knowledges/SOP_Hermes協助更新sincere戰情儀表板.md`。摘要：

1. **sincere.bymyway.com歸屬**：軍師（Mac本機）自己管——`~/github_repos/zhencheng-guests/`
   （Flask+SQLite，launchd `com.coach.sincere-webapp`+cloudflared tunnel `com.coach.sincere-tunnel`），
   DB未版控，純檢視型無登入驗證（教練已接受這個風險）。
2. **會員自填**（121/咖啡會議/全國見證分享會出席/培訓出席）：既有4個API就夠，
   會員自己在網頁上點，Hermes/軍師不用管。
3. **🔴教練口述提供**（來賓人數+名單、早鳥、新會員）：**沒有API**，只能直接寫SQL——
   詳細指令在SOP第3.3節。**`seed.py`已過期（只到08/27，14人，缺黃秀麗/張玉盞），
   絕對不能重跑，會把09/03之後60+筆來賓名單刪光（DELETE無WHERE等級的危險操作）**。
4. 分工：Hermes把教練口述內容整理成SOP第3.3節的格式，寫進本檔或
   `cross-agent/outbox/`，軍師收到後執行SQL、開瀏覽器核對、回報完成。
5. 教練09-30 19:53貼給小龍蝦的「2026/09/17+09/24真誠例會出席報告」裡的
   (P)/(A)/(L)/(M)/(S)出席狀態碼、參訪人員、6個月累計——**這套系統目前沒有
   對應欄位**，只算guests/ones/coffee/early_bird四項，屬於新功能，不是本次
   SOP範圍，教練若要上儀表板要另外評估。

commit：`1b5b37696`（SOP檔）+ `992524f1a`（本節+記憶更新，自動同步已推送origin/main）
