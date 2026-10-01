# v266～v267 接力棒＋「賈維斯成長計畫」詳細交辦段（2026-10-02 07:10 封存，v269 收工時瘦身）

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
