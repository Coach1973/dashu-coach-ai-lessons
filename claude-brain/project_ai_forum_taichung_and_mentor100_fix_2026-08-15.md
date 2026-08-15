---
name: project-ai-forum-taichung-and-mentor100-fix-2026-08-15
description: AI微論壇台中場(9/23-24)網頁概念稿建置進度+mentor100後台500錯誤根因(刪除記錄未清理外鍵)修復
metadata:
  type: project
  originSessionId: d28daa55-7874-4efb-9ad7-7a9774b6549f
  modified: 2026-08-15T10:30:27.743Z
---

**AI微論壇台中場進度**：教練9/23-24（週三週四，09:00-17:00）在台中沃茲新創空間忠明館辦兩天收費活動（單日1800元/兩日套票2988元），9位講師（含大樹教練兩天各一場專屬分享）。新建`Coach1973/ai-forum-taichung`，GitHub Pages概念稿：https://coach1973.github.io/ai-forum-taichung/ 。經教練十餘輪逐步調整定案（套票價格、大樹教練固定排下午第一堂、場地地址、議程早2晚3、含餐點、藍新金流付款連結、亮點bar字級統一、講師照片裁切修復）。**講師資料狀態（2026-08-15）**：8位已從mentor100完整撈取（大樹教練/JC老師原書銘/Lavi即林佳伶/曾思遠/李中閔/施育廷/廖韋評/王俊甫已改草稿），**唯獨彭晉澄完全查無mentor100任何記錄**，是唯一卡住項，需教練提供才能補上，補上後記得同步標記種子。

**mentor100後台500錯誤真根因（技術debug SOP參考）**：`db.delete_mentor()`（`github_repos/mentor100/db.py`）原本只執行`DELETE FROM mentors`，沒有同步清理`applications`表指向該id的外鍵。教練刪除某位導師後，申請名單裡仍有一筆記錄的`mentor_id`指向已不存在的id，變成孤兒外鍵。`templates/admin_list.html`渲染這筆記錄時嘗試`url_for('join_edit', token=a.edit_token)`，因為LEFT JOIN查不到對應mentor記錄，`edit_token`是None，`url_for`必要參數為None直接拋`werkzeug.routing.exceptions.BuildError`，整頁500。**排查方法可複用**：看到`/admin`類頁面500，先查`webapp.error.log`找`BuildError`關鍵字，追溯是哪個模板變數的欄位是None，再往上查資料庫關聯（LEFT JOIN後某欄位為NULL通常代表外鍵指向的記錄已被刪除）。已修復：①`delete_mentor()`刪除時同步`UPDATE applications SET mentor_id=NULL`②模板判斷從`not a.mentor_id`改`not a.edit_token`雙重防護。commit`87031ec`。

**mentor100功能缺口（教練要求後補上）**：後台原本完全沒有「把已發佈的講師改回草稿」的功能入口——`admin_mentor_edit`從未處理過`status`欄位。新增`db.toggle_mentor_status()`+`/admin/mentors/<id>/toggle-status`route+列表頁一鍵切換按鈕。commit`23304df`。

**Why**：mentor100是教練親自營運的百人導師計畫核心系統，後台當機直接影響教練日常操作；AI微論壇台中場是收費活動，講師資料/金流連結錯誤會直接影響報名者信任感與實際收款，兩者都是高風險生產環境操作，修復/驗證都用真實app物件模擬render_template()而非僅推論。

**How to apply**：往後mentor100任何「delete」類操作（刪除導師、刪除申請等），修改前先確認有沒有其他表透過外鍵引用這筆記錄，避免重演孤兒外鍵bug；AI微論壇台中場網頁後續修改，先查這則記憶確認講師資料最新狀態，避免重複查證mentor100。
