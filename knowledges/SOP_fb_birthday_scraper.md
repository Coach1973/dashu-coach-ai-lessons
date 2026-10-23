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

腳本內部邏輯：
1. 用 Puppeteer 無頭模式啟動瀏覽器
2. `userDataDir` 載入 `scripts/fb_session_data/`（教練先前登入留下的 cookie）
3. 前往 `https://www.facebook.com/friends/birthdays/`
4. 等 `networkidle2` + 多等 4 秒
5. 抓頁面上所有 `<h2>` 標籤
6. 找到「**今日壽星**」這個 h2
7. 抓它下面到「剛過生日 / 即將過生日」出現之前的全部名字
8. 結束時關閉瀏覽器

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
| `scripts/fb_session_data/` | 教練 FB 登入 cookie 存放處（首次需手動登入一次）。⚠️ 2026-10-03 起這份已搬到 953-SSD 外接碟，**launchd 背景執行會失敗**，腳本已改用 `/Users/bymyway/.openclaw/fb_session_data_local`（本機碟） |
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
| 🔴 報「The browser is already running for ...fb_session_data」 | **Chrome profile 放在外部磁碟（USB SSD）時，launchd 背景執行沒有權限寫那個磁碟**，Chrome 建不了 SingletonLock 就會噴這句假錯誤。**解法：profile 必須放本機碟**。本機版在 `/Users/bymyway/.openclaw/fb_session_data_local`，腳本會優先用它、找不到才退回舊路徑。（2026-10-24 實例：`fb_session_data` 在 10/03 被搬到 953-SSD，結果連續 19 天每天 exit 1，教練完全沒收到壽星名單卻沒人發現） |

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

---

## 📚 相關歷史

- **2026-04-12**：教練拍板「半自動 + 0 Token」商業決策
- **2026-05-25~05-27**：連續多日成功抓到壽星（最多 10 位 / 最低 0 位）
- **2026-06-01**：從系統 crontab 改用 OpenClaw cron（避免 crontab 寫入問題干擾）
- **2026-06-07**：SOP 整理入庫，釘在 `knowledges/`

---

> 本 SOP 由軍師（OpenClaw 終端機）於 2026-06-07 建立，教練親口確認「要存」。
> 違反 = 守則 #12（不當搬運工：叫教練手動抓壽星）+ 商業決策反覆（守則 #07 不在同個地方跌倒兩次）。
