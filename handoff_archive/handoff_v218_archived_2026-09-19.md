# 軍師接力棒 · 2026-09-18 v218（Mac桌面版 Sonnet 5，全部釋放+MiniMax團隊品質稽核機制建立+開工hook身份誤判根因修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

> 建立時間：2026-09-18 11:18 ~ 17:18（台灣時間）
> 上一棒：v217
> 本棒主軸：**教練要求執行「全部釋放」後，委託軍師以「賈維斯/老大哥」角色稽核兩個正在跑任務的手機MiniMax session品質。逐行讀transcript稽核後發現：兩個session的實際任務執行品質其實不差，但都在開工宣言自稱「Opus軍師」——查出根因是`feed_junshi_handoff.sh`寫死這句話，已修復為依環境變數動態判斷。順勢建立「AI團隊品質稽核」機制(既有13條Stop hook規則彙整器)+AI團隊名冊。教練追問「怎麼監督」+「幕僚長晨報/起床摘要/盲點監控三個名詞是什麼」+「不可逆待授權清單」，逐一查證回答並直接執行決定。過程中意外發現並協助排除bigtree-tw Netlify部署對中文檔名zip解壓的隱性bug(MiniMax已自行restore止血)。**

## 🎯 本場戰果

### 1. 全部釋放指令執行
教練喊「完整釋放」，經AskUserQuestion確認等同既有「全部釋放」指令，執行`scripts/release_all_memory.sh`：Chrome/LINE/Typeless本來就沒在跑、赫米斯已停止(bootout四個launchd服務)、RustDesk重啟(247M→208M)。

### 2. 兩個手機MiniMax session品質稽核：任務執行本身OK，但身份自稱是系統性bug
逐行解析`f7ded585`(真鑫/真鑽戰情儀表板更新)+`5876ed8b`(全都開始/v214-v217待辦執行)兩份完整transcript(非用猜的)：
- **真鑫/真鑽任務**：正確從教練貼的兩張週報截圖辨識分會+數字全部SUM驗證對齊教練原始週報，中途自行抓到並修正錯誤(林仁超邀4位一度誤寫1位)，方法論健全。教練誤以為「忘東忘西」的根源是：文字指令本身沒帶分會名稱，AI需要先踏查全部分會現況才能鎖定範圍，非真的亂猜。
- **全都開始任務**：正確把待辦分Class A(可自行動手)/B(等外部)/C(不可逆待授權)三類，只動手做A類，且都有扎實驗證(6個合成事件測試+18/19 regression測試+commit hash)，不可逆的三項(peipei金鑰/Netlify/FB審核)正確地沒有擅自動手。
- **真正問題**：兩個session開工宣言都自稱「Mac 軍師，Opus 最高決策層」。追查根因：`scripts/feed_junshi_handoff.sh`第212行原本無條件`echo "軍師（Opus）"`，不論實際觸發者是誰都灌輸這句話。**修復**：改用`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`是否被清空判斷身份——`claude rc`(手機Remote Control host)啟動時用`env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY`清空真Anthropic憑證，逼子session退回用`ANTHROPIC_DEFAULT_OPUS_MODEL`別名解析成MiniMax-M3；本機終端機/桌面版保有真實憑證。**踩坑記錄**：一開始誤用`ANTHROPIC_DEFAULT_OPUS_MODEL`本身內容判斷，發現這台Mac全域shell環境本來就把它設成MiniMax(不分session)，改用BASE_URL/API_KEY才是正確判斷點。已用真實環境模擬測試通過。commit`4de7654c0`。

