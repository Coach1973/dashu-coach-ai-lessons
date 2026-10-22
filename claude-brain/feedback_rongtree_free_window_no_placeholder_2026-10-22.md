---
name: feedback-rongtree-free-window-no-placeholder-2026-10-22
description: 教練10/22定：榮樹下預約改「整段空檔＋來賓自選一小時」，不准寫「來賓邀請中」佔位；每場分嘉賓／邀請人兩欄；LINE算法不用管；我沒查資料就說要清來賓資料被糾正
metadata:
  type: feedback
---

**規則**：預約頁（`event-signup/coach_schedule_view.py`）每天顯示整段空檔（例「19:00–21:00 有空檔」），來賓選想要的那一小時（每 30 分一個起點），前後訪談留 30 分由程式算（`_day_windows`／`_fits`）。前置作業（`rongtree_guest.public_prep` + `github_repos/rongtree/index.html`）：沒人預約、不知道來賓的場次不列；每場寫「嘉賓：X」「邀請人：Y」（行程表欄位 guest／booked_by）；另列「還有空檔的時間」。週四固定休息已停用。commit `f45ef789f`、rongtree `fe0c043`/`37870c3`。接 [[feedback-interview-30min-buffer-between-sessions-2026-10-19]]。

**教練原話**：「我連來賓是誰都不知道，你就寫來賓邀請中？那之前已經訂好的又幹嘛清？」「就不要有 LINE 的演算法了，他們不會用」。

**Why**：網頁只放確定的事實；固定格子配合不了來賓。我還沒打開資料就說要「清掉真實來賓資料」，教練問「沒有人填資料你要清什麼？」。
**How to apply**：講會動到什麼資料之前先查資料；排訪談只改網頁版，`coach_schedule.py open-slots`（LINE）不用同步改。
