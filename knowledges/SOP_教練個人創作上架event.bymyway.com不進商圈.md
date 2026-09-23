# SOP：教練個人創作（非店家）上架 event.bymyway.com，不進大台南商圈整合中心

> 🔴 **教練口語別名（一定要認得，教練不會念這份檔名）**：「走大樹創作SOP」「大樹作品SOP」「大樹作品上傳」「大樹創作」——聽到這幾種說法，就是指這份文件，**不是**`reference-curation-sop-2026-09-06`（店家策展SOP）。
>
> 2026-09-23 教練親自交辦「ai-story」漫畫案建立。跟既有「策展SOP」共用同一套 `/curated/<slug>/` 網址與檔案格式，差別只在**跳過店家專屬的三個步驟**。
>
> ⚠️ **2026-09-23 23:55~00:02（台灣時間）復發記錄**：教練當晚兩度明講「走大樹創作SOP」（送 zhaolin 人像照＋送 ai-application-submission-package zip），小龍蝦仍然跑了店家策展SOP、插了大台南商圈卡片，教練事後手動刪除。根因是這份SOP檔名跟教練嘴巴講的詞完全對不上、也沒有任何路由表指到這裡，AI 在壓力下預設用「最熟的那條路」（已用過很多次的店家策展SOP）。修復：已在 `路徑大全_憑證層.md` 的策展金鑰前+`AGENTS.md`按需讀取路由都補上別名警告，並在本檔加上這段別名清單。

## 適用情境
教練自己用外部 AI 工具（TAVA AI／Lovart／ChatGPT 等）做的個人創作（漫畫、故事、作品集……），只想放上 `event.bymyway.com` 有個網址可以分享，**不是店家/夥伴介紹網站**，不該出現在大台南商圈整合中心的店家名冊。

## 跟「策展SOP」的關鍵差異
既有 [[reference_curation_sop_2026-09-06]] 是為店家設計的，會自動做三件事，這三件事對個人創作都是不必要甚至錯誤的：
1. 抓地址、猜分類，插入大台南商圈整合中心店家名冊卡片
2. 自動發大台南商圈整合中心 FB 貼文宣布
3. 建立獨立 GitHub repo + 開 GitHub Pages（教練這次沒要求，只要 event.bymyway.com 一個網址）

**教訓案例**：2026-09-23 教練把「ai-story」漫畫包丟給小龍蝦，小龍蝦直接照策展SOP整套跑，被誤判成店家上架，後續處理（很可能是用 `/curation/admin/delete` 下架）連帶把 GitHub repo、Pages、registry 全部砍掉，導致 `event.bymyway.com/curated/ai-story/` 變 404、`log` 卻仍顯示「✅完成」——log 只代表當初上架流程本身沒有丟例外，不代表後來沒被整組刪除，兩者是不同時間點的事，查證時不能只看 log 就下結論。

## 正確做法（不需要教練重新上傳，本機直接可查到原始包）
1. **找到原始包**：教練說「打包給小龍蝦」，通常會落在
   `event-signup/curation_uploads/processed/<時間戳>__<檔名>.zip`（已處理過）或
   `event-signup/curation_uploads/incoming/`（還沒處理）。教練若同時貼過對話記錄或截圖，也可以在 `claude-brain/data/` 底下找到對應日期的資料夾。
2. **直接解壓縮到 `/Users/bymyway/github_repos/<slug>/`**（跟策展SOP用同一個根目錄，Flask 就是從這裡讀），保持檔案內容**完全不動**——教練要的是「原汁原味」，不要重新設計版面、不要換字型大小、不要加自己的排版巧思。
   ```bash
   unzip -q <zip路徑> -d /tmp/extract
   rsync -a /tmp/extract/<zip內的子資料夾>/ /Users/bymyway/github_repos/<slug>/
   diff -rq /tmp/extract/<子資料夾> /Users/bymyway/github_repos/<slug>/  # 逐檔比對確認一模一樣
   ```
3. **手動登記進 `event-signup/curated_sites_registry.json`**，不要跑 `scripts/curation_process.py`（那支腳本會執行上面三個店家專屬步驟）。用 Python 直接在 `sites`陣列補一筆：
   ```python
   {
     "slug": "<slug>",
     "title": "...",
     "description": "...",
     "category": "教練個人創作",
     "event_url": "https://event.bymyway.com/curated/<slug>/",
     "github_pages_url": "",
     "uploaded_at": "YYYY-MM-DD HH:MM",
     "status": "live",
     "source_package": "<原始zip檔名>",
     "no_shop_card": true
   }
   ```
   `no_shop_card: true`這個欄位是延用 2026-09-17 bigtree-1003 事故修復時就有的既有慣例（見接力棒 v220 前後），意思是「這筆有效但不是店家，不進名冊」。
4. **不用重啟 Flask**——`app.py` 的 `_load_curated_registry()` 每次請求都重讀 JSON，寫檔案存檔當下就生效。
5. **驗證**：`curl -sI https://event.bymyway.com/curated/<slug>/` 確認 200，再抓一段內容文字比對確認真的是原始版本（不是被哪個環節動過手腳）。
6. **🔴 登記進 coach888「AI作品一覽」，跟上架動作同一輪完成，不要等教練問才補**——這條規則其實[[reference_curation_sop_2026-09-06]]第56~57行早就寫了（「教練自己的作品→收coach888」，2026-09-05教練親定），2026-09-23第一次做這個SOP時漏做，教練事後問「為什麼老是忘記」才發現。做法：
   - `cd /Users/bymyway/github_repos/coach888 && git pull`
   - 在 `index.html` 找 `data-section="gongkai"`（對外公開分類）的 `<div class="grid" ...>`，把新項目插在**第一個** `<div class="item" ...>` 之前（既有規則：coach888新增項目一律放分類第一筆），其餘項目的 `<div class="num">` 依序遞增，`<span class="count">N項</span>` 的 N 一併更新
   - `git add index.html && git commit ... && git push origin master`（**注意這個 repo 預設分支是 `master` 不是 `main`**）
   - 驗證：GitHub Pages 部署有延遲（實測約15秒），`curl https://coach1973.github.io/coach888/` 確認新項目字樣出現才算完成，不要 push 完就回報完成

## 明確不要做的事
- 不要跑 `python3 scripts/curation_process.py`（會觸發店家三步驟）
- 不要呼叫 `insert_tainan_shangquan_card()`
- 不要呼叫 `post_to_facebook()`
- 不要自己重新設計版面/改字型大小/加自己的詮釋——教練要「一模一樣」就是像素級不動，有意見用視覺重新設計時，先問清楚教練是要「完全模仿」還是「做得更好」，不要自己預設立場硬改
