---
name: bigtree-publish-site
description: 教練要把一個網站／作品放上 event.bymyway.com 時使用——「上架」「走大樹創作 SOP」「走策展 SOP」「放到策展中心」「收進作品一覽」「給我一個網址」「這個 zip 幫我上」。決定是誰的網站、選短網址、上傳、等系統自動處理、驗證、交付，一次走完。
---

# 上架網站（完整規則在 `knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`，動手前讀它）

## 步驟

1. **先分「誰的網站」**（不是看是不是店家）：
   - 教練自己的作品 → `kind=creation`（不進大台南商圈）。
   - BNI 夥伴、朋友、客戶的網站 → `kind=shop`（策展店家）。
2. **短網址**：教練一開始就指定 → 直接用，不問。沒指定 → 一次給三個候選＋第四個「由您自己指定」（10 字內、小寫英文數字連字號、先查 `event-signup/curated_sites_registry.json` 不撞名、標出推薦哪個、每個網址獨立一行）。這是整個流程**唯一**要停下來等教練的點。
3. **圖片影片不用先壓**（伺服器上傳時自動跑 `scripts/optimize_site_assets.py`），也不要問教練要不要壓縮。
4. **上傳**（金鑰在 `event-signup/.env` 的 `CURATION_UPLOAD_KEY`，不要印出來）：
   ```bash
   KEY=$(grep '^CURATION_UPLOAD_KEY=' ~/.openclaw/workspace/event-signup/.env | cut -d= -f2)
   curl -s -F "kind=creation" -F "package=@<zip>" -F "custom_slug=<短網址>" \
     "https://event.bymyway.com/curation/upload?key=$KEY" -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
   ```
5. **等系統處理完**（通常 10～20 秒，會自動建 GitHub 倉庫、收進作品一覽、通知「活動報名即時通知」群）：`python3 ~/.openclaw/workspace/scripts/curation_check_result.py <短網址>`。卡住超過幾分鐘 → 看記憶 reference_curation_pipeline_stuck_diagnosis_2026-10-15。
6. **驗證**：
   - 網頁 `curl -sI https://event.bymyway.com/curated/<短網址>/` 要 200 且 `text/html`；每張圖 `curl -sI` 要 200 **且** Content-Type 是圖片（狀態碼對、Content-Type 錯，瀏覽器照樣不顯示）。
   - `python3 ~/.openclaw/workspace/scripts/module_kit.py check <短網址>`（送出資料有接、字 ≥20px、有 GitHub）。
   - 真瀏覽器 1280／390 寬量：沒有左右捲動、圖都有載入。
7. **有表單**：聯絡／索取資料一律打 `POST /api/works/contact`；活動報名走 `bigtree-event-signup` 技能。教練是講師＋有報名 → 該場 `events.site` 改成 `bigtree`（列入大樹小講）。
8. **新的後台／編輯網址** → 同一輪收進大樹作品集：`python3 ~/.openclaw/workspace/scripts/coach888_register_admin.py`，`--list` 讀回確認。
9. **交付**：`bash ~/.openclaw/workspace/scripts/deliver_open.sh <網址>`；網址獨立一行。

## 不要做
- 不用 Netlify（要教練說「推」才部署，`netlify_deploy_guard.sh` 會擋）。
- 不在 `~/github_repos/<slug>` 裡 checkout 別的分支驗收（那裡＝線上，切了就上線）。
