## 🔴 給跨對話框軍師讀的總結摘要（2026-10-06 01:10 台灣時間，Mac 桌面版 Sonnet 5.5，v285，教練說「總結」收工）

**主軸：真誠 10/01 數據寫入；真愛陳心入座信任遊戲；接雲端做完第三步（分支待驗收，未合併）；兩批原稿放進 `docs/source/`；Stop hook 誤判根因修；雲端接著寫了「專屬座位」企劃，等軍師評估。**

### 做了什麼（台灣時間）
1. **22:22 真誠 10/01 例會資料寫入**（聯想來信，Mac 資料庫）：出席 15、早鳥 10、來賓 7（陳佩君 3／楊在珍 3／林佳伶 1），網頁與資料庫核對一致；來信已歸檔；SOP 第 5 節更新（出席欄位已有、在籍 15 位、補教練口語叫法）。備份 `~/github_repos/zhencheng-guests/zhencheng_guests.db.bak-20261005-2222-before-2026-10-01`。workspace `cb37fcd6e`。**沒寫**：報告標題來賓 6 位但名單 7 位（照名單 7；教練若說 6，刪呂官諭那筆）、「大樹執董」（教練本人）、6 個月累計（沒有日期可對應）。
2. **23:14 陳心**（真愛分會、智匯保經）入座信任遊戲 #111：連結分會座位 91、俱樂部成員、頭像用分會名片；正式站驗證；測試紀錄補一行與回退點；備份 `bni-chapters/trust_game.db.bak-before-truelove-chenxin-20261005`。`6ea8df306`。
3. **23:17 回答「雲端任務能不能控制我 Mac 的網頁」**：一般雲端任務不行（Anthropic 隔離虛擬機，碰不到 Mac、Chrome、localhost）；能控制的是本機 Claude（Chrome 擴充、內建瀏覽器、電腦操作），手機用 Remote Control／Dispatch 遙控本機（Mac 要開著）。工具說明提到「雲端對話連結到本人電腦」模式，官方文件查不到、未證實。
4. **接雲端（教練 23:19 同意）**：bni-chapters 加環境變數 `BNI_CHAPTERS_DB`／`TRUST_GAME_DB`（預設不變）、`tests/`（全假名字的假資料庫、`conftest.py` 把「通知教練」換成只記錄不送出、基本盤 11 項，破壞測試驗證過會變紅）、`CLAUDE.md`（給雲端的規則）、`docs/task_step3.md`（任務書）、`requirements*.txt`；`4bcac06`。教練在終端機分頁按「信任此資料夾」後，雲端任務 **task_step3 implementation**（session_01PpSC8vJP5FQUtK1M7grBuU）建立。**雲端已做完第三步**：分支 `claude/task-step3-implementation-kwdkui`、commit `561ede9`（見證留一句話、好友動態只有恭喜、週年與很久沒見、本月見證上限；35 項測試全綠；完成說明 `docs/step3_done.md` 在該分支）。**尚未驗收、未合併 master、正式站還是舊版。**
5. **00:02、00:14 原稿放進 `docs/source/`**（私有倉庫，位元組相同，已掃過無金鑰電話 Email；README 有索引）：game-1004（網頁 5＋md 5）、ai-team-strategy（網頁 1＋原始對話 txt，沒有 md）、team-plan（計畫書 teamwork、企業健身房×團隊計畫提案、策略筆記）、industry-chain（SOP_產業鏈）。`c1dc9a3`、`d6ea92d`、`2c1f3d9`。
6. **Stop hook「HTML Chrome 查證鎖」誤判根因修**（誤報我改了 ai-team-strategy/index.html，其實是複製來源）：cp／mv／rsync 看寫出的目的地、只認指令位置（引號內文字不算）、原樣複製「這段事件之前就沒動過」的舊頁面不算。59 場歷史回測 186 條，舊判 16→新判 15，無新增誤判。`stop_rules_master.py` 的 `_html_written_by_bash`；workspace `2826aa820`、`9cb3d0004`。
7. **教練 00:29 說明（已存記憶）**：**「100 個案例」＝他三四年的見證影片，在 YouTube 非公開連結、不在 Mac**；先做簡短文字版，有興趣申請才限時開放；文字版**不放影片連結、不放可辨識個資**（不確定講見證的人是否還在 BNI）。**「產業服務列」是語音錯字，正確是「產業服務鏈」**（BNI 專用術語：大家共同來服務一個特定族群），做法＝`knowledges/SOP_產業鏈.md`（905 項專業清單），SOP 檔頭已補口語叫法。記憶 `project_100_cases_youtube_unlisted_text_first_2026-10-06.md`、`reference_industry_service_chain_term_2026-10-06.md`；workspace `50e2165bc`。

