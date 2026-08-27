---
name: reference-croncreate-future-date-automation
description: 教練要求「某個未來時間點後自動做X」時，用Claude Code原生CronCreate排一次性durable任務的做法+多機保險寫法
metadata: 
  node_type: memory
  type: reference
  originSessionId: d5fe9c18-5091-4fff-8716-7d9c0b806495
  modified: 2026-08-27T19:13:33.202Z
---

教練說「活動結束時再自動移過去」這類**未來某個時間點觸發一次性動作**的需求，不能只是口頭記著到時候會做（違反[[feedback_no_background_polling_lies.md]]），要用真實排程機制。

**做法**：Claude Code原生`CronCreate`工具支援一次性任務——`recurring:false` + `durable:true`，cron欄位填死當天日期時間（如`"30 17 16 9 *"` = 9/16 17:30）。`durable:true`會寫進該機器的`.claude/scheduled_tasks.json`，就算這場session結束、機器重開機，下次教練在那台機器開Claude Code時，錯過的一次性任務會被catch-up機制偵測到並補跑。

**已知限制**：這個排程只綁定在「當下這台機器」，若教練那天不一定會用同一台機器，單靠這個不夠保險。**保險做法**：同時把要執行的動作寫成一支獨立腳本（不依賴CronCreate才能跑），並把「等待觸發中」的待辦寫進共用workspace的`JUNSHI_HANDOFF_LATEST.md`主表最上面，附上腳本路徑+一句話說明「任何機器看到這行、時間到了直接手動跑腳本即可」，這樣不管教練那天用哪台機器開工，都能被接手。

實戰案例：`scripts/deploy_bigtree_after_0916_event.sh`（git pull+git archive+Netlify Deploy API）+ 聯想CronCreate job`ee5beb77`(9/16 17:30) + 待辦表記錄，三層保險並存。
