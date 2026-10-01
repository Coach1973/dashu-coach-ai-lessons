## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 03:46 台灣時間，Mac 桌面版 Opus 5.5，v268）

**主軸：賈維斯成長計畫第三步四項全部做完並走真實路徑驗證。**

### 做了什麼
1. **對外帳號禮遇版人設**：bni_tainan／jiaolian_thoughts 的 SOUL.md 加「🤝 禮遇版服務標準」四條（惦記對方說過的話／不把問題丟回給對方／聽懂人話／準確做事）；小龍蝦 SOUL.md 加「場景三 LINE 龍蝦小助教、群組朋友」（19,092 字，未超 2 萬）。bni_tainan AGENTS.md 第 101 行改成「系統自動附上📅行事曆」，不再叫它用 exec。三帳號 39 個 LINE 舊對話已封存（可還原）。假會員實測：記得「小美」並一次給齊 10/12 進階MSP 日期＋時間＋ZOOM＋報名連結；記得「阿明第一次上台」直接接上；main 逐字貼出場景三。commit 外層 `626a42590`、workspace `c4882f831`。
2. **聯想／宏碁接反射**：`scripts/reflex_router.py` 修 Windows 兩個地雷（cp950 讀中文變亂碼→反射全比不到且不報錯；印 ⚡ 被吞掉），`PYTHONIOENCODING=cp950` 模擬提醒、擋下都正常。信已寄 `cross-agent/inbox/lenovo/20261002-0338_…`（接線＋開工置頂🎯，只有聯想改 ps1）、`inbox/acer/20261002-0338_…`（只接線）。跨機鎖依教練 02:30 原話「聯想電腦、宏碁電腦…也要被注入」開。舊草稿移到 outbox。commit `f9708d4c0`。
3. **網址手滑校正**：新外掛 `extensions/url-typo-guard/`（`message_sending`，LINE 三帳號送出前把 `tainan-calendar`／`tainancalender` 等改回 `event.bymyway.com/tainan-calender/`，實測錯的都 404）；每 3 次寫信到 `cross-agent/inbox/mac/`，不發 Telegram 吵教練。舊 hook 已關。測試 12/12＋真實路徑（bni_tainan 回覆經 deliver 送假 LINE 收件人，外掛抓到並改正）。gateway 完整重啟兩次（03:42、03:44），版本先核對一致。commit `bc9b414bb`。

### 卡在哪／發現
- `state/member_context.log` 到 03:46 仍是空的（凌晨沒有真實 LINE 會員訊息），龍蝦小助教認人還沒驗證。
- `openclaw message send` 不經過 message_sending，測送出前外掛要走 `gateway call agent` 加 `deliver:true`＋假收件人（已寫進記憶 `feedback_openclaw_hook_fire_and_forget.md`）。

### 📋 下一場開工先做
賈維斯成長計畫第四步：①看 `state/member_context.log` 有沒有真實 LINE 流量、第 4 欄是不是 `sender:u…`（龍蝦小助教認人）；②`cross-agent/inbox/mac/` 有聯想／宏碁回信就驗收（反射畫面原文＋開工🎯＋commit）；③四位夥伴分身（peipei／kong／yijing／yang）SOUL.md 寫「三種標準」夥伴版（有智慧／聽懂人話／準確做事；peipei／kong／yijing 是獨立 repo），改完封存該群 session、走真實群組路徑測；④記憶 125 條未處理的轉反射。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 03:28 台灣時間，Mac 桌面版 Sonnet 5.5→Opus 5.5，v267）

**主軸：賈維斯成長計畫第二步——15 支「注入沒送到模型」的舊 hook 逐支分類，重要的搬進兩個新外掛，全部走真實路徑請模型逐字貼出驗證。**