### 3. AI團隊品質稽核機制 + AI團隊名冊建立
教練問「怎麼設計監督流程，事前送審還是事後查」，查證發現：`stop_rules_master.py`的13條規則(A~M)本來就對任何觸發Stop事件的session自動稽核(含手機MiniMax)，event-driven、非輪詢，親眼看到規則C今晚就攔到一個MiniMax session的時區違規並即時自我修正。真正缺口是違規記錄各自寫進`distill/*violations.log`沒人讀。新增`scripts/agent_team_qa_digest.py`：追蹤已讀行數，只彙整「上次讀過之後」的新違規，按session分組並用assistant訊息的`model`欄位判斷是📱手機MiniMax還是🖥️本機Claude，掛進`feed_junshi_handoff.sh`六步驟尾段——沒有新違規完全安靜，有才顯示，不新增輪詢cron。已用今晚真實違規資料(session`5876ed8b`的時區+輪詢設計違規)驗證正確分組顯示，首次執行的歷史backlog(6月至今上百筆)已消化為baseline不會一次倒給教練。`路徑大全.md`新增「AI團隊名冊」章節列出MiniMax-M3+LK888兩個已知成員的用途/額度來源/監督機制。commit`ca8752418`。

### 4. 三項教練委託評估的待辦，直接查證+決定+執行
- **幕僚長晨報**：查明這是「監看bni_tainan+jiaolian_thoughts兩個對外agent動態」的cron(跟「起床摘要」監看的是這台Mac自己的git commit完全是兩件事，不重複)。已重建cron`0d64be3c-061d-4ca8-add0-d22862677e59`，每日07:00送教練個人Telegram(chat`6124913915`)，已`cron run --wait`實測驗證`delivered:true`。
- **盲點監控**：查明這不是新系統，只是MiniMax今晚做rule#07白名單補強時發現的1個測試案例regex邊界問題(19個測試中1個fail)，非功能決策，已請它有空自行補丁即可。
- **peipei-ai-backup舊commit明文金鑰**：評估後決定不重寫git歷史——比照小二Telegram token外洩舊判例(private repo+風險可接受)，維持現況(金鑰已清空+.gitignore已補)，此項結案不再懸著。

