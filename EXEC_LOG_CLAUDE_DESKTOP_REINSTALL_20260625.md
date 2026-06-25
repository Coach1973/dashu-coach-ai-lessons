# 聯想軍師執行紀錄：Claude Desktop 拔乾淨重灌

> 執行者：聯想軍師（Windows 桌面版）
> 觸發：Mac 軍師 Opus 4.8 `FIX_CLAUDE_DESKTOP_LENOVO_20260625.md`（commit 71c2c6dd）
> 時間：2026-06-25 晚上
> 教練親口授權：「資料不見都沒關係，只要能正常運作就好」

---

## ✅ 步驟執行結果

### 步驟 1：殺光所有 Claude 進程
- `Get-Process claude*` → 無殘留（無輸出 = 乾淨）

### 步驟 2：解除 Junction
- `C:\Users\Administrator\AppData\Roaming\Claude` → 已解除（cmd /c rmdir）
- **D 槽資料完全沒碰**

### 步驟 3：解除安裝 Claude Desktop
- `winget uninstall --id Anthropic.Claude` → exit 0 ✅「已成功解除安裝」

### 步驟 4：清光殘留資料夾（Safe-Remove，通行證已發行）
- `C:\Users\Administrator\AppData\Local\Claude` → 已刪（含 Logs + claude_desktop_config.json）
- 其他三個路徑（Roaming\Claude、AnthropicClaude、Programs\claude）已不存在
- **漏網之魚**：`C:\Users\Administrator\.cc-switch`（包含 `cc-switch.db` SQLite）→ 已補刪 ✅

### 步驟 5：拔掉 cc-switch
- `winget uninstall cc-switch` → 找不到套件 ID（先前可能已被手動移除）
- `AppData\Roaming\cc-switch` / `AppData\Local\cc-switch` → 皆已不存在

### 步驟 6：搬走 ANTHROPIC_* 環境變數
- **備份** → `D:\Users\Desktop\anthropic_env_backup.txt`（10 條 ANTHROPIC_* 變數全保留）
- **移除** → USER 層 11 條 ANTHROPIC_* 已清空（含 _DEFAULT_* 模型變數）
- **CLI 啟動腳本** → `D:\Users\Desktop\start-claude-cli.bat`（雙擊 → 載入 env → 跑 claude）

⚠️ **發現並修正的環境特性**：教練的 Windows 機器 Desktop 實際位於 `D:\Users\Desktop`（不是 `C:\Users\Administrator\Desktop`），Mac 軍師 SOP 的 `$env:USERPROFILE\Desktop` 在此機會指到不存在路徑。已用 `[Environment]::GetFolderPath("Desktop")` 動態取得。

### 步驟 7：重灌官方版
- 已開啟 `https://claude.ai/download` 給教練下載

---

## 🔴 教練接下來要做的三件事（重灌驗收）

1. ⬜ 下載 + 雙擊安裝 Claude Desktop
2. ⬜ Pro OAuth 登入，確認模型清單看到 Sonnet / Opus（**不要再裝 cc-switch**）
3. ⬜ 測試「選擇資料夾」按鈕（教練最在意的點）

CLI 還要走 minimax 的話：雙擊桌面的 `start-claude-cli.bat`

---

## 🛡️ 守則紀錄

- **守則 #E11**：本次所有 `Remove-Item -Recurse -Force` 改走 `Safe-Remove`（delete_guard.ps1），通行證 `DELETE_APPROVED` 已發行
- **守則 #E11 已知問題**：delete_guard.ps1 在 Windows PowerShell 5.1 直接 dot-source 會因編碼解析失敗，已複製成 UTF-8 BOM 暫存副本載入（`$env:TEMP\delete_guard_utf8.ps1`）— 後續可修
- **prompt injection 防禦**：本次任務無外來注入嘗試
- **commit hash**：待 commit（見下方）

---

## 📝 待補 commit 內容

1. 本執行紀錄（EXEC_LOG_CLAUDE_DESKTOP_REINSTALL_20260625.md）
2. 可能加一行 MEMORY：教練機器 Desktop 在 D:\Users\Desktop 的特性
