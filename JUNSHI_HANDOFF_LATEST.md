## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 07:10 台灣時間，Mac 桌面版 Opus 5.5→Sonnet 5.5，v269）

**主軸：賈維斯成長計畫第四步③④完成——四位夥伴分身有了「三種標準」，記憶 127 條全部轉進反射系統（未處理 0）。**

### 做了什麼
1. **四位夥伴分身（peipei／kong／yijing／yang）SOUL.md 最前面加「🧭 三種標準（夥伴版）」**：先看紀錄與記憶、能推斷不問、說「做不到」前先看工具清單、語音錯字照最合理意思做、不答應做不到的事（例：不能主動傳訊息就別說「到時候提醒您」）；教練的公開活動直接查單場頁 `https://event.bymyway.com/curated/bigtree-月日/`（首頁「近期場次」是 JS 畫的，抓網頁看不到，別用首頁判斷）；yang 稱呼一律「Simona」。四群 session 已封存，gateway 真實路徑四位都逐字貼出第 3 點。**行為前後對照**（楊老師 10/1 真實語音句「大肅執動拜六那場AI課是幾點」）：改前叫「楊老師」並反問「您手邊有資料嗎」；改後叫 Simona、自己開 bigtree-1003，答出 14:00–16:30、13:40 入場、KR 養生廚房、免費（與網頁一致）。commit：peipei `cf586c1`、kong `9ff7bb119`、yijing `c9346f4`（三個獨立 repo，peipei／kong 含 09-24 未提交的「大樹作品 kind 分流」段一起存）、外層 `e6f5f4993`（yang）。測試對話 7 個已刪並 `memory forget`。
2. **記憶 127 條 → 反射系統**：新反射 13 條（git rebase 卡住、git 分岔先讀接力棒、改 coach888、寫 SOP 要寫口語別名、「全面X」範圍、BNI PPT SOP、claude rc 不 unset、sendBeacon CORS、策展刪除＝退役、git add -A 個資、MiniMax guard、大樹小講場次連動 event.db、台灣重心），每條都用歷史資料回測並收窄（coach888 408→135 次；台灣重心改抓 09-30 真實刺激「上海／廈門／中國商業」，命中正好是寫錯那一刻）；其餘 111 條登記 `memory_ledger`（併入哪條／參考資料／判斷類／已有程式／已退役）。`scripts/reflex_coverage.py` 新增記憶檢查：171 條未處理 0、索引斷鏈 0；補建從未寫入的 `feedback_no_wrong_posts_no_action_2026-09-18.md`、補收 `reference_openclaw_hook_inject_format`（標⛔過時）。`reflex_router.py` post_tool 自我排除也看指令（回測輸出曾誤觸）。commit `dfe39d869`、`bc0c25a79`、`e036177f6`，本次總結另計。

### 卡在哪／發現
- **楊老師（Simona）週六 AI 課提醒（07:08 教練原話：「要嘛讓小龍蝦能主動提醒，要嘛你幫忙提醒，對他來說只要有提醒就好」＝同意）**：yang 分身沒排程工具（安全鎖禁 exec），改由 Mac 端 `openclaw cron add` 代排兩個一次性工作，delivery 走 bot_main 投到她的群組 -5405039910：`08f1`→已換成 `4c706494-…`（10/2 12:00 台灣時間）、`e5fac0d4-…`（10/3 12:00 最後一次）。實測踩到 2 個坑：`--exact` 不能配 `--at`；分身若自己呼叫 message 工具發訊息，系統還會把它最後那句「已送出」再轉送一次（群組會多一則怪訊息）→指示改成「最終回覆就是提醒本文、不准用 message 工具」。已用只送教練的測試工作跑兩次，第二次確認最終回覆＝提醒本文、狀態 delivered，測試工作已刪。**12:00 後要確認**：`openclaw cron list --json` 看 `4c706494` 是否已消失/lastDelivered=true；教練說過「她說我知道了就停」，分身會先讀 MEMORY.md 判斷，她回「我知道了」時分身要把這句寫進 MEMORY.md。
- `state/member_context.log` 仍只有 03:34 兩筆測試，沒有真實 LINE 流量（龍蝦小助教認人未驗證）；聯想／宏碁沒回信（`cross-agent/inbox/mac/` 資料夾不存在）。
- 發現 kong 的 SOUL.md 寫「唯一指定模型 MiniMax M2.7」，但 `openclaw.json` kong 是 `minimax/MiniMax-M3`（peipei 的 SOUL 06-03 已升 M3），兩處矛盾；沒動（模型鎖需教練授權日期），記在 🔧 清單。

