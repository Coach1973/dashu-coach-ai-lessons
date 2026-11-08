---
name: reference_bots_quiet_no_exec_wake_v112_2026-11-08
description: 巴哈「沒人叫自己跑出來長篇回報」＝背景指令跑完通知叫醒主對話；「一直重複說不再回報」＝叫醒那輪沒 exec 工具＋進度鎖每3分鐘逼報進度；11/08 關 notifyOnExit＋safety-locks v1.12
metadata:
  node_type: memory
  type: reference
  originSessionId: 06826f58-cb0f-4738-8c87-cd0c4ef2d513
  modified: 2026-11-08T05:25:43.904Z
---

**查到的（11/08，巴哈 peipei 的 sqlite transcript_events＋/tmp/openclaw/openclaw-2026-11-08.log）**
- 11/06 19:03、11/07 19:05 巴哈自己跳出來解釋「Exec completed (ember-la…)」：每日 19:00 RPL 戰報排程跑的背景指令跑完，通知被送進 `agent:peipei:main`（教練私訊），叫醒一輪 AI。ember-la、clear-gl 是背景指令的隨機代號，不是機器，巴哈還誤認成「另一台機」。「開工，先讀 AGENTS.md」是模型把開機指示唸出來。
- 11/08 12:59 叫醒那輪：`toolsBySender` 對「沒有發話人」的叫醒輪套用 `*` 預設→**沒有 exec**；它找 exec 找 18 分鐘，進度鎖（3 分鐘沒講話就擋）一直逼它發進度→連發約 30 則。教練 13:03、13:15 的訊息因叫醒輪來源不同無法插隊（steer 要求同來源），只能排隊，所以「停」沒用。
- v1.11 叫醒鎖從沒觸發過（日誌 0 次「背景通知叫醒」），偵測條件對不上，等於沒裝。

**修法（commit 4ea325a73）**
- `openclaw config set tools.exec.notifyOnExit false`：背景指令跑完不再叫醒 AI（官方開關，免重啟；分身要結果得用 `process poll`）。
- safety-locks v1.12：一輪最多 3 則純文字 message（附檔不算）→安靜鎖；tool_search／tool_describe 一輪超過 5 次→找工具鎖，要它一句話說卡在哪；進度鎖、悶頭鎖一輪只提醒一次、限 30 字；收尾鎖改成一兩句話不列清單。
- **坑**：`openclaw gateway restart` 會做「restart recovery」把被中斷的那輪接著跑（13:24 又發 2 則給教練）。重啟前先 `openclaw gateway call chat.abort --params '{"sessionKey":"…"}'`，必要時 `sessions.reset {"key":…}`（保留歷史）。

**還沒驗證**：真實對話裡安靜鎖、找工具鎖的觸發（日誌字樣「🤐 安靜鎖觸發」「🔎 找工具鎖觸發」）。

相關：[[reference_bot_long_rounds_root_causes_2026-11-05]] [[reference_bahai_poster_30min_slow_progress_lock_v19_2026-11-03]]
