# 軍師接力棒 · 2026-07-08 v50（Mac 終端機 Sonnet 5，佩佩老師電腦雲端信箱系統上線，教練休息）

> 建立時間：2026-07-08 清晨 05:30（台灣時間）
> 本棒執行者：Mac 終端機軍師 **Sonnet 5**
> 上一棒：v49（2026-07-08 凌晨 03:55~04:53，Fable 5，系統全盤稽核+修復）
> 本棒主軸：**佩佩老師電腦第一次接上雲端大腦系統，建立「雲端信箱」讓她的 MiniMax 自主讀信執行 W03 SOP，教練已連續工作超長時間，交辦後去休息**

---

## 🎯 本場戰果

### 1. 破除「叫教練當搬運工」的錯誤做法
教練原本要我寫一段話叫他複製貼給佩佩老師電腦的 MiniMax，我一開始真的照做寫了要貼的文字——教練當場糾正：「我們不是已經建立一個雲端讀取的系統了嗎？」（守則 #12 拒絕當資訊搬運工）。改用既有的 `knowledges/TASK_xxx_給MiniMax.md` 雲端信箱慣例，把完整指示直接寫進 repo，commit + push，教練只要叫佩佩那邊的 CLI 讀信即可，不用貼任何技術內容。

### 2. 信件三次迭代，逐步補齊真實障礙
**檔案**：`knowledges/TASK_W03任務修正指示_給佩佩電腦MiniMax_2026-07-08.md`

- **第一版**（commit `3cbf96a09`）：糾正她查錯 `D:\Claude-Data\memory-source`（那是無關的舊機制），指出正確 repo 路徑、讀取順序（W03 → 案例30 → project_line_moved_to_e.md → 案例39）、Phase 1 執行規則、7天觀察期鐵律
- **第二版**（commit `a31a8894e`）：佩佩電腦回報 D 槽根本沒有這個 repo（她的機器是**第一次接上這套三機共用大腦系統**）——查證發現 `mac-openclaw-workflows` 是 **private repo**（curl 測試回傳 404 確認），且這台機器可能連 Git 都沒裝。信裡補上：`winget install Git.Git` 安裝檢查、私有 repo 認證流程（Username=`Coach1973`，Password=一次性 GitHub token，我用 `gh auth token` 現場取得並口頭告知教練，**沒有寫入任何檔案**，教練直接口頭轉達給佩佩電腦一次即可，之後 `credential.helper store` 會記住）
- **第三版**（commit `38ca34611`）：教練連續工作超長時間、天快亮要去休息，明確說「不要再問我了，也不想再盯著他」。信裡改為**自主執行模式**：
  - Phase 1（robocopy 搬資料 + 原資料夾改名 `.stale_backup` + 建 Junction + 驗證）本質可逆，**可以自主跑完全部 App，不用每個都停下來問**
  - 🔴 **安全紅線沒有放寬**：任何刪除動作（含 `delete_guard.ps1` 的 `Safe-Remove`）全程禁止；不做 W03 Phase 3 清理；遇到判斷不出來的陌生 App 一律跳過記錄、不用猜的硬做
  - 全部跑完後要求她的 MiniMax 寫一份 `knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md`（成功清單+待確認清單+`.stale_backup`路徑清單+一句話總結），commit+push，讓教練醒來一次看懂

### 3. 一次性 GitHub token（已口頭告知教練，不在任何檔案中）
用 Mac 端 `gh auth token`（Coach1973 帳號）取得，僅供佩佩電腦第一次 clone 私有 repo 認證用，之後 `credential.helper store` 會記住不用再輸入。**這個 token 沒有寫進任何 commit，純口頭轉達。**

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🔴 | **教練醒來後第一件事**：讀 `knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md`（如果佩佩電腦已經跑完並 push），確認搬移結果、待確認清單、`.stale_backup` 路徑；**7天內任何情況都不能刪這些資料夾** |
| 🟡 | 若佩佩電腦回報卡在認證或 Git 安裝問題，需要教練再次口頭確認 |
| 🟡 | v49 遺留：稽核報告 6 個🟡優化項逐項處理（見下方 v49 完整記錄） |
| 🟡 | biz-gym 黑金新版等教練說「推」 |
| 🟢 | 聯想/ACER 兩機的同款稽核（需教練拍板） |
| 🟢 | bigtree 7/29 場次 EDM 圖片教練做好後補上 |

---

## 🔑 關鍵檔案索引（本場）
- `knowledges/TASK_W03任務修正指示_給佩佩電腦MiniMax_2026-07-08.md` — 給佩佩電腦的完整雲端信箱
- `knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md` — 佩佩電腦執行完會產出的報告（教練起床後查）
- commit：`3cbf96a09`（初版）→ `a31a8894e`（補認證）→ `38ca34611`（自主模式+安全紅線）

---

## 📜 v49 完整記錄（Fable 5，2026-07-08 凌晨 03:55~04:53）

### 1. 全盤稽核報告
`knowledges/AUDIT_fable5_系統全盤稽核報告_2026-07-08.md`（commit `1ff4434d3`）
3 個🔴真問題 / 6 個🟡優化空間 / 7 個🟢查證過很好。每條附可重跑的查證方法。

### 2. 三個🔴全修完
- **紅1 自我餵養循環**：`session_end_auto_push.sh` 推送紀錄改寫 /tmp（`95fae5d2b`），順修空陣列舊 bug（`f197c7917`）
- **紅2 蒸餾三引擎**：LaunchAgent 卸載存檔 + 土炮排程器內建那份移除（`5d23cedc2`），只留 openclaw cron 單引擎
- **紅3 relay 殭屍四顆頭全斬**：LaunchAgent + 土炮排程器每分鐘輪詢 + kong/peipei 休眠分身各一，實測 relay 心跳停在 03:13 不再前進

### 3. 雙跑線路第二批拆除
crontab 三條註解 + 三個重複 LaunchAgent 卸載，commit `8332f5ab5`，全部存檔可復原（`_archive/launchagents_retired_20260708/`）

### 4. cloudflared 驗明正身
查 zsh_history 破案——LINE 頻道訊息通道，教練確認絕對不能斷，保留不動。閃電說（Tanwei Wuhan）教練核准刪除已完成。

### 5. cloudflared 三處永久封存
`路徑大全.md` 第十三節 + 試金石案例40 + `reference_xiaolongxia_line_tunnel_cloudflared.md`，commit `adf486baf`

---

> Sonnet 5 親筆，2026-07-08 清晨 05:30。本場處理教練跨機交辦佩佩老師電腦任務，核心是把「叫教練貼文字」修正為「雲端信箱系統」，並在教練休息前把執行規則從「逐App確認」升級為「自主執行+安全紅線不放寬」。教練休息中，下一棒接手時第一件事是看佩佩電腦的執行報告是否已產出。
