# 軍師接力棒 · 2026-09-11 v194（Mac桌面版 Sonnet 5，FB App Review深挖翻案+一鍵發布API上線+claude-in-chrome連錯裝置第5次發作根治）

> 建立時間：2026-09-11 10:40 ~ 12:28（台灣時間）
> 上一棒：v193（聯想Windows，FB粉專發文致命發現：App未過Review訪客看不到貼文，教練當時裁示放棄App Review改人工重貼）
> 本棒主軸：**教練追問「真的無解嗎」，深挖後推翻v193「放棄App Review」的裁示——用登出瀏覽器實測證明限制是App層級(不分粉專)、查到商業驗證早已完成、找到Tech Provider真正觸發條件，教練決定親自申請，目前卡在應用程式檢閱表單。同場也完成教練要求的「其他網站比照大台南商圈計畫不用經Mac即可更新」需求，以及claude-in-chrome第5次連錯裝置(連到聯想Windows教練看不到畫面)的根治。**

## 🎯 本場戰果

### 1. FB App Review深度翻案：查到3個關鍵事實，教練決定不放棄改親自申請
v193教練裁示「放棄App Review」，本場教練追問細節，深挖後發現：①用完全登出的瀏覽器交叉測試`大樹教練`/`海餅乾俱樂部`/`K R養生廚房`/`大台南策展中心`四個不同分類粉專，皆看到Facebook「目前無法查看此內容」——**證實限制是App層級、對14個粉專一視同仁，不是教練誤以為的「大樹教練是商業帳戶才被限制」**②大台南策展中心策展SOP自動上架通知(至少15篇店家上線通知)同樣受影響，尚未問教練是否要重貼③查到「Tech Provider」不可逆合約只在App「業務用途」設為「提供服務給其他企業」才觸發，教練只管自己粉專理論上可避開，但Meta Business Suite/App Dashboard介面上實際測試發現**這個特定的`pages_manage_posts`權限申請流程仍然要求先確認Tech Provider身份**（這點跟一般網路資料有出入，已用真實畫面驗證修正）④**意外發現商業驗證(Business Verification)其實早在2026-08-31就已完成**（BIG TREE EDUCATION CONSULTANT INC.），不用重新走文件審核。教練親自點擊確認Tech Provider（本人按下，不可逆），已進到「應用程式檢閱提交內容」頁面，7個權限已列入新申請。軍師新建隱私政策頁`event.bymyway.com/privacy-policy/fb-poster-app`(commit`ce4854802`)供表單「隱私政策網址」欄位使用，教練已填入。**下一棒待辦**：確認教練是否已填完其餘必填欄位(App圖示/顯示名稱)，最終「提交檢閱」不可逆需再次跟教練確認才能送出。

### 2. 一鍵發布API上線：event.bymyway.com/<slug>/系列21個網站不用經Mac即可更新
教練問「能不能比照大台南商圈計畫，其他網站不用經過Mac就能更新」，查明根因：這些網站讀活repo（Lenovo/ACER推送都算），但Mac讀的是本機clone，缺`git pull`這一步，跟大台南商圈計畫(內容寫DB、POST當下即生效)架構不同。新增`GET/POST /api/site-update/<repo_name>?key=<SITE_SYNC_KEY>`端點，做`git pull --ff-only`+回傳commit hash，21個已知repo白名單，已用真實HTTP請求驗證(錯誤key拒絕/正確key成功pull/未知repo回傳清單提示)。commit`4ed93a931`(event-signup)，SOUL.md補上教學(commit同批)，Hermes專屬H_HANDOFF也已同步交辦(`b289586`，hermes-h-workspace repo)。往後教練貼網址+說「請發布」，小龍蝦/Hermes可直接觸發，不用等軍師。

### 3. claude-in-chrome第5次連錯裝置：教練重話後根治，改成不用再問
早上處理FB貼文重貼時，Mac軍師session一開始沒選裝置就直接操作，連到了聯想Windows的Chrome（教練根本看不到畫面），連續點擊「沒反應」浪費教練一早上。教練重話：「拜託你可不可以以後不要再問了？永遠不要再問了。」查`list_connected_browsers`確認這台Mac的deviceId(`91bc8312-ebdc-4dcd-9df8-d25d6b1ac83d`)，已寫入記憶`feedback_claude_in_chrome_wrong_device`：往後任何claude-in-chrome任務第一步直接`select_browser`鎖定這個deviceId，不呼叫`list_connected_browsers`(會觸發強制詢問)，不用再問教練。

