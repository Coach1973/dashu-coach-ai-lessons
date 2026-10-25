## 🔴 給跨對話框軍師讀的總結摘要（2026-10-26 01:14 台灣時間（含 00:56 後追加），Mac 桌面版 Code 分頁（「開工1437」臨時 worktree kaigyo-1437-7ba0b0），Sonnet 5.5 ⇄ Opus 5.5；教練說「總結」；本段 10/25 14:38～10/26 01:14，對話容量約 46%）

**主軸：人才軍火庫邀請函連動排名、小龍蝦（巴哈）罷工根治、接手巴哈卡住的海報與台鐵研究案、巴哈改成只出海報。**
- **軍火庫**：邀請函首批 24 位連動首頁點擊排名（roster.json＋/api/skyteam/ranking），首頁換人要跑 skyteam_build_invite_roster.py。
- **罷工根因（10/26 教練糾正「額度」說錯）**：MiniMax 額度只在 10/25 22:00～23:03 用完過，後來恢復；真正擋住的是小龍蝦自己記的「限流冷卻」標記（冷卻倍增最長 24 小時，連整理對話也被擋）→對話塞爆。燒額度元兇＝台鐵標案研究的小幫手（一個 898 步、1.29 億 token）。源頭已改：看門員看到「冷卻中被擋」自動清標記（workspace `19aa8a39f`）；小幫手一層、同時 2 個、10 分鐘（outer `929586963`）；英文系統通知自動翻中文【軍師轉達】；塞爆自動換新對話。試金石案例 134 `ef69f9fc4`。
- **接手海報**：林家羽、蔡忠彬（新增副理事長）、楊彩藝、詹翔欽、陳佩君、李小龍，共 6 人橫直版，已更新 NMDA 理監事頁並推回巴哈群組（`a9bd8b21c`、`d53f8b50d`）。林家羽用最後重傳的生日自拍照，藍西裝 MDRT 那張可能是另一人，沒確認。
- **台鐵研究案接手**：圖文版 https://event.bymyway.com/curated/tra-taitung/ （插圖 4 張 LK888 出圖，已進大樹作品集「大樹常用」，`8bb5b96b6`）；PDF/HTML 報告在 workspace/reports。
- **新分工（教練 10/26 00:52）**：台鐵研究案由軍師統籌；巴哈只出中華新媒體橫＋直版海報。已用程式擋：巴哈 3 種身分都禁用上網、瀏覽器、小幫手（`da22958c9`），台鐵類訊息由巴哈追加到 state/tra_research_inbox.md（實測成功）。
- **教練原話線索**：「為什麼要讓我二選一」＝兩個資訊都給、讓他自己評估；「卡住的你就做、做完推回去」＝佩佩老師處理不了的由軍師接手、成品推回群組；「沒有查明之前怎麼可以胡說八道」＝講額度必附時間點與現況。

- **00:56 後追加：台鐵轉交自動觸發（未完成）**：教練要「轉交檔一寫入就自己處理、做完用巴哈推回群組」。已裝 `scripts/tra_inbox_worker.sh`＋`com.coach.tra-inbox-watch`（WatchPaths 監看 state/tra_research_inbox.md，幾秒內觸發，實測 OK；plist 已備份進 ops/launchagents_backup；一天上限 8 次）。**卡關**：腳本在背景叫 `claude -p` 每次約 30～50 秒、exit 0、輸出 0 bytes（json 也空）；同參數拆開單獨在 launchd 測都正常（短提示、長提示、三個 --add-dir、perl alarm 各自 OK），合起來就空白，根因未找到。補過 `USER/LOGNAME`（乾淨環境沒 USER 時 claude 顯示沒登入）。目前失敗會用主機器人私訊教練「請叫軍師接手」，不會推群組。除錯用 `TRA_DEBUG=1`（set -x 到 /tmp/tra_worker_debug.log）、`TRA_TEST=1`（答案改發教練私訊）。另：舊派工橋 `junshi_task_worker.sh` 的 WatchPaths 設定檔已不在 LaunchAgents（寫 JUNSHI_TASK_QUEUE 沒人接），10/25 的成功紀錄不知是誰觸發。
- **教練問（00:55）**：特殊任務結束後巴哈要恢復跟頂級特助一樣——恢復＝拿掉 openclaw.json peipei toolsBySender 三處 deny 裡我加的 `group:web`、`browser`、`sessions_spawn`、`subagents`，與 AGENTS.md 最上方「2026-10-26 教練指令」那段（原檔備份 state/backup_peipei_AGENTS_20261026.md）。兩邊原本設定就不同，只保證恢復原狀。

