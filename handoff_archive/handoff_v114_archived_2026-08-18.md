# 軍師接力棒 · 2026-08-17 v114（Mac桌面版 Sonnet 5，Mac/聯想Chrome擴充功能搶線根因+ezPay統編去重優化+coach888作品連結更新）

> 建立時間：2026-08-17 16:30 ~ 21:05（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v113（Mac桌面版 Sonnet 5，ezPay電子發票操作能力驗證+任務轉交聯想）
> 本棒主軸：**教練回報mentor100照片不清晰，換照+更正828→9/23-24台中場後，要求ezPay 177筆歷史補齊+備註查詢，過程中意外撞見本場最大插曲：Mac讀到的ezPay帳號(bymyway/大樹教育)跟教練親眼看到的(gtbctainan/BNI)對不上，教練一度懷疑「讀到聯想電腦」，來回排查十幾輪才找到真根因——同一個Claude帳號同時連了3台瀏覽器(Mac+2台Windows)，系統要求明確選擇卻先前默默選錯。教練裁示永久解法：聯想改用Edge、Mac維持Chrome物理隔離，已寫記憶+跨機信箱正式發信通知聯想。回到ezPay任務，教練連續兩次提出優化(只查B2B/238→163筆，同統編只查一次/163→108筆)，展現「先想有沒有更簡單做法」的協作默契。中途發現聯想已在git裡建好一套完整的BNI培訓紀錄資料庫(公開版+私有後台)，教練要求把這兩個新網址加進coach888作品總覽，此項本場結束時仍在執行中。**

## 🎯 本場戰果

### 1. 🟢 大樹教練照片換新+828/9-23誤植更正（已寫入待辦表首列，此處不重複）
詳見待辦狀態追蹤總表第一條，commit `7ac6b0e`（ai-forum-taichung）。

### 2. 🔴🔴🔴 Mac/聯想Chrome擴充功能「搶線」真根因找到，教練裁示永久解法改用Edge隔離
教練操作ezPay時發現Mac讀到的帳號(bymyway/大樹教育/商店344031309)跟教練親眼在Mac螢幕上看到的(gtbctainan/BNI/商店337391376)完全對不上，一度激烈質疑「你到底在讀哪一台電腦」。排查過程：①先用`claude-in-chrome`的`computer`截圖比對兩個實體螢幕，證實gtbctainan確實在這台Mac的可見視窗上，但擴充功能連的分頁始終讀不到那個分頁②教練最終自己想通根因：**聯想電腦當時也同時在用同一組帳號的Claude Chrome擴充功能執行任務，兩邊連線會搶到對方機器**③後續操作BNI Connect時系統主動跳出`list_connected_browsers`提示，證實當下同時有3台瀏覽器連線(Mac+2台Windows)，需明確`select_browser`才能鎖定正確目標——這才是真正機制：多瀏覽器連線需要顯式選擇，先前沒跳出提示是因為還沒觸發到選擇邏輯，之前的操作是默默選到了錯的一台。教練裁示：**聯想改用Microsoft Edge**裝官方擴充功能(來源限定Anthropic官方Chrome Web Store頁面，非Edge市集裡的第三方仿冒品)，Mac維持Chrome，物理隔離避免再搶線。已寫記憶`feedback_two_machines_same_chrome_extension_conflict_2026-08-17.md`+正式跨機信箱發信`cross-agent/inbox/lenovo/20260817-1920_mac-to-lenovo_switch-browser-to-edge.md`(教練確認可用「讀信」暗號觸發，不需開工儀式)，commit`b6ac36a8a`+`0588a4a86`。

### 3. 🎯🎯 ezPay 238筆歷史成功抓取(含備註前置作業)，教練連兩次優化查詢範圍
延續v113的177筆基礎，本場重跑12個時間窗查詢，發現**2026-08-16漏抓了2024-01~2024-07共5個月61筆**(查詢邊界誤判為近2年，實測發現真實可查邊界更早到2024-01-01)，補齊後總計238筆存檔`claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv`，commit`bee006ef8`。教練要求進一步補每筆的發票備註(會員姓名對照，因B2B買受人名稱是公司行號查不到人)，估算全查238筆要價6~10萬token後，教練連續給出兩層優化：①**只有B2B(統編非空)需要查，B2C的買受人名稱本身就是人名**——238筆篩到163筆B2B ②**同一統編對應同一會員，只要查一次代表性的那筆**——163筆再篩到**真正需要查的只有108個不同統編**，比原始238筆省了55%以上工作量。這兩層優化尚未實際執行查詢(教練要求先「總結」再繼續)，下次開工直接照108這個範圍做即可，不用重新想優化邏輯。

### 4. 🔧 BNI Connect真鑽（實為大台南南區5分會）會員資料查詢：已定位頁面但暫停執行
教練要求把94位會員(含真誠/真鑫/真富/真鑽/真愛5分會)的電話/email做成資料庫方便聯想開票。已定位到`operationsRegionManageMembership`會員清單頁+`operationsRegionEditMembership?memberId=X`個別會員編輯頁(內含電話/email，測試1筆成功抓到王彤：0937327857/tongtong129@hotmail.com)，並確認**這個React SPA必須用真實DOM click觸發路由，直接navigate()帶正確參數也會報錯**，是可行但成本不低的技巧(94筆逐一點開)。教練評估Token成本後選擇暫停(AskUserQuestion被dismiss)，隨後教練告知**聯想那邊已經用另一個方法(BNI Connect官方培訓報表xlsx，含電話email，姓名比對回填)找到45人的電話/email**，此項Mac端不用重複執行，已結案。

