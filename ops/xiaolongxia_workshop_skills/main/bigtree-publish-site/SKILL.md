---
name: bigtree-publish-site
description: 教練要把網站／作品放上 event.bymyway.com 時使用——「上架」「走大樹創作 SOP」「走策展 SOP」「放到策展中心」「後面檔名寫 xxx」「給我一個網址」，或傳來網頁 zip／html 說要上線。先分清楚是教練自己的作品還是別人的網站，選短網址，上傳，確認上線，網址獨立一行回覆。
---

# 上架網站（完整規則：`~/.openclaw/workspace/knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`，動手前讀它）

起因：9/23、9/24 教練兩度說「走大樹創作 SOP」，小龍蝦卻走了店家策展、插進大台南商圈卡片，教練還得刪掉重來。

## 步驟

1. **先分「誰的網站」**（不是看是不是店家）：
   - 教練自己的作品（教練的講座、漫畫、報告、個人品牌頁）→ `kind=creation`，**不進大台南商圈**。
   - BNI 夥伴、朋友、客戶的網站 → `kind=shop`。
   - 聽到「大樹」＋「作品／創作」＋「上架／SOP」任意組合 → 一律 creation。
2. **短網址**：教練說了「後面檔名寫 xxx」→ 直接用，不問。沒說 → 一次給三個候選（10 字內小寫英文數字連字號、先查 `~/.openclaw/workspace/event-signup/curated_sites_registry.json` 不撞名、標推薦哪個）＋「或您自己指定」，每個網址獨立一行。這是唯一要停下來等教練的點。
3. **圖片影片不用先壓縮，也不要問要不要壓縮**（伺服器會自動壓）。
4. **上傳**（金鑰不要印出來）：
   ```bash
   KEY=$(grep '^CURATION_UPLOAD_KEY=' ~/.openclaw/workspace/event-signup/.env | cut -d= -f2)
   curl -s -F "kind=creation" -F "package=@<檔案>" -F "custom_slug=<短網址>" "https://event.bymyway.com/curation/upload?key=$KEY" -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
   ```
5. **等 10～20 秒確認結果**：`python3 ~/.openclaw/workspace/scripts/curation_check_result.py <短網址>`，再 `curl -sI https://event.bymyway.com/curated/<短網址>/` 要 200。
6. **回覆教練**：一句「已上架」＋網址獨立一行（後面不黏任何字）。

## 檔案太大（Telegram 超過 20MB 收不到）
請教練用手機打開大樹作品集「大樹常用」裡的「作品上傳頁」，選「大樹教練個人作品」→選檔→填短網址→上傳，沒有 20MB 限制。這是唯一需要教練自己動手的情況，原因是檔案傳不進 Telegram。
