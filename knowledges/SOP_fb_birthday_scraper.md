# FB 生日抓取 SOP（標準作業程序）

> 教練親定 2026-04-12 商業決策（半自動路線），SOP 整理 2026-06-07，所有 AI 助教（終端機/桌面版/小龍蝦/Hermes）強制遵守。
> 原始決策文件：`.lessons_upload/memory/feedback_fb_birthday_automation_cost.md`

---

## 🎯 一句話總覽

> **每天早上 6 點，無頭瀏覽器自動登入教練的 FB，抓「今日壽星」名單，整理好發給教練，教練手動發祝福。整個抓取過程 0 Token。**

---

## 🔴 為什麼是「半自動」而不是全自動？（教練親定決策）

| 路線 | 成本 | 優點 | 缺點 |
|------|------|------|------|
| **傳統爬蟲**（目前採用） | **0 Token** | 速度極快、成本為零 | 脆弱：FB 改版 class 名稱就壞 |
| LLM 視覺代理 | 單次數萬 Token | 抗改版能力強 | 燒 Token 太兇，客戶錢包會哭 |

**教練 2026-04-12 拍板結論**：
- 先封存全自動版，**用半自動保護客戶錢包**
- 等未來 AI 算力降價再考慮升級視覺代理
- 採用「腳本抓名單 + 教練手動發送」的半自動模式

---

## ⏰ 排程設定

| 項目 | 設定值 |
|------|--------|
| 執行時間 | 每天 06:00（Asia/Taipei） |
| 觸發工具 | OpenClaw cron（已從系統 crontab 改用） |
| Cron Job ID | `12fad20b-9ee5-470d-aeb7-3666f08857ff` |
| Cron 任務名 | `FB 每日生日祝福` |
| 備註 | `【0 Token 半自動排程】` |

---

## 📋 執行流程（5 步驟）

### Step 1｜Cron 觸發
- 早上 6:00 自動觸發，不需要人手介入
- Cron 訊息內含固定指示詞：`【0 Token 半自動排程】`，提醒接收方走腳本不走 Browser Control

### Step 2｜跑腳本

```bash
node /Users/bymyway/.openclaw/workspace/scripts/fb_birthday_scraper.js
```

腳本內部邏輯（**2026-10-31 改版**）：
1. 從教練自己的 Chrome（`~/Library/Application Support/Google/Chrome`）複製 cookie 檔到工作 profile
   → 教練平常在 Chrome 登 FB，cookie 自動跟著走，不用手動同步
2. 用 `open -na "Google Chrome" --args --user-data-dir=... --remote-debugging-port=9225 --headless=new` 啟動 Chrome
   → **關鍵**：走 LaunchServices 讓 macOS 歸屬 responsible app，鑰匙圈才會放行 cookie
   → `--headless=new` → 教練螢幕不會跳出任何視窗
3. `puppeteer.connect({browserURL:'http://localhost:9225'})` 接上已開好的 Chrome
4. 前往 `https://www.facebook.com/friends/birthdays/`
5. 等 `networkidle2` + 多等 6 秒
6. 抓頁面上所有 `<h2>` 標籤
7. 找到「**今日壽星**」這個 h2（注意：「新朋友」h2 會出現在它之前，不能看到就 break）
8. 抓它下面到「剛過生日 / 即將過生日」出現之前的全部名字
9. 關閉 CDP port 上的 Chrome 實例（只關自己開的那個，不動教練的 Chrome）

### Step 3｜三種結果分支

| 狀況 | 怎麼判斷 | 顯示什麼 | 後續動作 |
|------|---------|---------|---------|
| ✅ 有壽星 | 抓到「今日壽星」h2 且下面有人名 | 列出編號 + 名字，提示「請教練直接複製名單進行半自動發送」 | 推 Telegram 給教練 |
| ✅ 沒壽星 | 抓到「今日壽星」h2 但下面 0 人 | 顯示「今天沒有 FB 壽星」 | **安靜不通知**（依安靜完成協議） |
| ⚠️ 沒抓到 h2 | 頁面完全沒 h2 | 視為 **FB 改版**，報錯並貼出頁面前 500 字 | 推 Telegram 報錯，請工程師修腳本 |
| ⚠️ Session 過期 | 網址被導去 `/login` 或 `index.php?next=` | 報錯 `process.exit(2)`，請教練先登入一次 FB | 推 Telegram 通知教練 |

