## 🔴 給跨對話框軍師讀的總結摘要（2026-10-03 00:05 台灣時間，Mac 桌面版 Sonnet 5.5↔Opus 5.5，v272）

**主軸：開工注入瘦身成「心法＋最新一棒」（30KB→9.7KB）；〈為你轉身〉導師席換成八位真人；ema1017 流程改；team01 戰情表講清楚「未來週次不開放填寫」。**

### 做了什麼
1. **開工注入 v3**（commit `bcf46f17c`→`d80a71691`）：`feed_junshi_handoff.sh` 只貼最新一棒＋🙋區，拿掉過期 HEARTBEAT 尾段／空 memory／已轉反射的試金石與 Top10／重複的三關；全域與 workspace CLAUDE.md「開工鐵律」同步改 v3（`d80a71691`）。教練問「心＋最新一棒」的「心」→ 實為「心法」，已改寫（`348b5aa25`）。同場補 `stop_rules_master.py` 徵詢偵測三句型「等你決定／要不要把…？／還是先…？」（回測 30 天 83 行）。
2. **〈為你轉身〉**（event.bymyway.com/curated/turnforyou/，資料夾 `~/github_repos/turnforyou`，**非 git**，備份 `index.html.bak-20261002(-b/-c)`、`data.json.bak-…`）：導師席 8 位現為 連啓佑／邱裕榮／施正益／顧瀚鈞／鄒昆廷／李中閔／王夏儷／凌榆舜（連第一、凌最後，教練指定）。鄒、李、王來自 mentor100 DB（照片、資歷皆取自本人填寫）；施正益資料取自教練貼的文字＋Threads 公開簡介，照片為其 Threads 頭像；邱裕榮照片是教練放 Downloads 的 images.jpeg（447px，偏軟）。頁面「八位」文案、領域清單、「選條件看路徑」席次對應、觀眾席（鄒王李移出、余尚恩放回）都已對齊。registry 描述 commit `a3baa90d4`、`b44100c82`。結構坑見記憶 `reference_turnforyou_site_structure_2026-10-03.md`。
3. **ema1017**（`~/github_repos/ema1017`，非 git，備份 `index.html.bak-20261002`）：時程改成 15:00 報到／15:30 小提琴開場／15:35 大樹開場／15:45 網紅協會理事長致詞並介紹有機水產火鍋／16:00 零基礎學 AI／17:30 用餐／19:30 會後貴賓室交流；同頁兩處時間標籤、標題句一併改。
4. **team01 戰情表**（team01-guests commit `7191081`）：教練問「第十週按了沒出現四項指標」→ 第十週＝11/25，未到的週次本來就不開放填寫。改成欄位標題加日期＋「尚未到」、預設展開本月＋上月、說明文字改 15 次例會。教練會問怡靜要不要提前開放，要的話他再說；**不要主動追問**。
5. 聯想兩封信（Tailscale 離線→取消）已確認是教練自己關的，歸檔。

### 卡在哪／發現
- 聯想、宏碁用的開工腳本（`feed_junshi_handoff.ps1`）**沒比照瘦身**，仍整份貼。
- 「八張椅子」場景圖（stage／ceiling）仍是八張，人數剛好對上，不用處理。
- 名字用字：連**啓**佑（mentor100 本人登記）、施正**益**（Threads 顯示「施正義」，海報／LinkedIn／教練都是益）。

### 📋 下一場開工先做
⓪ **10/03 00:30 教練要裝 macOS 26.7.1 小更新**（cron「教練-系統更新提醒-10-03凌晨」會 Telegram 提醒）：教練回「更新」→ 先 `tmutil startbackup` 確認備份完成 → `softwareupdate -i "macOS Tahoe 26.7.1-25G241" -R`（要密碼走 `scripts/coach_password_dialog.sh`）→ 重開後驗小龍蝦／赫米斯／Tailscale（教練手動關著，別動）／RustDesk／外接 SSD。27.0.1 大改版不裝。
① 10/03 早上量剩餘空間（`diskutil info / | grep "Container Free"`，00:00 為 45.9GB，快照到期後應多約 20GB）；08:10 點名要有「💾 備份…已自動備份一次」。
② 驗收新版開工注入：開工回報應不被截斷、約 10KB；有問題改回 `feed_junshi_handoff.sh` 第 2~5 步。
③ 🔧 AI 自己做：聯想／宏碁 ps1 開工腳本比照瘦身（先看實際大小再決定）；10/09 後刪 `~/Downloads.bak.20261002`、`Chrome.bak.20261002`。
④ 回憶牆第一則真實投稿進來時確認群組收到；四場線上講座主題教練說改時會通知，不主動問。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 21:30 台灣時間，聯想 Windows 桌面版 Sonnet 5.5，v269，教練在聯想前）

