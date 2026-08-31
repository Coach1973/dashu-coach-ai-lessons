---
name: hermes-pull-progress-rule-2026-08-31
description: Hermes聽到「開工」要主動讀JUNSHI_HANDOFF_LATEST.md（軍師進度），拉取模式取代軍師主動發信通知
metadata:
  type: project
---

教練2026-08-31拍板：Hermes（MiniMax桌面版）聽到「開工」等同義觸發詞時，除了讀自己的`H_HANDOFF_LATEST.md`，也要主動讀`JUNSHI_HANDOFF_LATEST.md`（軍師最新進度），已寫進`~/.hermes/workspace/AGENTS.md`「熱啟動4件套」第3項+`workspace/cross-agent/README.md`補充說明。

**Why**：ai-art動態官網任務，教練16:05口頭交辦給Hermes，Hermes查完架構問題寫信給軍師後，教練追加「教練追加的新需求：即時報名人數」等後續指示，Hermes卻3.5小時零進度也沒回報卡在哪，教練直接來問軍師才發現，軍師只好直接接手做完。軍師原本想寫封信提醒Hermes「這件事我做完了不用重做」，但被`cross_machine_dispatch_guard.sh`鎖擋下（跨機發信需教練先拍板）。教練聽完後沒有同意發那封信，而是指出根本解法：**Hermes沒有Claude Code式的hook介面能被動接收軍師通知**（見`H_HOOKS_PLAN.md`硬限制），與其軍師每次做完事都要手動發信通知（推送模式），不如讓Hermes養成「開工先看一眼軍師進度」的習慣（拉取模式）——這跟軍師自己的「開工六步驟讀接力棒」是同一個設計精神，教練原話：「這個就等同於你發封信提醒Hermes進度的簡訊，道理是一樣的」。

**How to apply**：以後任何「要不要主動通知另一個agent進度」的情境，先問「對方開工時能不能自己去讀」——能讀就優先用拉取模式（改對方的熱啟動必讀清單），不要預設要用推送模式（發信/webhook），後者需要額外的跨機發信審批（見[[reference_deterministic_hooks_over_docs_pattern]]同精神：機制要嵌進對方一定會走的流程，不能只靠單次提醒）。跟[[project_hermes_default_owner_event_tasks_2026-08-31]]、[[project_hermes_bni_connect_task_routing_2026-08-31]]同一組「軍師-Hermes分工」系列記憶，這條補的是「進度可見性」這個之前沒設計到的環節。
