---
name: feedback-verify-activity-via-git-log-not-relay-file
description: 判斷「某台機器今天有沒有活動」要查真實git commit紀錄，不能只憑中繼蒸餾檔案存不存在
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4eeebf94-4cbb-479b-9c44-1331f8eccf03
---

判斷「教練有沒有在某台機器上對話/工作」時，優先查該機器commit回共用repo的真實git log（例如`[Win]`/`[ACER]`前綴commit），不能只憑一個間接的「蒸餾/同步」中繼檔案存不存在來下結論。

**Why**：2026-07-19 三機每日總結cron誤報「聯想連續11天沒有對話」，教練當場反駁他其實一直在用。查證後發現：cron判斷邏輯只看`memory/verbatim/{acer,lenovo}/YYYY-MM-DD.md`存不存在，而這個檔案是靠`distill_and_push_acer.sh`/`distill_and_push_lenovo.ps1`這套中繼蒸餾機制產生的——但這套機制從2026-06-30建立以來，ACER端從未真正排程執行過（目錄只有空的`.gitkeep`），Lenovo端只手動跑過一次（7/8）之後11天沒有新檔案。同時查真實workspace git log，聯想軍師當天下午15:26才剛真實commit過一筆工作，直接推翻cron的誤判。詳見試金石案例52。

**How to apply**：
1. 任何「判斷某機器/某系統有沒有活動」的自動化邏輯，優先選「本來就會自然發生、不靠額外機制」的痕跡（如commit log），而不是設計一套額外的「蒸餾→推送」間接管線——間接管線環節越多，越容易在沒人發現的情況下斷掉
2. 一套跨機自動化機制上線時，只驗證過一次成功不代表它會持續運作，尤其是需要在別台機器上排程執行的部分，要定期抽查是否真的在跑（可比對這套機制自己的commit歷史）
3. 教練親口反駁系統的自動判斷時，優先信教練的真實使用經驗，回頭查證系統邏輯哪裡有假設沒有成立，而不是假設教練記錯

Related: [[feedback_check_crossmachine_history_before_system_ops]]、[[reference_openclaw_cron_json_stale_snapshot]]
