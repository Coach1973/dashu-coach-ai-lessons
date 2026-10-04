## 🔴 給跨對話框軍師讀的總結摘要（2026-10-05 05:30 台灣時間，Mac 桌面版 Sonnet 5.5，v280，教練說「總結」收工；04:20 第一次總結後又補了委員會專員名稱，一併寫入）

**主軸：積分表 v2 交件；信任裝備探測器擴到真鑫與籌備會；本屆領導團隊標籤上線；教練釐清 DnA 是「多重身份」。**

### 做了什麼
1. **積分表 v2**（教練上一場交辦）：併入職務四級、金質累加、綠燈 7 級、DnA 堆疊、連續月；列出還要新增的欄位；第一次用真實資料試算（真鑽中位 96、最高 1,073，帶來賓占 57%，沒人進第三階段；**「近三年」視窗程式還沒做**）。https://event.bymyway.com/curated/game-1004/score-v2.html ，檔 `knowledges/2026-10-05_信任遊戲_積分表設計_v2.md`。
2. **教練四點**：①真鑫裝上探測器（座位 17 位照 10/04 會期報告，公司取官方 94 人資料，專業類別空著等菁英表；教練卡片放上）；②籌備會也能探測（沒有會期報告也行、職務欄隱藏不加分；4 個籌備會目前 0 座位）；③用詞改「請跟領導團隊反映」；④一頁式簡介＝`~/Downloads/1791130445680.jpg`，已放真誠、真鑫教練卡片（`seed_coach_ppt_2026-10-05.py`）。
3. **本屆領導團隊**（教練貼 BNI Connect 名單，參考長虹白金分會＋BNI 官方頁）：卡片上紅色職務標籤、領導排前面；同一份資料補進探測器本屆職務（標「系統帶入」）。新表 `member_roles`；真鑫 12、真鑽 20。官方名稱「來賓接待人」「發展協調人」併入職務第二級；會員委員會與子委員會算第三級。**04:19 教練改：會員委員會四大專員用國家辦公室名稱＝品保專員／營造專員／關係專員／輔導專員（官網寫的品質保證、社區建設者、會員關係、會員參與不用）**，卡片標籤與腳本都已改。**04:20 教練再強調：沒標專員的一律叫「會員委員會」，標了才寫專員，不自己推測。**腳本 `seed_leadership_2026-10-05.py`。
4. **DnA 多重身份**（教練 04:08～04:13 親口）：母會只有領導團隊職務，助理大使／大使／董事顧問是在**母會以外的分會**另有的身份（「離開」不是離會）。邱南寅：真鑽卡片不寫，複製一份放真鑫（`source='dna-copy'`）寫「真鑫分會大使」，探測器 DnA 大使記本人；陳佩君老師補 DnA 董事顧問（真愛啟動董顧）。位階規則與小幫手資料庫原文存 `knowledges/2026-10-05_BNI位階與DnA規則_教練口述與小幫手資料庫.md`；新反射 `R-DNA-LABEL-OUTSIDE-CHAPTER-COPY-ONLY`。

### 卡在哪／發現
- **本場教練糾正兩次**：①檔名「1791130445680」我回報「找不到」，其實 `ls -t` 清單裡就有（記憶已更正）；②我把「離開」當離開母會、把大使標籤寫在邱南寅的真鑽卡片（已改）。
- 網頁上的「數字不對」表單送出後，通知仍只到教練，領導團隊不會自動收到（教練要的話要在各分會後台加回報清單）。
- 這場沒拿到截圖許可，領導標籤的版面（顏色、字體）只用 curl 驗過文字，沒親眼看過。
- 副本卡片是複製當下的快照，本人之後改自己的卡片不會同步。

### 📋 下一場開工先做（🎯 教練交辦＝其他分會照做）
① 教練陸續給**真富、真愛、真鑫菁英表、籌備會名單**：建座位＋跑 `import_detector_stats_2026-10-05.py <slug>`；真鑫菁英表來了補專業類別與希望合作對象；**真愛建座位時放陳佩君老師的複製卡片，標籤「真愛分會啟動董顧」**。
② 每月流程（沿用 v279 ③）：地區報表／官方紅綠燈檔 → `import_light_scores`＋來賓總覽＋`import_detector_stats`；領導團隊換屆時重跑 `seed_leadership_2026-10-05.py`（改名單與任期日期）。
③ 沿用 v277 ④⑤：10/09 後搬家舊夾（先確認捷徑指向的資料是活的、走五道閘門）、聯想／宏碁 ps1 瘦身、【聯想】開工講一次 E 槽備份提醒，講完刪這行。

