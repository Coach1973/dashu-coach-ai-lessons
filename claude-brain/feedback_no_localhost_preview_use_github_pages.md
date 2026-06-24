---
name: no-localhost-preview-use-github-pages
description: 軍師端的 Chrome MCP 看不到 Mac 本機 localhost；HTML 預覽走 GitHub Pages 線上版，不要起 python http.server 浪費時間
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b701cc5f-5498-4a6e-b723-0cd90da952c9
---

軍師端 Chrome MCP（mcp__Claude_in_Chrome__*）連到的是教練 Windows 機的 Chrome（透過擴充功能），不是 Mac 本機的瀏覽器。**所以 Mac 上跑 python -m http.server 8899 後，Chrome MCP 訪問 localhost:8899 一定失敗**（「Frame with ID 0 is showing error page」）。

**Why:** 2026-06-03 軍師改完 cool-case 想用 Chrome MCP 預覽，起了 localhost 伺服器但 Chrome MCP 載入失敗。教練順手指出之前已有部署鐵律 commit 5eec01dd：[[feedback-netlify-deploy-zip-api]] 講 Netlify 80 次不成熟部署燒掉 1,200 點——本質都是「別在本機反覆預覽，直接推上線」。教練的 RustDesk 環境又加深這層複雜度（[[coach-rustdesk-remote-env]]）。

**How to apply:**
- 改 cool-case／網頁類產品時，**省去本機預覽這一步**——直接 commit + push 到 gh-pages，看 https://coach1973.github.io/cool-case/ 線上版
- HTML 內容正確性用 Python 工具自驗（標籤閉合、關鍵字串、字數）就夠
- 教練要看視覺效果就讓他開瀏覽器看線上版（教練 Windows Chrome 可以正常連 GitHub Pages）
- 對應守則#08（討論是為了執行）：與其卡在本機預覽，不如直接推線上版

**例外：** Netlify 站點還是要遵守 commit 5eec01dd 鐵律——推前先給教練看本機檔（用 open 開 Finder 給教練親眼確認），確認後 zip+API 一次推送。

相關記憶：[[feedback-netlify-deploy-zip-api]]、[[coach-rustdesk-remote-env]]、[[feedback-no-screenshot-for-data]]
