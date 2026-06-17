# Windows 軍師對齊驗證 Checklist · SOP v1.1

> 適用對象：Windows 桌面版 Claude Code 軍師
> 觸發暗號：教練說「**對齊驗證**」或「**簽署 v1.1**」→ 你（Windows 軍師）讀本檔 → 照七步驟一氣呵成執行 → commit `[Win]` ack → push → 回報。
> 設立時間：2026-06-17 下午（Mac 軍師 Opus 4.7 寫定，commit fb357e5b 之後）

---

## 為什麼有這份 Checklist

教練要對齊驗證，但**不貼整份步驟給你**才對——那違反「動嘴就好」。
你只要看到暗號，自己照本檔執行，全程不用教練動手貼指令。

---

## 七步驟（請逐項勾選回報）

### ✅ 步驟 1：裝開工 hook（之後每場「開」「開工」自動觸發接力棒注入）

```powershell
cd $env:USERPROFILE\.openclaw\workspace
git pull
powershell -ExecutionPolicy Bypass -File scripts\install_windows_hook.ps1
```

回報：self-test 第一行輸出（應該包含「軍師接力棒」）。

---

### ✅ 步驟 2：讀身份卡（**本場 + 每場必讀**）

讀 `knowledges\IDENTITY_windows_desktop.md`，理解：

- **你是 Windows 桌面版 GUI**（不是 CLI 終端機）
- **工具能力跟 Mac CLI 完全同等**（Bash/Read/Edit/Write 全有）
- **路徑對應**：`/tmp/` → `$env:TEMP`；`~` → `$env:USERPROFILE`
- **指令對應**：`open -a "Google Chrome"` → `Start-Process chrome.exe`
- **commit 前綴**：`[Win]`（區分 Mac 軍師的 `[Mac]`）
- **稱呼教練**：大樹教練

回報：身份卡看完，三件最容易搞錯的事是哪三件？

---

### ✅ 步驟 3：驗證 `delete_guard.ps1` 的 `Safe-Remove` 函式可用

```powershell
. "$env:USERPROFILE\.openclaw\workspace\scripts\delete_guard.ps1"
Get-Command Safe-Remove
```

回報：`Safe-Remove` 是否有定義？（應顯示 `Function   Safe-Remove`）

---

### ✅ 步驟 4：寫簽署檔 `memory\feedback_kickoff_protocol.md`

內容包含五段（依此順序）：

1. **本人**（Windows 桌面版軍師，模型版本）已讀完：
   - `knowledges\SOP_windows_mac_kickoff_protocol.md` **v1.1**
   - `knowledges\IDENTITY_windows_desktop.md`
   - 試金石案例 24 完整剖析（636 GB E 槽蒸發）
2. **承諾遵守**：
   - commit 前綴 `[Win]`
   - 任何刪除走 `Safe-Remove`，禁止直接 `Remove-Item -Recurse -Force`
   - 超過 1 GB 任何身份不得自主刪除
   - Bash 呼叫 PowerShell 絕不用 `$variable` 傳路徑（案例 24 根因）
3. **案例 24 根因複述**（一句話證明真懂了）
4. **簽署時間**：台灣時區 YYYY-MM-DD HH:MM
5. **簽署人**：Windows 桌面版軍師 + 模型版本（例：Opus 4.7）

---

### ✅ 步驟 5：補記今日 memory（**不覆蓋既有段落**）

在 `memory\2026-06-17.md` 末尾**附加**（不要動前面段落）：

```markdown
### HH:MM Windows 軍師補記
- 已完成 SOP v1.1 對齊驗證（步驟 1-7）
- hook 安裝：通過 / 異常（貼 self-test 第一行）
- Safe-Remove：可用 / 不可用
- 案例 24 認知：跨 shell 跳脫 `$temp` 變空字串 → `Remove-Item -Recurse -Force` 從 `E:\` 遞迴刪
- 下次「開」/「開工」會自動觸發 hook 注入接力棒 + 身份卡
```

---

### ✅ 步驟 6：commit + push

```powershell
git add memory\feedback_kickoff_protocol.md memory\2026-06-17.md
git commit -m "[Win] 簽署 SOP v1.1 + 對齊驗證完成 + 案例 24 認知到位"
git push origin main
```

---

### ✅ 步驟 7：回教練（**只回三件事**，不要長篇大論）

```
[Win] 對齊驗證完成
- commit hash 前 7 碼：xxxxxxx
- hook self-test：通過 / 異常（細節）
- Safe-Remove：可用 / 不可用
```

---

## 卡住怎麼辦

| 卡點 | 處理 |
|------|------|
| `git pull` 衝突 | **不要 force**——直接回報教練，Mac 軍師處理 |
| `install_windows_hook.ps1` 報錯 | 貼完整錯誤訊息回報 |
| `Safe-Remove` 找不到 | 確認 `scripts\delete_guard.ps1` 存在；`Get-Content` 看內容是否完整 |
| Git push 被拒（權限）| 通常是 token 過期，回報教練 |
| 任何 1 GB 以上的刪除衝動 | **立刻停**，回報教練親口授權才能動 |

---

> 這份 Checklist 由 Mac 軍師（Opus 4.7）2026-06-17 晚上 7:15 寫定。
> 未來「對齊驗證」「簽署 vX.Y」一律走同樣模式——教練一個暗號，Windows 軍師讀檔自走，全程不用搬運工。
