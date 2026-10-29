---
name: project-jarvis-soul-loop-four-steps-2026-10-30
description: 教練靈魂拷問（10/30）：賈維斯要內在循環不是外部補丁；四步循環第四步「自我觸發」＝賈維斯成績單，10/30 已做好接進週一點名、變差自動體檢
metadata:
  type: project
---

教練 2026-10-30 02:47 問：一次次抓 bug 仍有很多問題，要的是賈維斯自己會偵測、除錯、優化的「靈魂」（內在循環），Haiku 照 Opus 設計的邏輯跑也能有 Opus 表現。報告 https://claude.ai/artifact/Xknxym4wGcvDn6zNYF78aL 。

回顧數字（10/21～10/30）：正式優化 2 次（10/21 `3b073e447`、10/30 `08a38eab4`）；「全面體檢」類原話 4 次（8/12、9/23、10/21、10/30）；規則字數 48,673→49,823；試金石 9 天新增 8 案；巴哈 MEMORY 同題二犯；「默默壞掉」同類 4 次。

**Why:** 兩次大體檢都靠教練開口，10/30 還要說兩遍＝迴圈沒自己轉。
**How to apply:** 四步循環——感知（每個自動化對答案，0 筆不算成功）→歸類（同類第二次改源頭，N8）→守上限（程式擋，不靠記得）→自我觸發（數字變差自己跑 [[jarvis-self-optimize]]）。第四步＝「賈維斯成績單」，10/30 03:00 已做好：`scripts/jarvis_scorecard.py` 接進每日點名（週一 08:10，上週對上上週：糾正／新案例／同類重犯／規則字數；逐字保險箱 0 句也算變差），變差自動背景跑 `jarvis_scorecard_trigger.sh`（Opus、關 hook＋指令白名單、同週一次、報告 reports/jarvis/、傳 Telegram）。第一次正式跑 11/2。教練 10/30 糾正：上一棒寫「他提起就做」的事，他說「開工」就該直接做，不准再問「要做嗎」。相關 [[reference_verbatim_vault_silent_zero_harvest_2026-10-30]]。
