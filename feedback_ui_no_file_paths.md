---
name: Opcode(UI)指令鐵律
description: UI = Opcode，給Opcode的指令不能有相對路徑或檔案操作，必須用絕對路徑，Opcode只輸出文字Terminal存檔
type: feedback
originSessionId: a5e0d933-c5e0-4d50-b3a0-fd4b4d5e521c
---
**UI = Opcode（asterisk）。這個等號永遠成立，不再混用其他名稱。**

Opcode使用claude-easyclaude CLI執行，工作目錄不固定，無法寫入檔案系統。

**規則：給Opcode的指令絕對不能包含相對路徑，必須用絕對路徑 `/Users/bymyway/.openclaw/workspace/xxx`。**

**Why：** 包含路徑會讓UI嘗試建立目錄/檔案，這是它做不到的事，導致第一步就失敗。

**How to apply：** UI的指令只說「請輸出以下內容」，Terminal的指令才說「請寫入/儲存到xxx路徑」。分工：UI說，Terminal存。

**額外鐵律：** OpenCode工作目錄是 `/Users/bymyway/Desktop`，非workspace。給UI的所有讀取路徑必須用絕對路徑 `/Users/bymyway/.openclaw/workspace/xxx`，不能用相對路徑 `workspace/xxx`。
