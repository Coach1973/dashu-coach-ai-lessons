---
name: project-lenovo-c-drive-slimdown-2026-07-11
description: 聯想C槽大瘦身(125.8GB→96.25GB)，觀察期至2026-07-18，教練確認無異常後可刪兩份保留備份釋放約100GB
metadata: 
  node_type: memory
  type: project
  originSessionId: 1770c262-04fd-4812-9b49-c06f84deed0b
---

# 2026-07-11 聯想C槽瘦身總結

## 已完成項目
1. Temp暫存檔清空（1.19GB→0）
2. Chrome/Edge瀏覽器快取清空（約8GB）
3. 休眠檔hiberfil.sys刪除（關閉休眠功能，15.89GB）
4. Chrome User Data搬到E槽（junction，10GB），Application程式本體留C槽
5. WinSxS元件存放區清理（17.18GB→11.17GB，省6GB，DISM官方工具建議清理）
6. 分頁檔從12GB手動固定，改成4GB手動固定（教練考量：常同時開3個瀏覽器、每個十幾分頁，需要一定緩衝，不設更小）
7. Comet瀏覽器修復：發現舊版曾把整個Comet資料夾（含Application程式本體）誤junction到E槽，違反「主程式留C槽」原則，已修正為Application搬回C槽真實資料夾、只針對User Data重建junction（跟ACER之前修過的同款問題）

**C槽總結果：125.8GB → 96.25GB，釋放約29.5GB**

## 🔴 待辦：2026-07-18（滿7天）觀察期結束後執行

教練親口：「若一週後沒有什麼問題，就可以刪除其他的備份檔案了，可以跟我說」

**Why：** 今天做了較大幅度的系統變動（Chrome/Comet搬家+休眠關閉+分頁檔改小+WinSxS清理），照established SOP（見 [[project-line-moved-to-e]] 4GB資料永久遺失血淚教訓）任何搬家/系統變動的備份都要保留至少7天才能刪，不管當下看起來多穩定。

**How to apply：** 教練開工時如果日期已到或超過2026-07-18，主動提醒並詢問「這幾天Chrome、Comet、電腦整體用起來正常嗎？」，教練確認無異常後，執行以下清理（用Safe-Remove/資源回收桶方式，非裸刪）：

| 項目 | 路徑 | 大小 |
|------|------|------|
| Chrome搬家前系統備份 | `E:\易数一键还原Windows系统备份_20260711搬家前保留_不要刪除\` | 91.21GB |
| Comet舊整包搬移殘留 | `E:\Claude-Data\AppData\Perplexity-Comet.bak-舊整包搬移.20260711-191240\` | 約3GB |

**釋放空間：約94GB**

刪除前務必：① 教練口頭確認這幾天使用正常 ② 用資源回收桶方式刪除非永久刪除 ③ 刪除後Test-Path驗證+回報釋放空間

## 相關檔案
- 聯想還原腳本：`mac-openclaw-workflows/scripts/restore_junctions_lenovo.ps1`（已包含Chrome/Comet正確架構記錄）
- 教練最終備份：`E:\易数一键还原Windows系统备份（不要删除）\SystemImage.pmf`（81.05GB，2026-07-11 23:01）

Related: [[project-line-moved-to-e]], [[feedback-check-crossmachine-history-before-system-ops]]