### Step 4｜整理後發給教練
- 自動去重（同一人重複出現只算一次）
- 早上 6 點直接推到 Telegram 給教練
- 沒壽星的日子 **安靜不通知**

### Step 5｜教練手動發送
- 腳本只負責「抓名單」
- **發祝福由教練本人到 FB 手動送**（避免被 FB 判定為機器人活動）

---

## 📂 相關檔案清單

| 檔案 | 用途 |
|------|------|
| `scripts/fb_birthday_scraper.js` | 主腳本（Puppeteer 無頭瀏覽器） |
| `scripts/fb_birthday_verify.js` | **獨立驗證腳本（2026-11-04 新增）**：自己同步 cookie、自己啟 Chrome、自己關；用「今日壽星 h2 → 往上找區塊容器 → 容器內 h2 + 容器文字 + profile 連結」三路徑交叉比對主腳本結果。抓不到會印出頁面所有 h2 與容器文字 1200 字，FB 改版時直接看得到長什麼樣 |
| `scripts/fb_session_data/` | 教練 FB 登入 cookie 存放處（首次需手動登入一次）。⚠️ 2026-10-03 起這份已搬到 953-SSD 外接碟，**launchd 背景執行會失敗**，腳本已改用 `/Users/bymyway/.openclaw/fb_session_data_local`（本機碟） |
| `~/Library/Application Support/Google/Chrome.ssd-link` | 2026-11-06 保留的**懸空 SSD 連結**（原 `Chrome` 指向 `/Volumes/953-SSD/Mac應用資料/Chrome`，SSD 沒接上時 Chrome 會崩潰）。`Chrome` 本身已改回本機真實目錄，SSD 接上後若要搬回去，用這個連結比對即可 |
| `/Users/bymyway/.openclaw/fb_session_data_local/` | **現行實際使用的 Chrome profile（本機碟）**。外部磁碟版保留備用，不要刪 |
| `.lessons_upload/memory/feedback_fb_birthday_automation_cost.md` | 商業決策文件（2026-04-12 教練拍板） |
| `.memsearch/memory/2026-06-01.md` | 排程確認紀錄（FB 生日每日爬蟲：✅ 明天 06:00 準時執行） |

---

## 🛠️ 故障排除速查

