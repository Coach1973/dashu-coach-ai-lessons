---
name: feedback-alert-only-when-actually-broken
description: 自動監控/健康檢查類cron的通知門檻，只有「現在仍壞+非provider暫時過載+真影響工作」三者都成立才能announce教練
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d8379d77-adf5-400e-83ab-3a764cb45d47
  modified: 2026-08-05T02:54:02.645Z
---

自動化監控（健康檢查cron、錯誤告警等）通知教練前，必須先問三個問題，全部成立才能真的傳訊息：①現在（本輪執行當下）還壞著嗎，不能只看歷史上連錯幾次；②錯誤原因是不是AI供應商端暫時過載（如minimax overloaded/FailoverError），這類錯誤教練無法介入處理，通知沒有意義；③這件事真的影響教練的工作或會員體驗嗎，不能是監控工具檢查自己時的meta迴圈打嗝。

**Why：** 2026-08-05上午「🦞每30分鐘任務健康檢查」cron（jobId `46e67e2e-6332-4589-aae2-ee7e10dd7279`）連錯5場（08:00~10:30，全是minimax provider暫時過載`FailoverError: temporarily overloaded`），觸發舊規則「連續錯誤≥3必announce」，但送出警報的那一輪執行本身其實已經成功——教練收到一則「早就解決」的假警報，當場糾正：「像這種事情就不要跟我報告了，因為根本不影響我的工作。不正常的時候，再來跟我報告。像這種情況寫這些給我，真的是浪費我的注意力。」舊規則的漏洞是只看「過去連錯幾次」的靜態計數，沒看「現在還壞不壞」的即時狀態。

**How to apply：** 已將該cron的payload.message改為v4.0版，加入三關判斷邏輯（`openclaw cron edit <id> --message "..."`），並用`openclaw cron run <id> --wait`實跑驗證：同樣的「已恢復+provider過載+不影響工作」情境下，v4.0版正確判定「三關全未通過」，不再announce（`deliveryStatus: not-requested`，`delivered: false`）。往後任何新建的健康檢查/監控類cron，通知門檻設計都要套用這三關邏輯，不能只用「連續失敗N次」這種不看當下狀態、不分錯誤原因的簡單計數規則。

Related: [[reference_openclaw_cron_json_stale_snapshot]]（cron設定要用CLI改，不能改靜態json檔）
