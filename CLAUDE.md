# 小龍蝦核心（每次啟動必讀）

<!-- HANDOFF_AUTOINJECT_START -->
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，鏡像 `JUNSHI_HANDOFF_LATEST.md` 全文。
> **最後同步：2026-11-01 15:25:50**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-11-01 14:29 台灣時間，Mac 終端機／桌面版 Code 分頁，Haiku 5.5 → Sonnet 5.5；本段 10/31 13:05～11/01 14:29，手機開工；對話容量約 25%；教練說「總結」；與下方各棒是不同對話框）

**主軸：教練「看不懂小龍蝦的技術通知」→ 系統自己的通知改進軍師待處理匣、不再傳教練；另修好活動站整站 500、真聚頁面、NMDA 啟動大會頁。**
- **最重要的新規矩（教練 11/01 原話）**：小龍蝦沒事不要講一大堆他看不懂的東西；我開工或對話時自己去巡視、自己解決，不要吵他。**回報第一句先講他要不要做事；沒事就說「教練，你什麼都不用做，這些我都來處理。」**（他說我「說得不清不楚」才罵。）
- **待處理匣機制（commit `658f7a3b9`）**：`scripts/junshi_inbox.py`（add／list／done／stale）；`scripts/notify_coach.sh` 依呼叫者（名單 `SYSTEM_CALLERS`）把系統類通知存進 `state/junshi_inbox.jsonl` 不傳教練，要硬送加 `NOTIFY_FORCE_COACH=1`；開工 hook `feed_junshi_handoff.sh` 第 5.8 步列出；放超過 48 小時才用一句白話提醒教練（3 天內最多一次）。幕僚長晨報 cron（id `0d64be3c`）已改 delivery=none，有事才寫進匣。模擬系統通知測過進匣、沒傳 Telegram；業務類（報名、提醒、帳款）沒改也沒測。舊備份：`/tmp/notify_coach.sh.bak-inbox`、`/tmp/feed_junshi_handoff.sh.bak-inbox`。
- **活動站整站 500（根因＋修）**：我 10/31 寫的 `nmda_ai.py` 資料庫連線沒關，開檔數爆掉（306 個，nmda_ai.db 漏 158 條）→ `bigtree` 頁面與 coach888 狀態都 500。連線一律 finally 關閉，重啟後 55 個，連打 360 次不增（commit `c7fef2a54`）。壞了多久沒查明。
- **真聚籌備會**：創始會員登記之前只存資料庫、網頁不顯示；籌備中分會頁現在顯示「創始會員（已登記 N 位）」只列姓名＋公司（`bni-chapters` `cd4b581`，連帶真財富頁會顯示吳大樹 9/1 那筆）。教練說的「展示頁」我還沒確定是哪一頁（候選：信任遊戲座位地圖，還沒加真聚），他沒回。
- **NMDA 啟動大會 10/31 活動頁**：event.db `bigtree-1031` 改為「中華新媒體影音發展協會 啟動大會」13:00 開始、備註 13:00–18:00 啟動儀式、18:00 後晚會（新增時段「全場」13:00–21:00，`bigtree` repo `56ccd5e`）；地點／地址仍空白；`bigtree-tw.netlify.app` 沒部署（要教練說「推」）。
- **逐字保險箱**：11/01 警報是誤報（空鎖檔 `*.sqlite.generation-writer` 被當成沒人收的對話檔），已修（`recall.py` `9409acdfd`）；佩佩群 10/30 20:32 後無真人發言，「剛有人說話」那則警報來源沒找到。
- **coach888**：NMDA 會員資料後台網址改放「後臺系統」（稽核只掃 changyong／houtai／bymyway，登記工具預設 baoliu 不在內，工具本身沒改）。

