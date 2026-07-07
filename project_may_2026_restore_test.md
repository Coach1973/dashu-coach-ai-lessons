---
name: may-2026-restore-test
description: 教練計畫一鍵復原到 2026年5月狀態，測試「主程式在C槽、增量資料在D槽」架構是否能無縫接續
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

## 背景（2026-07-03）

教練要做一個大膽測試：把 C 槽用一鍵還原退回 **2026年5月** 的最乾淨狀態（比目前用的 6月26日還原點更早），驗證「主程式留C槽、增量資料junction到D槽」這套架構，能不能撐過一次很久遠的系統回退。

**教練原話邏輯：** 資料留在 D 槽，就算 C 槽退回多舊的狀態，軟體重裝後只要重新橋接（junction）D 槽資料，讀取到的還是最新資料，不會有資料斷層。

**教練會先做的事：** 用一鍵還原軟體，先把「現在這個最好的狀態」備份一份，當作安全網。如果 5 月測試不 OK，教練會自己復原回來。

Related: [[browser-no-full-junction]], [[ask-before-reversing-unusual-config]], [[acer-post-restore-todo]]

---

## 這次要橋接的 6 套軟體（2026-07-02 ~ 07-03 已完成 C/D 分離）

| # | 軟體 | C 槽（主程式，不動） | C 槽連結點（junction，增量資料） | D 槽正本 |
|---|------|---------------------|--------------------------------|----------|
| 1 | Zoom | `AppData\Roaming\Zoom\bin` | `Zoom\data`, `Zoom\logs`, `Zoom\reports` | `D:\Claude-Data\Zoom-Roaming\{data,logs,reports}` |
| 2 | Chrome | `Local\Google\Chrome\Application` | `Chrome\User Data` | `D:\Claude-Data\Google-Chrome-UserData` |
| 3 | GanJing 乾淨世界 | `AppData\Roaming\Gan Jing Browser`（注意：程式本體在 Roaming，不在 Local！） | `Local\GanJing\User Data` | `D:\Claude-Data\GanJing-Local` |
| 4 | LINE | `Local\LINE\bin` | `LINE\Data`, `LINE\Cache` | `D:\Claude-Data\LINE-Data`, `D:\Claude-Data\LINE-Cache` |
| 5 | Telegram | `Roaming\Telegram Desktop\Telegram.exe`（跟資料同層，只挑 tdata） | `Telegram Desktop\tdata` | `D:\Claude-Data\Telegram-Desktop` |
| 6 | Perplexity (Comet) | `Local\Perplexity\Comet\Application` + `CometUpdater` + `Update` | `Comet\User Data` | `D:\Claude-Data\Perplexity-UserData` |

**2026-07-03 全部驗證過：9 個 junction 全部 `LinkType=Junction`，6 套軟體關閉重開都正常，Windows 事件記錄無當機，D 碟資料有即時讀寫。**

---

## 5 月還原後，下一棒 Claude（不管開在哪台機器）要做的事

### 第一步：先確認這份記憶還在
如果你看得到這份檔案，代表 GitHub 上的記憶同步機制正常，直接照下面步驟做即可。

### 第二步：修復 `~/Documents/mac-openclaw-workflows` 本機路徑（重要，容易漏）
這個路徑是**C 槽上的真實資料夾**，不是 junction，5 月還原後極可能消失或變成 5 月當時的舊版本。開工前**必須先確認**：
```powershell
Test-Path "$env:USERPROFILE\Documents\mac-openclaw-workflows"
```
- 如果不存在：`git clone https://github.com/Coach1973/mac-openclaw-workflows.git "$env:USERPROFILE\Documents\mac-openclaw-workflows"`
- 如果存在但是舊版本：`cd "$env:USERPROFILE\Documents\mac-openclaw-workflows"; git pull origin main`

### 第三步：其餘還原步驟，比照 [[acer-post-restore-todo]]
1. 重建 junction：`powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\restore_junctions_acer.ps1"`（這支腳本已經包含上表全部 6 套軟體的正確 Link/Target，會自動偵測 D 槽正本存在就接回去，不存在就 SKIP）
2. 還原 SSH key：從 `D:\Claude-Data\ssh-backup-acer\`
3. 還原 CLAUDE.md：從 `D:\Claude-Data\ssh-backup-acer\CLAUDE.md.bak`
4. 還原 settings.json（關閉 Yes/No 確認彈窗）：從 `D:\Claude-Data\ssh-backup-acer\settings.json.bak`，還原後**要重啟 Claude Code**
5. **重新安裝這 6 套軟體**（5 月當時可能還沒裝，或版本很舊）：Zoom、Chrome、GanJing、LINE、Telegram、Perplexity(Comet)，都從官網下載安裝即可，不用手動搬資料，裝完直接跑步驟 1 的腳本
6. 拉取最新記憶：`git pull origin main`

### 第四步：跑一次完整驗證（照今天 2026-07-03 的驗證方法）
對上表 9 個 junction 逐一 `Get-Item -Force` 檢查 `Attributes -band ReparsePoint`，確認全部是 Junction；確認 6 套軟體主程式檔案都在 C 槽原地；全部關閉重開一輪，確認進程穩定、Windows 事件記錄無當機、資料檔案有新的寫入時間戳；最後請教練親自打開每一套軟體，肉眼確認聊天記錄/書籤/密碼都還在。

### 如果測試失敗
教練會用他自己另外備份的「現在這個最好的狀態」還原回來，不需要 Claude 介入救援，但如果教練有要求協助，直接照本篇「第二步」的邏輯處理（GitHub 記憶不受影響，只有 C 槽本機路徑要重建）。

---

## 這次測試驗證的核心假設

D 槽資料 + junction 架構，可以让「C 槽被還原到任意舊時間點」這件事，對使用者資料（聊天記錄、瀏覽紀錄、Zoom設定等）完全無感——只要程式重裝、junction 重建，資料連續性就不會斷。這比只依賴「一鍵還原快照本身含有帳密」（教練之前的做法）更穩健，因為 junction 讓資料本身独立於任何一次特定的還原快照之外。
