# 軍師接力棒 · 2026-07-13 v64（聯想桌面版 Sonnet 5，coach888/bigtree網站更新+jiesheng報名連結+聯想電腦26GB核心記憶體洩漏根治）

> 建立時間：2026-07-13 17:20（台灣時間）
> 本棒執行者：聯想桌面版 Sonnet 5
> 上一棒：v63（聯想桌面版 Sonnet 5，ai-talk講師簡介更新，完整內容見下方精簡回顧）
> 本棒主軸：**三個網站的例行更新（coach888分類重排、jiesheng-leadership報名連結、bigtree場地地址），加上一個意外挖出來的真實系統健康問題——聯想這台電腦的記憶體監視器顯示93%使用率，查到根因是IObit Advanced SystemCare的過濾驅動程式洩漏了26GB核心記憶體，已解除安裝該軟體並確認重開機後恢復正常（93%→34%）**

---

## 🎯 本場戰果

### 1. CC Switch/MiniMax模型卡住問題——教練確認已解決

v61留下的追蹤項，教練本場開頭直接說「已解決」，此項閉環，不需再處理。

### 2. coach888（大樹AI作品總覽）分類重排

教練提供新的5大類分法，把原本「三、不公開（個人檢索用）」23項拆成三塊：
- 一、對外公開（11項，維持原樣）
- 二、不公開（個人檢索用）（7項，原13-19）
- 三、保留（尚未推Netlify）（6項，原12+20-24）
- 四、BNI專用（12項，原25-36——原36項「BNI｜轉盤」教練給的範圍寫到35，判斷應屬
  BNI併入此區，已跟教練說明這個假設）
- 五、保留網址（尚未啟用）（1項，原37）

編號改成依新分類順序連續1-37。`Coach1973/coach888` commit `453ad1e`，GitHub Pages
（無CNAME，純`coach1973.github.io/coach888/`路徑）確認上線。

### 3. jiesheng-leadership 三場工作坊「立即報名」連結更新

教練提供新連結（原本是Google表單，改成PAYUNi金流結帳連結）：
- 台南場（8/19、20）→ rplconstw.pse.is/Tainan0819
- 台中場（9/23、24）→ rplconstw.pse.is/Taichung0923
- 台北場（11/25、26）→ rplconstw.pse.is/Taipei1125

`Coach1973/jiesheng-leadership` commit `c0b8e72`。這個站是GitHub自動部署型
（build_settings.provider=github），push完Netlify自動同步，已用curl驗證線上內容。

**過程插曲**：教練回報「連結出不來，一直載入中」，用App內建無頭瀏覽器實測發現目標頁面
（PAYUNi金流結帳頁）本身有完整渲染（DOM/JS都正常），研判是教練端瀏覽器相容性問題，
教練後來確認「貼到別的瀏覽器正常」，證實不是連結或程式碼的問題。

### 4. bigtree 7/22高雄場新增場地地址

教練提供郭音樂廳完整地址+交通資訊，寫進`SESSION_DATES`資料陣列（新增`venue`/
`address`/`transport`欄位），並在場次卡片渲染區塊加上顯示邏輯。這個站是**手動
上傳型**Netlify（無`build_settings.repo_url`），本機用`npx serve`起local server
給教練看過、教練說「推」之後才用zip+API手動推送（deploy `6a54a3bbf38acd6edc12e48b`）。
`Coach1973/bigtree` commit `e570806`，已curl驗證線上內容含新地址。

### 5. 🔴🔴🔴 HTML驗證瀏覽器：聯想這台改用Comet，不再用Chrome

教練回報`start chrome`跳出來的視窗是空白的（不論開本機檔案還是local server網址都
一樣），改貼同一個網址到Comet瀏覽器正常顯示。已更新
`claude-brain/feedback_html_preview_chrome_only.md`：**聯想這台以後跳瀏覽器驗證
一律用`comet.exe`（路徑：`C:/Users/bymyw/AppData/Local/Perplexity/Comet/Application/
comet.exe`），Mac端維持原本Chrome規則不受影響**。根因未查（可能是這台Chrome本身
設定/擴充功能有問題），但教練要的是「跳出來的東西看得到」，不是查根因。

