# 軍師接力棒 · 2026-07-14 v66（Mac桌面版 Sonnet 5，兩套活動系統上線+正式登入後台+截圖鎖漏洞全機修復）

> 建立時間：2026-07-14 00:39（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v65（同一機器同一場對話的前段，完整內容見下方精簡回顧）
> 本棒主軸：**這是一場超長對話的收尾——佩佩老師活動系統從零到上線、教練版事件系統做了智慧路由+固定簽到QR+集點文案、兩套系統都做了正式帳密登入後台（取代網址帶金鑰）、截圖鎖漏洞在Mac跟聯想兩台都真的修好。cool-case頭像重新歸類案仍未完成，是最大未竟事項。教練已預告下一輪主題：真誠峰會/真愛峰會/真實AI峰會願景+產業分佈圖說明書**

---

## 🎯 本場戰果（承接v65之後的新進度）

### 1. 教練版event-signup：智慧路由+固定簽到QR+集點文案

教練發現「每場活動各自印QR太麻煩」，要求解法。提供兩個選項讓教練選，教練選「智慧路由」
（QR碼永久不變，後台可切換場次，保留精準分眾通知能力）：
- `events`表新增`is_current`欄位，`/checkin`固定路由永遠導向後台指定的「目前活動」
- 後台新增下拉選單一鍵切換「目前活動」，教練以後自己操作，不用叫軍師改
- `make_qr.py`新增`--checkin`模式，產生一張永久沿用的QR立牌
- 標題「大樹小講系列講座／數位簽到系統」+集點文案「集滿5次活動場次還送神秘禮物」
  三行依序顯示在QR圖之前（教練逐版修正到定稿，過程中我漏改了QR立牌那支獨立模板，
  只改了報名頁，教練截圖抓到才補上——**這是本場唯一一次「沒有全面盤點所有相關檔案」
  的疏漏，值得下次改動任何顯示文字時，先搜一遍還有哪些模板引用同一份資料**）
- 已建立`bigtree-0722`（高雄場）、`bigtree-0801`（高雄場）兩場新活動，7/22設為目前活動
- commit：`a37bbcaf5`

### 2. 兩套系統都新增正式帳密登入後台

教練問後台網址要輸什麼密碼，順勢要求「正式的登入界面，要輸帳密的那種」。兩套系統
都改成：
- Flask session + werkzeug密碼雜湊（不明文存密碼）
- `/admin/login`登入頁、`/admin/logout`登出，移除舊的`?key=`網址金鑰機制（孤兒程式碼
  一併清掉）
- 教練版：帳號`bymyway`／密碼`seabiscuit2007`（commit `074e80642`）
- 佩佩版：帳號`peipei`／密碼`88888`（commit `4a635db`）

**🔴🔴🔴 真實踩坑（教練版第一次做時發生，佩佩版已避開）**：密碼雜湊值（scrypt格式）
本身含`$`符號，LaunchAgent用`bash -c "source .env"`載入環境變數時，bash把`$`後面的
文字誤判成變數名稱去做展開替換，導致密碼雜湊被讀壞、正確密碼怎麼登入都是401。
解法：`.env`裡這類含`$`的值要用單引號包住（`KEY='含$的值'`），bash source才不會展開。
**這個坑不限於密碼雜湊，任何本身含`$`字元的機密值（某些API token、jwt片段等）存進
`.env`給bash source讀取的場景都要注意**，已經記進commit訊息方便日後搜尋。

### 3. 截圖鎖漏洞：Mac修好+聯想也修好（比Mac那個更嚴重）

