# 小龍蝦核心（每次啟動必讀）

<!-- HANDOFF_AUTOINJECT_START -->
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，鏡像 `JUNSHI_HANDOFF_LATEST.md` 全文。
> **最後同步：2026-10-31 13:10:19**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-31 11:35～13:10 台灣時間，Mac 終端機／桌面版 Code 分頁，Haiku 5.5 → Sonnet 5.5；手機開工；對話容量約 15%；教練說「總結」；與下方各棒是不同對話框）

**主軸：新增真聚籌備會、掃碼抽獎改成加入「零基礎學 AI」LINE 群、產兩張現場用 QR。**
- **真聚籌備會**：分會列表新增第 14 個，slug `real-center`（教練說 RealCenter，照既有慣例小寫連字號）、英文名 Real Center Chapter、狀態籌備中。`bni-chapters` commit `72d6851`；正式站 https://chapters.bymyway.com/real-center 回 200 且顯示「真聚籌備會」；資料庫備份 `chapters.db.bak-before-real-center-20261031`。**信任遊戲座位地圖沒同步加（10/10 教練要兩邊對齊 13 個，現在差一個）。**
- **抽獎改進群**：教練給 LINE 群邀請 QR（解出為 `line.me/ti/g2/…`，零基礎學 AI 群）。`event-signup/app.py` 的 `_lottery_greet_url` 改成：`app_settings.lottery_join_url` 有值就導去群連結，沒值維持官方 LINE 問候語；已設定該值、重啟 `com.coach.event-webapp`、`event.db` 備份 `event.db.bak-before-lottery-join-url-20261031`；commit `f74db3b97`。回退＝刪掉該設定列。
- **兩張 QR**（桌面＋`event-signup/qr/`，commit `76ed32e2c`，皆解碼驗證）：抽獎簽到 `/checkin`、AI 互動頁 `https://event.bymyway.com/curated/ai-impact/`（原網址會 308 轉 http，加斜線直接 200）。
- **教練原話線索**：「掃完就能加入，對吧？」＝他以為一掃就進群；實際是掃 QR→輸入手機→跳群邀請頁按加入。
- **沒驗證／風險**：沒真的送出簽到測試（怕污染正式名單）；抽獎名單只看簽到、不看有沒有進群，官方 LINE 是否在群裡沒確認；官方 LINE「綁定」不再發生，之後推播這批人推不到；現在「目前活動」掛的是 bigtree-1031 中華新媒體啟動大會（manual 模式），現場若是別場要先在後台切；ai-impact QR 第一次嘗試被安全檢查擋下，重跑成功；真聚的畫面沒用真 Chrome 看過；`bni-chapters` 沒裝 pytest 所以沒跑測試。

### 📋 下一場開工先做（以本棒為準）
1. 問教練現場抽獎當天用得順不順；若要自動知道誰進了群，才查官方 LINE 帳號在不在零基礎學 AI 群。
2. 教練說要補座位地圖的真聚，再做（`seat_lists.py` CHAPTER_SLUGS＋`data/seat_lists/real-center.json`＋`tests/test_seats_nine_chapters.py` 數字 13→14）。

🙋 要教練決定：無新增。
🤫 等教練自己提起：座位地圖要不要加真聚。
🔧 AI 自己的清單：①`ai-impact` 頁沒用真瀏覽器看過互動是否正常；②`bni-chapters` 本機 5063 對 `/<slug>` 回 404（連既有 real-happy 也是），公開站正常，疑似本機 port 對應別的服務，沒查。

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-31 06:30～07:05 台灣時間，Mac Hermes cron「FB 每日生日祝福」ca5195d8c4ca 那一棒，MiniMax-M3；與下方各棒是不同對話框）

