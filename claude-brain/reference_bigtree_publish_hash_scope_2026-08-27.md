---
name: reference-bigtree-publish-hash-scope-2026-08-27
description: bigtree_publish.py的一鍵發佈只比對events資料庫產生的SESSION_DATES內容有沒有變，index.html裡其他區塊（如報名成功彈窗文案）改了不會被偵測到，會誤判「已是最新」拒絕部署
metadata:
  type: reference
  originSessionId: f1ddb5b1-0158-46e6-8dd7-c3fae93c6e38
  modified: 2026-08-27T10:36:05.077Z
---

`event-signup/bigtree_publish.py`的`publish()`函式一開始會比對`target_hash`（由`render_session_dates(rows)`算出，只涵蓋資料庫events表驅動的那段`const SESSION_DATES = [...]`）跟`_get_published_hash(conn)`是否相同，相同就直接回傳「官網已經是最新內容，沒有需要發佈的變更」並中止，不會往下走git commit/push/Netlify部署。

這代表：如果只改了`index.html`裡SESSION_DATES**以外**的地方（例如成功彈窗文案、Hero區塊文字、任何純內容/樣式調整），這支腳本會誤判成「沒有變更」而拒絕部署，即使檔案內容其實真的改了。2026-08-27實際發生過：改報名成功頁的LINE加入誘因文案後跑`bp.publish()`，回傳`{'ok': False, 'step': '產生網頁', 'message': '官網已經是最新內容，沒有需要發佈的變更。'}`，但Chrome實際打開本機預覽確認文字真的改了。

**Why：** `bigtree_publish.py`設計初衷是解決「event.db跟index.html的SESSION_DATES兩份資料各自維護會漏改」的問題（見[[project_bigtree_session_admin_backend_2026-08-23]]），它的去重檢查天生只看得到自己負責的那個區塊，不是整份`index.html`的通用diff機制——這是範圍設計使然，不是bug。

**How to apply：** 之後改`bigtree/index.html`時，先判斷改動範圍：
- 只改SESSION_DATES場次資料（新增/改期/改費用等）→ 照常用`bp.publish(conn, message=...)`（記得`NETLIFY_DEPLOY_CONFIRMED=1`前綴）
- 改到其他區塊（文案/版面/彈窗等，不涉及場次資料）→ `bp.publish()`會擋下來，改用手動流程：`git add/commit/push` → 依bigtree_publish.py原始碼裡記載的成功配方手動打包（`git archive HEAD`解到暫存目錄 → 系統`zip`指令打包，不要用`git archive --format=zip`或Python zipfile，兩者都踩過中文檔名/UTF-8旗標的坑）→ 用`NETLIFY_DEPLOY_CONFIRMED=1`前綴直接curl POST到`api.netlify.com/api/v1/sites/40e580f0-1def-4777-adb8-587ef023ed36/deploys` → 輪詢deploy狀態到`ready`才算成功 → 手動補記`state/netlify_deploy_quota.json`（guard不會自動扣，因為指令包在bash -c或帶多個flag，不是單純以`/deploys`結尾）

相關：[[project_netlify_deploy_quota_2026-07]]（額度追蹤主檔）、[[project_bigtree_session_admin_backend_2026-08-23]]（bigtree_publish.py設計初衷）
