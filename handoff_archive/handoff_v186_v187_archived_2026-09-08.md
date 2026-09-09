> 封存原因：E16接力棒瘦身鐵律，主檔只留最新1~2棒，2026-09-08收工時搬移

# 軍師接力棒 · 2026-09-06 v186（Mac桌面版 Sonnet 5，牛市町上架驗收+策展SOP兩項根因修復：slug命名+暫代頁自動偵測讓上傳網址統一取代手動七步驟）

> 建立時間：2026-09-06 03:47 ~ 04:10（台灣時間）
> 上一棒：v185（Mac桌面版，MiniMax過載hook+策展中心通知漏洞修復+VPS真實用途查證）
> 本棒主軸：**教練驗收「牛市町」策展上架案例時追問到底，連續推動兩項架構修正：slug命名根因(整句標題轉拼音→只取品牌名)+暫代頁自動偵測(讓curation/upload端點對所有店家都安全)，最終撤回「有能力AI要手動做七步驟」規則，SOUL.md/Hermes/SOP三處同步統一改為一律上傳網址。教練同場釐清token消耗歸屬(背景處理零token/觸發動作的執行者模型才決定耗誰的額度)，週配額到90%後裁示今日收工。**

## 🎯 本場戰果

### 1. 「牛市町」上架驗收+slug命名根因修復
教練確認上傳流程可行後，指出網址`niu-shi-ting-zhi-zhang-bu-die-de-mei-wei-pin-pai-li-nian`太長。查明根因：`slugify_title()`把`<title>`標籤整句（含行銷標語）轉拼音。修法：新增`primary_title_segment()`只取分隔符號（｜/—/：等）前的品牌名稱去轉拼音。已手動改名既有案例（GitHub repo改名+本機資料夾+registry+tainan-shangquan卡片連結全部同步，新網址`event.bymyway.com/curated/niu-shi-ting/`curl驗證200），並修好`curation_process.py`原始邏輯，commit`82b7a2a2c`。

### 2. 暫代頁自動偵測：讓上傳網址對所有情況都安全
教練追問「牛市町案例比Hermes還快，為什麼不乾脆都走上傳網址」，點出舊規則（有終端機能力的AI要手動判斷有無暫代頁）的存在理由——上傳端點原本不會判斷店家是否已有`shops.bymyway.com`暫代頁，會誤建重複站。已寫進`curation_process.py`：新增`find_existing_shop_slug()`(比對品牌名拼音vs `_shops_slugs.json`既有記錄)+`overwrite_shop_placeholder()`(tar打包+SCP遠端解壓覆蓋，網址不變)，查無記錄才走全新GitHub Pages流程。**已用真實SCP測試驗證覆蓋機制(含assets子資料夾)，測試殘留已清除確認404**，commit`4de7aeb3c`。

### 3. 撤回「有能力AI要手動做」規則，三處同步統一
暫代頁判斷自動化後，手動七步驟規則的存在理由消失。已更新：①`SOUL.md`小龍蝦指示改成「一律curl上傳，不用自己建站」②`~/.hermes/workspace/H_HANDOFF_LATEST.md`寫新的最上層通知給Hermes，撤回00:33/00:50兩則舊指示③`claude-brain/reference_curation_sop_2026-09-06.md`規則一改寫定案。**查證確認`curation-prompt.md`（策展一鍵注入實際複製文字）從一開始就只寫「上傳就好」，不需要修改，此點有實際讀檔驗證非假設**。commit：workspace`3df878f1a`、hermes repo`3d91d8e`。