### 5. 🔍 意外發現：聯想已建好「BNI培訓紀錄總資料庫」公開版+私有後台雙軌系統
git pull時發現聯想同一天(2026-08-17)已完成一套完整系統：公開版`https://coach1973.github.io/BNI-Training/`(GitHub Pages，只放姓名/分會/出席，753筆官方培訓報表+45人電話email回填)+私有後台`claude-brain/data/bni_training_admin.html`(私有repo專用，含統編/載具/email，教練原話「後台要方便我做事」)。完整脈絡見`claude-brain/project_bni_training_records_db_2026-08-17.md`。教練要求把這兩個網址加進coach888作品總覽，**本場結束時此任務仍在執行中**（已確認coach888的`二、後臺系統`/`四、不公開`兩個section位置，尚未實際寫入HTML）。

## 📋 下一場直接開工任務
- ~~coach888加入BNI-Training公開版連結~~：**2026-08-17 21:30已完成**，加入「一、大樹常用」第14項，commit`7dc9234`(coach888 repo)，curl確認GitHub Pages已生效
- ~~coach888私有後台`bni_training_admin.html`連結~~：**2026-08-17 21:38更正結案**——先前記錄「需要決定localhost/URL形式」是Mac端查證錯誤(`find`指令`-maxdepth 4`深度不夠，沒搜到已經存在的檔案，誤判成「本機無此檔案」)。**真相**：這份私有後台本來就已經是`claude-brain/data/bni_training_admin.html`，跟其他claude-brain記憶檔一樣隨`workspace`私有repo(`mac-openclaw-workflows`)一起git同步，教練在任何一台機器`git pull`+`open`這個檔案就能開，不需要另外架server或URL。已用`open -a "Google Chrome"`實測在Mac開啟成功，畫面正常。coach888暫不加這條連結(純本機檔案沒有URL可掛連結)，教練若想要「隨時隨地點進去」的體驗，可考慮之後包成小型Flask服務掛上網址，屬另一個獨立任務，教練未提出前不主動做
- ~~ezPay發票備註查詢，範圍已定案108個不同統編~~：**2026-08-17 23:30已完成**，108/108全部查到，存於`claude-brain/data/ezpay_invoice_remarks_108taxid_2026-08-17.csv`，commit`dbd55d47d`。技巧：發票明細modal的token藏在「查看/補發」連結的`onclick="search_invoice_info.search_invoice_detail('token')"`屬性裡，每個發票獨立token無法預先推算，須先用日期查詢找到該筆列表列再抓token；modal內容讀取要鎖定`#invoice_detail .modal_div`(頁面同時存在`#notify_detail`開立通知modal，兩個都叫`.modal_div`容易抓錯)，且AJAX回填有明顯延遲，**必須用輪詢等到`發票號碼`欄位符合預期值才讀取**(固定等待1.6秒不夠、常抓到上一筆殘留內容)。過程中Chrome擴充功能連線中斷一次(1.5小時無操作後)，導致瀏覽器分頁JS記憶體內累積的51筆結果全部遺失——**教訓：長時間批次瀏覽器抓取不能只累積在頁面記憶體，要每查完一批立刻寫檔到硬碟**，本次之後改成每批次(約10筆)查完就存一個json檔，最後再合併，重做時只多花約10分鐘
- ~~聯想改用Edge~~：**2026-08-17 21:23教練口頭確認已切換完成**，Chrome搶線問題結案，見`feedback_two_machines_same_chrome_extension_conflict_2026-08-17.md`
- 「真誠分會」網頁主架構問題：**2026-08-17教練裁示擱置**，暫不處理
- 三機hook同步（Windows/ACER的Claude Code settings.json hook，非OpenClaw gateway hook）：ACER仍待處理
- **賈維斯計畫Phase 2月度cron**：9/1會第一次真實自動執行(cron`5d7acd65`，每月1日09:20)，8/16已手動驗證過一次全綠，9/1是排程本身的自然下次觸發時間，非異常，留意HEARTBEAT.md有無異常

## 🔑 本場關鍵檔案索引
- `claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv`：238筆完整清單
- `claude-brain/reference_ezpay_bulk_invoice_scraping_procedure.md`：批次爬取SOP
- `claude-brain/feedback_two_machines_same_chrome_extension_conflict_2026-08-17.md`：搶線根因+Edge解法
- `cross-agent/inbox/lenovo/20260817-1920_mac-to-lenovo_switch-browser-to-edge.md`：正式跨機信件
- `claude-brain/project_bni_training_records_db_2026-08-17.md`：聯想BNI培訓資料庫完整脈絡（唯讀，聯想維護）
- `github_repos/ai-forum-taichung/images/speaker-dashu.jpg`：教練新照片
- `github_repos/mentor100/mentors.db`：教練照片id=4已更新（DB直改不進git）
- commit：`7ac6b0e`（照片）+`b6ac36a8a`+`0588a4a86`（Chrome衝突）+`bee006ef8`（ezPay 238筆）
