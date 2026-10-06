## 🔴 給跨對話框軍師讀的總結摘要（2026-10-06 23:45 台灣時間，Mac 桌面版 Code 分頁，Sonnet 5.5，v288，教練說「總結」收工）

> ⚠️ **教練 Claude 額度已用到約 89%，週三 10/07 13:00 重置，他打算那時才請軍師開工。下一場請省著用：照下面「下一場開工先做」的省額度順序，不要整批讀 docs、不要 cat 三封信全文（摘要都在這裡）。**

**主軸：座位第 1～3 步驗收上線；雲端成果全部收回本機；第 4～6 步教練已在既有雲端對話做完（還沒驗收、沒上線）；Stop hook 連修多次誤判。**

### 做了什麼（台灣時間）
1. **17:14 驗收座位第 1～3 步**：丟棄式 worktree rebase → 1 項過期測試改用空資料夾、同名接力棒改名、網址統一 `/game/seat-map` → 56 項全綠 → 正式庫複本跑遷移（90 座位、111 玩家不變）→ 合併 master（bni-chapters `28e6e63`）→ 重啟 → 對 `trust.bymyway.com` curl 實測（三分頁各 30 座位、無禁用字）。快照 `trust_game.db.bak-before-seats-step123-20261006`；紀錄寫進測試紀錄檔（workspace `b2ecc711a`）。
2. **守則 hook 連修（都有迴歸測試 `bash scripts/test_stop_rules_master.sh` 24/24）**：#07 偵測器補洞（`a4f9087de`）、L2 測試資料補齊（`7eab6fc69`）、工具輸入若在維護偵測器本身不掃（`8d4d9b7bf`）、「指定時間」的「定時」不再誤判（`1b0563269`）；#12 把慣用語「點頭」當叫教練點擊的誤判（`85849e222`）。
3. **pxpipe（把上下文轉圖片省 token）**：查證存在（teamchong/pxpipe），但中文只「保守可用」、精確字串（hash／路徑／ID／人名）會安靜讀錯、桌面版與手機遙控接法對不上 → **教練 10/06 親口：不裝，結案，不再提。**
4. **雲端成果全收回本機**：掃 76 個倉庫，只有 bni-chapters 有雲端分支；三缺文件 8 份併進 master（`eddaf5c`）、總交接信（`69d0b03`）、雲端新規則（`01d96e7`）；`scripts/cloud_letters.sh` 原本因 Mac 沒有 `timeout` 指令從沒真的 fetch，已修並驗證（`442d7a62d`）；記憶 `reference_cloud_work_map_and_where_lessons_live_2026-10-06`。
5. **教練糾正（19:32）**：三缺頁是他獨立做，做好自己會說，不准拿價格／公開／網址問他 → 試金石案例106、🙋區清空、整條移🤫（`48bb9ce97`）。
6. **寫好座位第 4～6 步任務書**（`docs/task_seats_456.md`、`docs/next_task.md`、bni-chapters/CLAUDE.md「教練說開工＝讀 next_task.md 直接做」，master `b9d461c`）。教練在**既有雲端對話**（分支 `claude/optimistic-tesla-mi1zag`）說開工，雲端 19:52 做完，之後又重挑兩個分會清單。

### 🔴 雲端現況（三封信摘要；信在 `claude/optimistic-tesla-mi1zag` 的 `docs/to_junshi/`，**我沒標已讀**，開工 hook 會列出，驗收完才 `mark`）
- 分支領先 master **12 個 commit，可快轉合併（`git merge-base --is-ancestor` 已驗）**，雲端回報 **110 項測試全綠**（`master` 是 56 項）。
- **第 4～6 步**：`a79f7a2`（預約初次見面，新路由 `/game/seat-map/reserve`、`/reserve-cancel`）、`3579419`（到期釋出，頁面載入時檢查）、`29b511f`（後台 `/game/seat-admin/<簽章>`、`make_seat_admin_link.py`）。沒新增欄位、沒通知、沒排程；`git revert` 要由新到舊。
- **雲端動到已驗收的舊程式（請特別看）**：①`trust_game.py` `seat_map()` 補一行顯示 `notice／error`（第 3 步原本座位地圖頁看不到「已記錄」那句）；②`6bfccda` 換清單時移除「不在新清單、仍是空位、從沒人想坐過」的舊座位（改 `game_db.py`、`seat_lists.py`；有紀錄的座位一律保留，因為刪座位會連 `seat_claims` 一起 CASCADE 刪）；③`274a6b3` 真功夫換 5 項、真樂齡換 4 項（只改兩個 json）。
- 雲端另提三件事，**我已查證**：(a) `judge()` 沒金鑰會用備用金鑰 `"x"` → **正式站程序有設 `BNI_CHAPTERS_SECRET_KEY`（長度 48，10/06 23:40 實查），風險不存在**；(b) 座位地圖每載入寫 90 次資料庫（我本機實測 19 ms，雲端 132 ms；人多才可能卡，**低優先**，建議只在清單真的變了才寫）；(c) 座位標「已入會」後沒有畫面能改回空位（只能改資料庫，低優先）。
- 雲端提議可清理（**要教練同意才刪**）：遠端分支 `claude/seats-step123`（內容已進 master）、`claude/task-step3-implementation-kwdkui`（已完全併入）、`claude/optimistic-tesla-mi1zag`（驗收併入後）；教練雲端帳號的私有頁「給軍師的交接信」已過期。
- 教練在雲端確認：真功夫、真樂齡「服務對象方向正確」「真樂齡四象限方向正確」；**三個分會座位可以跨分會重複**（雲端曾自加互不重複，教練糾正已拿掉）。**30 項逐項看過、真功夫第四象限排序：還沒確認。**

