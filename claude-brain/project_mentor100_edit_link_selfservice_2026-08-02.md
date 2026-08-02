---
name: project-mentor100-edit-link-selfservice-2026-08-02
description: mentor100後台admin_list.html新增「複製修改連結」按鈕，教練可自行取得任一導師的edit_token連結轉發，不用每次都問AI查資料庫
metadata:
  type: project
---

教練問「老師想改資料但遺失自己的修改連結，我可以怎麼做立即發給他，不用每次都問你」——已在`/Users/bymyway/github_repos/mentor100/templates/admin_list.html`每列導師新增「複製修改連結」按鈕，點擊用`navigator.clipboard.writeText`把該導師`/join/edit/<edit_token>`完整網址複製到剪貼簿，教練登入`/admin`找到老師名字、點按鈕、貼到LINE發給對方即可，全程不用問AI。

**Why:** `edit_token`欄位本來就存在`mentors`資料表且已對所有40筆資料補齊（`db.py`的`init_db()`會自動幫舊資料補token），只是後台名單頁面本來沒有顯示這個連結——純UI缺口，不是資料缺口。專案自己的`CONTEXT.md`第26~30行「已知教訓」段落其實已經預先寫好這個答案（「若教練提到『舊導師沒有後台權限』，答案不是要開發新的權限系統，是查`mentors.edit_token`給他們對應連結」），這次直接照著做，證實**進新專案先讀`CONTEXT.md`**這個習慣有實際省時間的效果。

**How to apply:** 未來教練提到任何「導師/來賓/會員忘記自己的連結」類需求（尤其是token-based免密碼系統，如mentor100/event-signup這類專案），優先檢查後台管理頁面能不能直接顯示或一鍵複製該筆記錄的專屬連結，而不是每次由AI手動查資料庫回報。改動只碰`templates/admin_list.html`（純模板+前端JS，無後端邏輯變更），commit `820436c`（mentor100獨立repo，非workspace主repo），已push到`github.com/Coach1973/mentor100`。服務透過launchd管理（`com.coach.mentor100-webapp`），改完模板記得`launchctl kickstart -k`重啟才會生效（Flask未開debug模式，模板不會自動熱重載）。
