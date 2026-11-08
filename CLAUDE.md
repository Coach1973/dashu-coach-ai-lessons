# 小龍蝦核心（每次啟動必讀）

<!-- HANDOFF_AUTOINJECT_START -->
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，只鏡像 `JUNSHI_HANDOFF_LATEST.md` 的最新一棒＋🙋區。
> **最後同步：2026-11-08 20:05:57**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-11-08 20:05 台灣時間，Mac 桌面版 Code 分頁，模型 Haiku→Sonnet 5.5；本場 16:55～20:05；教練說「總」）

**三件事，都已 commit／上線：**
1. **高價銷售 12 週課程影片轉 MP3**：64 支全轉好放 `~/Downloads/高價銷售12週/`（檔名＝章節編號_週_主題_順序_課名，共約 27 小時 941MB，逐支比對長度零差異），要丟 NotebookLM。轉檔不佔 token（ffmpeg 在本機跑）。腳本 `/private/tmp/claude-501/scratch/htc_mp3.py`（暫存、不在 git）。過程中我第一次把 `-f mp3` 放在輸出檔名後面，64 支全失敗，卻先回報「轉換中」，下一則才發現更正。
2. **「1-2B」＝GitHub `Coach1973/a-to-b`（本機 `~/github_repos/a-to-b`，線上 `event.bymyway.com/curated/a-to-b/`）**：回頂端按鈕（表頭＋右下浮動）、「60 秒」全改「30 秒」、「一業一家排他」改「一個專業類別一個代表」、第 7 關第 2 點改教練給的句子；第 2 關痛點 4 張卡改成 **16 張點擊翻牌**（LK888 出 12 張新圖 `pain_*.jpg`，翻牌不用 3D 轉換）；第 4 關「自己搭橋」4 個方法擴成 **11 個**；第 5 關三張拼圖卡正面 emoji 換成新繪插畫 `puzzle_clients/talent/mentor.jpg`。圖片網址加 `?v=` 版本號。最新 commit `1765925`。
3. **教練說 Windows 看不到 4 張圖**：查了很久（伺服器對 Windows UA 全正常、檔案格式相同），最後教練自己發現是「一直刷新的是 TAVA 的頁面，不是我的網頁」。我做的診斷頁已移除（`a0a7179`），保險措施（取消 lazy、檔名 pain_ads→pain_budget）保留。

**沒做／留著**：自檢程式（page_preflight）對 a-to-b 仍有舊有紅燈——開頭 A／B 圓點與三個按鈕對比、「表頭沒固定」（其實 `.hud` 已 fixed，疑似誤報）——是原本就有的，我沒動；「已收進背包」對比被誤報（實算 4.88）。

### 📋 下一場開工先做
1. 教練玩一遍 `https://event.bymyway.com/curated/a-to-b/`，有要改的文字／順序再改（第 7 關第 2 點下方說明文字是我自己改寫的，非教練原話，教練可能要改回）。
2. （舊）看日誌有沒有「🤐 安靜鎖觸發」「🔎 找工具鎖觸發」字樣，確認 v1.12 在真實對話有碰到。
3. （舊）等教練看 reemployment 網頁教練那一格臉大小；IMG-005 封面要不要重出、佩佩老師 LINE `lin.ee/vyFqWVB` 是否正確。

🙋 要教練決定：無新增。 🤫 等教練自己提起：①巴哈戰報時間修改（DnA 週一 09:55 提醒、戰報會議週五 20:55、每日 19:00 提醒改週五 21:00、清舊 DnA 系列 `i7s6juuaa9nic4jemi9s6og2lg`、sync-google＋時間衝突回報）——11/08 13:15 教練說「先停止工作」，我本場開工時問過要不要接手，教練沒答、轉去做 a-to-b，依 N2 不再追問。 🔧 AI 自己的清單：①a-to-b 舊有對比紅燈與表頭誤報可另排時間處理；②巴哈每日 19:00 戰報提醒改 command 型；③v1.11 叫醒鎖可考慮刪。
- 記憶：`reference_a_to_b_1_2b_page_structure_and_flow_2026-11-08.md`、`feedback_background_batch_verify_result_before_reporting_2026-11-08.md`。

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