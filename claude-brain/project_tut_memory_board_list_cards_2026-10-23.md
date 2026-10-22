---
name: project-tut-memory-board-list-cards-2026-10-23
description: 南應大理監事 23 位：記憶牆「理監事校友名單」與 /tut/team 共用同一份資料（event.db tut_team_members board）；教練的「建置模式」短網址 /tut/m、/tut/b 可直接點卡片補照片簡介；整站字級 20px
metadata:
  node_type: memory
  type: project
  originSessionId: c2ca99d7-473c-431c-a47c-501f10611947
  modified: 2026-10-22T18:26:05.741Z
---

教練 2026-10-23 02:00～02:30 交辦：mentor100 的卡片架構搬到 https://event.bymyway.com/curated/tut-memory/#join（「終身校友網絡」改「理監事校友名單」），23 位名單由教練貼；又要求 /tut/team「兩邊同時都要有同一份資料」；又罵「沒有任何按鈕可以上傳照片跟修改、列出來沒照片沒簡介要幹嘛」，要「使用者找到自己位置點進去就能傳照片編輯簡介（像信任遊戲，他口誤說『新人遊戲』）」，且建置期間只有教練在用、要能直接在頁面上點。

**資料只有一份**：`workspace/event-signup/event.db` 的 `tut_team_members`（team='board'，23 位，順序照教練貼；`BOARD_SEATS` 在 `tut_team.py`，第一次用到自動放空座位）。記憶牆（`~/github_repos/tut-memory/index.html`）載入時讀 `GET /api/tut/team/board`（CORS *、no-store），讀不到才用頁內備援名單 `BOARD`（只有名字，不要在那邊補資料）。

**教練補資料的方式（建置模式）**：他的專屬短網址（簽章碼＝後台同一個 `admin_code`，碼存在服務環境，算法 `tut_team.admin_code(EVENT_SECRET_KEY)`；要算得 `source event-signup/.env` 後再 import app）：
- `https://event.bymyway.com/tut/m/<碼>` → 記憶牆理監事名單，每張卡「✏️ 編輯」
- `https://event.bymyway.com/tut/b/<碼>` → /tut/team 建置模式，每張卡「✏️ 編輯」
兩條都已收進大樹作品集「活動後台」與 /vault。編輯頁 `?build=碼`：職稱、簡介、照片可以只補其中一項、不發通知群。一般訪客：未填座位有「這是我，補簡介」（POST /tut/team/claim/<id> → 編輯頁，已補完的不能再認領）。

**🔴 同步鐵律（教練 10/23 02:25 親口：「不管透過記憶牆編輯，還是透過 /tut/team 專頁，只要其中一頁變更，兩邊都要同步」）**：理監事資料只准存在資料庫 `tut_team_members` 一份；記憶牆沒有自己的資料，編輯按鈕也都跳到 /tut/team 的編輯頁，所以任何一邊改都寫同一張表。往後不准在記憶牆頁面裡另存第二份資料、不准加快取（網址、介面都要維持 no-store）；若之後改成記憶牆能直接存檔，也一定要寫回資料庫。頁內 `BOARD` 備援名單只有名字，連不上時才用。

**坑**：
- `workspace/event-signup` 在 worktree 對話裡 Edit 工具會被擋，用 python 精準替換（比對剛好 1 處）＋改前 `sqlite3 .backup` 與複製原檔到 `workspace/state/backup_20261023_tut_team_board/`；commit 用 `git commit -- <路徑>`（workspace 常有大量別人的未提交變更）。
- 改完要 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`；測試 `cd event-signup && venv/bin/python test_tut_team.py`（77 項，用暫時資料庫）。
- 23 位都不在名片庫；event.db 其他表只有陳佩君（嗨餅乾藝術策展人）等同名紀錄，無法確定是同一人，沒帶入。照片、職稱、簡介都還是空的，等教練補。
- 字級：記憶牆與 /tut/team 整頁已 ≥20px（兩個帶 inherit 的 font 簡寫已拆開）；記憶牆選單改 ≤960px 才收漢堡；僅郵戳 9px／7.5px 與箭頭是裝飾保留。

commit：記憶牆 86e1f7b、8fb3e49、1c6d068；workspace 6dd7d087a。

**Why:** 下次教練說「補某人的照片／簡介」「為什麼不能改」直接用上面的機制，不要再叫他自己改程式或找 token。
**How to apply:** 先看這份再動；相關：[[project-tut-team-page-and-zhengui-copy-2026-10-14]]、[[feedback-web-font-min-20px-2026-10-14]]、[[feedback-new-admin-urls-auto-register-coach888-2026-10-10]]