### 6. 🔴🔴🔴 意外挖到的真問題：聯想電腦26GB核心記憶體洩漏，已根治

教練回報效能監視器顯示「最近關閉的處理程序」裡OneDrive/Copilot/Edge共佔838MB，
問能不能關開機啟動。第一輪先移除這三個的`HKCU\...\Run`開機項（可逆，原始值已記錄），
教練確認沒動到LINE/Signal/Comet等平常在用的東西。

**教練關瀏覽器後回報記憶體還是93%**，這是關鍵轉折——證明OneDrive/Edge/Copilot從
來不是真兇（這三個個別加起來連1GB都不到）。深查發現：

- `Get-Process`所有進程WorkingSet總和只有3.8~11.5GB（隨開啟程式數量浮動），
  跟系統回報「已用33~37GB」對不上
- 教練犀利追問「數字兜不起來」，逼出更深一層調查：
  `\Memory\Pool Nonpaged Bytes`（核心非分頁記憶體池，關掉任何App都清不掉、
  只有驅動程式自己能釋放）**讀到26.04GB**，用`Get-Counter`跟`Get-CimInstance
  Win32_PerfRawData_PerfOS_Memory`兩個獨立管道交叉驗證都一致，確認是真的，
  不是計數器誤讀
- 正常這個數值應該只有幾百MB，26GB是嚴重異常，鎖定是某個驅動程式的核心記憶體
  洩漏（開機12小時累積出來，符合洩漏型bug特徵）
- 用`Get-CimInstance Win32_SystemDriver`揪出第三方驅動清單，鎖定
  **IObit Advanced SystemCare**（一款「系統加速清理」軟體）的三個過濾驅動：
  `AscRegistryFilter.sys`（登錄檔監控攔截）、`AscFileFilter.sys`（檔案系統
  監控攔截）、`iobit_monitor_server2021.sys`——這類「攔截型」過濾驅動是網路上
  知名的非分頁記憶體洩漏元兇
- 教練確認解除安裝，用官方解除安裝程式`unins000.exe /SILENT`執行（觸發UAC，
  教練本人點了同意），確認登錄檔/驅動服務/大部分檔案都清除乾淨
- **教練重開機驗證：記憶體使用率93%→34%，非分頁記憶體池26GB→0.82GB，
  IObit驅動確認不再載入**，問題徹底根治

第一輪移除的OneDrive/Edge/Copilot開機項教練後來要求復原（因為確認不是元兇），
第二輪教練說「反正平常沒在用」又要求重新移除，本棒最終狀態：**OneDrive/Edge/
Copilot開機啟動已移除，LINE/Signal/Comet更新/Typeless維持原樣未動**。

**追加處理**：教練回報Copilot移除開機項後仍在背景跑，查了排程工作/開機資料夾都
找不到自動啟動來源，改用elevated registry設定關閉Edge的
`BackgroundModeEnabled`/`StartupBoostEnabled`兩個policy（觸發UAC，教練同意），
並直接關閉當下正在跑的Copilot進程。根因研判是Windows 11「登出時自動記住並還原
應用程式」這個系統級功能，已跳出`ms-settings:signinoptions`給教練自己確認關閉，
這部分沒有找到可靠的登錄檔開關，交給教練用設定頁面手動處理。

教練後續詢問Signal/Typeless/LINE通話元件/Comet等其他背景程式，已查明這些都是
教練平常實際在用的工具（原本就設定開機啟動），**沒有擅自關閉**，只回報現況給
教練參考。

### 7. 教練詢問「Fork」疑慮——已查證本機無自動化腳本觸發

