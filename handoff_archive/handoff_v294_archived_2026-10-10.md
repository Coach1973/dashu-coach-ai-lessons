## 🔴 給跨對話框軍師讀的總結摘要（2026-10-10 00:30 台灣時間，聯想 Windows 桌面版 Code 分頁，Sonnet 5.5→Haiku 5.5→Opus 5.5→Haiku→Sonnet 5.5（教練用 /model 切換），v294，教練說「總結」收工；對話 10/08 00:35～10/10 00:25）

**主軸：聯想端五件事——Plaud 連線測試；讀 Mac 的信裝好 NotebookLM 命令列工具並登入；三份 PDF 套 BNI 底圖輸出 PPT；10/08 當機調查；Plaud 最新兩筆錄音在聯想用顯示卡自己轉成逐字稿。另有一次被糾正（轉錄是我的任務，軍師早寫好 Plaud 做法，我沒先去雲端找）。**

### 1. Plaud 與 NotebookLM（Mac 來信 20261008-0240）
- Plaud 連線在聯想可用（只讀：list_files／get_file／get_note／get_transcript，沒有觸發轉錄）。
- 照信裝好 `notebooklm-mcp-cli` 0.15.4：`D:\NotebookLM工具\venv`；聯想本來就有 `default` 設定檔（plain 存放），`--storage protected` 被拒，改跑 `nlm login`，教練在主螢幕自己登入 bymyway7@gmail.com，`nlm login --check` 通過、150 本筆記本。**只做到第 4 步就停**（不建筆記本、不做簡報）。回信 `cross-agent/inbox/mac/20261008-1252_lenovo-to-mac_nlm-installed-login-ok.md`，來信已歸檔 `outbox/2026-10/`。

### 2. 三份 PDF 套 BNI ACCELERATE 底圖 → PPT（`E:\Claude-Data\簡報套底圖輸出\`）
- 《領袖加速器策略藍圖》12 頁（另有 PDF 版）、《96小時引爆億級商業宇宙》15 頁、《商戰破局的終極外掛》14 頁。用 `ai-go/ppt-prompt.md` 的 `brand_pptx.py`，底圖先放大 2 倍。
- **教練明講的規則：BNI LOGO 不能被內容蓋到（LOGO 可以蓋內容，內容不能蓋 LOGO）** → 聯想端改用 `--mode safe`（內容縮進 LOGO 上方乾淨區）；先前 mask 版第 4、15 頁底部字條壓到 LOGO／紅弧。
- ⚠️ **與 Mac v293 有出入**：Mac 10/09 的規則是「走 pdf_to_branded_pptx.py 預設 mask 滿版、不縮小」，聯想這邊因教練 10/08 17:04 的 LOGO 規則用了 safe（會縮小、四周留白）。兩邊是否統一，教練沒再說；先放 🤫。
- 教練 10/08 16:55 要求「PPT／PDF 一律給可點的 https 網址」；我問「要不要上傳公開」教練沒回「要」→ **沒有上傳**。後來 Mac 10/09 12:27 教練改說「打開所在資料夾並選取、不開內容」（要拖進 LINE），聯想對應做法＝`explorer /select,檔案`。

### 3. 10/08 22:45 聯想當機調查
- 事件記錄：22:45「虛擬記憶體用完」→ Chrome 0xc000012d 打不開、dwm 重啟、Lenovo Vantage／LogiOverlay 崩潰；22:52 教練登出再登入恢復。分頁檔被固定 4096MB、自動管理關閉（可用上限約 43.7GB，後來一度只剩 7GB，Comet／Chrome／Firefox／甘井各吃數 GB）。元兇程式查不到（沒留不足偵測紀錄）。登入後閃的視窗＝約 20 個開機自動程式，非病毒。建議分頁檔改系統管理——系統設定，AI 不代改，教練未回。記憶 `reference_lenovo_freeze_virtual_memory_exhausted_2026-10-08`。

### 4. Plaud 最新兩筆逐字稿（10/09 21:05、01:01）本機轉錄（教練 10/09 23:00 糾正）
- 教練：「逐字稿是你的任務，因為讓它轉是要扣點數的」「軍師有寫 plaud 技能，去雲端找」。我一開始只回「Plaud 還沒轉」，是失職；軍師做法在 `cloud_sync/skills/plaud-*` 與 `claude-brain/reference_plaud_backup_and_local_transcribe_2026-10-08.md`。
- 聯想做法（實測 92 分鐘 402 秒）：`D:\Plaud轉錄工具\`（faster-whisper large-v3-turbo＋RTX 3050 Ti，繁體用 OpenCC s2twp，「B&I」→BNI）。成品 `E:\Claude-Data\Plaud逐字稿\Plaud逐字稿_2026-10-09 21-05-40.txt`（92 分、1818 段）與 `…01-01-06.txt`（20 分、396 段），已用 explorer 開資料夾並選取。
- 三個坑：av 要 `<17`；Plaud 原始 `.opus` 無檔頭＝固定 80 位元組封包（`raw_opus_to_ogg.py` 包 ogg）；整段轉會因記憶體上限失敗，改 10 分鐘一段。記憶 `reference_lenovo_plaud_local_transcribe_gpu_2026-10-09`。

### 5. 收工整理
- 記憶庫自動同步留下的 stash pop 衝突（`claude-brain/MEMORY.md`、`feedback_opened_on_mac…`）已手動解：NotebookLM 與交付規則兩行取 Mac 較新版本，聯想的當機紀錄保留；我 10/08 寫的「PPT／PDF 給 https 網址」已標註被 10/09 規則取代。`stash@{0} auto-pull-stash-20261009225950` 未 drop（內容已並入）。

### 📋 下一場開工先做
**目前沒有教練交辦未完成。** 開工回報 5 行內，問「今天要從哪件事開始？」。
🔧AI 自己的（不問）：①教練丟簡報套 BNI 底圖：Mac 走 mask 滿版；聯想教練 10/08 說 LOGO 不能蓋，聯想用 safe——兩邊規則待教練哪天一句話統一；②D 槽 `D:\Plaud轉錄工具\audio` 與 `chunks_2105` 是工作檔（約 200MB），教練說可刪再清；③轉錄聯想已通，新錄音直接照記憶做。
🤫等教練自己提起：是否要把簡報上傳成公開網址；分頁檔改系統自動管理；`_new_repos/` 未追蹤資料夾不是我的，沒碰。
**commit**：mac-openclaw-workflows `057f664f8`（雲端合併 `b0fc688d1`，[Win] 聯想收工 v294）；工作檔在 E槽 Claude-Data/Plaud逐字稿（逐字稿成品）與 D槽 Plaud轉錄工具（轉錄工具），不在 git。