**主軸：RustDesk 直連方案收尾（教練裁示：在家用 ID 就好、Tailscale 是備援）；ema1017 單檔HTML作品上線並教赫米斯；聯想接上條件反射與開工置頂交辦；Comet 瀏覽器 Google 被擋已修。**

### 1. RustDesk 現行方式（教練 10-02 15:24 親口裁示）
- 官方中繼 21117 仍壞（15:18 重測 False）。在家同區網：**用 ID（蘋果 99479569）就通**（兩台直連，不經中繼）。
- Tailscale＋IP 直連（蘋果 100.91.228.91:21118）是**外出備援**，不是全面更好。**蘋果的 Tailscale 是教練自己手動關的**（在家不想動），**不要重開、不要修**；已寫 `inbox/mac/…1526…cancel` 取消先前誤寄的「修 Tailscale」信。哪天教練要出門遠端才開。
- 聯想桌面有捷徑「RustDesk連蘋果」（`--connect 100.91.228.91`）：Tailscale 開著才通；在家直接用 ID。
- 教訓：我先判斷「蘋果 Tailscale 掉線」就寫信請 Mac 去修，沒先想到可能是教練自己關的，白寫一封。

### 2. 條件反射＋開工置頂（Mac 交辦，已完成並被 Mac 驗收 bee1a7653）
- 聯想 settings.json 加 5 個 reflex_router hook（備份 settings.json.bak_20261002_reflex）；`scripts/pick_next_task.py` 挑最新交辦，`feed_junshi_handoff.ps1` 置頂注入。新對話框才會真的觸發。

### 3. 其他
- ema1017 作品頁（單檔HTML＋4圖下載打包）已上線；SOP 已補「單檔HTML自己下載圖片打包zip」段；已寫信給赫米斯。
- Comet 瀏覽器 google.com.tw「遭到封鎖／拒絕連線」：真因是擴充功能 **Enhancer 4 Google**，教練移除後正常（無痕視窗正常是判斷關鍵）。
- 教練明講：自己產生的暫存檔直接刪、不要問。刪檔鎖需先建 `C:\Users\bymyw\.openclaw\workspace\state\DELETE_APPROVED`（教練已同意才建）。

### 📋 下一場先做
1. 簡報 BNI版三份：底部字幕被左下 LOGO 蓋住，教練還沒決定「照現狀」或「有字幕頁內縮排版」（v262 遺留）。
2. 官方 RustDesk 中繼 21117 修好後驗證。
3. 宏碁↔聯想 RustDesk 直連教練是否實測過，尚無回報；不要主動追問，教練提起再處理。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 14:03 台灣時間，Mac 桌面版 Opus 5.5↔Sonnet 5.5，v271）

**主軸：Mac 本機瘦身（刪約 28GB、下載與 Chrome 資料改放外接 SSD）；全隊體檢修 3 件；南應校友回憶牆改成「投稿→群組審核→公開」。**

### 做了什麼
1. **本機瘦身**（記憶 `reference_mac_downloads_on_external_ssd_2026-10-02.md`）：刪舊 Claude-3p 10GB、ByeType 4.6GB、whisper large/medium＋uv/puppeteer/opencode 快取約 7GB、9/19 工作資料夾舊備份 6.7GB（皆先比對 SSD 副本差異 0）。`~/Downloads` 與 `~/Library/Application Support/Google/Chrome` 改成捷徑指向 `/Volumes/953-SSD/下載`、`/Volumes/953-SSD/Mac應用資料/Chrome`；舊夾改名保留到 **10/09**。**不能刪**：`~/.cache/whisper/base.pt`（小龍蝦語音）、`~/.cache/huggingface`（名片 OCR／記憶搜尋），已加反射 `R-KEEP-VOICE-OCR-MODELS`。每日點名加「外接SSD」檢查。
2. **全隊體檢**：①小龍蝦 `character-illustration-batch` 技能檔頭被 9/28 塞壞、4 天被略過→已修；②kong/peipei/yijing 夥伴備份庫改每天點名時自動推（`scripts/backup_partner_agents.sh`）；③鎖死分身（yang/yijing）的每週技能整理被擋不再報黃燈。yijing 加進外層 .gitignore。
3. **系統更新提醒**：cron「教練-系統更新提醒-10-03凌晨」10/3 00:30 Telegram 私訊教練（已演練送達）。
4. **南應校友回憶牆**（event.bymyway.com/curated/tut-memory/）：投稿＋照片存伺服器 `event-signup/memwall_uploads/`＋表 `memwall_notes`；審核通知送「活動報名即時通知」群（-5349981085，佩佩老師可審），簽章連結 `/memwall/review/<id>?t=` 按通過才公開；時光走廊 5 張校史圖可點放大；與召集令（/tut/）互相連結；「立即加入校友會」改開召集令真報名表。commit：event-signup `d9ca95060`、`825b9871a`；tut-alumni `085d738`；回憶牆原檔備份 `~/github_repos/_backups/`（tut-memory 資料夾不是 git）。

