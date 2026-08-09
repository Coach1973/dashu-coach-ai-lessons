---
name: reference-event-signup-line-binding-and-bigtree-deeplink
description: event-signup系統LINE綁定機制(送出訊息才算,跟加好友無關)+bigtree-tw已內建?session=深連結功能，2026-08-10查證
metadata:
  node_type: memory
  type: reference
  originSessionId: e8cec3a9-8587-471e-a1a2-aea003ee626a
  modified: 2026-08-09T16:32:26.661Z
---

**LINE綁定機制（`~/.openclaw/workspace/event-signup/app.py`）**：
`/line/webhook`只處理`event.type == "message"`，完全沒有處理LINE的`follow`事件。綁定條件是
「對方送出符合`GREET_PATTERN`（`^我是(.+?)，剛報名了`）的文字訊息」，比對邏輯是**用姓名比對**
`attendees`表（`db.match_line_identity()`），跟手機號碼、跟「有沒有加好友」都無關——單純加好友
不送訊息，系統資料庫完全不會知道對方的`line_user_id`，之後永遠無法對他推播。

**2026-08-10重新設計**：現場報到`/checkin`已改成單一介面——填手機號碼、按「我要參加抽獎」，
同一步驟伺服器直接302導向`line.me/R/oaMessage/...`（已帶好「我是OOO，剛報名了XXX。我要現場
立即參加抽獎（送出才算登記成功）」），不再停在「簽到成功」中繼畫面等使用者再按一次加好友。
`make_qr.py --wheel`可產生通用版「掃碼玩抽獎」QR立牌（不押日期，往後每場活動都用同一張）。

**bigtree-tw（`github_repos/bigtree/index.html`）已內建場次深連結，不用另外開發**：
網址帶`?session=YYYY-MM-DD`參數，`openRegisterFromQuery()`會自動彈出該場次的報名視窗、
場次還先幫忙選好（例：`https://bigtree-tw.netlify.app/?session=2026-08-26`）。這個功能
在2026-08-10被重新「發現」——教練要一個「點了直接跳8/26報名視窗」的連結，一度以為要新開發，
查原始碼才發現早就做好了。

**Why**：這兩個機制都非常不直覺（LINE的follow事件完全沒被處理；深連結功能藏在原始碼裡
沒有文件記錄），下次遇到類似需求（教練問「能不能做一個直接跳出XX的連結」或debug綁定率）
應該先查原始碼再回答，避免重複開發或誤判「做不到」。

**How to apply**：
- 教練問「綁定率低」類問題，先查`GREET_PATTERN`+`line_webhook`邏輯，不要假設是加好友率低
- 教練要某場次的專屬報名連結，直接組`bigtree-tw.netlify.app/?session=YYYY-MM-DD`，不用開發新功能
- 未來event-signup系統若要新增類似「一鍵完成」的流程，可比照`_lottery_greet_url()`這個helper的模式（app.py內）

Related: [[reference_signup_notify_pipeline]]（同系統的報名通知管線）