**commit**：bni-chapters `9063868`、`c91b416`、`126db9a`、`e108bda`、`a327278`、`1eec7d6`、`b8c090a`；workspace `9ab8323a5`、`44bd5851e`、`176c1dc37`、`b9de63070`、`b7914acc4`、`aed0b2af5`、`7b037b681`；本次總結另計。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-05 02:55 台灣時間，Mac 桌面版 Opus 5.5→Sonnet 5.5，v279，教練說「總結」收工）

**主軸：信任裝備探測器第一版上線（真鑽、真誠），被教練抓到「帶來賓」用錯來源後改正；順手把來賓總覽、真鑽戰情表、燈號分數全部接上教練每月下載的官方資料。**

### 做了什麼
1. **探測器第一版**（`bni-chapters` `2337e05`）：選名字→系統亮最近會齡／帶來賓／培訓，本人或夥伴補職務、推薦入會（換算金質）、DnA；每筆公開誰填何時、可「回報管理員」、「數字不對」附證明通知教練；「開始探測」出信任三階段等級＋稱號＋分享 LINE。網址 https://chapters.bymyway.com/real-diamonds/detector 、/sincere/detector 。
2. **教練 00:42 抓到帶來賓不對（康文彬寫 158、官方 254）**：名片庫 `guest_visits` 邀請人是手打、漏很多。改用官方 PALMS（同 /guests）、培訓改用 /training 同一份（含 MSP 課）→ `410a13b`、`ea35158`；試金石案例 105、反射 `R-BNI-GUEST-COUNT-SOURCE`。同場教練追加規則：同一屆可勾多個職務；連續綠燈、連續 100 分一律算月（暫定每月 +5／+10）；DnA 堆疊（助理大使 30／大使 80／董事顧問 180，照最高算一次）。
3. **來賓總覽**（BNI-Training `9d6b011`、`66e4566`、`6e85d8e`）：新增「沒有邀約來賓的名單」（同培訓總覽未參加名單邏輯，標最近一次邀約在近幾個月／從未邀約／入會未滿）；月數改照天數算（8/31 起算不再多一個月）；只用「至」＝最新匯出日的報表；**9/1 以後用三個戰情表每週來賓名單補上**；教練下載新報表後多了近 18 個月（真鑽、真誠）、近 36 個月（真鑽），跟地區報表逐人核對無差異。
4. **真鑽戰情表補 9/1～9/29 五週**（zhenzuan-guests `05c3929`，`import_weekly_reports_2026-10-05.py` 逐週核對週報人數）。判斷三處：標題 6/30 那份＝9/22；9/1 早鳥「洪嘉紜」＝洪嘉妘；9/29 黃玠瑛同時在遲到與代理→記代理（累計代理 2→3、遲到維持 2）。
5. **燈號自動帶入**（`e40351f`）：教練每月下載地區 PALMS（近 6 個月）算燈號，也給了官方「會員紅綠燈 - 真鑽 (2026-09).xlsx」。用 `bni-traffic` 算法重寫，47 人與官方得分完全一致；`import_light_scores_2026-10-05.py` 匯入 → 探測器的最近燈號、連續綠燈／連續完美月數自動算，有系統燈號的人不再顯示自填綠燈欄。
6. **新反射**：`R-GUESTS-UPDATE-DASHBOARDS-FIRST`、`R-LIGHT-SCORE-MONTHLY-IMPORT`、`R-BNI-GUEST-COUNT-SOURCE`、`R-REPLY-ENGLISH-PARAGRAPH`（回覆出現整段英文就擋下，回測 2599 輪命中 144，抽樣皆真英文段落）。記憶 `reference_guests_overview_update_flow_palms_plus_dashboards_2026-10-05`。

