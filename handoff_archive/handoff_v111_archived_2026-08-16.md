# 軍師接力棒 · 2026-08-16 v111（Mac桌面版 Sonnet/Fable 5，賈維斯計畫通盤規劃+全四階段落地）

> 建立時間：2026-08-16 09:44 ~ 10:30（台灣時間）
> 本棒執行者：Mac 桌面版 Fable 5（規劃）+ Sonnet 5（施工）
> 上一棒：v110（Mac桌面版 Sonnet 5，AI微論壇台中場網頁概念稿+mentor100後台500錯誤修復）
> 本棒主軸：**上半場處理v110遺留的報名雙寫觀察期疑慮——教練回報今天只有一筆「大樹小講」報名收到官網通知，查證後發現這不是故障，是AI微論壇/百人導師申請這兩個系統本來就沒接官網雙寫（各自獨立系統，非同一套）。教練順勢裁示「所有報名系統都要走官網」，於是幫官網API補上公司/Email欄位、把AI微論壇接上官網雙寫並推上Netlify正式站，mentor100因表單只收LINE ID沒收手機號碼、教練裁示B案暫不接。下半場教練用最高等級Fable 5拋出「賈維斯計畫」構想——希望AI變成像鋼鐵人賈維斯一樣的總管家，不用每次交代背景。先產出通盤規劃報告，教練說「做」後，同一場session內完整落地四階段：專案卡+自動接線員、Token每月自動體檢、待辦到期提醒掛進晨報、小龍蝦背景研究派工SOP+首航驗證。**

## 🎯 本場戰果

### 1. 🔴🔴 報名雙寫「故障」查證：其實是誤會，順勢擴大範圍
教練回報今天4則LINE通知只有1則有「官網」標籤，懷疑官網雙寫不穩定。查`event.db`+`webapp.log`確認：今天唯一一筆大樹小講報名（鄭幗瓏，8/22金門場）官網+舊版通知都成功，資料庫`POST /api/register`回應200。另外兩則（AI微論壇的Han、百人導師申請的廖韋評）是完全不同的獨立系統，程式碼從未接官網雙寫，不是今天壞掉。教練聽完後裁示「所有報名系統都要走官網」，並指出官網訊息缺公司/Email兩欄。

### 2. 🔴🔴🔴 官網API補齊公司/Email+AI微論壇接上官網雙寫，已推正式站
`event-signup/db.py`的`attendees`表新增email欄位，`upsert_signup()`同步儲存；`app.py`的`/api/register`通知訊息加上公司/Email兩行(比照舊版格式)。已用真實POST測試驗證資料庫正確寫入(測試資料已清除，但過程中誤觸發一則真的LINE推播給教練，已誠實告知)。commit(workspace)`b8c837a45`。

AI微論壇(嘉義場，ai-talk repo)新增第三路fetch打`event.bymyway.com/api/register`(slug=`bigtree-0828`)，GitHub commit`97dc479`後，教練說「推」，已完成Netlify手動zip部署(deploy`6a80639be6c3ebafa0b860bf`，額度40→39，手動補記quota)，curl驗證文字/圖片Content-Type/新JS程式碼皆已上線，用Chrome開啟正式站確認。

百人導師申請(mentor100)：查證發現申請表單只收LINE ID沒收手機號碼，跟官網系統「手機=同一人身分證」的設計不合，直接塞LINE ID進手機欄位會導致誤判撞名或寫入失敗。提交A(表單加手機欄位)/B(先不動)兩個選項，**教練裁示B案**，已把先前預建的`mentor100-apply`事件格從event.db清除，不留孤兒設定。

