---
name: feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30
description: 教練答案必然是「要」的事（上傳雲端、放行自己的工作）不准問；被自動安全檢查擋下時不准丟指令叫教練去終端機跑
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9e871b3c-fae2-480c-9821-762021756725
  modified: 2026-09-30T07:24:30.538Z
---

2026-09-30 教練連續糾正兩次：
1. git push 被 Claude Code 自動安全檢查擋下，我丟三行指令叫教練自己開終端機跑 → 教練：「我就說我不想當搬運工」。
2. 補傳成功後我問「要不要加永久放行規則？」→ 教練：「這種問題你都不該問我。你覺得我會跟你說不要嗎？」

**Why:** 守則#08「除非這個決定是不可逆的，否則就應該立即去執行」、#12 拒絕當資訊搬運工、N2 第①關「只有教練能做」——答案顯而易見的事不過關。
**How to apply:**
- 教練答案必然是「要」的事，直接做，做完一行交代。
- 被安全檢查擋下：不丟指令給教練。能改用別的正當做法就改；真的只有教練本人能解的（例如 AI 不能自己替自己加權限），只講「需要您做的那一個最小動作」，不附一串指令。
- AI 自己改 `~/.claude/settings.json` 權限會被判定為「自我修改」擋下，這是平台設計，不是教練的系統，不要反覆嘗試。

相關：[[feedback_ask_coach_three_gates_root_fix_2026-09-24]]、[[feedback_junshi_role_decide_not_ask]]