### 📋 下一場開工先做（以本棒為準）
1. **用 Opus 查 tra_inbox_worker 的 claude -p 空白根因**：重現法＝寫一行到 state/tra_research_inbox.md（先 `launchctl setenv TRA_TEST 1`，測完一定 `launchctl unsetenv TRA_TEST`），看 ~/Library/Logs/openclaw/tra_inbox_worker.log；可試改成直接把 PROMPT 寫檔、用 stdin 餵 claude，或加 `--debug` 看。修好前，佩佩老師的台鐵問題靠「私訊通知教練→叫軍師接手」。
2. 台鐵研究案：還缺標案正式 16 據點名單與標案形式，明天提案結果出來後補。
3. 林家羽海報照片是否正確，問佩佩老師。
4. 看門員「解除冷卻」與巴哈「禁用上網」都還沒碰到真實事件驗證，第一次罷工時看 state/openclaw_stall_watchdog.log。

🙋 要教練決定：無新增。
🤫 等教練自己提起：巴哈要不要重新開放研究工具（目前只出海報）。
🤫 等教練通知才掛軍火庫（教練10/26 01:16定，他要先跟本人確認，不追問）：蔡曜隆（richrd-tsai）、莊哲昀 AJ（ohth-at-aj）、哈囉！潛錩規劃行銷（hello-brand，老闆＝紀宇牧）；之後教練還會上傳「布萊恩紅茶」（同類，品牌背後是一個人）。教練說「可以掛了」才用 skyteam_link_expert.py 或手動插入；鄭憲聰已改連新頁 sendstudio（skyteam 8386342、be38728）。
🔧 AI 自己的清單：①session_length 提醒在 Stop hook 文字仍只提輪數；②workspace 有 1 個別場刪掉的 inbox 檔、all-works 1 個沒推上去（不是本場）；③看門員 plist 已備份進 ops/launchagents_backup（待 commit）。

> 📦 10/25 09:05 棒（寶華姐頁、邀請函改版、頁尾第4連結40頁、公益足跡自動進真公益、吳錦昌頁）已封存：`handoff_archive/handoff_2026-10-25_0905_寶華姐邀請函頁尾第4連結與足跡自動化_archived.md`（待辦已併入本棒）

> 📦 10/25 03:04 棒（軍火庫邀請函、曾志雄頁、全站表頭、NMDA 陳佩君）已封存：`handoff_archive/handoff_2026-10-25_0304_軍火庫邀請函與曾志雄頁與全站表頭_archived.md`（待辦已併入本棒）

> 📦 10/25 01:40 棒（全站壞圖檢查＋上架查圖、軍火庫前24位、黃伯樂海報、BNI 來賓互動教材學習報告）已封存：`handoff_archive/handoff_2026-10-25_0140_全站壞圖檢查與軍火庫與學習報告_archived.md`（待辦已併入本棒）

> 📦 10/25 00:28 棒（全站拿掉生平、軍火庫補10位、巴哈燒光額度案例133）已封存：`handoff_archive/handoff_2026-10-25_0028_全站拿掉生平與軍火庫補10位與巴哈燒光額度_archived.md`（待辦已併入 01:40 棒與本棒）

> 📦 10/24 20:50 棒（頁尾三句補 35 站、巴哈海報改一行指令、孔令峯頁）已封存：`handoff_archive/handoff_2026-10-24_2050_頁尾三句與巴哈海報指令_archived.md`（待辦已併入本棒）

> 📦 10/24 19:35 棒（巴哈群組清理、施正益頁、天團連結）已封存：`handoff_archive/handoff_2026-10-24_1935_巴哈群組清理與施正益頁與天團連結_archived.md`（待辦已併入本棒）

> 📦 10/24 10:45 棒（人才軍火庫一排6人、巴哈群組塞爆、6 張海報改協會標題）已封存：`handoff_archive/handoff_2026-10-24_1045_人才軍火庫一排6人與巴哈海報標題_archived.md`（待辦已併入 19:35 棒與本棒）

> 📦 10/23 15:40 棒（NMDA 理監事頁、TAVA、Dock 最近使用）已封存：`handoff_archive/handoff_2026-10-23_1540_NMDA理監事頁與TAVA與Dock_archived.md`（待辦已併入本棒）

> 📦 10/23 06:25 棒（榮樹下「我要預約」自動占位、週六 9:30、案例130）已封存：`handoff_archive/handoff_2026-10-23_0625_榮樹下預約占位與週六930_archived.md`（待辦已併入 10/23 15:40 棒與本棒）

