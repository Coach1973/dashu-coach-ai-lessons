# 名片資料庫（namecard-db）

教練的名片搜尋+產業鏈媒合系統。團隊把名片照片丟進 Amber 私有雲的「名片媒合中心」資料夾，
這套程式會自動讀照片、整理成資料庫，並提供手機可查的搜尋網頁。

## 這套系統做什麼

1. **擷取欄位**：讀名片照片，用 AI 直接看懂內容（不是傳統辨識軟體），抓出姓名/電話/Email/
   LINE/公司/地址/職稱/產品服務標語/推測產業類別
2. **搜尋網頁**：手機或電腦打開網址，用姓名/公司/地區/產品服務關鍵字/類別查
3. **產業鏈媒合**：AI 判斷哪些產業類別彼此適合互相認識（上下游或異業合作），
   自動把符合的名片兩兩配對，列在 `/matches` 頁面

## ⚠️ 目前狀態：程式碼寫好了，但還沒實機測試過

這台聯想機器沒有安裝 Python，沒辦法在這裡實際跑起來驗證。以下是照著程式邏輯仔細
檢查過、但**尚未真正執行過**的版本——第一次部署時務必先跑「小量測試」那一步
（步驟4），確認沒問題再處理全部名片，不要一開始就跑滿 1000~2000 張。

## 部署步驟（建議在 Mac mini 上跑，因為它能連到 Amber 私有雲，且已裝有 Python）

0. 需要 Python 3.10 以上版本（程式用了新版語法）

1. 確認 Amber 私有雲的名片資料夾已經用 SMB 掛載（Mac 用 Finder 的
   `smb://amber-Coach`，細節見共用大腦 `reference_amber_nas.md`）

2. 安裝套件：
   ```
   cd namecard-db
   pip install -r requirements.txt
   ```

3. 設定兩個環境變數：
   ```
   export ANTHROPIC_API_KEY="教練的API金鑰"
   export NAMECARD_FOLDER="/Volumes/home/名片媒合中心"
   ```
   教練已在 Amber 私有雲建立「名片媒合中心」資料夾（2026-07-12），路徑照 `reference_amber_nas.md`
   的慣例應該是 `home` 分享底下，如果 Mac 上實際掛載路徑不是 `/Volumes/home/...`，
   用 `ls /Volumes/` 確認實際掛載點名稱後調整。

4. **先小量測試**：把 `NAMECARD_FOLDER` 指到只有 10~20 張名片的測試資料夾，
   跑 `python watch_and_extract.py --once`，打開 `python app.py` 後看
   `http://localhost:5000` 檢查辨識品質（尤其是 LINE ID、地址這種容易讀錯的欄位），
   確認沒問題再指回正式資料夾跑全部 1000~2000 張。

5. 全量處理：
   ```
   python watch_and_extract.py --once      # 處理目前資料夾裡所有還沒處理過的名片
   python match.py                          # 產生產業鏈媒合建議
   python app.py                            # 啟動搜尋網頁，預設 http://localhost:5000
   ```
   之後每次有新名片上傳，重跑 `watch_and_extract.py --once`（只會處理新的、不會重複处理舊的）
   即可，也可以用 `--watch` 讓它每 60 秒自動掃一次。

6. **教練要的「丟名片就自動處理」，需要設定背景常駐程式**（這件事不能只靠對話承諾，
   要真的在 Mac mini 上裝一個系統服務）：
   ```
   which python3   # 先查出實際路徑，等下要填進plist
   cp com.coach.namecard-watch.plist.template ~/Library/LaunchAgents/com.coach.namecard-watch.plist
   # 打開剛複製的檔案，把 __PYTHON_PATH__ / __NAMECARD_DB_PATH__ / __NAMECARD_FOLDER__ / __API_KEY__ 四個佔位字串換成實際值
   launchctl load ~/Library/LaunchAgents/com.coach.namecard-watch.plist
   ```
   裝好之後，Mac mini 只要開著（登入狀態），教練丟名片進資料夾，60秒內就會被自動處理，
   不需要開終端機、不需要教練或AI手動觸發。可以用 `tail -f watch.log` 確認正在運作。
   `match.py`（產業鏈媒合）目前沒有排進自動排程，建議累積一批新名片後手動重跑一次即可，
   如果教練也想要這個自動化，之後可以再加一個定時任務。

7. **接上手機隨地可查**：比照現有「小龍蝦專線」的 Cloudflare Tunnel 做法
   （見共用大腦 `reference_xiaolongxia_line_tunnel_cloudflared.md`），
   在 cloudflared 設定裡新增一條路由，把一個網址（例如 `namecard.你的網域`）
   指到 `http://localhost:5000`，不需要另外申請新工具，跟 LINE 那條通道用同一套技術、
   不同路由，兩者互不影響。

## 檔案說明

| 檔案 | 用途 |
|---|---|
| `extract.py` | 讀一張名片照片，呼叫AI回傳結構化欄位 |
| `db.py` / `schema.sql` | SQLite資料庫（`namecards.db`，跟程式碼放一起） |
| `watch_and_extract.py` | 掃資料夾、批次擷取新名片 |
| `match.py` | 產生產業鏈媒合建議 |
| `app.py` + `templates/` | 搜尋網頁 |
| `com.coach.namecard-watch.plist.template` | Mac背景常駐服務樣板，讓「丟名片就自動處理」成真 |

## 已知限制 / 後續可以做的事

- LINE ID、手寫字、燙金反光名片辨識率會比較低，已設計「AI沒把握就標記需人工複查」機制，
  搜尋頁會顯示 ⚠️ 提醒
- 產業鏈媒合目前是「類別對類別」判斷（一次AI呼叫，不是每張名片兩兩比對），
  同一類別內部的人不會自動配對——如果教練想要「同業也建議互相認識」，可以再調整
- 目前沒有網頁登入保護，一旦接上公開網址，任何人拿到連結都能看到所有名片內容，
  之後可以視需要加一道簡單密碼保護
