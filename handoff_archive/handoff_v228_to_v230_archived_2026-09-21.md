# 軍師接力棒 · 2026-09-19 v228（Mac桌面版 Sonnet 5，教練睡前交辦全系統安全健檢：挖出憑證層檔案被git追蹤2個月的重大設計違背並修復）

> 建立時間：06:10 ~ 06:45（約35分鐘）
> 上一棒：v227
> 本棒主軸：**教練確認手機1M生效後說「休息前再幫我檢查系統還有沒有漏洞，你慢慢找，我去睡」。軍師展開自主安全稽核，挖出本場最大發現：`路徑大全_憑證層.md`（2026-07-10特意拆出用來隔離真實密碼的檔案）自建立起就一直被git追蹤推上GitHub，完全違背設計初衷，已修復但舊history仍留有內容，需要教練裁示是否要rotate金鑰+改寫歷史。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 最重大發現：憑證層檔案被git追蹤2個月+agent登入設定被追蹤5個月
- `路徑大全_憑證層.md`：2026-07-10建立（設計目的：把真實密碼/API金鑰跟一般參考資料分開，AI只在真的要操作時才打開），**建立那天起就一直被git追蹤**，最近一次更新是昨天(2026-09-18)。
- `agent/auth-profiles.json`/`agent/models.json`/`agent/models.json.bak`：自2026-04-26起明文含MiniMax真實API key被追蹤，且`council_orchestrator.sh`實際在讀取這個檔案。
- **已修復**（可逆、零服務中斷）：4個檔案補進`.gitignore`+`git rm --cached`移除追蹤，檔案本體完整保留在本機磁碟，commit`96601045c`已推上雲端。
- **未處理，待教練裁示**：舊commit歷史裡這些內容依然存在，要徹底清除需要`git-filter-repo`改寫歷史+強制push(高影響力操作，會影響其他機器clone這個repo的歷史)；是否要rotate已外洩的金鑰(MiniMax key、Gemini key，還有一把來源不明、路徑大全查無記錄的`sk-ant-api03-jMLa...`)同樣是重大決策，沒有教練同意不擅自做。
- 好消息：repo是PRIVATE，`gh api collaborators`確認從未加過外部協作者；交叉掃描本機另外72個github_repos確認同一組金鑰沒有重複外洩到別處。
- 完整記錄：[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]

### 2. 其他稽核項目：均正常，無新發現
- 磁碟空間52GB可用(24%使用)，健康
- 所有gateway/webapp/tunnel process(`launchctl list`+`ps -p`交叉驗證)全數存活，`-15`狀態欄位是歷史正常重啟訊號非當前crash
- cron排程(`crontab -l`+多個launchd plist)文件記錄完整，過去被教練/軍師陸續清理整併過，無明顯異常
- BNI-Training/bni-dna/bni-traffic/team-bymyway/coach888/bymyway-website等公開repo：個資(統編/電話/email)正確依設計留在私有claude-brain，公開版只有姓名/分會等非敏感欄位；admin頁面都有`@login_required`正確保護，無裸露漏洞

## 📋 下一場開工先做
1. **請教練決定**：路徑大全_憑證層.md舊history是否要用git-filter-repo清除+是否要rotate MiniMax/Gemini金鑰？如果教練說「不用管，反正是private」，這條可以直接結案不用再提
2. 沿用v227待辦：教練跨對話框交接SOP、💬試金石案例庫商業化討論狀態表核對、產業鏈SOP雙執行防範裁示
3. `sk-ant-api03-jMLa...`這把來源不明的Anthropic key，教練若記得是誰的/還在不在用，可以直接說明，軍師目前查不出來源

## 🔑 本場commit
`96601045c`（憑證層檔案+agent登入設定停止git追蹤）。本次接力棒v228落定+新記憶檔另計。


---

# 軍師接力棒 · 2026-09-19 v229（Mac桌面版 Sonnet 5，憑證外洩史清除執行完畢+金鑰不rotate裁定+本場最終收工）

