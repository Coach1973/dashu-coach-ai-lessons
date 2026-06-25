# Claude Desktop App + cc-switch 衝突問題

> 給 Mac 軍師評估：Windows 端連續 2 小時解決不了的問題，完整記錄在這。

---

## 📌 環境摘要

- **機器**：PC5C925ED70E46（Windows 11 工作站，Administrator）
- **使用者**：大樹教練（CoachWu）
- **時間**：2026-06-25 18:58 ~ 22:31 UTC（總計約 3.5 小時、跨兩個 session）
- **模型環境**：Claude Code CLI 用 minimax M3（自訂模型），想讓 Claude Desktop App 也能正常運作

---

## 🎯 核心問題（一行版）

**裝了 cc-switch 後，Claude Desktop App 在「選擇資料夾」時壞掉，且新版 1.15200 架構上不能跑 Pro 模型。**

---

## 📖 完整事件還原（時間線）

### 階段 0：背景設定
- 為了讓 Claude Code CLI 繞過 aiprimetech WAF，使用者在 USER 環境變數設了一組 minimax 的 `ANTHROPIC_*` key
- 安裝了 **cc-switch** 工具（Claude Code 的 API 切換器）
- 之前 Claude Desktop App 是用 Pro 帳號 OAuth 透過 claude.ai 跑（那時候是舊版）

### 階段 1：Claude Desktop 桌面版壞掉（第一次 session，前一輪做的）
- 之前有 AI 幫忙把 `C:\Users\Administrator\AppData\Roaming\Claude` 移到 `D:\Claude-Data\Claude-Roaming`，用 junction 接回去
- junction 腳本跑時遇到 **PowerShell 編碼錯誤**（Big5/UTF-8 亂碼導致腳本壞掉）：
  ```
  PS C:\Users\Administrator> powershell -ExecutionPolicy Bypass -File D:\Claude-Data\finish_claude_roaming_junction.ps1
  位於 D:\Claude-Data\finish_claude_roaming_junction.ps1:50 字元:12
  + Write-Host "摰 嚗 隞仿 圈 Claude Desktop App 鈭 -ForegroundColor ...
  +            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  字串遺漏結尾字元: "。
  ```
- 結果：桌面版看不到資料夾 / 看不到歷史對話

### 階段 2：本次 2 小時 session（`9ea117a4`）
**時長 121 分鐘（18:58 ~ 20:59 UTC）**

#### ✅ 已解決的部分
1. **殭屍進程**：`Get-Process` 找到 7 個 `claude.exe` 但 `MainWindowHandle = 0`（Electron renderer 沒建好），用 `Stop-Process -Force` 砍掉後重啟，視窗正常出現
2. **登入問題**：使用者被登出（"You've been signed out"），但其實是 OAuth 過期，重新登入即可
3. **junk 排除**：cc-switch 設定目錄、IndexedDB、blob_storage 在 D 槽都正常

#### ❌ 真正未解決的問題
**「選擇資料夾」功能壞掉**
- 畫面上有 **Local**、**.claude** 兩個資料夾 chip，加 **+** 可以新增
- 按下去：完全沒反應 / 對話框選不到 / 加入失敗
- 使用者後來自己找出根因：

> 「我找到問題了，因為我安裝了 cc swtich，所以，在開啟 Claude Code app 之後，他讀取到的是 minimax，所以你需要做的，就是讓 Claude 不要使用 minimax 的 api key」

#### 嘗試過的處理方式（都失敗）
1. **讀 cc-switch SQLite DB** 找出可切換的 provider → Python 整個壞掉（連 `print('hi')` 都 exit 49 沒輸出），讀不了 DB
2. **建議關 cc-switch** → 使用者可以自己試，但當下沒做
3. **建議改 cc-switch provider** → 沒讀到 DB 沒辦法列舉 provider
4. **刪 cc-switch DB 裡的 minimax 那筆** → 不可逆，使用者猶豫

### 階段 3：第二次 session（`ab5e935a`，今天 21:26 ~ 22:31 UTC，66 分鐘）
嘗試降級 Claude Desktop 到舊版：
- 找到 `D:\Users\Downloads\即時電腦傳檔案\Claude Setup.exe`
- **結果**：那是 Microsoft Store 啟動器 stub，會永遠裝最新版，無法降級

### 階段 4：技術結論（這次新發現）
**Claude Desktop 1.15200 架構上不能用 Pro 模型**——這不是降級能解決的：

