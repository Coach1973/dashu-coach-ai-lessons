# 修復大台南策展中心12則貼文縮圖+重複網址問題

> **寄件人**：Mac桌面版軍師（Sonnet 5）
> **收件人**：手機版（MiniMax-M3, Remote Control session）
> **背景**：教練看到你今晚貼的12則大台南策展中心貼文後，回報兩個問題：①沒有縮圖 ②文案裡「完整介紹」跟「圖片」兩行網址其實是重複的。教練把對話拿給我看，我已經驗證根因並跟教練討論出解法，現在把完整任務交給你執行（省教練的Sonnet流量，用你這邊的MiniMax額度做）。

## 根因（已驗證，不用重查）

`event.bymyway.com/curated/<slug>/` 這個路由是純粹的檔案passthrough（`event-signup/app.py`裡`curated_page()`直接serve `~/github_repos/<slug>/index.html`），**不是共用Flask template**——每個slug是自己獨立的靜態HTML檔案，OG標籤要逐一修，沒有「改一個檔案全部生效」這回事。

我用curl驗證過你貼的12個slug裡至少有這兩種問題：
- **完全沒有og:標籤**（例：`kangyenju`、`everydaycaf-tai-nan-san-dian`）
- **og:image是相對路徑**，FB爬蟲抓不到圖（例：`flower-site`的`img/hero.jpg`、`historic-residence`的`assets/hero-front.jpg`、`sbip`的`assets/og-card.jpg`）

你自己昨晚寫的SOP `claude-brain/reference_fb_real_browser_repost_sop_2026-09-18.md` 裡「文案格式範本」那段已經是正確的單一URL格式（沒有重複網址的問題），不用再改文案格式，只要把og:image修對，FB會自動抓圖產生縮圖卡片。

## 任務步驟

### 1. 逐一修復12個slug的index.html

對照你今晚貼過的12個slug（清單在你自己的`claude-brain/data/curation_21_posts_repack_2026-09-18.md`「✅可重貼」那12則），逐一打開`~/github_repos/<slug>/index.html`：

- 若已有`<meta property="og:image" content="相對路徑">`：改成絕對網址 `https://event.bymyway.com/curated/<slug>/<原本的相對路徑>`
- 若完全沒有og:標籤（目前已知至少kangyenju、everydaycaf-tai-nan-san-dian）：在`<head>`補上完整一組：
  ```html
  <meta property="og:type" content="website">
  <meta property="og:title" content="{用<title>裡的內容}">
  <meta property="og:description" content="{用<meta name=description>內容，沒有就自己從內文摘一句}">
  <meta property="og:image" content="https://event.bymyway.com/curated/<slug>/{頁面裡找到的第一張圖}">
  ```
- 改完每個repo，`git add`+`git commit`+`git push`（這些是各自獨立的git repo，在`~/github_repos/<slug>/`底下）
- 改完立刻curl驗證：`curl -s https://event.bymyway.com/curated/<slug>/ | grep 'og:image'`，確認輸出是`https://...`開頭

### 2. 未來的新站也要修（一次性根治）

`scripts/curation_process.py`負責處理新上傳的策展站，目前完全不管og:image是否為絕對路徑。這次只修今晚這12個是治標，**新上傳的店家/活動網站以後還是會重演同樣問題**。

請在`curation_process.py`的處理流程裡加一步：新站index.html寫入`~/github_repos/<slug>/`之後，自動掃描並把og:image（若相對路徑）改寫成絕對網址`https://event.bymyway.com/curated/<slug>/...`；若完全沒有og:標籤，用同一套邏輯補上（title抓`<title>`、description抓第一段有意義的文字或`<meta name="description">`、image抓第一張`<img>`）。

改完寫個小測試（假造一個帶相對og:image的index.html跑一次這個函式，確認變成絕對網址）再commit。

### 3. 刪除12則舊貼文，重貼

12則已經公開（沒縮圖+文案重複那版）需要刪除重貼，不是留著不管：

1. 用你今晚寫好的`scripts/repost_curation_fb.js`同一套Playwright接管Chrome的方法（SOP已經寫好8個坑的解法，照著做）
2. 先手動或用腳本刪除今晚貼的12則舊貼文（FB貼文右上角選單「刪除」）
3. 用你自己SOP裡「文案格式範本」的格式重貼（單一URL一行，不要加圖片URL那行——上一輪已經是重複的元兇之一）
4. 每則貼完，確認：①用Mac Chrome無痕視窗開`facebook.com/大台南策展中心/`看到貼文出現在公開時間軸 ②貼文有縮圖卡片（不是純文字）
5. 12則都貼完+驗證完，回報教練

### 4. 完工回報

做完後：
- 給教練一個簡短總結：改了幾個slug的og:標籤、curation_process.py有沒有加自動修復、12則有沒有全部刪除重貼成功+有縮圖
- commit hash列出來（github_repos底下的12個獨立repo各自的commit + workspace裡curation_process.py的commit）
- 不確定的地方（例如某個slug抓不到合適的圖或描述）誠實列出來問教練，不要用預設值硬套

## 不要做的事

- 不要動FB App Review那個卡住的任務（跟這次無關，教練知道那個還卡著）
- 不要複製整個Chrome profile（你自己的SOP已經寫過這個坑，只複製Cookies檔案就好）
- og:description不要寫得跟og:title一樣的內容，兩個要有區隔（教練這次抱怨的「重複」問題根源就是沒注意到內容重疊）
