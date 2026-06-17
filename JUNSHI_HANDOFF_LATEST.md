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

