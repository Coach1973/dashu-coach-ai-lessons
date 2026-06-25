---
name: project-d-drive-migration
description: PC5C925ED70E46 搬家到 D 槽完成（2026-06-25）——C 槽一鍵還原不怕了
metadata: 
  node_type: memory
  type: project
  updated: 2026-06-25
  originSessionId: b72dd63d-94ff-4916-93ea-d08b2b41cc0e
---

# C→D 槽搬家完成紀錄（2026-06-25）

## 背景

這台機器（PC5C925ED70E46）有一鍵還原功能，執行後 C 槽清空回原廠。
為保護重要資料，把所有大型或重要資料搬到 D:\Claude-Data，用 Junction 讓 C 槽程式感覺不到差異。

## 已搬到 D:\Claude-Data 的項目

| 項目 | C 槽 Junction 路徑 | D 槽實體位置 | 大小 |
|------|-------------------|-------------|------|
| Claude 共用大腦 | `.claude\projects\C--Users-Administrator--claude\memory` | `mac-openclaw-workflows\claude-brain` | 4 MB |
| LINE | `AppData\Local\LINE` | `LINE-AppData-Local` | 1,378 MB |
| Chrome User Data | `AppData\Local\Google\Chrome\User Data` | `Google-Chrome-UserData` | 5,998 MB |
| GanJing | `AppData\Local\GanJing` | `GanJing` | 1,814 MB |
| Perplexity | `AppData\Local\Perplexity` | `Perplexity` | 2,502 MB |

合計保護：約 **11.7 GB**

## 一鍵還原後重建方法

C 槽還原後，用系統管理員身分執行：
```
powershell -ExecutionPolicy Bypass -File D:\Claude-Data\restore_junctions.ps1
```

腳本在 D:\Claude-Data\restore_junctions.ps1，也備份在 GitHub：
`mac-openclaw-workflows/scripts/restore_junctions.ps1`

## 尚未搬的大型項目

- `Packages`（12 GB）：Windows Store 套件，動了會壞，不移
- `Microsoft`（2 GB）：系統相依，不移
- `Temp`（1.2 GB）：暫存，清掉即可，不必移
- `Google-Chrome`（6.5 GB）：Chrome exe + User Data 的完整複製，
  User Data 已有 junction，這份是冗餘備份，確認 Chrome 正常後可刪

## Why / How to apply

**Why:** 一鍵還原後 C 槽歸零，重要資料必須在 D 槽。
**How to apply:** 下次有人問「這台機器還原後怎麼恢復」→ 跑 restore_junctions.ps1 一鍵搞定。
