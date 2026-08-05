---
name: feedback-netlify-deploy-zip-api
description: Netlify站分兩型(手動zip上傳/GitHub自動部署)，動手前必查是哪型——jiesheng-leadership是後者，2026-06-09+2026-08-05兩度因沒查證而誤推上線
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
  modified: 2026-08-05T13:01:46.464Z
---

教練 23 個 Netlify 站中，多數是**手動上傳型**，已知至少 2 個連 GitHub 自動部署：
health-news-tw、northern-tw（northern411 repo，2026-07-13查證確認，詳見
[[project_ai_talk_recurring_event_url_policy]]）。⚠️ 「只有1個」是舊記憶（18天前）
留下的過時數字，動手改任何站之前務必用下方方法1實測查證當下的部署類型，不要沿用
這個數字。

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

**🔴🔴 2026-08-05 第二次血淚：同一個站台、同一種錯，這次是 Claude Sonnet 5 犯的**

教練要求《結繩領導學》官網大改版（新書發表→兩日工作坊銷售頁），全程都先本機預覽+開真實 Chrome 給教練確認才動作，唯獨最後一步：教練說「可以先推到 GitHub，我讓團隊看完後再決定要不要推 Netlify」，我直接執行 `git push`——**完全沒有停下來查證 `jiesheng-leadership` 的部署類型**，想當然爾套用了同一場對話裡其他手動上傳型站台（bigtree 等）的經驗。結果 Netlify 自動部署上線，教練親自發現「已經是新內容了」才揭穿。

**為什麼會再犯**：本檔第 47 行早就寫死「jiesheng-leadership 是 GitHub 自動部署型」，`feedback_web_push_sop.md` 的判斷表格第一行代表站台也是它——這兩份記憶檔都在，但我當下只想著「教練說先推 GitHub」這句話本身，沒有觸發「動手前查一下這個站是什麼部署類型」的查證動作。**教訓不是記憶不存在，是行動前沒有查記憶**。

**教練原話（2026-08-05）**：「這個就是你的問題，因為你沒有讀取開工檔案，你不曉得我每一次推播都會扣點數。像你這樣改回去又改回來，每次都會扣 15 點……既然你已經做了，現在這些就先不要動，之後所有的修改都在 GitHub 上處理。」

**新增鐵律**：任何時候聽到教練說「推 GitHub」「先推到 GitHub」這類指令，**只要涉及 Netlify 網站，一律先查 `curl /api/v1/sites/{site_id}` 或直接查本記憶檔案裡的站台清單**，確認是不是 GitHub 自動部署型——是的話，「推 GitHub」跟「推 Netlify」是同一個動作，不能分開處理成「先推一半」。這條查證不能跳，即使教練那句話聽起來只是要推 GitHub。

相關記憶：[[project-unrestricted-war-website]]、[[reference-netlify-token]]、[[feedback-web-push-sop]]
