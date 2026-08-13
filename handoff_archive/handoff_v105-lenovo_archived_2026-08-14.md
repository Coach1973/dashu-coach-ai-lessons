# 軍師接力棒 · 2026-08-10（聯想 Windows 終端機 Sonnet 5，LINE VOOM備份下載解壓+Zoom junction查證+C碟清理調查+一鍵備份驗證）

> 建立時間：2026-08-10（台灣時間）
> 本棒執行者：聯想 Windows 終端機 Sonnet 5
> 上一棒：v105（Mac桌面版 Sonnet 5，event-signup抽獎報到流程重新設計+bymyway.com/coach888多站維護）
> 本棒主軸：**教練LINE VOOM服務9/30停用前下載官方備份，全程協助下載進度核對+7-Zip解壓縮+驗證。過程中教練順勢追問過去資料事故歷史，AI主動查證試金石確認案例29/51真實性並誠實承認。教練接著要一鍵備份前清C碟暫存檔，AI一度查錯方向(查到E碟東西對C碟備份無幫助)，教練點破後重查，順帶查出Zoom的E碟junction已失效，教練裁示風險可接受不修。最後驗證教練剛做的一鍵備份確實只留最新一份無殘留。教練說「總結」時明確指出這是要開新視窗的信號，AI總結後又被追問「有上傳接力棒嗎」——這正是本節在補的SOP缺口。**

## 🎯 本場戰果

### 1. 🎯🎯 LINE VOOM備份下載+解壓縮（本場核心）
教練收到LINE VOOM官方通知(2026-09-30停止服務)，下載密碼保護的備份(65個分割zip，`da53f34c_partN.zip`)。過程AI多輪協助教練核對「還缺哪些part」，抓出瀏覽器對同一part重複下載會存成`(1)`後綴檔案的行為，逐輪清除重複+補齊清單，最終65個全數到齊、無缺件無重複。裝7-Zip(這台機器原本沒有)後用密碼`x8xcjleahd`解壓縮全部65個到`E:\LINE VOOM`：2847則貼文資料夾、21GB、完整性測試(`7z t`)0失敗。教練確認後刪除D碟`Downloads`裡的65個原始zip。過程中教練問「多數資料夾裡面沒什麼內容」，查證後說明是純文字貼文(無圖片影片)只有小小的index.html，非解壓縮出錯。

### 2. 🔧🔧 教練歷史資料事故查證：案例29(LINE 4GB)+案例51(Zoom誤刪)
教練提及「E碟資料不見，是被你刪除的，救都救不回來」，AI沒有辯解，直接查試金石確認屬實：案例29(2026-06-25，LINE 4GB聊天記錄因AI用`Remove-Item -Recurse -Force`把兩份備份都刪光，永久遺失)+案例51(2026-07-17，AI查證方法有漏洞誤導教練同意刪除Zoom增量資料，1.8GB+746MB)。誠實確認兩次事故都是真的、無法挽回，不粉飾。

### 3. 🔧 Zoom C碟junction失效查證+教練裁示不修
教練追問「確認增量資料都成功在E碟」，AI實測發現`C:\Users\bymyw\AppData\Local\Zoom`(403.91MB，8/1至今239個檔案持續寫入)不是junction，是獨立真實資料夾；對應的`E:\Claude-Data\AppData\Zoom-Local`8/1至今0異動，是凍結在7月中旬的舊快照——代表案例51修復時建的junction後來失效了(推測被Zoom更新/重裝覆蓋)。教練確認「資料量小、增量也沒多少，就不管它了」，裁示不修，已寫入記憶`project_zoom_c_drive_junction_broken_accepted_2026-08-10`。過程中教練也追問Chrome/Comet/Perplexity/甘靖四個瀏覽器的junction是否正常，AI逐一實測確認Chrome/Comet/甘靖都是真連結，但發現「Perplexity」(2.58GB)是個沒有任何程式連結的孤兒複本(比一般快取更適合直接清)，查試金石確認這是2026-07-11 App搬家時期已知模式的殘留。

