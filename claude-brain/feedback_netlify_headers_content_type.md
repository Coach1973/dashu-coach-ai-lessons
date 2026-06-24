---
name: feedback-netlify-headers-content-type
description: Netlify 手動上傳型部署必須帶 _headers 檔案寫死 Content-Type，否則顯示原始碼（至少三次血淚）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d045433-c07e-4194-8146-7178d4ce8a81
---

Netlify 手動上傳型站台，zip 裡只放 index.html 而不帶 `_headers` 檔案時，Content-Type 預設為 `text/plain`，瀏覽器會顯示 HTML 原始碼而非渲染網頁。

**Why:** 2026-05-30 在 cool-case.netlify.app 至少發生三次「教練說上去看是原始碼」，每次都浪費教練時間確認。根因是 zip 裡沒有 `_headers`。

**How to apply:** 每次 zip 部署前，永遠加這一步：
```bash
printf "/*\n  Content-Type: text/html; charset=UTF-8\n" > /tmp/_headers
```
然後 zip 裡同時包含 `index.html` 和 `_headers`。部署後用 `curl -sI` 確認 content-type 是 text/html 才算完成。

相關記憶：[[project-coolcase-xinfa-website]]、[[feedback-netlify-deploy-zip-api]]