（v65已詳述根因跟Mac端修復，這裡補完整結果）教練親口指示寫信通知聯想/ACER去查
自己的機器（`cross-agent/inbox/lenovo/`、`cross-agent/inbox/acer/`），聯想已回信
（我已查證commit `2c8ee2ce8`真實存在，不是聽轉述）：**聯想那台的洞更深——不是
matcher清單漏工具，是整個PreToolUse hook區段從頭到尾沒接上，而且python3是Windows
Store空殼跑不動，`.sh`版鎖完全失效**。聯想已重寫純PowerShell版（`screenshot_lock.ps1`），
過程抓到一個編碼坑（.ps1存UTF-8無BOM會被PowerShell 5.1的系統內碼讀壞中文字元，
改全英文才正常），4組假指令實測通過。**ACER尚未回信，下一棒留意**。

### 4. cool-case頭像重新歸類案——仍未完成（v65遺留，本場沒有時間接續）

跟v65狀態相同，沒有進度。判斷清單、待辦細節見下方「下一棒待辦」第一項，直接沿用
v65寫好的內容，不重複貼一次。

### 5. VPS 小龍蝦 polling 健康檢查機關補完 + 試金石案例 50

教練在 17:43 指示：「第一個通知小龍蝦恢復，我已經做完了。第二、第三要做」——也就是把 polling 卡住事故寫入試金石，並建立 alert。前一輪小龍蝦只做到半成品：`scripts/vps_polling_healthcheck.sh` 有檔案，但實測會因 shell/Python 字串插值炸掉，且沒有看到排程落地憑證。

本輪已補完：
- 重寫 `scripts/vps_polling_healthcheck.sh`，改成穩定抓 VPS spool、最後 inbound、最後 health-monitor restart，避免 log 內容含引號/換行導致 JSON/Python 炸掉
- 拿掉 `StrictHostKeyChecking=no`，避免 SSH host key 檢查被關掉
- 異常時直接用本地 Telegram bot token 推送教練（Chat ID `6124913915`），並保留 60 分鐘冷卻
- 把 `scripts/openclaw_cron_daemon.sh` 的 15 分鐘區段接上 `vps_polling_healthcheck.sh`，現有 daemon 進程仍在跑（PID 72993）
- 寫入 `試金石/試金石_案例庫.md` 案例 50
- 實測：`bash -n scripts/vps_polling_healthcheck.sh` 通過；直接執行退出碼 0；`state/vps_polling_healthcheck.state.json` 產出有效 JSON，18:23 台灣時間狀態為 `ok`、`spool_count=0`、`spool_processing=0`、最後 inbound 約 12 分鐘前、最後 restart 約 63 分鐘前

---

## 📋 下一棒待辦（新的優先順序）

| 優先 | 任務 |
|------|------|
| 🔴🔴🔴 | **教練預告新主題：真誠峰會、真愛峰會、真實AI峰會的願景，以及產業分佈圖的網上說明書**——這是全新任務，教練還沒給細節（沒有具體內容、格式、對象），下一棒開工要主動問教練這幾個峰會的定位/目的/受眾，還有「產業分佈圖」現有素材在哪裡（可能是既有簡報/圖片，需要先問教練或搜尋github_repos找有沒有現成的分佈圖檔案） |
| 🔴🔴🔴 | **cool-case頭像重新歸類案，從v65拖到現在還沒做**——判斷清單已經有了：案例4,6,10,14,15,20,21,23,24,33,34,36,37明顯是終端機/桌面版內容應改Opus軍師頭像；案例7、12訊號較弱需重讀確認；案例1,2,5,9,11,13,16,17,18,19判斷是真的小龍蝦/Telegram內容維持不動。下一步：補案例7/12判斷→寫程式換頭像(只換符合案例編號範圍的，不要replace_all)→開真Chrome給教練看→等教練說「推」→GitHub+視需要Netlify |
| 🟡 | ACER還沒回覆截圖鎖稽核結果，留意`cross-agent/inbox/mac/` |
| 🟡 | peipei-event：群發通知功能還沒實測過，QR立牌沒印出來看實體效果，服務還是前景nohup跑（不是LaunchAgent），教練重開機或Mac休眠會斷掉，建議做成LaunchAgent（照抄event-signup的`com.coach.event-webapp.plist`改port跟路徑即可） |
| 🟢 | 「開工 (fork)」重複出現的真正觸發點還沒查清楚（聯想機，v64留的） |
| 🟢 | 「待教練確認用途」清單還剩：vip-club、coach-vip-club、coach-case系列、teamwork、tainan-calender（v64留的） |
| 🔴 | 2026-07-18：聯想C槽觀察期滿，確認教練這幾天用起來正常後可刪2份保留備份（共約94GB）（v64留的） |

