## 🔴 給跨對話框軍師讀的總結摘要（2026-10-10 04:45 台灣時間，Mac 桌面版 Code 分頁，Sonnet 5.5⇄Opus 5.5（教練用 /model 切換），v296，教練說「總結」收工；對話 10/10 02:36～04:45）

**主軸：教練追問「為什麼忘記 GitHub」→ 查原話、根因修復、51 站全補；南應大記憶牆大改；信任遊戲加入座／新座位／刪除玩家／邀請朋友。**

### 1. 策展站 GitHub 化（教練 09-30 原話：上架大樹作品SOP／策展SOP時同時建一份 GitHub；10-10 教練說「是我們的問題，光明正大承認」）
- **根因**：09-30 命令只落成工具 `curated_git.py`＋接力棒🔧一列；大樹作品 SOP 與 `publish_creation()` 還寫「不做：建GitHub」，AI 照 SOP 做＝違令；開工不唸🔧區，擱 10 天，51 站有 20 站沒 repo。SOP 與教練的話衝突時**以教練的話為準，且要當場提出**。
- **修法**：`publish_creation()` 上架自動 `ensure`（建私有 repo＋掛通知）、SOP 改字、每晚 00:40 launchd `ai.openclaw.curated-github-ensure`、**GitHub 推送自動換新**＝event-signup `/hooks/github-site`（HMAC，`GITHUB_WEBHOOK_SECRET` 在 .env，只服務策展名單）；模擬聯想推送 4 秒換新。**51/51 站有 GitHub＋通知**（10 站被 GitHub 限速，03:43 第 3 次重試補完）。commit `b213b9a79`、`25fae3865`、`f5fea0159`、`d1b5f147b`；試金石案例113 `3c700c604`；記憶 `feedback_event_sites_must_have_github_wired_into_pipeline_2026-10-10`。
- **範圍被教練糾正**：只管大樹作品＋策展 SOP，**不碰 bni-traffic、bigtree 等早期舊站**；我誤掛的 19 個舊站通知已拆掉。

### 2. 111-wei（蔡筱薇競選頁）：頁尾「本網頁由 TAVA AI 製作，由南應校友陳佩君贈送給學姊蔡筱薇」＋佩君 LINE@（`@701ohlly`）按鈕；集氣區加「聯絡召集人陳佩君」。GitHub `Coach1973/111-wei`。

### 3. 南應大記憶牆 tut-memory（網址不變，GitHub `fa1ff54`）
拿掉十景投票；講座改「票選最想聽的主題」（不壓日期、可送建議）；專屬商務團隊資源點開 17 位夥伴（`BIZ_TEAM` 陣列）；外部產業資源點開 6 個連結（`EXT_LINKS`）；終身校友網絡連召集令；「支持陳佩君競選理事長」按讚（不記 IP、不限次數）；候選人橫幅（34px＋邊框燈泡＋字幕跑馬燈，文字「…陳佩君競選理念」）。後端新接口 `/api/works/poll/<site>`（票選＋建議，建議通知進活動報名群）、`/api/works/counter/<site>/<key>`，workspace `601906dbb`、`3a571abed`。

### 4. 信任遊戲 bni-chapters（`7c2f5cb`、`793b480`、`a415cbf`、`bbd628f`，測試184項）
座位地圖加真公益；無清單團隊「我要入座」、有清單「我要新座位」；已成立（active）團隊連到團隊頁；玩家可用專用修改連結自刪名片；座位後台加「玩家管理」；`game_delete_player.py`（手機版 Claude 刪人，只標記可還原）；新手說明書「邀請朋友一起玩」改接信任邀請函。另一個對話窗也在改這個專案（已改名「團隊」「珍貴席次」），只動需要的檔。備份 `trust_game.db.bak-before-sit-delete-20261010`。

### 5. 教練最後交代：**新做的後台系統要自己登記進「我的大樹作品」(coach888)**，他不記。已把「信任遊戲座位後台」放進 coach888「活動後台」第 7 項（伺服器狀態，備份 `state/coach888_state_backup_20261010_before_trust_admin.json`）；教練再說「做了後台沒自動收錄是 bug」→ 已做 `scripts/coach888_register_admin.py`（一行登記、可重複、先備份）＋**執行細則 N10**（已同步全域 CLAUDE.md）＋反射 `R-NEW-ADMIN-URL-REGISTER-COACH888`＋SOP／bni-chapters CLAUDE.md；試金石案例114。

### 📋 下一場開工先做
**目前沒有教練交辦未完成。** 開工回報 5 行內，問「今天要從哪件事開始？」。
🔧AI 自己的（不問）：①聯想／宏碁開工腳本加「貼 event 網址→指路對應 GitHub」（`feed_junshi_handoff.ps1`，未做）；②**新做任何後台／管理／編輯／刪除網址，當場跑 `coach888_register_admin.py`（N10）**；③教練丟簡報套 BNI 底圖走 `pdf_to_branded_pptx.py`、交付檔案用 `deliver_open.sh`；④教練短問句「要不要改 X」＝交辦。
🤫等教練自己提起：tut-memory 第 1 個講座《記憶開箱：南應十景票選 LIVE》題目提到已拿掉的十景票選；首頁「1,268 位校友／842 則回憶」是寫死的預設數字；教練哪天填一筆 hnv-cc 表單測通知後要清 `works_contact_leads` 測試筆。
**commit**：workspace `d1b5f147b`、`051a59aba`；bni-chapters `bbd628f`；tut-memory `fa1ff54`；111-wei GitHub 已建。

---

