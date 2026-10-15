## 🔴 給跨對話框軍師讀的總結摘要（2026-10-15 12:40 台灣時間，Mac 桌面版 Code 分頁，Sonnet 5.5；教練說「總結」收工；本段對話 10/14 18:51～10/15 12:36，對話容量用到約 36%）

**主軸：榮樹下訪談時間表網頁＋來賓卡刪除鈕＋朱元中／陳淑玲訪談備課；查出「上架卡死」根因；短網址上傳 405 修好；TAVA 更新版網址→自動備份流程固定下來；對話容量提醒 hook。**
- **榮樹下訪談建議時間表**：`github_repos/rongtree/interview-flow.html`（網址 /curated/rongtree/interview-flow.html，commit `0f20993` `bb458da` `4cbc983`）：60 分鐘錄製流程＋邀約到追蹤時程；教練改字「樹蔭席→嘉賓席」「吳董-嘉勉及建議事項」，藍圖 md 與承諾牆腳本同步（`c0f2dfd86` `643a22a8d`）。已收大樹作品集「大樹常用」＋/vault（`e565105b5`）。內部頁不放公開連結、noindex。真公益俱樂部頂部選單加「榮樹下」（social-club `e0c5f9d`）。
- **來賓卡**：查證朱元中（Patrick，天下顧問）**從未送出資料**（伺服器日誌五次 POST 全對得上 DB、系統無任何刪除功能）；新增**刪除／還原**（軟刪除，列表與來賓卡頁各有鈕，`d6b75a3ab`，測試 12 項），教練要刪的陳淑玲第一筆（AQGsXEnm8GKe，CBMC）我已刪；留下的 mmLIhyXPfHBM2 被人 23:33 按過「從公開名單隱藏」，已告知教練。朱元中／陳淑玲聯訪備課（3 重點＋關聯點「全人健康」＋做球給吳董 3 題）都在對話裡，沒存檔。
- **Podcast 抓取**：榮樹下「用到才現看」（開頁才讀 SoundOn RSS，5 分鐘快取），新兩集已抓到；SoundOn **沒有 webhook／WebSub**，做不到即時推；可把快取 5→1 分鐘（教練還沒說要）。
- **上架卡死根因**（最重要）：`scripts/optimize_site_assets.py` 的檔名替換 regex 遇 10MB 內嵌圖片資料變平方級，陳淑玲包（angel-sister）空轉 15 分鐘沒發完成通知，10/13 真公益包同病（當時用瘦身繞過）。已改直線寫法＋`test_optimize_rewrite_refs.py` 15 項（`2b3ae30b5`），卡住的包重跑成功：angel-sister、patrick-chu 上線並進作品集。
- **短網址上傳 405**：`/u/<代碼>` 的表單沒寫 action，POST 回自己被擋；補 `action="/curation/upload"`＋3 項測試（`f52b6667d`）。10/10 以來短網址上傳一直壞，只是長網址那條沒壞。
- **TAVA 更新版流程**：教練貼 `tava-ai.com/chat/…html`＝要我更新備份（TAVA 每版網址都新，無固定網址可輪詢）。已做 `tava-brand-web-playbook` v2（`443a8d8`）、my-tools 說明（`d70703e`）、coach888 工具類改名 v2；SOP `knowledges/SOP_TAVA更新版備份_my-tools與作品集收錄.md`＋反射 `R-TAVA-UPDATED-PAGE-SYNC`（`e6dfe1b71`，實測會跳）。
- **對話容量**：桌面版畫面看不到 context，改用 `mcp__ccd_session_mgmt__get_usage` 讀（本場 1M 視窗）；新增 `scripts/context_percent_hook.sh`（30/35/40/50% 各提醒一次，`7627c3888`），已掛 settings.json（備份 `.bak-20261014-before-context-hook`）——**本場沒自動跳，新對話才生效**。
- **10/17 零基礎學 AI 課＋海鮮鍋**（ema1017）名額 50→30（`1fe49ad`）；報名系統沒有名額欄位，不會自動額滿。
- **聯想信**（`/api/mytools/state`）已部署重啟、實測 GET/POST 後還原，已回信（inbox/lenovo）。
- **教練原話線索**：「我不喜歡輪詢機制」（第 6 次，事件觸發優先）；「我一般 30% 出頭就開新對話框」；「我只要丟更新版網址，你就知道要更新什麼」＝要固定流程不要每次交代；「我要網頁版，不是本機顯示版」＝交付一律線上網址。

### 📋 下一場開工先做
1. 新對話確認 `context_percent_hook.sh` 有自動在 30% 跳提醒（沒跳就查 settings.json 載入）。
2. 朱元中重送資料表後，看 `webapp.error.log` 有沒有 POST；陳淑玲 mmLIhyXPfHBM2 被隱藏，教練說沒印象才恢復公開。
3. 志工頁有人加入後教練報人數 → 改 `volunteer.html` 的 `JOINED`。
4. 教練回應模組化下一步 4 項（建議名冊引擎）；教練給南應大理監事名單 → 後台新增座位＋專屬連結。
5. 🔧 AI 自己：「報名名額」做成活動欄位並在額滿時自動關報名（ema1017 目前只有網頁文字）；Podcast 快取要不要 1 分鐘等教練一句話；時間沒換算改程式擋；43 站小字改到那站才調。

🙋 要教練決定：模組化下一步 4 項｜動到夥伴在用的系統要教練拍板｜問過：2026-10-14 報告內
🤫 等教練自己提起：預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；TAVA 備份頁放「工具類」還是「大樹常用」（已告知，教練沒回）；Podcast 快取改 1 分鐘。

---
> 📦 10/14 18:50 棒（志工頁／漢堡選單／來賓卡電報）已封存：`handoff_archive/handoff_2026-10-14_1850_志工頁_漢堡選單_來賓卡電報_archived.md`

---

> 📦 10/14 13:41 棒（嘉賓席改名／邀請函／字 20px）已封存：`handoff_archive/handoff_2026-10-14_1341_嘉賓席改名_邀請函_字20px_archived.md`

> 📦 10/14 09:50 棒（一週盤點與模組化報告）已封存：`handoff_archive/handoff_2026-10-14_0950_一週盤點與模組化_archived.md`