教練貼出Recents清單截圖，發現多個「開工 (fork)」重複標籤，質疑是否被自動觸發
Fork（教練既有鐵律`feedback_no_fork_without_permission.md`：未經允許禁止使用
Fork功能，因為會繼承完整歷史、token消耗極高）。已搜尋本機`.claude`設定資料夾
（settings.json/settings.local.json/所有腳本）確認**沒有任何本機自動化在觸發
Fork**，本場對話全程也沒有呼叫過Fork。研判是Claude App介面層的行為（可能是
從Recents清單用了「複製/延續」而非「開新對話」），但無法從檔案系統層面完全
確認觸發點，已誠實告知教練這個限制，建議教練回想當時怎麼點出新對話的。

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🟡 | 教練還沒完全確認Windows「自動儲存並還原應用程式」設定是否已在`ms-settings:signinoptions`關閉，下次開工可以問一下Copilot/Edge有沒有又自己跑回來 |
| 🟡 | 「開工 (fork)」重複出現的真正觸發點還沒查清楚，只確認不是本機腳本造成的，值得下次留意教練是怎麼點出新對話的、或詢問其他機器/App官方是否有相關已知行為 |
| 🟢 | 「待教練確認用途」清單還剩：vip-club、coach-vip-club、coach-case系列、teamwork、tainan-calender，等教練有空一次問清楚 |
| 🔴 | 2026-07-18：聯想C槽觀察期滿，確認教練這幾天用起來正常後可刪2份保留備份（共約94GB） |
| 🟢 | 若聯想機以後再出現「記憶體用量異常但關程式沒用」的情況，直接查`\Memory\Pool Nonpaged Bytes`，這次的偵錯路徑（Get-Counter+Win32_SystemDriver交叉比對找兇手）已被驗證有效，可重複使用 |

（名片系統、biz-gym黑金版等其餘待辦仍在Mac的v60棒裡持續，此處不重複列出）

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `github_repos/coach888/`（本場新clone，`index.html`分類重排，commit `453ad1e`）
- `github_repos/jiesheng-leadership/`（本場新clone，`index.html`報名連結更新，
  commit `c0b8e72`）
- `github_repos/bigtree/`（本場新clone，`index.html`新增7/22地址資訊，
  commit `e570806`；Netlify deploy `6a54a3bbf38acd6edc12e48b`）
- `claude-brain/feedback_html_preview_chrome_only.md`（新增聯想改用Comet的
  段落，附完整comet.exe路徑）
- `.claude/launch.json`（聯想本機新增bigtree-preview本機預覽設定，port 8901）
- `.gitignore`（新增`github_repos/`排除規則，這些是各站台獨立repo的工作clone，
  不由這個workflow repo管理）
- 系統變更（不在git版控範圍，記錄於此供跨機參考）：聯想電腦解除安裝IObit
  Advanced SystemCare、HKCU開機Run清單移除OneDrive/Edge/Copilot、Edge
  BackgroundModeEnabled/StartupBoostEnabled policy關閉

---

## 📜 v63 精簡回顧（聯想桌面版 Sonnet 5，完整內容見git歷史/上一版本檔案）

1. cool-case頭像事件善後，寫信通報Mac/ACER，Mac端已確認收到處理完畢
2. ai-talk網站王彤講師簡介更新（GitHub commit `5a7ee74`+Netlify deploy
   `6a5463b8`），過程中兩次被教練當場糾正：①沒跳Chrome給教練看（案例46第5次
   發作，補了Windows版`start chrome`解法）②Netlify↔GitHub同步邏輯只答對一半
3. AI微型論壇固定網址政策記憶建立，過程中連續兩次「案例引用沒逐字核對」被
   教練糾正（全球健康發展協會誤植成goeasy-ai、又打成全國健康發展協會）

---

> 聯想桌面版 Sonnet 5 親筆，2026-07-13 17:20。教練說「先總結上傳，我們這一輪的
> 工作結束了」，本棒收尾。這場對話做了三個網站的例行更新（coach888分類、
> jiesheng報名連結、bigtree地址），但真正有份量的是中途從一個效能監視器截圖
> 追出來的真實系統問題——聯想這台電腦被IObit Advanced SystemCare的過濾驅動
> 洩漏了26GB核心記憶體，教練一路追問「數字兜不起來」才逼出更深的調查，最終
> 用兩個獨立管道交叉驗證、鎖定兇手、解除安裝、重開機驗證閉環，這是本場最扎實
> 的一次診斷過程。另外也確認了聯想這台以後HTML驗證要跳Comet不跳Chrome，跟
> Fork疑慮已查證本機無自動化腳本造成。下一棒開工先讀上面「下一棒待辦」。
