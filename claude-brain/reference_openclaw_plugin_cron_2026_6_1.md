---
name: reference-openclaw-plugin-cron-2026-6-1
description: OpenClaw 2026.6.1 兩個坑——hook 外掛要宣告 activation 才會被 agent runtime 載入；升級會把 cron/jobs.json 變孤兒
metadata: 
  node_type: memory
  type: reference
  originSessionId: 63e2294f-d791-4dcd-8b54-33aa3d74747c
---

# OpenClaw 2026.6.1 兩個血淚坑（2026-06-11 軍師實戰確認）

## 坑一：hook 外掛沒宣告 activation = 鎖永遠不觸發
- 真正跑指令的是 agent runtime，它只載入「啟動名單」上的外掛
- hook 型外掛要進名單，openclaw.plugin.json 必須宣告：
  `"activation": {"onStartup": true, "onCapabilities": ["hook"]}`
- 症狀：gateway 主進程 register() 有 log，但 before_tool_call 永不觸發（safety-locks 外掛 v17.4 誤判為上游 bug，實為缺宣告）
- 驗證法：gateway.log 開機行「http server listening (N plugins: ...)」要看到外掛名字
- gateway stderr 已改導 `~/Library/Logs/openclaw/gateway.err.log`（原 /dev/null）

## 坑二：升級會把 cron jobs 留在舊檔變孤兒
- 2026.6.1 把 cron 搬進 `state/openclaw.sqlite`，舊 `cron/jobs.json` 的 12 個工作沒被遷移，斷頭 4 天（6/7~6/11，執董週會/信貸提醒/主動關懷全停）
- 已用 `openclaw cron add` 全數重建；真相源從此 = `openclaw cron list`，jobs.json 是遺骸
- 新版規矩：main session 系統事件不可帶 --announce；安靜型（不通知教練）要 --no-deliver
- 教訓：每次 OpenClaw 升級後必跑 `openclaw cron list` 對照工作數量

相關：[[feedback-openclaw-hook-fire-and-forget]]、[[project-vps-xiaolongxia-healthcheck-2026-06-09]]
