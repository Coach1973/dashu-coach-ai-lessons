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

## 追加（2026-10-16 17:05 台灣時間）：教練回報 https://event.bymyway.com/curated/angel-sister/ 無法顯示，且 Mac 本機一樣被 Hook 擋
雲端查到的（雲端連不到 event.bymyway.com：雲端網路規則回 403，WebFetch 連 example.com 都解析不到，所以**沒有親眼看到這個網址的回應**）：
- 網頁本身沒壞：`Coach1973/angel-sister` 最新 commit `e3d6d6a`（10/16 01:50 台灣時間）只改頁尾一行，index.html 10.6 MB（90 張內嵌圖，自 10/15 上架就這麼大），HTML 標籤成對、結尾完整。
- 這站由 `event-signup/app.py` 的 `/curated/<slug>/` 供應：**每次請求都從硬碟讀** `event-signup/curated_sites_registry.json`，檔案不存在就當名冊為空，所有 `/curated/*` 一律 404；再從 `/Users/bymyway/github_repos/<slug>/index.html` 送出。
- `origin/master` 沒有 `event-signup/`、`scripts/` 大部分、`CLAUDE.md`（共 3827 個檔案只在 `main`）。如果 Mac 的 workspace 工作區被切到只含 master 內容的狀態，Hook 腳本和這份名冊會**同時**消失，剛好解釋「Hook 缺檔」和「策展頁 404」兩件事。**這只是推論，尚未在 Mac 驗證。** 10/15 21:08 也發生過同類事故（commit `614c4c6`，名冊被 stash 走沒放回，angel-sister 當時 404）。
- 網站程式監聽 5060（`EVENT_PORT` 預設），launchd 用 `workspace/event-signup/venv/bin/python app.py` 並 `source .env`；`venv/`、`.env` 不在 git，若被清掉無法從 GitHub 還原。

Mac 端一次檢查＋補缺檔（只補硬碟上不存在的檔案，不覆蓋、不刪除；補完本機仍非 200 才重啟 `com.coach.event-webapp`）：
```
cd ~/.openclaw/workspace
echo "分支: $(git branch --show-current)"; echo "最近動作:"; git --no-pager reflog -6
echo "補之前本機回應: $(curl -s -m 10 -o /dev/null -w '%{http_code}' http://127.0.0.1:5060/curated/angel-sister/)"
git fetch -q origin main
git ls-tree -r -z --name-only origin/main | while IFS= read -r -d '' f; do [ -e "$f" ] || printf '%s\0' "$f"; done > /tmp/missing_files.nul
echo "工作區缺檔數: $(tr -cd '\0' < /tmp/missing_files.nul | wc -c | tr -d ' ')"
[ -s /tmp/missing_files.nul ] && git --literal-pathspecs restore --source=origin/main --worktree --pathspec-from-file=/tmp/missing_files.nul --pathspec-file-nul && echo "已補回缺的檔案"
c=$(curl -s -m 10 -o /dev/null -w '%{http_code}' http://127.0.0.1:5060/curated/angel-sister/)
if [ "$c" != "200" ]; then launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp; sleep 6; c=$(curl -s -m 10 -o /dev/null -w '%{http_code}' http://127.0.0.1:5060/curated/angel-sister/); fi
echo "補完後本機回應: $c"; echo "網頁檔: $(ls ~/github_repos/angel-sister/index.html 2>&1)"
```
本機回應 200 但公開網址仍打不開 → 查 `com.coach.event-tunnel`（cloudflared）。
