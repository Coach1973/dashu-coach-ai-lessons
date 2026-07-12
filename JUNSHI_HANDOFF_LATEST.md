# 軍師接力棒 · 2026-07-13 v61（聯想桌面版 Sonnet 5，名片系統首次評估建置+密碼界線規則確認+bni-dna Netlify同步）

> 建立時間：2026-07-13（台灣時間）
> 本棒執行者：聯想桌面版 Sonnet 5
> 上一棒：v60（Mac，名片系統雙通道+PaddleOCR換血+Hook稽核+ai-talk網站上線，完整內容見下方精簡回顧）
> 本棒主軸：**這場對話跟Mac的v58~v60是同一個名片專案的兩端——我這邊負責從零評估+初版建置+交接，Mac那邊接手後做了大量真實部署與修正，兩邊時間線有重疊，細節以Mac那邊為準**

---

## 🎯 本場戰果

### 1. 名片資料庫（namecard-db）從零評估到初版建置＋交接給Mac

教練要把Amber私有雲名片資料夾累積的1000~2000張名片建成搜尋資料庫+產業鏈媒合系統。
查證GitHub沒有現成完整方案（既有公開專案多是英文OCR課程作業等級），判斷自建。這台
聯想沒裝Python沒辦法實機測試，寫好完整程式碼（Claude視覺讀卡→SQLite→Flask搜尋頁→
類別媒合）、`launchd`背景服務樣板、部署README後commit+push，寫inbox交接信給Mac軍師
接手部署。

**⚠️ 重要：Mac軍師接手後做了實質性修正，不要照抄我這邊寫的初版**——最大的一個是
Claude視覺直接讀圖辨識率太差（教練實測抓到把名片內容整個捏造），Mac改成PaddleOCR
先讀文字、MiniMax再整理成欄位的兩階段管線；背景常駐也從我原本設計的輪詢式`--watch`
改成事件驅動（launchd WatchPaths監控SMB資料夾變更）。完整最新狀態看Mac的v58~v60
接力棒段落，我這邊只是起點。

### 2. 🔴🔴🔴 密碼界線衝突：小龍蝦提議「AI自動打密碼」被駁回，已列入JUNSHI_RULES規則#6

小龍蝦學長引用教練2026-05-15/2026-03-02原話，主張「教練已開最高權限，AI應主動讀密碼
自己填」。查證原話屬實，但我判斷這條界線不因授權鬆動而拒絕比照辦理，把疑慮攤給教練。
後來Mac軍師也獨立做了同樣判斷，教練親口拍板採修正版（「不當搬運工」全採納，但「AI
自己打密碼」不採納）。已寫進`JUNSHI_RULES.md`規則#6，我確認過聯想的開工hook
（`feed_junshi_handoff.ps1`第154~167行）本來就有讀取這份正典的邏輯，不用額外修改，
已勾選確認。記憶：`feedback_password_boundary_vs_courier_resolution.md`。

### 3. 🟡 CC Switch換API key後Claude Code還是停留在MiniMax——已診斷未修復

教練在CC Switch新增/啟用一組新API key，但這台聯想的Claude Code還是叫用MiniMax-M3。
查證：CC Switch確實有更新`~/.claude/settings.json`（剛改過，只含`ANTHROPIC_BASE_URL`/
`ANTHROPIC_AUTH_TOKEN`兩個欄位）。但目前process環境變數裡有一個`ANTHROPIC_MODEL=
MiniMax-M3`，**不是**來自settings.json、也不是User/Machine層級的Windows環境變數，
來源還沒查到（懷疑是啟動Claude Code的捷徑或腳本裡寫死的）。已建議教練先試「完全關閉
Claude Code再重開」（CC Switch官方說明：環境變數只在process啟動時讀取一次），
**這件事還沒有教練回報是否重開後解決，下一棒要追蹤**。

順帶查過這台電腦上還有哪些軟體有API Key設定：OpenClaw(`~/.openclaw/workspace/agent/
models.json`)本來就刻意固定MiniMax（教練自訂規則，非bug）；OpenCode、Hermes這台電腦
上完全沒安裝；opcode只找到`opcode-源碼備份`，是程式碼備份非執行中軟體。

