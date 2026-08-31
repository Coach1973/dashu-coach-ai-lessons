# 軍師接力棒 · 2026-08-30 v152（Mac終端機 Sonnet 5，逐步脫離Netlify：4個新路由+3處連動+作品總覽更新）

> 建立時間：2026-08-30 14:26 ~ 18:56（台灣時間，接續v150同一天新對話框，因context overflow於14:26自動重啟）
> 上一棒：v150（Mac終端機，同日較早，真誠分會邀約來賓重複建置根因查明+移除+5位會員專屬編輯網址交付）
> 本棒主軸：**教練拍板方向——大樹小講/AI微論壇/紅綠燈看板/培訓行事曆改成event.bymyway.com即時渲染，逐步脫離Netlify部署次數限制，並同步更新所有引用這些連結的地方。**

## 🎯 本場戰果

### 1. 大樹小講9/22台南場「下午」時段修改（session時間+移除點心飲料文案）
教練口頭指示：9/22台南場下午時段改13:30-16:30、拿掉「附點心飲料」文案。借用bigtree既有但未使用的`下午`slot(13:30-16:30，跟`午半`14:00-16:30區隔，不影響同用`午半`的9/5 KR養生廚房場次)，同步更新`event.db`。commit`f8ac8fc`（bigtree repo）。

### 2. 大樹小講/AI微論壇/培訓行事曆/紅綠燈看板改event.bymyway.com即時渲染上線
教練確認方向：先兩邊(Netlify+bymyway)同步，穩定後才退場Netlify。技術核心：`event-signup`既有Flask app新增路由，請求當下直接讀取各自github repo原始檔案渲染，大樹小講額外疊上`event.db`即時場次資料(沿用`bigtree_publish.py`既有`read_sessions`/`render_session_dates`函式)，完全不需要「發佈」動作。網址命名邏輯（教練拍板）：**網址代表活動格式/系列，不代表地點**——跟`ai-talk-tw.netlify.app`過去台南→嘉義直接覆寫同網址同一套邏輯。上線4條路由：
- `/bigtree/`（大樹小講，DB即時渲染）
- `/ai-forum/`（兩天制系列，現為台中場9/23-24，之後10/7-8台南場沿用同網址；教練原本要求`/ai-forum-taichung`後又親自糾正改成無地名的`/ai-forum`）
- `/ai-talk/`（半天制系列，現仍8/28嘉義場內容，等教練補齊凌榆舜/李明燦兩位講師資料後改9/22台南場，設攤/贊助商區塊維持不動）
- `/tainan-calender/`（純靜態，沿用既有拼法不改calendar）
- `/bni-traffic/`（紅綠燈看板，純client端Excel解析工具，零風險）

全部路由均：本機另開測試埠驗證→真實Chrome開過→重啟正式服務`com.coach.event-webapp`→在`event.bymyway.com`公開網址再驗證一次→確認其餘既有路由(`/admin`等)無回歸，才commit。commit`f8ac8fc`+`3df06cab7`+`fc58dc783`+`7d4b1e5e9`（event-signup，皆workspace repo）。

### 3. 三處連動同步更新
①`bni-chapters`資料庫`chapter_links`表：9分會×2種連結(紅綠燈看板/培訓行事曆)共18筆改新網址，重啟服務後在`chapters.bymyway.com/real-ai`公開頁curl驗證連結已更新。②`bni_tainan`小幫手：`AGENTS.md`4處member-facing連結+`knowledge/tainan_calendar.md`來源引用+`scripts/sync_calendar.py`實際抓取來源全部改新網址，**過程中發現`event.bymyway.com`前面的Cloudflare會擋掉urllib預設User-Agent(403)**，已補上`Mozilla/5.0`headers修復，重跑驗證106筆活動正常同步。commit`5fabb60d`（外層`.openclaw`repo，agents/bni_tainan路徑）。③`coach888`作品總覽：新增「bymyway自架版」區塊列出5個新路由(綠色badge)，對應5個Netlify舊版項目標「待退場」(橘色badge)，一眼可辨識新舊。教練追加要求把此區塊從第七移到第三順位，其餘區塊依序順延，已完成並在GitHub Pages正式站curl驗證順序正確。commit`230d735`+`cafe1f4`（coach888 repo，GitHub Pages自動部署免確認）。

## ⚠️ 本場教訓/發現（已寫入記憶）

1. **`event.bymyway.com`前面的Cloudflare會擋掉沒有瀏覽器樣式User-Agent的請求(403)**——`sync_calendar.py`改抓自家bymyway網址時直接403，curl實測`-A "Python-urllib/3.11"`→403、`-A "Mozilla/5.0"`→200證實是UA被擋非內容問題。任何腳本要fetch`*.bymyway.com`子網域都要注意這點，已寫入記憶`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。
2. **這套「讀活repo+DB即時渲染」模式的核心價值不只是「另一種不受限的部署方式」，是讓這類小改動(改時間/改文案)根本不需要「部署」這個動作**——editing DB或repo原始碼立刻反映，這點在跟教練說明時比單純講「省Netlify額度」更能讓他理解價值所在。
3. **新增自架服務時優先掛在既有已有launchd看護的Flask app底下(本場全部掛`event-signup`)，不新增獨立子網域/Tunnel/launchd**——降低「服務被遺忘」風險（呼應`peipei-event`斷線5天、ACER 49天未開機兩個舊案例的同一種病根：服務越分散越容易有一個沒人顧到）。

## 📋 下一場開工先做
1. **待教練提供**：凌榆舜/李明燦兩位講師的職稱/講題/簡介/照片（mentor100查證確認兩人都不在資料庫），到齊後把`/ai-talk`一次改成9/22台南場正式內容上線。
2. 教練提到「跟BNI相關的把netlify裡面我常常有在用的都變成event.bymyway.com」——目前只確認並處理了紅綠燈看板+培訓行事曆兩個，`路徑大全.md`裡的GitHub作品總表把`bni-traffic`歸類「早期練習」已證實是過時分類，若教練心裡還有其他常用的BNI相關Netlify站台，等他指名再處理，不用自己瞎猜逐一嘗試舊站台。
3. FB粉專商家驗證後續（舊待辦，v147/v148/v150留下，本場未觸及）。
4. `/bni-credit`補公司欄位：2026-09-02教練有額度時的舊待辦，本場未觸及。
5. 「釋放記憶體」白名單範圍：v148留下，本場未觸及。

## 🔑 本場commit
`bigtree`：`f8ac8fc`（9/22時段+文案修改）。`event-signup`（workspace repo內）：`f8ac8fc`~`7d4b1e5e9`區間共4筆（新增4條bymyway路由）。`.openclaw`外層repo：`5fabb60d`（bni_tainan agent連結更新）。`coach888`：`230d735`+`cafe1f4`（作品總覽新增區塊+順序調整）。記憶：`project_bymyway_dynamic_hosting_escape_netlify_2026-08-30`+`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。
