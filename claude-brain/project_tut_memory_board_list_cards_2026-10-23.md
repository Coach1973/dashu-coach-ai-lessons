---
name: project-tut-memory-board-list-cards-2026-10-23
description: 南應大記憶牆「加入校友會」第三張卡改成「理監事校友名單」（照 mentor100 卡片版型，23 位）；資料放哪、怎麼補照片簡介職稱連結；同輪把整站字級調到 20px
metadata:
  node_type: memory
  type: project
  originSessionId: c2ca99d7-473c-431c-a47c-501f10611947
  modified: 2026-10-22T18:10:02.790Z
---

教練 2026-10-23 02:00 交辦：把 mentor100（AI 百人導師）的「照片＋名字＋職稱＋簡介按鈕」卡片架構，搬到 https://event.bymyway.com/curated/tut-memory/#join 的「終身校友網絡」，改名「理監事校友名單」，名單 23 位由教練貼。

- 程式：`~/github_repos/tut-memory/index.html`（改了就上線，main 分支）。資料在 JS 陣列 `BOARD`（每人一行 `{name,title,bio,photo,links:[{label,url}]}`，欄位同 mentor100）；點卡片區的「理監事校友名單」展開，「簡介」按鈕開視窗。簡介跟連結都空的人沒有簡介按鈕、照片空顯示姓名首字。
- 教練要補的「照片、簡介、職稱、超連結」就改那一行；照片放 `images_web/board/`（換圖要換檔名，快取 4 小時）。教練是透過 AI 補，不要叫他自己改程式。
- 「AI 版導出檔格式」我解讀為 mentor100 的欄位（姓名、職稱、簡介、照片、連結）；教練沒糾正。
- 名單是教練 02:00 貼的 23 人，順序照貼；陳佩君在名單裡（也是 2027 理事長候選人）。
- 同輪整站字級調到 ≥20px（教練 10/14 規則：改到那站一起調）；選單字變大，漢堡選單改 ≤960px 才收合。剩 3 處刻意不動：圓形郵戳 9px／7.5px 與箭頭 ▾ 12px（裝飾，aria-hidden）。
- commit：86e1f7b（功能）、8fb3e49（字級＋選單）。
- 另有 `/tut/team`（event-signup 的理監事與顧問自助簡介頁，10/14 做的）理監事仍是空的；教練這次沒要求合併，沒動。

**Why:** 下次教練說「補某某的照片／簡介／職稱／連結」就直接改 BOARD 那一行，不用重查結構。
**How to apply:** 先 `git pull` 再改；改完用 Chrome 開 live 頁量 23 張卡與手機寬度；相關：[[project-tut-team-page-and-zhengui-copy-2026-10-14]]、[[feedback-web-font-min-20px-2026-10-14]]
