---
name: reference_gitbash_powershell_dollar_underscore_quoting_2026-09-04
description: Windows機器用Bash工具(Git Bash)呼叫PowerShell -Command時若用雙引號包整段指令，Bash會把PowerShell的$_管線變數當成自己的參數展開吃掉導致語法錯誤
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1583342f-6c6a-4f3a-85c0-5749ee197c32
  modified: 2026-09-04T05:51:15.075Z
---

`powershell -NoProfile -Command "... $_.Property ..."` 在Windows Claude Code的Bash工具（跑Git Bash / POSIX sh）下，`$_` 會被Git Bash自己的shell語法解讀（bash也有`$_`代表上一指令最後一個參數）並展開/清空，導致傳給PowerShell的字串壞掉，出現`unsetenv.XXX`之類的亂碼或`MissingEndParenthesisInMethodCall`語法錯誤——錯誤訊息看起來像PowerShell語法壞掉，其實是shell層級的引號問題。

**修法**：整段PowerShell指令改用**單引號**包裹外層：
```
powershell -NoProfile -Command 'Get-Process | Select-Object @{n="Name";e={$_.ProcessName}}'
```
單引號讓Git Bash完全不對內容做展開，`$_`原封不動傳給PowerShell。PowerShell內部若需要字串常值（如雜湊表鍵名），改用雙引號，兩層引號不衝突。

**Why**：診斷聯想Windows記憶體洩漏（見[[project_lenovo_nonpaged_pool_leak_2026-09-04]]）時，前3次PowerShell查詢指令因此全部失敗噴錯，浪費一輪來回才發現是shell層級問題不是PowerShell語法錯誤。

**How to apply**：之後在這台機器（或任何Git Bash環境）用Bash工具組PowerShell指令，只要用到`$_`（管線物件）語法，一律用單引號包裹整個`-Command`參數。