### 4. 教練提問澄清：權限範圍、token消耗歸屬、機器無關性
- 上傳網址權限：查證`app.py`程式碼確認`key`參數等同繞過登入，沒有IP/次數/期限限制，跟後台主密碼分開設計(外流風險有限，已跟教練說明可隨時換key)。
- token消耗歸屬：背景處理(`curation_process.py`)全程零AI呼叫(純Python+API)，任何AI/機器觸發都一樣零消耗；但「觸發上傳」這個動作本身的token算在誰頭上，取決於執行的AI底層模型——小龍蝦/Hermes是MiniMax(不動Claude配額)，我自己(Claude桌面版/軍師)是Claude/Sonnet(會動用配額，雖然量很小)。已更新記憶`project_claude_quota_conservation_until_wednesday_2026-09-06`補充這個具體案例。
- 機器無關性：Mac/聯想/宏碁執行curl上傳這個動作，結果完全一樣，因為只是打一個公開網址的HTTP請求，跟哪台實體機器發出無關；真正決定要用誰配額的是「哪個AI/哪個模型」在觸發，不是「哪台電腦」。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **SOP規則的生命週期可能很短**——昨晚才訂的「有能力AI要手動做」規則，今晚因為背景自動化補強，存在理由就消失了，該立刻撤回而非讓舊規則繼續誤導執行者。
2. **判斷「AI要不要自己動手 vs 用自動化捷徑」，優先問「捷徑功能不足的地方能不能直接補進自動化本身」**，而不是預設「手動比較保險」——把判斷邏輯內建進系統一次，比每個AI各自判斷更省資源更一致。
3. **「動作簡不簡單」不是決定要不要轉給小龍蝦/Hermes的標準，「誰在執行、燒誰的token」才是**——一行curl指令自己做看似無傷大雅，但只要是我(Claude)執行就是在燒教練的稀缺配額，這類任務應優先問「能不能讓小龍蝦/Hermes做」。

## 📋 下一場開工先做
1. **MEMORY.md索引已達20.2KB接近24.4KB讀取上限**，收到系統提示要求瘦身到17.1KB以下，本場因教練要收工未處理，下一場找時間做（合併/移除過時條目，細節搬進主題檔）。
2. 沿用v184/v185待辦：「後台系統帳密集中」清單未建置、materials系統42份教材待勾選公開、VPS是否承接event.bymyway.com服務防斷電（教練未決定）。
3. 遵守週配額保守策略：到2026-09-11(週三)前，任務先問能不能轉小龍蝦/Hermes。

## 🔑 本場commit
`workspace`：`82b7a2a2c`(slug命名根因修復)、`4de7aeb3c`(暫代頁自動偵測)、`3df878f1a`(SOUL.md+SOP規則一定案)。`niu-shi-ting`(GitHub repo)：改名+remote更新(無新commit，純repo/資料夾更名)。`tainan-shangquan`：卡片連結更新(隨牛市町改名commit)。`hermes workspace`：`3d91d8e`(H_HANDOFF更新)。記憶：`reference_curation_sop_placeholder_autodetect_and_slug_fix_2026-09-06`(新增)、`project_claude_quota_conservation_until_wednesday_2026-09-06`(補充token歸屬案例)。

---

# 軍師接力棒 · 2026-09-06 v187（Mac桌面版 Sonnet 5，教練後台帳密統一改手機號碼+策展網址改短根因修復+coach888收錄機制徹底翻修）

> 建立時間：2026-09-06 05:38 ~ 07:57（台灣時間）
> 上一棒：v186（Mac桌面版，牛市町上架驗收+策展SOP兩項根因修復）
> 本棒主軸：**修復Hermes停擺；建密碼保護的「教練專屬後台密碼總覽」(vault)+6個後台帳號統一改教練手機號碼登入；教練否決策展改短網址的redirect補救方案，改成上傳當下強制輸入短網址(源頭解決)+用Graph API編輯修正5則FB貼文舊網址；新增「大台南商圈整合計劃」後台管理頁讓教練自己下架已上架店家；coach888收錄機制因教練連續4次「找不到」徹底翻修——從「commit訊息措辭比對」改成「直接讀程式碼路由結構性比對」，跟文字寫法完全脫鉤。**

## 🎯 本場戰果

### 1. Hermes停擺修復
四個launchd服務(gateway/desktop/menubar/config-watcher)被`launchctl bootout`關閉未重啟，逐一`bootstrap`拉回，確認程序正常運作。

