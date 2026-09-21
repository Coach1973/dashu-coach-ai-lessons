---
name: feedback-check-handoff-before-diagnosing-git-anomaly-2026-09-21
description: git pull失敗/歷史異常時，先Read本機HEARTBEAT.md和接力棒檔案內容(不透過git)，很可能其他機器已經記錄過同類事件和正確處理方式，不用自己從零診斷
metadata:
  node_type: memory
  type: feedback
  originSessionId: d6427818-40d6-4ebb-b6c7-7df37b76c1f0
  modified: 2026-09-21T13:25:49.676Z
---

2026-09-21「總結」流程裡，`mac-openclaw-workflows`(聯想Windows clone)出現`git pull`回報`refusing to merge unrelated histories`、且卡在一個中斷6天的interactive rebase。軍師直接一頭栽進git底層診斷（`git merge-base`查共同祖先、`git log`比對兩邊commit數量），花了不少功夫得出「這是一個未知原因、從很早以前就存在的雙歷史問題」的錯誤結論，還為此寫了一則記憶檔。

**真相**：Mac那邊2026-09-19已經用`git-filter-repo`把含明文金鑰的4個檔案從全部16000+ commit歷史徹底清除並強制推送，接力棒待辦表最上面就有一條🔴🔴🔴「⚠️全機必讀：這個repo的git歷史已被改寫，其他機器的本機clone跟遠端分岔」，連正確處理方式（`git fetch origin && git reset --hard origin/main`）都寫好了。軍師是在git pull失敗、卡進rebase診斷的過程中才意外看到系統自動附加的CLAUDE.md鏡像內容才發現這條警示，等於繞了一大圈才撞見答案，過程中還寫錯一則記憶檔（已刪除更正）。

**Why**：`git pull`失敗本身就是「本機repo跟其他機器的操作不同步」的直接訊號，這正是接力棒/HEARTBEAT.md存在的意義——記錄「其他機器已經做過什麼會影響這台機器」的事。直接對著git底層下診斷指令，等於跳過了「先看看有沒有人已經記錄這件事」這一步，是重複發明輪子。

**How to apply**：
1. 任何git操作出現非預期錯誤（pull被拒、歷史異常、push衝突）時，第一反應不是繼續下更多git診斷指令，而是先用Read工具直接讀本機的`JUNSHI_HANDOFF_LATEST.md`最上方待辦表 + `HEARTBEAT.md`——這兩份檔案是本機檔案，不受git pull失敗影響，隨時可讀，且是「其他機器已知問題」最可能被記錄的地方
2. 尤其是`mac-openclaw-workflows`這個repo，任何機器對它做危險操作（git-filter-repo改寫歷史、大規模reset等）都應該（且過去實際上有）第一時間寫進接力棒待辦表最上面標🔴🔴🔴，這是查證的第一站，不是最後一站
3. 對不確定的分析先別急著寫進memory——這次錯誤記憶檔只存在了幾分鐘就被更正，代價不大，但如果沒有及時發現接力棒裡的真相，錯誤記憶可能會誤導未來的session

Related: [[reference_openclaw_repo_dual_branch_trap_2026-09-10]]（同類「多機git協作藏著看不見的分歧」教訓，但那次也是靠查證/沒有先看記錄才繞了一圈）
