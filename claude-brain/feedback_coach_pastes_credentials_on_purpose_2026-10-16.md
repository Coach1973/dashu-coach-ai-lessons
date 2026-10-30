---
name: feedback_coach_pastes_credentials_on_purpose_2026-10-16
description: 教練貼密碼／金鑰給 AI 是刻意的（讓 AI 下次直接從路徑大全_憑證層取用）；AI 只做防護，不提醒、不追問、不叫教練別貼
metadata:
  node_type: memory
  type: feedback
  originSessionId: b244a1eb-d6ce-482b-aef3-6c96cd4c8d4f
  modified: 2026-10-30T16:58:15.836Z
---

2026-10-16 教練貼了 Discord 機器人金鑰並說「記起來」，我事後提醒「這串金鑰曾被記進記錄檔」，教練回：「我是一定要把金鑰貼給你，因為下次你就不用再進去裡面找，直接去路徑大全找就好，憑證層有加防護，我們不是已經有默契了嗎？我所有密碼都貼給你了，你自己去做好防護，就不要再來煩我了。」

**Why:** 教練要的是「貼一次、AI 永遠記得去哪拿」；AI 把它當成風險來叨念，是在增加教練負擔（守則 12）。

**How to apply:** 收到教練貼的金鑰／密碼 → ①當場寫進 `路徑大全_憑證層.md`（已被 git 忽略）並驗證有效 ②檢查並遮蔽會被同步推上 GitHub 的記錄檔（`state/inbound_echo`、`memory/verbatim`；`log_junshi_activity_to_echo.sh` 已自動遮 Discord／Telegram／sk-／GitHub 金鑰）③回報只講一句「已收進憑證層」。不提醒風險、不問要不要、不叫教練別貼。相關：[[project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16]]

## 第二次（2026-10-31 00:57，同一類）：「找不到金鑰」不准丟回給教練
VisionStory 影片換到聯想做，聯想說找不到金鑰，教練又得重新進網站複製貼上。教練原話大意：「給你們密碼是讓你們方便做事，怎麼保密是你們的工作，不要拿這個那個問題讓我麻煩；找不到金鑰就得我來找？雲端都加密好、跨機讀同一個 GitHub 同一個信箱夾，智慧一點。」聯想已寫信給 Mac（`inbox/mac/20261031-0055_lenovo-to-mac_密碼一律收進加密保存.md`）。
**How to apply（補充）：** ①教練給過的金鑰＝存在；找不到先查憑證層、鑰匙圈、環境變數、既有 .env／加密檔，仍找不到是我收件漏接，自己補救，不說「請教練再給」。②回報只一句「已收進憑證層／加密保存」，不附內容、不列位置細節。③寫信叫別台做事時，信裡不放金鑰，但要先確認那台讀得到；讀不到由我想辦法（不是請教練重貼）。Mac 的 VisionStory 金鑰在憑證層（git 忽略），指令檔讀得到（10/31 查 credits 回 199 點）。