### 卡在哪／發現
- **雲端分支除了第三步，還有 5 個企劃文件 commit**：`plan_trust_league_v1/v2`（信任聯盟：免費信任遊戲→被見證成候選人→付費 6 人戰隊 90 天賽季）、`plan_seat_v1`（專屬座位 v1：三個新分會的座位攤開給所有人看、被 3 位俱樂部成員見證才能預約 14 天、設計過的初次見面、見面後才決定付費入會）、`for_junshi_seat_review.md`（請軍師評估 7 件事，最新 commit `d7bb0d8`）。雲端說**沒有寫任何座位功能程式**，等軍師評估。教練 00:14 貼的「還缺幾份原稿」就是這個雲端對話在要資料。
- 第三步有 5 個細節預設值已選、列在 `step3_done.md`「需要教練決定」：④的詮釋、留言可否撤回、好友動態要不要上公共頁、90 天門檻、60 字上限。
- 雲端對話容量 34%（00:31）；我建議不重開、一路跑完，叫它讀 docs/source 只讀 README。我問過教練要不要我代傳訊息給雲端（回「傳」），教練沒回。
- 週額度 10/05 20:54 為 76%，週三 13:00（台灣）重置；本對話框已 2.7 小時、多主題，所以收工換新對話框。

### 📋 下一場開工先做
① **驗收雲端第三步**（Sonnet 可做）：`cd ~/github_repos/bni-chapters && git fetch origin` → 用另一個資料夾或分支檢查，**不要在正式站跑的 master 上直接改**；重建測試環境（scratchpad 的舊 venv 不一定還在：`python3 -m venv <暫存>/testvenv && pip install -r requirements-dev.txt`）→ `python -m pytest tests -q`（應 35 項全綠）；**先手動快照 `trust_game.db`**，再拿「複本」跑 `game_db.init_db()` 看遷移；讀 diff 一遍（重點：`trust_game.py` 四個路由結尾的動態偵測有包 try/except、見證留言有跳脫、不新增通知）；沒問題 → 合併到 master → 重啟 `launchctl kickstart -k gui/$(id -u)/com.coach.bni-chapters-webapp` → 對 `trust.bymyway.com/game/` 實測（動態要兩個座位互動才會有）→ 在 `knowledges/2026-10-05_信任遊戲_測試紀錄與回退點.md` 加一行（commit、取消方式、要看的回饋）。
② **評估雲端的「專屬座位」企劃**（`for_junshi_seat_review.md` 的 7 件事）：只讀 `plan_seat_v1.md`、`plan_trust_league_v2.md`、`step3_done.md` 三份（都在雲端分支，用 `git show origin/claude/task-step3-implementation-kwdkui:docs/<檔名>` 讀，不整批讀 docs/source）。核心問題：**版本 A（植入現有信任遊戲）或版本 B（獨立輕量版、先做 12 人市場測試）？**這是策略與設計，**建議切 Opus 5.5 做**；結論重點寫在回覆（教練看不到 md 檔），也可寫回雲端分支。其中「哪三個新分會」「12 人從哪挑」「對外招募付費會籍的說法是否符合 BNI 規範」只有教練能答；「用 taxonomy.json 905 項產生座位清單靜態檔」AI 可做。
③ 沿用 v284 ③：教練實際操作後的回饋（「提醒他」按鈕、見面紀錄「對方確認」、放鴿子逾期、非會員見證分量）＋第三步完成說明那 5 項細節決定。
④ 沿用 v284 ④（第三～五分會、真富／真愛／真鑫菁英表與籌備會名單、買竣淯簡報、每月流程、10/09 後搬家舊夾、宏碁注入確認）原文不變，見下方 v284 該段。

**commit**：bni-chapters `4bcac06`、`c1dc9a3`、`d6ea92d`、`2c1f3d9`（雲端分支 `561ede9`…`d7bb0d8` 未合併）；workspace `cb37fcd6e`、`6ea8df306`、`2826aa820`、`9cb3d0004`、`50e2165bc`；本次總結另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-05 22:10 台灣時間，Mac 桌面版 Sonnet 5.5／Opus 5.5，v284，教練說「總結」收工）