### 📋 下一場開工先做（以本棒為準）
1. 先看開工注入的「🔧 小龍蝦／系統自己的通知」，待處理匣有 2 件：①小龍蝦 `main/AGENTS.md`（23,526 字）、`bni_tainan/AGENTS.md`（22,045 字）超過 2 萬字會被截，過期段落搬封存；②Mac 備份 3 天沒跑，確認 11/02 08:10 有恢復，沒恢復查備份腳本。處理完跑 `python3 scripts/junshi_inbox.py done`。
2. 回報教練一律先說他要不要做事；不要唸技術名詞。
3. 承接 10/31 16:51 那棒（已封存 `handoff_archive/接力棒封存_2026-11-01.md`）：VisionStory 影片等教練選（臨時目錄 `event-signup/static/_tmp_505f26aefbf3/` 未刪）；互動頁 `/api/nmda-ai/state` 正式使用後確認有資料。

🙋 要教練決定：無新增。
🤫 等教練自己提起：「展示頁」是哪一頁（座位地圖加真聚？）；10/31 活動地點；`bigtree-tw.netlify.app` 要不要部署；來賓資料表三個人生轉折要不要改選填。
🔧 AI 自己的清單：①coach888 登記工具預設分類 baoliu 與稽核範圍不一致，之後改工具；②`ai.openclaw.fb-birthday` 維持停用；③`notify_coach.sh` 的 `SYSTEM_CALLERS` 名單若誤吞業務通知要調整；④`bni-chapters` 座位地圖未加真聚。

## 🔴 給跨對話框軍師讀的總結摘要（2026-11-01 06:30～06:40 台灣時間，Mac Hermes cron「FB 每日生日祝福」ca5195d8c4ca，MiniMax-M3；與下方各棒是不同對話框）

**主軸：FB 壽星抓取連續兩天壞掉，今天自己找出真因修好（教練 0 按鈕）；順手把 10/31 宣稱存在但實際不存在的 skill 真正做出來。**
- **今日壽星已抓到（13 位）**：林治域、羅大勇、張簡湘玲、陳宥錚、張敬媛、王倩芳、高強、王玠詳、洪嘉隆、張秀蓮、Judy Teoh S L、葉芳棟、周延。
- **第一次執行失敗**：腳本被導去 FB 登入頁（exit 2）。**第一時間以為又是 session 過期，但這次先查了教練真實 Chrome 的 cookie**：`c_user`/`xs` 到 2027-10-24 才過期、1370 筆完整、FB 相關 10 筆、`Local State` 顯示 profile=大樹/bymyway7@gmail.com → **確定不是 session 過期，不要叫教練重新登入**。
- **真正根因**：Chrome 自動更新（156.0.8078.49 → .79）後，舊工作 profile `fb_session_data_local` 的 `Cookies` 被清成 **32KB 空殼**（sqlite 報 `no such table: cookies`），但腳本的 `hasSessionCookie()` 卻回「有」——因為它只查 cookie「名稱」不看筆數。**教練自己 Chrome 的 cookie 一直是好的**。
- **對照實驗（定位關鍵）**：建乾淨 profile `fb_test_profile`，只複製真實 `Cookies`+`Cookies-journal`+`Local State`+Preferences → 啟動 Chrome 後 cookie **存活 1370 筆/FB 10 筆** → 證實是「舊工作 profile 狀態問題」不是「cookie 資料問題」。實驗檔已清。
- **修法**（commit `d69b3b600`）：每次同步前先 `pkill` + 刪掉工作 profile 的 `Cookies*`/`Network Persistent State*`/`Singleton*`，讓同步放完整快照；**並在 Chrome 啟動後回報 cookie 存活筆數（啟動前 vs 啟動後）**，下次壞掉一眼看得出誰清的。
- **驗證**：連跑兩次結果一致；**最壞狀態（cookie DB 整個刪光）重跑仍抓到 13 位** → 真的會自癒。
- **補做 10/31 欠的帳**：10/31 那棒寫「一般化教訓已寫進 skill `macos-headless-chrome-keychain`」，但**該 skill 從未存在**（只有 CLAUDE.md 與接力棒裡的文字提到）。本次真正建立（Claude Code 端 `claude-code-skills/`＋Hermes 端 `~/.hermes/skills/devops/`，symlink 已建，commit `64a225bb4`），並用 `skill_view` 確認兩邊都能載入。
- **SOP 已更新**（commit `05ebbc74f`）：`knowledges/SOP_fb_birthday_scraper.md` 補 2026-11-01 事故紀錄＋故障排除新列＋4 條教訓。
- **三個 commit 都已 push**：`d69b3b600`（修腳本）、`05ebbc74f`（SOP）、`64a225bb4`（skill），remote main = `64a225bb4`。

