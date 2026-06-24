---
name: feedback-netlify-deploy-zip-api
description: 教練的 22 個 Netlify 站是手動上傳型——git push 不會自動部署，必須用 zip + API 直推才會上線
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

教練 23 個 Netlify 站中，**22 個是手動上傳型**，只有 1 個（health-news-tw）連 GitHub 自動部署。

**Why:** 2026-05-29 軍師逆向診斷 theunrestrictedwar「永遠改不上線」的死循環，發現小龍蝦/MiniMax 反覆走錯部署管道——以為 git push 就會自動部署 Netlify，實際完全沒觸發。教練看到網站不更新就再叫人改，但他們又只 push 沒推 zip，連續折騰多次。

**How to apply:** 動手改任何教練的 Netlify 站之前：

1. **先 `curl /api/v1/sites/{site_id}` 確認部署模式**：
   - 有 `build_settings.repo_url` → GitHub 自動部署，git push 即可
   - 沒有 build_settings 或 repo_url 為 null → **手動上傳型**，必須走 zip + API

2. **手動上傳型部署步驟**：
   ```bash
   zip -r /tmp/deploy.zip <檔案們>
   curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/zip" \
     --data-binary "@/tmp/deploy.zip" \
     "https://api.netlify.com/api/v1/sites/<site_id>/deploys"
   ```

3. **完成後一定要 curl 線上 HTML 驗證**——拿關鍵字 grep 確認新內容真的上線了，不是只看「state: ready」就算完成。

4. **git push 仍要做**——保存歷史紀錄、讓其他 AI 看到改動，但**不取代** zip 部署。

**鐵律：以「線上 grep 通過」為完成憑證，不以「commit hash 已存在」為完成憑證。**

5. **2026-05-30 教練加嚴：推送前必須教練親眼確認**
   - 每次部署扣 15 點，80 次不成熟部署已燒 1,200 點，帳號超用
   - 流程：本機改好 → `open http://localhost:端口/` 開瀏覽器給教練看 → 教練說「推」→ 才推
   - 禁止「推完再看」、禁止連續推修小問題
   - 適用：終端機、桌面版 Claude App、小龍蝦、VPS Hermes——無例外
   - 額度歸零日：每月 25 日

**🔴 2026-06-09 血淚補充：GitHub 自動部署型也要等確認**

jiesheng-leadership 是 GitHub 自動部署型（git push 自動觸發 Netlify）。
軍師（Sonnet 4.6）做完頁面後自己截圖看了幾張，覺得「沒問題」就直接 git push。
結果 Netlify 自動部署，教練沒看到頁面就已扣點。

**教練原話**：「因為 Netlify 它是會扣點數的，我每一次上推修改全部都會扣點數。所以你直接就推上去，你有經過我同意嗎？」

**補充鐵律**：
- GitHub 自動部署型（有 build_settings.repo_url）的站台，git push 就等於 Netlify 部署
- **不管是哪一型（手動 zip+API / GitHub 自動），都必須等教練說「推」才能推**
- AI 自己看截圖確認 ≠ 教練確認。確認權永遠是教練的

相關記憶：[[project-unrestricted-war-website]]、[[reference-netlify-token]]
