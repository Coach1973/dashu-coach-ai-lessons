---
name: reference_google_calendar_private_ical_for_bots_2026-10-13
description: 教練 Google 日曆(bymyway7@gmail.com)的非公開 iCal 網址已存 Mac 憑證層，機器人可不登入每天讀；日曆早就分享給「陳佩貞 amber840214」有編輯權
metadata:
  node_type: memory
  type: reference
  originSessionId: ab89fdb0-6436-42cd-9378-510d4b330288
  modified: 2026-10-13T12:25:45.687Z
---

2026-10-13 教練要巴哈助理（佩佩老師）用 Google 日曆做漂亮的每日提醒＋空檔，並讓佩佩老師把行程加進來。

- **讀取通道已通**：非公開 iCal 網址存 `~/.openclaw/credentials/google_calendar_private_ical_url.txt`（權限 600，在 git 忽略範圍外的憑證層，不進任何 commit）。實測 HTTP 200、340 筆活動。排程／機器人用 curl 讀即可，不用教練登入。網址外洩要到 Google 日曆設定→整合日曆按「重設」。
- **Google 日曆設定頁**：`calendar.google.com/calendar/u/0/r/settings/calendar/YnlteXdheTdAZ21haWwuY29t`（教練 Chrome 已登入，用 claude-in-chrome 可讀，捲動用 get_page_text 比截圖省）。
- **共用名單**：a39521102@gmail.com（查看活動詳細資料）、「陳佩貞」amber840214@gmail.com（進行變更並管理共用設定＝可編輯）。陳佩貞是不是佩佩老師（陳佩君）**尚未確認**。
- **Google 日曆跟本機「行程總表」(knowledges/教練行程總表.json) 是兩本帳**：Google 有歸仁學法點學法、依倫等；總表有榮樹下訪談、預約頁預約。Google 因 Cal.com 同步有重複項（真誠分會固定上線、戰報會議等各兩筆）。
- 桌面版 Claude 的 Google Calendar 連接器(list_events)能讀寫，但只在桌面版對話內可用，排程機器人用不到。

**Why:** 教練只維護 Google 日曆，機器人讀總表就會漏／錯。
**How to apply:** 做每日報告／空檔／預約頁時，讀取來源改成「Google iCal ＋ 總表獨有項目(榮樹下訪談、預約頁)」合併、重複項去重。相關：[[project_rongshuxia_group_interview_scheduler_2026-10-12]]