### 4. FB貼文重貼進度
9/16高雄場正式版一篇已用教練真實登入的Meta Business Suite手動重貼成功，並用完全登出的瀏覽器驗證確認一般人真的看得到。9/23-24台中場AI微論壇教練決定自己動手貼（軍師打字自動化多次失敗，圖片檔案已備妥於`/tmp/fb_repost_20260911/1_ai_forum_taichung.jpg`）。教練裁示「只貼有效貼文即可」，KR養生廚房返場+9/16舊版兩篇已過期，不用管。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **教練登入自己粉專永遠看得到任何貼文，不能拿來當「一般訪客也看得到」的證據**——Page擁有者的瀏覽權限是獨立通道，唯一可靠驗證法是用完全登出的瀏覽器或請無關的人測試。已補進`reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11`。
2. **claude-in-chrome連線裝置問題（第5次以上發作）**：往後這台Mac固定用deviceId`91bc8312-ebdc-4dcd-9df8-d25d6b1ac83d`，任務一開始就`select_browser`鎖定，不要等出問題才回頭查。
3. **Meta Business Suite的貼文編輯器contentEditable偶發性無法正確聚焦，導致type動作沒有真的寫入DOM**（同一組操作步驟時好時壞），這是本場唯一沒解決的技術債，教練最終選擇自己動手貼。

## 📋 下一場開工先做
1. **確認FB App Review表單進度**：教練是否已填完其餘欄位，最終「提交檢閱」需再次確認才能送出（不可逆）。
2. **大台南策展中心15篇店家上線通知**：問教練是否也要重貼。
3. 沿用v190/v192/v193既有待辦：BNI Connect打勾確認出席、更新BNI培訓總覽資料庫、張育慈統編待查、Amber TimeMachine清理、MEMORY.md索引瘦身、後台帳密清單、materials系統42份教材待勾選、跨機信箱一封來自Mac的未讀信（聯想v193留下）。
4. E16接力棒瘦身：本次已把v190搬進`handoff_archive/`，主檔維持v192+v193+v194三棒（略超過建議的1~2棒，下次開工先瘦身）。

## 🔑 本場commit
`event-signup`：`4ed93a931`(一鍵發布API)、`ce4854802`(隱私政策頁)。`SOUL.md`同批commit。`hermes-h-workspace`：`b289586`。`workspace`：`c658c04ba`(接力棒過期訊息修復,誤報ACER案例)、`4b4c8e16a`(待辦表過期偵測機制)、`ab76aba54`(FB App Review根因深挖記憶補充)、`1f388dc14`(coach888稽核基準線補登)。記憶：`reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11`(更新)、`feedback_claude_in_chrome_wrong_device`(更新，補第5次發作+deviceId)。

---

# 軍師接力棒 · 2026-09-11 v195（Mac桌面版 Sonnet 5，FB App Review表單填寫：圖示透明背景修復+權限精簡建議）

> 建立時間：2026-09-11 14:31 ~ 15:52（台灣時間）
> 上一棒：v194（Mac桌面版，FB App Review深挖翻案+一鍵發布API+claude-in-chrome裝置問題根治）
> 本棒主軸：**接續v194的App Review表單填寫，解決App圖示白底被拒問題，並發現7個申請權限裡有3個App實際沒在用，建議教練移除避免拖累整包審核。**

## 🎯 本場戰果