### 4. 🔧 C碟暫存檔清理調查（教練糾正查錯方向）
教練要求「清理暫存檔以節省空間」準備一鍵備份，AI第一輪列出約10GB的瀏覽器快取——**教練點破這些快取都是junction到E碟，對「C碟一鍵備份」大小沒幫助**，AI方向抓錯。重新查證後發現C碟其實已經很乾淨(7/11大瘦身後這個月只胖回5.6GB)，真正的暫存垃圾(使用者Temp/縮圖快取/Windows更新快取/回收桶)加總不到0.3GB，唯一有意義的清理空間是WinSxS系統元件庫(7/11清過11.17GB，現又長回16.26GB，DISM官方工具可再省4~5GB)。**教練尚未回覆是否要執行DISM清理**，下一場先問。

### 5. 🟢 一鍵備份驗證
教練做完一鍵備份後要求確認「應該都清除之前的舊檔，只留這個最新的8月10日」。查證E碟只有一份「易數一鍵還原Windows系統備份（不要刪除）」，`BootImage.pmf`(0.07GB)+`SystemImage.pmf`(85.29GB)皆為8/10當天寫入，之前3月的舊版本已被取代不存在，總大小85.36GB，符合教練預期。

### 6. 🔴 教練糾正：「總結」後要記得上傳接力棒
教練說「總結」，AI給了文字總結但誤以為`git status`乾淨(只確認到之前hook commit那批)就等同完成SOP，沒有真的寫新的接力棒條目就準備結束對話。教練直接問「你有上傳接力棒嗎？這不是SOP嗎？」，AI誠實承認遺漏，立刻補寫本節內容+更新狀態總表對應4個新項目。**教訓**：往後聽到「總結」，除了口頭摘要，一定要實際檢查JUNSHI_HANDOFF_LATEST.md有沒有寫新條目、commit+push了沒，不能只憑`git status`乾淨就當作交接完成——那只能證明「已commit的東西沒有未存檔改動」，不能證明「這場的工作已經寫進接力棒」。

### 🔧 環境教訓：PowerShell 5.1中文編碼系列問題（本場多次踩坑）
除了三機hook同步待辦已記錄的BOM/InputEncoding問題，本場又多次踩到同一根因的變體：
- inline `-Command`帶`$_.Name -match "中文正則"`會被bash參數傳遞+ PowerShell解析雙重出包，改寫成獨立.ps1檔案較穩
- 純ASCII wildcard(`-like "*delete*"`)無法匹配中文檔名(`删除`)，查資料夾時改用ASCII子字串(如`*Windows*`)或直接讀完整JSON輸出(`ConvertTo-Json`寫檔+用Read工具讀，比終端機直接印中文可靠)
- 這些坑目前都是每次遇到才繞過，還沒有系統性解法，下次軍師寫Windows查詢腳本時可以先預期這類編碼問題

## 📋 下一場直接開工任務
- **C碟WinSxS清理**：教練尚未回覆要不要執行DISM `/StartComponentCleanup`(預估再省4~5GB)
- **三機hook同步**：ACER仍待處理，見[[project_cross_machine_hook_sync_todo_2026-08-08]]
- LINE VOOM備份：教練可能會再確認`E:\LINE VOOM`裡的內容(用index.html瀏覽)，暫無其他待辦
- Zoom junction：已裁示不修，不用再主動提起

## 🔑 本場關鍵檔案索引
- `E:\LINE VOOM`：解壓縮後的完整備份(21GB，非git專案)
- `E:\Claude-Data\.claude\projects\E--Claude-Data\memory\project_zoom_c_drive_junction_broken_accepted_2026-08-10.md`：新建
- commit(memory記憶庫)：`af0407d7`
- 本場無workspace repo commit(純查證+本機操作，無腳本異動)
