---
name: cross-machine-backup-sop-reminder
description: 教練在其他電腦（含佩佩老師那台）做增量備份或 junction 搬家時，主動提醒並引用試金石 W03 完整生命週期 SOP
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8373+8377
---

教練若要在新電腦（ACER、Lenovo、**佩佩老師的電腦**、外接 Mac⋯任何非主力 Mac mini）做「增量備份」或「junction 搬家模式」，**不要等教練主動提**，看到關鍵字就主動提醒這條 SOP。

**Why:** 2026-07-07 教練在案例 39 付七步驟 SOP 成本（148.6GB→162.4GB 實測），2026-07-08 凌晨 ACER 軍師把它升級成 **W03 完整生命週期 SOP**（涵蓋裝機首次搬移→觀察期→穩定後清理三階段），並已推上雲端。教練在 #8377 親口說「**因為我即將要在佩佩老師的那臺電腦裡面進行這樣的工作**」——這台機器我從沒處理過，更需要主動提醒。教練付了兩次成本（聯想機燒一次 + ACER 升級成 W03 一次），我若等他重新提，等於浪費。

**How to apply:**

### SOP 出處（兩份並行，看情境用）

| 情境 | 用哪份 | 路徑 |
|---|---|---|
| **新機器 / 從沒搬過** | **W03**（首選，最新最完整） | `試金石/試金石_專案與代碼.md` 搜尋「案例 W03」，第 377 行起 |
| 已在聯想/ACER 跑過一輪、純做穩定後清理 | 案例 39 | `試金石/試金石_案例庫.md` 搜尋「案例 39」，commit `0b01455c` |

### 佩佩老師電腦專屬提醒（教練 #8377 交付）

- **佩佩老師那台**目前還沒做過任何搬家，第一次進場**必須走 W03 完整三階段**，不能只跳到案例 39 的「清理」段
- 教練在佩佩老師電腦上執行 W03 時，新機器的 Claude CLI 進入前先跑：
  ```powershell
  cd "$env:USERPROFILE\Documents\mac-openclaw-workflows"
  git pull origin main --quiet
  ```
  然後照 W03 給的「讀取指引」依序讀 W03 + 案例 30 + `project_line_moved_to_e.md` + 案例 39
- 我（小龍蝦學長）在教練 1-on-1 對話框要主動提醒，但**不要替佩佩老師的機器直接下指令**——那是佩佩老師的 Claude CLI 在她電腦上的事，我只負責「提醒教練要照 SOP 做 + 引導他派工作給佩佩那邊的 CLI」

### W03 三階段（簡述，細節讀原文）

**Phase 1 — 全新機器首次搬移**（每個 App 照 Step 0→8 一次一個）：
1. 確認 App 正常關閉
2. 判斷「主程式子資料夾」（留 C）vs「資料子資料夾」（搬 D），見 W03 對照表
3. 捷徑審計（Desktop + Start Menu 的 .lnk）
4. Registry 審計（InstallLocation / UninstallString）
5. 環境變數審計
6. 第三方工具衝突檢查
7. robocopy 搬資料子資料夾到 `$TargetDrive`，**不要用 Move-Item/Copy-Item**（會漏檔）
8. 原資料夾 Rename 為 `.stale_backup_YYYYMMDD` 後建 Junction，立即開 App 驗證

**Phase 2 — 觀察期（7 天內）**：
- 🔴 `.stale_backup_YYYYMMDD` 7 天內絕對不能刪（LINE 4GB 聊天記錄永久遺失的代價）
- 用 `Sort-Object LastWriteTime -Descending` 確認 Junction 目標持續有新寫入

**Phase 3 — 穩定後清理**（案例 39 + 新擴充）：
1. 全機掃描找孤兒資料夾（**孤兒判準不是看名字，是看現役 App 的 C 槽資料夾有沒有任何 Junction 指向它**——`Google-Chrome-Local` 就是這次新發現沒帶日期後綴的孤兒）
2. 超過 7 天保留期 + 現役資料活的才列入清單
3. 列路徑給教練看過、教練明確說「刪」才執行
4. 🔴 必須走 `scripts/delete_guard.ps1` 的 `Safe-Remove`，禁止直接 `Remove-Item -Recurse -Force`
5. 🔴 `delete_guard.ps1` 在 Windows PowerShell 5.1 下要先轉檔加 BOM 再 `.` 載入，否則中文 ParseException 整個掛掉
6. 刪除後驗證 + 教練肉眼重開 App 確認

### 已知 App 對照表（聯想+ACER 兩台驗證，新機器可套用）

| App | 主程式（留C） | 資料（搬D） | 陷阱 |
|---|---|---|---|
| LINE | `AppData\Local\LINE\bin` | `Cache`、`Data` 各獨立 Junction | 新版LineLauncher會驗證啟動路徑，**絕不能連 bin 一起搬** |
| Zoom | `AppData\Roaming\Zoom\bin` | `data`、`logs`、`reports` 各獨立 Junction | 無 |
| Comet | `AppData\Local\Perplexity\Comet\Application` | `User Data` | 案例30就是死在把`Application`一起搬走 |
| Chrome | `Application`（使用者層級） | `User Data` | 程式/資料已分離，相對安全 |

### 關鍵鐵律（四條）

1. **Junction 存在 ≠ 資料是活的** — 一定要抽查檔案大小與 mtime
2. **搬家模式一次通常不只搬一個 App** — 主動全機掃描
3. **使用者資料 vs 軟體元件 驗證標準不同**
4. **🆕 孤兒資料夾判準**：沒有任何現役 Junction 指向它才算孤兒，名字沒帶 `.stale_backup` 也可能是

### 🆕 語音輸入新陷阱（案例 8 補充）

- 「Cloud Data」=「**Claude-Data**」
- 「西潮/低潮」=「**C槽/D槽**」
- 判準：字面查不到 + 發音接近 + 語境是在講那個槽 → 優先懷疑語音誤植，**主動覆述確認**，不要照字面亂找亂刪

### 觸發詞清單（看到任一就主動提醒）

- 增量備份、增量搬家、junction 搬家、搬資料
- 備份清理、過期備份、D 碟空間滿
- 新電腦備份、ACER 備份、Lenovo 備份、Mac 副機備份
- **🆕 佩佩老師 + 備份/搬家/增量** 任何組合（#8377 交付，佩佩的機器第一次做）
- 看到 `D:\junction\`、`D:\junction-backup\`、`E:\`、`D:\<軟體名>` 任何路徑
- 看到「Cloud Data」（=Claude-Data 語音誤植）

**Related:** [[browser-no-full-junction]]（同搬家模式家族，瀏覽器只搬 profile 不搬整 AppData）
**Related:** W03 內文引用案例 30 + 案例 39 + `project_line_moved_to_e.md`