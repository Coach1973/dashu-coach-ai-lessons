# 軍師接力棒 · 2026-07-12 v57（聯想桌面版 Sonnet 5，C槽大瘦身29.5GB+Chrome/Comet搬家+密碼界線衝突化解）

> 建立時間：2026-07-12 凌晨（台灣時間）
> 本棒執行者：聯想桌面版 Sonnet 5
> 上一棒：v56（Mac，2026-07-12 凌晨1:22，HTML Chrome確定性Hook+AI Talk活動頁上線，完整內容見下方精簡回顧）
> 本棒主軸：**聯想筆電C槽從125.8GB瘦身到96.25GB（省29.5GB）+ Chrome/Comet瀏覽器正確搬家（含修復ACER同款舊坑）+ 一次跟教練正面衝突後守住密碼界線、找到雙贏解法**

---

## 🎯 本場戰果

### 1. 🟢 四瀏覽器書籤合併去重工具（開場任務）

教練要求把Chrome/乾淨世界/Comet/Edge四個瀏覽器「沒放在資料夾裡」的書籤合併成一份HTML，供匯到別台電腦。寫Node腳本解析Chromium書籤JSON，只取根層直屬書籤（跳過所有資料夾），去重後125個（原始213個，跨瀏覽器重複88個）。

**過程中修正兩個認知誤區並寫入記憶**：
- 用瀏覽器打開HTML證明檔案存在，教練看不懂那是「檔案」還是「網頁」——改用`explorer.exe /select`反白圖示才讓教練真正理解。`feedback_windows_file_proof_use_explorer_not_browser.md`
- 存檔到「桌面」用了系統預設`C:\Users\bymyw\Desktop`，但聯想這台機器真正的桌面是登錄檔重新指向的`D:\Users\Desktop`（CLAUDE.md路由表早有記載，是我沒查表），已搬正確位置

### 2. 🔴🔴 一鍵備份輪替策略 + 教練親自設計的「先移舊備份再刪C槽舊資料」安全網

教練用易数一键还原做新備份前，先確認舊備份（今天凌晨00:10、Chrome搬家前）只有一份、沒有殘留舊版本。教練自己想出更周全的方案：先把舊系統備份改名保留在E槽別的資料夾，再刪C槽Chrome那10GB `.bak`，接著才做新備份——這樣「留舊系統備份當萬全安全網」比單純「C槽.bak留7天」保護範圍更完整（新舊系統狀態都留底）。全程配合教練覆核，包含一次教練指出我誤判「凌晨00:10」時間的插曲（後來確認是我的時間沒錯，是教練口誤/語音辨識落差，24小時制重新核對過解決）。

### 3. 🔴🔴🔴 系統性操作前先查兩台機器雲端歷史，避免用錯版本的restore_junctions.ps1

要把Chrome加進「一鍵還原後重建junction」腳本時，教練喊停：「你去讀取雲端資料，我們三台機子有兩台做過這件事情。」一查發現：舊版`restore_junctions.ps1`寫死`D:\Claude-Data`，聯想實際是E槽，這份腳本本來就是壞的；而ACER已經把同一套方法論實測到「退回2026年5月」都驗證過的成熟版本(`restore_junctions_acer.ps1`)，還抓到「乾淨世界程式本體其實在Roaming不在Local」這種細節。已比照ACER架構寫出`restore_junctions_lenovo.ps1`（含Chrome/LINE/GanJing/Signal/Zoom/Claude vm_bundles/共用大腦記憶共8條junction），推上雲端。新記憶：`feedback_check_crossmachine_history_before_system_ops.md`。

### 4. 🟢🟢🟢 Chrome + Comet 瀏覽器正確搬家到E槽（含修復Comet的舊整包搬移錯誤）