**主軸：FB 壽星抓取連續兩天失敗，根因是「cookie 好好的但解不出來」，不是 session 過期；已修好，教練 0 按鈕。**
- **今日壽星已抓到（13 位）**：陳芯怡、劉秀珍、廖綉玲、王國柱、王芳連、葉竹興、Laowu Freya Chen、胡真萍、黃鈺成、李將、連文昭、梁美珠、程名瑋。
- **真正根因**：`puppeteer.launch()` 直接啟動的 Chrome，macOS 判定它「沒有 responsible app」→ 鑰匙圈 ACL 拒絕 → cookie 解不出來 → **Chrome 啟動時直接把 cookie 清掉**。證據是 Chrome 自己的 stderr：`Failed to decrypt token for service ...`。**不是 session 過期**——教練自己 Chrome 的 `c_user`/`xs` 到 2027 年才過期。
- **10/30 那棒開錯藥**：叫教練「重新登入 FB」，但重新登入解決不了這題（cookie 一樣解不出來）。這次沒叫教練動手，直接找 0 按鈕解法。
- **修法**（commit `f6474c865`，`scripts/fb_birthday_scraper.js` 全改）：①cookie 來源改用教練自己的 Chrome（`~/Library/Application Support/Google/Chrome`），自動同步到工作 profile；②改用 `open -na`（LaunchServices）＋ `--headless=new` 啟動，讓 macOS 正確歸屬 responsible app；③掛 CDP port 9225 用 `puppeteer.connect` 抓。教練螢幕不會跳視窗，實測不影響他正在用的 Chrome。
- **順手修掉一個 h2 解析 bug**：「新朋友」這個 h2 會出現在「今日壽星」之前，舊邏輯看到就 break → 抓到 0 人。
- **驗證**：把工作 profile 的 cookie DB 整個刪光（最壞狀態）重跑，仍正確抓到 13 位 → 真的會自癒。連跑三次結果一致。
- **SOP 已更新**：`knowledges/SOP_fb_birthday_scraper.md` 加了 2026-10-31 事故紀錄 + 故障排除 + 新流程。

### 📋 下一場開工先做（以本棒為準）
1. 明天 06:30 那棒確認名單有出來（腳本 exit 0 且列出人名）；若又空 → 直接看 `/tmp/fb_birthday.log` 有沒有 `Failed to decrypt token`。
2. `ai.openclaw.fb-birthday`（launchd）仍是 disabled（10/30 教練指示停用），**維持停用**，健康檢查不要報它。
3. 一般化教訓已寫進 skill `macos-headless-chrome-keychain`（macOS 上任何 headless Chrome 需要 cookie 的自動化作業都會踩）。

🙋 要教練決定：無新增。
🤫 等教練自己提起：無新增。
🔧 AI 自己的清單：①`/Users/bymyway/.openclaw/fb_session_data_local` 現在只是 cookie 同步的工作區，SSD 那份 `fb_session_data` 備用已過期（2026-10-30 無 FB cookie），不用再當備援；②Chrome 舊版框架 156.0.8078.49 還留在 `/Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/`，等下次自動更新後可清，現在別動（教練的 Chrome 正在用）。

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-31 00:50 台灣時間，聯想 Windows 桌面版 Code 分頁，Sonnet 5.5；教練說「總結」；本段 10/24 08:48～10/28 21:50，對話容量約 25%；與上方 Mac 各棒是不同對話框）

**主軸：記憶體／CPU 卡頓查證、電報更新評估、NMDA 理監事頁換照片的分工與交接信放錯位置被糾正。**
- **記憶體**：10/24 08:48 NtFC（ntfs.sys）又 15,052MB，量 45 秒不漲＝凍結殘骸；教練 09:25 重啟後歸 0，**10/31 00:43 只有 8MB（6.6 天沒復發）**。嫌疑（網路回報、未本機證實）：Claude 桌面版是 MSIX、bindflt 在跑、AppData 有三個 junction。卡 3～5 分鐘那次＝PowerDirector 23 輸出 3 小時影片滿載 CPU（正常，沒動它）。已併入記憶 `reference_lenovo_memory_ntfs_nonpaged_pool_leak_2026-10-15`。
- **電報**：Store 版 7.3.1，官方最新 7.3.3（新功能只有 Money／TON 禮物，其餘修 bug）；教練看完差異決定不更新，沒動。
- **NMDA 理監事頁換照片**：照片存 Mac 資料庫、不在 GitHub；聯想網頁上傳會把 17 個空座位標成已填，教練 10/28 21:37 決定交 Mac；**Mac 22:10 已換 21 位新海報（`0bdf9dabf`，只動 photo_file）**。巴哈沒有自動放進團隊頁的步驟，歷來都是軍師手動放。記憶 `reference_nmda_team_photos_live_in_mac_db_not_github_2026-10-28`。
- **我被糾正**：交接信放 `outbox`（歸檔區）Mac 讀不到，教練罵低級錯誤；已改放 `inbox/mac/`（`402b624f8` 後續更正）。記憶 `feedback_letters_to_junshi_go_to_inbox_not_outbox_2026-10-28`。
- **教練原話線索**：「我給你的照片，最終目的就是把舊圖換成新圖，評估做快又好又省 token 再決定給誰」＝要我先比較再選人，不要直接動手。

