# 結繩領導學工作坊即時戰報（jiesheng-report）

> 教練 2026-07-26 構想：台南／台中／台北三場工作坊，工作人員需要一個地方隨時看到「誰報名了、誰繳費了、誰還沒繳」。
> 比照 `mentor100.bymyway.com` 模式——**純手動輸入，不接LINE／Google表單，工作人員直接在後台打字**。
> 架構比照教練現有的 `event-signup`：Flask + SQLite，這次改成單表設計（一人只報一場，不需要多對多關聯）。

## 這台（Windows）已完成的部分

- 完整程式碼：`app.py`（路由）、`db.py`（資料庫）、`schema.sql`（表結構）、`templates/`（登入頁＋戰報後台，黑金風格沿用教練其他系統的視覺）
- 已用 Flask 開發伺服器在本機（`127.0.0.1:5061`）測試過：登入、三場各自新增報名者、勾選繳費＋填繳費方式/金額、編輯、刪除、統計數字即時反映——完整測試記錄見接力棒
- **這台 Windows 電腦沒有 cloudflared、沒有對外網域能力**，`bymyway.com` 子網域全部要靠 Mac 那台的 Cloudflare Tunnel，所以只做到「本機驗證程式碼沒問題」這一步，正式上線需要 Mac 那邊接手

## Mac 那邊要做的事（比照 event-signup／bni.bymyway.com 部署SOP）

1. 把這個 `jiesheng-report/` 資料夾同步到 Mac（雲端 `mac-openclaw-workflows` repo git pull 就會拿到）
2. 建 Python 虛擬環境＋裝套件：
   ```bash
   cd ~/.openclaw/workspace/jiesheng-report   # 或實際 workspace 路徑
   python3 -m venv venv
   ./venv/bin/pip install -r requirements.txt
   ```
3. 設定帳密（環境變數，不進版本庫）。**教練已指定密碼（公司統編），雜湊值已產生好，直接用即可，不用重新產生：**
   - `JIESHENG_SECRET_KEY`：隨機字串（例如 `openssl rand -hex 32`）
   - `JIESHENG_ADMIN_USER`：`rpl`（2026-07-26教練指示由預設`staff`改為`rpl`小寫）
   - `JIESHENG_ADMIN_PASSWORD_HASH`：`scrypt:32768:8:1$uxXZ8x5sRmBQ97XV$3a8e071bf28e76526543e1599977f67f1d04351243f9d42497ab74948c5c4f0aba33a2342f0091f1b825b4e6a6cce7035d5f92f07a650e6350bee5856ec10022`
   - `JIESHENG_PORT`：**實際部署用 5063**（原建議 5061 跟既有 `peipei-event` app 撞了，5060=event-signup、5061=peipei-event、5062=mentor100，Mac上線時改用5063錯開）
   - 明文密碼本身沒有寫進任何檔案（一律只存雜湊值），教練本人知道是公司統編，需要時教練自己告訴工作人員
4. **兩種部署方式擇一，建議選①（更省事，比照 `bni.bymyway.com` 的做法）：**

   **① 沿用既有 tunnel `openclaw-macmini` 加一條新 Route（推薦，Mac已採用此法）**
   - Cloudflare Zero Trust 網頁後台有帳單資訊卡關（同seabiscuit.bymyway.com遇到的狀況），改用CLI+臨時API Token：`cloudflared tunnel route dns openclaw-macmini rpl-workshop.bymyway.com`建DNS，再用臨時建立、範圍限縮為「Cloudflare Tunnel:Edit」、短效期的API Token透過`PUT /accounts/{account}/cfd_tunnel/{tunnel}/configurations`把新hostname加進ingress規則，完成後立即刪除該臨時Token
   - Published application：subdomain `rpl-workshop`（教練已定案）、domain `bymyway.com`、service `http://localhost:5063`
   - 不用另外裝 LaunchAgent 跑 cloudflared，只要保證 Flask app 常駐執行即可（見下方 LaunchAgent）

   **② 另開一顆專屬 tunnel（比照 event-signup 原本的做法，較費工，非必要不建議）**
   - 新增 `~/.cloudflared/jiesheng-config.yml`＋對應 LaunchAgent，跟 event-signup 的 `event-tunnel.plist` 同樣寫法

5. 常駐 Flask（LaunchAgent，KeepAlive 開機自動跑，比照 `com.coach.event-webapp.plist`）：
   ```xml
   <!-- ~/Library/LaunchAgents/com.coach.jiesheng-report.plist -->
   <key>ProgramArguments</key>
   <array>
     <string>/Users/bymyway/.openclaw/workspace/jiesheng-report/venv/bin/python3</string>
     <string>/Users/bymyway/.openclaw/workspace/jiesheng-report/app.py</string>
   </array>
   <key>EnvironmentVariables</key>
   <dict>
     <key>JIESHENG_SECRET_KEY</key><string>（隨機字串）</string>
     <key>JIESHENG_ADMIN_USER</key><string>rpl</string>
     <key>JIESHENG_ADMIN_PASSWORD_HASH</key><string>（雜湊值）</string>
   </dict>
   <key>KeepAlive</key><true/>
   ```
