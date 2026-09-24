## 🔴 給跨對話框軍師讀的總結摘要（2026-09-24 01:20，Mac桌面版，新的一棒 v244）

**本場主軸：教練問「大樹創作SOP有沒有告訴其他人」，查出小龍蝦當晚連兩次無視教練口令跑錯SOP的根因（SOP檔案沒寫教練會講的口語別名），修復後委託赫米斯成功執行大檔案上架，過程中又抓到並修復coach888新增項目時切壞既有項目HTML結構的bug，最後依教練指示重新調整coach888分類+補上熱門排行刪除功能。**

### 1. 🔴🔴 「大樹創作SOP」口語別名缺失，小龍蝦深夜連兩次跑錯SOP
教練問「有沒有把SOP告訴小龍蝦/赫米斯/佩佩老師/孔大哥」，查小龍蝦即時對話紀錄（`agents/main/agent/openclaw-agent.sqlite`）發現教練當晚23:55~00:02兩度明講「走大樹創作SOP」，小龍蝦仍跑店家策展SOP插進大台南商圈整合中心，教練手動刪除。根因：SOP檔案完全沒寫「大樹創作SOP」「大樹作品」這些教練口語別名。已修復：SOP檔加別名區塊、`路徑大全_憑證層.md`策展金鑰前加警告、`AGENTS.md`路由表補一行，同步補上kong/peipei的AGENTS.md（教練確認要放，但這兩個agent目錄整個被.gitignore排除，無commit hash）。回信赫米斯附完整SOP+根因說明。commit `08c796b60`。

### 2. 🔧 大樹創作SOP補上完成通知步驟
教練發現送件包上架後找不到完成報告，一查發現這條SOP從頭到尾沒有Telegram通知這一步（店家策展SOP有）。已重用`curation_process.py`既有`notify()`補上第7步，實測發送成功。commit `86c93473e`。

### 3. 🔴 軍師門檻修訂+克勞德/赫米斯命名澄清
教練親口修訂身份判定鐵律：軍師門檻從「限定Opus」放寬為「Sonnet 5以上（含Opus/Fable）」。已改`~/.claude/CLAUDE.md`（本機燒錄檔不進git）+ `workspace/claude_global_backup/CLAUDE.global.md`（commit `2116626cf`）。另確認「克勞德=Claude、赫米斯=Hermes」是教練固定音譯叫法，寫入新reference記憶。

### 4. 🔴🔴 赫米斯成功執行大檔案上架，但意外抓到coach888插入bug
教練驗證赫米斯上架《造林》漫畫成功（大檔案繞過小龍蝦Telegram 20MB上限，改用赫米斯處理），但回報coach888「AI作品一覽」找不到新作品。查出赫米斯插入新項目時，把新的item div插在既有「AI人才檢索提案」項目的`<div class="thumb">`跟`<div class="meta">`中間，切壞了該項目的`<a>`標籤結構——根因是這個分類混雜新舊兩種item模板，單純字串比對「第一個`<div class="item">`」容易誤判位置。已修復coach888 index.html（commit `31739ac`）+ 補強SOP插入步驟加上標籤配對檢查（commit `86e8fa472`）。

### 5. 🔧 coach888分類重組+熱門排行新增刪除功能
教練指出「對外公開」分類已在線上改名「Netlify代表作」（伺服器同步狀態`/api/coach888/state`跟git靜態HTML是兩個不同地方，之前沒查到才報錯分類名稱），要求新建「最新作品」分類專放教練個人創作。已建立`zuixinzuopin`新分類，把《造林》/《AI人才檢索提案》/《32MB封包攻防戰》移入，同步更新靜態HTML+伺服器狀態（coach888 commit `71ab9f7`）。另外教練要求熱門排行榜要能刪除已結束活動——查出這個排行榜是純點擊次數自動排名，完全沒有刪除機制，已新增後端DELETE端點（workspace commit `e3cbcd4f3`）+前端✕刪除鈕（coach888 commit `c4bf5df`），已重啟服務+實測驗證。

### 6. 🔧 MEMORY.md consolidate-memory執行完畢
教練授權「去做」，MEMORY.md從39KB/188行壓到18.6KB/139行，主要靠壓縮批次回補區塊+砍37條過時/重複索引，未刪除任何原始記憶檔案。

### 📋 當時的下一步（已被v245取代，不要照唸）
E16瘦身本場已執行：v238~v241封存進`handoff_archive/handoff_v238_to_v241_archived_2026-09-24.md`。其餘待辦以開頭待辦表為準。

### 🔑 本場commit
`08c796b60`、`86c93473e`、`2116626cf`、`86e8fa472`（workspace repo）；`e3cbcd4f3`（workspace repo, click-counts DELETE端點）；`31739ac`、`c4bf5df`、`71ab9f7`（coach888 repo）。本次總結commit另計。

---