**主軸：信任遊戲「好友／共同好友」機制第一、二步上線；葉佰蒼入座、真鑫名單依 10/08 菁英表更新；bni_tainan 補「BNI 資訊資料庫優先」；教練問「能不能把寫程式交給雲端、落地回本機」（本場收尾，等教練回覆）。**

### 做了什麼（台灣時間）
1. **開工補救**：教練 10/05 04:04～04:08 在 bni_tainan LINE 糾正「BNI 資訊以資料庫為優先、不要上網搜」。補 `agents/bni_tainan/SOUL.md` 最上層規則＋新檔 `knowledge/bni_rank_ladder.md`（教練口述位階：助理大使→大使→董顧→區域董事，區域董事以上資料庫沒有就說沒有）；封存教練舊 LINE 對話（可還原）；新對話實測答對。外層 `4c8f02640`、`70e2536b1`。
2. **19:42 葉佰蒼**（AI 百人導師 #53）入座信任遊戲 #110，**友善夥伴**（BNI 資料查不到，教練確認不是會員）。
3. **19:50 真鑫**依 `1151008真鑫菁英表.pdf`（15 位）移除薛如媛、范郁琪（備份 `~/github_repos/_backups/zhenxin_removed_members_2026-10-05.json`；遊戲座位只隱藏不刪）；真鑫剩 19 位（含 4 張教練／DnA 複製卡片）；第二位姓買的新會員＝買竣淯，已有座位，沒照片沒公司，等簡報。
4. **好友機制**（教練 19:56 構想→研究 FB「10 天 7 位好友」、LinkedIn 完整度／背書；FB／LinkedIn／IG／Threads 好友**無法自動匯入**）：20:12 教練拍板「**不自動加好友，同分會也要本人按**」。
   - 第一步 `8ab8092`：任何兩座位互按「我認識他」、對方確認才算好友；好友列（同分會／跨分會／曾經會員／友善夥伴、想認識他人數、共同好友）；「這台手機是我」cookie（tg_me，一年，誠信制）。
   - 20:36 教練改**互相認識上限「每月 20」→「每天 20」**；第二步 `7b4c4b8`：請共同好友介紹（新表 intro_requests）、你可能認識的人、起步七友（入座 10 天內互加 7 位）、個人頁完整度條。
   - 20:47 教練：BNI 會員身份限制對社交功能多餘 → 查證程式本來沒限制，是社交區塊放在會員關卡後面；`d7f485a` 移出關卡、**見證不限 BNI 會員**。
   - 20:52 教練確認：好友加分**維持「對方確認才算」**（按的人要去提醒對方，互動性才高）。
5. **測試紀錄**（教練 20:47：全是測試、每步留紀錄、不好用就取消）：新檔 `knowledges/2026-10-05_信任遊戲_測試紀錄與回退點.md`（一行一步：時間、commit、怎麼定的、怎麼取消、要看的回饋；**新一步做完在最下面加一行**）；資料庫快照 `~/github_repos/_backups/trust_game_20261005-2055.db`（資料庫不進 git，手動快照，不是自動）。
6. **新反射** R-PROPOSAL-MD-NOT-VISIBLE-TO-COACH＋記憶：教練畫面看不到 .md 提案，重點寫回覆、檔案只當存檔。
7. **雲端銜接**（教練 20:54：週額度已用 76%、週三 13:00 重置、雲端有 $91 credit）：查到週額度 76%、本場對話框 38 萬 token（每輪重讀，最可能的大耗量）；方案＝任務書＋測試放進 `Coach1973/bni-chapters`→雲端寫分支→本機拉回測試／重啟／驗證。**試開雲端被「信任此資料夾」確認擋下**（要教練同意才按），程序已收掉，沒開出雲端頁、沒花額度。