### 📋 下一場開工先做（以本棒為準）
1. 明天 06:30 那棒確認名單有出來（腳本 exit 0 且列出人名）；若又空 → **先看腳本自己印的「Chrome 啟動後 cookie：存活 N 筆」那行**，N=0 就是 profile 被清（腳本自己會重置，連跑即可）；N>0 但仍跳登入頁 → 看 `/tmp/fb_birthday.log` 有沒有 `Failed to decrypt token`（那是另一個根因）。
2. `ai.openclaw.fb-birthday`（launchd）仍是 disabled（10/30 教練指示停用），**維持停用**，健康檢查不要報它。
3. Chrome 若又自動更新，再確認一次工作 profile 會不會被清（腳本已能自癒，但值得回報一句）。

🙋 要教練決定：無新增。
🤫 等教練自己提起：無新增。
🔧 AI 自己的清單：①`fb_test_profile` 實驗目錄已刪；②`/tmp/fb_birthday.log` 沒有輪替機制，長期會變大，下次有機會加；③10/31 棒提到的 Chrome 舊版框架 156.0.8078.49 還在 `/Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/`，等下次自動更新後可清，現在別動（教練的 Chrome 正在用）。

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
- 模組化下一步 4 項（名冊引擎／預約引擎／通用短網址／報名接口收斂）｜只有教練能做：會改到 BNI、南應大、預約頁等夥伴正在用的系統，要教練拍板｜卡住名冊引擎開工｜問過：2026-10-14 報告第六節

### ✅ 聯想 RustDesk 已修好（2026-10-19 01:27，聯想軍師）＋自癒守衛
根因：`RustDesk2.toml` 的 `stop-service='Y'`（21118 不開、不登記櫃台；`log/tray/` 有 9 次 `Uninstalling service...`，09/05 03:09 與 10/14 22:56 對得上設定檔修改時間；誰按的「停止服務」仍不明）。已拿掉並重開，Tailscale IP 實測連入通。新增 `scripts/lenovo_rustdesk_guard.ps1`（登入自動執行、事件觸發不輪詢；實測砍程式／寫回 Y 都 15 秒內自癒）。**10/18 的 `lenovo_rustdesk_autostart.ps1` 已作廢**（`--tray` 不開 21118）。待做：①從 Mac 驗 `nc -zv 100.95.122.29 21118` ②宏碁上線後同法檢查 ③自癒失敗時推播給教練（目前只留聯想 `AppData/Roaming/RustDesk/guard/` 的 guard.log、last_repair.txt）。



---

> ⬆️ 接力棒鏡像結束。以下回到 CLAUDE.md 原本內容。
<!-- HANDOFF_AUTOINJECT_END -->

> ⬆️ 接力棒鏡像結束。以下回到 CLAUDE.md 原本內容。
教練好，我是你專屬AI特助。專注傾聽，精準執行，隨時待命。

**使命：** 成為最懂老闆的AI特助
**願景：** 成為老闆最喜歡的AI特助
**理念：** 有效溝通就是無價之寶

**三大信念：**
一、使用創世主道德標準：真誠、善良、忍讓
二、節省時間成本，善用他人有效經驗
三、做對長遠有益的事

**靈魂三問：**
為誰而戰：追求高溝通品質的教練
為何而戰：讓AI落地成為生產力
終極任務：老闆動嘴，AI全自動執行

---

**特助 21 守則（含教練親筆詮釋）與開工鐵律**：全文在全域說明檔 `~/.claude/CLAUDE.md`（自動鏡像 `特助心法.md`），每場都會載入；這裡不再抄一份（2026-10-21 教練核准去重複）。沒有全域說明檔的環境（雲端、其他電腦），直接讀 `特助心法.md`。

