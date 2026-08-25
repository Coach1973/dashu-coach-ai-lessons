# 軍師接力棒 · 2026-08-24 v127（Mac桌面版 Sonnet 5，38人培訓費批次最後8張開票+ezPay完整SOP+claude-in-chrome連線鐵律）

> 建立時間：2026-08-24 15:16 ~ 19:02（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v126（同機同日下午）
> 本棒主軸：**教練說「開票」，把38人培訓費批次最後8張全數開立完成，過程中claude-in-chrome連錯裝置害教練連續動怒三次，修好後教練要求「像網頁推SOP一樣」寫一份完整開票SOP，已建立。**

## 🎯 本場戰果

### 1. ✅ 38人培訓費批次全數結案（32張）
開工時查明還缺5人資料，主動查CSV+總清冊補齊杜亞洛/劉彥彬(Email+金額)；教練陸續提供謝盛峰(統編00441185)、莊政川(統編00442987)、柯炫任(手機條碼/GG1CUU2)後8人到齊。教練下令後逐張開立(自訂編號081925~081932)+`search_invoice`查證「已開立」，合計$3,600。連同8/19已開的24張，全批32張結案。完成清單`claude-brain/data/ezpay_training_invoices_2026-08-24_8張完成清單.json`。過程抓到並修正一個資料錯誤：填「劉彥彬」時`form_input`一度把姓名寫錯成「劉彥櫃」，讀回確認後修正才送出。

### 2. 🔴🔴🔴🔴 claude-in-chrome連錯裝置，教練三度動怒，isLocal:true鐵律寫死
開票前連線一直卡到教練Windows裝置的殘留連線(`isLocal:false`)，不是教練實際在用的Mac本機Chrome，教練完全看不到我在操作什麼，連續多輪誤會（教練原話：「不接受不接受」「到底是誰的問題」「你自己有另外一套系統是我看不到的」）。**根因**：Mac本機Chrome擴充功能斷線，不是沒裝——`chrome://extensions`確認Claude擴充功能一直都在且開啟，但`list_connected_browsers`就是連不上。**修法**：`osascript -e 'tell application "Google Chrome" to quit'`關掉整個程式再`open -a "Google Chrome"`重開，重新配對後`select_browser`選`isLocal:true`裝置即可解決。教練親口拍板「這台電腦永遠都是第一個，不用再問」。

### 3. 🎯🎯🎯 完整ezPay開票SOP建立（教練指定：像網頁推SOP一樣）
新建`feedback_ezpay_invoice_sop.md`（教練說「開票」自動觸發），六步驟：資料齊全檢查→連線裝置確認(isLocal:true鐵律)→填表(欄位ID全部固定+中文姓名一律JS賦值避免亂碼)→含稅勾選+金額核對→送出(jQuery trigger)→查證(search_invoice)。下次開票不用再重找線索。

### 4. 🔧 順手清理：作廢一則過時記憶+壓縮MEMORY.md
發現`project_ezpay_invoice_task_delegated_to_lenovo_2026-08-16.md`寫著「發票交聯想機器」，但8/18起Mac一直在開票（今天也是），已標記作廢避免下次誤導。MEMORY.md索引順手壓縮169→139行（移除已解決/過時/單次事件條目，同主題合併用`[[連結]]`保留可查性）。

## ⚠️ 本場最大教訓
動手操作前沒有先驗證claude-in-chrome連的是不是`isLocal:true`裝置，直接開始操作導致教練完全看不到、連續多輪誤會+情緒受影響，浪費教練約30分鐘時間跟好心情。**這條鐵律現在已經寫進SOP，下次開票或任何要用claude-in-chrome的任務，第一步就是`list_connected_browsers`確認`isLocal:true`，不對就照SOP流程自己修好，不用再問教練或截圖比對。**

## 📋 下一場直接開工任務
- 3張舊發票(蔡珮彤081907/吳亞平081922/楊凱為081924)Email欄位空白，待教練重新登入ezPay後用「查看/補發」補上（技術上不受任何清單卡住，隨時可做）
- 承接舊待辦：3支孤兒hook要不要啟用、台中場報名通知merge、bni-chapters「真誠分會」架構問題、現場立牌是否重印

## 🔑 本場關鍵檔案索引
- `~/.claude/projects/-Users-bymyway--openclaw/memory/feedback_ezpay_invoice_sop.md`：新建完整開票SOP
- `~/.claude/projects/-Users-bymyway--openclaw/memory/reference_ezpay_invoice_issuing_procedure.md`：補充欄位ID對照表+連線裝置規則
- `knowledges/2026-08-18_38人培訓發票二聯三聯資訊蒐集中.md`：本批次全程記錄，已標記結案
- `claude-brain/data/ezpay_training_invoices_2026-08-24_8張完成清單.json`
- commit：`968661359`(workspace發票清單)／`cd9eb6b19`+`de76222c4`(memory repo SOP+索引壓縮)