### 做了什麼
1. **會員端外掛 `extensions/member-context/`**：LINE 每位朋友的過去對話（寫入仍由 line-user-memory hook）、jiaolian_thoughts 知識庫檢索、bni_tainan 行事曆（問到日期且檔案超過 4 小時先跑 `sync_calendar.py`）。舊 hook `knowledge-search-inject`、`bni-calendar-inject` 已關。
2. **教練端外掛 `extensions/coach-context/`**：教練說「釋放」由外掛跑腳本、真實結果交給模型照實轉述；提到專案別名附專案卡。只認教練本人。舊 hook `rustdesk-free-memory-trigger`、`project-card-router` 已關。
3. **反射索引**新欄位 `agents`（只給指定分身；軍師端 `reflex_router.py` 跳過）＋ `R-BNI-OFFICIAL-TEXT`（bni_tainan／jiaolian_thoughts，會員版不提教練）＋ `R-VOICE-CHECK`（語音轉文字先確認）＋ `R-ZSH-VAR-COLON`（試金石案例99）。
4. 驗證：member-context 15 項、coach-context 11 項、reflex-prompt 24 項；gateway 真實路徑假會員與 main（測試模式旗標 `state/RELEASE_DRYRUN`，已移除），模型逐字貼出📓記憶、📅行事曆、⚡會員版官方條文、📚知識庫、🖥️釋放結果、🗂專案卡。測試對話、假會員檔、測試紀錄都已清掉。
5. 分類表寫在記憶 `feedback_openclaw_hook_fire_and_forget.md`（group-activity-memory 不搬：群 8/24 後沒訊息；usage-query／bot-relay 資料 7/8 起就停；client-memory 不搬）。

### 卡在哪／發現
- **行事曆停在 8/30**（9/10 拿掉 exec 後沒人同步）：10/12 進階MSP 已改 ZOOM 線上、舊檔還寫安平路。已手動同步，之後外掛自動同步。bni_tainan `AGENTS.md` 第 101 行還叫它用 exec 同步，改人設時順手刪。
- **漏洞已補**：舊釋放 hook 只看 agentId=main，龍蝦小助教的 LINE 會員說「釋放」也會重啟 Mac 的 RustDesk。
- **未驗證**：龍蝦小助教（main）認人只能靠 senderId，要等真實 LINE 會員訊息；看 `state/member_context.log` 第 3 欄 `line`、第 4 欄 `sender:u…`。
- gateway 完整重啟兩次（03:14、03:22），每次約 15 秒；版本已先核對一致。設定備份 `openclaw.json.bak-20261002-before-member-context`／`-before-coach-context`（gitignore）。

### 📋 下一場開工先做
（第三步已完成，見上方 v268 的「下一場開工先做」。）

<!-- 原文：賈維斯成長計畫第三步：①先看 `state/member_context.log` 有沒有真實 LINE 流量、第 4 欄是不是 `sender:u…`（龍蝦小助教認得出人才算數）；②對外帳號「禮遇版」人設寫進 jiaolian_thoughts／bni_tainan／main 的 SOUL.md（2 萬字上限見 R-BOOTSTRAP-20K），順手刪 bni_tainan AGENTS.md 第 101 行 exec 同步那句，改完刪 session、走真實路徑測；③聯想／宏碁 `feed_junshi_handoff.ps1` 開工注入讀反射索引（舊信草稿 `cross-agent/drafts/20261002-0125_mac-to-lenovo_kaigong-top-task-port.md` 改寫再發，教練 02:30 已說三台都要）；④`line-url-typo-guard` 改用外掛 `message_sending`。 -->

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 03:05 台灣時間，Mac 桌面版 Sonnet 5.5 ⇄ Opus 5.5，v266）

**主軸：賈維斯成長計畫第一級上線——查出小龍蝦 15 支 hook 的「注入給模型」從沒生效，改用外掛 reflex-prompt 接手。**

