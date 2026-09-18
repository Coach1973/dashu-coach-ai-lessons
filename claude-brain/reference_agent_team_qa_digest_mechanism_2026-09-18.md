---
name: reference-agent-team-qa-digest-mechanism-2026-09-18
description: AI團隊(MiniMax手機Remote Control等)品質稽核機制——stop_rules_master.py 13條規則本來就event-driven稽核所有session，新增agent_team_qa_digest.py彙整違規log掛進開工流程
metadata: 
  node_type: memory
  type: reference
  originSessionId: 915e272e-7a9b-4c59-b1ae-7377bdea7f62
  modified: 2026-09-18T09:23:33.015Z
---

教練問「怎麼監督MiniMax小老弟的品質」，查證發現`scripts/stop_rules_master.py`的13條規則(A~M)本來就對「任何觸發Stop事件的session」自動稽核，不管是軍師自己還是手機MiniMax Remote Control session，同一套標準：完成聲明要有commit hash證據(B/H)、不能叫教練複製貼上(A)、時區換算(C)、不該用輪詢設計(D)、未查證就下結論(E)、方向清楚卻多此一舉問(F)等。這套機制不是2026-09-18才建立，是本來就在跑，只是違規記錄各自寫進`distill/*violations.log`沒人讀，等於黑洞。

**已補上的彙整機制**：`scripts/agent_team_qa_digest.py`——
- 追蹤每個violations.log的已讀行數(`state/agent_team_qa_last_read.json`)
- 只彙整「上次讀過之後」的新違規，按session分組
- 用session transcript裡assistant訊息的`model`欄位（非猜測平台）判斷是📱手機MiniMax還是🖥️本機Claude
- 掛進`scripts/feed_junshi_handoff.sh`六步驟注入尾段：沒有新違規完全安靜不輸出，有才顯示

**已知限制**：這套機制只能抓「機械式規則」(有沒有守規矩)，抓不到「這個任務的理解/做法是否恰當」這種語意判斷——像評鑑MiniMax處理真鑫/真鑽戰情儀表板任務的做法是否合理，仍需要軍師實際讀transcript才能判斷，無法自動化。

**AI團隊名冊**：已寫進`路徑大全.md`「🤖 AI團隊名冊」章節，列出MiniMax-M3(教練手機Remote Control任務執行)+LK888(產業鏈圖生成)，之後教練提到新的免費/便宜API直接補進那張表。

**相關**：[[feedback_hook_hardcoded_identity_assumption_2026-09-18]]（同一場稽核發現的另一個問題）
