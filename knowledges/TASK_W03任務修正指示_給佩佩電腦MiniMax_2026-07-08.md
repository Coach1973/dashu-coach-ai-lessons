# 任務：修正 W03 C槽增量搬家執行方向（給佩佩老師電腦 MiniMax 終端機）

> 設計者：Mac 軍師 ｜ 2026-07-08 清晨
> 執行者：佩佩老師電腦 OpenClaw MiniMax
> 起因：你剛才查了 `D:\Claude-Data\memory-source\`，那是別的機制，跟這次任務無關，方向查錯了

---

## 🎯 一句話任務

幫佩佩老師電腦做「C 槽資料增量搬到外接碟」，走 **W03 完整生命週期 SOP**（跟聯想機、ACER 機做過的同一套）。

## 🌙 教練已經去休息了，這次改成「自主跑完，安全內行動」

教練已經連續工作超長時間，天快亮了，現在要去睡覺，**不會再盯著你、也不會再回覆你的問題**。所以這次規則改成：

- **能自主做的（Phase 1 搬移），你自己判斷、自己跑完全部 App，不用每個都停下來問**
- **但任何「不可逆」的動作，一律不做，全部留到教練醒來自己確認**——這是安全紅線，不因為教練说不用问就放寬
- 全部跑完（或跑到不能再跑）之後，寫一份總結報告，讓教練起床一次看懂，而不是要他一步步盯著

**什麼算「不可逆」，绝对不做：**
- ❌ 不要刪除任何東西（包括呼叫 `delete_guard.ps1` 的 `Safe-Remove`）——即使看起來很有把握
- ❌ 不要進入 W03 Phase 3（清理孤兒資料夾）——那是搬完、觀察 7 天之後才能做的事
- ❌ 遇到「這個 App 該怎麼分類（主程式 vs 資料）」判斷不出來、或跟 W03 對照表對不上的陌生 App → **跳過這個 App，不要用猜的硬做**，記錄進報告的「待確認清單」，繼續下一個

**Phase 1 本身是安全的，因為原資料只改名成 `.stale_backup`，不刪除、隨時可還原**——這就是為什麼這部分可以自主做完，不用等教練點頭。

---

## 🔴 你剛才查錯的地方（先看這段，避免重蹈覆轍）

你去查了 `D:\Claude-Data\memory-source\` 這個資料夾，發現裡面沒有 W03、沒有 git repo、只有 `sync-memory.ps1` 單向鏡像。**那個資料夾是別的用途，跟這次任務無關，不要再往那邊查。**

真正的 SOP 都在 `mac-openclaw-workflows` 這個 git repo 裡（教練跟另外兩台電腦共用的雲端大腦）。

---

## 📂 第一步：確認環境，pull 最新版

**這個 repo 是私有的（private），不掛認證會 clone 失敗，這是這台機器第一次接這套系統，請照下面順序做：**

### 1a. 先確認 Git 有沒有裝
```powershell
git --version
```
如果報錯「找不到命令」，先裝：
```powershell
winget install --id Git.Git -e --source winget
```
裝完**重開一個新的 PowerShell 視窗**再繼續（PATH 才會生效）。

### 1b. 確認這台機器有沒有 clone 過
```powershell
Test-Path "$env:USERPROFILE\Documents\mac-openclaw-workflows"
```

**如果回傳 True（資料夾已存在）：**
```powershell
cd "$env:USERPROFILE\Documents\mac-openclaw-workflows"
git pull origin main --quiet
```

**如果回傳 False（第一次接這個 repo，需要一次性認證）：**
教練會親口告訴你一組一次性授權碼（GitHub token），**只需要輸入這一次**，之後 git 會自動記住不用再問：
```powershell
cd "$env:USERPROFILE\Documents"
git clone https://github.com/Coach1973/mac-openclaw-workflows.git
```
執行後如果跳出 Username/Password 提示：
- Username 填：`Coach1973`
- Password 填：**教練現在告訴你的那組授權碼**（不是 GitHub 登入密碼，是一組 `gho_` 開頭的字串）

clone 成功後設定記住認證，之後永遠不用再輸入：
```powershell
cd mac-openclaw-workflows
git config credential.helper store
git pull origin main --quiet
```

pull/clone 完成後，**這封信本身**就在剛拉下來的 repo 裡：
`knowledges/TASK_W03任務修正指示_給佩佩電腦MiniMax_2026-07-08.md`（就是你現在讀的這份）

---

## 📖 第二步：依序讀這四份檔案（都在剛才 pull 下來的 repo 裡）

1. `試金石/試金石_專案與代碼.md` —— 搜尋「案例 W03」，從第 377 行開始讀完整套 SOP
2. `試金石/試金石_案例庫.md` —— 搜尋「案例 30」（Comet 瀏覽器搬家死在把 Application 一起搬走的教訓）
3. `claude-brain/project_line_moved_to_e.md` —— LINE 搬家成功案例，含七步驟驗證法
4. `試金石/試金石_案例庫.md` —— 搜尋「案例 39」（穩定後清理孤兒資料夾）

不要跳過任何一份，也不要自己另外找資料或猜測做法——這四份讀完就有完整答案。

---

## ⚙️ 第三步：執行規則（W03 Phase 1 — 全新機器首次搬移）

對每一個 App，照 W03 寫的 Step 0→8 順序做：

1. 確認 App 正常關閉
2. 判斷「主程式子資料夾」（留 C 槽）vs「資料子資料夾」（搬去外接碟），對照 W03 裡的 App 對照表
3. 捷徑審計（桌面 + 開始選單的 .lnk）
4. Registry 審計（InstallLocation / UninstallString）
5. 環境變數審計
6. 第三方工具衝突檢查
7. **一律用 `robocopy` 搬資料子資料夾**，禁止用 `Move-Item` / `Copy-Item`（會漏檔）
8. 原資料夾改名成 `.stale_backup_YYYYMMDD`，建立 Junction 指向新位置，**立刻打開 App 驗證正常**

**規則（本次修改版）：一個 App 做完、驗證 App 打開正常，就直接接著做下一個 App，不用停下來等教練回應——教練現在看不到訊息。每個 App 的結果記下來，全部做完後一次整理成報告。**

**遇到不確定（陌生 App、對照表沒有、Registry 資訊怪異、看不出主程式/資料怎麼分）→ 跳過這個 App，寫進報告的「待確認清單」，繼續下一個，不要用猜的硬做。**

---

## 🔴 收尾鐵律（沒有例外，即使教練說不用問也不能鬆）

1. 搬完的原資料夾（`.stale_backup_YYYYMMDD`）**7 天觀察期內絕對不能刪**——這是 LINE 4GB 聊天記錄永久遺失換來的教訓
2. **本次任務全程不執行任何刪除動作**（包括 `scripts/delete_guard.ps1` 的 `Safe-Remove`）——就算你判斷「這個一定安全可以刪」也不要做，刪除永遠留給教練醒來親自確認
3. 不要做 W03 Phase 3（清理孤兒資料夾）——那是要等 7 天觀察期過後才能做的事，本次任務只做 Phase 1

---

## 📋 全部做完後：寫一份總結報告，讓教練起床一次看懂

跑完所有能跑的 App（或跑到能力所及）之後，在 repo 裡建立一個報告檔：

`knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md`

內容至少要有：
1. **成功搬移清單**：每個 App 名稱 + 搬了多少 GB + Junction 驗證結果（App 打開正常與否）
2. **待確認清單**：跳過的 App + 為什麼跳過（陌生 App / 判斷不出來 / 對照表沒有）
3. **注意事項**：所有 `.stale_backup_YYYYMMDD` 資料夾的完整路徑清單，提醒教練 7 天內不能刪
4. 一句話總結：搬了幾個 App、共釋放多少 GB

寫完後：
```powershell
git add "knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md"
git commit -m "佩佩電腦W03搬家執行報告（自主完成，等教練醒來確認）"
git push origin main
```

這樣教練睡醒直接讀這份報告就好，不用一步步問你做了什麼。

---

## 🚫 不要做的事

- ❌ 不要再去 `D:\Claude-Data\memory-source\` 找答案，那裡沒有
- ❌ 不要自己發明新做法，四份文件讀完就有標準流程
- ❌ 不要執行任何刪除動作，不管看起來多有把握
- ❌ 不要進入 Phase 3 清理
- ❌ 不要在 7 天觀察期內刪除 `.stale_backup` 資料夾
- ❌ 遇到判斷不出來的 App，不要用猜的硬做——跳過、記錄、繼續下一個

---

*Mac 軍師撰寫，2026-07-08 清晨，供佩佩老師電腦 MiniMax 直接讀取執行。教練已休息，本次任務改為自主跑完 Phase 1（安全可逆的部分），刪除類動作一律留給教練醒來確認。*