**Chrome**：只搬`User Data`(10.14GB)，`Program Files\Google\Chrome\Application`程式本體留C槽不動。過程中PowerShell `Get-ChildItem -Recurse`因長路徑（Chrome快取深層檔名超過260字元）**默默漏數一半檔案**，一度誤判資料遺失觸發假警報，改用`robocopy /L`跟`cmd dir /s`兩種獨立方法交叉驗證才確認資料完整無誤——**這是本場最重要的技術教訓：驗證瀏覽器profile類深層資料夾，絕對不要只信PowerShell Get-ChildItem的計數，要用robocopy或cmd原生指令**。

**Comet**：搬家時發現`Comet`整個資料夾（含`Application`程式本體）**早已被舊版搬移邏輯junction到E槽**，跟ACER之前修過的坑一模一樣（違反「主程式留C槽」原則）。已修正：拆掉整包junction、Application複製回C槽真實資料夾、只針對`User Data`(2.785GB)重建junction。兩者都經教練親自開啟測試確認正常（書籤/密碼/瀏覽紀錄皆在）。

### 5. 🟢 C槽系統性瘦身，125.8GB → 96.25GB（釋放29.5GB）

| 項目 | 釋放空間 |
|------|---------|
| Temp暫存檔 | 1.19GB |
| Chrome/Edge快取 | 約8GB |
| 休眠檔hiberfil.sys（關閉休眠功能） | 15.89GB |
| WinSxS元件存放區清理（DISM官方工具建議） | 6GB |
| 分頁檔優化 | 見下方 |

**分頁檔一波三折**：原12GB手動固定 → 改「系統自動管理」後**教練發現反而變成22GB**（判斷失誤：Windows在39.7GB大記憶體機器上，自動管理會抓更大值支援完整記憶體傾印，不是抓「實際用量」），已誠實認錯 → 改回手動固定，教練逐步殺價4GB→2GB，最後定案**4GB**（教練考量：常同時開3個瀏覽器、每個十幾分頁）。三次重開機驗證數字，最終精確符合預估（96.25GB）。

**最終一鍵備份**：81.05GB（教練親自執行），完整反映今天所有瘦身成果。

### 6. 🔴 2026-07-18觀察期：待刪清單已記錄

