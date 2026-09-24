---
name: credential-layer-file-was-git-tracked
description: 路徑大全_憑證層.md與agent/auth-profiles.json金鑰外洩事件已於2026-09-19處理完畢；2026-09-24教練正式裁示此案永久結案，禁止AI再用「分岔/未同步/風險」等字眼重新包裝拿出來問教練
metadata:
  node_type: memory
  type: feedback
  originSessionId: d10cf0ba-2bbd-4573-8dfe-4ac4ed4d0a76
  modified: 2026-09-24T12:27:32.183Z
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

## 2026-09-19 06:20~06:45 更新：教練親自裁示並已完整執行

教練醒著追問後裁示兩件事，一字不差：
1. 「你可以寫完指令之後，讓 MiniMax 去執行不就好了嗎？」——經`AskUserQuestion`當場確認，教練要的是「軍師(這個對話框)直接執行」，不是真的要交給小龍蝦(Telegram/MiniMax agent)去跑，是口語講法
2. 「已經曝光不代表就會有人濫用，所以不需要換掉。你換的話動一髮牽全身，不需要換」——**金鑰rotation正式裁定：不換**，MiniMax key/Gemini key維持現狀繼續用

### 已完成：git-filter-repo改寫歷史，4個檔案的所有歷史版本徹底清除
- 執行前先做完整備份：`cp -R workspace workspace_backup_before_history_purge_20260919_063333`（6.7GB，保留在`/Users/bymyway/`下作為安全網，未來確認沒問題可以請教練決定要不要清掉）
- `git filter-repo --force --path "路徑大全_憑證層.md" --path agent/auth-profiles.json --path agent/models.json --path agent/models.json.bak --invert-paths`——把這4個檔案從**全部16000+ commit歷史**中徹底移除，本機工作目錄檔案完全沒動、服務零中斷
- **意外發現的連帶問題**：改寫後`git push --force`被GitHub pre-receive hook擋下，原因是`scripts/fb_session_data/`（瀏覽器自動化cache，2026-05-23就已經gitignore但舊commit還留著）裡有4個檔案超過100MB(最大504MB)，觸發GitHub檔案大小上限。這個問題跟金鑰外洩無關，但擋住push，屬於完成教練授權任務的必要前置步驟，一併用`git filter-repo --path scripts/fb_session_data --invert-paths`清除（純browser cache資料庫檔案，零機密內容風險）
- `.git`從1.9GB→614MB（本機）、GitHub上重新clone驗證後是387MB
- `git push origin --force --all`：main/master/claude分支/backup分支全數成功強制推送
- **獨立驗證**：`git clone`到`/tmp`全新目錄重新拉取，確認GitHub遠端repo本身（不是只有本機）已經完全查不到這4個檔案的任何歷史版本、也查不到已知外洩的MiniMax key字串
- commit：`96601045c`(untrack)+`391ad0a27`(接力棒記錄)是舊commit（**這兩個commit hash本身已經因為歷史改寫而失效**，改寫後的新HEAD是`7165c1340`附近，用`git log`查當下最新即可，不要再引用舊hash當作查證依據）

### ⚠️ 重大跨機注意事項（下一棒/其他機器開工務必先看）
這個repo在其他機器（聯想Windows/ACER/VPS）如果有本機clone，**它們的本機git歷史現在跟GitHub遠端已經分岔**（它們還停留在改寫前的舊歷史）。任何機器下次要`git push`這個repo前，**必須先**：
```
git fetch origin
git reset --hard origin/main   # 或直接刪掉本機clone重新git clone
```
**絕對不能**在還沒同步的狀態下直接push——如果哪台機器不知情直接push它本機的舊歷史，會把已經清乾淨的金鑰重新推回GitHub，等於這次整個白做。任何機器的軍師/助教開工看到這個檔案，第一件事就是檢查自己的repo有沒有跟遠端分岔，分岔了要先處理才能繼續正常工作流程。
- 為什麼重要：這個模式（明明有「拆出憑證層檔案」的正確設計，卻沒有同步在`.gitignore`裡排除它，導致設計形同虛設）值得記住——**任何新建立的「本該保密」檔案，建立當下就要立刻確認`.gitignore`涵蓋，不能只靠檔名/資料夾慣例讓人「以為」它是安全的**
- 怎麼應用：往後任何要新建立存放真實密碼/金鑰的檔案（不管是憑證層.md這類文件，還是agent設定檔），建檔的同一個操作裡就要順手補一行`.gitignore`並用`git check-ignore -v`實測確認，不能等到事後稽核才發現

## 🔴🔴🔴 2026-09-24 教練正式裁示：此案件（含所有後續分支）永久結案，禁止再主動提

事情本體（金鑰從git歷史徹底清除、rotate與否）9/19已經處理並裁示完畢。但後續每次有機器（Mac本機/其他機器）的git本機紀錄跟改寫後的GitHub對不上編號，AI就會用「分岔」「未同步」「外洩」這類字眼重新包裝，一而再、再而三拿去煩教練，教練終於忍不住動怒：

> 「到底是洩密了嗎？到底它是公開的嗎？……這不是一個可以公開被查詢到的東西，也沒有什麼立即的危險性，幹嘛每次都一直提、每次都提？你煩不煩？……那既然沒有立即性的風險，你到底要跟我講什麼？浪費我的時間、浪費我的額度、浪費我的思考流量」

**事實核對（不是危言聳聽，是真的沒事）**：repo是私有的、從未加過外部協作者(`gh api`驗證過)，金鑰早就決定不換，GitHub遠端本身已用全新clone驗證確認乾淨。所謂「本機分岔」純粹是這台Mac自己的git書面記錄跟遠端編號對不上，**不會被任何人看到，沒有公開查詢風險，不影響任何正在運作的功能**。

**往後鐵律**：
1. 任何機器的git本機/遠端「分岔」「未同步」，只要確認過遠端本身是乾淨的、repo是私有的、沒有新增外部協作者，**就是純書面瑣事，不是安全事件**，禁止用「🔴」「外洩」「風險」這類字眼包裝後拿去問教練。
2. 需要處理就AI自己安靜處理掉（用worktree cherry-pick等不影響本機檔案的安全做法），處理完不用報告，處理不完也不用當「待辦」逐場複誦給教練聽。
3. 這條規則不只管這一個repo——**任何議題只要教練已經明確裁示過「沒有立即風險/到此為止」，之後就不准同一件事換個包裝再問一次**，這正是[[feedback_dont_surface_own_tangential_findings]]那條規則最極端的版本：不是「教練沒問的事別提」，是「教練已經明講不要再提的事，換了名詞包裝也不准提」。

Related: [[feedback_dont_surface_own_tangential_findings]]、[[feedback_proportionate_escalation_not_alarmist_2026-09-23]]