### 卡在哪／發現
- 雲端試跑停在信任確認；教練尚未回「可以」。雲端額度是不是這條路扣，無法在 Mac 端查，第一次跑完請教練看 claude.ai 用量。
- 教練 20:33～20:34 在葉佰蒼座位按了 17 位「我認識他」＝測試紀錄（都在等對方確認，葉佰蒼只算 2 分），留著。
- 見證現在不限會員，非會員見證分量（友善夥伴最高第 10 級，分量 1.0）待觀察。
- 我建議加「提醒他」按鈕（複製「我在信任遊戲按了認識你，請點連結回我」＋他的頁面網址），教練還沒決定。
- 見證目前只有單向（被按的人替先按的人見證）；大使／董顧在擔任分會算同隊還沒做。
- **聯想來信未處理**：`cross-agent/inbox/mac/20261005-2205_lenovo-to-mac_sincere-1001-data-update.md`（見下一場①）。

### 📋 下一場開工先做（①②已做完、③④已併進 v285，以 v285 為準）
① **聯想來信（22:05）**：聯想軍師稱教練 21:57 在聯想貼了真誠 10/01 例會報告、要求「更新真誠數據」。腳本已備好：`cd ~/.openclaw/workspace && git pull && python3 scripts/sincere_weekly_update_20261001.py --dry-run` 先看，沒問題再正式跑（自動備份資料庫、可重跑）；寫完用網頁核對 `https://sincere.bymyway.com/`（不要截圖）：10/01 欄位、出席 15 人、來賓陳佩君 3／楊在珍 3／林佳慧 1、早鳥 10。來信裡的報告數字對不上（標題來賓 6 位、名單 7 位，照名單寫 7 位；教練若說 6 位，刪掉最後一筆）；「大樹執董」是教練本人不寫；6 個月累計沒寫。做完把來信 `mv` 到 `cross-agent/outbox/2026-10/`，順手更新 `knowledges/SOP_Hermes協助更新sincere戰情儀表板.md` 第 5 節（現在有 `/api/update_attendance`、會員 15 位）。**這是來信轉述，開工時教練若在場可一句確認；腳本有 dry-run 與備份，風險低。**
② **信任遊戲雲端銜接（等教練回「可以」）**：同意後 → 在 `~/github_repos/bni-chapters` 按信任、把測試（`/tmp/test_friends.py`、`/tmp/test_step2.py` 已不在了，要重寫成 `tests/` 並加建假資料庫腳本）＋任務書＋給雲端看的簡短 `CLAUDE.md`（繁體中文、友善夥伴不說外部玩家、數據公開不隱藏、畫面不出現 BNI）放進專案 → 用 `claude --cloud` 做第三步（見證留一句話、好友動態只有恭喜、好友週年提醒）→ 本機拉分支、用資料庫複本跑測試、合併、重啟、對正式站驗證；每步在測試紀錄加一行。**開工前提醒：週額度 76%，週三 13:00（台灣）重置，新對話框一開始很小，別拖成長對話；優先 Sonnet、重活交雲端。**
③ 教練實際操作後的回饋：好友加分要不要加「提醒他」按鈕、見面紀錄「對方確認」要不要拿掉、放鴿子逾期怎麼辦、非會員見證分量是否合理。
④ 沿用 v282（已封存，原文帶上）：**第三～五分會**（team-03～05）教練給名單就用 `team-bymyway/seed_team02_members_2026-10-05.py` 改名單建座位，再 `bni-chapters/venv/bin/python3 seed_team01_players_2026-10-05.py team-0N` 排進遊戲，重複人名以戰情表為主；真富／真愛／真鑫菁英表、籌備會名單來了建座位＋`import_detector_stats_2026-10-05.py <slug>`（真愛放陳佩君老師複製卡片，標籤「真愛分會大使」）；買竣淯簡報來了抽照片（照投影片顯示比例）補上；每月流程（領導換屆重跑 `sync_official_photos_2026-10-05.py`、`seed_leadership_2026-10-05.py`，地區報表→`import_light_scores`＋來賓總覽＋`import_detector_stats`）；10/09 後搬家舊夾（先確認捷徑指向的資料是活的、走五道閘門）；宏碁下次開工確認注入約 9KB（聯想／宏碁共用的開工 ps1 聯想 10/05 22:15 已瘦身 42KB→9KB；聯想 E 槽備份提醒 21:56 已講，這兩項不用再做）。

**commit**：bni-chapters `8ab8092`、`7b4c4b8`、`d7f485a`；外層 `4c8f02640`、`70e2536b1`；workspace `9d67f7abe`、`164840dfa`、`3430035f9`、`4eec6ebd9`、`847291d83`、`5b58bbccd`、`6fb4ffbfb`；本次總結另計。

