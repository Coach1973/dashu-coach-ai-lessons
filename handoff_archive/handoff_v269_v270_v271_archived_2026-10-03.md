# 封存：v269／v271／v270 三棒（2026-10-03 收工時由 v273 搬出）

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
3. **南應校友回憶牆**（event.bymyway.com/curated/tut-memory/）：投稿＋照片存伺服器 `event-signup/memwall_uploads/`＋表 `memwall_notes`；審核通知送「活動報名即時通知」群（-5349981085，佩佩老師可審），簽章連結 `/memwall/review/<id>?t=` 按通過才公開；時光走廊 5 張校史圖可點放大；與召集令（/tut/）互相連結；「立即加入校友會」改開召集令真報名表。commit：event-signup `d9ca95060`、`825b9871a`；tut-alumni `085d738`；回憶牆原檔備份 `~/github_repos/_backups/`（tut-memory 資料夾不是 git）。

### 卡在哪／發現
- 審核通知改送群組後，**群組那一步還沒真實走過**（怕測試訊息吵到佩佩老師，只驗了 bot 是群管理員、sendPhoto 本機成功）。第一則真實投稿時確認群組收到。
- 回憶牆「四場線上講座」報名仍是假的（只存瀏覽器）。教練 14:01 說四場主題可能會改，**改時他會通知**，屆時再接活動報名系統，不要主動問。
- 本機剩餘空間：刪完顯示仍約 43GB，因時光機本機快照未到期，約一天後會多出約 20GB。

### 📋 下一場開工先做
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
① 查 12:00 楊老師（Simona）課程提醒：`openclaw cron list --json` 看 `4c706494` 是否 delivered；② 10/03 08:10 點名訊息要有「💾 備份：全員正常，已自動備份一次」，且 `tmutil listbackups | wc -l` 多一份；③ 下次有大樹作品上傳，看通知有沒有「🗜 壓縮」一行、圖片是 webp。三項都正常就問教練今天從哪件事開始。

---


> 📦 v268（Mac 10-02 03:46，賈維斯成長計畫第三步：禮遇版人設、聯想／宏碁接反射、網址手滑校正外掛）完整內容已封存：`handoff_archive/handoff_v268_archived_2026-10-02.md`

---

> 📦 v265（Mac 10-02 02:40，試金石 95 案全部轉成反射＋教練定名「賈維斯成長計畫」）完整內容已封存：`handoff_archive/handoff_v265_archived_2026-10-02.md`

---

> 📦 v263 聯想棒（RustDesk 改 Tailscale IP 直連＋大樹作品單檔 HTML ema1017）完整內容已封存：`handoff_archive/handoff_v263_lenovo_archived_2026-10-02.md`；未結事項已移入下方「🤫等教練自己提起」與「🔧AI自己的工作清單」

---

