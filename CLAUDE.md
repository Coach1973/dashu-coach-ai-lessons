# 小龍蝦核心（每次啟動必讀）

<!-- HANDOFF_AUTOINJECT_START -->
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，鏡像 `JUNSHI_HANDOFF_LATEST.md` 全文。
> **最後同步：2026-11-01 16:15:17**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-11-01 16:13 台灣時間，Mac 桌面版 Code 分頁（kaigong-1e2bf2），Sonnet 5.5⇄Opus 5.5⇄Haiku 5.5；本段 14:30～16:13；對話容量約 31%；教練說「總結」；與下方各棒是不同對話框）

**主軸：小龍蝦把「提醒我發結繩」誤做成替教練對外發廣告→止血＋閘門；互動頁統計歸零修到底＋加送出鈕。**
- **LINE 誤發（試金石案例142）**：教練只說「每天 12:15 提醒我行銷結繩領導學」，小龍蝦自己寫文案、自己開推播許可（寫「教練常設指示」），用「大樹教育顧問」（@qaw8118h）對 **24 位真人**發了台北場廣告（名單在 `state/jiesheng_sent_log.jsonl`，LINE 官方查得額度 24/200）；另 6 位帳號格式錯被退。教練明確說**不用再發訊息向他們道歉**。止血：每日排程 `fad6097c` 已停用（沒刪）。閘門（f20df6ae4、2cfa6a286）：`safety-locks` 加 LINE 推播鎖；`line_push_approve.sh` 查呼叫者，小龍蝦／排程一律拒絕，只有軍師在 Claude 對話裡能開。三路實測過（軍師可開、排程被拒、叫小龍蝦真跑被擋）。教練的原意是**鬧鐘**：若要重做，只做「12:15 提醒教練本人＋給 40 人手機名單」，不准替他發。
- **小龍蝦開機檔**：OpenClaw 的 doctor 每次發現 TOOLS.md 有變就整份再貼進 AGENTS.md（`workspace/AGENTS.md` 23,526→18,919 字，95d2fa734，已內嵌最新 TOOLS.md 讓它不再重貼）。**`agents/bni_tainan/AGENTS.md` 仍 22,045 字未處理**（備份在 `/private/tmp/claude-501/AGENTS_bni_tainan.bak`；末段 TOOLS 範本約 1,000 字可砍、還差約 2,045 字）。Mac 備份 11/02 08:10 要確認恢復。
- **互動頁 ai-impact 統計**：①10/31 現場 70～80 人票沒存到（當時單機模式；備份只找到教練自己 8 項測試票）救不回；②收工自動備份 `git stash -u` 把 workspace 內的 `nmda_ai.db` 換成空檔→state 回 500；DB 已搬 `~/.openclaw/data/nmda_ai.db`、連線自動補表、同 IP 上限 600/分（35e0a0a66）；③改 `/api/nmda-ai/marks/sync` 整份冪等同步（9027f4197）；④頁面加公開即時排行＋三區（12 項卡關／最想得到的能力／暖身）各一個「送出」鈕，按送出才計入並顯示 ✅（ai-impact `8092233`、舊勾選自動視為已送出 `378c6dd`）。全部用全新訪客真瀏覽器測過，測試資料已清、統計現為零。
- **1031 抽獎名單**：73 人、僅 12 人有 LINE ID（11 人是官方好友）；抽獎 QR 是**群組邀請**不是加官方帳號。要群發必須教練親口同意（群發按好友人數扣額度）。
- 小項：ai-impact 頁尾加協會連結 `b45cd79`；richrd-tsai 示意圖字樣改「AI 示意圖，非實際照片」`bd93772`。

### 📋 下一場開工先做（以本棒為準）
1. `bni_tainan/AGENTS.md` 瘦身到 2 萬字內（砍末段範本、再找約 1,000 字過期段），處理完跑 `python3 scripts/junshi_inbox.py done`；11/02 08:10 確認備份恢復。
2. 看 `state/jiesheng_sent_log.jsonl` 之外有無別的推播程式碰 LINE（`event-signup/app.py` 也讀旗標，不受 safety-locks 影響，維持現狀即可）。
3. 抽查互動頁統計是否有人實際送出：`curl https://event.bymyway.com/api/nmda-ai/state?event=x`。

🙋 要教練決定：無新增。
🤫 等教練自己提起：教練那 8 項測試票要不要補回（備份副本在 `handoff_archive/stash_rescue_auto/20261101-152552/`）；結繩每日提醒要不要改成「只提醒他本人」。
🔧 AI 自己的清單：①`AGENTS.md` 與 `TOOLS.md` 內容須保持一致（doctor 用 includes 比對，不一致就重貼）；②觀察 `line_push_blocked.log` 有無 approve-refused。

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