### 4. 🟢 bni-dna網站Netlify同步

`coach1973.github.io/bni-dna/` → `bni-dna.netlify.app`，用既有Netlify token走zip+API
直推（site id `4174fb1c-db98-40ec-a07c-09cd00ec2ea9`），記得加`_headers`檔避免顯示
純文字原始碼的老問題。deploy後用瀏覽器讀取頁面內容確認出席表格/規則文字正常顯示。

### 5. 🟡 小龍蝦委託找「CLAUDE圓形頭像」設計記錄——這台也查無結果

`state/LETTER_TO_LENOVO_ACER_JUNSHI_2026-07-13.md`託聯想/ACER軍師找一個教練記得的
「圈裡寫CLAUDE」頭像設計對話。在這台電腦搜過session紀錄關鍵字、本機cool-case本地
clone的assets資料夾（只有`coach-avatar.jpg`/`xiaolongxia-avatar.jpg`/`wu-badge.png`/
`analysis-badge.jpg`/`img_2.png`/`wu_small.png`，沒有claude相關圖檔），也是**查無**，
跟Mac那邊的搜尋結果一致。教練說下次會主動告知資料實際位置，這件事目前是等教練提供
線索，不是繼續盲找。

---

## 📋 下一棒待辦（聯想視角，跟Mac待辦清單分開列，避免混淆）

| 優先 | 任務 |
|------|------|
| 🟡 | 追蹤CC Switch/MiniMax模型卡住的問題：教練重開Claude Code後有沒有解決？如果沒解決，要繼續查是哪個捷徑/腳本寫死了`ANTHROPIC_MODEL` |
| 🟢 | CLAUDE圓形頭像：等教練主動提供線索再查，不要重複盲找 |
| 🔴 | 2026-07-18：聯想C槽觀察期滿，確認教練這幾天用起來正常後可刪2份保留備份（共約94GB），見更早的`project_lenovo_c_drive_slimdown_2026-07-11.md` |

（名片系統、biz-gym黑金版、ai-talk、cool-case等其餘待辦全部在Mac的v60棒裡，此處不重複列出，避免兩邊資訊不同步）

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `namecard-db/`（初版建置，多數檔案已被Mac後續修改，見git log）
- `inbox/名片資料庫任務交接_請Mac軍師接手部署_20260712.md`
- `claude-brain/feedback_password_boundary_vs_courier_resolution.md`（新增後續段落）
- `claude-brain/project_namecard_db_2026-07-12.md`（我建立，Mac後續大幅補充）

---

## 📜 v60 精簡回顧（Mac桌面版 Sonnet 5，完整內容見git歷史/上一版本檔案）

1. 名片系統雙通道（LINE/Telegram）+ PaddleOCR取代直接視覺辨識（準確率教練評95%以上）
2. Hook系統性稽核：23支宣告為hook的腳本只有少數真的註冊進settings.json，已全部補齊+設SessionStart自動稽核
3. Amber無法自架Docker App，改用獨立Cloudflare Tunnel（`namecard.bymyway.com`）
4. AI微型論壇(ai-talk)網站從零上線，GitHub Pages+Netlify雙掛
5. cool-case案例33~40上架，網站累計40個案例
6. 待辦：biz-gym黑金版（教練指定每棒必提醒）、佩佩老師名片跨帳號讀取問題（改走Google Drive方案）、ACER尚未確認JUNSHI_RULES規則#6

---

> 聯想桌面版 Sonnet 5 親筆，2026-07-13。教練說「總結，我開新對話」，本棒收尾。這場
> 對話跟Mac端的名片系統開發是同一個專案的兩段時間線，我負責起頭評估+初版，Mac負責
> 落地部署+除錯精修，下一棒接手時記得名片系統細節以Mac的v60為準。CC Switch模型卡住
> 的問題還沒確認是否解決，是本場唯一需要追蹤的未完事項。
