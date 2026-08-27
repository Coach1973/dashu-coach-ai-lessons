---
name: project-cron-cleanup-2026-07-06
description: 2026-07-06 一次性查清並修好三個cron問題：假關閉的每4小時報告、無授權的每30分鐘健康檢查、12個任務失敗通知全靜音
metadata: 
  node_type: memory
  type: project
  originSessionId: 7e7803f9-e7a6-4dbc-a8e9-67c3e8fbcf89
---

# Cron 大體檢 · 2026-07-06

教練連續三次追問觸發的體檢，最終狀態（都已用 `openclaw cron` CLI 驗證live生效，不只是改檔案）：

1. **`d6a8b3cd` 終端機對話總結（每4小時推播）→ 已真的停用**。7/5 的「已關閉」commit是假修復（只改了脫節的 `cron/jobs.json`），live系統當天中午還在推播，7/6 用 CLI 直接 disable 才真的生效。詳見 [[reference_openclaw_cron_json_stale_snapshot]]。
2. **`1cbe1701` 每4小時主動關懷 → 確認本來就沒在打擾教練**，不用處理。live delivery 是 `not requested`，且查 `BOT_MESSAGES.md` 發現這個問候文字最後一次真的送達是 6/6，之後改成 systemEvent 內部模式就沒再對外送出過。
3. **`5d687b38` 每30分鐘任務健康檢查 → 已停用**。查遍 git log（回溯到5/22）與 memory（回溯到5/23）都找不到教練授權這個任務的紀錄，判斷是早期AI自行建立、從未被質疑過。教練親口指示要軍師自己評估利弊再決定，不要丟選擇題回去（詳見 [[feedback_junshi_role_decide_not_ask]] 2026-07-06二次發作記錄）。最終判斷：30分鐘一次的檢查主要價值只是「git自動commit」+「cron連續失敗提醒」，這兩件事完全可以併入既有的每日23:00任務，不需要獨立高頻cron。已把這兩步併進 `dc9bdf5c`（原「場景化升華」，改名「場景化升華+系統健檢（每日23:00）」），平常安靜不額外輸出，只有真異常（cron連續失敗≥3次）才多講一句。
4. **全部12個目前啟用中的cron任務 → 統一關閉failureAlert**（`--no-failure-alert`）。「AI服務暫時過載」這類自癒性錯誤不再推播打擾教練，真正的問題還是會被23:00那次健檢抓到。

## 教訓
`~/.openclaw/cron/jobs.json` 這份檔案曾被視為「改了=生效」，實際上是脫節的靜態快照，導致至少兩次假修復（見 [[reference_openclaw_cron_json_stale_snapshot]]）。以後任何cron變更一律用 `openclaw cron` CLI 操作+驗證，不再手動編輯這份JSON。

## 🔴 2026-07-07 更新：「已修好」其實只修了一半，真正的鎖是 delivery.bestEffort 不是 failureAlert

教練 23:00 那天晚上還是收到「Cron job ... failed: FailoverError: The AI service is temporarily overloaded」的錯誤推播，證明前一天「統一關閉failureAlert」的修復不完整。查 openclaw CLI 原始碼（`~/.hermes/node/lib/node_modules/openclaw/dist/server-cron-CJwAiILI.js`）才發現：

- `job.failureAlert` 只控制「連續失敗N次」的門檻型警報（`emitFailureAlert`），這條路徑昨天確實關對了。
- 但還有第二條完全獨立的路徑 `dispatchCronFailureDestinationNotifications`——**只要單次執行status="error"，且`job.delivery.bestEffort !== true`，不論failureAlert設什麼都會照樣發送**「⚠️ Cron job X failed: ...」到Telegram。這條路徑昨天完全沒處理到。
- 真正能同時擋住兩條路徑的欄位是 `delivery.bestEffort`（CLI參數 `--best-effort-deliver`）。已對4個真的會announce到Telegram的任務（06:00起床摘要 a8450f2c、23:00場景化升華 dc9bdf5c、行事曆每週同步 89b8648d、7/24繳費提醒peipei的de70413e）加上此參數；另外7個delivery本來就是「not requested」的任務不受影響，不用改。
- 驗證方式：讀原始碼確認`mergeCronPayload`是merge不是覆蓋（不會清空message欄位），逐一`cron get`確認`delivery.bestEffort:true`且message欄位完整保留。因為這4個任務會對外送真實訊息（含教練Telegram、佩佩老師群組車貸提醒），沒有用`cron run`實際觸發測試，避免誤發訊息。

**教訓：`--no-failure-alert` 跟「這個任務不會再打擾我」不是同一件事**，openclaw的cron通知系統有兩條互相獨立的程式碼路徑，只改一個參數＝只堵住一半的水管。以後遇到「說關了還是有收到」，第一步是去讀CLI原始碼確認欄位真的對應哪段邏輯，不能只看CLI `--help`的中文說明就假設懂了。

關聯：[[feedback_junshi_role_decide_not_ask]]、[[reference_openclaw_cron_json_stale_snapshot]]、[[feedback_false_success_report_pattern]]