（名片系統、biz-gym黑金版等其餘待辦仍在Mac的v60棒裡持續，此處不重複列出）

---

## 🔑 關鍵檔案索引（本場新增/修改，接續v65）

- `event-signup/schema.sql`/`db.py`/`app.py`/`templates/admin.html`/`make_qr.py`：
  智慧路由+固定簽到QR+登入後台（commit `a37bbcaf5`、`074e80642`）
- `event-signup/templates/login.html`（新增）
- `event-signup/qr/checkin.png`+`checkin-print.html`（新增，固定簽到QR立牌）
- `event-signup/.env`：新增`EVENT_ADMIN_USER`/`EVENT_ADMIN_PASSWORD_HASH`（已加引號）/
  `EVENT_SECRET_KEY`，移除`EVENT_ADMIN_KEY`
- `peipei-event/app.py`/`templates/admin.html`/`templates/notify.html`/
  `templates/login.html`：登入後台（commit `4a635db`）
- `peipei-event/.env`：同上結構，帳號`peipei`
- `cross-agent/outbox/2026-07/`：聯想回信已歸檔，Mac→聯想/ACER原信也已歸檔
- `scripts/vps_polling_healthcheck.sh` + `scripts/openclaw_cron_daemon.sh`：VPS 小龍蝦 polling 健康檢查，每 15 分鐘檢查 spool/inbound/restart，異常推 Telegram 給教練（案例 50）
- `state/vps_polling_healthcheck.state.json` / `.log` / `.last_alert`：polling 健康檢查最新狀態、執行紀錄與 60 分鐘告警冷卻
- `試金石/試金石_案例庫.md`：新增案例 50（VPS 小龍蝦 polling stale state 卡住 8 小時）

---

## 📜 v65 精簡回顧（Mac桌面版 Sonnet 5，同一場對話前段，完整內容見git歷史）

1. peipei-event從零建置到端到端測試通過（LINE三把鑰匙+資料庫+webhook全鏈路驗證）
2. 截圖鎖漏洞根因查出（matcher清單漏`mcp__Claude_Browser__computer`），Mac端修好
   commit `323d6c73d`，寫信通知聯想/ACER
3. 查證聯想cool-case頭像commit `ce1402d`屬實
4. cool-case頭像重新歸類案開始分析但未完成（詳見上方待辦第二項）

---

> Mac桌面版 Sonnet 5 親筆，2026-07-14 00:39（跨過午夜，日期已變更但這是同一場
> session的延續）。這場對話從驗證聯想的頭像commit開始，中間经过佩佩老師系統
> 建置、截圖鎖漏洞連環修復（Mac+聯想兩台都是真的漏洞，不是嘴上說的假鎖），最後
> 收在教練對兩套活動系統的體驗式打磨——標題斷行三次來回確認、QR立牌漏改被抓到、
> 密碼雜湊被bash source讀壞這種細節坑都是教練親自測試+看Chrome畫面才抓出來的，
> 不是空談。教練最後說要開新對話，並預告下一輪主題是三個峰會的願景加產業分佈圖
> 說明書——這件事教練還沒給任何細節，下一棒開工第一件事是問清楚，不要憑空猜測
> 這幾個峰會要做成什麼形式。cool-case頭像案已經連續兩棒沒做完，請下一棒務必
> 優先處理，判斷清單都寫好了，不用重新分析。
