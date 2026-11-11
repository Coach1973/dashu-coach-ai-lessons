---
name: reference_windows_hook_python_path_and_encoding_pitfalls_2026-11-11
description: 聯想(Windows)寫 hook／腳本的三個坑：py 不認 /e/ 路徑、py -I 忽略 PYTHONIOENCODING 中文亂碼、PS 5.1 沒設輸出編碼 hook 整段失效
metadata:
  type: reference
---

2026-11-11 聯想賈維斯體檢時踩到的三個坑（修好的檔：taiwan_time_hook.py、feed_junshi_handoff.ps1、delete_guard_hook.ps1）。

- **Windows 的 py 不認 Git Bash 的 `/e/...` 路徑**：`py -I -c` 或 `py x.py` 讀 `/e/` 會 FileNotFound。Python 裡用 `E:/Claude-Data/...`；bash 的 `/tmp` 也跟 Python 的不是同一個（要寫檔就放倉庫目錄）。
- **`py -I` 會忽略 PYTHONIOENCODING**：輸出中文會 cp950 UnicodeEncodeError。要在程式裡 `sys.stdout.reconfigure(encoding="utf-8")`，hook 也一樣。
- **PowerShell 5.1 hook 沒設 `[Console]::OutputEncoding`**：中文整段變亂碼（`u{1f550}` 這種字面），等於沒生效，而且不報錯。要設 UTF-8，或改用 Python 一支。

**How to apply:** 聯想寫新 hook 先用 `echo '{...}' | py 腳本` 實測輸出是不是正常中文，再接進 settings.json。
