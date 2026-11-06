---
name: reference-amber-nas-delete-goes-to-smbrecyclebin
description: Amber(NAS) 刪檔會先進 @SmbRecyclebin，空間要再從回收筒刪一次才回來；時光機 sparsebundle 比實際資料多佔約108G，唯一解是刪整份重做
metadata:
  node_type: memory
  type: reference
  originSessionId: 48b6c4d9-725d-4e13-82e4-a814a44af93b
  modified: 2026-11-06T09:25:56.156Z
---

2026-11-06 Amber 清理：`~/amber-mnt` 底下 rm 檔案，NAS 會把它搬進 `~/amber-mnt/@SmbRecyclebin/<原路徑>`，`df` 空間不變；要再 `rm -rf` 回收筒裡那份才真的釋放（>1GB 照 N6 五道閘門）。

時光機 APFS 實際只用 135G，但 sparsebundle 的 bands 佔 244G，`hdiutil compact` 對 APFS 映像幾乎無效（只回收 161MB）。唯一回收方式＝先 `hdiutil detach` 卸載，刪整份 sparsebundle，讓時光機下次自動重建。

結果：Amber 352G→51G（剩 416G）。課程影片 `~/amber-Videos` 不動，SSD 雙份在 `/Volumes/953-SSD/Amber重要備份/課程影片/`。細節見 workspace `knowledges/Amber整理/Amber盤點結果_2026-11-06.md`。

**Why:** 刪完 `df` 沒變差點誤判失敗、也差點誤報清出空間。
**How to apply:** 在 Amber 上刪東西，刪完立刻檢查 `@SmbRecyclebin`，並用 `df` 驗證實際變化。相關：[[feedback-check-benefit-before-recommending-2026-11-06]]
