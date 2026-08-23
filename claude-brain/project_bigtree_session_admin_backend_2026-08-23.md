---
name: project-bigtree-session-admin-backend-2026-08-23
description: 大樹小講場次管理後台＋一鍵發佈上線——event.db成為場次唯一真相源，教練可自行增修場次不必透過AI；教練長期目標是所有活動都歸後台管理
metadata: 
  node_type: memory
  type: project
  originSessionId: 586e8d1b-6f90-4d2f-a3fc-7b66a47f227c
  modified: 2026-08-23T01:28:57.136Z
---

2026-08-23 教練創意發想：想要一個能自己管理大樹小講活動的後台（新增／編輯／刪除、已完成自動列歷史、一鍵部署不用 AI 確認），並問「要做在 GitHub 還是 bymyway 官網」。

**軍師判斷：不新建系統。** `event.bymyway.com/admin`（`workspace/event-signup`，Flask+SQLite，24 小時跑在 Mac mini 上）早就是完整後台。真正的病根是**同一份場次資料同時存在兩個地方**：bigtree 網頁原始碼裡的 `SESSION_DATES` 陣列、以及 `event.db`，兩邊手動同步必定會漏——2026-08-22 改期出包（教練抓到 9/22 排在 8/26 前面）就是漏在這裡。

**做法：`event.db` 成為唯一真相源。**
- `events` 表擴充 `site/slot_key/location/venue/address/transport/status` 欄位，官網 16 場全部匯入（順帶補上 8/26 早半場一直缺的 slug，那場原本報名根本寫不進資料庫）
- `/admin/sessions` 頁：新增／編輯／刪除／設為已取消／草稿。**有報名紀錄的場次不給刪**，只能設「已取消」，避免報名資料變孤兒
- **過期場次自動歸「已結束」**：後台自動分區，且官網前端 `buildSessions()` 也會自動濾掉過期場次——不用教練手動關閉、也不用等下次發佈
- `event-signup/bigtree_publish.py`：資料庫 →產生 `SESSION_DATES` → 寫回 index.html → git commit/push → Netlify 部署，一顆按鈕完成

**教練本人按發佈＝本人授權，不需要 AI 再確認。** 原本「要教練說推才能部署」的規矩是防 AI 自作主張，不是防教練本人；教練自己在後台按按鈕不經過 Claude Code 的 hook，天然不受攔截。

**Why（教練的原始痛點）：** 「目前大樹小講所有的動作我都是要透過你去完成，是比較沒有效率的。」

**How to apply：**
1. 往後大樹小講場次異動，**先問教練要不要自己在後台改**，不要預設由 AI 改網頁原始碼——除非教練明確要 AI 動手，否則優先讓他自主操作
2. 若真的要 AI 改場次，**改資料庫不要改 `index.html` 的 `SESSION_DATES`**（那段現在由程式產生，手改會在下次發佈時被覆蓋）
3. **教練長期目標：「所有活動都歸後台管理」**（不只大樹小講）。欄位已預留 `site` 區分站台，等這套用順了再擴充；`ai-fit` 這類單一活動微站尚未納入
4. 交付這類「教練自己會反覆使用」的自動化工具，務必實測到最後一步——本次首發就因 zip 打包踩到舊坑而失敗，見 [[feedback-netlify-headers-content-type]] 第7條

commit：`bde5ae160`（後台系統）、`7a096531b`（發佈流程兩個 bug 修復＋變動明細文案）