---

> 📦 v282完整內容已封存：`handoff_archive/handoff_v282_archived_2026-10-05.md`（信任遊戲三分會連結＋第一、二分會夥伴＋金質獎章區＋真鑫／真鑽一頁式簡報＋官方照片同步；原「下一場開工先做」已併進 v284 ④）


> 📦 v283完整內容已封存：`handoff_archive/handoff_v283_archived_2026-10-06.md`（信任遊戲友善夥伴玩法第二步＋規則關卡；原「下一場開工先做」已併進 v284 ④、v285 ④）

> 📦 v281完整內容已封存：`handoff_archive/handoff_v281_archived_2026-10-05.md`（信任遊戲測試版上線 trust.bymyway.com、94 位入座、DnA 名單；原「下一場開工先做」已併進 v282）
> 📦 v280完整內容已封存：`handoff_archive/handoff_v280_archived_2026-10-05.md`（積分表 v2＋探測器擴真鑫／籌備會＋本屆領導團隊標籤＋DnA 多重身份＋官方照片同步；「下一場開工先做」①②③已搬進 v282）
> 📦 v279完整內容已封存：`handoff_archive/handoff_v279_archived_2026-10-05.md`（探測器第一版上線＋帶來賓改用官方 PALMS＋來賓總覽／真鑽戰情表／燈號自動帶入；未做完的項目已併進 v280、v281「下一場開工先做」）
> 📦 v278完整內容已封存：`handoff_archive/handoff_v278_archived_2026-10-05.md`（《AI企業團隊戰略》原話報告書＋真誠正式照與一頁式簡報＋真鑽空座位按鈕與教練卡片；未做完的項目已併進 v280「下一場開工先做」）
> 📦 v277完整內容已封存：`handoff_archive/handoff_v277_archived_2026-10-05.md`（真鑽 47 席上線＋信任裝備探測器方案 v2 定案＋積分表 v1 拍板；仍未做完的項目已併進 v279「下一場開工先做」）
> 📦 v276完整內容已封存：`handoff_archive/handoff_v276_archived_2026-10-05.md`（商務遊戲第二～四批問答＋積分表 v1＋Keynote／輔助鍵盤插話）
> 📦 v274＋v275完整內容已封存：`handoff_archive/handoff_v274_to_v275_archived_2026-10-04.md`（v274 手機版：AI 百人導師架構＋商務遊戲題庫＋原話報告書＋curation-watch 修復／v275 大樹小講 bigtree-1107＋ema1017＋歷史頁自動補登＋kr1003＋macOS 26.7.1；10/04 收工整理時搬出，仍未完成的項目已併進 v277「下一場開工先做」④⑤）
> 📦 v273完整內容已封存：`handoff_archive/handoff_v273_archived_2026-10-04.md`（v273 macOS 26.7.1 更新＋BNI 信用證補登＋空間盤點＋10/03～04 大樹小講零碎記錄；10/04 整理接力棒時整段搬出）
> 📦 v272完整內容已封存：`handoff_archive/handoff_v272_archived_2026-10-04.md`（開工注入瘦身v3＋〈為你轉身〉導師席換八位＋ema1017流程＋team01戰情表「未來週次不開放填寫」）

---

## 🎯 「賈維斯成長計畫」（簡稱「反射條件」）進度（2026-10-02 07:10 瘦身版；詳細交辦段與第 1~3 步經過已封存 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`）

教練 02:30 原話：教練訓練出來的每個 AI 都要有條件反射；三種標準＝有智慧的反應、聽懂人話的反應、準確做事情的反應；對外服務再加「讓人備受禮遇、被尊重，惦記用戶說的話，不把問題丟回給用戶」。已全權授權，**不准再拿細項問教練**。

