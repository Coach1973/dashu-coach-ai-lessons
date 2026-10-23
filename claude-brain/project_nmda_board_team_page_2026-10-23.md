---
name: project-nmda-board-team-page-2026-10-23
description: NMDA（中華新媒體影音發展協會）網站新增「理監事團隊」頁 team.html：照南應大 tut_team 機制複製成 nmda_team.py，名單先放陳佩君、吳大樹空座位，本人點名字補照片簡介；建置模式短網址與後台已收進大樹作品集
metadata:
  node_type: memory
  type: project
  originSessionId: a2cfaed8-7619-4c27-809a-b58ba08013e0
  modified: 2026-10-23T07:19:07.136Z
---

教練 2026-10-23 15:12 交辦：在 https://event.bymyway.com/curated/nmda/ 多一頁「理監事團隊」，照 tut-memory #join 那套（來自 AI 百人導師機制：使用者隨時點進去補資料）；名單還沒有，先放陳佩君、吳大樹，之後直接在頁面上補。

**做法（照「一模一樣＝抄程式只換資料」）**：不改南應大 `tut_team.py`，整份複製成 `workspace/event-signup/nmda_team.py`（獨立資料表 `nmda_team_members`、只有一個團隊、拿掉科系年欄位、簽章鹽 `nmda-team-admin`、NMDA 紅黑米色、字級 ≥20px）。路由在 `app.py`「校友回憶牆」註解前一段：`/api/nmda/team/board`（CORS *、no-store）、`/nmda/team/{join,claim/<id>,edit/<token>,photo/<name>,a/<code>}`、`/nmda/b/<碼>`。公開頁是 NMDA 倉庫自己的靜態檔 `github_repos/nmda/team.html`（不是 team/ 子資料夾，策展伺服器的子路徑對 `team/` 不回 index），載入時讀 API，一律 textContent 不用 innerHTML。首頁導覽加「理監事團隊」，首屏加「認識理監事團隊」按鈕（手機導覽文字連結會被隱藏，所以首屏按鈕必要）。

**教練補資料**：建置模式短網址 `/nmda/b/<碼>`（碼同後台簽章＝`nmda_team.admin_code(app.secret_key)`，要 `source event-signup/.env` 後 import app 才算得出）→ 每張卡「✏️ 編輯」，可只補照片。一般訪客：空座位按「我是○○，補上我的簡介」。兩個網址都已收進大樹作品集「活動後台」與 /vault。座位只有名字，職稱簡介照片都空著，沒替本人編。

**坑 / 驗證**：測試 `cd event-signup && venv/bin/python test_nmda_team.py`（27 項，暫時資料庫、假通知）。Edit 對 workspace 會被擋，用 python 精準替換（備份在 `workspace/state/backup_20261023_nmda_team/`，含 app.py.orig 與 event.db.bak）；改完要 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`。截圖有鎖（要教練同意才 touch SCREENSHOT_APPROVED），用 get_page_text＋javascript 量尺寸驗證；Chrome 縮窗沒生效，手機寬度用「fetch 頁面 → srcdoc iframe 375px」量。公開頁手機沒橫向捲動。

commit：nmda `5b965f8`；workspace `7b3c08f26`。

**Why:** 下次教練說「協會要加理監事／顧問團隊頁」「像理監事名單那樣能自己補資料」，直接複製這套（nmda_team.py → 換名稱）。
**How to apply:** 先看這份再動；相關：[[project-tut-memory-board-list-cards-2026-10-23]]、[[feedback-identical-means-copy-the-reference-code-2026-10-21]]、[[feedback-new-admin-urls-auto-register-coach888-2026-10-10]]
