---
name: verbatim-pipeline-cli-only-not-desktop-chat
description: 跨機verbatim蒸餾機制只抓CLI/Code面板session的Stop hook，不抓Desktop一般聊天；查「為何無對話紀錄」先分清介面
metadata: 
  node_type: memory
  type: reference
  originSessionId: 957df68d-14bc-4084-9cf4-4096d678d3de
  modified: 2026-08-25T16:37:21.558Z
---

`memory/verbatim/{acer,lenovo,mac}/` 蒸餾機制（`scripts/distill_and_push_{acer,lenovo}.*`）掛在各機自己 Claude Code `settings.json` 的 **Stop hook**：只有在該機跑 **Claude Code CLI 或 Desktop App 的 Code/Agent 面板** agentic session、session 結束觸發 Stop hook 時，才會把當天 `memory/YYYY-MM-DD.md` 的🦞小龍蝦bullet point推上雲端。

**如果教練是用 Desktop App 的一般聊天介面**（不開Code面板叫AI做任務），這套機制從設計上就不會被觸發——不是排程壞掉，是機制本來就沒涵蓋這種用法。一般聊天內容存在 Chromium IndexedDB（`~/Library/Application Support/Claude/IndexedDB/https_claude.ai_0.indexeddb.leveldb/`，二進位格式）加 Anthropic 雲端帳號，不是 workspace 系統能直接讀的平面檔案。

2026-08-25 也發現：Mac 端做「死腳本體檢」時只掃 Mac 本機的 settings/cron/hooks 引用，看不到 ACER 自己 settings.json 裡掛的 Stop hook，把 `distill_and_push_acer.sh` 誤判成死腳本歸檔——這類跨機腳本的「使用中」判斷不能只看發起機（Mac）本機掃描結果。

**Why：** 2026-08-26 教練糾正「ACER/聯想8月明明有對話，為什麼查不到紀錄」，查證後發現是兩層問題疊加：ACER腳本被誤歸檔（已修復），加上更根本的「一般聊天从不進蒸餾管線」架構缺口（未解，需教練決定是否要另外做手動匯出/匯入機制）。

**How to apply：** 之後遇到「某機為什麼查無對話紀錄/verbatim是空的」，先問「教練那次是用CLI/Code面板還是Desktop一般聊天」，不要直接下「XX天無對話」的結論（呼應 [[feedback_verify_activity_via_git_log_not_relay_file]]）。查跨機腳本是否死掉，要連對方機器自己的hook/settings一起查，不能只憑發起機掃描結果判定。