### 2. 教練專屬後台密碼總覽(vault)上線+6個後台統一帳號
教練反映在其他電腦登不進去多個後台，查證根因非裝置限制，是9個系統各自用不同帳號名稱(bymyway/Admin/RPL)。教練提供手機號碼(`0901056777`)後：①統一改event.bymyway.com/admin、namecard.bymyway.com三系統(team_members表)、chapters.bymyway.com超級管理員、mentor100.bymyway.com、team.bymyway.com超級管理員共6個後台帳號為手機號碼+`88888`，逐一curl驗證登入成功②新增`event.bymyway.com/vault`密碼保護頁(帳號`bymyway`/密碼`123457`)，列出全部11個系統網址+帳密，教練自己就能查不用問AI③查證發現`路徑大全_憑證層.md`原本完全漏記`team.bymyway.com`通用分會系統，已補上④查證`rpl-workshop.bymyway.com`其實2026-08-27已改免登入，本檔記錄過時已修正。**過程修復真bug**：`namecard-db/app.py`有獨立寫死的`OWNER_USERNAME = "bymyway"`常數，跟資料庫分開維護，改密碼時漏改導致教練登入成功卻被「僅限教練本人查看」擋下，已修復並用claude-in-chrome實際登入驗證。commit`a874e32fb`+`b76b47287`+`30cc828a7`(修復)+`fcfc084c2`(vault上線)。

### 3. 策展網址改短：教練否決redirect方案，改源頭強制輸入短網址
教練連續4次要求把自動上架的過長網址改短，發現改名後FB貼文/策展中心舊連結全部失效。第一版修復用「舊網址301轉址到新網址」的redirect機制，教練當場否決：「明明就是一個錯的網址，還要轉址，我覺得很費勁，比較喜歡從源頭解決」。改為：①`curation/upload`上傳表單新增**必填**「自訂短網址」欄位，送出前教練/夥伴自己決定，伺服器驗證格式+查重複，`process_one()`優先採用②`curation-prompt.md`+`SOUL.md`+Hermes `H_HANDOFF_LATEST.md`三處同步更新curl指令加`-F custom_slug=`③用Graph API編輯(非刪除重貼)修正5則FB貼文(bai-sheng/yang-shang-ru/zhang-teng-wen/yang-zai-zhen/niu-shi-ting)的舊網址文字，逐一驗證生效，保留原貼文互動紀錄。**redirect機制保留當zero-cost安全網，不刪除**。過程中測試custom_slug功能時失手觸發完整正式流程(真建GitHub repo+真發FB貼文+真插店家卡片)，已清乾淨(FB測試貼文刪除、GitHub repo改名封存、tainan-shangquan測試卡片移除、Telegram群組發更正說明)。commit`48fabb5e1`。

### 4. 「大台南商圈整合計劃」後台管理頁上線
教練要求：已上架店家有些資料有誤/不想要，要能自己登入刪除不用每次找軍師。新增`event.bymyway.com/curation/admin`(沿用/admin登入)，列出所有已上架店家+下架按鈕，下架會自動：registry移除+策展中心卡片同步拔掉+本機資料夾封存(只搬不刪)+GitHub repo關Pages改名封存。陳佩君老師誤上架網站已依此流程下架驗證。commit`d833a1d66`。

