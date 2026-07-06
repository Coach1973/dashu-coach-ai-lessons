---
name: reference-openclaw-cron-json-stale-snapshot
description: ~/.openclaw/cron/jobs.json 是脫節的靜態快照，不是live來源；改cron只能用openclaw cron CLI
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7e7803f9-e7a6-4dbc-a8e9-67c3e8fbcf89
---

# `~/.openclaw/cron/jobs.json` 不是即時來源，改它沒有用（2026-07-06 血淚查證）

**發現**：這個檔案跟 gateway 實際在跑的 cron 狀態會脫節，而且脫節後**改檔案完全不會生效，連 gateway 重啟都救不回來**。

**證據一**：7/5 commit `85421091` 把 `cron/jobs.json` 裡 `d6a8b3cd`（終端機對話總結，每4小時推播）的 `enabled` 改成 `false`，commit 訊息宣稱「已關閉」。但 7/6 中午用 `openclaw cron show d6a8b3cd-...` 查live狀態，顯示 `enabled: yes`，而且中午12點才剛真的推播過一次給教練——**假修復**，檔案上寫的跟系統實際跑的完全兩回事。

**證據二**：6/30 有一次改動把 `cron/jobs.json` 裡 `bbb7a348`（原名「小龍蝦對話蒸餾每4小時」）改名成「小龍蝦每日三機總結（每日23:05）」，看起來像是改好了。但 7/6 用 `openclaw cron get bbb7a348-...` 查，回傳 `cron job not found`——**這個 job 在 live 系統裡根本不存在**，只存在於這份靜態檔案裡，是空氣。

**根因推測**：live 系統的 cron 真正儲存位置不是這個 `cron/jobs.json`（可能是別的資料庫/內部狀態），這個檔案疑似只是某次匯出的快照，之後被人工繼續編輯、繼續 commit，但沒有任何機制把編輯同步回 gateway。

**唯一可信的查詢/修改方式**：
- 查詢即時狀態：`openclaw cron list` / `openclaw cron show <id>` / `openclaw cron get <id>`
- 修改：`openclaw cron edit <id> --xxx`、`openclaw cron enable/disable <id>`——這些指令有實際生效（有驗證過：disable 後 `cron show` 立刻顯示 `enabled: no`）
- **絕對不要**只憑編輯 `~/.openclaw/cron/jobs.json` 就回報「已修復/已關閉」，那只是改了一張過期的照片

**How to apply**：任何要新增/停用/修改 cron 任務的任務，動手前用 `openclaw cron list` 先看 id，動手後一定要再 `openclaw cron show <id>` 驗證live狀態，不能只看檔案內容或只憑「我改過檔案」就回報完成。

關聯：[[feedback_junshi_role_decide_not_ask]]、[[feedback_false_success_report_pattern]]、[[feedback_settings_hook_verify]]
