---
name: reference-zip-to-github-pages-deploy-sop
description: 教練丟一個zip/tar.gz靜態網站檔案要求上傳GitHub做成公開網站的完整SOP，2026-09-05在ACER實測兩次成功
metadata:
  type: reference
---

教練外出用這台機器工作時常見的一種任務：手上有一個已經做好、瀏覽器測試過的靜態網站(index.html+assets圖片)zip或tar.gz壓縮檔，要求「解壓縮、上傳到GitHub、做成可公開瀏覽的網站」。2026-09-05本場實測跑通兩次（台南匹克藝術扶輪社、KingMauii品牌網站），流程穩定可重複。

## 完整步驟

1. **解壓縮**：zip用`Expand-Archive`（Windows原生，這個方向沒有Compress-Archive那個反斜線bug，那個bug只發生在「打包成zip」時，「解壓縮」用Expand-Archive安全）；tar.gz用`tar -xzf`。解壓到`/tmp/`暫存，不要直接動教練Downloads資料夾原始檔。
2. **確認repo名稱是否為ASCII**：GitHub repo名稱**不支援中文字元**，用中文檔名下`POST /user/repos`會被靜默過濾成類似`-_-`的殘缺名稱（親身踩過）。**動手前先檢查來源檔名是否含中文/非ASCII字元**，含的話要先跟教練確認英文/拼音替代名稱（或教練授權「隨便取接近的」就直接照established慣例取，比照本作品總表其他站的命名法：`jiesheng-leadership`、`bigtree`、`coach-case`這種風格），不要先建立再返工改名。
3. **取得GitHub token**：這台機器沒裝`gh` CLI，但Windows Git Credential Manager已經快取教練GitHub帳號(Coach1973)的OAuth token，可以直接用這個指令白嫖，不用去憑證檔案翻：
   ```bash
   printf 'protocol=https\nhost=github.com\n\n' | git credential fill
   ```
   拿到的`password=gho_...`就是token，有`repo`權限（可以create/push），**但沒有`delete_repo`權限**（實測刪除回403 Must have admin rights），如果建錯名字，用PATCH改名代替刪除重建。
4. **建repo**（REST API，中文內容一律寫進檔案再用`--data-binary @file`傳，不要用`-d`inline字串，inline字串在這台機器的bash下傳中文會出現`Problems parsing JSON`）：
   ```bash
   curl -s -X POST "https://api.github.com/user/repos" \
     -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
     --data-binary "@payload.json" -o resp.json -w "HTTP_%{http_code}\n"
   ```
5. **push內容**：本機`git init`+`add -A`+`commit`+`branch -M main`，remote URL**暫時**內嵌token(`https://Coach1973:$TOKEN@github.com/...`)push完，push成功後**立刻**`git remote set-url origin`換回不含token的乾淨URL（避免token留在`.git/config`明碼）。push完用`git ls-remote origin main`核對本地commit hash真的出現在遠端，不能只信push指令回傳成功。
6. **開GitHub Pages**：
   ```bash
   curl -s -X POST "https://api.github.com/repos/{owner}/{repo}/pages" \
     -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
     -d '{"source":{"branch":"main","path":"/"}}'
   ```
   回應的`html_url`就是最終網址(`https://coach1973.github.io/<repo>/`)。
7. **驗證上線**：Pages建置需要約60~90秒，第一次curl常常還是404，**不能當作失敗**，等30秒左右重試。驗證要文字+圖片分開查（同[[feedback_image_compression_by_scenario]]、`2026-07-25_ai-talk圖片部署事故檢討報告`同一套紀律）：`<title>`抓得到、任一張`assets/`圖片curl回`200`且`content_type`正確(`image/jpeg`等)，兩項都過才算真的驗證完成，不能只看HTTP狀態碼。

## Why
教練不在家、用這台機器（不一定是Mac或有gh CLI裝好的環境）處理客戶素材是常見情境，這套SOP完全靠REST API+已快取的git credential，不依賴`gh` CLI、不需要教練另外提供token，最大化這台機器「拿到就能用」的即戰力。

## How to apply
下次教練丟類似「幫我把這個zip上傳GitHub做成網站」的任務，直接照上面7步走，不用重新摸索GitHub API或token取得方式。步驟2的ASCII檢查是最容易漏掉、也最浪費一輪來回的地方，務必動手前先看一眼檔名。

Related: [[project_bigtree_eventsignup_sync_rule]]（同樣是「教練要求上傳成公開網站」類任務，但那支是靠Netlify zip API+deploy guard，本篇是GitHub Pages+REST API，兩套機制服務不同的部署型態）
