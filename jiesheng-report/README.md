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
   - `JIESHENG_ADMIN_USER`：`staff`
   - `JIESHENG_ADMIN_PASSWORD_HASH`：`scrypt:32768:8:1$uxXZ8x5sRmBQ97XV$3a8e071bf28e76526543e1599977f67f1d04351243f9d42497ab74948c5c4f0aba33a2342f0091f1b825b4e6a6cce7035d5f92f07a650e6350bee5856ec10022`
   - `JIESHENG_PORT`：預設 5061（跟 event-signup 的 5060 錯開，跟其他既有服務對照 `~/.cloudflared/` 底下各 config 確認沒撞）
   - 明文密碼本身沒有寫進任何檔案（一律只存雜湊值），教練本人知道是公司統編，需要時教練自己告訴工作人員
4. **兩種部署方式擇一，建議選①（更省事，比照 `bni.bymyway.com` 的做法）：**

   **① 沿用既有 tunnel `openclaw-macmini` 加一條新 Route（推薦）**
   - Cloudflare Zero Trust 後台 → Tunnels → `openclaw-macmini` → Routes → Add route
   - Published application：subdomain `rpl-workshop`（教練已定案）、domain `bymyway.com`、service `http://localhost:5061`
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
     <key>JIESHENG_ADMIN_USER</key><string>staff</string>
     <key>JIESHENG_ADMIN_PASSWORD_HASH</key><string>（雜湊值）</string>
   </dict>
   <key>KeepAlive</key><true/>
   ```
6. 驗證：`curl https://rpl-workshop.bymyway.com/admin/login` 回 200，帳密登入後看得到三場戰報頁面

## 網址（部署後才會生效）

- 後台：`https://rpl-workshop.bymyway.com/admin`（教練可改名，記得同步更新這份文件跟接力棒）

## 資料表

單一 `registrants` 表（`schema.sql`）：姓名／電話／報名日期／已繳費／繳費方式（ATM／PAYUNi／其他）／金額／備註。
`db.py` 沿用教練既有 `PRAGMA table_info()` 檢查升級模式（見 `event-signup/db.py`），未來要加欄位時比照辦理，不會動到既有資料。

## 檔案

- `app.py` 網頁主程式｜`db.py` 資料庫｜`schema.sql` 表結構
- `templates/login.html`、`templates/admin.html`——黑金風格，Noto Sans TC，沿用教練其他系統視覺
- `jiesheng_report.db` 資料庫檔（不進版本庫，Mac 上線後才會產生）
