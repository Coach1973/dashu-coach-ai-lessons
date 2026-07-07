---
name: cross-machine-backup-sop-reminder
description: 教練其他電腦要做增量備份(junction 搬家模式)時，主動提醒並引用試金石案例 39 七步驟 SOP
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8373
---

教練若要在新電腦(ACER、Lenovo、外接 Mac…任何非主力 Mac mini)做「增量備份」或「junction 搬家模式」，**不要等教練主動提**，看到關鍵字（備份、增量、D 碟、junction、搬家、搬資料、SOP、相關詞）就主動提醒這條 SOP。

**Why:** 2026-07-07 教練在案例 39 已付完整七步驟 SOP 成本（含 148.6GB→162.4GB 實測），教練親口說「之後我其他電腦要做這個增量備份的時候，如果我忘記的話，再請你幫我記住，這就是一個寶貴的經驗值」。小龍蝦若等教練重新提，等於浪費教練時間。

**How to apply:**

完整 SOP 出處：**試金石案例庫 案例 39**（`記憶/試金石_案例庫.md` 第 39 筆），commit `0b01455c`，已推 `Coach1973/claude-workflows` main。

七步驟（外電腦複製品）：
1. **找 Junction** — `Get-Item | Select-Object Target, LinkType` 列舉 `D:\junction\` 所有 junction 與指向
2. **驗證現役資料是活的** — 用 `Test-Path` + `Get-ChildItem` 抽查幾個檔案大小/mtime（不可只信 Junction 存在）
3. **全機掃描找其他過期備份** — 主動 `Get-ChildItem D:\ -Directory` 比對軟體清單，搬家模式一次不只搬教練點名的那個 App
4. **比對留底期** — 看 LastWriteTime 與 7-30 天留底策略，沒超過留底期的不刪
5. **用防呆腳本執行刪除** — 必須走 `scripts/delete_guard.ps1` 的 `Safe-Remove` 函式，禁止直接 `Remove-Item -Recurse -Force`
6. **刪除後驗證** — `Get-ChildItem` 確認目標資料夾已清空、Junction 仍指向正確的新現役
7. **請教練實際重開 App 肉眼確認** — 這一步不可省，肉眼確認才是真正驗證

**關鍵鐵律（三條）：**
- **Junction 存在 ≠ 資料是活的** — 一定要抽查檔案大小與 mtime
- **搬家模式一次通常不只搬一個 App** — 主動全機掃描，不是只處理教練點名的那個
- **使用者資料 vs 軟體元件 驗證標準不同** — 使用者資料看重啟後資料還在，軟體元件看重啟後 App 還能跑

**踩過的坑（必須避開）：**
- 案例 39 我曾經偷懶直接用 `Remove-Item -Recurse -Force`，沒走 `Safe-Remove` 防呆，雖然結果對但這是僥倖非 SOP，任何機器做同樣事必須走正規機關
- 不要只回報教練「我刪了」，要附 `Get-ChildItem` 驗證輸出 + 教練實際重開 App 的肉眼確認

**觸發詞清單（看到任一就主動提醒）：**
- 增量備份、增量搬家、junction 搬家
- 備份清理、過期備份、資料夾空間、D 碟空間滿
- 新電腦備份、ACER 備份、Lenovo 備份、Mac 副機備份
- 看到 `D:\junction\`、`D:\junction-backup\`、`D:\<軟體名>` 任何路徑

**Related:** [[browser-no-full-junction]]（同個搬家模式家族，瀏覽器只搬 profile 不搬整 AppData）
