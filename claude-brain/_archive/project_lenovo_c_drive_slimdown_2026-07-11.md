---
name: project-lenovo-c-drive-slimdown-2026-07-11
description: 聯想C槽大瘦身(125.8GB→96.25GB)，觀察期至2026-07-18，教練確認無異常後可刪兩份保留備份釋放約100GB
metadata: 
  node_type: memory
  type: project
  originSessionId: 1770c262-04fd-4812-9b49-c06f84deed0b
  modified: 2026-07-25T06:05:05.774Z
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

## 🔴🔴 2026-07-25更新：這份備份的刪除計畫作廢——它已經被拿去做過一次真實還原

原訂「觀察期滿(7/18)後刪除」的計畫**不再適用**。2026-07-24發生LINE junction事故（見[[project_line_moved_to_e]]鐵律9-11），教練最終用這份`E:\易数一键还原Windows系统备份（不要删除）`（SystemImage.pmf，87GB，2026-07-11 23:01建立）做了一次真正的系統還原，成功救回機器。2026-07-25查證這份備份檔案本身仍完整存在（未被任何後續操作動過）。

**Why：** 這份備份已證明有實際救援價值，不是理論上的保險——不能再照舊計畫刪除。且7/24~25期間又對這台機器做了不少改動（OpenCode/CC Switch資料搬E槽、Advanced SystemCare移除等），這份7/11的舊備份完全不知道這些新狀態，若又拿它還原會把這些新改動全部清空。

**How to apply：** 之後開工若教練問起這份備份，不要再引用「7/18觀察期滿可刪」這個舊結論。應建議：確認2026-07-24~25這波改動穩定後，做一次新的一鍵備份取代這份，新備份要重新走一輪至少7天觀察期，才能考慮刪除這份7/11舊的。

Related: [[project-line-moved-to-e]], [[feedback-check-crossmachine-history-before-system-ops]]
