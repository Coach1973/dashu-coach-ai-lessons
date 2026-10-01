---
name: reference_partner_agent_reminder_via_openclaw_cron_2026-10-02
description: 夥伴分身（yang／yijing 等）沒有排程工具時，由 Mac 端 openclaw cron add 代排一次性提醒；含 3 個實測踩到的坑與驗證法
metadata:
  type: reference
---

夥伴分身被安全鎖禁 exec、工具清單沒有 cron，夥伴請它「每天中午提醒我」只能回「做不到」。教練裁示（2026-10-02 07:08）：夥伴只在乎有收到提醒，誰發都行——由 Mac 端軍師代排，不給分身開排程權限。

**做法**（照 `openclaw cron add --help` 驗證過）：
`openclaw cron add --name … --at "2026-10-03T12:00:00+08:00" --tz Asia/Taipei --agent <id> --session isolated --announce --channel telegram --account <群組綁定的 bot> "--to=<群組chat id>" --delete-after-run --wake now --message "…"`
- `--to` 是負數 chat id 要寫成 `--to=-123`；account 看 `openclaw.json` bindings（yang 群＝`bot_main`）。
- 時間用台灣時間 +08:00 寫，`cron list` 看到的是 UTC（12:00 台灣＝04:00Z）。

**3 個坑**（2026-10-02 實測）：
1. `--exact`／`--stagger` 只能配 `--cron`，配 `--at` 直接報錯、什麼都沒建。
2. 訊息要寫成「最終回覆＝提醒本文、不准呼叫 message 工具」。分身若自己用 message 工具發出，系統又會把它最後一句「已送出」當 announce 轉送，群組多一則怪訊息。
3. 要附「夥伴已回『我知道了』就只回 NO_REPLY」時，要註明「記憶檔裡單純的規則說明不算」，否則分身可能把 MEMORY.md 的規則字句當成她已回覆而靜默不發。

**驗證法**：另建一個同設定、`--to` 改教練 DM（6124913915）的測試工作，`openclaw cron run <id>`，用 `cron list --json` 看 `lastDeliveryStatus`，再讀分身最後一輪對話確認最終回覆正是提醒本文；測完 `openclaw cron rm`。不要拿夥伴的群組當測試對象。

相關：[[reference_agent_session_keeps_old_rules_archive_after_edit_2026-10-01]]、[[reference_cron_job_disappear_root_cause_sop_2026-09-18]]