### 3. 🎯🎯🎯 賈維斯計畫：通盤規劃報告+全四階段同場落地
教練用Fable 5拋出構想：希望AI像鋼鐵人的賈維斯一樣，開口就懂，不用每次交代背景。盤點現有家底(24個repo/35個Netlify站/23筆cron/10個本機服務/130+條記憶/57個試金石案例)後，核心診斷是「知識按時間存(日記)、不是按主題存(病歷)」，產出通盤規劃報告存於`knowledges/2026-08-16_賈維斯計畫_三合一智能管家系統通盤規劃.md`(commit`5fd6bf8e0`)，含現況盤點/核心診斷/解決方案(專案卡+自動接線員)/四大管理問題解答/小龍蝦分工可行性/誠實做不到清單(#15)/四階段施工計畫。

教練說「做」後，同一場session內完整落地：

**Phase 1（專案卡+自動接線員）**：`projects/cards/`建11張核心專案病歷(大樹小講/AI微論壇嘉義+台中/mentor100/event-signup/bni-chapters/BNI Connect/結繩領導學/tainan-calender/LINE三帳號/VPS)，`projects/INDEX.md`做別名路由表，`scripts/project_card_router.sh`做UserPromptSubmit hook自動接線員(教練訊息命中別名如「金門的活動」自動注入對應卡片，同session去重、單則訊息上限2張)。4組模擬測試(命中/去重/多卡/不誤觸發)全過，已註冊進`~/.claude/settings.json`(備份`/tmp/settings.json.bak-20260816101722`)。commit`70fa68ef7`。

**Phase 2（Token每月自動體檢）**：`scripts/monthly_token_healthcheck.sh`逐一curl驗證9項憑證(Netlify/Cloudflare/WordPress/LINE三帳號/Telegram三帳號)，全綠靜默、有壞才輸出FAIL詳情。已用真實token(9/9 OK)+注入假token(正確觸發FAIL分支)雙向測試。用`openclaw cron create`建月度cron(id`5d7acd65`，每月1日09:20 Asia/Taipei，`--no-deliver`讓agent自主判斷，比照46e67e2e三關精神)，`cron run --wait`手動觸發驗證：全綠時正確安靜收隊、`deliveryStatus:not-requested`，沒有誤發訊息。`路徑大全_憑證層.md`新增Token總表(用途/到期日/上次驗證)。commit`cacef61f5`。

**Phase 3（待辦到期提醒掛進晨報）**：`scripts/todo_staleness_check.py`解析待辦表格，對🔒/⏳/⚠️狀態列做①用task文字hash比對first_seen日期，卡住≥7天才提醒②抓文字裡M/D日期格式，未來3天內才提醒，全正常時安靜不輸出。3組測試驗證(真實表首跑建25筆baseline不誤報/手動backdate驗證卡住偵測/注入測試日期驗證到期偵測)全過。`morning_digest.sh`新增呼叫，刻意讓待辦提醒獨立於「有沒有commit」判斷之外(原本零commit會整段安靜跳過，改成沒commit但有待辦警示仍輸出)，既有06:00晨報cron(`f487652d`)完全不用改。commit`83adc0381`。

**Phase 4（小龍蝦背景研究派工）**：`knowledges/SOP_小龍蝦背景研究派工.md`定義派工單五要素。首航實測：用`openclaw cron create --agent main --session isolated --delete-after-run`一次性派工「找5個BNI風格網站」，小龍蝦用web_search+web_fetch實測5個真實站點(BNI Global/Japan/Atlanta/Hong Kong/ニュース子站)HTTP 200存在，按四欄格式產出研究筆記存於`knowledges/研究_BNI分會參考網站_2026-08-16.md`，並自主整理共通元素摘要表。已用`ls`+`cat`實際讀取驗證(非空檔/非散文)，job跑完自動刪除不留重複排程。commit`289b83c17`。

## 📋 下一場直接開工任務
- **Phase 1驗收**：下次教練提到任一張卡的別名時，確認自動接線員真的有觸發(目前僅模擬測試過，未經過真實對話框驗證)
- **報名雙寫觀察期**：先問教練是否已確認AI微論壇官網通知有正常收到，收到指令才考慮下一步
- 「真誠分會」網頁主架構問題：教練仍未說明具體是什麼
- 三機hook同步（Windows/ACER的Claude Code settings.json hook，非OpenClaw gateway hook）：ACER仍待處理
- **賈維斯計畫Phase 2月度cron**：下次1號09:20會自動跑第一次真實排程(今天是手動觸發驗證的)，之後留意HEARTBEAT.md有無異常記錄

## 🔑 本場關鍵檔案索引
- `event-signup/app.py`+`db.py`：官網API補email欄位
- `github_repos/ai-talk/index.html`：新增BYMYWAY_API第三路fetch
- `knowledges/2026-08-16_賈維斯計畫_三合一智能管家系統通盤規劃.md`：通盤規劃報告
- `projects/cards/`（11檔）+`projects/INDEX.md`+`scripts/project_card_router.sh`：Phase 1
- `scripts/monthly_token_healthcheck.sh`+openclaw cron `5d7acd65`：Phase 2
- `scripts/todo_staleness_check.py`+`.sh`+`morning_digest.sh`：Phase 3
- `knowledges/SOP_小龍蝦背景研究派工.md`+`knowledges/研究_BNI分會參考網站_2026-08-16.md`：Phase 4
- commit序列：`b8c837a45`→`97dc479`(ai-talk repo)→`a9fb72fca`→`5fd6bf8e0`→`70fa68ef7`→`cacef61f5`→`83adc0381`→`289b83c17`

