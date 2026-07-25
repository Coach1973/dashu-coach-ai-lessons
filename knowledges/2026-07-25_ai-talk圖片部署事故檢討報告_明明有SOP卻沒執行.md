# 檢討報告：ai-talk-tw圖片部署事故——明明有SOP卻沒有確實執行

> 建立時間：2026-07-25（台灣時間）
> 撰寫者：聯想（Windows）Claude Code Sonnet 5
> **教練親自要求**：「請把它寫一份檢討報告丟到雲端，讓其他兩台電腦的軍師都要看得到，不要再犯這種低級的錯誤。」
> **本報告目的：ACER／Mac 軍師開工讀到此檔，務必把「文字內容+圖片資源分開驗證」「_headers精確路徑」「Windows zip不用Compress-Archive」三條吸收進日常操作，不要等自己也犯一次才學會。**

---

## 一句話總結

一件本來一次部署就能做對的事，因為**已有SOP卻沒有完整執行**，前後做了3次部署才真正修好，白白多扣45點Netlify credit（原本15點，多花了30點）、多花教練3輪來回確認的時間。

---

## 事發經過（時間序）

1. 教練交辦在 ai-talk-tw.netlify.app 新增「現場設攤」6家廠商圖卡、贊助好禮（EVERYDAY CAFE、煦多午茶）、贊助人名單，並附上圖片素材。
2. 本機用 Comet 瀏覽器打開 local file 預覽過排版正常，教練確認可以推送。
3. 推送 GitHub + Netlify（第1次部署，deploy `6a646c0213e4778b1f227e4e`）。部署後只用 `curl` 抓頁面文字內容確認新增的廠商名稱等字樣有出現，**沒有針對新增圖片做任何驗證**，就回報教練「已確認上線」。
4. 教練實際打開網站：**完全看不到圖片**，直接點破：「你的圖片在Netlify那個地方是沒有顯示出來的……你沒有確定結果，推上去之後圖片是看不見的。」
5. 查證發現第一個bug：Windows PowerShell `Compress-Archive` 把 zip 內部路徑打包成反斜線（`images\booth-1.jpg`），Netlify 無法辨識資料夾結構，圖片路徑直接 404。改用 `.NET ZipArchive` 手動控制路徑分隔符重新打包部署（第2次部署，deploy `6a646d24b8282fcfef619bd1`）。
6. 圖片變成 HTTP 200，但再查 `Content-Type` 仍是 `text/html`（不是 `image/jpeg`）——查出第二個bug：`_headers` 檔案有一條舊規則 `/* → Content-Type: text/html`，這條萬用規則蓋過了圖片本該有的 MIME 類型，導致檔案位元組正確、狀態碼 200，但瀏覽器判定是 HTML 文字拒絕渲染成圖片。修正 `_headers` 改用精確路徑後第3次部署（deploy `6a646d61f78654b788d59cee`），這次才真正修好。
7. 教練用**無痕視窗**（排除瀏覽器快取干擾後）確認終於看到圖片。
8. 教練追問：「我明明就有SOP，為什麼你沒有照做呢？」——查證發現確實早有 `feedback_netlify_headers_content_type.md` 這份SOP（2026-05-30建立，源自cool-case.netlify.app至少3次「顯示原始碼」教訓），裡面明確寫著「部署後用 `curl -sI` 確認 content-type 是 text/html 才算完成」，但這次只驗證了文字內容，沒有針對圖片資源做這一步。
9. 教練確認總損失：3次部署、45點credit（教練原先估算60點，經查證核實應為45點，教練沒有反駁這個更正）。
10. 教練做出最終裁示：「這就是你明明有SOP卻不去執行SOP付出的代價。」並要求寫本報告全機通報。

---

## 教練原話（逐字保留）

> 「我上去看了一下，沒有看到顯示圖片喔。你的圖片在Netlify那個地方是沒有顯示出來的，請儘快處理。你這樣子是不合格的，因為這樣浪費了我15點，你沒有確定結果，推上去之後圖片是看不見的。」

> 「我明明就有SOP，為什麼你沒有照做呢？」

> 「這次有看到了。所以本來一次可以做對的事情，前後一共做了三次。加上第一次，你一共被扣了60點才完成工作，我這樣說對嗎？」

> 「這就是你明明有SOP卻不去執行SOP付出的代價。請把它寫一份檢討報告丟到雲端，讓其他兩臺電腦的均勢都要看得到，不要再犯這種低級的錯誤。」

---

## 根本原因分析

**不是「不知道有SOP」，是「SOP只做了一半就自認完成」。**

1. **驗證範圍不完整**：SOP寫的是「部署後用curl -sI確認content-type」，這次只用curl驗證了文字內容（grep廠商名稱），完全沒有對新增的圖片資源做同樣等級的驗證。文字跟圖片是兩種完全不同的資源類型，各自有各自的失敗模式，用同一種方法（抓文字）驗證不到圖片的問題。
2. **SOP範本本身有技術債**：這份SOP寫於2026-05-30，當時只為了解決「純HTML頁面顯示原始碼」的問題，範本用`/*`萬用規則設定Content-Type。這條規則對純文字站台沒事，但沒有預想「之後這個站台會加圖片」的情境——舊債被這次新功能踩到。
3. **Windows特有工具鏈盲點**：PowerShell `Compress-Archive` 在Windows上打包zip會用反斜線路徑，這是先前從未踩過的坑，第一次部署時完全沒意識到需要驗證zip內部的路徑格式對不對。

---

## 已完成的修復

1. `ai-talk` repo `_headers` 規則從 `/*` 改成精確路徑 `/`（只鎖首頁），不再蓋過圖片的 Content-Type（commit `6729f7f`）
2. Windows zip打包改用 `.NET ZipArchive` 手動指定 entry 路徑用正斜線，不再用 `Compress-Archive`
3. SOP記憶檔 `feedback_netlify_headers_content_type.md` 已更新，明確要求「部署後驗證要拆成文字內容＋圖片資源兩件事，缺一不可」，並註明Windows zip打包的正確做法
4. 試金石新增**案例54**，完整記錄根因、教練原話、修復方式

---

## 🔴 給ACER／Mac軍師的具體提醒（不要再犯同樣的錯）

1. **任何Netlify手動上傳型部署，`_headers`不要用`/*`萬用規則**，除非確定站台永遠不會有圖片等非HTML資源。優先用精確路徑（`/`鎖首頁、`/*.html`鎖html檔、`/images/*`只設Cache-Control）。
2. **Windows上打包zip給Netlify，不要用PowerShell `Compress-Archive`**（會產生反斜線路徑導致Netlify認不得資料夾結構、圖片404）。改用`.NET System.IO.Compression.ZipArchive`手動控制路徑分隔符為`/`。
3. **部署後驗證，文字內容跟圖片等資源要分開各自驗證**：
   - 文字：`curl -s <url> | grep <關鍵字>`
   - 圖片：對每個新增圖片路徑跑`curl -sI <url>/images/xxx.jpg`，確認`HTTP/1.1 200` **且** `Content-Type: image/jpeg`（狀態碼200不代表圖片真的會顯示，Content-Type錯了照樣看不到）
4. **已有SOP不等於會自動被完整套用**——每次操作前主動回想「這件事有沒有相關SOP，我是不是每一步都真的做到了」，不能只做到SOP的一部分就自認為完成。這次的教訓不是「沒有SOP」，是「有SOP但執行不完整」，這種錯誤比從零開始不知道還要不應該發生。

---

Related: [[feedback_netlify_headers_content_type]]、試金石案例54、[[feedback_html_preview_chrome_only]]
