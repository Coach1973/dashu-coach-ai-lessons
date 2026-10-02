---
name: project-yang-agent-telegram-group
description: 楊尚儒老師專屬小龍蝦分身yang已上線綁新群組-5405039910，無分會資料庫/LK888、鎖死不能跑指令；楊老師Telegram ID=6376666419（Simona Yang）
metadata: 
  node_type: memory
  type: project
  originSessionId: f36b59a3-f552-535f-bdca-e3da6b7ecb04
  modified: 2026-10-01T04:29:32.897Z
---

2026-10-01 教練新建群組（連結 t.me/+OoNSfuuA7wM5MDg1，chat id -5405039910），把楊尚儒老師與小龍蝦設為管理員，要專屬分身。已建 agent `yang`（`~/.openclaw/agents/yang/`，commit 9fccbf313），SOUL.md 是特助心法正典複製。

**Why:** 教練說目前不需要資料庫與 LK888 權限，只要一般小龍蝦功能。

**How to apply:**
- 安全鎖 `extensions/safety-locks/index.js` 的 `SANDBOXED_AGENTS` 含 yang：不能 exec／process，只能改自己資料夾。要開新功能（分會工具、LK888）就改這裡的 yang 分支。
- 楊老師的 Telegram user_id 尚未知：gateway 紀錄與收訊事件表都沒存發話者；他發言後從 yang 對話記錄讀，寫進 `agents/yang/USER.md` 與 IDENTITY.md。群組目前 `"*": {}` 全員可用。
- 範本與同類坑見 [[project_yijing_agent_telegram_group_2026-09-30]]、[[reference_yijing_lock_chain_and_default_arg_bug_2026-10-01]]。

**查人ID的正解：** 群組發言在設定前被當「沒點名」丟掉、紀錄沒存發話者；用 Telegram `getChatAdministrators`（腳本內讀 token、不印出）列管理員即可得ID（教練都設為管理員）。我曾誤說「要等他發言才查得到」被教練糾正。
