# v291 封存（2026-10-09 收工時由 v293 搬出）

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-08 12:46 台灣時間，Mac 桌面版 Code 分頁，Sonnet 5.5，v291，教練說「總結」收工；對話 10/07 21:05～10/08 02:38，與 v290 平行）

**主軸：教練買了 Plaud 錄音筆。本場把 Plaud 接進 Claude（Mac 本機＋claude.ai 連接器）、175 筆錄音全備份到 SSD 並本機轉成繁體中文；同時做出三個「貼給任何 AI 就會」的技能（生圖／簡報套底圖）並上大樹作品；最後把 NotebookLM 自動化（nlm）裝好登入，教練說「只是要測能不能進入」。**

### 1. 兩個可貼給任何 AI 的技能（皆已進 coach888「大樹常用」第一、二項）
- **生圖一鍵注入**（用 LK888 出與當下專案畫風一致的圖，先做風格卡、先試一張、一張只付一次錢）：`https://coach1973.github.io/ai-go/lk888-inject.html`；技能 `~/.claude/skills/lk888-project-style-images/`。**沒有真的呼叫 LK888 出圖測過**（要扣點），金鑰不放頁面。
- **簡報套底圖一鍵注入**（任何底圖，自動判斷 mask／safe／overlay，不用手量座標）：`…/ai-go/ppt-inject.html`；技能 `~/.claude/skills/pptx-brand-background/`、備份 `knowledges/SKILL_簡報套底圖_通用版.md`。實測 BNI 真底圖＋5 種假底圖。**NotebookLM 簡報底部有說明文字，BNI 底圖要用 `--mode safe`，預設 mask 會被 LOGO 吃掉字。**
- commit：ai-go `0a5c7c4` `818d14a`；coach888 `ecf0241` `6de66c2` `fe16c70`；workspace `f536c66f3` `11a55a9fe` `7b7948dcc`。

### 2. Plaud（全部在 SSD `/Volumes/953-SSD/Plaud錄音備份/`，不占本機）
- MCP 已裝（Claude Code／桌面版／Codex 都被設定；安裝程式順手覆蓋了剪貼簿）；claude.ai 連接器教練自己點連接（我被 classifier 擋下，**教練早就是 bypass，我沒查就叫他去切＝試金石案例109**，commit `82a640283`，已改源頭記憶＋反射 R-CLASSIFIER-DENIED-CHECK-REAL-MODE）。
- 175 筆音檔 1.8 GB 下載完，ffprobe 驗 174 通過（1 筆是 Plaud 教學範例差 7 秒）；Plaud 自己的逐字稿＋AI 筆記 101 筆已一併存。本機 mlx-whisper large-v3-turbo 轉繁中 **10/08 05:45 全部完成 175/175，平均 18.5x，共 308 分鐘**；預覽頁 `預覽.html`（有搜尋）；轉完會 Telegram 通知教練（監看程式已結束，應已送出，**我沒確認教練收到**）。
- Plaud MCP **沒有刪除功能**；刪雲端只有教練能做。7 筆不到 1 分鐘（5 筆可刪；「會議記錄：錄音功能的運作與應用示範」46 秒、「國立台北科技大學億光大樓」55 秒有正式名稱，刪前要教練確認）。教練回覆「全部下載、轉錄後刪雲端」我答：可行，但刪前先備第二份、聯想拿錄音靠 Plaud 雲端（刪了聯想拿不到）。
- 讀取 Plaud 不扣 300 分鐘額度（實測對未轉寫的錄音只回空）。Muse.app＝Meta AI App，無可呼叫的語音模型，且不建議送 BNI 對話給 Meta。

### 3. NotebookLM（`/Volumes/953-SSD/NotebookLM工具/`）
- `notebooklm-mcp-cli` 0.15.4（非官方、用未公開介面、有條款風險）裝好；教練 Google 登入 bymyway7@gmail.com（PRO 方案，149 個筆記本）。**實測整條通**：建筆記本→放文字→`nlm slides create --format detailed_deck --language zh-TW`（生成約 7 分鐘）→下載 PDF／PPTX（10 頁，每頁是一張圖）→套 BNI 底圖。試做成品在 `NotebookLM工具/試做/`；教練帳號留了測試筆記本「【試做】BNI會員心得分享（Plaud錄音）」（要不要刪是教練的事）。
- 🔴 **教練糾正：「只是要測是否能進入 NotebookLM，你跑得有點太快」**——測試類只做到能回答「能／不能」，下一步一句話講（記入 `reference_notebooklm_cli_pipeline_2026-10-08.md`）。
- 聯想：寫信 `cross-agent/inbox/lenovo/20261008-0240_mac-to-lenovo_install-notebooklm-cli-test-login.md`（commit `72909e315`），**只叫它安裝＋登入＋`nlm login --check` 後停**；教練只要對聯想的 Claude 說「去讀信」。尚無回信。
- **ACER**：教練收工時補一句「ACER 也要寫信、聯想有的技能也複製過去」→ 寫信 `cross-agent/inbox/acer/20261008-1250_mac-to-acer_install-skills-and-notebooklm-test.md`：裝兩個技能（生圖、簡報套底圖，檔在 `knowledges/SKILL_*.md`）＋同樣的 NotebookLM 登入測試。**我看不到聯想實際裝了什麼**，信裡請 ACER 回報有沒有更多技能要補。

### 📋 下一場開工先做
**目前沒有教練交辦未完成。** 開工回報 5 行內，問「今天要從哪件事開始？」。
🔧AI 自己的（不問）：①教練提「Plaud 對照表」時，讀 `local_text/` 175 份逐字稿（先濾重複幻覺，預覽頁已有 collapse 範例 `tools/make_preview.py`）→出「時間＋建議標題＋長度」表，優先 77 筆沒有名稱的；②聯想、ACER 回信後讀 `inbox/mac/`（目前這個資料夾還不存在，對方回信時會建）；③查 Telegram 通知有沒有真的送達（`logs/notify.log` 是空的）。
🤫等教練自己提起：刪 Plaud 雲端（前提：對照表驗證完＋備份第二份）；NotebookLM 一鍵注入頁（待聯想測通再做）；LK888 生圖技能真跑一次。
**commit**：workspace `f536c66f3` `7b7948dcc` `82a640283` `72909e315` `11a55a9fe`；ai-go `0a5c7c4` `818d14a`；coach888 `ecf0241` `6de66c2` `fe16c70`；本棒另計。

