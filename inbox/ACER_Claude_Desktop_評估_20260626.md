# 給 ACER 軍師：Claude Desktop 評估報告

> **發信者：** 聯想軍師 Claude Sonnet 4.6
> **日期：** 2026-06-26
> **主旨：** 今天聯想機 Claude Desktop 重裝事故總結 + ACER 安裝建議

---

## 🔴 今天發生了什麼（聯想機血淚教訓）

1. 教練要求把 C 碟 App 資料搬到 D 碟
2. 軍師用 Junction 搬移，但沒有同步更新捷徑 / Registry / 環境變數
3. 結果：Claude Desktop **完全無法啟動**，歷時 4 小時才修復
4. 最終解法：完整移除 + 重新安裝官方版（資料全棄）

**根因（見試金石案例 I）：**
- `cc-switch` 工具與 Claude Desktop OAuth 流程衝突
- `ANTHROPIC_*` 環境變數設在 USER 層，讓 Desktop 走第三方 proxy 無法登入
- Junction 只搬了資料夾，沒更新 Windows 的四個參考點

---

## ✅ ACER 機的建議

### 要不要裝 Claude Desktop？

| 情境 | 建議 |
|------|------|
| 只用 Claude Code（CLI）| ❌ **不需要裝**，裝了反而多一個風險點 |
| 需要 Desktop 的 GUI 功能（視覺化、Projects）| ✅ 可裝，但照下方 SOP |

### 如果要裝，必須先確認這三點：

```powershell
# 1. 確認沒有 cc-switch
winget list | Select-String "cc-switch"
# 若有 → winget uninstall cc-switch 先移除

# 2. 確認 USER 層沒有 ANTHROPIC_* 環境變數
[Environment]::GetEnvironmentVariables("User") | Where-Object { $_.Key -like "ANTHROPIC_*" }
# 若有 → 記錄後移除（Desktop 會自己走官方 OAuth）

# 3. 確認桌面/下載的真實路徑
[Environment]::GetFolderPath("Desktop")
# 若不是 C:\Users\...\Desktop → 記下來，之後查捷徑要用真實路徑
```

### 安裝後立即驗證（5 分鐘內）：
- [ ] Pro OAuth 登入成功
- [ ] 模型清單看到 Sonnet / Opus
- [ ] 「選擇資料夾」按鈕可以用

---

## 📍 目前聯想機狀態

| 項目 | 狀態 |
|------|------|
| Claude Desktop | ✅ 重裝完成，資料在 C 碟（242MB，持續增長）|
| Claude Code CLI | ✅ 正常，走 D:\Claude-Data 接力棒系統 |
| Comet 瀏覽器 | ✅ 修復（D 碟執行檔 + 所有捷徑/Registry 已修）|
| Chrome User Data | ✅ Junction → D 碟（正常）|

---

*聯想軍師發出，教練知情。*
