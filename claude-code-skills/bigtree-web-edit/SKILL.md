---
name: bigtree-web-edit
description: 教練要改既有網頁時使用——「改網頁」「這頁改一下」「字太小」「照片換一張」「這段文字改成…」「為什麼網頁沒變」「手機版跑掉」。從找到網頁背後的檔案、改、用真瀏覽器量、推上線、確認線上版，到交付網址，一次走完。
---

# 改網頁（教練不分 GitHub 跟網頁：改 GitHub＝改網頁）

## 步驟

1. **找到檔案，不猜**：
   - 教練給網址 → `event.bymyway.com/curated/<slug>/` 直接讀 `~/github_repos/<slug>/`（改了就是上線）；`coach1973.github.io/<repo>/` 是 GitHub Pages，倉庫在 `~/github_repos/<repo>/`。
   - 找不到 → 先查作品一覽 `coach1973.github.io/all-works`（三來源去重、可搜人名），再查 `event-signup/curated_sites_registry.json`。
   - 進倉庫先跑 `git branch --show-current`，push 用它印出來的名字（分支守門會擋寫錯的分支名）。
2. **改之前先備份原檔**（`cp index.html index.html.bak-日期` 放倉庫外的暫存區）。
3. **改的規矩**：
   - 字最小 20px（`python3 ~/.openclaw/workspace/scripts/module_kit.py check <slug>` 會擋 px 寫法；`font` 簡寫加 `inherit` 會整條失效）。
   - 版面重疊：保持原位置、讓區塊加高把字往下推，**不可以橫移去遮照片人物**。
   - 頂部選單加項目前先量寬度（20px 字多一項就會折兩行）；手機選單用共用 `nav-burger.js`。
   - 數字類先分清楚是「目標」還是「目前進度」（100 席位≠已 100 位）。
   - 換圖一定換檔名（伺服器圖片快取 4 小時）。
4. **用真瀏覽器量，不截圖**（教練禁截圖）：內建瀏覽器先 `resize_window` 設 1280 與 390 寬再量；檢查 `scrollWidth<=clientWidth`（手機沒有左右捲動）、圖片 `naturalWidth>0`、最小字級。
5. **推上線**：`git add <改的檔> && git commit -m "[Mac] …" && git push origin <分支>`。
6. **確認線上版真的變了**：`curl -s "<網址>?v=$RANDOM" | grep <新文字>`。GitHub Pages 部署要 1～2 分鐘；沒變先重試，再查 `gh api repos/Coach1973/<repo>/pages/builds/latest`（errored 就 `gh api -X POST repos/Coach1973/<repo>/pages/builds` 重跑）。
7. **交付**：`bash ~/.openclaw/workspace/scripts/deliver_open.sh <網址>`（直接跳出 Chrome）。回報第一次就講：「已推上、線上已確認；如果您那邊還是舊的，等 1～2 分鐘再按 Ctrl+F5（瀏覽器快取 10 分鐘）」。網址獨立一行，後面不黏字。
8. 如果這次做出新的後台／編輯／刪除網址 → 同一輪收進大樹作品集：`python3 ~/.openclaw/workspace/scripts/coach888_register_admin.py`（用 `--list` 讀回確認）。

## 相關記憶
feedback_github_edit_is_the_web_edit_say_wait_and_cache_2026-10-15、feedback_web_font_min_20px_2026-10-14、feedback_layout_fix_keep_position_dont_cover_photo_subject_2026-10-13、feedback_nav_add_item_measure_width_with_20px_font_2026-10-14、feedback_number_change_target_vs_progress_2026-10-14