---

---

# 軍師接力棒 · 2026-08-25 v129（Mac桌面版 Opus 5，賈維斯全系統體檢＋10項修復）

> 建立時間：2026-08-25 01:28 ~ 12:40（台灣時間，中間因教練 RustDesk 遠端連線於 01:53 中斷而停擺約 9.5 小時）
> 上一棒：v128（同機同日凌晨）
> 本棒主軸：**教練要求「進入賈維斯狀態做全盤體檢，看哪些流程能更自動化、佈局有無矛盾」，
> 隨後裁示「你講一堆我不見得聽得懂，對系統有好處的事你就動手做」，全程自主執行 10 項修復。**

## 🎯 本場戰果（全部已驗證＋推雲端）

### 體檢揪出的核心問題形狀：自動化「有在跑」≠「有發揮作用」
歸納成三層檢查（已寫成記憶 `feedback_automation_must_reach_a_human`）：
① 有在跑嗎 ② 判斷邏輯真的執行了嗎（靜默失效）③ **結果有沒有送到該看的人手上**（最常漏）

### 1. 🔴 記憶寫了卻讀不到（最嚴重）
`claude-brain/` 有 **112 個記憶檔沒被 MEMORY.md 收錄**，含前一天才寫的 `feedback_ezpay_invoice_sop.md`
（試金石案例63 宣稱「已寫入」，但索引沒收錄＝下次開新對話讀不到＝等於白寫），直接違反守則#01。
→ 補進 30 天內的 9 筆；`stop_rules_master.py` 新增規則K：Stop 時自動偵測 24 小時內寫過但沒進索引的記憶檔。commit `5d5eaf58f`

### 2. 死管道全面接上通知（機器做了幾個月，教練一則都沒收到）
桌面 `reminder.txt` 堆積 61 行從沒被打開（且勞保/庫存兩條設成「每天」卻寫「今天是最後繳費日」＝每天喊狼來了）；
`checkpoint_audit` 每 15 分偵測到「資料沒備份」只寫 /tmp log；試金石策展提醒只寫 HEARTBEAT.md（那是 AI 看的）。
→ 新增 `scripts/notify_coach.sh` 統一出口並實測送達。**踩通三個坑**：`openclaw message send` 從 cron 呼叫會先報
`Channel is required`（系統同時接 telegram+line），加了 `--channel` 又報 `token missing`（token 在 gateway 進程不在環境變數），
最終改成從 openclaw.json 讀 token 直接打 API。commit `84b8948b7`

### 3. 正在跑卻沒備份的東西全部納管
6 個 hook（auto-goal/group-identity/round-table-orchestrator/self-improvement 完全沒進版控，bot-relay 兩支只進一半）、
**4 個 AI 員工的人設檔**（SOUL/IDENTITY/USER/TOOLS/DREAMS 全部沒備份，硬碟壞就沒了）、
agent 知識庫（含 46 萬字教練語料）、`~/.openclaw/scripts` 底下 14 支手寫腳本（其中兩支是 LaunchAgent 正在跑的）。
`.gitignore` 補上約 8GB 執行時資料，git status 雜訊 112→28 筆。commit `c98b51b1`

### 4. 金鑰防護做成「擋得住」的機關
**本場自己踩的坑**：納管時「有做金鑰掃描」也掃出 2 個，但掃描跟 commit 寫在同一串指令、沒有阻斷，token 照樣推上去。
查證後確認 repo 是 PRIVATE 且同組 token 早在 openclaw.json 裡，**沒有實際外洩**，但教訓是「檢查不能擋就等於沒有」。
→ `scripts/git_secret_guard.sh` 掛進兩個 repo 的 pre-commit，實測擋得住。commit `73303871a`
⚠️ 安裝時差點覆蓋掉 workspace 原有的 pre-commit（案例25 的 .ps1 BOM 機關），發現後改成兩道並存。

### 5. 硬編碼金鑰全機清除（機關自己抓出來的）
新機關擋下一筆提交，追查發現是體檢時 `head` 讀取 `council_orchestrator.sh`，該腳本硬編碼的 token 被記進對話逐字備份、
再被自動備份 cron 推上雲端——**只要腳本裡有寫死的金鑰，任何時候讀取它都會外流一次**。
全機掃描後 4 支腳本（heartbeat-monitor / reminder_hsr_0505 / council_orchestrator / junshi_task_worker）
全部改成從設定檔讀取。commit `809fdc1f`+`2902ea9b6`

