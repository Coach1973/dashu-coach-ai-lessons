---
name: project-acer-c-d-cleanup-20260708
description: 2026-07-08宏碁機工作總結——分割區調整後備份處理、D槽增量資料驗證+清理11.25GB重複、建立W03完整SOP，待辦：觀察期後刪除舊一鍵備份
metadata:
  type: project
  updated: 2026-07-08
---

# 2026-07-08 宏碁機工作總結

## 背景事件
教練用 MiniTool Partition Wizard 把 D 槽移了 118GB 到 C 槽，導致「易数一键还原（Eassos Restore）」判定既有備份失效無法還原。

## 已完成事項

1. **系統健康檢查**：實體硬碟/C槽/D槽皆 Healthy，NTFS 事件記錄僅一筆分割區調整後的自我修復（Event ID 130，已自動修復，未再發生），判定系統正常
2. **舊一鍵備份保留**：把調整分割區前（2026-07-03）建立的舊備份資料夾改名保留，**沒有刪除**：
   ```
   D:\一键备份Windows系统（重要！勿删）_20260703_before_resize\
     ├─ BootImage.pmf   42.4MB
     └─ SystemImage.pmf 約36.3GB
   ```
   教練已完成新的一鍵備份（分割區調整後）
3. **驗證D槽增量資料現況**：LINE（Cache+Data）、Zoom（data/logs/reports）、Comet（User Data）、Chrome（User Data）全部確認是「bin/Application留C、純資料junction到D」的正確架構，且都有近期寫入紀錄，證實是活的、正常運作中
4. **清理D槽重複舊快照，共釋放約11.25GB**：
   - 第一輪4.33GB：LINE-Cache.stale_backup_20260702、LINE-Data.stale_backup_20260702、Perplexity.stale_backup_20260703、Perplexity-Local.stale_backup_20260703、LINE-AppData-Local（06/25整包舊備份）
   - 第二輪6.92GB：Google-Chrome-Local（孤兒資料夾，沒有.stale_backup命名但沒有任何C槽Junction指向它）
   - 全程用 `scripts/delete_guard.ps1` 的 `Safe-Remove`，刪除後皆用 `Test-Path` 驗證回傳 False
   - **C槽本身這次沒有刪除任何東西**——C槽只保留必要主程式（bin/Application），不是重複品
5. **建立完整生命週期SOP**：`試金石/試金石_專案與代碼.md` 案例 W03，整合案例30+W01+案例39+`project_line_moved_to_e.md`，供另一台筆電照做

## 🔴 待辦事項（下次開工務必檢查）

**觀察期：2026-07-08 起算 3～7 天（最早 2026-07-11，穩妥抓 2026-07-15）**，期間教練會正常使用電腦確認無異常。

**觀察期結束、教練確認無問題後**，可以刪除以下已改名保留的舊備份，釋放約36.3GB：
```
D:\一键备份Windows系统（重要！勿删）_20260703_before_resize\
```
刪除前務必：① 再次跟教練口頭確認「這幾天用起來都正常嗎」② 用 `Safe-Remove` 走防呆流程，不要裸刪 ③ 刪除後 `Test-Path` 驗證 + 回報釋放空間

Related: [[project-acer-post-restore-todo]]