### 📋 下一場開工先做（省額度順序；≥ 週三 13:00）
① **驗收座位第 4～6 步＋清單改動**（只讀這三處的 diff，**不要讀 tests、不要 cat 三封信**）：`trust_game.py`（`seat_map` 的 notice 補丁、`seat_reserve`／`seat_admin`／`_seat_admin_ok`）、`game_db.py`（`start_seat_talk` 條件式更新搶座位、到期釋出、換清單移除舊座位）、`seat_lists.py`。流程：先 `cp trust_game.db trust_game.db.bak-before-seats-step456-<日期>` → 建暫時 venv（`python3 -m venv /tmp/tv && /tmp/tv/bin/pip install -q -r requirements-dev.txt`，上一場的在 scratchpad 已失效）在 bni-chapters 跑 `pytest tests -q`，預期 **110 passed** → `git merge --ff-only origin/claude/optimistic-tesla-mi1zag` → `launchctl kickstart -k gui/$(id -u)/com.coach.bni-chapters-webapp` → curl `/game/seat-map?chapter=real-ai|real-kungfu|real-age`（各要 30 個座位、無「保留／專屬給／你的座位／BNI」）→ 查 `sqlite3 trust_game.db "select chapter,count(*) from seat_slots group by 1; select count(*) from seat_claims;"`（換清單後每分會 30、確認沒有舊座位殘留）→ push master。
② **產生教練的後台連結**：金鑰從執行中的程序取、不要印出來：`KEY=$(ps eww -p $(launchctl list | awk '/bni-chapters-webapp/{print $1}') | tr ' ' '\n' | sed -n 's/^BNI_CHAPTERS_SECRET_KEY=//p'); BNI_CHAPTERS_SECRET_KEY="$KEY" python make_seat_admin_link.py` → 印出的 `/game/seat-admin/<簽章>` 接 `https://trust.bymyway.com` 給教練（連結不會過期，換網站金鑰才失效，且會連放鴿子判定頁已發的連結一起失效）。
③ 收尾：`docs/next_task.md` 改成「目前沒有任務」（雲端沒動它）；`bash scripts/cloud_letters.sh mark`；在 `knowledges/2026-10-05_信任遊戲_測試紀錄與回退點.md` 加一行（含取消方式：`git revert` 由新到舊 `29b511f 3579419 a79f7a2`，清單改動 `274a6b3 6bfccda` 可各自退；整庫還原用上述快照）。
④ AI 自己的事（不問教練）：見 🔧 清單新增三項（座位地圖每次寫 90 次、已入會不能改回、CLAUDE.md 鏡像停擺；額度緊繃時動手前先跟教練說一聲）。
⑤ 沿用 v285 ③（原文在 `handoff_archive/handoff_v284_to_v285_archived_2026-10-06.md`）：教練實際操作信任遊戲後的回饋、第三步 5 項預設值、第三～五分會等。教練說自己的線（三缺頁）不追。

**commit**：bni-chapters `28e6e63` `eddaf5c` `69d0b03` `01d96e7` `b9d461c` `5691bf0`；workspace `b2ecc711a` `a4f9087de` `7eab6fc69` `8d4d9b7bf` `1b0563269` `85849e222` `442d7a62d` `48bb9ce97`；本次總結另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-06 17:20 台灣時間，Mac 手機遙控 Remote Control，Sonnet 5.5，v287，教練說「總結」收工）

