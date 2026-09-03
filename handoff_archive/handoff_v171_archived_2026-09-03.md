# 軍師接力棒 · 2026-09-03 v171（聯想Windows Sonnet 5，tut-alumni校友會網站從融合設計到資料庫/API/Telegram全通，含一次效率教訓）

> 建立時間：2026-09-03 01:13 ~ 02:38（台灣時間）
> 上一棒：v170（聯想Windows，9/16活動FB貼文發滿5個粉專，9/5+9/16行銷任務全數結案）
> 本棒主軸：**教練帶兩份AI生成的南應大校友會設計稿要求融合，完成後推GitHub Pages上線；教練接著要求資料庫接手交給Mac，聯想寫信交接；過程中在Google表單/Apps Script的UI自動化死角上死磕過久被教練點名「效率太慢」，教訓已寫入記憶；後來發現Mac已平行完成資料庫+API+Telegram通知全套，聯想採用Mac版本收尾。**

## 🎯 本場戰果

### 1. tut-alumni校友會網頁融合上線
教練提供`design (3).html`(喜歡版型)+`preview.html`(喜歡文案)兩份AI生成設計稿，要求融合5項需求：①Hero文案換成Preview那句「我們曾經在同一個校園裡青春過...」②新增1964~2010母校沿革時間軸③新增「加入不只是留一筆資料」倡議區塊④校友名單合併(Design 8位+Preview不重複的5位，去重3位重複，共13位)⑤加入表單新增5個分會(台南/台中/高雄/台北/嘉義)選項。已用瀏覽器完整測試表單驗證流程，新建GitHub repo`Coach1973/tut-alumni`並開通Pages，`https://coach1973.github.io/tut-alumni/`已curl驗證上線。

### 2. 資料庫工作交接Mac
教練明確裁示「資料庫只能在軍師那邊做」，寫信`cross-agent/inbox/mac/`交接，說明表單目前純前端假成功、需要的5個欄位、GitHub repo位置。

### 3. ⚠️ 效率教訓：同一死角死磕過久，教練訂下3次回報規則
教練接著提供一個真實存在的Google表單連結(南應大校友會官方入會申請)，希望複製一份改介紹文字+接Telegram通知。查證發現無法直接複製別人的viewform連結(需編輯權限)，教練選擇「軍師重建等效新表單」路線。動手時卡在Google表單「必填」自訂開關(六七種點擊/事件模擬手法都點不動)+改用Apps Script程式碼編輯器又踩到中文混打吃掉所有標點符號的怪異行為，兩個技術死角各自磨了十幾分鐘沒有及時停手回報。教練直接點名「效率太慢」「浪費我時間/token/金錢/生命」，並訂下明確規則：**同一個問題試差不多3次不行，就要立刻回報，不能悶頭硬幹**。已寫入記憶`feedback_cap_retries_report_when_stuck_2026-09-03`，跟既有`feedback_exhaust_own_tools_before_asking_coach`是互補的兩面(該自己扛的扛，扛不動的要儘早講)。

### 4. 改道後發現Mac已平行完成，避免重複
放棄Google表單路線，改用「Mac資料庫+既有網頁」方案繼續，準備自己動手接Telegram通知時，查git log發現**Mac軍師已經同步完成**：`event.bymyway.com/tut`動態路由+`/api/tut/join`端點(CORS雙入口)+`tut_alumni_signups`資料表+Telegram通知「活動報名即時通知」群組+導流佩佩老師LINE官方帳號，已用真實POST驗證。聯想這邊也剛好寫了一版GitHub Pages前端串接程式碼，push時發現Mac已推送更完整的同款版本，直接`git reset --hard origin/main`採用Mac版本，避免兩份AI各自重工，已驗證GitHub Pages正式站同步生效。

## ⚠️ 下一場開工先做
1. 跨機信箱仍有1封未讀(ACER 8/31狀態回報)，教練未指示處理，繼續掛著。
2. tut-alumni整體已全通(前端+後端+通知)，教練若有後續修改需求(如校友名單調整、文案微調)直接交辦即可。
3. 這次「Mac跟聯想平行做同一件事」提醒：**日後接到跨機交辦任務、準備動手做「補強/延伸」動作前，先git pull確認對方是否已經處理過**，避免像今天這樣兩邊重工(雖然這次代價不大，只是白寫一版前端程式碼)。

## 🔑 本場commit
`tut-alumni`：`9cf4377`(融合上線)+`ca94ad6`(Mac版接資料庫，聯想reset採用)。`workspace`：跨機信箱交接信+`feedback_cap_retries_report_when_stuck_2026-09-03`記憶。


---
