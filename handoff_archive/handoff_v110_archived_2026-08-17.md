> 封存說明：本檔為 v110 完整內容，2026-08-17 因 JUNSHI_HANDOFF_LATEST.md 只保留最新 2 棒的慣例，被 v112 頂替出主檔，移入封存區保留備查。

# 軍師接力棒 · 2026-08-15 v110（Mac桌面版 Sonnet 5，AI微論壇台中場網頁概念稿+mentor100後台500錯誤修復）

> 建立時間：2026-08-14 17:12 ~ 2026-08-15 18:25（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v109（Mac桌面版 Sonnet 5，官方LINE推播驗證+品牌短網域上線+Cloudflare API Token申請）
> 本棒主軸：**兩條主線。①教練交辦新任務：9/23-24台中場AI微論壇（收費、9位講師）要先做GitHub Pages概念稿來回確認。從0建立`ai-forum-taichung`新repo，比照既有AI微論壇風格但升級優化，經過十餘輪教練逐步調整（套票價格/大樹教練專屬分享主題/場地/議程排序/付款連結/字級/講師照片裁切）逐步定案，講師資料持續從mentor100撈取補齊，最終只剩彭晉澄一位完全查無資料。②教練回報mentor100後台500當機，查證抓到「刪除導師記錄未清理申請名單孤兒外鍵」的真根因，止血+根治雙管齊下，並依教練要求新增後台從未有過的「已發佈改草稿」一鍵切換功能，同時依教練指示重新盤點14位「種子」講師標籤。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 AI微論壇台中場(9/23-24)網頁概念稿：十餘輪迭代定案
教練提供9位講師名單+基本場次資訊，要求先做視覺概念稿在GitHub上來回確認再推正式站。新建`Coach1973/ai-forum-taichung`，GitHub Pages：https://coach1973.github.io/ai-forum-taichung/ 。查證mentor100發現9位裡僅5位有完整資料，其餘4位（林佳伶/王俊甫/彭晉澄/廖韋評）誠實標示「資料籌備中」不瞎編，逐一交代給教練。

教練持續加碼調整，逐輪落實：兩天套票2988元(單日1800，比分開報名省612)；大樹教練除開場/總結外，兩天各安排一場專屬分享（只出一張嘴叫AI做事／如何將AI導入LINE成為你的生活小幫手），且教練主動要求固定排在「下午第一堂最容易犯睏的時段」由自己扛；場地補上沃茲新創空間忠明館（台中市南屯區忠明南路478號B1）；議程從「上午3下午2」改「上午2下午3」；報名費含午餐+下午茶；接上藍新金流付款連結（`core.newebpay.com`），誠實告知教練連結對應金額尚未逐一核對；亮點bar字級歷經兩輪調整（先放大到56/40px，教練回饋電腦版看起來不協調，改成四組說明文字統一字級、以最長文字不換行為準抓出24px）。

期間主動查證並修復兩張講師照片頭部被裁切的問題（施育廷、JC老師原名書銘）——正方形頭像框用cover模式對直式照片預設置中裁切，頭頂距原圖邊緣太近會被切掉，改用`object-position:center top`精準修復，且JC老師這張是主動預防、不等教練回報。

**講師資料補齊進度**：書銘→JC老師（更名+補齊簡介/照片/連結）、林佳伶=Lavi（教練澄清是同一人）、廖韋評（含教練事後更新照片的二次同步）皆已從mentor100完整撈取上線。**王俊甫查證發現mentor100照片其實是Facebook預設空白大頭貼截圖、簡介只有姓名重複**，未採用，同步在mentor100後台改為草稿。**彭晉澄仍完全查無mentor100任何記錄**，是唯一卡住項。commit序列：`d27464b`→`f6b5c5e`→`c2cda50`→`1d4b6d8`→`aa90a9a`→`4d1c48c`→`6ab0649`→`932a652`→`424ac65`→`495546d`。