**主軸：手機 13:11 開工後，查出「雲端對話寫的信軍師收不到」的根因，兩頭補上固定路徑；讀完雲端的交接信（座位第 1～3 步在雲端分支）；守則#07 輪詢偵測器誤判，改設計做到一半被安全檢查擋下。座位第 1～3 步的驗收這場沒開始。**

### 做了什麼（台灣時間）
1. **13:11 開工、讀信**（Mac 信箱空）；Stop hook 兩項補正：時間要標台灣時間、補記憶索引 `feedback_coach_chinese_file_mapping.md`（`fdad9ca8d`）。
2. **讀雲端交接信**：教練貼雲端頁面連結要我複製；守則#12 改成直接從倉庫分支讀 `origin/claude/optimistic-tesla-mi1zag:docs/letter_to_junshi_2026-10-06.md`（`23b2a0f`）。要點：座位第 1～3 步在 `claude/seats-step123`（最新 `bea0091`，56 項測試 55 過 1 失敗）；「三缺」文件在 `claude/task-step3-implementation-kwdkui`（最新 `b33887f`，8 份）；兩分支 rebase 到 master 無衝突。
3. **14:28 教練追問「雲端寫信為什麼軍師收不到、要給他正確路徑」**。根因兩頭都漏：雲端只接 bni-chapters、碰不到 workspace 的 `cross-agent/inbox/mac/`，而 bni-chapters/CLAUDE.md 沒寫信放哪；Mac 的「讀信」只看 inbox/mac。修法：雲端規則＝信放自己分支 `docs/to_junshi/YYYYMMDD-HHMM_cloud-to-mac_主題.md` 並推上去（bni-chapters master `afa34c4`）；Mac 端新增 `scripts/cloud_letters.sh list|cat|mark`（掃所有遠端分支、以檔案內容雜湊記已讀），開工 hook `feed_junshi_handoff.sh` 有未讀就列在最前面，反射 R-CROSS-LETTER 也叫跑它；用丟棄式測試倉庫＋真實乾跑驗證過。workspace `b6c124674`；記憶 `reference_cloud_letters_to_junshi_path_2026-10-06`。
4. **守則#07 輪詢偵測器誤判**：它把我寫的「每次開工多約 1～2 秒的雲端檢查」當成定時輪詢（規則「每.*秒.*檢查」太貪婪；白名單已補過 4 次治不好，依試金石反射改設計）。我把規則改成「『每』後面要緊接（數字）時間單位」，但寫的時候把數字誤設成必填，歷史紀錄回測會放過「每小時查一次」這類真輪詢。要把必填改成選填（一個字元）時，被自動模式安全檢查以「改自己的守門檔」為由擋下；我沒繞過，停手回報。**這個半成品已被 14:37 的 session-end 自動同步一起提交（`d63575338`），線上版有缺口。**
5. **收工查證發現上一棒寫法過期**：雲端第三步早已合併進 master（`3a9ba09`，「軍師驗收：34 項測試全綠、複本遷移通過」）；座位企劃評估也早已做完（`518b731`：選版本 A 最薄一層、不做 B）。所以 v285 ①②已完成，不用再做。

### 卡在哪／發現
- **雲端信列的待修項**：①`tests/test_seats_step2.py::test_three_real_chapter_tabs_show_coming_soon` 前提過期（真名單已在 master，建議 monkeypatch 名單資料夾為空夾）；②兩分支各有一份 `docs/handoff_2026-10-06.md`，會 add/add 衝突（改名其一）；③文件與任務書寫 `/game/seats`，程式是 `/game/seat-map`；④`seats_step123_done.md`「卡住的事」與 task-step3 分支的接力棒已過期。
- 已開著的雲端對話仍是舊規則，要先 pull master 或被告知新路徑才會寫到 `docs/to_junshi/`；task_step3 implementation 的 id＝`session_01PpSC8vJP5FQUtK1M7grBuU`，optimistic-tesla 的 id 不明。
- 開工 hook 注入「身份等級：特助（MiniMax-M3…）」，實際模型是 Sonnet 5.5（軍師）；已以實際為準，hook 那行尚未修。
- 守則#07 偵測器缺口：已問過教練一次（10/06 17:00 左右），沒回覆，**依 N2 不追問**。

### 📋 下一場開工先做
（v287 當時的四項：①②已完成、③④併進 v288 下一場開工先做。）

**commit**：workspace `fdad9ca8d`、`b6c124674`、`d63575338`（含偵測器半成品）；bni-chapters `afa34c4`；本次總結另計。