### 5. coach888收錄機制翻修（教練今晚連續4次「找不到/有沒有收錄」後徹底重做）
教練逐一發現：「大台南商圈整合計劃後台」漏放、「策展上傳網址」放錯分類(卡在教練不會點的「保留」分類)、vault頁面本身也沒收錄。修復分三層：
1. **查明Stop hook規則L2從建立起就完全失效**：規則沿用L1的heredoc排除邏輯把含`<<'EOF'`的commit指令整段跳過，但commit訊息一律用heredoc是系統規定寫法，等於規則對100%正常commit從未真正檢查過；就算不跳過，`-m後緊接引號+新增`的anchor也跟heredoc格式對不上。已修復並用當晚實際commit指令重新測試驗證有效。
2. **升級檢查標準**：從「這個名字有沒有出現在檔案任何角落」改成「只認『大樹常用』『後臺系統』兩個教練實際會看的分類才算真的收錄」，放進「保留」等其他分類一律視同沒收錄——這才是錯誤一直複製自己的真正原因（隨便塞進哪裡都能通過舊檢查）。已搬移curation/admin、curation/upload、curation-inject、vault共4個項目到正確分類。
3. **新增結構性稽核**(`scripts/audit_coach888_coverage.py`)：直接掃`event-signup/app.py`真實`@app.route`清單比對coach888，完全不依賴commit訊息措辭。一次掃出過去累積18處落差，排除客戶店家網站(改規則歸tainan-shangquan)+QR操作頁(寫入`coach888_audit_baseline.txt`基準線)後收斂到4個已知合理保留項目。已接進Stop hook規則M，每輪無條件執行，只有超出baseline的「新」缺漏才擋收工。用模擬測試驗證機制真的會擋不是裝飾。

commit：`c88d8783b`(規則L2修復)+`c2c7ccf52`(新增規則M結構性稽核)+`409ea36`/`3fa9088`/`3f8b140`(coach888 repo，分類搬移)。

### 6. 其他
- 教練詢問zhang-teng-wen網址更新流程：確認正確做法是先用curation/admin下架、再重新上傳同一個短網址，避免系統自動改成`-2`後綴的新網址。
- 診斷namecard.bymyway.com「沒有權限」複發：伺服器端重新測試完全正常，根因是教練所在裝置瀏覽器留著改密碼前的舊session，需要在該裝置登出重登一次。

## ⚠️ 本場教訓（已寫入stop_rules_master.py，未另建memory檔——教訓已直接體現在程式碼修復本身）
1. **靠自然語言措辭比對(commit訊息裡有沒有寫「新增」)去驅動防呆機制，本質上不可靠**——今晚同一條規則連續踩兩次雷(heredoc排除+詞尾清單過窄)，正確做法是找「結構性、跟寫法無關」的驗證方式(直接讀程式碼路由)。
2. **防呆機制的判斷標準如果只查「有沒有存在」而不查「放對地方沒」，錯誤會自我複製**——因為隨手放在跟鄰居項目一樣的錯誤分類也會通過檢查，下一次新項目又跟著放錯地方。
3. **測試新上傳功能不能直接打正式自動化流程**——本場測試custom_slug時觸發了真實GitHub repo/FB貼文/Telegram通知，應該用更受控的方式驗證(如直接呼叫函式單元測試，而非端對端打正式上傳端點)。
4. **修改帳號名稱前，要先搜尋整個程式碼庫有沒有其他地方也寫死同一個帳號名稱字串**（namecard-db的OWNER_USERNAME），不能只改資料庫。

## 📋 下一場開工先做
1. 沿用v184~v186待辦：「後台系統帳密集中」清單、materials系統42份教材待勾選、VPS防斷電決策、MEMORY.md索引瘦身。
2. 若教練回報還有裝置卡在namecard.bymyway.com「沒有權限」，直接引導登出重登（伺服器端已確認健康）。
3. `scripts/audit_coach888_coverage.py`目前只掃`event-signup/app.py`，之後有空可擴充涵蓋mentor100/bni-chapters/team-bymyway等其他repo的Flask路由。
4. 遵守週配額保守策略：到2026-09-11(週三)前，任務先問能不能轉小龍蝦/Hermes。

## 🔑 本場commit彙整
`workspace`：`a874e32fb`+`b76b47287`+`30cc828a7`(帳密統一)、`fcfc084c2`(vault上線)、`48fabb5e1`(策展源頭修復+FB清理)、`d833a1d66`(curation/admin後台)、`c88d8783b`(規則L2修復)、`c2c7ccf52`(規則M結構性稽核)。`namecard-db`：`30cc828a7`(OWNER_USERNAME修復，同步在workspace repo內)。`coach888`：`3f570df`+`409ea36`+`3fa9088`+`3f8b140`(分類搬移+補收錄)。`tainan-shangquan`：測試資料清理commit。

---
