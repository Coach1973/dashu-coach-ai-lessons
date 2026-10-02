---
name: agent-session-keeps-old-rules-archive-after-edit
description: 改了分身(yijing等)的AGENTS.md/工具後，該群組舊對話仍沿用舊規則，必須封存session才會讀新版，否則分身一直說「沒有工具」
metadata:
  type: reference
---

怡靜群分身在 09-30 23:57 前開的對話，當時 AGENTS.md 寫「沒有查詢工具」；後來補了 team_tool 與新規則，但同一個 session 繼續沿用舊規則，10-01 01:58 教練丟12個名字時分身回「我沒有工具」（教練：測試完怎麼一做事又出問題）。

**Why:** 分身 session 存在 `agents/<id>/agent/openclaw-agent.sqlite`，規則在 session 內被快取，改檔不會自動生效。
**How to apply:** 改完分身 AGENTS.md／新增工具後，必跑 `openclaw sessions archive --agent <id> "<session key>"`（封存可還原），再用 `openclaw agent --agent <id> --session-id test-xxx --message "【系統測試】…"` 實測一句，測完再封存測試 session。延伸 [[feedback_flag_unscoped_token_cost_before_fixing_2026-09-30]] 之外的交付前實測原則見試金石案例94。
