---
name: feedback-no-scripts-in-temp
description: 在執行系統清理任務時，把 .ps1 腳本寫到 %TEMP% 會被自己清掉而中斷執行
metadata:
  type: feedback
  originSessionId: 7a00178d-d0f6-42f9-a9b8-06d2af7a07e9
---
清理 Temp 暫存的腳本若放在 `%TEMP%` 裡，腳本執行到清理該資料夾時會把**自己**刪掉，導致中斷或後續驗證失敗。

**Why:** 實際踩過。`C:\Users\Administrator\AppData\Local\Temp\clean_A.ps1` 在執行 `Clean-Folder $env:TEMP` 時把自己也刪了，輸出檔也消失，無法驗證結果。

**How to apply:** 把清理用的腳本放到穩定位置，例如 `C:\Users\Administrator\.claude_cleanup\`，不要放 %TEMP% 或被清理目標路徑下。

## 相關教訓：清整個 %TEMP% 會動到正在跑的程式自己的暫存檔（2026-09-21）

清 `%TEMP%` 底下**全部**項目時，Claude Code session 自己的暫存輸出檔（`%TEMP%\claude\<project>\...\tasks\*.output`）也會被刪掉——因為它是一般檔案，Windows 不會像鎖檔案控制代碼那樣阻擋 `Remove-Item`。結果是那個指令當下的畫面輸出讀不到（`ENOENT`），但 session 本身不受影響，之後的指令照常運作。

**Why:** 2026-09-21 幫教練清 Temp 時，`Remove-Item` 遍歷 `$env:TEMP` 底下所有項目、逐一刪除，剛好刪到自己這個 session 正在寫入的 output 檔。

**How to apply:** 清 `%TEMP%` 前，用 `Get-ChildItem \$env:TEMP` 排除掉 `claude`（Claude Code 自己的暫存目錄）等「目前有程式在跑」的子資料夾，只清散落的舊暫存檔；或是接受少數項目會顯示「跳過（使用中）」而不是硬清全部，這是正常現象不是失敗。
