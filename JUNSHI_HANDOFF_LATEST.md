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


## 🔴 給跨對話框軍師讀的總結摘要（2026-11-06 14:30 台灣時間，Mac 桌面版 Code 分頁（kai-2d6c69 worktree），Haiku 5.5→Sonnet 5.5；本段 13:01～14:30；教練說「總結」；對話容量約 22%）

**主軸：照上一場交辦清出本機空間，本機可用 31G → 71G（df 前後實測），並把 Amber 接回、查清它的 305G 是什麼。**
- **已完成**：①刪 `Claude-3p/vm_bundles` 11G（教練口頭授權＋通行證）；②`~/.openclaw/.git` 25G 搬到 SSD（`/Volumes/953-SSD/Mac應用資料/openclaw-git/.git`），本機 `.git` 改成指向它的捷徑；另一份保險備份在 Amber `大樹大腦備份/openclaw-git-backup-20261106/.git`。兩份核對：檔案數都 2222、大小 25G、HEAD 相同、fsck 無錯；換前換後檔案清單逐一比對無差異；③Amber「名片媒合中心」23M 已刪（19 個檔案逐一 md5 與本機 `team_uploads`/`public_uploads` 一致才刪）；④Chrome 5.9G 在 13:37 已被另一個視窗搬到 SSD，我沒重做（正在跑的 Chrome 有 215 個檔案開在 SSD）。
- **Amber 連不上的真因（查到）**：SMB 登入帳號是 `bymyway7`（AmberCloud email 前半，Amber 後台「檔案服務」頁寫明），不是主機名 `amber-Coach`；鑰匙圈存的就是 bymyway7。現掛載點 `~/amber-mnt`（不是 `/Volumes/home`）。macOS 沒有 `timeout` 指令，用 `perl -e 'alarm N; exec @ARGV'`。
- **Amber 305G 報告**：TimeMachine sparsebundle 244G（時光機自己算只用 135G、僅 10/29、10/30 兩個備份點、上限 150G；推論多的約 109G 是空殼、要 hdiutil compact，**未證實未動**；結果代碼 56 未查）、Videos 20G（2024 課程影片，教練說重要不動）、其餘合計不到 1.2G；約 40G 來源未查明。
- **教練糾正／裁示**：①SSD 半年才斷一次，**不准再拿它當問題問**（我第一段就讀到卻還問）；②時光機只留最近幾次穩定備份，不要佔那麼多；③名片辨識系統早已打掉重練、全在 Mac 本機，我先前說「名片辨識停著」是看舊錯誤紀錄（最後寫入 10/30）誤判。

### 📋 下一場開工先做
1. 時光機 sparsebundle 壓縮可行性實測（Amber 空間，預期釋出約 100G）：先確認時光機沒在跑、Amber 掛載、備份檔未被占用；實測安全再請教練決定；查結果代碼 56 與那 40G 來源。
2. 清舊監看設定：`~/Library/LaunchAgents/com.coach.namecard-amber-watch.plist`（指向已刪的 Amber 資料夾，早已無作用；改前先 launchctl 確認未載入）。
3. 上一場第 5 項仍未做：`scripts/daily_team_rollcall.py` 加「本機硬碟 <30G 或 Chrome 暫存複本 >5 份」紅燈、逐字保險箱「6 小時沒新增」改白天才判；SSD 一掉線當下用白話通知教練（事件觸發，不輪詢）。
4. 「開工」worktree 約 88 份 32G 等超過 30 天用 `clean_up_worktrees` 一次清。

🙋 要教練決定：無新增。 🤫 等教練自己提起：無新增。 🔧 AI 自己的清單：上列 1～4。


## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務，AI 自己用，不算這一關。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
- 模組化下一步 4 項（名冊引擎／預約引擎／通用短網址／報名接口收斂）｜只有教練能做：會改到 BNI、南應大、預約頁等夥伴正在用的系統，要教練拍板｜卡住名冊引擎開工｜問過：2026-10-14 報告第六節

🤫 等教練自己提起：①bymyway.com 後台登入一次（11/06 已問、未回；下一輪做到「建課程」那步才需要，到時直接講一句，不先問）；②高價銷售課程的價格、版本、網址放哪、舊工具課（Kajabi／GetResponse 等）標附錄或重錄（報告書第七節，教練說陪跑制不急）。
🔧 AI 自己的清單：①上列「下一場開工先做」1～3；②`.git` 25G：本機刪除前先對 SSD 備份跑 `git fsck`＋核對檔案數，再複製一份到 Amber（`~/amber-mnt`），並先對教練講「SSD 掉線時小龍蝦 commit 會失敗」的風險讓他決定；③SSD `Chrome.old-20261002` 5.3G 舊複本，確認新版穩定幾天後處理；④`daily_team_rollcall.py` 加本機硬碟 <30G 紅燈、逐字保險箱「6 小時沒新增」改白天才判，SSD 一掉線當下用白話通知（事件觸發）；⑤**11/06 14:2x `system_health_check.py --quick` 在 `verbatim_on_prompt.sh` 逾時 60 秒**，沒修，下一輪查；⑥「開工」worktree 88 份 32G 等超過 30 天用 `clean_up_worktrees` 清；量不到的 47G 沒查；`rules_health_audit.py` 仍提示執行細則與特助心法重複約 16 字，只出建議。
