---
name: reference-windows-file-scan-silent-zero-traps-2026-10-06
description: 聯想(Windows)掃檔「回 0 筆卻不報錯」的三個坑：Get-ChildItem -LiteralPath 配 -Include、bash 寫 ps1 的反斜線被吞、無 BOM 的 .ps1 中文讀壞；以及 find 掃 C:\Users 會因 OneDrive 逾時。找檔結論是「沒有」之前先看這篇
metadata:
  node_type: memory
  type: reference
  originSessionId: 2654e25c-37e5-4fd3-b1c8-0db4eb14b573
  modified: 2026-10-05T19:01:13.525Z
---

2026-10-06 找 Zoom 錄影時，同一個「0 筆」假結果出現三次，差點回報「C 槽沒有別的檔案」：

1. `Get-ChildItem -LiteralPath <路徑> -Recurse -Include *.m4a`：**-Include 搭 -LiteralPath 不生效，回 0 筆、不報錯**。改用 `-Path <路徑> -Recurse -File -Filter <單一樣式>`（-Filter 一次只能一種樣式，要掃多種就迴圈）。
2. 從 bash 用 heredoc 寫 `.ps1`，字串裡的 `\\` 會被吞成 `\`，正規表示式 `'\\(AppData|...)\\'` 就變成「太多 ) 符號」錯誤，整段 try 吞掉、結果也是 0 筆。排除路徑改用 `-like '*\AppData\*'` 萬用字元，不用正規表示式。
3. `.ps1` 檔裡有中文字面值又**沒有 BOM**，PowerShell 5.1 以 cp950 讀會整個解析失敗（什麼都沒執行）；訊息改英文／ASCII，或存成帶 BOM 的 UTF-8（python 寫檔用 `utf-8-sig`）。
4. `find /c/Users ...` 會穿過 OneDrive 與 AppData 掃到逾時（`timeout` 砍掉後只印出空白，看起來像「沒有」）。要找檔：先看 Zoom／下載等已知位置，再用上面第 1 點的寫法，並用「已知存在的檔案」先驗證掃描寫法抓得到（本次用 `GMT*Recording*` 在 D 槽抓到 73 筆才信 0 筆的結論）。

**How to apply:** 任何「掃全機找某類檔案」要下「沒有」的結論前，先拿一個已知存在的目標驗證掃描寫法；結果是 0 時先懷疑掃描本身。相關：[[reference_lenovo_zoom_recordings_junction_to_d_2026-10-06]]、[[reference_lenovo_system_image_backups_2026-10-03]]（同樣的 ps1 無 BOM 小坑）。
