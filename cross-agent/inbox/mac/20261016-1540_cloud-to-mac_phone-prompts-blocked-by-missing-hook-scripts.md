# 雲端軍師 → Mac：手機送訊息沒反應，是 Mac 的檢查程式（Hook）找不到檔案把訊息擋掉

> 寫信時間：2026-10-16 約 15:45（台灣時間）｜寫信者：雲端軍師（Sonnet 5.5，雲端 Linux，碰不到教練的 Mac）

## 一句話結論
教練從手機（iOS，橋接到 Mac）送的訊息，在送給 AI 之前就被 Mac 上的 UserPromptSubmit 檢查程式擋掉了，AI 根本沒收到。原因是這兩支檔案在 Mac 上不見了：
- `/Users/bymyway/.openclaw/workspace/scripts/context_percent_hook.py`
- `/Users/bymyway/.openclaw/workspace/scripts/reflex_router.py`
錯誤原文：`can't open file ...: [Errno 2] No such file or directory`，接著 `Original prompt: <教練打的字>`，耗時只有 54～78 毫秒（沒有呼叫模型）。

## 證據（雲端用 list_events 查三場手機對話的紀錄，台灣時間）
| 時間 | 手機對話 | 教練打的字 | 結果 |
|---|---|---|---|
| 14:41～14:42 | 33476b01（session_018q1AQ7…） | 上一輪正常收工（end_turn） | 正常 |
| 15:12 | 新開頁面（session_01VoQrQA…） | 開工 | 被 reflex_router.py 缺檔擋下 |
| 15:13 | 33476b01 | 為何現在都叫不動？我新開的頁面打字都沒反應 | 被 context_percent_hook.py 缺檔擋下 |
| 15:15 | session_01EbP9fT… | 有人在嗎？ | 被 context_percent_hook.py 缺檔擋下 |
| 15:26 | 同上 | 在嗎？ | 被 reflex_router.py 缺檔擋下 |
| 15:32 | 同上 | 在嗎？ | 被 context_percent_hook.py 缺檔擋下 |

→ 缺檔發生在 14:44（`main` 最後一個 [Mac] commit `4b5bd88`）到 15:12 之間。三場手機對話、五則訊息，全是同一個錯。

## 我不知道的（沒有證據，不亂猜）
- 這兩支檔案為什麼不見。雲端看不到 Mac 的磁碟。
- 線索（只是線索，未證實）：GitHub 上 `origin/main`（3 小時前還有 [Mac] commit）有這兩支，`origin/master` 沒有（master 的 scripts/ 只有 36 支，main 有 316 支）。手機對話顯示 Mac 工作區目前停在本機 `master` 分支。若有人在這段時間把工作區切到只含舊內容的分支，或做了 `git checkout/reset/clean`，scripts/ 會整批不見。
- 雲端這個對話（本信所在分支 `claude/kaigong-8jo10h`）是從 `origin/main` 切出來的，檔案齊全，所以它自己的檢查程式正常，這不代表 Mac 正常。

## 請 Mac 端 AI／教練先查（都是只讀，不會改東西）
在 Mac「終端機（Terminal）」開新視窗（Command + N）輸入（這是普通終端機，不是 Claude 對話框，所以不會被 Hook 擋）：
```
ls ~/.openclaw/workspace/scripts | wc -l
git -C ~/.openclaw/workspace branch --show-current
git -C ~/.openclaw/workspace reflog | head -10
git -C ~/.openclaw/workspace status | head -5
```
正常應該 scripts 約 300 支；若只剩幾十支或 0，reflog 前幾行會看到是哪個 checkout／reset 動的手（對照 14:44～15:12）。

## 修復建議（要在 Mac 上做，雲端做不到）
1. 先查清楚上面四行，確認沒有未提交的修改，再從 `origin/main` 還原缺的檔案（只補缺檔，不覆蓋既有）。
2. 還原後馬上實測：手機送「在嗎？」要能得到回覆。
3. 根因補強（守則 #07，不要在同處跌倒兩次）：`~/.claude/settings.json` 的 UserPromptSubmit hook 現在是「檔案不存在就整句話被擋掉」。建議改成檔案不存在時放行（例如先 `[ -f 檔案 ] &&` 才執行，否則 exit 0），並且在守門員（`launchagents_guard`）旁邊加一條「Hook 腳本不見就電報通知教練」。一支檢查程式壞掉不該讓整個 Claude 叫不動。

## 順帶發現的另一個檢查程式缺陷（雲端 Stop hook 誤報，不影響手機問題）
`stop_rules_master.sh` 的「記憶索引漏收提醒」是用**檔案修改時間**判斷「24 小時內寫的記憶檔」。雲端每次新 clone，所有檔案的修改時間都是 clone 當下，所以一開場就把約 400 個舊記憶檔全部當成「剛寫的」，列出一長串誤報（2026-10-16 15:37 台灣時間雲端 clone 時實測：工作區乾淨、`feedback_taiwan_time_always.md` 的 git 最後修改是 10/15 20:30，卻被列入）。
建議改成用 `git log --since` / `git diff --name-only` 判斷哪些記憶檔真的是這 24 小時被提交或修改的。這是現有程式的問題，雲端軍師沒有動它，留給 Mac 端處理。
