# 給 ACER 軍師：Hook 設定指引

> **發信者：** 聯想軍師 Claude Sonnet 4.6
> **日期：** 2026-06-26
> **主旨：** ACER 機 Claude Code Hook 一鍵安裝步驟

---

## 🎯 目標

讓 ACER 的 Claude Code 具備：
1. **session 結束自動推送** — 對話結束後自動備份 + push 到 GitHub
2. **記憶同步** — 每次開工自動 git pull 取得最新接力棒

---

## 📋 前置確認（先跑，再裝）

```powershell
# 1. 確認 repo 已 clone 到 D 碟
Test-Path "D:\Claude-Data\workspace\mac-openclaw-workflows"
# → True 才繼續；False → 先執行 bootstrap_acer_laptop.ps1

# 2. 確認 Claude Code 已安裝
claude --version

# 3. 確認 git 設定正確
cd D:\Claude-Data\workspace\mac-openclaw-workflows
git remote -v
# 應看到 origin → https://github.com/Coach1973/mac-openclaw-workflows.git
```

---

## ⚡ 一鍵安裝（三個 Hook）

### Hook 1：Windows Session 結束自動推送

```powershell
# 安裝
powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\workspace\mac-openclaw-workflows\scripts\install_windows_session_end_hook.ps1"

# 驗證
Get-Content "$env:USERPROFILE\.claude\settings.json" | Select-String "session"
```

### Hook 2：Windows 主要 Hook（記憶同步 + 開工流程）

```powershell
# 安裝
powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\workspace\mac-openclaw-workflows\scripts\install_windows_hook.ps1"

# 驗證觸發
# 開新 Claude Code session，送任何一句話，應在 context 看到接力棒內容
```

### Hook 3：若以上失敗，用診斷修復版

```powershell
powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\workspace\mac-openclaw-workflows\scripts\install_or_restore_windows_hook.ps1"
```

---

## ✅ 安裝後驗證清單

```powershell
# 確認 settings.json 有 hooks 區段
$s = Get-Content "$env:USERPROFILE\.claude\settings.json" | ConvertFrom-Json
$s.hooks | Format-List

# 應看到至少兩個 hook（UserPromptSubmit 或 Stop）
```

| 驗證項目 | 通過條件 |
|---------|---------|
| settings.json 有 hooks 區段 | `$s.hooks` 不是空的 |
| 開新 session 有讀到接力棒 | 回應第一句話時有提到上次進度 |
| session 結束有自動 push | `git log --oneline -3` 看到新 commit |

---

## 🚫 ACER 機特別注意事項

1. **所有 Claude 資料必須在 D 碟**（C 碟有一鍵還原風險）
2. **workspace 路徑：** `D:\Claude-Data\workspace\mac-openclaw-workflows`
3. **不要裝 cc-switch**（見 Claude Desktop 評估信）
4. **桌面真實路徑先確認：** `[Environment]::GetFolderPath("Desktop")`（可能不是 C:\Users\...）

---

## 🔗 相關檔案（git pull 後在 repo 裡找）

| 檔案 | 用途 |
|------|------|
| `scripts/install_windows_hook.ps1` | 主要 hook 安裝腳本 |
| `scripts/install_windows_session_end_hook.ps1` | session 結束推送 hook |
| `scripts/diagnose_and_fix_windows_hook.ps1` | 診斷 + 修復工具 |
| `scripts/bootstrap_acer_laptop.ps1` | ACER 一鍵初始化（若尚未建立據點）|
| `skills/self-improving-agent/references/hooks-setup.md` | Hook 原理說明 |

---

*讀完執行，有問題回報教練。*
*聯想軍師發出，2026-06-26。*
