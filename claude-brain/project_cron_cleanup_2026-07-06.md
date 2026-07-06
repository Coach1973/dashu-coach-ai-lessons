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

關聯：[[feedback_junshi_role_decide_not_ask]]、[[reference_openclaw_cron_json_stale_snapshot]]、[[feedback_false_success_report_pattern]]
