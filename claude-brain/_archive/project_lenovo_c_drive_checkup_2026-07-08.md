---
name: project-lenovo-c-drive-checkup-2026-07-08
description: 聯想機(TREE)C槽大體檢+瘦身完成記錄——釋放約34GB，發現Chrome早已用細粒度Junction搬家
metadata:
  type: project
  originSessionId: a8416d87-73e6-474e-98f8-1a099e9b1ad3
  updated: 2026-07-08
---

# 聯想機（TREE）C 槽大體檢 + 瘦身完成記錄（2026-07-08）

## 背景

同一場對話從「LINE 增量資料是否都在 E 槽」的簡單查證，延伸成完整的 C 槽健康檢查與瘦身。C 槽總容量 310GB，起始可用 148.6GB，最終可用約 182.5GB，**總共釋放約 34GB**。

## 完成項目

| 項目 | 結果 | 備註 |
|---|---|---|
| LINE/GanJing/Perplexity/Claude桌面版沙盒 過期搬家備份 | 刪除 5 組，釋放 13.8GB | 見 [[project_line_moved_to_e]] 第五節、試金石案例 39 |
| Desktop 舊 opcode 開發資料夾 | target(7.15GB)+node_modules(0.23GB)刪除，剩餘原始碼(0.01GB)搬存 E 槽 | 這個 Desktop 資料夾早已被 D 槽的真桌面取代，是純殘留 |
| Chrome User Data | **發現早已用細粒度 Junction 搬家**（只搬 `Default`+`OptGuideOnDeviceModel` 兩個子資料夾到 E 槽，不是整包搬），不需動作 | 見試金石案例 41，過程中誤建過一次重複資料夾已清除 |
| NotebookLM 工具舊登入資料(chrome-profiles) | 刪除 4.35GB | 下次用該工具需重新登入 |
| 開發工具真快取(.cargo\registry、.bun\install\cache) | 刪除約 0.74GB | `.rustup`（工具鏈本體）、`.openclaw`（系統設定檔）、`.local` 皆確認未動 |
| Windows.old | 用 `cleanmgr /sagerun` 官方磁碟清理機制清除，1.1GB | 手動 takeown+icacls+Remove-Item 組合失敗過一次，改用官方機制才成功 |

## 關鍵發現：Eassos Restore（易數一鍵還原）備份系統健康

- 這台機器裝的是「易數一鍵還原 4.13.1」（Eassos Restore，秦皇岛易数科技），安裝於 `C:\Program Files\易數一鍵還原\`
- 備份目錄：`E:\易数一键还原Windows系统备份（不要删除）`，內含母片(SystemImage.pmf)+多個時間點增量(.ptp)
- 該工具的 `Options.ini` 內建完整的備份影像清單（`[ImageFiles]` 區段 Image0~Image8），且 `[Restore]` 區段本來就已預設指向最新時間點——教練當初擔心「搜尋找不到備份」是虛驚一場，工具本身完全正常，只是掃描 287GB 大量資料速度較慢
- 教練另有獨立的書籤保險：`D:\Users\Desktop\四瀏覽器書籤合併.html`（2026-07-02 建立），不依賴瀏覽器 profile 本身

## Why / How to apply

**Why:** 這場檢查證明「Junction 存在」不等於「沒有其他細節」——Chrome 表面上外層資料夾是一般目錄，但內部兩個最大子資料夾早已個別 Junction，若沒有先查巢狀結構就直接整包搬家，會製造出重複資料的畸形結構（見試金石案例 41）。

**How to apply:** 下次任何機器要做類似的 C 槽瘦身或 App 搬家檢查，先讀本檔案+試金石案例 39/41，不用重新從零摸索。任何「搬家前」動作，第一步永遠是檢查目標資料夾內部有沒有巢狀 Junction。