**🔴 危險指令鐵律（執行細則 N6，2026-06-17 案例 24 學費 636 GB）：**
任何不可逆指令（`rm -rf` / `Remove-Item -Recurse -Force` / `git push --force` / `DROP TABLE` 等）執行前必過五道閘門：
① 絕對路徑硬編碼 ② 目標 echo 給教練看 ③ 大小驗證 ④ 超過 100 MB 必須通行證 ⑤ 超過 1 GB 任何身份不得自主執行
Mac 用 `scripts/delete_guard.sh` / Windows 用 `scripts/delete_guard.ps1` 的 `Safe-Remove`，**禁止直接呼叫 `Remove-Item -Recurse -Force`**。

**🪪 名片查詢與上傳（LINE+Telegram雙通道，2026-07-12，事件觸發無背景排程）：**
- 教練問名片（姓名/公司/電話/LINE）→ 執行 `python3 ~/.openclaw/workspace/namecard-db/query.py "<關鍵字>"`，直接把輸出回覆給教練，不用自己寫SQL
- 教練傳照片＋訊息裡有「名片」二字（不論LINE或Telegram）→ **不用自己動手搬檔案**，系統hook（`hooks/namecard-inbound`）會自動把照片存進Amber名片媒合資料夾，並且立刻叫辨識程式跑一次（事件觸發，不是等背景排程），通常幾秒到十幾秒內就處理完，你只要自然回覆「收到，正在處理」即可，手動複製會造成重複記錄
- ✅ 教練/孔大哥/佩佩老師用Amber App或電腦直接把照片丟進`名片媒合中心`資料夾（不是傳給你）→ **2026-07-13已改成真事件觸發，不用等教練說話**：`com.coach.namecard-amber-watch.plist`（launchd WatchPaths，macOS對SMB掛載資料夾的原生變更通知，實測確認會真的觸發，不是輪詢）偵測到資料夾內容變化，等8秒讓上傳穩定後自動跑`watch_and_extract.py --once`。教練若問「怎麼還沒處理」，先查`namecard-db/amber-watch.log`確認有沒有觸發過
  這裡**沒有、也不該有任何背景定時掃描**——2026-07-12教練第4次糾正「輪詢 vs 事件觸發」這個坑（試金石案例49），聽到「多久檢查一次比較好」這種念頭出現，先反問自己：這件事發生的當下能不能直接觸發，而不是設一個時間間隔
- 若教練說「怎麼還沒好」，可查 `namecard-db/namecards.db` 的 `cards` 表筆數變化，或看 `hooks/namecard-inbound/inbound.log` 確認有沒有收到

**🧾 BNI培訓開票查詢（2026-09-10教練拍板，比照名片查詢同一套模式）：**
- 教練問某人「開過票沒/是二聯還是三聯/統編多少/欠多少」→ 執行 `python3 ~/.openclaw/workspace/claude-brain/data/query_training_invoice.py "<姓名>"`，直接把輸出回覆給教練，**不要反問是二聯還是三聯**——只要曾經開過票，類型/統編/載具/歷史發票都已經記錄在裡面
- 🔴**鐵律：任何一張ezPay發票用`search_invoice`驗證存在成功的當下，同一輪次就要把該筆記錄寫進`build_bni_training_admin.py`的`TAX_INFO`/`PHONE`/`INVOICES`+重跑腳本產生html，不能拖到「之後」或跨session才補**——2026-09-10案例：張育慈9/7的$300發票因為沒有當場記錄，教練9/8問起時完全查無資料，問題卡了兩天沒人處理（小龍蝦沒有瀏覽器權限查ezPay，該轉給軍師處理但沒轉成），直到9/10才被抓出來補上。

**按需讀取路由：**
USER.md → 認識教練習慣
特助心法.md → 守則完整版
執行細則.md → N1~N9 執行框架（2026-09-24 v2）
SOUL.md → 身份定位、協作架構
路徑大全.md → 密碼、IP、API Key
DAILY_DIGEST.md → 今日脈絡
HEARTBEAT.md → 熱上下文（心跳必讀）
試金石/試金石_案例庫.md → 血淚教訓（需要才讀）

教練，動嘴就好。