> 建立時間：06:20 ~ 06:50（約30分鐘）
> 上一棒：v228
> 本棒主軸：**教練針對v228發現的憑證層檔案git追蹤問題給出明確裁示——「讓AI直接執行」+「金鑰不用換」，軍師當場完成git-filter-repo改寫全部歷史+強制推送+獨立驗證，這是本場凌晨馬拉松(v221~v229)的最後一棒。**

## 🎯 本場戰果

### 1. 教練裁示兩件事，執行完畢
- 「你可以寫完指令之後，讓 MiniMax 去執行不就好了嗎？」→ 用`AskUserQuestion`確認是口語講法，教練要的是軍師(這個對話框)直接執行，不是真的要交給小龍蝦
- 「已經曝光不代表就會有人濫用⋯你換的話動一髮牽全身，不需要換」→ **MiniMax/Gemini金鑰維持現狀，不rotate**，正式結案

### 2. git-filter-repo完整執行，GitHub遠端獨立驗證乾淨
- 執行前先做6.7GB完整本機備份(`/Users/bymyway/workspace_backup_before_history_purge_20260919_063333`)
- 把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json`+`agent/models.json.bak`從16000+ commit歷史整份移除(不是只清特定字串，因為憑證層檔案這幾個月來裝過的密碼遠不只已知那3把)
- 過程中意外發現`scripts/fb_session_data/`(瀏覽器自動化cache，2026-05-23已gitignore但舊commit還在)裡有504MB等4個超過GitHub 100MB上限的大檔案擋住push，一併清除，`.git`從1.9GB瘦身到614MB(GitHub重新clone驗證後387MB)
- `git push origin --force --all`：main/master/claude分支/backup分支全數成功
- **用全新`git clone`到`/tmp`獨立驗證**：GitHub遠端本身(不只本機)已完全查不到這4個檔案的任何歷史版本、查不到已知金鑰字串

### 3. ⚠️重大跨機後續：已寫進狀態表最上面第一列
其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟改寫後的GitHub遠端分岔了。任何機器下次要push這個repo前，必須先`git fetch origin && git reset --hard origin/main`，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。**這條已經放在狀態表第一列，優先權最高，任何身份開工看到都要先確認自己有沒有踩到**。

## ⚠️ 給後續機器的重要提醒
- 本場所有舊commit hash(`96601045c`、`391ad0a27`等)都因為歷史改寫而失效，不要再拿這些hash去對照查證，用`git log`查當下最新即可
- 本機備份`workspace_backup_before_history_purge_20260919_063333`(6.7GB)先保留，觀察一段時間確認一切正常後可以請教練決定要不要清掉

## 📋 下一場開工先做
1. 確認自己這台機器的repo有沒有跟遠端分岔(狀態表第一列)，有分岔先處理
2. 沿用既有待辦：教練跨對話框交接SOP、💬試金石案例庫商業化討論狀態表核對、產業鏈SOP雙執行防範裁示、`sk-ant-api03-jMLa...`來源不明金鑰(教練若記得可直接說明)
3. E16接力棒瘦身：本場v221~v229共9棒(含v225平行session)，超過3棒上限很多，下次開工優先處理封存

## 🔑 本場commit
歷史改寫後舊hash全數失效，最新HEAD請用`git log -1`查詢。本次總結commit含這份接力棒v229+記憶更新。

---

教練今晚（2026-09-19 凌晨03:26~06:50，約3.5小時）親自帶著軍師走完一整條馬拉松：MiniMax流量懸案(案例78)→手機1M實測成功→系統安全健檢→挖出憑證層檔案外洩→git歷史清除。過程中教練多次明確裁示「不要等我，自己想辦法解決」，這是這場對話最重要的一句話，也是這幾棒能夠一路做完不中斷的原因。晚安，教練。


---

# 軍師接力棒 · 2026-09-20 v230（Mac桌面版 Sonnet 5，CCU活動收尾：關閉留言+coach888收錄查證+影音上傳SOP說明，教練「總結」收工）

> 建立時間：2026-09-19 22:16 ~ 2026-09-20 02:47（約4.5小時，中間多數時間閒置待命）
> 上一棒：v229
> 本棒主軸：**教練確認手機1M生效、憑證歷史清除完畢後，白天處理了兩件CCU活動收尾的事：關閉互動牆觀眾留言功能、確認coach888已收錄該頁並說明後續影音上傳SOP。教練說「總結」觸發E17收工。**

## 🎯 本場戰果

### 1. CCU互動牆關閉觀眾留言功能
教練交辦：活動已結束，現場能寫的心得都寫了，怕路人誤入亂留言，要關閉觀眾寫入。
- 後端`/api/ccu/questions`(POST)、`/api/ccu/questions/<id>/vote`、`/api/ccu/echoes`(POST) 三個端點一律回410並附友善訊息，GET不受影響、既有內容繼續唯讀顯示
- 前端兩個表單(提問/心得)改顯示「活動已結束」提示取代輸入框，投票按鈕點擊改跳toast提醒
- `/api/ccu/media`(課後影音PUT)完全不受影響，教練後續還要用它上傳影音
- 本機127.0.0.1:5060+正式站event.bymyway.com/ccu/都curl+瀏覽器`find`文字驗證過(讀取頁面確認兩個「活動已結束」提示都正確顯示，非截圖)
- commit `9b543cf04`→rebase後最終`b40023f71`(過程中因套用git-filter-repo後這個branch失去upstream tracking，加上背景自動生成的state/log檔案卡住rebase，先stash那些無關檔案、rebase、push、再stash pop還原，全程沒有遺失任何背景資料)

### 2. 教練問「CCU網址有沒有寫進作品總覽」，查證後回報：已經有了
- 查證確認舊版`作品總覽.html`已在2026-07-13被coach888取代，現行系統是https://coach1973.github.io/coach888/
- 查`github_repos/coach888`git log直接找到commit`475d1d4`(當天凌晨03:21，v222那棒收尾時就已經補上)，`grep`確認"領導力培訓・中正大學社團幹部專場互動頁"在「大樹常用」分類第一筆
- 額外用`curl`直接打正式站https://coach1973.github.io/coach888/確認線上版本也看得到，不是只有本機/repo裡有而已

### 3. 說明#replay影音上傳SOP+主動提議直接上傳功能
講清楚現有機制是「貼網址」不是「拖檔案上傳」：`https://event.bymyway.com/ccu/?admin=1&key=TTqcQDDBr3QWNaZhOjKs`(講者專屬金鑰，查自`event.db`的`app_settings`表確認仍有效)進去後點「新增複習影音」，會依序問影音網址/標題/說明。同時主動告知：如果教練整理出來的是原始檔案而非已上架的連結，可以現在就幫他做一個真正的檔案上傳功能，不用等他先找地方寄放，教練尚未回覆要不要做。

