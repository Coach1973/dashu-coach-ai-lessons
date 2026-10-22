---
name: project_rongtree_booking_hold_and_saturday_930_2026-10-23
description: 榮樹下網頁「我要預約」＋選時間送出就自動占位（待確認）怎麼運作、程式在哪、怎麼確認／取消、上限與隱私；週六可約起點改 9:30 的設定鍵
metadata:
  node_type: memory
  type: project
  originSessionId: 0d9a0596-c5e4-4098-a53c-c959434a309a
  modified: 2026-10-22T22:24:29.846Z
---

2026-10-23 教練要求（原話線索：「寫有空檔，但後面沒有任何可以按的按鈕，那有空檔有個屁用」），並回「要」自動占位。

**前端**（`~/github_repos/rongtree/index.html`，event.bymyway.com 直接讀工作目錄＝推上去立刻上線，`Cache-Control: no-cache`；提交 `17af887`、`da3ba4c`）
- #prep 的「還有空檔的時間」每列右邊「我要預約 →」→ 帶到 #join 表單：自動選「節目專訪」、帶入日期與起點；表單選「節目專訪」才出現「想預約的時間」（哪一天／哪一個小時，每 30 分鐘一個起點，一場一小時）。
- 選了時間送出 → 先 POST `/api/rongtree/hold`；成功顯示「已保留 …」；`409 code=taken`（被搶走）→ 提示改選、清單刷新、表單保留；`409 code=full` 或網路／伺服器異常 → 退回原本的 `/api/works/contact`（通知帶「想預約的時間」）。沒選時間照舊走留資料。

**伺服器**（`workspace/event-signup/app.py` 的 `api_rongtree_hold`，提交 `e1d984776`）
- 呼叫 `coach_schedule_view.book(date, start, "榮樹下訪談", who="官網預約", note=…)`（新增 who／note 參數，原預約頁呼叫不變）：寫成「待確認」、前後各留 30 分緩衝，所以空檔清單馬上不再出現。
- 通知進「佩佩老師的巴哈助理」群（送不出退回活動報名群），內含「確認預約 <id>」「取消預約 <id>」；同時寫 `works_contact_leads` 一筆、並 push 到 Google 日曆。取消後空檔自動恢復。
- 隱私：姓名單位聯絡方式只在私人 `note` 與群通知；總表沒有 `guest` 欄位、`booked_by`＝「官網預約」，公開的 `/api/rongtree/prep` 只會看到「待確認／邀請人：官網預約」。
- 防亂點：官網待確認同時最多 6 筆（`_RONGTREE_HOLD_MAX_OPEN`）、每 IP 每小時 4 次（只有欄位正確的請求才計次）、隱藏欄位 `website` 有字＝假裝成功不占位。這些數字是我定的預設，可調。
- 測試：`event-signup/test_rongtree_hold.py` 15 項（行程總表換暫存複本、通知／留資料／Google 全換成空動作；跑法 `cd event-signup && set -a; source .env; set +a; venv/bin/python test_rongtree_hold.py`）。**尚未在正式站實際占過一次位**（會半夜通知群組）；第一筆真的官網預約進來時要看一眼通知與空檔是否消失。

**週六可約起點 9:30**（`269afc94f`）：行程總表 `interview_window_start_by_weekday`（鍵＝星期幾、0＝週一）目前 `{"5": "09:30"}`；預約頁 `_win_start`、LINE `win_start` 同讀，測試第 12 組。晚上時段不受影響。

**Why:** 教練要「有空檔就能按、按完就能預約」，且不想每筆都人工搶時段。
**How to apply:** 要調上限或改占位規則改 app.py 這支；改完 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`；Edit 工具會被臨時工作區的 hook 擋，要教練授權後用終端機補丁（改前備份、path-limited commit）。

相關：[[feedback_rongtree_free_window_no_placeholder_2026-10-22]]、[[reference_worktree_session_edit_hook_blocks_openclaw_2026-10-15]]
