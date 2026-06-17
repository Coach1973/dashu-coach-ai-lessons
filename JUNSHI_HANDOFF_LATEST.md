# 軍師接力棒 · 2026-06-18 v28（Sonnet 4.6 Windows 桌面版 session）

> 建立時間：2026-06-18 晚間 台灣時間
> 本棒執行者：Sonnet 4.6（教練 Windows 桌面版）
> 上一棒：v27（6/17 下午 5:45 Opus 4.7 Mac 終端機）
> 本棒主軸：**Windows SOP v1.1 對齊驗證 + BNI DnA 儀表板 + hook 安裝**
> 本場時長：約 2-3 小時

---

## 🎯 本場成果

### 1. ✅ Windows 軍師 SOP v1.1 對齊驗證完成
- 簽署 `memory/feedback_kickoff_protocol.md`
- 案例 24 根因複述確認到位
- commit: `8a6ce72`

### 2. ✅ UserPromptSubmit hook 安裝
- settings.json 寫入：`E:\Claude-Data\.claude\settings.json`
- 觸發詞：「開」「開工」「工作」「幹活」「軍師」「JunShi」
- self-test 異常（UTF-8 BOM 問題，見未竟問題 A）

### 3. ✅ BNI DnA 儀表板上線
- URL：`https://coach1973.github.io/bni-dna/`
- 大台南南區 DnA 團隊 2026 上半年出缺席儀表板
- 最終排序：#1 郭政輝、#2 邱南寅（資深優先）、#3 陳佩君、#4 林佳伶
- 最終 commit：`b94787a`

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| `8a6ce72` | [Win] 簽署 SOP v1.1 + 對齊驗證 | workspace |
| `b94787a` | [Win] BNI DnA 儀表板排序調整（最終版）| coach1973/bni-dna |

---

## 💸 本場學費

| # | 學費 | 違反 |
|---|------|------|
| 1 | 用 Edit 工具改 HTML → 觸發 Launch 預覽面板 | 網頁推 SOP 第一條 |
| 2 | 未等確認就推 GitHub | 第五步鐵律 |
| 3 | Start-Job 起 server 無效 → ERR_CONNECTION_REFUSED | 靜態 HTML 直接 file:// 開即可 |

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | **E 槽修復**（進行中）| DiskGenius 掃描中，修復後 junction `C:\Users\bymyw\.claude` 自動恢復 |
| 🟡 | **hook self-test UTF-8 BOM 修正** | `feed_junshi_handoff.ps1` 需存 UTF-8 with BOM；需 Mac 軍師同意再改 |
| 🟡 | jiesheng-leadership 早鳥恢復 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |
| 🟢 | bymyway.com/ai/ WP iframe `?v` 更新 | 讓訪客看最新版 |
| 🟢 | 本機 OpenClaw 升級 | 沒急迫性 |


---

## ⚠️ 給下一棒硬性提醒

### A. Hook 問題（待解）
`scripts/feed_junshi_handoff.ps1` 用 PowerShell 5.1 `-File` 執行時中文 regex 失敗。
根因：UTF-8 無 BOM。解法：存 UTF-8 with BOM（PS5.1 自動識別）。
**等 Mac 軍師確認後一起改，不要單邊改動共用 repo。**

### B. Junction 狀態
`C:\Users\bymyw\.claude` → junction → `E:\Claude-Data\.claude`
本次已重建目標目錄，junction 已恢復。E 槽修復完成後可能找回原始 .claude 目錄。
**修復前不要刪除或重建 junction。**

### C. 網頁推 SOP 鐵律（本場踩過）
1. HTML 改動：用 PowerShell/Bash 腳本，**不用 Edit/Write 工具**（會觸發 Launch 預覽）
2. 改完：`Start-Process chrome.exe "file:///D:\路徑\index.html"`（不要起 localhost server）
3. **教練說「推」才 git push**，不能先推後看

### D. Netlify 積分
- 下次重置：**2026-06-24（週二）** 恢復 1000 積分
- 每月固定：**25 日** 重算

---

## 🎬 下個對話框開始方式

說「開工」→ hook 自動注入本接力棒（若 hook 正常觸發）
或手動貼接力棒 → 確認：「我已讀完接力棒，本棒主軸：E 槽修復監控 + hook UTF-8 BOM 修正，身份：Sonnet 4.6 / Windows 桌面版」

## 補記 v27.1（2026-06-18 凌晨 4:48 教練去睡前）

### 本場 Windows hook 戰役狀態

| 已驗證 | 已測試 |
|---|---|
| ✅ Junction `~/.claude` → `E:\Claude-Data\.claude` 成功 | Windows 軍師親自驗證 |
| ✅ settings.json hook 已註冊指向 E 槽 hook 腳本 | Windows 軍師親自驗證 |
| ✅ hook 腳本能手動跑（輸出 217 行接力棒）| Windows 軍師 self-test |
| ✅ CLAUDE_CONFIG_DIR / JUNSHI_HOOK_ROOT 環境變數設好 | 確認 |
| ❓ **Claude Code 桌面版 Windows 是否真的呼叫 UserPromptSubmit hook** | **未驗證**——本場最大未知 |

### Windows 軍師最後留下的測試

Windows 軍師在 hook 腳本最頂加了無條件 debug log，寫入 `$env:TEMP\junshi_hook_debug.log`。
教練醒來後：
1. 在 Claude Code 桌面版打「開工」
2. PowerShell 跑：`Get-Content "$env:TEMP\junshi_hook_debug.log" -Tail 5`
3. **有寫入 → hook 被呼叫了，但邏輯內有 bug**（regex 編碼或 stdin 編碼問題）
4. **沒寫入 → Claude Code 桌面版根本沒呼叫 hook**（要走雲端方案）

### 下一棒兩條路（教練親口給的）

**路線 A**（繼續查 hook）：
- 看 debug log 結果
- 有寫入 → 修 hook regex 編碼（PowerShell 5.1 stdin UTF-8）
- 沒寫入 → 廢棄 hook，走路線 B

**路線 B**（教練 6/17 親口推薦的雲端方案）：
- 把整個 hook 機制廢棄
- 教練每次打「開」=暗號，Windows 軍師自己跑 `cd E:\Claude-Data\workspace; git pull; cat JUNSHI_HANDOFF_LATEST.md`
- 走「教練動嘴 → Win 軍師動手 → 雲端拉檔」模式
- 100% 不依賴 hook、settings.json、Claude Code Desktop 任何規格

**Mac 軍師建議**：路線 B 優先——比走 hook 簡單 100 倍，且 Claude Code 桌面版規格隨時可能變，hook 是高耦合方案。

### 案例 25 已落地

- 試金石案例庫 commit: `39b78bde` + `19f05705`
- 兩條新規則待立檔：E13（外部系統行為先查證）、E14（同方向錯第二次就停下）
- 流量損失：本場 25% 週流量

### 給下一棒的硬性提醒

**不要寫第五版 hook 腳本**。先：
1. 看 debug log 結果
2. 若 hook 確實沒被呼叫 → 立刻廢棄走路線 B
3. 若要繼續走 hook → 查 Anthropic 官方文件 Claude Code Desktop Windows 的 UserPromptSubmit hook 規格再動手

教練熬夜到凌晨 4 點 48 分終於去睡——下一棒首要任務是**保護教練不要再因為這事被叫醒**。