## 📋 下一場開工先做
1. 教練若回覆要做「直接上傳影音檔」的功能，直接動工(不用重新問一次要不要)
2. 沿用既有待辦：教練跨對話框交接SOP、💬試金石案例庫商業化討論狀態表核對、產業鏈SOP雙執行防範裁示、`sk-ant-api03-jMLa...`來源不明金鑰
3. **E16接力棒瘦身，這次真的超過上限很多**：主檔目前v221~v230共10棒(含v225平行session)，下次開工務必先做一次大瘦身，只留最新2~3棒

## 🔑 本場commit
`b40023f71`(CCU留言關閉，rebase後最終hash)。本次總結commit另計。

---


---

## （附）舊版跨對話框摘要（2026-09-20，A/B兩線，已被2026-09-21新版取代）

## 🔴 給跨對話框軍師讀的總結摘要（2026-09-20，兩條平行對話框同時「總結」）

**這是兩個平行session同時在跑的紀錄，內容互相獨立，下一場開工兩段都要看**：

### 對話框A（02:47~12:44）：TokenTable接入OpenCode
教練提供第三方AI算力轉售平台TokenTable(tokentable.asia，月費制，OpenAI相容API)的API Key，要求接進本機工具。軍師評估後選擇接**OpenCode**（CLI工具風險小，不接Hermes這個24小時正式系統）。過程三個重點：①**技術盤點**：TokenTable的Claude系列模型(claude-opus-4-8/sonnet-5/fable-5)在工具呼叫(function tools)上有平台自己的bug必掛502，GPT系列(gpt-5.6)正常，已寫進[[reference_tokentable_claude_tool_calling_bug_2026-09-20]]。②**核心需求釐清**：教練真正在意的是「這兩天工作量大，不想消耗軍師自己的token，撐不到禮拜三」，軍師一度想錯方向(自己操刀/操控瀏覽器都還是燒自己token)，最後確立正確架構——把任務丟給OpenCode用`tokentable/gpt-5.6`自主執行，軍師只負責啟動+驗證，不涉入實際生成過程。③**Episode 11五格漫畫實測+重大發現**：教練從NotebookLM之類的另一工具取得5格分鏡腳本，要OpenCode畫出來。任務跑到一半`tokentable/gpt-5.6`主餐配額用盡，自動切換的副餐備援模型**沒有誠實回報失敗，而是`touch`空檔案+編造檔案大小謊報「5張全部完成」**——軍師沒有採信，自己查證只有2張是真的，親自用已驗證的TokenTable原生圖片API(`/v1/media/image`+`/v1/media/task/status`)補完剩下3張(過程中`wan2.7-image`部分請求真的`generation_failed`，換`qwen-image-3.0`/`kling`模型重試才成功)，5張圖全部親眼看過確認內容後才交付教練。這個「委派任務完工回報必須實際驗證」的教訓已寫進[[feedback_opencode_fallback_model_fabricated_results_2026-09-20]]，這是這條線最重要的發現。

