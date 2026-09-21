---
name: feedback-powershell-utf8-bom
description: 在 Windows 寫 .ps1 腳本若含中文字串/路徑比對，必須加 UTF-8 BOM 才能被 PowerShell 正確解析
metadata:
  type: feedback
  originSessionId: 7a00178d-d0f6-42f9-a9b8-06d2af7a07e9
---
寫 .ps1 腳本若內容含中文字串字面值（例如 `-match '紅綠燈'`、`if ($name -in '燈號資料倉庫'...)`），必須讓檔案以 **UTF-8 BOM** 編碼儲存，否則 PowerShell 會用系統 codepage（Big5/cp950）讀字串，導致 parse error 或比對失敗。

**Why:** Windows PowerShell 5.x 沒有 BOM 時預設用 system codepage 讀腳本檔。Write tool 寫出來的是 UTF-8 無 BOM，所以中文字面值會壞掉。

**How to apply:**
1. 用 Write tool 先寫腳本到 `.ps1`
2. 用 bash 加 BOM：`{ printf '\xef\xbb\xbf'; cat input.ps1; } > input_bom.ps1`
3. 執行加了 BOM 的版本

附帶：中文檔名比對若失敗，可改用「不靠中文字元」的判斷邏輯（例如用建立日期年份、檔名 -match 的 ASCII 部分、排除清單），這樣穩定性更高。