---


> 📦 v286完整內容已封存：`handoff_archive/handoff_v286_archived_2026-10-06.md`（聯想 Windows：真誠 10/01 驗證、開工 ps1 瘦身、Zoom 錄影搬 D 槽）；原「下一場開工先做」已併進 v287／v288。

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
（目前沒有。10/06 教練糾正：轉述雲端／其他 AI 寫的「待決定」前，每項各自過 N2 三關，不准整段搬進來——案例106）


### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- **座位第 4～6 步的三個小決定**（教練已在雲端對話看過，不卡上線，不主動問）：後台「已入會／釋出」要不要確認視窗、取消預約後「想坐」要不要自動回來、洽談中見證被撤回洽談要不要中斷；另真功夫、真樂齡換掉的 9 項專業還沒被教練逐項確認、真功夫第四象限排序。
- **pxpipe**：教練 10/06 親口不裝，結案，換任何說法都不再提。
- **三缺行銷頁**：教練自己獨立製作，做好會自己告訴我（10/06 19:32 親口）。**不問價格／公開／數據來源／影片／網址／申請觀看通知**；文件 8 份已併進 bni-chapters master 備查。
- 座位清單內容待教練哪天提起再換：`real-age` 主軸、`real-kungfu` 第 4 象限、年底成立哪幾個（只是換 `data/seat_lists/*.json`，不卡任何程式）。
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
| 🟢 | **座位功能三個低優先小改（雲端 10/06 夜查到，我已查證）** | ⏳驗收併入後 AI 自己處理 | ①座位地圖每載入就寫 90 次資料庫（`seat_map()` 內逐一 `sync_chapter`）→ 只在清單檔內容真的變了才寫（比對檔案 mtime／雜湊）；②座位標「已入會」後無畫面可改回空位（後台加「改回空位」，需確認視窗）；③後台「已入會／釋出」沒有確認視窗。都不卡上線，不問教練。 |
| 🟡 | **`workspace/CLAUDE.md` 的接力棒鏡像停在 10/01，吃額度又過期（10/06 v288 查證）** | ⏳AI 自己處理（額度緊繃時動手前先跟教練說一聲） | 查證：`ai.openclaw.cron-daemon` 每 5 分鐘都有跑 `sync_handoff_to_claudemd.sh`，是腳本 9/30 加的格式防呆（開頭 500 字必須有「新的一棒 vN」）自 10/01 起每次拒絕，`/tmp/sync_handoff.log` 已累積 1,050 次拒絕；現在接力棒標題沒有「新的一棒」字樣。鏡像段約 2.2 萬字、占 CLAUDE.md 一半以上，在 workspace 內工作時會載入。**建議做法**：10/02 開工改 v3 的本意就是只注入最新一棒，所以比較對的是拿掉鏡像（CLAUDE.md 換成一行指標、cron-daemon 停掉這一步），不是修防呆；改前要確認 `feed_junshi_handoff.sh` 第 317 行那段說明沒有仰賴它。 |
| 🔴 | **守則#07 輪詢偵測器半成品（10-06）** | ⏸被安全檢查擋下，已問教練一次沒回，不追問 | `scripts/stop_rules_master.py` `_D_EVERY` 數字誤設必填，線上版（`d63575338`）會放過「每小時查一次」；補法與回測方式見 v287 ②。 |
| 🟡 | **雲端寫給軍師的信（10-06）** | ✅Mac 端＋雲端規則已上線 | 雲端信放分支 `docs/to_junshi/`，Mac 端 `scripts/cloud_letters.sh list｜cat｜mark`，開工 hook 與「讀信」反射會叫；已開著的舊雲端對話要先 pull master 才會用新路徑。記憶 `reference_cloud_letters_to_junshi_path_2026-10-06`。 |
| 🟡 | **bni-chapters 雲端協作（10-06）** | 第三步已合併(`3a9ba09`)、座位評估已做(`518b731`)；座位第 1～3 步（分支 `claude/seats-step123`）待驗收 | 步驟見 v287 ①。基礎建設：`tests/`（假資料庫、`conftest.py` 擋掉通知教練）、環境變數 `BNI_CHAPTERS_DB`／`TRUST_GAME_DB`、雲端用 `CLAUDE.md` 規則；雲端只看得到專案，要給它資料請放 `docs/source/`（README 為索引）；`claude -p "訊息" --cloud session_01PpSC8vJP5FQUtK1M7grBuU` 可代傳訊息給雲端任務（要教練先同意）。 |
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
