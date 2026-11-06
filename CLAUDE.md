# 小龍蝦核心（每次啟動必讀）

<!-- HANDOFF_AUTOINJECT_START -->
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，只鏡像 `JUNSHI_HANDOFF_LATEST.md` 的最新一棒＋🙋區。
> **最後同步：2026-11-06 15:20:58**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-11-06 15:20 台灣時間，Mac 桌面版 Code 分頁（此對話為 Sonnet 5.5；開頭由 Haiku 5.5 起手），本段 14:37～15:20；教練說「總」；對話容量約 26%）

**主軸：教練貼「高價銷售課程上架報告書」要求「照上一輪說的、掛在 bymyway 執行」→ 影片通道＋Tutor 課程整套建好；時光機壓縮只做檢查沒動。**
- **高價銷售 12 週陪跑課程已建進 bymyway.com**：課程 ID **27448**，狀態「**私人**」（教練 15:13 裁示維持私人，只有管理員看得到），13 章節、77 堂（64 支影片＋13 個「本週講義與作業」頁，附件 40 份、作業文字都在）。真 Chrome 實測 `設立基礎` 課堂頁影片可播（1080p、22 分）、拖曳進度條正常、附件與作業文字在。我試做的 3 個測試課堂（L1/L2/L3）已丟垃圾桶。commit `e0d5965cb`（影片伺服器）、`30a9e8dd3`（課程規格）。
- **影片通道**：Mac 只讀伺服器 `knowledges/高價銷售課程/htc_video_server.py`（127.0.0.1:5075，只送 ~/amber-Videos 的 mp4、Referer 限 bymyway.com、支援 Range）＋ cloudflared 通道 `htc-video` → `htcvideo.bymyway.com`，launchd：`com.coach.htc-video-server`、`com.coach.htc-video-tunnel`（已載入，公開網址實測 206）。**限制：Mac 關機／斷網／Amber 沒掛上，課程影片就播不出來。**
- **Tutor 3.9.15 的坑（已寫記憶）**：新版課程編輯器程式沒載入（wp-admin 與前台 dashboard 都空白）、`tutor/v1` REST 對登入 cookie 一律 403；改用教練在 Chrome 的登入狀態打 admin-ajax：`tutor_save_topic`（`title`＋`course_id`）、`tutor_save_lesson`（`topic_id`、`course_id`、`title`、`description`、`video[source]=external_url`、`video[source_external_url]`、`tutor_attachments[]`）、`tutor_update_course`（要 `post_author`＝2）。草稿課程的課堂前台是 404，預覽要改「私人」。記憶檔：`reference_bymyway_tutor_course_build_via_ajax_htc_video_tunnel_2026-11-06.md`。
- **時光機壓縮（教練說「排時間壓縮」，我先做檢查就被新指示插隊，沒排）**：Amber 已掛載、時光機沒在備份；`tmutil` 自動備份是關的（AutoBackup=0）；Mac 設定永不睡眠；sparsebundle 244G 目前被系統掛著（`hdiutil info` 可見 /dev/disk5），Results.plist 結果代碼 **56**，已用 135GB、剩 15GB（上限 150G）。壓縮要先卸載再 `hdiutil compact`，網路硬碟上會跑很久；**未卸載、未壓縮、未建任何排程**。
- **舊名片監看排程**：`com.coach.namecard-amber-watch` 已 `launchctl bootout` 停用（`launchctl list` 確認不在了），但想把 plist 搬去備份資料夾被權限擋（Permission denied），**檔案還在 `~/Library/LaunchAgents/`**，重開機也不會載入。
- **TAVA**：教練問「TAVA 做好了把打包檔案給你就可以？」→ 答「對」：給我 HTML＋CSS＋圖片資料夾，我放進 WordPress 銷售首頁（先私人）、把按鈕接到申請表／預約頁、檢查手機版與 20px。價格、自學版／陪跑版是否分開賣還沒決定。

### 📋 下一場開工先做
1. **時光機壓縮排程**（教練已說「排時間壓縮」）：先挑時段（任何時段都不會與自動備份互撞），腳本要含防呆（確認沒在備份、備份檔沒被占用、卸載成功才 compact、全程 log、失敗不留半殘狀態），用乾跑驗證檢查項目後排 launchd 一次性任務並讀回確認；再查結果代碼 56 與那 40G 來源。壓縮動作本身不可逆性高，執行前對教練講一句時段與預估時間。
2. 高價銷售課程後續（教練說了才做）：TAVA 首頁進來後放進 WordPress；每週自動解鎖（Tutor Pro Content Drip）；作業改 Tutor 作業題型；結業證書；價格與購買頁；公開前把影片防護從 Referer 檢查升級成有時效簽名網址。
3. 殘留：`com.coach.namecard-amber-watch.plist` 檔案還在（已停用）；`scripts/daily_team_rollcall.py` 加「本機硬碟 <30G 或 Chrome 暫存複本 >5 份」紅燈、逐字保險箱「6 小時沒新增」改白天才判；「開工」worktree 約 88 份 32G 等超過 30 天用 `clean_up_worktrees` 清。

🙋 要教練決定：無新增（課程維持私人已裁示）。 🤫 等教練自己提起：高價銷售課程的價格、版本、舊工具課標附錄或重錄。 🔧 AI 自己的清單：上列 1～3。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
- 模組化下一步 4 項（名冊引擎／預約引擎／通用短網址／報名接口收斂）｜只有教練能做：會改到 BNI、南應大、預約頁等夥伴正在用的系統，要教練拍板｜卡住名冊引擎開工｜問過：2026-10-14 報告第六節

🤫 等教練自己提起：①bymyway.com 後台登入一次（11/06 已問、未回；下一輪做到「建課程」那步才需要，到時直接講一句，不先問）；②高價銷售課程的價格、版本、網址放哪、舊工具課（Kajabi／GetResponse 等）標附錄或重錄（報告書第七節，教練說陪跑制不急）。
🔧 AI 自己的清單：①上列「下一場開工先做」1～3；②`.git` 25G：本機刪除前先對 SSD 備份跑 `git fsck`＋核對檔案數，再複製一份到 Amber（`~/amber-mnt`），並先對教練講「SSD 掉線時小龍蝦 commit 會失敗」的風險讓他決定；③SSD `Chrome.old-20261002` 5.3G 舊複本，確認新版穩定幾天後處理；④`daily_team_rollcall.py` 加本機硬碟 <30G 紅燈、逐字保險箱「6 小時沒新增」改白天才判，SSD 一掉線當下用白話通知（事件觸發）；⑤**11/06 14:2x `system_health_check.py --quick` 在 `verbatim_on_prompt.sh` 逾時 60 秒**，沒修，下一輪查；⑥「開工」worktree 88 份 32G 等超過 30 天用 `clean_up_worktrees` 清；量不到的 47G 沒查；`rules_health_audit.py` 仍提示執行細則與特助心法重複約 16 字，只出建議。

> 前一棒、🤫／🔧 待辦、封存索引：需要才讀 `JUNSHI_HANDOFF_LATEST.md`。問教練之前的三關：見執行細則 N2。


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