### 2. 🔴🔴🔴🔴 mentor100後台/admin頁500錯誤：孤兒外鍵根因修復
教練回報`mentor100.bymyway.com/admin`顯示Internal Server Error。查`webapp.error.log`抓到`werkzeug.routing.exceptions.BuildError`，追溯到`templates/admin_list.html`第73行對已刪除的mentor記錄組`url_for('join_edit', token=None)`失敗。根因：`db.delete_mentor()`只執行`DELETE FROM mentors`，沒有同步清理`applications`表指向該id的外鍵——教練先前刪除id69導師後，申請名單裡「Jack Du」那筆記錄變成指向空氣的孤兒引用，模板渲染到那一筆就整頁死。

止血：清空該筆孤兒外鍵資料，立即用真實app物件+資料庫連線完整模擬`render_template()`驗證恢復正常（非僅推論）。根治：①`delete_mentor()`刪除時同步`UPDATE applications SET mentor_id=NULL WHERE mentor_id=?`②模板判斷條件從`not a.mentor_id`改為`not a.edit_token`雙重防護。commit`87031ec`，重啟服務後本機+正式網域皆驗證200/302正常。

### 3. 🟢 後台新增「改為草稿/已發佈」一鍵切換功能
教練指出：某些講師是教練自己先建好資料架子、但講師本人還沒補齊資料，這種情況需要能隨時改回草稿不對外顯示——查證確認`admin_mentor_edit`從未處理過`status`欄位，教練確實沒有任何入口能自己切換發佈狀態。新增`db.toggle_mentor_status()`（CASE WHEN切換published/draft）+新route`/admin/mentors/<id>/toggle-status`+列表頁按鈕（文字依當前狀態動態顯示）。commit`23304df`，已用真實資料庫模擬驗證64筆published正確顯示「改為草稿」、王俊甫(draft)正確顯示「改為已發佈」。

### 4. 🟢 mentor100「種子」標籤依教練指示重新盤點
教練要求：AI微論壇+其他有實際擔任講師的活動才標種子，教練自己手動建的（非講師身份）都不算種子。第一輪只設AI微論壇8位講師為種子，教練隨即澄清王彤/蘇秦/燒茶林祥禔是「7/29的講師」需要保留種子——查證後改為完整盤點三場活動：7/29場3位+8/28嘉義場3位（查ai-talk repo講師陣容比對mentor100 id）+AI微論壇台中場8位，共14位種子，其餘全部改回自助送出。直接改資料庫並用真實模板渲染驗證badge數量正確。

## 📋 下一場直接開工任務
- **AI微論壇概念稿**：問教練GitHub Pages版本整體看過確認沒問題了嗎，確認後才能推正式站（且要問是否要新建bigtree-tw之外的獨立正式網址，或整合進既有大樹小講/AI微論壇品牌）
- **彭晉澄資料**：教練若已取得資料，記得同步更新mentor100+AI微論壇網頁+標記種子
- 「真誠分會」網頁主架構問題：教練仍未說明具體是什麼
- 三機hook同步（Windows/ACER的Claude Code settings.json hook，非OpenClaw gateway hook）：ACER仍待處理
- 報名雙寫觀察期：先問教練bymyway.com新舊系統是否都已確認收到真實報名

## 🔑 本場關鍵檔案索引
- `github_repos/ai-forum-taichung/index.html`：全新9/23-24 AI微論壇台中場概念稿
- `github_repos/mentor100/db.py`：`delete_mentor()`同步清理孤兒外鍵+新增`toggle_mentor_status()`
- `github_repos/mentor100/app.py`：新route`admin_mentor_toggle_status`
- `github_repos/mentor100/templates/admin_list.html`：判斷條件加固+新增切換按鈕
- `github_repos/mentor100/mentors.db`：source(種子)欄位14位重新盤點，直接改資料庫
- commit(ai-forum-taichung)：`d27464b`~`495546d`共10筆
- commit(mentor100)：`87031ec`+`23304df`