### 卡在哪／發現
- **本場教練不滿兩次**：①我打算進 BNI Connect 抓約 40 份報表，教練問「你進 Connect 查什麼」「花多少 tokens 考慮過嗎」——其實戰情表早有每週來賓資料，不用進；②有一則回覆整段寫英文被糾正。
- 真誠、真鑫燈號目前只有 8/31 換算分，等教練下次下載近 6 個月地區報表。
- 暫定值：連續綠燈 +5／月、連續完美 +10／月、培訓每場先算 3 分、嚮導／修煉大師等級門檻、第二級職務 +15（教練都沒反對）。
- BNI Connect 仍是教練已登入狀態（沒登出），分會選項已切回真富。
- 柯朝陽 9/29 週報仍在（早鳥、邀請人），但會期報告顯示已離會，所以探測器座位沒有他。
- 大樹歷史頁排程首跑確認：`distill/bigtree_history_sync.log` 10-05 00:20 已出現「無需補登」✅（v277 ④ 前半完成）。

### 📋 下一場開工先做（🎯 教練交辦＝其他分會照做＋積分表 v2）
① 教練會陸續給其他分會資料（真富、真愛、真鑫菁英表，籌備會名單）：照真鑽做法建座位＋空座位按鈕，跑 `import_detector_stats_2026-10-05.py <slug>` 套用探測器。真鑫戰情表／真誠夥伴 PPT 已處理過者不重做。
② **積分表 v2**：併入職務四級、金質累加制、綠燈 7 級、DnA 堆疊、連續月（燈號每月紀錄）；列出新增欄位（遲到、早鳥、培訓分值表、見證與雙方確認按鈕）。
③ 教練每個月給新的地區報表／官方紅綠燈檔時：`python3 ~/github_repos/bni-chapters/import_light_scores_2026-10-05.py`（燈號）＋ BNI-Training `guests_build_data.py`→`guests_build_html.py`（來賓總覽）＋ bni-chapters `import_detector_stats_2026-10-05.py real-diamonds sincere`（探測器）。
④ 沿用 v277 ④⑤ 後半：10/09 後搬家舊夾（`~/Downloads.bak.20261002`、Chrome.bak、`fb_session_data.bak.20261003`、`vm_bundles.bak.20261003`，先確認捷徑指向的資料是活的、走五道閘門）；聯想／宏碁 ps1 開工腳本瘦身；【聯想】開工時講一次：E 槽兩份整機還原備份，容量不夠時 9/19 那份由教練自己刪，講完刪這行。

**commit**：bni-chapters `2337e05`、`410a13b`、`ea35158`、`18e7b28`、`e40351f`；BNI-Training `9d6b011`、`66e4566`、`6e85d8e`；zhenzuan-guests `05c3929`；workspace `3334c02`、`0b2123e`、`23ca726f5`、`1bd165a58`；本次總結另計。

---

> 📦 v278完整內容已封存：`handoff_archive/handoff_v278_archived_2026-10-05.md`（《AI企業團隊戰略》原話報告書＋真誠正式照與一頁式簡報＋真鑽空座位按鈕與教練卡片；未做完的項目已併進 v280「下一場開工先做」）

---

> 📦 v277完整內容已封存：`handoff_archive/handoff_v277_archived_2026-10-05.md`（真鑽 47 席上線＋信任裝備探測器方案 v2 定案＋積分表 v1 拍板；仍未做完的項目已併進 v279「下一場開工先做」）

---

> 📦 v276完整內容已封存：`handoff_archive/handoff_v276_archived_2026-10-05.md`（商務遊戲第二～四批問答＋積分表 v1＋Keynote／輔助鍵盤插話）

> 📦 v274＋v275完整內容已封存：`handoff_archive/handoff_v274_to_v275_archived_2026-10-04.md`（v274 手機版：AI 百人導師架構＋商務遊戲題庫＋原話報告書＋curation-watch 修復／v275 大樹小講 bigtree-1107＋ema1017＋歷史頁自動補登＋kr1003＋macOS 26.7.1；10/04 收工整理時搬出，仍未完成的項目已併進 v277「下一場開工先做」④⑤）

---

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
（目前沒有）


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

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
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