### 做了什麼
1. 開工後動手前先查證接點：`rule-reminder` 用的 `event.context.inject` 根本沒人讀（2026.9.4 原始碼：`message:preprocessed` 發了不等、`agent:bootstrap` 只讀回 `bootstrapFiles`，整個 dist 沒有任何地方讀 inject）。上一棒「小龍蝦已有 rule-reminder 在注入」的前提是錯的。
2. 新外掛 `extensions/reflex-prompt/`（`before_prompt_build`→`prependContext`，真的進模型）：讀反射索引 prompt 時刻、依發話者三級分流（教練 ID→coach；peipei／kong／yijing／yang→partner；其他→public，非教練看 `say_other`、不附出處）、同場同條 30 分鐘冷卻、心跳／排程不出聲。`openclaw.json` 加了 allow＋`allowConversationAccess`；新外掛要**完整重啟 gateway** 才掛上（熱重載只套設定、不掛外掛），已重啟一次。
3. 索引新增 `audience`／`say_other`；新反射 `R-OC-HOOK-INJECT-DEAD`；記憶 `feedback_openclaw_hook_fire_and_forget` 補全並進索引、`reference_openclaw_hook_inject_format` 標過時；試金石案例98。
4. 驗證：4092 句教練原話 JS／Python 21 條完全一致；分流測試 18 項（`node extensions/reflex-prompt/test.mjs`）；gateway 真實路徑 main 一字不差貼出 R-HERMES、yijing 只拿到客氣版且無教練專用條。commit workspace `c556570c0`、外層 `76fa20aee`，本次總結另計。

### 卡在哪／發現
- **死注入 hook 清單**（只有「注入給模型」那段無效，記錄與直接發訊息照常）：auto-goal、bni-calendar-inject、bni-reminder-schedule、bot-relay-inbound、context-overflow-guard、group-activity-memory、knowledge-search-inject、line-user-memory、project-card-router、round-table-orchestrator、rustdesk-free-memory-trigger、session-summary-trigger、usage-query、rule-reminder、client-memory。**只驗證了機制，沒逐支驗證哪支的注入真的重要**，下一場逐支分類。
- `line-url-typo-guard` 訂的 `message:sending` 事件在 2026.9.4 已不存在（gateway 日誌警告），bni_tainan 網址手滑校正從沒觸發。
- LINE 會員級還沒有真人流量驗證：看 `state/reflex_hits.log` 第 5 欄有沒有 `oc:main:public`；LINE senderId 沒帶到會被當教練級。
- 備份 `openclaw.json.bak-20261002-before-reflex-prompt`（被 gitignore，不進 git）；兩場測試對話已刪、記憶已 forget。

### 📋 下一場開工先做
（第二步已完成，見上方 v267 的「下一場開工先做」。）

---

> 📦 v265（Mac 10-02 02:40，試金石 95 案全部轉成反射＋教練定名「賈維斯成長計畫」）完整內容已封存：`handoff_archive/handoff_v265_archived_2026-10-02.md`

---

> 📦 v263 聯想棒（RustDesk 改 Tailscale IP 直連＋大樹作品單檔 HTML ema1017）完整內容已封存：`handoff_archive/handoff_v263_lenovo_archived_2026-10-02.md`；未結事項已移入下方「🤫等教練自己提起」與「🔧AI自己的工作清單」

---

## 🎯 教練交辦：下一場第一件事＝「賈維斯成長計畫」（簡稱「反射條件」）植入所有 AI（2026-10-02 02:35 Mac Opus 5.5；教練 02:30 原話定案）

**教練要的結果**：今天做出來的整套條件反射，要讓教練訓練出來的每一個 AI 都有。三種標準：**有智慧的反應、聽懂人話的反應、準確做事情的反應**；對外服務再加：**讓人備受禮遇、被尊重，惦記用戶說的話，不把問題丟回給用戶**。教練已全權授權，**不准再拿細項問教練**。

| 對象 | 誰在跟它說話 | 要放什麼 |
|---|---|---|
| ① 教練自己的 AI：Telegram「頂級特助」(main)、LINE 龍蝦小助教(main)、Mac／聯想／宏碁軍師、雲端工作頁 | 教練 | 全套反射，照教練的標準 |
| ② 四位夥伴分身：佩佩老師(peipei)、孔大哥(kong)、怡靜(yijing)、楊尚儒(yang) | 夥伴 | 三種標準＋他們能力範圍內用得到的反射；不必照教練全部標準 |
| ③ LINE 對外帳號：教練都在想什麼(jiaolian_thoughts)、BNI 大台南小幫手(bni_tainan)、龍蝦小助教 | 教練說話＝①；一般會員＝禮遇版 | 會員不能動系統設定，但要感受到頂級特助（21 條的客製服務感） |