| 問題 | 解法 |
|------|------|
| 顯示「FB session 已過期」 | 用本機 Chrome 登入一次 FB，cookie 會自動同步到 `fb_session_data` |
| 顯示「找不到任何 h2」 | FB 改版了，需要更新腳本裡的選擇器（請工程師修 `fb_birthday_scraper.js`） |
| 完全沒跑 | 檢查 OpenClaw cron 狀態（`cron list` 確認 `12fad20b` 還在） |
| 跑很久沒回應 | Puppeteer 等 `networkidle2` + 多等 4 秒，網路慢就會慢（屬正常現象） |
| 重複抓到同名壽星 | 已是已知行為，Step 4 會自動去重（不必改腳本） |
| 🔴 想知道名單抓對沒 | 跑 `node scripts/fb_birthday_verify.js` 交叉比對。**2026-11-04 起有這支獨立驗證腳本**，主腳本壞掉或 FB 改版時用它確認，不要只信主腳本一次輸出 |
| 🔴 2026-11-04 新坑：想抓「profile 連結文字」會抓到 0 筆 | **FB 目前 DOM 結構：壽星名字本身就是 `<h2>`（parent=A）**，不是 profile 連結的 innerText。驗證腳本第一版就是這樣寫的，結果抓到 0 筆誤判「抓不到」。**正確做法：抓 h2**（主腳本原本就是對的），或抓「今日壽星 h2 往上找的區塊容器的 innerText」 |
| 🔴 報「The browser is already running for ...fb_session_data」 | **Chrome profile 放在外部磁碟（USB SSD）時，launchd 背景執行沒有權限寫那個磁碟**，Chrome 建不了 SingletonLock 就會噴這句假錯誤。**解法：profile 必須放本機碟**。本機版在 `/Users/bymyway/.openclaw/fb_session_data_local`，腳本會優先用它、找不到才退回舊路徑。（2026-10-24 實例：`fb_session_data` 在 10/03 被搬到 953-SSD，結果連續 19 天每天 exit 1，教練完全沒收到壽星名單卻沒人發現） |
| 🔴 2026-11-06 新坑：Chrome 一開就崩 `Failed to get the path for 1001` | **症狀**：任何 Chrome 啟動（無頭、有頭都一樣）立刻崩潰，DiagnosticReports 產生 `EXC_BREAKPOINT / Trace-BPT trap: 5` crash 檔，stderr 印 `[FATAL:base/path_service.cc:264] Failed to get the path for 1001`。**根因**：教練的 Chrome 資料夾 `~/Library/Application Support/Google/Chrome` 是指向未掛載外接 SSD 的**懸空 symlink**（→ `/Volumes/953-SSD/Mac應用資料/Chrome`），SSD 沒接上時 Chrome 連預設資料夾都建不出來。**注意 1001 不是使用者 uid**（教練是 501），是 Chromium 內部的目錄編號，別誤判成權限問題。**解法**：把 SSD 連結改名保留（`Chrome.ssd-link`），再從本機備份 `Chrome.bak.20261002` 用 rsync 複製回本機真實目錄（跳過 `OptGuideOnDeviceModel` 等 4GB 可重新下載的 AI 模型目錄），並把 `Last Version` 寫成當前 Chrome 版本避免 cookie 被清。**修復後**：教練平常的 Chrome 也恢復正常開啟、FB cookie 1236 筆（`c_user`/`xs` 到 2027-10-02）、生日腳本抓出 8 位壽星。**對照實驗法**：暫時把懸空連結換成真實目錄 → Chrome 立刻能開 → 證實是資料夾問題不是 session 問題 |
| 🔴 2026-10-31 新坑：cookie 在但還是被導去登入頁 | **Puppeteer 直接 `puppeteer.launch()` 啟動的 Chrome，macOS 判定它「沒有 responsible app」，鑰匙圈 ACL 會拒絕 → cookie 解不出來 → 直接被丟掉（不是 session 過期）**。Chrome 自己的 stderr 會寫 `Failed to decrypt token for service ...`。**解法：改用 `open -na "Google Chrome" --args --user-data-dir=... --remote-debugging-port=9225 --headless=new`（LaunchServices 啟動）**，macOS 才會正確歸屬 responsible app、鑰匙圈才放行；再 `puppeteer.connect({browserURL})` 接上去。`--headless=new` 保證教練螢幕不會跳出視窗。**已驗證有效（2026-10-31 修好）** |
| 🔴 2026-11-01 新坑：Chrome 更新後工作 profile 的 cookie 變空殼 | **症狀一樣（被導去登入頁），但根因是「舊工作 profile 被 Chrome 判定版本不符 → 啟動時把 cookie 清掉」**。徵狀：工作 profile 的 `Cookies` 變成 32KB、sqlite 報 `no such table: cookies`（空殼），而教練真實 Chrome 的 `Cookies` 完整（1370 筆、FB 10 筆、`c_user`/`xs` 到 2027 年才過期）。**解法：每次同步前先 `pkill` + 刪掉工作 profile 的 `Cookies*`、`Network Persistent State*`、`Singleton*`，讓同步放進去的是完整快照；並在 Chrome 啟動後回報 cookie 存活筆數（啟動前 vs 啟動後）**。已驗證有效（2026-11-01 修好，commit `d69b3b600`） |

### 🔴 2026-10-31 事故紀錄（cookie 好好的一直在，卻抓不到）