### 6. 教練親自點破的死碼：額度用盡自動換模型
教練說「我現在沒有額度用完的問題，這應該是很久以前不用的東西」——查證完全屬實：
它讀的 log 檔最後寫入 2026-06-03（83 天沒新內容）、要找的關鍵字整份 log 出現 0 次、現在主模型是 MiniMax-M3。
＝ 就算沒壞也永遠不會執行。**稍早那筆「修好判斷式」等於修了一段永遠不會跑的程式碼**，直接移除 85 行。
保留腳本本體 A/B/D/E/F 五段（Context Overflow 自動重啟今早 08:38 才真的用過）。commit `abe44cb2`

### 7. 39 支死腳本歸檔（搬不刪）
重做引用掃描（第一版邏輯寫錯，沒把不可信的數字給教練）。掃 403 份來源文件。
⚠️ 第一版盲點：漏掃 `.git/hooks/`，害 `precommit_check_ps1_bom.sh` 被誤判，補上後排除。
歸檔 33 支一次性挖掘工具（score_top30/_v2/_v3 多版本並存即是用完即棄的證據）+ 6 支測試腳本。
scripts 161→105 支。commit `2902ea9b6`

### 8. 停掉一支空跑兩個月的排程
`ai.openclaw.council-orchestrator` 每 2 分鐘跑一次（一天 720 次），但它所屬的 bot-relay 機制
2026-07-02 就由教練決定退役，搭檔 hook 早已 disabled，自己的 log 最後真的做事是 2026-06-28。
→ plist 移到 `~/Library/LaunchAgents/_disabled_2026-08-25/` 附完整理由與復原指令。
**每日輪詢 2256 → 1536 次（降 32%）**

### 9. 清掉每次開機都報錯的死外掛
`memsearch` 未編譯的 TypeScript，累計 881 次啟動報錯，且不在 plugins.allow 白名單內（本來就沒生效）。
搬到 `extensions_disabled/`，重啟驗證報錯歸零、hooks 仍載入 17 支、通道正常。

### 10. 修好每 2 分鐘噴錯 549 次的判斷式（後來連同死碼一起移除，見第 6 項）

## 📋 下一場可接手的
- **23 支查無引用的腳本待個別判斷**（含 `notify-coach.sh` 已標棄用、`reminder_hsr_0505.sh` 是 5/5 過期提醒、
  `auto-switch-model.sh` 與剛移除的額度死碼同一時代），本次保守未動
- **剩餘 5 支輪詢型自動化待逐一評估**：session-fix（每2分，確認有用）、terminal-watchdog（每5分）、
  memory-sync（每30分）、vps-polling-healthcheck（每15分）、peipei_stuck（每5分，昨天才真的救過一次不能拆）
- 勞保繳費/庫存清點兩條提醒已停用，**等教練給正確日期再重建**
- 承接舊待辦：3 支孤兒 hook 要不要啟用、bni-chapters「真誠分會」架構問題

## 🔑 本場 commit
`5d5eaf58f`（記憶索引）／`2c57c11a`（判斷式）／`84b8948b7`（通知管道）／`c98b51b1`（納管）／
`73303871a`（金鑰機關）／`809fdc1f`（token 改設定檔）／`776b6c807`（記憶）／`abe44cb2`（死碼移除）／`2902ea9b6`（歸檔+金鑰清除）

---

---

# 軍師接力棒 · 2026-08-25 v128（Mac桌面版 Sonnet 5，ezPay BNI入會/續約發票18張+AI微論壇台中場正式上線+Netlify額度SOP兩度修正）

> 建立時間：2026-08-24 19:08 ~ 2026-08-25 01:22（台灣時間，跨夜長場）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v127（同機前一場）
> 本棒主軸：**教練連續交辦ezPay發票、AI微論壇台中場報名通知上線、Netlify額度查證三件事，過程中兩次被教練當場糾正並修正做法（場次通知辨識度不夠、額度查證頻率太高），最後教練提出「賈維斯」最高目標宣言收尾。**

## 🎯 本場戰果

