---
name: verbatim-vault-silent-zero-harvest
description: 逐字保險箱（memory/verbatim）群組停收約 6 週(9/16起)、桌面版 worktree 停 3 天(10/27起)的真相與修法；收到 0 句卻印成功
metadata:
  type: reference
---

- 收集程式 `scripts/recall.py --harvest`（cron daemon 每 30 分鐘）原本只讀 `agents/*/sessions/*.jsonl` 與 `terminal-notes/raw_sessions/`。小龍蝦 OpenClaw 2026.9.4（9/12 裝、9/16 修 gateway 版本不匹配）後對話改存各分身 sqlite；桌面版「開工」的 worktree 對話存在 `~/.claude/projects/-Users-bymyway--openclaw*/`。兩處都沒人接。
- 教練 10/30 問「誰叫它停的」：查證＝沒人下令、沒人關排程；程式一直印「✅ 新收 0 句」，設計缺口。群組最後一筆 9/16 03:54，桌面版 10/27 17:04（修前）。
- 已修（`f9d59c3a7`）：recall.py 加 scan_agent_dbs、LIVE_TERMINAL_GLOB；補回 1,552 句。待做（B 項）：來源超過 6 小時沒新增就警報、事件觸發。
- 之後看到「查不到教練說過」先確認這個保險箱有沒有在長（`tail -1 memory/verbatim/2026-10.jsonl` 看時間），再下「沒講過」的結論。
- 相關：[[feedback-hooks-must-fail-open-never-block-coach]]（同樣是「默默壞掉」類）；試金石案例136。
