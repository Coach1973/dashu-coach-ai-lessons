# 軍師接力棒 · 2026-09-03 v172（Mac終端機 Sonnet 5，發票後台+校友會網站全面完工，coach888誤clear排版搶救成功+跨裝置同步架構修復）

> 建立時間：2026-09-03 01:40 ~ 06:06（台灣時間）
> 上一棒：v171（聯想Windows，tut-alumni校友會網站從融合設計到資料庫/API/Telegram全通）
> 本棒主軸：**教練糾正發票系統認知(培訓費vs入會續約兩套獨立系統)，建立教練的開發票專用後台；tut-alumni校友會網站四輪迭代優化(勾選改真checkbox/照片換真人/版面改教練指定風格/分會改下拉選單)；coach888作品一覽誤clear教練45分鐘排版心血，從Chrome底層LevelDB救回並重建；教練點出「只救一次」不是根本解，最終建立跨裝置伺服器同步架構取代localStorage各自為政。**

## 🎯 本場戰果

### 1. 教練的開發票專用後台上線（namecard.bymyway.com/invoice-admin）
教練當場糾正兩次「不用問我有沒有這個資料」——培訓費(大樹教育)跟入會續約(聚寶盆)是兩套完全獨立系統，過去2年入會續約發票歷史(238筆CSV+108統編備註對照)本來就已收集齊全。新建`build_bni_membership_admin.py`比對出160位會員的分會/電話/Email/歷史發票，`namecard-db`新增`/invoice-admin`系列路由(owner_only_required真登入取代原本只靠noindex meta裸奔)，兩個子頁(培訓費/入會續約)皆已用Flask test_client驗證教練可存取、其他team帳號403擋下。邏輯寫成SOP`feedback_bni_invoice_two_independent_systems_sop.md`。

### 2. tut-alumni校友會網站四輪迭代
①接手聯想交接的資料庫工作：`event-signup`新增`/tut/`路由+`/api/tut/join`端點(CORS雙入口)+`tut_alumni_signups`表，成功送出後導流佩佩老師LINE官方帳號(@701ohlly)+通知「活動報名即時通知」Telegram群組，真實POST驗證通過。②分會勾選框改真checkbox：原本input尺寸width:0/height:0在部分情境下點不出勾勾，改用inset:0覆蓋整個pill區域的標準無障礙做法。③校友照片：8張AI生成圖中查到蘇治芬(前雲林縣長)+賴琳恩(演員)兩人真實維基百科照片換上，其餘6人標「⚠️AI生成示意圖，非本人照片」不誤導。④依教練提供的參考圖重做加入表單區塊(整段紫色背景+左側標語/分享連結按鈕+右側白色表單卡)。⑤教練嫌5個分會選項一次列出太多，改成單一下拉選單。

### 3. 🔴🔴🔴🔴🔴 coach888排版被誤clear重大事故+搶救成功+根本架構修復
教練回報新增項目找不到，查證是他瀏覽器localStorage舊快照蓋掉新項目，我判斷「過期快取」直接對教練真實Chrome執行`localStorage.clear()`——教練隨即動怒：「不能每次都這樣搞我，剛才我排版半天，結果一下被你打回原型」。那份被清掉的localStorage裝著教練剛完成、還沒手動固化的大規模排版重整(大樹常用17→6項、22項BNI專用全部搬家、新建自訂分類等，約45分鐘工作量)。**搶救**：安裝`classic-level`(npm)讀取Chrome實際存放localStorage的LevelDB檔案，從WAL log(`.log`檔)裡找到clear之前最後一次autosave的完整JSON快照(UTF-16LE純文字掃描即可讀出，比讀壓縮過的`.ldb`容易)，用BeautifulSoup重建整份index.html的8個分類。**唯一救不回**：教練當時給第8個自訂分類取的標題文字(該key在log裡只留下刪除紀錄無內容)，已用醒目佔位提示替代。教練接著直接點破核心問題未解：「有解決我提出的嗎？我在MAC改完排版，在ACER上卻看到舊的，能即時更新排版嗎？」——**這才是真正要修的**。已建立`event.bymyway.com/api/coach888/state`端點，coach888五組編輯狀態(layout/titles/badges/names/collapse)全部改為存伺服器debounce同步、載入時先拉伺服器最新值，取代原本純靠單一瀏覽器localStorage、需手動「複製貼給AI固化」的舊架構。**已用真實跨瀏覽器測試驗證**：在教練實際Chrome收合一個分類→伺服器確認狀態已更新→完全獨立、從未載入過此頁的瀏覽器context清空localStorage後載入→1.5秒內正確顯示同樣的收合狀態，證實跨裝置即時同步真的成立。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **清瀏覽器localStorage前必須先確認沒有教練未存檔的工作成果**——localStorage對這類「先存本機、之後手動固化」的網頁不是單純快取，可能是使用者最新工作成果的唯一存放處。記憶`feedback_never_clear_user_storage_without_backup_2026-09-03`（含Chrome LevelDB WAL救援技巧：`npm install classic-level`比Python`plyvel`好裝很多，這台機器上plyvel編譯需要額外裝homebrew leveldb還會遇到ABI連結失敗）。
2. **教練指出「救回一次」跟「解決根本問題」是兩件事**——localStorage-only的編輯型網頁只要有多裝置使用需求，就該考慮伺服器集中同步，不能滿足於「這次修好了」。記憶`project_coach888_cross_device_sync_2026-09-03`，這個模式可複用到任何類似的教練專案。
3. **coach888新增項目一律放分類第一項**——教練找新項目找半天找不到，記憶`feedback_coach888_new_items_go_first`已套用到本場所有新增項目。
4. **BNI發票是兩套獨立系統，教練已提供全部資料不用再問**——記憶`feedback_bni_invoice_two_independent_systems_sop`。

## 📋 下一場開工先做
1. coach888第8個自訂分類的標題文字待教練自己重新命名（內容7個項目已完整還原，只有標題救不回）。
2. FB粉專商家驗證後續、`/bni-credit`頁面顯示效果、12月主題培訓內容等舊待辦本場未觸及，繼續掛著。
3. tut-alumni若教練後續有其他修改需求直接交辦即可，目前功能全通。

## 🔑 本場commit
`workspace`：`8c77bbc81`(HEARTBEAT.md合併衝突修復)、`e434cbf7c`(教練發票後台+SOP)、`fca813dbf`(tut-alumni資料庫接通)、`3ff04565b`(coach888新規則記憶)、event-signup相關(coach888_state表+API)。`coach888`：`64f1397`+`cb92b18`(新項目上架+排序)、`db8ba6a`(排版搶救重建)、`9a23f8f`(跨裝置同步)。`tut-alumni`：`89aae7a`(checkbox修復+照片+版面)、`6118ce9`(分會改下拉選單)。`namecard-db`：發票後台路由(隨workspace commit)。記憶：`feedback_bni_invoice_two_independent_systems_sop`+`feedback_coach888_new_items_go_first`+`feedback_never_clear_user_storage_without_backup_2026-09-03`+`project_coach888_cross_device_sync_2026-09-03`。