**✅ 第一級「小龍蝦端教練說話時」已上線（2026-10-02 02:49，Mac 桌面版 Sonnet 5.5→Opus 5.5）**：
- 🔴 原計畫的接點是錯的：`rule-reminder` 的 `event.context.inject` **從來沒送到模型**（2026.9.4 原始碼：message:preprocessed 發了不等、context 用完就丟，整包沒人讀 inject）。同病的還有 12 個 hook（清單見記憶 `feedback_openclaw_hook_fire_and_forget.md`），它們的記錄／直接發訊息照常，只有「注入給模型」那段是死的。
- 改做外掛 `~/.openclaw/extensions/reflex-prompt/`（before_prompt_build → prependContext，有人等、真的進模型）：直接讀 `knowledges/反射索引.json` 的 prompt 時刻，依發話者分三級（教練 ID→coach；peipei／kong／yijing／yang→partner；其他→public），非教練看 `say_other`、不附出處；同場同條 30 分鐘冷卻；心跳／排程不出聲。索引新增欄位 `audience`、`say_other`（目前 R-PLAIN-TALK／R-SEARCH-HISTORY-FIRST 開到三級，R-SHOW-NOT-DO／R-COPY-EXACT 開到夥伴）。
- 驗證：4092 句教練原話 JS／Python 命中 21 條全一致；分流測試 18 項全過（`node extensions/reflex-prompt/test.mjs`）；gateway 重啟後走 `openclaw gateway call agent` 真實路徑，main 一字不差貼出 R-HERMES、yijing 只拿到「聽不懂」客氣版且沒有教練專用的那條。命中紀錄 `state/reflex_hits.log` 第 5 欄 `oc:<agent>:<級別>`。
- 防再犯：新反射 R-OC-HOOK-INJECT-DEAD（改 hook 寫 inject 時提醒，回測 18/39091 全命中正確情境）；舊記憶 `reference_openclaw_hook_inject_format.md` 標過時。
- **下一步**（10-02 03:25 ①②已完成：外掛 member-context／coach-context＋反射 R-BNI-OFFICIAL-TEXT，見 v267；03:46 ④也完成：外掛 url-typo-guard，見 v268；③等真實 LINE 流量）：①把死掉的注入搬到外掛（價值高先做：line-user-memory 每位朋友記憶、knowledge-search-inject、bni-calendar-inject、client-memory 守則）；②bni_tainan／jiaolian_thoughts 的「官方條文一字不差」提醒（rule-reminder 那條教練 08-05 親口裁示的，一直沒生效）搬進索引 public 級；③真實 LINE 會員流量出現後，看 hits log 有沒有 `oc:main:public`，確認 LINE senderId 有帶到（沒帶到會被當成教練級）；④`line-url-typo-guard` 訂的 `message:sending` 事件 2026.9.4 已不存在（gateway 日誌警告），bni_tainan 網址手滑校正從沒觸發，改用外掛 `message_sending`。
- 原計畫（保留脈絡）：讓 rule-reminder 讀反射索引＋加適用對象欄，依 agentId＋發話者分流。
- 對外「禮遇版」是人設不是反射：寫進 jiaolian_thoughts／bni_tainan／main 的 SOUL.md（2 萬字上限，見 R-BOOTSTRAP-20K）。
- 聯想／宏碁：`feed_junshi_handoff.ps1` 開工注入加讀反射索引＋Windows 版路由；舊信草稿 `cross-agent/drafts/20261002-0125_mac-to-lenovo_kaigong-top-task-port.md` 要改寫成這件再發（教練 02:30 已明說三台都要＝跨機鎖解除）。
- 雲端工作頁：確認 `cloud_sync/` 有帶上反射索引與路由。
- 每個分身改完：刪該群 session 重開、走真實群組路徑測過才算（R-AGENT-RULES-SESSION）；付費功能不真測。

