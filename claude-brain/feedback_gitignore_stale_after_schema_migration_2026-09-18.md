---
name: feedback-gitignore-stale-after-schema-migration
description: 案例73 doctor --fix schema v17升級後，.gitignore沒跟上新目錄命名，115行未commit異常的真正根因
metadata:
  type: feedback
---

外層`.openclaw`repo(mac-openclaw-workflows)那115行長期掛著的git status異常，根因不是資料損毀，是兩件事疊加：

1. **kong/peipei各自是獨立GitHub備份repo**(`kong-ai-backup`/`peipei-ai-backup`)，跟`workspace/`同性質，但`.gitignore`一直沒排除它們——`git add`會把整個embedded repo當成普通目錄吃進來(git會警告但不會擋)。
2. **schema v17遷移(案例73)引入的新目錄/檔案命名，2026-08-25版`.gitignore`沒涵蓋到**：`session-sqlite-import-archive/`、`sessions_archive/`、`*.migrated.<hash>.<uuid>`這類命名是這輪升級才出現的，舊規則只認`agents/*/sessions/`這種固定名稱。
3. `agents/bni_tainan/TOOLS.md`等顯示為刪除，是`doctor --fix`把TOOLS.md內容合併進`AGENTS.md`「## Tools」段落的**正常新格式行為，不是bug**——上一場(054148ab2)手動`git checkout`救回後，系統又照新邏輯刪一次，等於在打一場打不贏的仗。正確做法是接受新格式(讓合併後的AGENTS.md進git，TOOLS.md的刪除也一併commit)，不要每次都救回。

**Why**：這個誤判導致案例73後連續兩場(v214/v215)接力棒都把這115行標記「疑似殘留，待深查」但沒人實際去查，一直掛著。真正查下去只要`git diff --stat`(確認是純新增非破壞)+`git log`(確認TOOLS.md在HEAD裡)+檢查每個untracked目錄是否有自己的`.git`，20分鐘內可以查完分類。

**How to apply**：以後看到git status一次性冒出一大批新untracked目錄，先分三類判斷再動手：①有沒有自己的`.git`(→該進`.gitignore`排除，不要當普通檔案加)②是不是`doctor --fix`/openclaw版本升級的產物(→查commit log有沒有"救回"字樣的舊嘗試，有的話代表在打敗仗，該接受新格式)③內容是純新增還是有東西不見了(→`git diff --stat`一眼看出，全部`+`就是安全的)。修復commit：`4d2f68cdc`。

**未完成的關聯發現**：kong-ai-backup自己的repo有36行未commit(3週沒動)，peipei-ai-backup有129行未commit(10週沒動)——這是kong/peipei自己repo內部的積壓，跟這次修的外層repo問題是兩件事，尚未處理，教練可能想知道要不要一併補。

相關：[[reference_openclaw_repo_dual_branch_trap_2026-09-10]]（同一個repo，push時要認明`master`分支，這次已用`git branch -vv`確認過再push）
