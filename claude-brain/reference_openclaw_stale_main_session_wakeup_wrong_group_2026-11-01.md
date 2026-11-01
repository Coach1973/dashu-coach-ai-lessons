---
name: reference_openclaw_stale_main_session_wakeup_wrong_group_2026-11-01
description: 11/01 巴哈圖送進分工群＋週一寫成今晚＋約440次空轉的根因鏈與修法（safety-locks v1.8、提醒改直送、私人主對話每天4點重開）
metadata:
  node_type: memory
  type: reference
  originSessionId: 25abffdd-c633-4ecc-84be-1599b091ba85
  modified: 2026-11-01T14:30:06.901Z
---

**根因鏈（原始紀錄查到）**：20:55 會議提醒是 agentTurn＋全部工具 → AI 自己讀行程總表把 weekday=0（週一）當週日 → 它開的背景 exec 完成通知被送到 `agent:peipei:main`（私人主對話，沒設自動清空）→ 醒來讀到自己 10/30 寫的「下一輪接著做海報」自己開工 → 傳送工具不准讀 media/peipei_out，亂試 201 次 → sessions_send 叫小龍蝦 → bot_main 不在佩佩群 → 從 4/25 舊紀錄誤推 -1003877502911 是佩佩群「真實編號」→ 借 bot_peipei 送進頂級特助分工群。佩佩群 -5115910257 從沒遷移（每天 07:00 行程報告用它送成功）。

**怎麼查**：transcript_events 的 assistant 事件多半存在 `event_zstd`（壓縮），event_json 是 NULL，要 `zstd -dqc` 解開才看得到思考與工具呼叫；session_windows 對 session_key。`sessions.reset` 後 sessionId 不變、token 歸零，所以「同一個 sessionId 跨好幾天」不能當成沒重開的證據。

**已修（a5609df2c、635b2dded）**：safety-locks v1.8＝帳號鎖（只能用自己的機器人帳號）、群組發送鎖（只有該群自己的對話能在群裡講話；peipei 可送 -5115910257；破例 touch state/GROUP_SEND_APPROVED）、對話累計上限（同一 sessionKey 一小時 200 次，跨輪累計）、提醒排程鎖（peipei 不准新增 agentTurn 型 cron）；巴哈 25 個提醒改 command 直送 `openclaw message send`；`session.resetByType.direct` 每天 4 點；coach_schedule.py save() 自動寫「星期」欄。

**待做**：建議教練關 agentToAgent（等拍板）；明早確認 4 點有清；傳送工具媒體白名單（~/.openclaw/media/、media/tool-image-generation）是否為 10/30 升級新限制未查。相關 [[reference_turn_budget_lock_bots_silent_loop_2026-10-30]] [[project_peipei_poster_only_tra_research_to_junshi_2026-10-26]]
