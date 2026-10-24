---
name: project-game-report-interactive-materials-2026-10-25
description: 互動教材（策展頁，如 bni-gusest）玩完產生學習報告的通用系統：POST /api/game/report、/game-report/<代碼>、/gr/<碼> 講師後台；第一個用的是 BNI 來賓接待工作坊（教練與孫林博士共同創作），已放上 drsoonlin 頁「共同創作」區
metadata:
  type: project
---

教練 2026-10-25 交辦：bni-gusest 互動遊戲要「真的可以輸入、可以玩、最後產生報告」，做好放在孫林博士（Dr. Soonlin，drsoonlin 頁）網頁，因為是兩人共同創作。

**做法**：遊戲頁是靜態 HTML（github_repos/bni-gusest），作答原本只在瀏覽器。新增後端 `workspace/event-signup/game_report.py`＋app.py 三個網址：`POST /api/game/report`（遊戲頁整理成「sections／scores／feedback／takeaway」格式送上來，site＝策展代號，姓名【測試】開頭不發通知）、`/game-report/<代碼>`（個人報告頁，noindex，可列印）、`/gr/<碼>`（講師後台短網址，已收進大樹作品集「活動後台」）。完成通知進「活動報名即時通知」群。測試 `cd event-signup && venv/bin/python test_game_report.py`（14 項，暫時資料庫＋假通知）。

**別的互動教材要出報告**：照同格式 POST，site 填策展代號（要在策展名冊裡），前端照 bni-gusest 最下面「學習報告」區與 `buildReport()` 寫。報告資料表 `game_reports`（event.db，改前備份在 state/backup_20261025_game_report/）。

**坑**：①改 app.py 要 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`；②驗證用 Chrome 從頭玩一次再按產生，驗完刪測試報告（`game_report.delete(token)`）；③截圖有鎖，用程式量尺寸；④教練字級規定最小 20px，改到這站就一起調。

commit：workspace `f202ba9c3`、bni-gusest `65d76a6`、drsoonlin `dbef2a7`。**還沒有真人送出過報告**，第一位學員送出時才算真實驗證通知。

相關：[[feedback-new-admin-urls-auto-register-coach888-2026-10-10]]、[[feedback-web-font-min-20px-2026-10-14]]
