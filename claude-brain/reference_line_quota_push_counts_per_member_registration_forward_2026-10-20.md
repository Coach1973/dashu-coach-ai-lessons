---
name: reference-line-quota-push-counts-per-member-registration-forward
description: LINE 官方帳號（小龍蝦 default）每月 200 則，推播按「收件人數」扣、群組按成員數；10/20 已用 199；報名通知含「香檳下午茶」會轉進 LINE 群「小旭老師報名通知」的規則放哪、怎麼加群
metadata:
  node_type: memory
  type: reference
  originSessionId: 5a30dc0b-103a-44dd-9abc-ef0d318c8cfe
  modified: 2026-10-20T10:35:52.826Z
---

- **扣額度規則（LINE 官方文件實查 2026-10-20）**：推播（push）按「收件人數」扣，推到 3 人群＝扣 3 則；reply 不在文件的計數段（實測 10/1~10/19 reply 1151 則、用量卻只有 199，所以 reply 不扣）。查額度（唯讀、免費）：`/v2/bot/message/quota`、`/quota/consumption`、`/delivery/push?date=YYYYMMDD`、`/group/<id>/members/count`；金鑰在 `~/.openclaw/openclaw.json` 的 `channels.line.channelAccessToken`（default 帳號）。`/message/validate/push` 可免費驗訊息格式。
- **10/20 17:40 實測：本月已用 199／200**（10/19 中午才 27；10/19 一天 push 123 次）。10/19 小龍蝦 rongshuxia 在 LINE 群共 49 則 assistant 訊息（「榮樹下談公益-run-for-future」16 點那一小時 19 則）——**推論（未證實）**：小龍蝦在群組裡有一部分回話是以推播送出、按成員數扣。額度 11/1 重置。
- **報名通知 → 指定群轉發（教練 10/19 要求，commit `3a8e58cc4`；10/20 `5f6b27b73` 改成可轉 Telegram 或 LINE 群）**：`event-signup/app.py` 的 `GROUP_FORWARD_RULES`（關鍵字→`telegram_chat_id` 或 LINE `group_id`），函式 `_forward_by_keyword`，在 `_notify_xiaolongxia` 發到「活動報名即時通知」Telegram 群時觸發、背景執行緒。**教練 10/20 決定另開 Telegram 專屬群「小旭老師活動報名通知」**（不扣 LINE 額度；不加進舊群，因為舊群收所有活動的姓名電話，小旭老師會全看到）；機器人 @openclaw_macbook4_bot（頂級特助）；Telegram 群編號填入規則表後，要把 LINE 那條規則拿掉。LINE 規則的細節：`LINE_FORWARD_MIN_QUOTA=30`，本月剩餘低於 30 就不轉、原文寫進 `event-signup/notify_failures.log`（`chat_id=line:<群編號>`，可事後補轉）。小旭老師報名通知群編號 `C37ef97aa4155577abfb2f6a53500d8b3`（OpenClaw 會把大寫 C 轉小寫，LINE API 要大寫 C）、群人數 3。測試 `event-signup/test_line_group_forward.py`（假網路），接進 pre-commit 3.7。
- **怎麼加第二個群**：在規則表加一行 `{"keyword": …, "group_id": …, "name": …}`；群編號用 `/group/<id>/summary` 驗證回 200。
- 相關：[[feedback-blocking-messages-must-not-say-ask-coach-2026-10-13]]（LINE 每月 200 則、聊天回覆不扣）、[[reference-worktree-session-edit-hook-blocks-openclaw-2026-10-15]]（這場又被臨時工作區擋、教練授權後用終端機改）
