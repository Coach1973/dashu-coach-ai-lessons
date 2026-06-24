---
name: feedback-taiwan-time-always
description: 時區鐵律——所有時間顯示永遠用台灣時間（UTC+8），不可用 UTC 字面值騙自己看成現在時間
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cdae7e71-8e47-47bc-bf18-e9dbfee6ced3
---

# 🔴🔴🔴 時間顯示鐵律：永遠用台灣時間（教練親令 2026-06-09，多次提醒）

**規則**：所有時間輸出/呈現/判斷給教練看，**一律換算成台灣時間（UTC+8）**。
不論來源是 UTC ISO 8601、Unix timestamp、log 行頭，全部要在呈現前轉換。

## Why（為什麼這條這麼重要）

2026-06-09 上午，軍師讀 BOT_MESSAGES.md 看到 `2026-06-08T23:54:39.251Z` 直接判斷成「昨晚 23:54」，
其實 UTC+8 是「今天 07:54」——教練 17 分鐘前剛丟的測試題。
誤判直接讓軍師走錯方向。

教練親口：「**永遠以台灣時間為主，這個錯誤，已經提醒多次了**」——這是反覆型錯誤。

## How to apply（怎麼落地，每次都要記得）

1. **看到 `Z` 結尾的 ISO 時間**：自動 +8 小時呈現
2. **看到 `+00:00` 或 `UTC`**：自動 +8 小時呈現
3. **看到沒標時區的時間**（如 log 行頭）：先查資料源默認，多半也是 UTC，預設 +8
4. **呈現給教練時格式**：`2026-06-09 07:54（台灣）` 或 `07:54 台灣時間`，避免裸寫
5. **判斷「現在/剛剛/昨天」前**：先 `date "+%Y-%m-%d %H:%M %Z"` 對齊台灣現在時間

## 反例（不可再犯）

❌ 看到 `2026-06-08T23:54:39Z` 直接說「昨晚 23:54」
❌ Bash 跑 `date -u` 然後拿來判斷
❌ BOT_MESSAGES.md 的 ts 直接複製貼出來給教練看

## 正例

✅ 看到 `2026-06-08T23:54:39Z` 在心裡 +8 → 「台灣 07:54」呈現給教練
✅ 拿台灣時間判斷「現在 vs 訊息時間」差幾分鐘
✅ 若不確定時區，先 `TZ=Asia/Taipei date` 對齊

## 2026-06-09 下午 2:31 第 N 次違反 → 寫死系統機制（教練怒問「該當何罪」）

光寫記憶**沒用**——AI 不會每次主動讀。必須**寫死系統自動注入**：

- ✅ `scripts/inject_taiwan_time.sh`：UserPromptSubmit hook，教練每次說話自動把當下台灣時間注入 AI context 開頭（commit `2a3447b9`）
- ✅ `hooks/bot-relay-inbound/handler.js`：toLocaleTimeString 明確指定 `timeZone:'Asia/Taipei'`（commit `7a72cb1`）
- ✅ `HEARTBEAT.md` 首段加紅標時間鐵律（commit `2a3447b9`）

教訓：寫記憶 + 寫 SOUL ≠ 系統行為。**反覆型錯誤要 hook 強制注入，不靠 AI 自覺**。
這跟 [[feedback_no_background_polling_lies]] 同理：行為要寫成程式碼，不是寫成文字。

關聯：[[feedback_no_silent_waiting]]、[[feedback_no_background_polling_lies]]、守則#04（修好不要只解釋）、守則#07（不要同一地方跌倒兩次）