| 日期 | 現象 |
|------|------|
| 2026-10-30 05:54 | Chrome 自動更新 156.0.8078.49 → **156.0.8078.79** |
| 10/30 起 | 腳本每天被導去登入頁。**教練自己 Chrome 的 cookie 一直有效**（`c_user`/`xs` 到 2027 年才過期），但工作 profile 的 cookie 被 Chrome 啟動時清掉 |
| 10/30 | 前一班 AI 診斷為「新版拿不到鑰匙圈授權，要教練手動重新登入 FB」——**診斷方向對，但開錯藥**（重新登入也沒用，因為不是 session 過期） |
| 2026-10-31 | 本人查出真正根因：**Puppeteer 直接啟動的 Chrome 沒有 responsible app → 鑰匙圈拒絕 → cookie 解不出來被丟棄**。改用 `open -na`（LaunchServices）+ `--headless=new` + CDP → **一次就通** |

**教訓**：
1. **「被導去登入頁」有兩種原因，症狀一樣、根因完全不同**：(a) session 真的過期 → 要人重登；(b) cookie 解不出來 → **人重登也沒用**，要改啟動方式。**先用 stderr 判斷**：`Failed to decrypt token` = (b)，沒有這行 = (a)。
2. **診斷要抓原始錯誤，不要只看症狀**。Chrome 的 `dumpio: true` stderr 才有真因。
3. **macOS 上「從程式啟動 App」≠「使用者啟動 App」**。任何需要鑰匙圈授權的 App（Chrome、密碼管理器、密鑰庫）都受影響，headless/背景執行特別容易踩。
4. **「壞掉時不要急著叫人來修」**——10/30 叫教練重新登入 FB 是白叫，因為重新登入解決不了 (b)。先自己找出 0 按鈕解法。

### 🔴 2026-11-01 事故紀錄（Chrome 更新後，cookie 變空殼）

| 日期 | 現象 |
|------|------|
| 2026-11-01 06:30 | cron 首次執行被導去 FB 登入頁，腳本 exit 2。**第一時間以為又是 session 過期** |
| 11/01 診斷 | **教練真實 Chrome 的 cookie 完全正常**：1370 筆、FB 相關 10 筆、`c_user`/`xs` 到 2027-10-24 才過期（`Local State` 顯示 profile = 大樹 / bymyway7@gmail.com）。**所以不是 session 過期** |
| 11/01 診斷 | 反過來查工作 profile `fb_session_data_local` → `Cookies` 只有 32KB，sqlite 直接報 `no such table: cookies`（空殼）；但 `hasSessionCookie()` 卻回「有」——因為它查的是「有沒有 `c_user`/`xs` 這兩個名稱」，空殼裡剛好有殘留 |
| 11/01 對照實驗 | 建乾淨 profile `fb_test_profile`，只複製真實 `Cookies` + `Cookies-journal` + `Local State` + Preferences → 啟動 Chrome 後 cookie **存活 1370 筆 / FB 10 筆** → 證實「cookie 本身沒問題，是舊工作 profile 被 Chrome 更新後判定版本不符、啟動時清空」 |
| 2026-11-01 | 修法落地（commit `d69b3b600`）：每次同步前先 `pkill` + 刪掉工作 profile 的 `Cookies*`/`Network Persistent State*`/`Singleton*`，同步放完整快照；啟動後回報 cookie 存活筆數。**連跑兩次都抓到 13 位，結果一致** |

**教訓（補）**：
5. **「有 cookie」不等於「cookie 是好的」**。`hasSessionCookie()` 只查名稱不看筆數，空殼 DB 也會回「有」。**要看總筆數**（`select count(*) from cookies`），空殼會是 32KB / 0 筆。
6. **Chrome 大版本更新後，工作 profile 一定要「重置 cookie 狀態」再同步**，否則複製進去的檔案會被 Chrome 啟動時丟掉。
7. **判斷「session 過期 vs 環境壞掉」永遠先查教練真實瀏覽器的 cookie 到期日**——這是最快、最不會誤導教練的分法。
8. **對照實驗是最快的定位法**：建一個乾淨 profile 複製同樣的檔案，跑一次就知道是「資料問題」還是「環境問題」。

### ✅ 2026-10-31 修好後的日常流程（0 按鈕，不需要教練做任何事）

