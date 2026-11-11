---
name: reference-claude-usage-query-oauth-endpoint-2026-11-11
description: 教練問「流量使用情況」＝Claude 額度；用鑰匙圈憑證打 oauth/usage 端點直接查 5 小時／7 天百分比與重置時間
metadata:
  node_type: memory
  type: reference
  originSessionId: 879da469-2b6a-5ee6-8feb-83d48b108010
  modified: 2026-11-11T04:59:43.087Z
---

教練說「目前流量使用情況」指的是 Claude 訂閱額度（不是對話容量、不是 LK888）。

查法（不印出憑證）：
```bash
TOK=$(security find-generic-password -s "Claude Code-credentials" -w | python3 -c "import sys,json;print(json.load(sys.stdin)['claudeAiOauth']['accessToken'])")
curl -s https://api.anthropic.com/api/oauth/usage -H "Authorization: Bearer $TOK" -H "anthropic-beta: oauth-2025-04-20"
```
看 `five_hour.utilization`、`seven_day.utilization`（百分比）與 `resets_at`（UTC，要 +8 換台灣時間再講）。

**Why:** 2026-11-11 教練問流量，原本沒有現成腳本，翻了一輪才找到這個端點。
**How to apply:** 回報用白話：「5 小時用了 X%，下午 N 點重置；這週用了 Y%，M 時重置」。相關 [[reference_claude_desktop_worktree_quota_2026-10-26]]。
