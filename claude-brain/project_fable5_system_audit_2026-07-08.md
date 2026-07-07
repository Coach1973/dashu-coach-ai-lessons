---
name: project-fable5-system-audit-2026-07-08
description: Fable5系統全盤稽核完成：3紅(session-end自我餵養/蒸餾雙引擎/relay殭屍輪詢)6黃7綠，報告在knowledges/，修復待教練說「修」
metadata: 
  node_type: memory
  type: project
  originSessionId: a21977a4-b019-4888-996c-b12b5186897b
---

2026-07-08 凌晨教練親口指定用 Fable 5 對小龍蝦系統做全盤健診，已完成，報告：`workspace/knowledges/AUDIT_fable5_系統全盤稽核報告_2026-07-08.md`（commit `1ff4434d3`）。

**3 個🔴已修復（教練 7/8 凌晨 3:05 親口核准「當然是要修嘍」，council 保留不動之後再議）：**
1. ✅ `session_end_auto_push.sh` 自我餵養循環：推送紀錄改寫 /tmp 不寫 HEARTBEAT（commit `95fae5d2b`）；驗證時暴露原腳本空陣列 bash3.2 set-u 舊 bug 一併修（`f197c7917`）。連跑兩次實測 HEARTBEAT 保持乾淨
2. ✅ 增量蒸餾其實是**三引擎**不是雙引擎：LaunchAgent（已卸載存檔 `_archive/launchagents_retired_20260708/`）+ 土炮排程器 `openclaw_cron_daemon.sh` 第39行（已移除，`5d23cedc2`）+ openclaw cron（唯一保留）
3. ✅ relay 殭屍共**四顆頭**全斬：LaunchAgent relay-poll（卸載存檔）+ 土炮排程器每分鐘輪詢（移除）+ kong/peipei 休眠分身 jobs.json 各一個每分鐘任務（enabled:false，備份 `.bak.before-relay-retire-20260708`）。實測 relay 心跳停在 03:13 不再前進

**🔴 修復中新發現（已報教練待議）：土炮排程器 vs 系統 crontab 大面積雙跑**
`openclaw_cron_daemon.sh`（KeepAlive while 迴圈，6/5 建）註解自稱 6/20「從 crontab 接管」備份/鏡像/查話，但 crontab 舊線路沒拆：backup_terminal（雙跑每15分）、sync_handoff（雙跑每5分）、recall（雙跑每30分）；LaunchAgents split-memory/distill-watchdog/heartbeat-audit 也各與 daemon 內排程重複。這就是當年「撞 lock 96% 失敗」的根源，病根是「搬家只搬新的忘拆舊的」模式第三次發作。

**關鍵查證結論（下一棒可直接引用）：**
- cron 失敗通知**只有兩條路**（sendCronFailureAlert 門檻型 + dispatchCronFailureDestinationNotifications 單次型），沒有第三條；globalFailureDestination 未設定；4 個 announce 任務 bestEffort=True 已驗證生效。但新建 announce cron 預設 bestEffort=false，必須記得加 `--best-effort-deliver`（該寫進 E09）
- UserPromptSubmit 10 個 hook 實測每句話合計 2.5 秒，2.27 秒在兩個 scan hook（含對話路徑上的 git pull）
- WEBSITE_REPOS 是全機唯一寫死站台清單，其他無同類地雷
- 大腦架構：`~/.claude/projects/.../memory` → symlink → `workspace/claude-brain`，隨 workspace repo（[[reference-openclaw-nested-git-repos]]）
- 試金石編號三套並行（字母/數字/W系列），案例 25 重複兩次
- 聯想/ACER 同款稽核未做（需各機自跑，發跨機指令要教練拍板）