### 1. App圖示上傳卡在「偵測到白色背景」錯誤，已修復
教練上傳`bigtree_logo_1024(1).jpg`被Meta拒絕，錯誤訊息要求透明背景。查明根因：**該檔案是JPG格式，JPG格式本身不支援透明度**，不管圖案多乾淨都一定會判定成白底。用Python PIL對原圖做flood-fill去背（只清除連通的外部白色背景，不誤傷logo內部設計），輸出透明PNG，用不同顏色背景合成驗證確認去背乾淨無白邊/鋸齒。已放在桌面`大樹教練圖示_透明背景.png`供教練自己上傳（嘗試多種自動化路徑失敗：Meta這個上傳元件用新式File System Access API，DOM裡沒有傳統`<input type=file>`可操作，且該頁面CSP擋掉跨網域fetch，data URI覆寫`showOpenFilePicker`也因payload過大+CSP雙重卡關，最終判斷教練親自點2下最快，已誠實跟教練說明技術限制非偷懶不做）。教練已成功上傳，「應用程式設定」步驟完成。

### 2. 🔴重要發現：7個申請權限裡有3個App實際沒在用，建議移除
查`fb_automation/*.py`+`curation_process.py`實際呼叫的Graph API端點，只用到`/feed`+`/photos`（純發文字/圖片貼文）。但App Review表單裡列了7個權限：`pages_manage_posts`/`pages_show_list`/`pages_manage_metadata`/`pages_messaging`/`business_management`/`pages_read_engagement`/`public_profile`——後三個裡的**`pages_manage_metadata`（粉專設定/webhook）、`pages_messaging`（Messenger）、`business_management`（企業管理平台API）App完全沒有對應功能**，這3個推測是選「管理粉絲專頁的所有內容」這個大分類時被自動打包進去的，不是刻意申請。每個權限都要求上傳「示範操作」錄影，這3個根本錄不出真實畫面。已建議教練移除，避免審核員發現「申請的權限沒在用」導致整包退回，連真正需要的`pages_manage_posts`一起卡住。**教練尚未答覆是否移除**。

### 3. 已代填pages_manage_posts的使用說明文字，其餘待續
在表單textarea裡打好`pages_manage_posts`權限的英文使用說明（誠實描述：僅供教練本人管理自己約14個粉專發文，不涉第三方，好處是省去逐一登入手動貼文的時間），已用JS驗證字數(948字元)確認真的寫入。`pages_show_list`/`pages_read_engagement`的說明文字尚未寫，是下一棒待辦。API測試呼叫這項`pages_manage_posts`已顯示「已完成」（今天查證過程中用這個App的憑證打的真實API呼叫算數）。

## ⚠️ 本場教訓/發現（已寫入記憶，待補commit）
1. **JPG格式本身不支援透明背景，不管圖案設計多乾淨，只要副檔名是.jpg一定會有實心白底**——遇到「請用透明背景」類錯誤，先檢查副檔名，不用懷疑圖片本身乾不乾淨。
2. **Meta新版上傳元件（App圖示等）用File System Access API而非傳統`<input type=file>`，claude-in-chrome的file_upload工具無法直接操作，且該頁面CSP會擋掉自製的跨網域fetch/覆寫技巧**——這類卡點目前唯一可靠解法是請教練本人點擊，已誠實說明技術限制，不硬拗。
3. **申請App Review權限前，應先比對App實際呼叫的Graph API端點，只申請真正用到的權限**——多餘的權限不只是浪費工，錄不出真實示範影片還會拖累整包審核被拒。

## 📋 下一場開工先做
1. **確認教練是否同意移除3個沒用到的權限**（pages_manage_metadata/pages_messaging/business_management），同意的話操作移除。
2. 續寫`pages_show_list`+`pages_read_engagement`的使用說明文字。
3. 教練需要自己錄製各權限的操作示範螢幕錄影並上傳（軍師無法代勞，需要真人操作畫面）。
4. 每個權限的「我同意遵守允許的使用方式」勾選框，教練親自確認勾選。
5. 沿用v194既有待辦：大台南策展中心15篇店家上線通知是否要重貼、BNI Connect打勾出席、更新BNI培訓總覽資料庫、Amber TimeMachine清理、MEMORY.md索引瘦身、後台帳密清單、materials系統42份教材待勾選。
6. E16接力棒瘦身：目前v192+v193+v194+v195四棒略多，下次開工先瘦身封存最舊的v192。

## 🔑 本場commit
本場為表單填寫+除錯過程，未產生新commit（App圖示PNG在教練本機桌面，非git追蹤範圍；未新增/修改程式碼）。

