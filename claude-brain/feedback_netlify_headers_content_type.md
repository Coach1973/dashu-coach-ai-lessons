---
name: feedback-netlify-headers-content-type
description: Netlify 手動上傳型部署必須帶 _headers 檔案寫死 Content-Type，否則顯示原始碼；若站台含圖片等資源，_headers 規則要用精確路徑不能用/*萬用（否則圖片會被蓋成text/html顯示不出來，2026-07-25第4次血淚）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d045433-c07e-4194-8146-7178d4ce8a81
  modified: 2026-07-25T08:09:26.010Z
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

相關記憶：[[project-coolcase-xinfa-website]]、[[feedback-netlify-deploy-zip-api]]