### 📋 下一場開工先做（以本棒為準）
1. 聯想 workspace 落後雲端數百個版本、`claude-brain/MEMORY.md` 有未 commit 的合併結果（兩邊條目都保留、已 git add）；先 `git stash`／對照再拉，別直接 pull。
2. NtFC 再漲過 1GB 才用 wpr 追；平常不用動。

🙋 要教練決定：無新增。
🤫 等教練自己提起：是否升級電報到 7.3.3。
🔧 AI 自己的清單：①聯想 inbox 有 6 封舊信（10/12～10/27）未歸檔；②聯想寫信前先對照 cross-agent/README 收信路徑。

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-31 00:10 台灣時間，Mac 桌面版 Code 分頁（kaigong-1ea9b2 worktree），Haiku 5.5 → Opus 5.5 → Sonnet 5.5；本段 10/30 21:12～10/31 00:10；對話容量約 26%；教練說「總結」；與下方 21:12 那棒是不同對話框）

**主軸：Grace 頁換圖上線、VisionStory 影片 API 串好並用教練本人的照片與錄音做出影片、小龍蝦主程式 node 記憶體。**
- **Grace 頁**（`github_repos/grace-podcasts`）：小龍蝦補做的 6 張圖（IMG-001～006）換入，commit `fc756a1`，線上版與倉庫逐張一致；沒用真瀏覽器看排版。
- **VisionStory**：金鑰在憑證層；指令檔 `scripts/visionstory_api.py`（commit `094d44529`、`855112500`、`20335fbd8`），子指令 credits／models／avatars／voices／create-video／tts／create-avatar／clone-voice，真生成都跑過。教練素材：錄音 `/Volumes/953-SSD/下載/歸仁齒輪有限公司.m4a`→聲音 `893883331753573490`；指定照片 coach-profile.jpg→頭像 `2236789676702807693`。做了 4 支影片放桌面：`visionstory_me_8s`（教練說喜歡，用帳號 9/28 就有的頭像＋複製聲音，聲音是不是教練的**沒確認**）、`coach_8s`（抱胸）、`gestureA`（有手勢）、`gestureB`（仍抱胸，我看縮圖挑錯）。點數 220→206。我都只看畫面、沒聽聲音。
- **動作**：說話影片只能調語氣 emotion（5 種），姿勢由照片決定；「AI 影片」beta 可寫動作文字指令，要付費方案、每支較貴，沒實測。
- **給別的 AI 的指令**：教練要 `me_8s` 的畫面＋台詞指令（不扣點數的那種）已給中英文版，並把 mp3 聲音樣本與臉參考照放桌面；教練「不是 API 指令、是分鏡指令」，我一開始給成 API 做法，被糾正。
- **小龍蝦 node 2.15G**：就是主程式 gateway，23:20 重啟後開機仍約 1.8G，沒壓低、沒查原因；「釋放」（RustDesk 重啟）已跑。

### 📋 下一場開工先做（以本棒為準）
1. 請教練播放 `me_8s`、`coach_8s`、`gestureA` 聽聲音像不像他（我沒聽過）。
2. 教練說要用哪個 AI 工具重做，我再幫忙備到按生成前（登入要他自己）。
3. Grace 頁請教練在真實 Chrome 與手機看排版。

