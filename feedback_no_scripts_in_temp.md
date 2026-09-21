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
