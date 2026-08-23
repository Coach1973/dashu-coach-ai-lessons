---
name: feedback-netlify-headers-content-type
description: Netlify圖片類部署一次做對checklist——_headers精確路徑(非/*萬用)/Windows zip不用Compress-Archive/文字圖片分開驗證/輪播類圖片要預先載入(preload)不能等切換才下載，每次遇到血淚就加一條
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d045433-c07e-4194-8146-7178d4ce8a81
  modified: 2026-08-23T01:36:13.017Z
---

Netlify 手動上傳型站台，zip 裡只放 index.html 而不帶 `_headers` 檔案時，Content-Type 預設為 `text/plain`，瀏覽器會顯示 HTML 原始碼而非渲染網頁。

**Why:** 2026-05-30 在 cool-case.netlify.app 至少發生三次「教練說上去看是原始碼」，每次都浪費教練時間確認。根因是 zip 裡沒有 `_headers`。

**🔴 2026-07-25更新（第4次血淚，ai-talk-tw）：** 舊版 SOP 的 `_headers` 範本用 `/*` 萬用規則蓋所有路徑的 Content-Type，這對純文字頁面沒問題，但**只要站台之後加了圖片等非 HTML 資源，`/*` 規則會把圖片也蓋成 `text/html`，圖片檔案本身正確、HTTP 200，但瀏覽器因為 Content-Type 宣告錯誤拒絕渲染成圖片**（純看 curl 文字內容或狀態碼都測不出來，要專門查 Content-Type header 才會發現）。同時這次還疊加了 Windows `Compress-Archive` 產生反斜線路徑導致圖片 404 的獨立 bug，兩者一起讓「新增圖片」這個改動完全上不了線，詳見試金石案例 54。

**How to apply（更新版）：**
1. `_headers` 規則優先用精確路徑，不要用 `/*`：
```
/
  Content-Type: text/html; charset=utf-8
/*.html
  Content-Type: text/html; charset=utf-8
/images/*
  Cache-Control: public, max-age=31536000
```
只有確定站台**完全沒有圖片等其他資源、未來也不會加**時，才能用最簡版 `/* → text/html`。
2. Windows 上打包 zip 給 Netlify，不要用 PowerShell `Compress-Archive`（會產生反斜線路徑 `images\x.jpg`，Netlify 認不得），改用 `.NET ZipArchive` 手動指定 entry 路徑用 `/`。
3. **部署後驗證要拆成兩件事，缺一不可**：
   - 文字內容：`curl -s <url> | grep <關鍵字>` 確認新增文字出現
   - 圖片等資源：對每個新增的圖片路徑跑 `curl -sI <url>/images/xxx.jpg`，確認 `HTTP/1.1 200` **且** `Content-Type: image/jpeg`（不是只看狀態碼，Content-Type 錯了狀態碼照樣是 200 但瀏覽器不顯示）

**🔴 2026-08-02更新（第5個坑，ai-talk-tw活動花絮輪播）：** 教練回報「活動花絮一開始都沒有照片，要等一段時間才出現」。根因跟 Content-Type 無關——是輪播/幻燈片這類「自動切換顯示」的圖片功能，程式碼只在切換的當下才去下載下一張（`img.src = 下一張網址`），完全沒有預先準備。網路稍慢時，切換那一瞬間新照片還沒下載完，畫面就空白，等下載完才補上；且不是只發生一次，是每次自動切換（每 4 秒）都可能重演。這種問題**部署前用 curl 測 Content-Type 完全測不出來**，因為圖片本身沒壞，只是「臨時才下載」的時機點錯了。

4. **任何輪播/幻燈片/多張切換顯示的圖片功能，部署前檢查是否有預先載入(preload)機制**：初始化時應該用 `new Image()` 把該輪播會用到的「全部」圖片網址都跑一輪觸發下載進瀏覽器快取，不要讓「使用者切換到那一張」才是該圖片第一次被請求。範例寫法：
```js
function preloadCarouselImages(){
  for (let i = 1; i <= TOTAL; i++){
    const img = new Image();
    img.src = `images/carousel/photo-${String(i).padStart(2,'0')}.jpg`;
  }
}
```
在輪播 init 時呼叫一次即可，靠瀏覽器原生快取機制，不用等使用者主動切換才臨時抓。

**🔴 2026-08-13更新（第6個坑，Mac端`git archive`中文檔名編碼，bigtree-tw）：** 教練糾正「這種失敗是不能接受的，SOP應該要防止」。根因：Mac 用 `git archive --format=zip -o x.zip HEAD` 打包部署 zip，repo 裡含中文檔名（如 `archive/2026-07-01_創業x政府xAI講座/`）時，git archive 產生的 zip **沒有設定檔名的 UTF-8 旗標**（`ZipInfo.flag_bits & 0x800` 為 0），Netlify 伺服器端解壓時直接整包判定失敗（`error_message: "Deploy failed while extracting zip"`），不是內容錯誤，是打包工具本身的編碼缺陷，且本機用 `unzip -l` 或 macOS `zip` 指令重新打包**同樣會誤判**（macOS Info-ZIP 對 UTF-8 旗標的支援不可靠，即使設了 `LANG=en_US.UTF-8` 也一樣）。這一類 bug 光在 localhost 瀏覽器預覽（SOP 第2步）完全看不出來，因為預覽測的是「內容對不對」，不是「zip 打包機制本身能不能被 Netlify 正確解壓」——兩者是不同層次的驗證，SOP 原本沒有涵蓋後者。

**How to apply：** Mac 端只要 repo 目錄含中文檔名／路徑，打包部署 zip 一律不用 `git archive` 直接產出 zip、也不用 macOS 內建 `zip` 指令，改用 Python 標準庫手動控制：
```python
import zipfile, os
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src):
        for f in files:
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, src))
```
Python 3 的 `zipfile.write()` 遇到非 ASCII 檔名會自動設定 UTF-8 旗標（可用 `info.flag_bits & 0x800` 驗證為 True）。**部署前務必先跑這行驗證**，確認旗標為 True 才送出 POST，不要等 Netlify 回傳 `error_message` 才發現——這一步現在併入 SOP 第1步「本機建好檔案」的必經檢查，跟 Windows 端禁用 `Compress-Archive` 是同一種坑的 macOS 版本，兩邊都源自「作業系統內建打包工具對非 ASCII 檔名的 zip 編碼不可靠」。

**🔴🔴 2026-08-23更新（第7個坑＝第6個坑原地復發，教訓在「什麼時候會忘記查這份記憶」）：** 幫教練建「大樹小講場次後台＋一鍵發佈」時，為了修掉「打包會夾帶工作區未提交內容」這個風險，把打包方式從既有的 `git archive HEAD | tar -x` → `zip` 改成 `git archive --format=zip HEAD`——**正好是上面第6個坑白紙黑字禁止的寫法**。結果教練第一次按下自己的發佈按鈕就失敗，官網完全沒更新，白白扣掉一次額度。

**Why（比技術細節更重要的部分）：** 上一次踩是「手動部署時忘記」，這次是**「把部署流程寫成自動化程式時忘記」**——注意力全放在架構設計（資料庫當真相源、指紋比對、錯誤處理），完全沒意識到自己正在重寫的那幾行就是踩過雷的地方。**自動化的坑比手動的坑嚴重一個量級**：手動錯一次就發現，寫進程式裡的錯會在教練每次按按鈕時重演，而且是教練自己按的、我不在現場。

**同一次還抓到第二個獨立 bug：把 Netlify 回 HTTP 200 當成「部署成功」。** 200 只代表「zip 收到了」，解壓失敗時狀態會永遠停在 `uploaded` 不會變 `ready`，`published_at` 是 null。因為誤判成功，系統還把「已發佈」記錄下來，畫面顯示「官網與後台一致」——**教練看到的是成功，實際官網是舊版**，這比單純失敗更糟。

**🔴🔴🔴 2026-08-23 二次更正——上面「UTF-8 旗標」的診斷是錯的，真因是「目錄項」：** 修好編碼後又失敗一次（教練連續兩次按發佈都白費額度）。拿 08-22 實際部署成功的包跟失敗的包逐項比對才確認：

| | 08-22 成功包（系統 `zip` 指令） | 失敗包（Python `zipfile` 自己走訪檔案） |
|---|---|---|
| 項目數 | 101 | 92 |
| **目錄項** | **9 個** | **0 個** |
| 中文檔名 UTF-8 旗標 | 沒有 | 有 |

**兩包的中文檔名位元組其實都是 UTF-8，Netlify 都解得正確**（線上 `archive/大樹小講_歷史講座紀錄.html` 實測最終 200）。旗標有沒有設根本不影響。**真正致命的是壓縮檔裡沒有寫入資料夾條目**——`zipfile.write()` 只加檔案時不會自動建立 `archive/` 這種目錄項，Netlify 的解壓器需要它，缺了就整包 `Deploy failed while extracting zip`。

**唯一該用的打包方式（08-22 實證成功、08-23 再次驗證結構一致）：**
```bash
git archive HEAD | tar -x -C <暫存目錄>     # 只取已提交內容，不夾帶工作區未確認的修改
cd <暫存目錄> && zip -qr <輸出>.zip . -x ".git*"   # 系統 zip 會自動寫入目錄項
```
送出前用 `zipfile.ZipFile(p).infolist()` 確認**目錄項數量 > 0**，這個檢查不花任何額度。

**Why（方法論層次的教訓，比技術細節重要）：** 第一次失敗我看到「中文檔名顯示成亂碼」就下結論是編碼問題，其實那只是 Python 用 cp437 解讀無旗標檔名的顯示結果，**跟失敗與否無關**。憑單一可疑現象就當成根因、沒有跟「已知成功的樣本」逐項比對，導致修錯地方、又燒掉教練一次額度。**手上有「已知成功」的對照組時，第一步永遠是 diff，不是推論**（對應既有記憶 [[feedback-compare-before-diagnose]]）。

**How to apply：**
0. **失敗診斷先找對照組**：這類「同一件事以前成功過、現在失敗」的問題，先把成功與失敗的產物逐項比對，差異項才是嫌疑犯；不要看到某個可疑特徵就當根因。
1. **凡是動到「部署／打包／推送」這幾行程式碼，動手前先重讀這份記憶**，不管當下是在做手動部署還是在寫自動化。判斷觸發點是「我正在碰打包或部署邏輯」，不是「我正在手動部署」。
2. 部署成功的判準是 **`state == "ready"`**，不是 HTTP 200。POST 拿到 deploy id 後要輪詢 `GET /sites/<id>/deploys/<deploy_id>` 直到 `ready` 或 `error`；逾時就當失敗回報，**絕不可在未確認 ready 前寫入任何「已發佈」狀態**。
3. 交付自動化部署工具前，至少驗證「打包出來的 zip 中文檔名旗標正確」這件事（`flag_bits & 0x800`），這個檢查不花任何部署額度，沒有理由跳過。

相關記憶：[[project-coolcase-xinfa-website]]、[[feedback-netlify-deploy-zip-api]]、[[feedback-web-push-sop]]、[[project_bigtree_session_admin_backend_2026-08-23]]