### 5. 意外發現：bigtree-tw Netlify部署對中文檔名zip解壓的隱性bug
`5876ed8b`session嘗試部署10/3 KR場EDM連結時連續失敗，軍師介入用自己重新產生、驗證過完全乾淨的zip獨立測試，**同樣失敗**，確認非zip打包方式問題。最終跟`5876ed8b`各自查出根因：**Netlify的zip deploy API對中文檔名/目錄的zip會直接「Deploy failed while extracting zip」**，不論編碼策略(git archive/Python zipfile UTF-8 flag/STORED不壓縮)皆無效，唯一成功策略是完全排除中文檔名。`5876ed8b`已負責任地**restore回9/16最後一次成功的deploy**(`6aaae4738f7bad35092afcb8`)止血，10/3改動暫未上線，已用curl驗證首頁+歷史講座紀錄頁面皆恢復200正常。詳見`claude-brain/reference_netlify_zip_deploy_chinese_filename_2026-09-18.md`(MiniMax撰寫)。**軍師決定**：暫採方案C(不急著把bigtree靜態版中文檔名rename成ASCII)，因為10/3場次的實際使用者入口`event.bymyway.com/curated/bigtree-1003/`(動態版)已驗證正常運作(HTTP 200)，靜態版只是歷史宮格牆的index，非主力入口，不影響教練實際業務需求；未來若要一併解決可批次rename成英文檔名一次到位。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_hook_sender_id_vs_group_id_gating_2026-09-18`延續案例：任何寫死字串的hook注入邏輯，都要考慮「這支hook可能被非預期的觸發者共用」，開工hook的「軍師(Opus)」字串就是一個活生生的反例。
2. AI團隊品質監督的本質：機械式規則(有沒有守規矩)可以完全自動化event-driven稽核，但「這個任務理解/做法是否恰當」的語意判斷仍需要實際讀transcript，無法用regex取代，這是本場對教練誠實揭露的已知限制。
3. `reference_netlify_zip_deploy_chinese_filename_2026-09-18`：任何要走Netlify zip deploy API的repo，若含中文/非ASCII檔名，deploy前務必`unzip -l`檢查，避免重演本場5+2次連續失敗燒掉的部署額度。

## 📋 下一場開工先做
1. **沿用既有待辦**：確認孔大哥/佩佩老師端industry-chain-sop hook真人實測(教練已表態不催收)、峰哥產業服務鏈SOP待Telegram ID、FB App Review(教練自行處理中，已從軍師待辦移除)、`stop_rules_master.py`規則#07誤判regex(教練已示意MiniMax有空自行補丁)。
2. **bigtree-tw中文檔名rename**：非緊急，教練若想讓靜態版也能穩定部署，未來找時間批次rename成ASCII安全命名(`archive/大樹小講_歷史講座紀錄.html`→英文、`archive/2026-07-01_創業x政府xAI講座/`→英文，後者目前無任何連結指向，屬孤兒資料夾)。
3. **agent_team_qa_digest.py上線觀察**：下次開工留意尾段有沒有正確顯示新違規彙整，若MiniMax session之後有新的規則觸發，確認分組/顯示邏輯持續正確。
4. E16接力棒瘦身：主檔v214~v218共5棒，下次開工可考慮把v214~v215搬進archive。

## 🔑 本場commit
`workspace`：`4de7654c0`(開工hook身份判斷修復)+`ca8752418`(AI團隊品質稽核機制+名冊)+本次commit(接力棒v218+幕僚長晨報狀態更新)。cron：`0d64be3c-061d-4ca8-add0-d22862677e59`(幕僚長晨報，非git版控，已用`cron run --wait`驗證取代commit hash為證)。`5876ed8b`session並行產生的commit(peipei決定執行/netlify chinese filename記憶檔等)不在本次commit範圍內，各自獨立commit。

---

> 建立時間：2026-09-18 16:16 ~ 17:23（台灣時間，約1.1小時）
> 上一棒：v217
> 本棒主軸：**教練交辦「更新分會來賓戰情儀表板」，貼兩張週報（真鑫 09/17 應到 22/來賓 1/早鳥 7；真鑽 09/15 應到 48/來賓 13/早鳥 21），本棒從查 DB 狀態→拆邀請人對應→INSERT weekly_data→SUM 對齊教練原始週報，全程自糾「林仁超 4 位來賓一度誤寫 1 位」的 ON CONFLICT 覆蓋 bug。教練當場糾正 2 個關鍵錯誤認知（zhenzuan-webapp 是退役不是真鑽線上 webapp、真鑫 members 24 vs 應到 22 是因 2 人離會），收工前主動補上退役根因（分會名稱不是他要的所以停）。ones/coffee 全部 NULL 守底（守則 #15 沒給不填 0）。**

## 🎯 本場戰果

### 1. BNI 來賓戰情儀表板：真鑫 09/17 + 真鑽 09/15 雙週寫入完成
教練貼兩張週報截圖，本棒逐步：
- **真鑫 09/17**：建立 week row（解卡：`weeks` 表 schema 是 5 欄 `(week_date, label, is_active, note, sort_order)` 不是直覺的 3 欄）→ 吳玫萱（id=64）guests=1（陳柏麟為她邀的來賓）→ 7 位早鳥 early_bird=1（吳志煒/林佳慧/買駿航/連皓宇/范郁琪/蔡姵彤/王聖凱）
- **真鑽 09/15**：建立 week row（**解 4 週停擺**：DB 卡在 08/25 之後完全沒新資料）→ 13 位邀請人按實際邀請數寫入（**自我糾錯發現**：第一次用 INSERT 13 次同一人 `ON CONFLICT UPDATE SET guests=1` 把多人邀請壓成 1，正確應為林仁超=4 / 楊智帆=2 / 康文彬=2 / 其他 5 位=1）→ 21 位早鳥 early_bird=1（20 位直配 + 1 位「羅　琳」id=48，DB 名字是「羅琳」無空格，鍵盤輸入差異）
- **DB SUM 對齊驗證**（教練週報 vs DB）：真鑫來賓 1=1 ✓ / 早鳥 7=7 ✓；真鑽來賓 13=13 ✓ / 早鳥 21=21 ✓
- **ones / coffee 全部 NULL**（守則 #15 沒給就不填 0 假裝），等會員回報再 UPDATE
- **真貴 09/17** week row 已存在但教練沒給本週週報，照教練裁示不動
- **真鑽 webapp（com.coach.zhenzuan-webapp）**：教練確認是退役服務不重啟

### 2. 教練當場糾正 2 個關鍵錯誤認知，已寫入記憶
- **錯誤 1**：把 `com.coach.zhenzuan-webapp` 誤當真鑽線上 webapp，發現 exit -15 就想重啟。教練回「這個本來就是停用的東西，不要浪費那麼多時間」，**真鑽線上 = `real-diamonds.bymyway.com`**，本機 Flask 部署方式不在 zhenzuan-webapp 裡。
- **錯誤 2**：真鑫 `members` 表 24 人 ≠ 教練週報應到 22 人。差 2 位**已離會**：張晴晴 + 楊為凱。
- 已寫入 `memory/reference_chapter_real_names_and_zhenzuan_webapp_retired_2026-09-18.md` + MEMORY.md 索引更新
- **退役根因補釘**：教練收工前補一句「分會名稱不是我想要的所以叫他停了，真鑽有專門的名字」，已 commit `83b0745e1` 加進 memory，未來看到 zhenzuan-webapp 任何狀態都不必再追查。

### 3. INSERT ON CONFLICT 自我踩坑 → 修正 → 寫成 SOP
第一次寫 13 個邀請人時，每人都是 `INSERT ... ON CONFLICT(member_id, week_date) DO UPDATE SET guests=1`，**結果同一人多次 INSERT 都被壓回 1**，林仁超實際邀 4 位變成 1 位。立即修正成正確的 `UPDATE weekly_data SET guests=N WHERE week_date=... AND member_id=...`，並 SUM 驗證=13 對齊教練週報。**教訓**：`ON CONFLICT DO UPDATE SET <col>=excluded.<col>` 的「excluded」是指「這次嘗試 INSERT 的值」，**多次同 PK INSERT 不會累加**，只會覆蓋。多人邀請同一會員必須算總數後一次性寫入。

## ⚠️ 本場教訓（已寫入記憶）
1. `reference_chapter_real_names_and_zhenzuan_webapp_retired_2026-09-18`：BNI 三分會網域↔真名對照表 + zhenzuan-webapp 是退役服務（含退役根因）+ 真鑫 active 名單扣掉離會 2 人 + weekly_data 用 `INSERT ... ON CONFLICT` 模式。
2. **ON CONFLICT DO UPDATE SET 不會累加**（E12「INSERT OR IGNORE 靜默失敗」的姊妹案例）：多人邀請同一會員時，必須先把總數算出來再一次性寫入；多次 INSERT 只會覆蓋。守則 #15「沒給不填」+ #14「提煉」雙重落實。
3. **`weeks` 表 schema 是 5 欄不是 3 欄**：原以為 `(week_date, label, is_active)`，實際多了 `note` 和 `sort_order`。下棒動手前先 `.schema`。

## 📋 下一場開工先做
1. **沿用既有待辦**：BNI 三分會的 ones / coffee 數字還沒給，等會員各自回報再 UPDATE 不影響現有 guests/early_bird。真貴 09/17 不動（教練沒給本週週報）。真鑽線上 webapp 部署方式未查（real-diamonds.bymyway.com 本機 Flask 來源），這次沒動。
2. **commit 待 push**：`workspace` repo 已 commit 但未 push（`git push` 需要 origin 設定，這次只 local commit），下一場開工確認 `git push origin master` 狀態。
3. **E16 接力棒瘦身**：主檔現在含 v217 + v218 共 2 棒完整戰果，總檔案 314KB 接近 312KB 上限警戒線，下場可考慮把 v217 戰果搬進 archive。

## 🔑 本場commit
`workspace`：`3711f7f6c`(BNI 戰情儀表板+總表+memory 首次建立) + `83b0745e10`(補 zhenzuan-webapp 退役根因)。外層 `.openclaw` repo 本場無變更（workspace 被 .gitignore 排除，內層獨立 repo）。


---

