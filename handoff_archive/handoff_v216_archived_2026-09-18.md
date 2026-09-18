# 軍師接力棒 · 2026-09-18 v216（Mac桌面版 Sonnet 5，EDM連結補完+三個repo git hygiene清理(含peipei倉庫金鑰歷史殘留發現)+手機版FB貼文思考模式評鑑與派工）

> 建立時間：2026-09-18 02:16 ~ 03:30（台灣時間）
> 上一棒：v215
> 本棒主軸：**補完大樹小講10/3 KR場EDM連結；查明並清理外層`.openclaw`repo長期積壓的115行未commit異常，順手一併清乾淨kong/peipei兩人各自獨立備份repo的3週/10週(實為4個月)積壓，過程中發現peipei倉庫舊commit含明文MiniMax/Google金鑰；教練委託分析手機版(MiniMax-M3)執行FB貼文任務的思考模式是否合理，讀取完整session transcript+獨立curl驗證後給出評估，並把後續修復工作寫成派工信交給手機版執行(省教練Sonnet流量)。**

## 🎯 本場戰果

### 1. 大樹小講「歷史講座紀錄」補10/3 EDM連結
確認素材已存在`~/github_repos/bigtree-1003/edm.jpg`(佩佩老師包好的第4場返場EDM)，複製進主站`archive/edm/`，「歷史講座紀錄」宮格牆新增第24張卡片，連結指向已上線的`event.bymyway.com/curated/bigtree-1003/`。用真實Chrome開過+node解析JS陣列驗證資料格式正確+圖片本身用image工具看過確認文字無誤。commit`fdfaff0`(bigtree repo)已推GitHub，Netlify正式站尚未部署(curl驗證過)，等教練喊「推」。

### 2. 外層`.openclaw`repo 115行未commit異常根因查明+清理，順手清乾淨kong/peipei兩人的獨立備份repo
根因是兩件事疊加：①`agents/kong`、`agents/peipei`各自是獨立GitHub備份repo(`kong-ai-backup`/`peipei-ai-backup`)，跟`workspace/`同性質，但外層`.gitignore`一直沒排除它們②案例73 schema v17升級新增的目錄命名(`session-sqlite-import-archive`、`sessions_archive`等)，8/25版`.gitignore`沒涵蓋到。TOOLS.md顯示「刪除」是doctor --fix把內容合併進AGENTS.md的正常行為，不是bug，之前手動救回其實是在打一場打不贏的仗。已補齊`.gitignore`規則+確認無金鑰洩漏後commit，115行歸零，commit`4d2f68cdc`已推上GitHub。

教練追問「不處理掉要放著幹嘛，萬一出問題怎麼辦」後，一併清理kong-ai-backup(3週積壓，commit`3861d382e`)+peipei-ai-backup(10週未commit，實際回溯發現是4個月memory日記從未進版控，commit`d4034d4`)。**清peipei倉庫時的重大發現**：`agent/models.json`跟`agent/auth-profiles.json`過去的git commit裡含明文的全系統共用MiniMax金鑰+一組Google API Key，現況兩檔已被清空/刪除(不確定何時、誰清的)，已commit現況+把兩檔加進`.gitignore`防止未來再犯。金鑰本體仍留在較舊的git歷史裡，repo已確認是private(`gh repo view`驗證)，風險比照先前terminal-notes token洩漏案例判斷可接受，是否要改寫歷史清除舊commit待教練裁示(不可逆操作)。詳見`claude-brain/reference_peipei_backup_repo_had_plaintext_api_keys_2026-09-18.md`。