### 📋 下一場開工先做
賈維斯成長計畫第四步剩兩項，都在等外面（10-02 07:10 查過仍無動靜）：①看 `state/member_context.log` 有沒有真實 LINE 流量、第 4 欄是不是 `sender:u…`（龍蝦小助教認人）；②`cross-agent/inbox/mac/` 有聯想／宏碁回信就驗收（反射畫面原文＋開工🎯＋commit）。兩項都沒動靜就問教練今天從哪件事開始，不要空轉。

---

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
（已由上方 v269 取代：③④已完成，只剩等真實 LINE 流量與聯想／宏碁回信。）


---

> 📦 v265（Mac 10-02 02:40，試金石 95 案全部轉成反射＋教練定名「賈維斯成長計畫」）完整內容已封存：`handoff_archive/handoff_v265_archived_2026-10-02.md`

---

> 📦 v263 聯想棒（RustDesk 改 Tailscale IP 直連＋大樹作品單檔 HTML ema1017）完整內容已封存：`handoff_archive/handoff_v263_lenovo_archived_2026-10-02.md`；未結事項已移入下方「🤫等教練自己提起」與「🔧AI自己的工作清單」

---

## 🎯 「賈維斯成長計畫」（簡稱「反射條件」）進度（2026-10-02 07:10 瘦身版；詳細交辦段與第 1~3 步經過已封存 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`）

教練 02:30 原話：教練訓練出來的每個 AI 都要有條件反射；三種標準＝有智慧的反應、聽懂人話的反應、準確做事情的反應；對外服務再加「讓人備受禮遇、被尊重，惦記用戶說的話，不把問題丟回給用戶」。已全權授權，**不准再拿細項問教練**。

| 對象 | 狀態 |
|---|---|
| ① 教練自己的 AI | 小龍蝦端外掛 reflex-prompt／member-context／coach-context 上線；Mac 軍師 hook 85 條反射；**聯想 10-02 07:45 已接上並回信（Mac 驗收過：commit `bee1a7653` 存在、`pick_next_task.py` 在 Mac 接力棒實跑輸出正確、ps1 有 BOM 且呼叫它；聯想自己的反射／擋下是用管線模擬，要等教練在聯想開新對話框才算真實驗收）；宏碁 10-02 09:15 已接線並回信（裝了 Python 3.12、加 5 個 hook，用模擬事件測過反射與擋下；開工置頂🎯等聯想推上去後會自動帶到，真實新對話框畫面待教練下次開新對話框才算驗收）** |
| ② 四位夥伴分身 | ✅ 10-02 04:20 SOUL.md「三種標準（夥伴版）」＋群組 session 封存＋真實路徑測過（見 v269） |
| ③ LINE 對外帳號（禮遇版） | ✅ 人設上線（v268）；**真實 LINE 會員流量還沒驗證**（看 `state/member_context.log` 第 4 欄 `sender:u…`） |
| 試金石 97 案／記憶 171 條 | ✅ 全部有去向，`python3 scripts/reflex_coverage.py` 未處理 0、斷鏈 0 |

之後：開工改成「心＋最新一棒摘要」；Stop hook 只留行為檢查、拿掉字眼檢查。待查：`handoff_sync_guard.sh` 判斷1 用 PreToolUse＋stderr＋exit 0 提醒，AI 可能看不到。量尺：教練訊息「重講」比例 5月19%／6月13%／7月14%／8月12%／9月16%，重跑 `python3 scripts/render_top30_report.py` 看 10 月有沒有降。

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
| 🔴 | **賈維斯成長計畫（反射條件）總進度（v265~v269）** | ✅第 1~4 步完成，剩 2 項等外部 | 第 1 級反射 hook＋小龍蝦外掛 reflex-prompt／member-context／coach-context／url-typo-guard；禮遇版人設；四位夥伴三種標準；試金石 97 案＋記憶 171 條全有去向。**剩**：①真實 LINE 流量驗證 `state/member_context.log` 第 4 欄 `sender:u…` ②聯想／宏碁回信驗收。測試法：外掛類走 `openclaw gateway call agent`（記憶 `feedback_openclaw_hook_fire_and_forget.md`），分身類封存群組 session 後用真實語音句前後對照。詳細見 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`。 |
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
