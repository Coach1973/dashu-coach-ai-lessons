---
name: feedback_coach_pastes_credentials_on_purpose_2026-10-16
description: 教練貼密碼／金鑰給 AI 是刻意的（讓 AI 下次直接從路徑大全_憑證層取用）；AI 只做防護，不提醒、不追問、不叫教練別貼
metadata:
  type: feedback
---
2026-10-16 教練貼了 Discord 機器人金鑰並說「記起來」，我事後提醒「這串金鑰曾被記進記錄檔」，教練回：「我是一定要把金鑰貼給你，因為下次你就不用再進去裡面找，直接去路徑大全找就好，憑證層有加防護，我們不是已經有默契了嗎？我所有密碼都貼給你了，你自己去做好防護，就不要再來煩我了。」

**Why:** 教練要的是「貼一次、AI 永遠記得去哪拿」；AI 把它當成風險來叨念，是在增加教練負擔（守則 12）。

**How to apply:** 收到教練貼的金鑰／密碼 → ①當場寫進 `路徑大全_憑證層.md`（已被 git 忽略）並驗證有效 ②檢查並遮蔽會被同步推上 GitHub 的記錄檔（`state/inbound_echo`、`memory/verbatim`；`log_junshi_activity_to_echo.sh` 已自動遮 Discord／Telegram／sk-／GitHub 金鑰）③回報只講一句「已收進憑證層」。不提醒風險、不問要不要、不叫教練別貼。相關：[[project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16]]