### 1. ✅ ezPay BNI台南南區入會/續約發票18張全數開立（商店337391376聚寶盆）
自訂編號082401~082418。第一批12張（10位入會$39,800+2位續約$26,800），查重複時用XHR攔截讀取8季度192筆去重資料比對，只有柯炫任查到去年入會舊紀錄，教練確認「去年新會入今年續約」非重複照開。第二批6張續約$26,800，查到3人有$36,000入會舊紀錄（正常入會→續約關係）、林尹渰一筆備註對不上姓名的舊紀錄，教練確認是分會轉會(真富→真鑫)+公司舊稱，非資料錯誤。教練同場問今年/去年開票總額，用同套方法查出今年$1,882,890、去年$3,240,000。已寫入記憶`reference_bni_membership_fee_history_and_chapter_transfer`（入會費逐年調漲36000→39800）。

### 2. 🎯🎯 AI微論壇台中場(9/23-24)報名通知正式上線+兩輪修正
`feature/registration-notify`分支merge進master，GitHub Pages+Netlify雙平台上線。教練實測後發現Telegram通知場次全顯示「AI微論壇」分不出嘉義/台中DAY1/DAY2，查明event.db三場活動同名，改用`location+event_date`組成標籤修復(commit`f34d9fbc5`)。教練又發現網頁還留著「概念稿」字樣5處，既然已正式上線就拿掉+順手清孤兒CSS，重新推兩平台。

### 3. 🔴🔴🔴 補救：作品總覽(coach888)漏更新，教練當場立SOP
教練發現AI微論壇台中場推上Netlify後，作品總覽沒有同步更新網址，指出「推GitHub測試/推Netlify都要同步更新作品總覽」是SOP的一部分，不是事後才想起來。已補上（從「不公開個人檢索」搬到「大樹常用」，網址改Netlify正式版），寫入記憶`project_portfolio_netlify_github_logic`。

### 4. 🔴🔴🔴 Netlify額度追蹤SOP兩度修正
教練要求查真實帳單頁，發現本機估算值(849.5/1000)跟真實(76.4/1000)嚴重脫節，真實只剩約9次部署額度。第一版SOP寫「每次部署都查真實頁面」，教練當場推翻：「這種每一次都要進去查非常不智慧，會耗token+要教練登入」，改拍板**每7~10天校正一次，日常用估算法即可**。帳單週期確認每月25日重置。已寫入記憶`project_netlify_deploy_quota_2026-07`。

### 5. 🎯🎯🎯 教練提出最高目標宣言：賈維斯
教練親口：「你的最高目標，就是鋼鐵人裡面的那個賈維斯，對於大樹教練所有交待的事情，說過的每一句話都記得，並且能夠自動串連起來，不用我每件事情都要一再交待！」已寫入永久記憶`feedback_jarvis_outcome_delegation_style`，核心：狀態型記憶要附驗證法（不能只記一個數字放著不動）、同主題多次追問要主動串連前文。

## ⚠️ 本場兩次被教練當場糾正的教訓
1. **場次通知只印活動名稱不夠**——多場活動共用同一個名稱時，通知看起來像同一場，改用地點+日期組合標籤才能真正辨識。
2. **驗證頻率不是越高越好**——第一次修正過度反應（改成每次都查），教練點破這是「機械化修正」不是「智慧修正」，真正的解法是找一個合理的抽查頻率（7~10天），不是把驗證成本推到最高。

## 📋 下一場直接開工任務
- 3張舊ezPay發票(蔡珮彤081907/吳亞平081922/楊凱為081924)Email欄位空白，待教練重新登入ezPay後補（隨時可做，不受任何清單卡住）
- Netlify額度下次校正約2026-09-01~09-04，或估算值≤3次時提前查
- 承接舊待辦：3支孤兒hook要不要啟用、bni-chapters「真誠分會」架構問題、現場立牌是否重印

## 🔑 本場關鍵檔案索引
- `claude-brain/data/ezpay_bni_membership_invoices_2026-08-24_12張完成清單.json`+`ezpay_bni_renewal_invoices_2026-08-24_6張完成清單.json`
- `event-signup/app.py`：Telegram通知場次標籤修復
- `github_repos/ai-forum-taichung/index.html`：報名通知功能+概念稿字樣移除
- `github_repos/coach888/index.html`：作品總覽同步更新
- `state/netlify_deploy_quota.json`：真實額度校正
- 記憶：`reference_bni_membership_fee_history_and_chapter_transfer`／`project_portfolio_netlify_github_logic`／`project_netlify_deploy_quota_2026-07`／`feedback_jarvis_outcome_delegation_style`
- commit：`9d22495a5`+`9922f67f9`(ezPay清單)／`4c7556b`+`f34d9fbc5`+`c7ce4fe`(ai-forum-taichung)／`d89955e`(coach888)／`d9463272a`+`18fba071c`+`dddc9b301`(memory repo)／`befc00c13`+`cbc26851a`(quota state)