### 卡在哪／發現
- 審核通知改送群組後，**群組那一步還沒真實走過**（怕測試訊息吵到佩佩老師，只驗了 bot 是群管理員、sendPhoto 本機成功）。第一則真實投稿時確認群組收到。
- 回憶牆「四場線上講座」報名仍是假的（只存瀏覽器）。教練 14:01 說四場主題可能會改，**改時他會通知**，屆時再接活動報名系統，不要主動問。
- 本機剩餘空間：刪完顯示仍約 43GB，因時光機本機快照未到期，約一天後會多出約 20GB。

### 📋 下一場開工先做
⓪ **10/03 00:30 教練要裝 macOS 26.7.1 小更新**（見下方那一棒 v270 的 ⓪ 條：回「更新」→ 先 `tmutil startbackup` 確認備份→ `softwareupdate -i "macOS Tahoe 26.7.1-25G241" -R`→ 重開後驗小龍蝦／赫米斯／Tailscale／RustDesk／SSD）。27.0.1 大改版不裝。
① 10/03 早上量本機剩餘空間（`diskutil info / | grep "Container Free"`）。
② 回憶牆第一則真實投稿進來時，確認「活動報名即時通知」群有收到照片＋審核連結。
③ 10/09 後刪 `~/Downloads.bak.20261002`、`~/Library/Application Support/Google/Chrome.bak.20261002`（先確認 Chrome／下載正常）。
④ v270 原有三項仍有效：楊老師 12:00 提醒（已 delivered ✅）、10/03 08:10 點名要有「💾 備份…已自動備份一次」、下次大樹作品上傳看「🗜 壓縮」。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 11:45 台灣時間，Mac 桌面版 Sonnet 5.5→Opus 5.5，v270）

**主軸：大樹作品 SOP 加三條新規則；Mac 備份從「每小時」改成「好的時候才備份」四條；教練兩次糾正「叫我自己找畫面」「密碼欄看不到」，都改成機制。**

### 做了什麼
1. 開工驗收：聯想（`bee1a7653`）、宏碁（09:15）條件反射回信都驗過並歸檔（`80f31b5b0`、`ddf32614f`）；真實 LINE 流量仍無。
2. ema1017 頁（教練交辦）：大標去逗號、70→50 人、加「席次有限，美味無限」＋台灣日期倒數（10/02 顯示 15 天）；圖片 13.2MB→1.1MB（webp，PSNR 45~48dB）。這資料夾不是 git，原檔備份在 scratchpad（會清掉）。
3. 大樹作品 SOP 三條（`fae7d44e4`，寫在 SOP 第 11 行起）：①上傳自動壓縮 `scripts/optimize_site_assets.py` 已接進 `curation_process.py` kind=creation（失敗照原檔上架，通知多一行🗜）②短網址：教練指定就用；沒指定提三個 10 字內＋第四「自己指定」③教練是講師＋有報名→`events.site` 改 `bigtree` 就列入大樹小講（讀碼確認 read_sessions 只看 site）；沒名字先不列，教練說一聲再改。
4. Amber 剩 8% 警告→Time Machine 改四條（`8831c072c`、`ab09e7892`）：教練自己改成手動；①08:10 點名無🔴才 `tmutil startbackup`（`daily_team_rollcall.py backup_when_healthy`，launchd 環境實測 exit 0）②反射 `R-BACKUP-BEFORE-UPGRADE`：升級前 6 小時內沒備份就擋（14 例全對，回測 11/39091 全是真升級）③QuotaGB=150 ④排除 `.cache/.npm/.rustup` 約 13GB（`.nvm` 刻意保留）。刪 3 天前 12 份：35→23，映像內 142→119GiB。
5. 機制修正：`stop_rules_master.py` A2b（回覆出現「設定→A→B」兩段箭頭又沒寫「已幫您打開」就擋，回測 6/2461 全真）；要密碼一律用 `scripts/coach_password_dialog.sh`（`sudo -A`，跳畫面最前面，教練實測看得到）＋反射 `R-SUDO-SHOW-TERMINAL`；`~/.claude/settings.json` PreToolUse 反射加接 run_in_terminal（備份 `.bak_20261002_terminal_reflex`）。記憶 2 筆。

