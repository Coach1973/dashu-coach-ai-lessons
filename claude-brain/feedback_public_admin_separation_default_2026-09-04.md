---
name: feedback-public-admin-separation-default
description: 任何要給外部人(學員/來賓/客戶)看的網頁，管理功能(新增/刪除/勾選公開)絕對不能跟公開內容共用同一個網址
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-03T21:37:17.002Z
---

建學員/來賓/客戶會看到的網頁時，管理控制項（新增表單、刪除按鈕、勾選公開清單等）必須放在獨立的 `/xxx/admin` 網址，公開網址只渲染教練勾選過的乾淨內容，這是**一開始設計就要內建的預設**，不是等教練發現問題才補救的事後修正。

**Why:** 2026-09-04 教材線上觀看系統(`/materials/`)第一版把新增教材表單、42份檔案的公開/隱藏勾選清單全部放在同一個網址，教練問「我沒有看到我的後台啊，我的後台是哪一個？」才發現——如果照原計畫把這個網址直接傳給學員，學員會看到教練的管理介面、還沒公開的檔案標題清單、以及刪除按鈕。這不只是體驗差，是真的會洩漏未公開內容+給外部人可乘之機的設計漏洞。

**How to apply:** 只要任務描述包含「給學員看」「給來賓看」「公開網址」「分享連結」這類外部受眾字眼，動手前先問自己：這個網址教練自己會不會也用來管理內容？如果答案是會，就必須從架構上直接拆成兩個路由（`is_admin` flag 或獨立 route 都可以），不要等到教練親眼確認才拆。參考實作：`event-signup/app.py` 的 `materials_page`(公開)/`materials_admin`(後台) + `templates/materials.html` 用 `{% if is_admin %}` 包住所有管理控制項。

Related: [[project_materials_viewer_system_2026-09-04]]