### 3. 手機版(MiniMax)FB貼文任務思考模式評鑑
教練今晚讓手機版(Claude Code Remote Control連進這台Mac，實際跑MiniMax-M3)執行大台南策展中心12則貼文重貼任務，貼出後回報「沒縮圖+文案重複網址」，質疑MiniMax「做事情欠缺考慮」，把對話貼給軍師要求通盤分析思考模式對不對。軍師直接讀取該session完整transcript(`~/.claude/projects/.../1de66f96-....jsonl`)，逐項評鑑後給出結論：**核心root cause診斷(og:image用相對路徑，FB爬蟲抓不到)本身是對的，而且有先curl驗證才回答，這部分方法論健全**；但整個過程有幾個真實(非偏見)的問題——①一開始搞不清楚自己是跑在雲端還是教練Mac本機，來回猜測浪費好幾輪②第一個念頭是複製教練整顆953MB Chrome profile(等於複製所有網站密碼)，靠系統自動安全機制擋下才沒發生③教練明確說「聽不懂行話」後才發現一直在講remote debugging port這類專有名詞，違反守則#10④用錯网址(GitHub Pages舊網址而非`event.bymyway.com`)，是教練自己發現糾正回來的。**核心問題**：12則一次貼完才發現沒縮圖，沒有先貼1則驗證格式再批次執行——這正是「先斷言後查證」，軍師自己當晚稍早也連續犯了4次同類錯誤(`feedback_assert_before_verify_pattern_2026-09-17`)，不是MiniMax特有的毛病，是這套系統裡AI普遍會犯的模式。

教練追問「為何用GitHub網址而非event.bymyway.com，是不是資料庫裡完全沒教過」，查證屬實：`reference_curation_sop_2026-09-06.md`裡雖然說明了`event.bymyway.com/curated/<slug>/`路由存在的機制(避免曝光內部repo結構)，但從未明確寫下「所以對外貼文/行銷要用這個網址，不要用GitHub Pages」這條規則——這是真實的文件缺口，直到手機版今晚自己寫的新SOP才第一次把這條規則明確記下來。

已把後續修復工作(逐一修12個slug的og:image絕對路徑+`curation_process.py`加自動修復機制治本+刪除重貼12則)寫成完整派工信`cross-agent/inbox/mobile/20260918-0330_mac-desktop-to-mobile_fix-og-image-and-repost.md`(commit`c40e76eff`)，交給手機版用它自己的MiniMax額度執行，不消耗教練的Sonnet流量。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_gitignore_stale_after_schema_migration_2026-09-18`：git status突然冒出一大批新untracked目錄時，先查是否有獨立`.git`(embedded repo需排除非直接add)、是否為版本升級產物(查commit log有沒有"救回"字樣的舊嘗試代表在打敗仗)、diff是純新增還是有東西不見。
2. `reference_peipei_backup_repo_had_plaintext_api_keys_2026-09-18`：清理任何agent的獨立備份repo積壓前，應順手grep一次`models.json`/`auth-profiles.json`這類含embedded apiKey欄位的設定檔。

## 📋 下一場開工先做
1. **等手機版回報**：og:image修復+12則刪除重貼結果如何，讀`cross-agent/inbox/mobile/`那封信有沒有被執行。
2. **等教練喊「推」**：bigtree-tw Netlify靜態版一鍵發佈(EDM連結已就位)。
3. peipei-ai-backup舊commit金鑰歷史是否要改寫清除，待教練裁示(不可逆，需親口確認)。
4. 沿用既有待辦：確認孔大哥/佩佩老師端industry-chain-sop hook真人實測、峰哥的產業服務鏈SOP待Telegram ID、幕僚長晨報cron消失原因(40+天未覆核)、FB App Review(商家資產管理組合卡住)、`stop_rules_master.py`規則#07誤判regex。
5. E16接力棒瘦身：**本場已完成**，v207~v213已搬進`handoff_archive/handoff_v207_to_v213_archived_2026-09-18.md`，主檔現維持v214~v216共3棒。

## 🔑 本場commit
`bigtree`(github_repos)：`fdfaff0`(EDM連結)。外層`.openclaw`repo：`4d2f68cdc`(.gitignore修復+115行清理)。`kong-ai-backup`：`3861d382e`。`peipei-ai-backup`：`d4034d4`。`workspace`：`f409b192a`+`873450ca9`(記憶檔)+`c40e76eff`(派工信)+本次commit(接力棒+E16瘦身封存)。

---

