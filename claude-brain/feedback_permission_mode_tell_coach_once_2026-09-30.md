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
- 同一場對話第二次被自動模式擋下，就一次講清楚：「這是 Claude Code 自動模式的檢查；您在對話框把權限模式切成 bypass（一個按鈕）就不會再擋」，之後不再逐件要「上」。
- 教練已表態偏好 bypass；在 bypass 下仍要自己守 N6 危險指令五道閘門與紅線，因為已經沒有外層檢查幫忙擋。

相關：[[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]
