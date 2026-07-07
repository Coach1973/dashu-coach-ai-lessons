# 任務：修正 W03 C槽增量搬家執行方向（給佩佩老師電腦 MiniMax 終端機）

> 設計者：Mac 軍師 ｜ 2026-07-08 清晨
> 執行者：佩佩老師電腦 OpenClaw MiniMax
> 起因：你剛才查了 `D:\Claude-Data\memory-source\`，那是別的機制，跟這次任務無關，方向查錯了

---

## 🎯 一句話任務

幫佩佩老師電腦做「C 槽資料增量搬到外接碟」，走 **W03 完整生命週期 SOP**（跟聯想機、ACER 機做過的同一套），一次搬一個 App，搬完一個給教練看過再搬下一個。

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

**規則：一次只做一個 App。一個 App 做完、驗證正常，立刻停下來給教練看，教練確認沒問題才進下一個，不要一次做完全部才回報。**

---

## 🔴 收尾鐵律（沒有例外）

1. 搬完的原資料夾（`.stale_backup_YYYYMMDD`）**7 天觀察期內絕對不能刪**——這是 LINE 4GB 聊天記錄永久遺失換來的教訓
2. 刪除任何超過 100MB 的東西，一律用 `scripts/delete_guard.ps1` 的 `Safe-Remove`，**禁止直接呼叫 `Remove-Item -Recurse -Force`**
3. 每做完一個 App，回報：App 名稱 + 搬了多少 GB + Junction 驗證結果，讓教練看得懂在做什麼

---

## 🚫 不要做的事

- ❌ 不要再去 `D:\Claude-Data\memory-source\` 找答案，那裡沒有
- ❌ 不要自己發明新做法，四份文件讀完就有標準流程
- ❌ 不要一次搬完所有 App 才回報，要一個一個來
- ❌ 不要在 7 天觀察期內刪除 `.stale_backup` 資料夾

---

*Mac 軍師撰寫，2026-07-08 清晨，供佩佩老師電腦 MiniMax 直接讀取執行。*