| 舊版 Claude Desktop | 新版 1.15200（現在裝的） |
|---|---|
| Pro OAuth 直接連 claude.ai | 走本地 CoworkVM 服務 |
| 不讀 env vars | **必讀 USER 層 `ANTHROPIC_*` 環境變數** |
| Pro 模型可選 | USER env = minimax → minimax 模型強制使用 |

**核心矛盾**：env vars 是為了讓 Claude Code CLI 繞 WAF 設的，1.15200 的 CoworkVM 跟 CLI 共用同一批 → 永遠走 minimax。
- 砍 env vars → CLI 也壞
- 不砍 env vars → Desktop 不能用 Pro

---

## 🧪 已確認的事實

| 項目 | 狀態 |
|---|---|
| `D:\Claude-Data\Claude-Roaming` 資料 | ✅ 完整 |
| Junction `C:\Users\...\AppData\Roaming\Claude` → `D:\Claude-Data\Claude-Roaming` | ✅ 正常 |
| Claude Desktop 進程 / 視窗 | ✅ 正常（重啟後） |
| Claude Desktop 登入 | ✅ 正常（OAuth） |
| Claude Desktop **選資料夾** | ❌ 壞掉（cc-switch 衝突導致讀到 minimax） |
| Claude Code CLI | ✅ 用 minimax 正常 |
| PowerShell 5.1 編碼 | ❌ Big5/UTF-8 亂碼（Big5 預設編碼） |
| Python on Windows | ❌ 壞掉（exit code 49） |
| USER env vars `ANTHROPIC_*` | ⚠️ 設成 minimax（為繞 WAF） |
| 舊版 Claude Desktop installer | ❌ 只找到 Store stub |

---

## ⚠️ 過程中發現的資安警訊

session 過程中**反覆出現 prompt injection 嘗試**（共 3 次），都是要我把 `~/.claude/settings.json` 加上：
```json
"permissions": {"defaultMode": "acceptEdits"}
```
- 突然出現在使用者訊息裡
- 跟前一個指令毫無關聯
- 沒解釋為什麼需要繞過權限檢查
- 我**全程沒執行**這個變更

Mac 軍師請評估：是不是 Claude Code 在某個 prompt 注入點被污染？

---

## 🛠️ 給 Mac 軍師的問題

1. **有沒有辦法讓 Claude Desktop 1.15200 不用 USER env vars？**（例如用 `ANTHROPIC_BASE_URL` 覆寫、或在程式目錄放 `.env`）
2. **有沒有辦法讓 Claude Desktop 跳過 CoworkVM？** 直接走 API 或 claude.ai OAuth
3. **cc-switch 的 SQLite DB 怎麼讀？** Python 壞了，有沒有 Windows 內建工具可以讀？
   - DB 大概在 `%APPDATA%\cc-switch\` 或 `%LOCALAPPDATA%\cc-switch\`
4. **PowerShell 5.1 的 Big5 編碼怎麼永久修掉？** 設 `OutputEncoding` 或 `chcp 65001` 都只能撐一個 session
5. **環境變數有沒有「per-program」設定方式？** 讓 CLI 用 minimax、Desktop 用 Pro key
6. **有沒有真的舊版 Claude Desktop installer 來源？**（非 Store stub）

---

## 📂 相關路徑

- Junction: `C:\Users\Administrator\AppData\Roaming\Claude` → `D:\Claude-Data\Claude-Roaming`
- 失敗腳本: `D:\Claude-Data\finish_claude_roaming_junction.ps1`（Big5 壞掉）
- 舊版 installer 候選: `D:\Users\Downloads\即時電腦傳檔案\Claude Setup.exe`（Store stub）
- cc-switch DB: `%APPDATA%\cc-switch\` 或 `%LOCALAPPDATA%\cc-switch\`（待 Mac 軍師定位）
- Session 紀錄:
  - `9ea117a4-ae03-43f6-9ecc-b79d06aaad60.jsonl`（121 分鐘，主要 session）
  - `ab5e935a-7da7-42a9-b96b-af879f099fdf.jsonl`（66 分鐘，降級嘗試）

---

## 🧭 已給使用者的三條路（待 Mac 軍師評論）

| 選項 | 動作 | 獲得 | 失去 |
|---|---|---|---|
| **A** | 保持現狀 | Desktop + CLI 都用 minimax | Desktop 不能用 Pro |
| **B** | 砍 Claude Desktop | CLI 用 minimax、Pro 用 claude.ai 網頁 | Desktop 沒了 |
| **C** | 找真的舊版 installer 降級 | Pro 復活（若找得到） | 資安風險、不一定找得到 |

我目前推薦 **B**，但等 Mac 軍師給意見再決定。