> 📦 10/23 02:30 棒（南應大理監事 23 位、記憶牆理監事名單、建置模式）已封存：`handoff_archive/handoff_2026-10-23_0230_南應大理監事23位與記憶牆_archived.md`（待辦已併入本棒）

> 📦 10/22 17:50 棒（推播許可旗標漏洞已修、榮樹下整段空檔預約）已封存：`handoff_archive/handoff_2026-10-22_1750_推播旗標與榮樹下整段空檔_archived.md`（待辦已併入本棒與 10/23 02:30 棒）

> 📦 10/22 12:25 棒（巴哈海報換人換字、meihua 上架）已封存：`handoff_archive/handoff_2026-10-22_1225_巴哈海報換人換字與meihua上架_archived.md`（待辦已併入本棒🔧第③項）

> 📦 10/21 19:20 棒（賈維斯自我檢測、規則越少越好）已封存：`handoff_archive/handoff_2026-10-21_1920_賈維斯自我檢測_archived.md`（待辦已併入 10/22 17:50 棒）

> 📦 10/21 09:35 棒（推播許可旗標殘檔、MiniMax 過載、不設備援裁示）已封存：`handoff_archive/handoff_2026-10-21_0935_推播旗標與MiniMax過載_archived.md`（待辦已併入本棒）

> 📦 10/21 09:24 棒（小旭老師報名通知、LINE 額度、my-tools 最近刪除、雲端根治）已封存：`handoff_archive/handoff_2026-10-21_0924_小旭報名通知與雲端根治_archived.md`（待辦已併入 10/21 19:20 棒）

> 📦 10/21 00:50 棒已封存：`handoff_archive/handoff_2026-10-21_0050_archived.md`

> 📦 10/21 08:55 棒（my-tools 驗收、含糊指稱鎖）已封存：`handoff_archive/handoff_2026-10-21_0855_my-tools驗收與含糊指稱鎖_archived.md`

---

> 📦 10/21 00:25 棒（雲端規則包與交件接手）、10/20 22:20 棒（LINE 額度 199 與推播閘門、常設禁令）已封存：`handoff_archive/handoff_2026-10-21_0025_2026-10-20_2220_雲端規則包與LINE閘門_archived.md`（待辦已併入 10/21 08:55 棒）

> 📦 10/19 11:36 棒（審查員觀察期、預約頁訪談緩衝、友善連結）已封存：`handoff_archive/handoff_2026-10-19_1136_審查員與訪談緩衝_archived.md`

> 📦 10/18 12:20 棒（Suno 加歌、守則 21 條融入對話、小龍蝦變聰明、提到群組一律寫全名）已封存：`handoff_archive/handoff_2026-10-18_1220_Suno加歌與守則融入對話_archived.md`（其待辦已併入 10/19 棒第 6 項）


---


---

> 📦 10/17 02:42 棒（守則納入賈維斯研究、案例128、容量與額度怎麼讀）已封存：`handoff_archive/handoff_2026-10-17_0242_守則納入賈維斯研究_archived.md`（審查員／提醒次數／規則體檢已完成，見本棒）

> 📦 10/17 02:05 棒（Discord 榮樹下開通、手機遙控修復、陌生詞先問）已封存：`handoff_archive/handoff_2026-10-17_0205_Discord榮樹下與手機遙控_archived.md`

> 📦 10/17 00:50 棒（Discord 兩種腦、先查再答、教練原話線索）已封存：`handoff_archive/handoff_2026-10-17_0050_Discord先查再答_archived.md`

> 📦 10/16 19:45 棒（workspace 被拉錯分支事件、守門員與技能、盤查救回）已封存：`handoff_archive/handoff_2026-10-16_1945_軍師棒_archived.md`（待辦清單已併入新一棒）

> 📦 10/16 23:55 棒（Discord 建置過程、被糾正的兩個低級錯、金鑰防護、教練原話線索）已封存：`handoff_archive/handoff_2026-10-16_2355_Discord建置_archived.md`

> 📦 10/16 15:10 追加棒（網站斷線通知、香檳下午茶頁上架）已封存：`handoff_archive/handoff_2026-10-16_1510_香檳下午茶追加_archived.md`

> 📦 10/16 01:55 聯想 v259 棒已封存：`handoff_archive/handoff_2026-10-16_0155_聯想v259_archived.md`

> 📦 10/16 02:10 棒、13:06 棒已封存：`handoff_archive/handoff_2026-10-16_0210_1306_網站斷線守門員_archived.md`