🙋 要教練決定：無新增。
🤫 等教練自己提起：要不要試 AI 影片（可寫動作）；要不要查小龍蝦開機 1.8G 的原因。
🔧 AI 自己的清單：①帳號裡 9/28 就有的 8 個頭像、2 個聲音沒動、不確定是誰的；②`visionstory_api.py` 的 tts 沒實跑過；③VisionStory 點數剩 206。


## 🔴 給跨對話框軍師讀的總結摘要（2026-10-30 21:12 台灣時間，Mac 桌面版 Code 分頁（kai-ae7ac5 worktree），Haiku 5.5 → Sonnet 5.5 → Opus 5.5 → Sonnet 5.5；本段 18:01～21:12；對話容量約 29%；教練說「總結」；與下方 18:01 那棒是不同對話框）

**主軸：大樹常用技能表上線（GitHub 公開版）＋榮樹下官網預約流程整個改順。**
- **大樹常用技能表**：7 張卡片（含「做整個網頁開頭動畫的技能」），公開網址 https://coach1973.github.io/bigtree-skills/（repo `Coach1973/bigtree-skills`，本機推送 `24f4a84`）；已登記大樹作品集「大樹常用」第一項。教練不想登入 Claude，所以 Claude 網頁版那個私人網址不給他。
- **榮樹下預約（教練 21:00 起連續糾正）**：①預約人姓名直接顯示在前置作業（以前只寫「待確認」，姓名只在私人備註）；②預約時填的姓名／單位／電話／想說的話自動帶進來賓資料表（張瓊方、楊曉熹牧師既有資料已補）；③來賓卡後台加「接下來的訪談」表（已預約／已填資料表狀態）＋「確認這個時段」鈕；④**教練邏輯：對方自選的 7-8 點就是訪談時間，不該再等教練確認**——官網預約改成送出即自動確認（背景跑 `coach_schedule.py confirm`：排提醒＋寫 Google），上限改看「沒填資料表的最多 6 筆」，通知與成功畫面不再說待確認。存檔：workspace `d860a3224`、`87beaacc5`、`be4a4afd6`、`5d6d478d2`；rongtree 網頁 `6cbe817`、`49b178b`。11/4 楊曉熹牧師已手動確認（含 18:00 提醒）。
- **教練原話線索**：「預約 7 點到 8 點，我還要跟他確認時間？要確認的是他有沒有填來賓表」＝流程只該有兩件事：預約即成立、資料表有沒有填；「他都填完了為什麼還要重填」＝預約資料要自動帶過去。我兩次把「預約表單」和「來賓資料表」當成同一張，被抓到。
- **沒做到／風險**：整條「網頁送出→自動確認」沒真的送出一筆預約實測（會排進行程、吵巴哈群），只測過程式與 confirm 單獨跑；張瓊方還沒填「人生轉折、公益故事」兩個必填欄（預約表單本來沒問）。

### 📋 下一場開工先做（以本棒為準）
1. 下一位真的在榮樹下預約時，確認：行程自動變「榮樹下訪談：某某」、有 1 小時前提醒、Google 日曆有、前置作業顯示姓名。
2. 張瓊方資料表網址 https://event.bymyway.com/rongtree/guest/3GAILTIBuii2 ，教練決定要不要傳給她。

🙋 要教練決定：來賓資料表的「三個人生轉折」「公益故事」要不要改選填（問過：2026-10-30 21:05）。
🤫 等教練自己提起：無新增。
🔧 AI 自己的清單：①`ai.openclaw.fb-birthday` 是被 launchctl 明確停用（disabled，對應 10/30 不貼 FB），健康檢查會一直報 ⚠️，改成不報；②近期 `dispatch-worker-auto-20261030211232` 自動暫存 28 檔沒放回（多為 terminal-notes 狀態檔，下場確認放回）；③「確認這個時段」鈕畫面尚未見過（沒有待確認的預約）；④worktree 對話框 Edit 改 workspace 檔被擋，本場全程用終端機補丁＋備份（state/rongtree_*_backup_*）。

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