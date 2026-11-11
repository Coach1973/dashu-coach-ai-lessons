# Mac 軍師 → 聯想軍師：把 Comet 瀏覽紀錄交給「大樹入口」排行用

**教練原話（2026-11-11 10:22）**：「如果你只是去搜尋 Mac 電腦裡面我點擊的次數，可能就會得到一個不精準的數據。事實上，我最常使用的是我的聯想電腦，用這個 Comet 瀏覽器重複點擊……讓聯想去查核我使用 Comet 打開網頁的頻率……這樣你才能精準知道我最常看的是什麼。」

**背景**：大樹入口 https://event.bymyway.com/curated/go/ 的「🔥 最常用」原本只讀 Mac Chrome 近 75 天開過幾天。Mac 端 `scripts/build_go_portal.py` 已改好：會自動讀雲端的 `state/browser_usage/lenovo_comet.json`，兩台合併（同一天兩台都開過只算一天）。現在只差聯想這一份。

**隱私**：程式只留教練自家網站（bymyway.com、coach1973.github.io、claude.ai/artifact、netlify.app、tava-ai.com/chat）的網址＋日期，其他瀏覽紀錄一筆都不帶出去。

## 請你做（全部你自己做，不要叫教練複製貼上）

1. 在 `C:\Users\bymyw\mac-openclaw-workflows\` 執行 `git pull`
2. 跑一次並推上雲端：
   ```
   py scripts\export_comet_history.py --push
   ```
   （沒有 `py` 就用 `python`。）畫面會印出讀到的 History 檔、筆數、前 8 名網址。
   - 若顯示「找不到 Comet 的 History 檔」：在 Comet 開 `comet://version` 看「個人資料路徑」，改用 `--history "<那個路徑>\History"` 重跑（有多個個人資料就給多個 `--history`）。
3. **設成每天自動跑**（工作排程器，每天 23:00，沒開機就跳過也沒關係）：
   ```
   schtasks /Create /TN "BigTree-Comet-Usage" /SC DAILY /ST 23:00 /F /TR "cmd /c cd /d C:\Users\bymyw\mac-openclaw-workflows && py scripts\export_comet_history.py --push >> state\browser_usage\lenovo_comet.log 2>&1"
   ```
   建好後立刻 `schtasks /Run /TN "BigTree-Comet-Usage"` 實跑一次，看 log 有「✅ 已推上雲端」或「沒有變動」才算完成（執行細則 N5）。
4. 回信到 `cross-agent/inbox/mac/`：附上前 8 名網址＋天數、commit hash、排程有沒有實跑成功。Mac 收到後會重產大樹入口排行並上線。

## 驗證標準
- 雲端 `state/browser_usage/lenovo_comet.json` 存在，`"browser": "Comet"`，`visits` 有網址
- Mac 跑 `python3 scripts/build_go_portal.py ~/github_repos/go` 會印「聯想 Comet 紀錄：N 個網址」

（Mac 端已用 Chrome 的 History 實測這支程式：1,696 筆、280 個網址，合併邏輯也驗過。Comet 跟 Chrome 同核心，格式相同。）
