---
name: project-bigtree-eventsignup-sync-rule
description: 大樹小講(bigtree-tw)新增/修改場次時，event-signup後台event.db的events表必須同一輪同步更新，教練2026-08-11明確要求連動
metadata: 
  node_type: memory
  type: project
  originSessionId: 2cdfc226-e7f0-4f31-b7c8-9eb232aef739
  modified: 2026-08-12T02:37:29.067Z
---

教練2026-08-11親口要求：大樹小講(bigtree-tw)新增/修改場次時，event-signup後台（`event-signup/event.db`的`events`表）必須跟著同步更新——「這樣才連動」。

**Why**：現場QR掃碼簽到（`/checkin`）跟抽獎輪盤靠後台`event.db`的`routing_mode=auto`自動判斷「這是哪一場」，前台bigtree-tw網站有場次但後台`events`表沒對應資料，會導致當天掃碼簽到抓不到對應場次（例如自動跳到下一個真實存在的未來場次，日期對不上）。

**How to apply**：往後只要教練交辦「大樹小講新增/改場次」，改完前台`github_repos/bigtree/index.html`的`SESSION_DATES`後，同一輪要直接寫入`event-signup/event.db`的`events`表（`slug`/`name`/`event_date`[/`start_time`]），不能只改前台就結案。

**同場修復的架構坑**：`event.db`的`get_current_event()`（`db.py`）原本同一天有多場次時只認`ORDER BY event_date ASC LIMIT 1`抓到的第一筆，會讓後開始的場次（例如晚場）來賓資料誤記到先開始的場次（午場）去。已加`start_time`欄位+改路由邏輯（同一天多場時挑「已開始的場次裡最晚開始那個」，都還沒開始則挑當天最早那場），2026-08-25台南場午晚兩場是第一個實測案例，本機模擬多時間點驗證切換點正確落在14:00/18:00，但**尚未經過8/25當天真實流量驗證**，下次見到教練先問8/25當天有沒有異常。

相關commit：workspace `c3501af57`（db.py/schema.sql改動）、bigtree `8a6c699`（新增8/25場次）+`cfa30d9`（全站場次名稱改時間制）+`82ff888`（主題文字修正）。