```
腳本自動做三件事：
1. 從教練自己的 Chrome（~/Library/Application Support/Google/Chrome）複製 cookie 檔到工作 profile
   → 教練平常在 Chrome 登入 FB，cookie 自動跟著走，不用手動同步
2. 用 open -na（LaunchServices）＋ --headless=new 啟動 Chrome（教練螢幕不會跳視窗）
   → 讓 macOS 歸屬 responsible app，鑰匙圈才放行
3. 掛 CDP port 用 puppeteer.connect 抓「今日壽星」h2 底下的名字
```

**唯一會壞的情況**：教練自己把 FB 登出，或 FB 真的把 session 廢掉 → 那時才需要教練重新登入一次。

### 🔴 2026-10-24 事故紀錄（19 天靜默失敗）

| 日期 | 現象 |
|------|------|
| 2026-10-03 | `fb_session_data` 被搬到 `/Volumes/953-SSD/Mac本機搬移_20261003/fb_session_data`（symlink） |
| 10/04 起 | `ai.openclaw.fb-birthday`（launchd）每日 exit 1，錯誤訊息是誤導性的「browser is already running」 |
| 10/04～10/24 | **連續 19 天**背景排程失敗，但 `ca5195d8c4ca`（Hermes cron）同時也在跑，所以教練**實際上還是有收到名單**，只是多了一條壞掉的排程在暗處失敗 |
| 2026-10-24 | 找出根因（Chrome stderr: `Failed to create ... SingletonLock: Operation not permitted`），profile 改本機碟，launchd kickstart 驗證 exit 0 |

**教訓**：
1. **看到「already running」先看 Chrome 真正報什麼錯**，不要照字面以為有殘留行程。開 `dumpio: true` 才看得到 `process_singleton_posix.cc` 的真因。
2. **外部磁碟搬移後，所有需要寫入的 Chrome/DB profile 都會在 launchd 下失效**。搬檔前先想清楚「這個路徑會不會被背景排程寫」。
3. **有兩條排程做同一件事時，一條壞掉不會有人發現**——因為另一條還在送。健康檢查要盯「每一條」，不是只看「教練有沒有收到」。


---

## ⛔ 禁止事項

- ❌ **禁止**用 Browser Control 工具抓 FB 壽星（會燒好幾萬 Token，違反 0 Token 鐵律）
- ❌ **禁止**把腳本改回 LLM 視覺代理路線（除非教練親口重新拍板）
- ❌ **禁止**自動代發 FB 生日祝福（會被 FB 判定為機器人活動）
- ❌ **禁止**動 `scripts/fb_session_data/` 裡的 cookie（刪掉就要重登一次）
- ❌ **禁止**在沒壽星的日子打擾教練（依安靜完成協議）

---

## ✅ 自我驗證 Checklist

每次跑完確認：

- [ ] Cron Job ID `12fad20b` 還在 `cron list` 裡
- [ ] 腳本執行結束有正確關閉瀏覽器（不留殘留 process）
- [ ] 有壽星的日子有推到 Telegram
- [ ] 沒壽星的日子安靜完成
- [ ] 報錯有推到 Telegram（不要悶著不報）
- [ ] **跑過 `scripts/fb_birthday_verify.js` 交叉比對，名單一致**（2026-11-04 加；單一腳本輸出不算數，兩個獨立路徑一致才算數）

---

## 📚 相關歷史

- **2026-04-12**：教練拍板「半自動 + 0 Token」商業決策
- **2026-05-25~05-27**：連續多日成功抓到壽星（最多 10 位 / 最低 0 位）
- **2026-06-01**：從系統 crontab 改用 OpenClaw cron（避免 crontab 寫入問題干擾）
- **2026-06-07**：SOP 整理入庫，釘在 `knowledges/`

---

> 本 SOP 由軍師（OpenClaw 終端機）於 2026-06-07 建立，教練親口確認「要存」。
> 違反 = 守則 #12（不當搬運工：叫教練手動抓壽星）+ 商業決策反覆（守則 #07 不在同個地方跌倒兩次）。