| 對象 | 狀態 |
|---|---|
| ① 教練自己的 AI | 小龍蝦端外掛 reflex-prompt／member-context／coach-context 上線；Mac 軍師 hook 85 條反射；**聯想 10-02 07:45 已接上並回信（Mac 驗收過：commit `bee1a7653` 存在、`pick_next_task.py` 在 Mac 接力棒實跑輸出正確、ps1 有 BOM 且呼叫它；聯想自己的反射／擋下是用管線模擬，要等教練在聯想開新對話框才算真實驗收）；宏碁 10-02 09:15 已接線並回信（裝了 Python 3.12、加 5 個 hook，用模擬事件測過反射與擋下；開工置頂🎯等聯想推上去後會自動帶到，真實新對話框畫面待教練下次開新對話框才算驗收）** |
| ② 四位夥伴分身 | ✅ 10-02 04:20 SOUL.md「三種標準（夥伴版）」＋群組 session 封存＋真實路徑測過（見 v269） |
| ③ LINE 對外帳號（禮遇版） | ✅ 人設上線（v268）；**真實 LINE 會員流量還沒驗證**（看 `state/member_context.log` 第 4 欄 `sender:u…`） |
| 試金石 97 案／記憶 171 條 | ✅ 全部有去向，`python3 scripts/reflex_coverage.py` 未處理 0、斷鏈 0 |

✅ 開工已改成「心法＋最新一棒」（10-02 14:2x，注入 30KB→9.7KB，全域與 workspace CLAUDE.md 開工鐵律同步改 v3）；之後：Stop hook 只留行為檢查、拿掉字眼檢查。待查：`handoff_sync_guard.sh` 判斷1 用 PreToolUse＋stderr＋exit 0 提醒，AI 可能看不到。量尺：教練訊息「重講」比例 5月19%／6月13%／7月14%／8月12%／9月16%，重跑 `python3 scripts/render_top30_report.py` 看 10 月有沒有降。

> 📦 v264（Mac 10-01 22:20，小龍蝦卡核准修好、第一分會雙週＋口頭填數據、Tailscale 三台＋手機入網）完整內容已封存：`handoff_archive/handoff_v264_archived_2026-10-02.md`

---

> 📦 v262（聯想 10-01 18:50，RustDesk 中繼故障→Tailscale、BNI 簡報 3 份）＋v263 宏碁（10-01 21:50，真鑫戰情表、宏碁 Tailscale＋RustDesk 直連）完整內容已封存：`handoff_archive/handoff_v262_v263acer_archived_2026-10-02.md`

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
（目前沒有；10/05 20:54 問的「雲端銜接」教練 23:19 回可以、已按信任，結案）


### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- 手機出門用行動網路輸入 Tailscale 100.x 位址連 RustDesk 實測（v264，教練要出門用時再測）
- RustDesk 直連實測：聯想→ACER（ACER 100.78.106.14:21118，ACER 離線就等醒來）、ACER→Mac 教練還沒回報（v263，教練要用時再測）；官方中繼 21117 修好後再驗證
- 聯想 `E:\Claude-Data\` 殘留 ai-class-1017.zip／ema1017.zip／pk2／zpk／cookie.tmp（刪檔鎖擋，需教練同意才清，v263）
- 怡靜群若回「沒有填121功能」→封存該群 session 重來（v264，教練或怡靜反映時處理）
- 小龍蝦一次處理多張名片照片：程式讀過用 card_splitter 切圖但沒實跑（v264，教練要時找一張多卡照片實跑）
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
- 手機遙控開機自動啟動（現在重開機就消失、要 AI 手動重跑；10/03 問過一次，教練只回「搞定了」沒回這題）
- 第一分會「陳迎薰、王純藝」：教練名單有、戰情表沒有，當新增夥伴加了、專業類別空白（教練名單寫投資型保單、行動美容；v282，教練沒再提就不問）
- 「100 個案例」整理成簡短文字版（教練 10/06：影片在 YouTube 非公開連結，整理需要時間，先知道就好；教練開始整理再動，不放影片連結與個資）
- `docs/source/` 之後有新原稿再補（教練或雲端貼清單才放，先查 README 索引）
- 雲端第三步的 5 項細節決定（預設值已選，見 `step3_done.md`；教練玩過有想法再說）

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟡 | **bni-chapters 雲端協作（10-06）** | ⏳第三步分支待驗收、專屬座位待評估 | 步驟見 v285 ①②。基礎建設：`tests/`（假資料庫、`conftest.py` 擋掉通知教練）、環境變數 `BNI_CHAPTERS_DB`／`TRUST_GAME_DB`、雲端用 `CLAUDE.md` 規則；雲端只看得到專案，要給它資料請放 `docs/source/`（README 為索引）；`claude -p "訊息" --cloud session_01PpSC8vJP5FQUtK1M7grBuU` 可代傳訊息給雲端任務（要教練先同意）。 |
| 🟢 | **MEMORY.md 超過 200 行（約 204）＋記憶檔命名檢查提示 `project_netlify_deploy_quota_2026-07.md` 不合規** | ⏳AI 自己找時間做 | 合併已過時（⛔）與同主題的索引行，只留一行一則；改名時同步改索引連結。不問教練。 |
| 🟢 | **team 站分會／友好夥伴後續（10-05 v282）** | ⏳教練給第三～五分會名單才做 | team-bymyway 認座位功能已上線；友好夥伴在 team 站補照片不會同步進遊戲（可寫小同步腳本）；金質獎章得主未寫進探測器（只知等級、不知推薦人數，等教練給數字）；「分會之光 vs 分會精神」模板規則要不要改（教練沒問就不動） |
| 🟡 | **信任遊戲／分會座位（10-04 軍師）後續** | ✅探測器已上線（真鑽、真誠、真鑫；籌備會程式已支援但 0 座位）；積分表 v2 已交 | 見 v280「下一場開工先做」。**AI 自己的程式待辦（不問教練）**：「近三年」視窗（`trainings_json` 要改成連月份一起存才切得出來）、培訓分值表、遲到／早鳥接進探測器、領導標籤版面拿到截圖許可後親眼看一次、真鑫戰情表 24 人 vs 會期報告 17 人要核對（張晴晴、楊凱為戰情表是現任但不在報告；范郁琪、薛如媛戰情表標離會但在報告，座位以報告為準）、`scripts/reflex_coverage.py` 列出的幾個 10/01～10/03 記憶檔尚無反射去向。DnA 的啟動董事／支持與增長董事／區域董事分數教練沒定，不主動問。技術備忘沿用：技術備忘：bni-chapters 的 `chapter_members.claim_phones`（不是 NULL＝依菁英表建的座位；內容是菁英表手機，只留存不顯示、DB 不進 git、repo 私有）、`claimed_at`＝第一次補資料時間、`member_edit_log` 存舊資料可還原；前台不能刪座位，要下架請直接改 DB。柯朝陽、蘇志揚已離會，不在名單。 |
| 🟢 | 〈林士民〉shihmin 頁手機上形象照框偏窄（`img` 的 `height="552"` 屬性蓋過 CSS `aspect-ratio`，舊照片也是這樣） | ⏳低優先-沒要求不動 | 要改只需在 `.portrait img` 加 `height:auto`；教練只要求換照片，N7 不順手改。 |
| 🟢 | 記憶檔名不合規：`claude-brain/project_netlify_deploy_quota_2026-07.md`（commit hook 每次提示，應改 `<type>_<snake_case>.md`，描述用底線） | ⏳低優先-AI自己改 | 10/04 commit 時發現，舊檔非本場造成；改名時同步改 MEMORY.md 索引連結，不用問教練。 |
| 🔴 | **賈維斯成長計畫（反射條件）總進度（v265~v269）** | ✅第 1~4 步完成，剩 2 項等外部 | 第 1 級反射 hook＋小龍蝦外掛 reflex-prompt／member-context／coach-context／url-typo-guard；禮遇版人設；四位夥伴三種標準；試金石 97 案＋記憶 171 條全有去向。**剩**：①真實 LINE 流量驗證 `state/member_context.log` 第 4 欄 `sender:u…` ②聯想／宏碁回信驗收。測試法：外掛類走 `openclaw gateway call agent`（記憶 `feedback_openclaw_hook_fire_and_forget.md`），分身類封存群組 session 後用真實語音句前後對照。詳細見 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`。 |
| 🟡 | **Mac 備份改四條（10-02 教練定，取代每小時）＋Amber 空間** | ✅四條都上線；⏳明早 08:10 首次點名備份待看 | 【10-02 11:40 完成】上限 QuotaGB=150 已生效；刪 3 天前 12 份（35→23，留 09-29 23:40 起），備份映像內用量 142→119GiB。密碼改用 `scripts/coach_password_dialog.sh`（sudo -A，教練看得到）。Amber 本身空間有沒有回升，下次看 Amber 通知（AI 分類 >15% 才恢復）。以下為原規劃：①點名正常才備份 `daily_team_rollcall.py backup_when_healthy`（launchd 環境實測 startbackup exit=0）②升級前必備份 反射 `R-BACKUP-BEFORE-UPGRADE`（14 例全對、回測 11/39091 全是真升級）③上限 150GB＋刪 3 天前 12 份：App 終端機分頁「備份設定：只差輸入密碼」跑 `scratchpad/tm_setup.sh`，教練輸入密碼後看 `tmutil listbackups|wc -l`（應 34→22 左右）與 `defaults read /Library/Preferences/com.apple.TimeMachine` 有無 Quota；scratchpad 會清掉，腳本要留就搬進 scripts/ ④排除 `.cache/.npm/.rustup`（約13GB，`.nvm` 刻意保留）。**明早 08:10 首次點名要看到「💾 備份：全員正常，已自動備份一次」**。教練頻率已自己改手動（AutoBackup=0）。記憶 `project_mac_backup_policy_good_state_and_pre_upgrade_2026-10-02.md`。 |
| 🟢 | `reflex_coverage.py` 記憶索引斷鏈 2 筆（聯想 bee1a7653 合併索引帶進來的 `feedback_single_html_work_download_images_and_zip_myself_2026-10-02`、`reference_rustdesk_direct_ip_over_tailscale_2026-10-01`，Mac 沒有這兩個檔） | ⏳待處理-低優先 | 從聯想 claude-brain 取回檔案或改索引；補進 memory_ledger。 |
| 🟢 | Claude 自動記憶索引 `~/.claude/projects/-Users-bymyway--openclaw/memory/MEMORY.md` 已 188 行（200 行起截斷），要壓到 140 行內（10-03 hook 提醒） | ⏳待處理-低優先 | 比照索引底部「📦 舊記憶主題分組彙整」做法，把 08~09 月已固化的 🔴 單篇合併成主題分組行；只合併索引行，不刪記憶檔。 |
| 🟡 | kong 的 `agents/kong/SOUL.md` 第 3 行寫「唯一指定模型 MiniMax M2.7」，但 `openclaw.json` 的 kong 實際是 `minimax/MiniMax-M3`（peipei 的 SOUL 06-03 已升 M3）（10-02 v269 發現） | ⏳待處理-低優先 | 設定檔與人設矛盾，無害但別讓 kong 以為自己被鎖在 M2.7。查 kong 升 M3 的授權日期（git log／記憶）後補一行更新紀錄，比照 peipei SOUL.md 第 6~8 行寫法；找不到授權紀錄就維持現狀不動。kong 是獨立 repo（`agents/kong`），改完在該 repo commit+push。 |
| 🟡 | **BNI簡報3份（藍圖／生態圈／商戰制勝密碼）底部字幕開頭被左下LOGO保護區蓋掉**（10-01聯想，v262） | ⏳等教練選（已問過1次，不追問） | 檔案在`D:\Users\Downloads\BNI版簡報\`。教練選「內縮排版」才改`scripts/pdf_to_branded_pptx.py`重跑；選「照現狀」就結案。poppler在聯想不在PATH（見v262）。 |
| 🟡 | **Tailscale雙機互連（聯想tree 100.95.122.29／Mac 100.91.228.91）＋RustDesk官方中繼21117故障** | ✅聯想→蘋果已通；⏳等RustDesk官方修復 | 聯想桌面捷徑「連蘋果電腦」＝TigerVNC。蘋果→聯想教練不需要（RDP已開、Windows密碼教練不記得，教練要用才自己設）。RustDesk不卸載。 |
| 🔴 | **策展網站全面GitHub化收尾（09-30教練交辦，10-01教練已切bypass＝授權）** | ⏳下一場直接做 | 工具`scripts/curated_git.py`已備妥：跑`ensure-all`補11站→接回`curation_process.py`三條上架路（github_note，大樹作品/全新店家/暫代頁覆蓋）→event-signup加`/hooks/github-curated`(HMAC)＋每repo掛webhook→聯想宏碁`feed_junshi_handoff.ps1`加「貼event /curated/網址→指路GitHub」＋Mac `projects/INDEX.md`策展卡→模擬聯想push驗證線上換新；順手清ema/huitou origin夾帶的GitHub金鑰。 |
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

> 📦 v112～v267 各棒的封存檔名一覽已搬到 `handoff_archive/INDEX_舊棒封存指標_v112-v266.md`（v266~v267 另見 `handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`）（2026-10-02，主檔只留最新兩棒＋待辦表）
