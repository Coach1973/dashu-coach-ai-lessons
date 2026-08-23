---
name: reference-telegram-registration-notify-group
description: 報名通知已全面改走Telegram群組「活動報名即時通知」(chat_id -5349981085，教練+佩佩老師同見)，LINE推播已拔除；含新群組接通SOP與requireMention靜默忽略陷阱
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5cf36a03-0875-4e26-b65b-23d197258bb4
  modified: 2026-08-23T19:21:02.529Z
---

**報名通知唯一管道＝Telegram 群組「活動報名即時通知」**（chat_id `-5349981085`，成員：教練＋佩佩老師＋`@openclaw_macbook4_bot`）。2026-08-24 教練裁示 LINE 全面停用，`event-signup/app.py` 的 `_notify_coach_line()` 與 `COACH_LINE_USER_ID` 已完整移除（commit `95ea143de`）。

**為什麼拔 LINE**：LINE 官方帳號**每一則主動推播都扣月配額**（免費方案 200 則/月），報名通知＋健康檢查＋各種提醒全部共用龍蝦小助教（@268dptjc）同一個池子。2026-08-17 左右配額用完，`_notify_coach_line()` 收到 `HTTP 429 You have reached your monthly limit`，但原始碼用 `except Exception: return False` 吞掉，教練完全不知情、以為報名系統壞了（實際上資料庫從未漏接，8/21-22 金門場當天還湧入 30+ 筆）。**只有主動推播扣配額；教練先開口、bot 回覆（reply）不扣、不限量。**

**🔴 新 Telegram 群組接通 SOP**（未登記群組的訊息會被靜默忽略、連 log 都不寫，這是最容易誤判成「教練沒發成功」的陷阱）：
1. 在群組發 `@openclaw_macbook4_bot 測試`——**必須 @提及**，因為 `resolveChannelGroupRequireMention()` 對未登記於 `groups` 白名單的群組最後一行 `return true`
2. 查 `~/Library/Logs/openclaw/gateway.log` 取得 `telegram:group:<chat_id>`
3. `openclaw.json` → `channels.telegram.accounts.bot_main.groups["<chat_id>"] = {requireMention: false}`
4. 重啟 gateway：`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
5. 直接呼叫 `sendMessage` API 驗證回傳的 `chat.title` 正確

**⚠️ 名稱陷阱**：教練有兩個名稱只差一字的群組——「活動報名即通知」（舊，ACER/聯想跨機協作討論用）vs「活動報名即**時**通知」（新，報名通知用）。動手前逐字核對，不要看到相似就當同一個。

**報名統計**：教練要求「之後問幾個人報名，直接統計給我，不用手動算，要做成報名表」。資料在 `event-signup/event.db`，`signups` + `attendees` + `events` 三表 join 可查任一場次真實人數與完整名單。

Related: [[reference_event_line_oa_push_quota]]（@qaw8118h 另一個帳號的配額紀錄）、[[試金石案例62]]、[[reference_signup_notify_pipeline]]
