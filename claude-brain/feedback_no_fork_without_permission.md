---
name: feedback_no_fork_without_permission
description: 未經教練允許，禁止自行使用 fork 功能開啟新 session
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5eef2d3a-ccfa-41e3-b78c-4152ba8e0ac5
---

未經教練明確允許，禁止自行使用 FORK 功能。

**Why:** Fork 會繼承完整歷史 context，token 消費遠高於一般新對話。教練親身踩過這個坑——軍師未經授權 fork，導致 token 快速消耗。這是教練 2026-06-02 親定的歷史教訓。2026-06-25 教練開場第一指令再次強調，視為最高警戒等級。

**How to apply:** 需要開新對話框時，等教練說要 fork，或主動問「要開新對話還是繼續這個？」不得自行判斷並執行 fork。這是每個新 session 開場就必須遵守的第一條戒律。
