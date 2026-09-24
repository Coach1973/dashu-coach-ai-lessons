---
name: agents-directory-lost-from-git-history
description: agents/bni_tainan與agents/jiaolian_thoughts兩個子agent的AGENTS.md/DREAMS.md曾整批從HEAD跟origin/main消失(高度疑似09-19 git-filter-repo改寫與並行commit分岔)，已從懸空commit救回，commit fff330028
metadata:
  node_type: memory
  type: reference
  originSessionId: 055522b8-9175-4e6b-8d08-d83e98515a06
  modified: 2026-09-23T05:16:21.799Z
---

2026-09-23教練交辦「全面體檢」時，`openclaw doctor`回報「Agent bni_tainan: Memory system not found in workspace」，查證發現`agents/bni_tainan/`、`agents/jiaolian_thoughts/`兩個子agent的AGENTS.md+DREAMS.md完全不在當時的HEAD跟origin/main的git樹裡（`git ls-tree HEAD agents/`兩邊皆空），磁碟上也不存在——不是沒commit，是整批消失。

## 查證細節
- 這兩個子agent的內容曾在commit `936dfd205`(Sep 18)、`3361e3078`(Sep 19 05:35 "補燒核心對話紀律精簡版")真實存在過，`git show 3361e3078:agents/bni_tainan/AGENTS.md`可以讀出完整內容
- `git merge-base --is-ancestor 3361e3078 HEAD`確認：**不是HEAD的祖先**——這兩個commit是懸空(dangling)物件，還沒被gc回收，但已經不在目前分支的正常歷史線上
- 高度疑似根因：09-19 06:20~06:45那次`git-filter-repo`徹底清除金鑰歷史+強制推送(見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]])，跟另一個並行對話框當時剛好也在commit這兩個子agent的人設更新(05:35)撞在同一個時間窗，導致這批commit沒被納入改寫後的歷史，本機ref之後被同步腳本reset到改寫後的遠端版本
- 這台Mac本地reflog只保留約1.5天的量(269筆)，找不到更早的rewrite事件痕跡，無法100%還原改寫當下的操作序列，但内容確定沒有真的遺失

## 已完成的修復
用`git show 3361e3078:<path>`從懸空commit救回4個檔案(agents/bni_tainan/AGENTS.md+DREAMS.md、agents/jiaolian_thoughts/AGENTS.md+DREAMS.md)，內容經檢查完整無損(834~901行不等)，commit `fff330028`已推上雲端。這兩個小幫手運作時用的是硬碟上獨立的當前版本檔案，這段期間沒有實際功能受影響，差別只在「雲端git歷史裡有沒有備份」。

## 教訓
1. **懸空commit不會立刻消失，但會被gc清掉**——這次能救回是運氣，`git gc --aggressive`或系統自動gc如果先跑，這批內容就真的永久遺失了。以後任何「git歷史突然對不上」的異常，優先檢查`git log --all`裡有沒有相同commit訊息但不同hash的版本，可能就是類似的分岔遺留
2. 教練認為這類事故跟「全面改」指令範圍沒問清楚有關，見[[feedback_quanmian_scope_must_clarify_2026-09-23]]
3. 這個repo在高頻並行寫入(多個對話框/自動化腳本同時commit)的情況下，任何大規模歷史改寫操作(filter-repo/rebase)都有跟並行commit相撞的風險，未來要做類似操作前，最好先確認當下沒有其他session正在對同一個repo寫入
