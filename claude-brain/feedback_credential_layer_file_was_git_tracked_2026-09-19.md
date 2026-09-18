---
name: credential-layer-file-was-git-tracked
description: 路徑大全_憑證層.md與agent/auth-profiles.json自建立起就被git追蹤推上GitHub，違背拆檔隔離金鑰的設計初衷，2026-09-19全機健檢發現並修復
metadata:
  type: feedback
---

2026-09-19教練睡前交辦「好好檢查系統還有哪些漏洞」，軍師自主稽核時發現：`路徑大全_憑證層.md`（2026-07-10特意從`路徑大全.md`拆出、專門用來隔離真實密碼/API金鑰、明確寫著「AI只在真的要操作對應系統時才會打開這份檔案」的安全設計）**自建立那天起就一直被git追蹤，每次更新都推上GitHub**，完全違背當初拆檔案的目的。同案發現`agent/auth-profiles.json`、`agent/models.json`、`agent/models.json.bak`自2026-04-26起也明文含MiniMax真實API key被追蹤。

## 查證細節
- `git ls-files` 直接確認這4個檔案在HEAD都被追蹤（用`git grep`等工具掃描時第一次因為中文檔名shell quoting問題誤判成「沒被追蹤」，第二次改用`git ls-files -- "檔名"`才抓到真相——**中文檔名的git指令一定要對檔名做好quoting，不能只看grep有沒有命中就下結論**）
- repo `Coach1973/mac-openclaw-workflows` 是PRIVATE，且`gh api repos/.../collaborators`確認只有Coach1973本人有存取權，從未加過外部協作者——降低了「已被外部看到」的急迫性，但不代表沒風險（帳號憑證外洩/repo設定失誤都可能讓它曝光）
- 交叉掃描本機另外72個github_repos的HEAD，確認同一組已知外洩金鑰(MiniMax/Gemini/Anthropic)**沒有**重複出現在其他repo
- 掃描BNI-Training/bni-dna/bni-traffic/team-bymyway/coach888/bymyway-website等公開repo，確認個資(統編/電話/email)都有依設計正確留在私有`claude-brain`不外流；admin頁面都有`@login_required`正確保護

## 已完成的修復（可逆、安全）
1. 這4個檔案補進`.gitignore`
2. `git rm --cached`移除git追蹤，**檔案本體完整保留在本機磁碟**，`council_orchestrator.sh`等既有腳本讀取路徑不受影響，服務零中斷
3. commit `96601045c` 已推上雲端

## 尚未處理、需要教練裁示的部分
- **舊commit歷史裡這些內容依然存在**（`git log`/`git show <舊commit>`還挖得出來），untrack只能擋住「未來新增的內容」，不會清掉過去。要徹底清除需要`git-filter-repo`改寫歷史+強制push，這是高影響力操作（會讓其他clone這個repo的機器/session的本機歷史跟遠端產生分歧，需要協調），沒有教練同意不擅自做
- 是否要因此rotate這些已外洩的金鑰（MiniMax key、Gemini key，以及一把在`distill/all_coach_messages.md`裡出現、來源不明、路徑大全裡查無記錄的`sk-ant-api03-jMLa...`金鑰），屬於會影響正式服務的重大決策，同樣留給教練
- 為什麼重要：這個模式（明明有「拆出憑證層檔案」的正確設計，卻沒有同步在`.gitignore`裡排除它，導致設計形同虛設）值得記住——**任何新建立的「本該保密」檔案，建立當下就要立刻確認`.gitignore`涵蓋，不能只靠檔名/資料夾慣例讓人「以為」它是安全的**
- 怎麼應用：往後任何要新建立存放真實密碼/金鑰的檔案（不管是憑證層.md這類文件，還是agent設定檔），建檔的同一個操作裡就要順手補一行`.gitignore`並用`git check-ignore -v`實測確認，不能等到事後稽核才發現
