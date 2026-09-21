---
name: project-downloads-location
description: 使用者已把 Windows 下載資料夾重導向到 D 槽，並建立了分類資料夾結構
metadata:
  type: project
  originSessionId: 7a00178d-d0f6-42f9-a9b8-06d2af7a07e9
---
**實際下載位置：** `D:\Users\Downloads`（不是預設的 `C:\Users\Administrator\Downloads`，預設那個是空的）

**註冊表登錄：** `HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\{374DE290-123F-4565-9164-39C4925E467B}` = `D:\Users\Downloads`

**Downloads 內現有分類結構（2026/5/13 建立）：**
- `燈號資料倉庫` — 所有含「紅綠燈」「燈號」字眼的檔案（不論副檔名）
- `資料收集` — 錄音檔（.aac/.m4a/.mp3）+ 其他既有子資料夾
- `PPT`、`PDF`、`Excel`、`Word`、`圖片`、`軟體安裝` — 依副檔名分類
- `待刪除` — 雜檔（.txt/.log/.ini/.ps1/.conf/.xml）
- `即時電腦傳檔案`、`會議音樂`、`123` — 既有資料夾，不動

**How to apply:** 處理使用者下載相關需求時，**用 `D:\Users\Downloads`**，不要去掃 C 槽預設路徑。新檔案分類時遵守上述規則（紅綠燈優先於副檔名）。