**第 3 步進度（本場）**：
- ✅ 試金石 95 個案例標題全部有去向：新增反射 13 條＋判斷 4 條＋已有程式擋住登記 2 條，案例去向表 15 筆；全用歷史資料回測、真實輸入端到端測過（commit `3bd71c9ef` `f58598c12` `ce8608c85`）。新工具：`scripts/reflex_add.py`（併入）、`scripts/reflex_coverage.py`（覆蓋率，未處理＝0）。
- ⏳ 記憶 165 條：40 條已被反射引用、125 條未處理（前 30 條已初判）；吸收 `trigger_index.md` 還沒做。
- 發現：Mac 的反射 hook 只接 Bash／Edit／Write（送檔工具接不到）；`model_tier_advisor.sh` 切 Opus 後第一則仍報 sonnet（舊 bug 重現）。

**之前第 1、2 步**：四個時刻＋雲端都接上（`2ce76cad1` `04978969b`，外層 `d5470c305`）；Top 30 報告 `knowledges/2026-10-02_Top30條件反射報告.html`，回測 `scripts/reflex_backtest.py`（原話庫與快取含密碼，不進 git）。
- 量尺：教練訊息「重講」比例 5月19%／6月13%／7月14%／8月12%／9月16%；重跑 `python3 scripts/render_top30_report.py` 看 10 月有沒有降。
- 跨機（跨機鎖，教練沒提就不問）：聯想／宏碁還沒接上反射；Windows 開工沒有「置頂教練交辦」。信已寫好草稿 `cross-agent/drafts/20261002-0125_mac-to-lenovo_kaigong-top-task-port.md`，教練說「發」才搬進 inbox。
- 之後：開工改成「心＋最新一棒摘要」；Stop hook 只留行為檢查、拿掉字眼檢查。
- 待查：`handoff_sync_guard.sh` 判斷1 用 PreToolUse＋stderr＋exit 0 提醒，AI 可能看不到（所有對話紀錄沒出現過）。

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

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🔴 | **賈維斯成長計畫第二步：15 支死注入 hook 逐支分類＋重要的搬到外掛（v266）** | ✅兩批都已上線 | **10-02 03:25 第二批完成**：外掛 `extensions/coach-context/`（教練說「釋放」由外掛跑腳本、真實結果交給模型；提到專案別名附專案卡；只認教練本人——舊 hook 連龍蝦小助教的 LINE 會員說「釋放」都會重啟 Mac 的 RustDesk），`rustdesk-free-memory-trigger`、`project-card-router` 兩支 hook 已關；測試 `node extensions/coach-context/test.mjs`（11項）＋真實路徑（測試模式旗標 `state/RELEASE_DRYRUN`，測完已移除）。group-activity-memory 不搬（群 8/24 後沒訊息）。剩 auto-goal／round-table 再評。**10-02 03:20 第一批完成**：分類表寫在記憶 `feedback_openclaw_hook_fire_and_forget.md`。新外掛 `extensions/member-context/`（每位朋友記憶／知識庫／BNI行事曆，行事曆超過4小時先同步），`knowledge-search-inject`、`bni-calendar-inject` 兩支 hook 已關；反射索引加 `agents` 欄（軍師端 `reflex_router.py` 跳過）＋`R-BNI-OFFICIAL-TEXT`＋`R-VOICE-CHECK`。測試 `node extensions/member-context/test.mjs`（15項）、`node extensions/reflex-prompt/test.mjs`（24項）；gateway 真實路徑假會員四段都收到。**待真實流量確認**：`state/member_context.log` 出現 LINE 那幾列時，看第3欄是 `line`、第4欄是 `sender:u…`（龍蝦小助教 main 只能靠 senderId 找人）。bni_tainan `AGENTS.md` 第101行還叫它用 exec 跑同步（exec 早被拿掉），行事曆現在系統會自動附上，不影響回答，改人設時順手刪。 |
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

> 📦 v112～v266 各棒的封存檔名一覽已搬到 `handoff_archive/INDEX_舊棒封存指標_v112-v266.md`（2026-10-02，主檔只留最新兩棒＋待辦表）