6. 驗證：`curl https://rpl-workshop.bymyway.com/admin/login` 回 200，帳密登入後看得到三場戰報頁面

## 網址（已上線，2026-07-26 Mac軍師部署）

- 後台：`https://rpl-workshop.bymyway.com/admin`
- 常駐：`com.coach.jiesheng-webapp.plist`（LaunchAgent，KeepAlive，比照event-webapp）
- 驗證：`curl https://rpl-workshop.bymyway.com/admin/login`回200、標題正確；AI未曾輸入過真實密碼（公司統編僅教練本人知道），登入流程需教練親自測試一次

## 資料表

單一 `registrants` 表（`schema.sql`）：姓名／電話／報名日期／已繳費／繳費方式（ATM／PAYUNi／其他）／金額／備註。
`db.py` 沿用教練既有 `PRAGMA table_info()` 檢查升級模式（見 `event-signup/db.py`），未來要加欄位時比照辦理，不會動到既有資料。

## 檔案

- `app.py` 網頁主程式｜`db.py` 資料庫｜`schema.sql` 表結構
- `templates/login.html`、`templates/admin.html`——黑金風格，Noto Sans TC，沿用教練其他系統視覺
- `jiesheng_report.db` 資料庫檔（不進版本庫，Mac 上線後才會產生）

## 🔴 2026-07-26 真bug記錄：.env裡的$符號被bash source吃掉，導致密碼永遠登不進去

**根因**：LaunchAgent啟動時用`bash -c "set -a; source .env; ..."`載入環境變數，`.env`裡`JIESHENG_ADMIN_PASSWORD_HASH`的值含有scrypt格式特有的`$`分隔符（例如`1$uxXZ8x5sRmBQ97XV$3a8e...`），沒加引號時bash的`source`會把`$uxXZ8x5sRmBQ97XV`、`$3`當成變數展開（皆為未定義，展開成空字串），導致實際載入到Flask程式裡的雜湊值被吃掉一截，跟教練的真實密碼永遠對不上——即使密碼打得完全正確也無法登入。

**修復**：`.env`裡任何含`$`字元的值都要用單引號包住，例如：
```
JIESHENG_ADMIN_PASSWORD_HASH='scrypt:32768:8:1$uxXZ8x5sRmBQ97XV$3a8e...'
```

**驗證方式（不經過網頁登入表單，純本機雜湊比對）**：
```bash
bash -c 'set -a; source .env; set +a; echo "$JIESHENG_ADMIN_PASSWORD_HASH"'
```
比對輸出是否跟原始雜湊值逐字一致；再用Python `werkzeug.security.check_password_hash(hash, 真實密碼)`確認回傳True。

**教訓**：這條規則跟既有試金石教訓「`.env`含`$`字元的值要單引號包住」（見待辦列表兩個小工程教訓之一）完全相同，這次是真的踩到了才發現先前只是記錄提醒、沒有在這個新專案套用到。以後任何`.env`檔案，只要值裡有`$`、反引號、空白等shell特殊字元，一律加單引號，不要假設「反正只是資料，不會被當成程式碼」。

## 2026-07-26 教練追加需求：邀請人/倒數/目標達成率

- **邀請人**欄位（原叫「成交人員」，教練2026-07-26指示改名，選項/限制不變）：下拉選單，僅四選一（曜董／大樹／佩君／Lavi），新增報名時可選，也可事後在名單表格編輯。DB欄位名`referrer`
- **備註欄**：本來就有（schema/UI皆支援），教練誤以為沒有，實際上新增/編輯表單都看得到
- **開課倒數**：三場戰報卡片各自顯示距離開課還剩幾天（依`WORKSHOP_DATES`即時計算，不用手動更新）
- **目標達成率**：`WORKSHOP_TARGETS`（台南25／台中20／台北50）搭配目前報名人數算出百分比+進度條

**歷史資料匯入**（2026-07-26，教練提供Downloads資料夾3張分場Google表單截圖）：
- 已建入5筆確定資料（台南4筆+台中1筆），姓名/電話/報名日期/是否已繳費/繳費方式/金額(皆NT$10,000)/備註/邀請人皆有
- 邀請人比對規則：原始資料寫「大樹／大樹教練／吳大樹(先生)」→歸類「大樹」，「陳佩君」→歸類「佩君」；不屬於固定4人名單的其他人名（如蔡宇騏、鄧溢錩等）→邀請人欄留空，原始姓名保留在備註欄不遺失
- **待辦（卡住）**：台北場10筆資料截圖沒有帶到最左邊「時間戳記」（報名日期）欄，姓名/電話/邀請人/備註都齊全但缺報名日期，需教練補提供或指定日期後才能建入
