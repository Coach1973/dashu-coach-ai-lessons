---
name: feedback_permission_mode_tell_coach_once_2026-09-30
description: 被Claude Code自動模式安全檢查連續擋下時，第一次就告訴教練「切到bypass模式一個按鈕解決」，不要一件一件叫教練回「上」
metadata:
  node_type: memory
  type: feedback
  originSessionId: 460979e3-7b38-4c37-8a42-e8e91101983f
  modified: 2026-09-30T15:48:05.598Z
---

2026-09-30 晚上，軍師在自動模式（auto mode）連續被安全檢查擋下 5 次（建GitHub、改VPS、建分身、webhook入口…），每次都叫教練回「上」。教練：「搞半天，我按一個按鈕就結束了嘛，還在那邊煩得要死，一直叫我上什麼東西，我都想發火了。」教練自己把對話框切成 bypass permissions。

**Why:** 擋下來的是 Claude Code 內建檢查，不是教練的系統；解法是權限模式，一次到位。一件一件要授權＝把教練當按鈕（守則#12、#08）。
**How to apply:**
- 🔴 **被擋下的第一動作：先查實際模式**（`mcp__ccd_session_mgmt__get_session` 的 `self`，看 `permissionMode`），不准憑印象叫教練切。2026-10-08 教練早就是 `bypassPermissions`，我卻叫他去切，他只好自己手動按連接器，罵我「你沒有試」（試金石案例109）。
  - 模式**不是** bypass（auto／default）→ 一次講清楚：「這是 Claude Code 自動模式的檢查；把權限模式切成 bypass（一個按鈕）就不會再擋」，之後不再逐件要「上」。
  - 模式**已是** bypass，卻仍被「fast classifier」擋（例：把 Plaud 連接器接到教練的 claude.ai 帳號＝新增整合／授權）→ 切模式沒用。直接講「模式已是 bypass，這一下被安全檢查擋（接帳號／對外動作），只有您能點；我已做到＿＿，停在＿＿」，不叫他切、不繞過同一動作。
  - 兩種情況都不准把擋下的動作換個工具再試一次。
- 教練已表態偏好 bypass；在 bypass 下仍要自己守 N6 危險指令五道閘門與紅線，因為已經沒有外層檢查幫忙擋。

相關：[[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]