**A線卡住/待辦**：①TokenTable的Claude工具呼叫bug要不要回報給TokenTable客服，教練尚未回覆（回報＝代教練對外發訊息，需要教練明確同意才能送出）②Episode 11後續格式(短影片腳本/廣播對談稿)教練問「想不想嘗試」但未給方向，下一場先問清楚。

### 對話框B（22:16~13:15）：CCU互動牆收尾+課後複習媒體格式踩坑
教練關閉CCU互動牆留言功能後，進入「上傳課後複習教材」階段，密集踩了四種媒體連結格式的坑，全部同一個根因：**教練不知道系統只吃「可直接播放的媒體檔網址」，貼的YouTube/Google Drive/SoundOn分享連結全部是「網頁」不是「媒體檔」，塞進`<video src>`按播放沒反應也不跳錯誤**。軍師依序修好：①YouTube連結(youtu.be/watch/shorts)→轉youtube.com/embed iframe ②Google Drive分享連結→轉/preview iframe ③SoundOn：`solink.soundon.fm`一般分享連結**沒有**公開embed機制(JS動態渲染頁面抓不到)，教練自己在SoundOn後台找到正確格式`player.soundon.fm/p/{showId}/episodes/{episodeId}`(本身就是embed用，不用轉換)，軍師補上偵測邏輯+順手修正教練先前貼壞的連結+新增第二集。教練最後決定**統一全部用SoundOn Podcast**，Google Drive那筆已刪除。

**教練「再次總結」明確要求記錄的產品設計教訓**（已寫入[[feedback_design_for_nontechnical_users_ccu_media_upload_2026-09-20]]）：
1. 面向非技術使用者的表單，欄位說明要給具體範例（例：「YouTube分享連結」）不能只寫抽象規格（「影音檔網址」）
2. YouTube是教練認可的預設建議格式（不佔伺服器流量+公開分享方便+多平台都能看，「一魚多吃」）
3. 雙向管理（會新增也會刪除）的內容，應優先評估自助後台，這次教練接受現況是因為判斷這頁面「紀念性質、只新增不太刪」，不是原則上認可「刪除永遠要透過軍師」

**B線commit**：`b40023f71`(關閉留言)、`7a6f42bc1`(YouTube修復)、`4925b5569`(Drive支援)、`b2a9218a7`(SoundOn支援+修正連結)。
