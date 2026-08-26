---
name: feedback-minimax-batch-call-redline-guard-2026-08-27
description: 教練畫下永久紅線——任何批次呼叫MiniMax的程式碼都必須接上scripts/minimax_batch_guard.py的guard_call()，越線自動硬停不是口頭提醒
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65db632c-0f23-4fd8-aaf3-3f247ae2fd81
  modified: 2026-08-26T17:24:43.283Z
---

案例65（2026-08-26，見[[project_namecard_manual_trigger_matching_design_2026-08-27]]）：
`chain_matcher.py`批次跑428人媒合，系統提示詞沒快取、呼叫沒節流，短時間燒了
約150萬token，把MiniMax帳號5小時4500次呼叫額度全部打滿，教練所有服務
（小龍蝦/BNI小幫手/教練都在想什麼/VPS小龍蝦）同時停擺3小時。當時的修復
（cache_control+3秒節流）只補了那一支腳本，不是系統性防線。

2026-08-27教練追加明確指令：「畫下一條紅線，之後任何類似這種一次性會把我
5個小時、4500次呼叫額度全部用完的行為，全部都要拉紅線限制…用AI智慧去判斷，
永遠不要再出現這種情況。」

**已建立的紅線（程式碼層級，不是文件宣告）**：`scripts/minimax_batch_guard.py`
提供`guard_call(caller_name)`，任何要呼叫MiniMax API的地方在真正發API request
前都要先呼叫這個函式。機制：
- 用共用log檔（`state/minimax_batch_call_log.jsonl`）記錄「所有批次腳本」
  過去5小時內的呼叫次數（滾動窗口，不是各腳本各自算，因為帳號額度本來就共用）
- 硬上限400次/5小時（帳號真實上限4500次的~9%，其餘91%永遠留給即時互動服務）
- 越線直接拋`MiniMaxBatchGuardError`中止整個批次（呼叫端不可try/except吞掉），
  同時主動發Telegram通知教練，不用等教練自己發現服務停擺
- 每滿50次額外推播一次進度，讓教練有感知，不是悶頭燒到中止才第一次出聲
- 2026-08-27已用真實情境測試驗證：正常呼叫通過/超過上限正確中止/超過5小時
  窗口的舊紀錄正確被排除不誤判/中止時Telegram真的送達（非僅程式邏輯正確）

**已接上的呼叫點**（namecard-db，案例65發生地）：`chain_matcher.py`的
`_call_ai()`、`extract.py`的`extract_card_fields()`、`match.py`的
`build_category_relationships()`——這三個是目前workspace裡所有會迴圈呼叫
MiniMax的實際choke point。

**Why**：教練把這件事定位成「僅次於Windows硬碟被整個刪掉」的第二嚴重事故，
明確要求要有結構性防線而非事後檢討。跟既有原則[[feedback_lock_must_be_hook_not_optin]]
（防呆鎖必須是hook不能opt-in）同一個精神——把規則寫進memory只能防「我這次
記得」，寫進程式碼的hard ceiling才能防「我這次沒想到會這樣」。

**How to apply**：
1. 未來在workspace任何專案裡新寫或修改會呼叫MiniMax/Anthropic相容API的程式碼，
   第一件事就是`sys.path`加`scripts/`後`from minimax_batch_guard import guard_call`，
   在每次`client.messages.create()`之前呼叫`guard_call("<呼叫端名稱>")`，
   不分專案、不分是不是「看起來只會呼叫幾次」——案例65一開始也沒人覺得
   428人算多。
2. 看到任何"for 迴圈 + API呼叫"的組合，先假設它有跑到幾百次以上的可能性，
   接上guard再寫，不要等出事才補。
3. 這個400次/5小時的上限如果哪天真的因為業務需要（例如一次要處理上千人）
   顯得太保守，要調整前先跟教練確認「這次批次任務大概要用多少次額度」，
   由教練決定要不要臨時放寬，不要自己偷偷改CEILING數字繞過。

Related: [[project_namecard_manual_trigger_matching_design_2026-08-27]]（案例65
本體）、[[feedback_lock_must_be_hook_not_optin]]（同精神：防呆要是機制不是
opt-in）、[[feedback_jarvis_outcome_delegation_style]]（同場教練要求自主判斷
不用每次都問）