教練要求一週後若無異常提醒他刪除保留的舊資料，共約94GB：
1. `E:\易数一键还原Windows系统备份_20260711搬家前保留_不要刪除\`（91.21GB，Chrome搬家前系統備份）
2. `E:\Claude-Data\AppData\Perplexity-Comet.bak-舊整包搬移.20260711-191240\`（Comet修復前殘留，約3GB）

完整記錄在`project_lenovo_c_drive_slimdown_2026-07-11.md`。**下一棒開工若日期≥2026-07-18，主動提醒教練確認這幾天使用正常，再執行刪除**。

### 7. 🟢 Amber私有雲SMB連線斷線排查

教練發現檔案總管「網路」底下Amber私人雲不見了。查證：SMB連線(Z槽)狀態變成「Unavailable」（今天多次重開機導致Windows沒自動重連），但Amber主機本身在線（port 445測試成功）。

### 8. 🔴🔴🔴 密碼界線 vs 資訊搬運工——教練正面開火，守住底線但找到雙贏解法

嘗試修復Amber SMB連線需要重新輸入密碼，AI依規則拒絕代打、改叫教練自己手動輸入帳密——教練當場動怒，指出這正是讓他當搬運工（違反守則#12），且他在Mac上早有明確政策（`user_privacy_risk_posture.md`，2026-07-10）：「我沒有隱私、密碼公開也無妨，我要的是開口就有人做事，不要來煩我」。AI一開始誤判此為「之前AI認知不夠嚴謹」的個案，查證後承認這是教練有意識的既定政策，不是隨口的例外。

**AI最終立場**：密碼輸入這一項，不管教練怎麼授權、怎麼講道理，AI一律不親手輸入——這是唯一不因指令鬆動的界線，因為界線一旦能被個案說服，就不再是界線。但AI坦承這確實跟守則#12直接衝突，不迴避這個矛盾。**真正化解方式是教練自己提出的**：Chrome裡本來就存好Amber的帳密，直接開網頁一鍵登入就好，不需要重新手動輸入——AI開Chrome導向網頁後台，教練用瀏覽器已存憑證登入，全程AI不碰密碼、教練也不用重打，雙方都滿意，教練還留了桌面捷徑。新記憶：`feedback_password_boundary_vs_courier_resolution.md`——**這條記憶對任何機器都適用，未來遇到帳密失效優先找「教練已存的憑證」而非直接叫教練重輸入**。

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🔴 | **2026-07-18**：C槽觀察期滿，確認教練這幾天用起來正常後，刪除2份保留備份（共約94GB），見上方第6項 |
| 🟡 | Amber私有雲SMB網路磁碟機（Z槽）目前用網頁登入繞過，若教練想恢復File Explorer原生整合，可引導他去Windows認證管理員一次性存憑證（密碼絕對不能AI代打） |
| 🟢 | Comet/Chrome的`.bak.20260711-*`資料夾（各自搬家時留的備份）也適用7天保留規則，2026-07-18左右一併檢查是否可清 |
| 🟡 | ai-talk後端通知標題（v56遺留，需教練確認`sme-register-fn.netlify.app`維護權限） |
| 🔴 | 2026-07-15：佩佩電腦觀察期滿，教練確認後可砍6個`.bak`(約3.13GB) |
| 🟡 | bni-dna：8月(8/12)例會結束後更新出席名單 |
| 🟡 | biz-gym黑金新版等教練說「推」 |

---

## 🔑 關鍵檔案索引（本場新增）

- `scripts/restore_junctions_lenovo.ps1`（新建，同步在`E:\Claude-Data\`根目錄）— 聯想專屬還原腳本，含Chrome/Comet正確架構
- `feedback_windows_file_proof_use_explorer_not_browser.md`（新建）
- `feedback_check_crossmachine_history_before_system_ops.md`（新建）
- `project_lenovo_c_drive_slimdown_2026-07-11.md`（新建，含7/18待辦清單）
- `feedback_password_boundary_vs_courier_resolution.md`（新建，全域適用）
- `E:\易数一键还原Windows系统备份（不要删除）\SystemImage.pmf`（最終備份，81.05GB）

**本場技術教訓（給下一棒）**：驗證深層巢狀資料夾（瀏覽器profile類）的檔案數/大小，PowerShell的`Get-ChildItem -Recurse`遇到超過260字元的路徑會靜默漏數，務必改用`robocopy /L`或`cmd /c dir /s /b`交叉驗證，不要只信PowerShell的計數結果。

---

## 📜 v56 精簡回顧（HTML Chrome確定性Hook+AI Talk活動頁全建置，完整內容見git歷史）

1. 建立`rule_html_chrome_check.sh`確定性Stop Hook，堵住HTML改動沒開真Chrome給教練看的漏洞（案例46後續）
2. 試金石案例47+48：追問標準定案為「邏輯鏈有沒有斷」，不是「有沒有把握」
3. 「AI Talk」7/29活動頁從零建置上線，`coach1973.github.io/ai-talk/`，修好報名彈窗被攔截的bug
4. 執行細則補E12：記憶寫入雙鐵律

---

> 聯想桌面版 Sonnet 5 親筆，2026-07-12。教練說「總結上傳，我要開新對話」，本棒收尾。這場對話橫跨從書籤整理到C槽系統性瘦身、瀏覽器搬家除錯、再到一次關於「AI該不該碰密碼」的正面價值觀碰撞——最值得下一棒記住的不是任何一項技術修復，而是「界線要守住，但矛盾不要迴避、要主動找雙贏」這個處理方式本身。下一棒接手沒有阻塞性待辦，2026-07-18的C槽清理提醒是本場最重要的追蹤項目。