### 卡在哪／發現
- App 終端機面板（run_in_terminal＋show_pane）教練兩次都看不到；osascript「管理員權限」視窗會失去完整磁碟取用，tmutil 看不到備份。兩個螢幕本來就是鏡像，不是螢幕問題。
- 備份只佔 Amber 約三分之一（其他約 270GB 是影片照片，用 09:14「剩 8%」推算）；Amber 本身空間有沒有回升還沒確認。
- 自動壓縮只測過函式＋ema1017 正式資料夾，還沒經真實上傳流程跑過一次。

### 📋 下一場開工先做
⓪ **10/03 00:30 教練要裝 macOS 26.7.1 小更新**（cron「教練-系統更新提醒-10-03凌晨」會 Telegram 提醒他）。教練回「更新」→ 先 `tmutil startbackup` 備份並確認完成 → `softwareupdate -i "macOS Tahoe 26.7.1-25G241" -R`（要密碼走 coach_password_dialog.sh）→ 重開後驗小龍蝦／赫米斯／Tailscale／RustDesk／外接SSD(Chrome、下載是捷徑)。27.0.1 大改版不裝，等一兩週。教練回「改天」就記下。另：10/09 後刪 `~/Downloads.bak.20261002`、`~/Library/Application Support/Google/Chrome.bak.20261002`；10/03 早上量本機剩餘空間(時光機快照到期後應多約 20GB)。
① 查 12:00 楊老師（Simona）課程提醒：`openclaw cron list --json` 看 `4c706494` 是否 delivered；② 10/03 08:10 點名訊息要有「💾 備份：全員正常，已自動備份一次」，且 `tmutil listbackups | wc -l` 多一份；③ 下次有大樹作品上傳，看通知有沒有「🗜 壓縮」一行、圖片是 webp。三項都正常就問教練今天從哪件事開始。

---


> 📦 v268（Mac 10-02 03:46，賈維斯成長計畫第三步：禮遇版人設、聯想／宏碁接反射、網址手滑校正外掛）完整內容已封存：`handoff_archive/handoff_v268_archived_2026-10-02.md`

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

✅ 開工已改成「心法＋最新一棒」（10-02 14:2x，注入 30KB→9.7KB，全域與 workspace CLAUDE.md 開工鐵律同步改 v3）；之後：Stop hook 只留行為檢查、拿掉字眼檢查。待查：`handoff_sync_guard.sh` 判斷1 用 PreToolUse＋stderr＋exit 0 提醒，AI 可能看不到。量尺：教練訊息「重講」比例 5月19%／6月13%／7月14%／8月12%／9月16%，重跑 `python3 scripts/render_top30_report.py` 看 10 月有沒有降。

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
| 🟡 | **Mac 備份改四條（10-02 教練定，取代每小時）＋Amber 空間** | ✅四條都上線；⏳明早 08:10 首次點名備份待看 | 【10-02 11:40 完成】上限 QuotaGB=150 已生效；刪 3 天前 12 份（35→23，留 09-29 23:40 起），備份映像內用量 142→119GiB。密碼改用 `scripts/coach_password_dialog.sh`（sudo -A，教練看得到）。Amber 本身空間有沒有回升，下次看 Amber 通知（AI 分類 >15% 才恢復）。以下為原規劃：①點名正常才備份 `daily_team_rollcall.py backup_when_healthy`（launchd 環境實測 startbackup exit=0）②升級前必備份 反射 `R-BACKUP-BEFORE-UPGRADE`（14 例全對、回測 11/39091 全是真升級）③上限 150GB＋刪 3 天前 12 份：App 終端機分頁「備份設定：只差輸入密碼」跑 `scratchpad/tm_setup.sh`，教練輸入密碼後看 `tmutil listbackups|wc -l`（應 34→22 左右）與 `defaults read /Library/Preferences/com.apple.TimeMachine` 有無 Quota；scratchpad 會清掉，腳本要留就搬進 scripts/ ④排除 `.cache/.npm/.rustup`（約13GB，`.nvm` 刻意保留）。**明早 08:10 首次點名要看到「💾 備份：全員正常，已自動備份一次」**。教練頻率已自己改手動（AutoBackup=0）。記憶 `project_mac_backup_policy_good_state_and_pre_upgrade_2026-10-02.md`。 |
| 🟢 | `reflex_coverage.py` 記憶索引斷鏈 2 筆（聯想 bee1a7653 合併索引帶進來的 `feedback_single_html_work_download_images_and_zip_myself_2026-10-02`、`reference_rustdesk_direct_ip_over_tailscale_2026-10-01`，Mac 沒有這兩個檔） | ⏳待處理-低優先 | 從聯想 claude-brain 取回檔案或改索引；補進 memory_ledger。 |
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
