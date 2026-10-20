---
name: reference-line-quota-push-counts-per-member-registration-forward
description: LINE 官方帳號（小龍蝦 default）每月 200 則，推播按「收件人數」扣、群組按成員數；10/20 已用 199；報名通知含「香檳下午茶」會轉進 LINE 群「小旭老師報名通知」的規則放哪、怎麼加群
metadata:
  node_type: memory
  type: reference
  originSessionId: 5a30dc0b-103a-44dd-9abc-ef0d318c8cfe
  modified: 2026-10-20T10:40:59.612Z
---

- **扣額度規則（LINE 官方文件實查 2026-10-20）**：推播（push）按「收件人數」扣，推到 3 人群＝扣 3 則；reply 不在文件的計數段（實測 10/1~10/19 reply 1151 則、用量卻只有 199，所以 reply 不扣）。查額度（唯讀、免費）：`/v2/bot/message/quota`、`/quota/consumption`、`/delivery/push?date=YYYYMMDD`、`/group/<id>/members/count`；金鑰在 `~/.openclaw/openclaw.json` 的 `channels.line.channelAccessToken`（default 帳號）。`/message/validate/push` 可免費驗訊息格式。
- **10/20 17:40 實測：本月已用 199／200，額度 11/1 重置。10/20 晚已查實誰用掉（完整報告 side-session-notes 的「LINE額度199查因報告_2026-10-20.md」）**：回答（reply）免費，是約 8 則「外送路徑」訊息＝推播，送進 24 人的「榮樹下談公益 Run for Future」一則扣 24（群 10/12 約 17 人）。10/19＝3（小旭老師報名通知群自我介紹）＋5×24（下午 4:05～4:06 AI 連發 5 次 `message send` 進度播報，撞到 Tool exec not found）；10/20＝24（10:11）＋24（10:46「AI service temporarily overloaded」出錯通知進群）＋4（榮樹下-訪談預約系統 11:06）。兩天各自反推群人數都是 24。外掛程式碼：即時回覆走回覆憑證（免費），外送一律 `pushMessageLine`（扣額度）；`message:sent` 紀錄（`logs/line-delivery-fallback-probe.log`）裡 `to=line:group:…` 的成功項＝推播，可直接當帳本。教練 10/20 已把機器人移出大群。三個 LINE 帳號只有龍蝦小助教（@268dptjc）爆；大台南南區AI小幫手、教練都在想什麼？、活動報名系統的大樹教育顧問（@qaw8118h）本月皆 0。方案（待教練選）：禁 AI 在 LINE 群用發訊息工具播報、攔「AI service overloaded」字樣、事件觸發的額度哨兵（過 50/80/95% 通知）、排程對話只留 4 人群。
- **報名通知 → 指定群轉發（教練 10/19 要求，commit `3a8e58cc4`；10/20 `5f6b27b73` 改成可轉 Telegram 或 LINE 群）**：`event-signup/app.py` 的 `GROUP_FORWARD_RULES`（關鍵字→`telegram_chat_id` 或 LINE `group_id`），函式 `_forward_by_keyword`，在 `_notify_xiaolongxia` 發到「活動報名即時通知」Telegram 群時觸發、背景執行緒。**教練 10/20 決定另開 Telegram 專屬群「小旭老師活動報名通知」**（不扣 LINE 額度；不加進舊群，因為舊群收所有活動的姓名電話，小旭老師會全看到）；機器人 @openclaw_macbook4_bot（頂級特助）；Telegram 群編號填入規則表後，要把 LINE 那條規則拿掉。LINE 規則的細節：`LINE_FORWARD_MIN_QUOTA=30`，本月剩餘低於 30 就不轉、原文寫進 `event-signup/notify_failures.log`（`chat_id=line:<群編號>`，可事後補轉）。小旭老師報名通知群編號 `C37ef97aa4155577abfb2f6a53500d8b3`（OpenClaw 會把大寫 C 轉小寫，LINE API 要大寫 C）、群人數 3。測試 `event-signup/test_line_group_forward.py`（假網路），接進 pre-commit 3.7。
- **怎麼加第二個群**：在規則表加一行 `{"keyword": …, "group_id": …, "name": …}`；群編號用 `/group/<id>/summary` 驗證回 200。
- 相關：[[feedback-blocking-messages-must-not-say-ask-coach-2026-10-13]]（LINE 每月 200 則、聊天回覆不扣）、[[reference-worktree-session-edit-hook-blocks-openclaw-2026-10-15]]（這場又被臨時工作區擋、教練授權後用終端機改）
