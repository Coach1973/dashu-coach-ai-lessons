# 軍師接力棒 · 2026-09-04 v180（Mac終端機 Sonnet 5，seabiscuit20媒體報導補齊20篇+全面盤點報告+新增「關於創辦人」頁面）

> 建立時間：2026-09-04 19:23 ~ 22:08（台灣時間）
> 上一棒：v179（Mac終端機，seabiscuit20部署四項調整+coach888作品一覽補漏+兩輪真bug修復）
> 本棒主軸：**教練指出seabiscuit20媒體報導篇數不對，查證找到真正官方20篇來源(bigtree/speakers-2026)並補齊；教練委託「一天沒睡前」的全面盤點報告，跨43個repo技術掃描+待辦事項清查；教練交辦新增「關於創辦人」頁面，經過iframe架構查證+3輪教練回饋(頭像被切/間距太大)才定案，全數已推正式站。**

## 🎯 本場戰果

### 1. seabiscuit20「媒體報導」從14篇補齊為官方完整20篇
教練說官網有20篇(4×5排版)但seabiscuit20只有14篇。查證發現真正的官方完整清單其實是`bigtree/speakers-2026/index.html`(8/9建立，非bymyway.com WordPress首頁)，seabiscuit20原本14篇有7篇不在這份官方清單內，缺了7篇官方有的。改用官方20篇清單覆蓋，實測4欄×20張=剛好5排，commit`55876db`。

### 2. 全面盤點報告（教練委託「休息前」的通盤稽核）
背景Agent掃描43個github_repos的git狀態(uncommitted/unpushed)，加上親自查證materials系統(42份教材已上傳但`visible`全部是0，一份都還沒公開)、`true-ai-team`repo從未設遠端(有遺失風險)。報告寫入`knowledges/2026-09-04_全面盤點報告_教練休息前委託.md`，commit`3772f6783`。**過程中一個查證失誤**：curl測`zhenzuan.bymyway.com`/`zhengui.bymyway.com`顯示DNS不解析，誤判「真鑽/真貴還沒部署」，教練糾正後查launchd/cloudflared config才發現真正網址早已改成`real-diamonds.bymyway.com`/`real-wealth.bymyway.com`(命名規則對齊chapters.bymyway.com)，兩個其實都已上線，已更正待辦表(見上方第一列)。

### 3. 新增「關於創辦人」頁面，三輪迭代定案
教練要求把bymyway.com「關於教練」內容原封不動搬到seabiscuit20，附截圖(用生命熱愛教育的演說家+三個身份標籤+創業歷程)。**查證繞了一大圈**：curl查了bymyway.com根目錄/`/about/`/`/coach/`/`/ai/`/`/old/`五個頁面全部搜不到內容(含用claude-in-chrome連教練真實Chrome查證)，教練連續澄清後才想起是iframe嵌入架構——`bymyway.com/coach/`頁面本身只是WordPress殼，真正內容用`<iframe>`嵌入`coach1973.github.io/bymyway-website/`(GitHub Pages)。找到後複製「about」+「timeline」兩個section(關於大樹教練介紹+1997~2025創業歷程17個節點)到seabiscuit20新增`#founder`頁面，三個身份標籤加超連結(俱樂部創辦人→自己首頁/BNI大台南南區執行董事→`chapters.bymyway.com`/AI百人導師計畫召集人→`mentor100.bymyway.com`)，commit`e54124d`。**教練驗收兩輪回饋**：①直式大頭照被當成寬版橫幅背景導致裁切放大變形，改用金色漸層背景取代，commit`540df63`②教練覺得標題橫幅到內文間距太大，乾脆整個拿掉hero橫幅，點進去直接顯示內容，commit`e0f8e28`。三次修改都本機div平衡驗證+正式站curl確認+`open -a "Google Chrome"`開給教練看過才算完成。

## ⚠️ 本場教訓/發現（已寫入記憶+試金石）
1. **bymyway.com找不到內容時要先查`<iframe`標籤，不能只curl文字搜尋**——這個網站至少`/ai-go/`、`/coach/`兩頁是iframe嵌入GitHub Pages，父頁面原始碼裡本來就不會有內容文字。試金石案例71+記憶`feedback_check_iframe_before_text_search_2026-09-04`。教練原話：「這就是你不去查歷史資料、瞎猜的代價...把它汲取教訓，寫在那個世界史檔案裡面」。
2. **查證「網址是否已部署」時，若curl DNS不解析，先確認是不是網址本身命名已變更（查launchd plist/cloudflared config找真實網址），不要直接下結論「還沒做」**——真鑽/真貴的真實網址跟盤點報告裡沿用的舊記錄不一致，教練親口指出「那都已經處理好了」才發現查證方法有漏洞。
3. **教練當天稍早才讀過的記憶檔內容，動手前要主動連結回來用**——`feedback_verify_online_before_answering.md`本場稍早的盤點報告就引用過，裡面已經寫明`/coach/`嵌入`bymyway-website`，但新任務時沒有回頭連結這條線索，繞了一大圈才用翻舊對話逐字稿的方式重新找到同一個答案。

## 📋 下一場開工先做
1. **coach888「已同步」狀態指示器 vs 手動上傳按鈕**，教練仍未回覆選哪個，開工先問。（v179留下，本場未觸及）
2. 「後台系統帳密集中」任務存放位置，教練仍未回覆。（v179留下，本場未觸及）
3. **`true-ai-team`repo要不要補上GitHub遠端**，本場盤點報告發現的新風險項，教練尚未回覆是否還要這個專案。
4. materials系統42份教材待教練自行去`/materials/admin`勾選公開，教練說「現在還顧不上」，非阻塞待辦。
5. bigtree黑金改版的草稿殘留檔案，盤點報告建議清理歸檔，教練尚未回覆要不要動手。

## 🔑 本場commit
`seabiscuit20`：`55876db`(媒體報導補齊20篇)、`e54124d`(新增關於創辦人頁面)、`540df63`(修復大頭照裁切)、`e0f8e28`(拿掉hero橫幅)。`workspace`：`3772f6783`(全面盤點報告)。記憶庫(`.claude/projects`)：`24e0d84ac`(補MEMORY.md索引)、`d55f7931f`+`3818d5895`(試金石案例71+記憶新增)。記憶：`feedback_check_iframe_before_text_search_2026-09-04`。

---

