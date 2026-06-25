# 收工摘要：2026-06-26 聯想機大災難與全面修復

> 日期：2026-06-26
> 機器：聯想 Windows（本機）
> 軍師：Claude Sonnet 4.6
> 工時：約 6 小時

---

## 📋 今日任務清單

| # | 任務 | 狀態 |
|---|------|------|
| 1 | 三機共用大腦 Junction 接上 | ✅ |
| 2 | 「開工」加入 CLAUDE.md 觸發詞 | ✅ |
| 3 | 載入 ai-go 特助心法（21 守則）為工作標準 | ✅ |
| 4 | 修復 Comet 瀏覽器（捷徑 + 圖示 + Registry）| ✅ |
| 5 | 試金石：C→D 搬移大災難永久記錄 | ✅ |
| 6 | 評估 C→D 搬移目標是否實現 | ✅ |
| 7 | 清除 10GB D:\Claude-Data\Claude-Roaming 廢料 | ✅ |
| 8 | 提煉 Cowork 2026-03-02 C槽瘦身 session | ✅ |
| 9 | 寫 ACER inbox 兩封信（Desktop 評估 + Hook 指引）| ✅ |
| 10 | 查高鐵取票代號 | ✅ **00379290** |
| 11 | Claude Desktop 資料備份（一鍵備份）| ⏸ 中斷，待下次 |
| 12 | Claude Desktop 資料 Junction 到 D 碟 | ⏸ 待下次 |

---

## 🔑 今日最重要的結論

### 1. 試金石案例 I — C→D 搬移大災難（已寫入永久庫）

Junction 只做了一件事：讓路徑透明轉向。但 Windows 還有四個參考點沒更新：
- 桌面捷徑（.lnk）
- Registry（InstallLocation / UninstallString）
- 環境變數（USER 層）
- 第三方工具（cc-switch）

**鐵律：搬 AppData 前必先執行七步驟 SOP（見試金石_專案與代碼.md W01）**

### 2. C→D 搬移目標實際達成情況

| 項目 | 結果 |
|------|------|
| Chrome User Data | ✅ Junction 成功，資料在 D 碟 |
| Comet 瀏覽器 | ⚠️ exe 在 D，但 C 碟舊拷貝 757MB 未清 |
| Claude Desktop | ❌ 重裝後資料回到 C 碟（242MB 持續增長）|

### 3. 高鐵取票代號

**00379290**（嘉義→台北，26 Jun 17:08，664 次，5車廂 16B/17B）

---

## ⏸ 下次開工待辦

1. **Claude Desktop 一鍵備份** — 用 Bash `cp -r` 代替 PowerShell（長路徑問題）
   ```bash
   cp -r "/c/Users/Administrator/AppData/Roaming/Claude" \
         "/d/Claude-Data/backup_before_junction_$(date +%Y%m%d-%H%M%S)/"
   ```

2. **確認備份大小**（應約 242MB）

3. **Junction Claude Desktop 到 D 碟**
   - 移動到 `D:\Claude-Data\Claude-Roaming`
   - 建 Junction：`cmd /c mklink /J "C:\...\AppData\Roaming\Claude" "D:\Claude-Data\Claude-Roaming"`
   - 驗證 Claude Desktop 正常啟動

---

## 🛡️ 安全提示（寫給下次的軍師）

- 備份時用 Bash 的 `cp -r`，不要用 PowerShell `Copy-Item`（長路徑會炸）
- Junction 操作前**必先**備份，教練已確認「出差錯可以救回來」最重要
- Claude Desktop 目前在 C 碟，大小 242MB，每次對話會增長

---

*2026-06-26 聯想軍師收工，教練今晚搭 664 次高鐵回台北。*
