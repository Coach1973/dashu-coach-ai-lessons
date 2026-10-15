---
name: reference-line-any-group-answers-coach-free-slots-2026-10-15
description: LINE 小龍蝦（預設帳號）任何群組問「最近 N 場／N 天／一週／半個月可以訪談的時間」都答得出來：萬用接線→rongshuxia、open-slots 指令、外掛 parseRange、觸發詞；怎麼用真實群組路徑測
metadata:
  node_type: memory
  type: reference
  originSessionId: 0ceac93f-49ab-403d-ab7d-987a5b68da20
  modified: 2026-10-15T12:54:08.291Z
---

教練 10/15 拉了新 LINE 群「榮樹下-訪談預約系統」(C6d82fc6…cdc)，問「拉進群要不要特別通知你？任何人問最近五場訪談時間它能答嗎？」。查到：小龍蝦 20:24 自己進群（gateway 日誌 `channels/join-intro` 有紀錄，**歡迎詞沒送出去，原因沒查**），但新群原本落到通用 `main`——沒有行程資料、群組裡沒擋外人。**教練不用通知**，日誌看得到。

**現在的做法（commit `f3a7b843e` workspace、`e8cba79ed`＋`577325273` 外層）：**
- `openclaw.json` bindings 加 `rongshuxia <- line accountId=default peer=group:*`（萬用）；之後任何拉進來的 LINE 群自動接專屬分身，不用逐群綁。`openclaw agents bindings` 可查。
- 教練 10/15 糾正：只給「5 個時段」一天就查完沒參考價值 → `coach_schedule.py open-slots --count N`（最近 N 個一小時時段，晚上優先）與 `--days N`（逐天列晚上／白天可約時段）；與預約頁前 8 個時段逐一比對一致。
- 外掛 `schedule-context` 的 `parseRange` 讀「最近五場／3 天／一個禮拜／半個月／兩週／一個月」，把系統算好的清單放進提示（沒說多久→先給 5 個並提示可問更久）；測試 `node extensions/schedule-context/test.mjs` 41/41。
- 群組要先「叫得動」才處理：觸發詞在 `openclaw.json` 的 `agents.entries.rongshuxia.groupChat.mentionPatterns`（蝦、訪談、有空、空檔、行程、預約…，10/15 補了 可以約／可約／哪些時間／哪些時段／最近＋數字＋天場週月）；沒命中的訊息日誌是 `line: drop no mention target`。改這個 hot reload 即時生效（bindings 也是）；外掛改了要重啟 gateway（`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`）。
- 規則給外人：行程名稱公開、地點備註不給（SOUL.md／外掛已寫）。

**怎麼用真實群組路徑測（不發 LINE、不扣額度）：**
`openclaw gateway call agent --params '{"agentId":"rongshuxia","sessionKey":"agent:rongshuxia:line:group:<小寫群ID>","message":"[LINE 群名 id:<群ID>] 路人甲 (Utest…): 問題","idempotencyKey":"唯一值","deliver":false}' --expect-final`；測完 `openclaw sessions delete --agent rongshuxia --yes "<sessionKey>"` 讓真群組從乾淨狀態開始（不要對**舊群**這樣測，會污染「整理對話」用的歷史）。

**未查：** 新群歡迎詞為何沒送出（額度 20/200 沒問題）；gateway 每次啟動都有一則與本案無關的 `providers.nvidia.models[17].input` 設定驗證錯誤（10/15 01:52 起就有）。

相關：[[project-rongshuxia-group-interview-scheduler-2026-10-12]]
