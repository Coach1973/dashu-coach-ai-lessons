---
name: feedback-line-push-needs-coach-approval-standing-order
description: 教練常設禁令（2026-10-20）：所有 LINE 小龍蝦沒有他允許，永遠不得用會扣額度的推播；閘門在哪、怎麼許可、怎麼重新補、哪些沒涵蓋
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5c639ade-2875-478d-b19c-cdbb974e4aae
  modified: 2026-10-20T11:13:35.209Z
---

**教練原話（2026-10-20 19:05）**：「所有的LINE小龍蝦，沒有經過我的允許，永遠不得使用會扣額度的方式來工作。」起因：額度被扣光都是「事後才發現」，很久以前用 Kimi 時也發生過同樣的事（同類錯第二次＝要改機制，不是再寫記憶，[[reference-line-quota-push-counts-per-member-registration-forward]]）。

**Why**：LINE 官方帳號每月 200 則；LINE 官方文件：推播「算幾則＝送給幾個人」（群組＝人數，一次送 4 個訊息框給 5 人群也只算 5），回覆（reply）不計。所以 24 人群一則推播＝24。10/19～20 榮樹下 24 人大群約 8 則推播就用掉 185。

**How to apply（機制已上線，不靠記得）**：
- 閘門＝補在 LINE 外掛唯一推播出口 `sendLineProviderMessages`（`~/.openclaw/npm/projects/openclaw-line-*/node_modules/@openclaw/line/dist/send-*.js`），回覆永遠放行、非回覆（push）一律擋；套用／檢查／還原：`python3 ~/.openclaw/workspace/scripts/line_push_gate_patch.py [--check|--revert]`（冪等）。外掛更新換世代會洗掉補丁→每日點名 `check_line_push_gate` 會發現並自動補回、報 🔴（補回後要重啟 gateway 才生效）。
- 同一套規則也套在 Python 推播者：`agents/bni_tainan/scripts/send_line_push.py`（三個 LINE 帳號都能推，line-delivery-fallback hook 會呼叫它）與 `workspace/event-signup/app.py` 的 LINE 群轉發（用龍蝦小助教金鑰）。
- **許可方式**：教練在對話裡明說同意某次推播後，AI 才 `touch ~/.openclaw/workspace/state/LINE_PUSH_APPROVED`，10 分鐘內有效（同 DELETE_APPROVED 慣例）；用完把 mtime 設回舊日期作廢（`touch -t 202001010000`），不要靠自動過期。沒有教練明說，AI 自己不准建這個旗標。
- 被擋會寫 `workspace/state/line_push_blocked.log`（時間／來源／收件／前 40 字），這是「有誰想推」的稽核帳；事件轉發被擋時原文另留在 `event-signup/notify_failures.log`。
- 實測（10/20，commit outer `ae2032337`＋`a39fd133f`、workspace `42efb64f6`）：真實 C 群編號經運作中的 gateway → `OutboundDeliveryError: 403 …常設禁令`、不重試、不進重送佇列、額度仍 199；有旗標時放行到 LINE 吃 429；旗標作廢再擋。
- **沒涵蓋**：①「大樹教育顧問」(@qaw8118h，event-signup 自己的 OA，本月 0／200)不屬於小龍蝦，沒加閘門 ②Telegram／Discord 不扣額度，不受影響 ③AI 手動 curl LINE 推播 API 繞過閘門（靠這條記憶與自律，禁止）④舊世代 2026.6.33 外掛目錄沒有 send-*.js，沒補。
- 有許可旗標時才送得出去的推播，仍受月額度限制（LINE 回 429 "You have reached your monthly limit." 不扣）。
- **解釋 LINE 計費別用「群發簡訊」比喻（教練 10/20 22:10 當場挑出不合理）**：教練認為群組裡訊息只出現一次、不是每人單獨收到，卻扣成員人數，覺得 LINE 計費不合理（「這不就是在騙錢嗎」，並說不怪我）。他說得對：那個比喻不準確。以後直接講事實——「這是 LINE 的計價規則，按成員人數算（官方文件白紙黑字，教練自己帳號的每日統計也反推出 24），我們改不了，所以用閘門避開」，不替 LINE 辯護、不編比喻。
