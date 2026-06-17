# SESSION · 2026-06-18 Windows 桌面版軍師（Sonnet 4.6）

> 建立時間：2026-06-18 晚間（台灣時間）
> 執行者：Windows 桌面版軍師，Claude Sonnet 4.6
> 本場主軸：SOP v1.1 對齊驗證 + BNI DnA 儀表板建立 + hook 安裝

---

## 🎯 本場成果

### 1. ✅ Windows 軍師 SOP v1.1 對齊驗證完成
- 讀完 SOP_windows_mac_kickoff_protocol.md v1.1、IDENTITY_windows_desktop.md、案例 24 剖析
- 簽署 `memory/feedback_kickoff_protocol.md`（案例 24 根因複述 + 三大承諾）
- 補記 `memory/2026-06-17.md`
- commit: `8a6ce72`

### 2. ✅ UserPromptSubmit hook 安裝
- `settings.json` 寫入 `E:\Claude-Data\.claude\settings.json`（junction 目標重建後恢復）
- hook 腳本：`scripts/feed_junshi_handoff.ps1`
- self-test 異常：PowerShell 5.1 UTF-8 無 BOM → 中文 regex 解析失敗（待解，見未竟問題）
- 實際觸發行為待下一場「開工」驗證

### 3. ✅ BNI DnA 儀表板建立並上線 GitHub Pages
- 來源：`D:\Users\Downloads\gemini-code-1781720964657.html`
- repo：`coach1973/bni-dna`（新建）
- URL：`https://coach1973.github.io/bni-dna/`
- 修改項目：
  - `<title>` 改為「大台南南區 DnA 團隊戰情儀表板」
  - `<h1>` 同步改為「大台南南區 DnA 團隊戰情儀表板」
  - 移除 `text-transform: uppercase`（避免 DnA → DNA 強制大寫）
  - 排序調整：郭政輝 #1、邱南寅 #2（資深夥伴優先），陳佩君 #3、林佳伶 #4
- commits：`5644fc7`（初始）→ `96d6bc2`（h1 修正）→ `5e8d9e8`（CSS 修正）→ `b94787a`（排序）

---

## 🔴 本場學費

| # | 問題 | 違反 SOP |
|---|------|---------|
| 1 | 用 Edit/Write 改 HTML → 觸發 Launch 預覽面板 | 網頁推 SOP 第一條鐵律 |
| 2 | 未等教練確認就推上 GitHub | 第五步鐵律「教練說推才推」|
| 3 | 先用 widget 預覽，不是 Chrome | SOP 規定唯一指定 Chrome |
| 4 | Start-Job 起的 Python server 沒真正綁 port → ERR_CONNECTION_REFUSED | Windows 老問題，靜態 HTML 應直接 file:// 開 |

---

## ⚠️ 未竟問題（下一棒接手）

### 問題 A：hook self-test UTF-8 BOM 問題
- 症狀：`feed_junshi_handoff.ps1` 用 `-File` 執行時中文 regex 解析失敗
- 根因：PowerShell 5.1 讀 UTF-8 無 BOM 的 .ps1 時編碼錯誤
- 解法：存成 UTF-8 with BOM（PS5.1 識別）
- 卡點：共用 repo，需 Mac 軍師確認（BOM 不影響 Mac bash 執行 .ps1）
- 優先：中（hook 已安裝，實際觸發待驗證）

### 問題 B：Junction 損壞（案例 24 殘留）
- `C:\Users\bymyw\.claude` → junction → `E:\Claude-Data\.claude`
- E 槽被清空後目標目錄消失 → junction 損壞
- 本次已重建 `E:\Claude-Data\.claude` 讓 junction 恢復
- E 槽修復進行中：若 Disk Genius 找回原 `.claude` 目錄，junction 目標自動恢復
- 優先：低（已暫時修復，等 E 槽回復）

---

## 📊 Netlify 積分狀態（教練 2026-06-18 親口告知）
- 下次重置：**2026-06-24（週二）** 恢復 1000 積分
- 每月週期：**每月 25 日** 重新計算

---

## 🔑 commit hash 憑證

| commit | 內容 | repo |
|--------|------|------|
| `8a6ce72` | [Win] 簽署 SOP v1.1 + 對齊驗證 | workspace (main) |
| `5644fc7` | Add DnA team dashboard | coach1973/bni-dna |
| `96d6bc2` | Fix h1 title: add 大台南南區 | coach1973/bni-dna |
| `5e8d9e8` | [Win] 移除 text-transform: uppercase | coach1973/bni-dna |
| `b94787a` | [Win] 調整排序：郭政輝第一、邱南寅第二 | coach1973/bni-dna |