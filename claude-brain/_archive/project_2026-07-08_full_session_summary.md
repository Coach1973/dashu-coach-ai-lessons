---
name: project-2026-07-08-full-session-summary
description: 2026-07-08整場session總結——LINE驗證起頭，延伸C槽大體檢/查證方向系統/教練工具箱/佩佩電腦跨機協作
metadata:
  type: project
  originSessionId: a8416d87-73e6-474e-98f8-1a099e9b1ad3
  updated: 2026-07-08
---

# 2026-07-08 整場對話總結（聯想機軍師 Sonnet 5）

## 這場對話的完整脈絡（一件事牽出一件事）

1. **起點**：教練只問「LINE 增量資料是不是都在 E 槽」——查證 Junction 正常、E 槽資料每天都有新寫入，確認搬家成功
2. **延伸出過期備份清理**：順手全機掃描，發現 GanJing、Perplexity、Claude 桌面版沙盒也有同一批 6/25、6/30 搬家留下的過期 `.bak`，教練確認後五組一起清除，釋放 13.8GB（詳見 [[project_lenovo_c_drive_checkup_2026-07-08]]、試金石案例 39）
3. **教練要求做完整 C 槽大體檢**：找出 AppData 佔用大戶、評估 Windows.old 存廢，一路查到 Eassos Restore（易數一鍵還原）備份系統的內部結構（`Options.ini` 的 `[ImageFiles]`/`[Restore]` 區段），證實備份系統本身完全健康，教練擔心的「找不到備份」只是掃描 287GB 較慢
4. **Chrome 差點被誤判成需要搬家**：查證中發現 `robocopy` 會跟隨巢狀 Junction 但 `Get-ChildItem` 不會，導致同一份資料算出兩種數字，一度誤建重複資料夾，及時發現並清除，記錄成試金石案例 41
5. **Windows.old 清除**：手動 `takeown`+`icacls` 組合失敗一次，改用官方 `cleanmgr /sagerun` 機制成功
6. **關鍵轉折——教練重話糾正**：軍師問「你有沒有印象 Chrome 書籤變空過」，教練當場糾正「凡走過必留痕跡，不准問我記不記得」，軍師改用 `git log --grep` 五分鐘內查到根因（宏碁機三帳號遺失教訓，commit `737bd140`）。這次事件被系統化成**查證方向七層系統**（見 [[feedback_never_ask_coach_recall_self_verify]]、試金石案例 42），並延伸建立 **[[reference_coach_common_toolbox]]**（教練常用工具箱，收錄 yes/no 免問指令等反覆需求）
7. **跨機協作——佩佩老師電腦**：教練把 W03 SOP 指派給佩佩老師的電腦（她的 Claude CLI 第一次接上這套三機共用大腦），過程中：
   - Mac 軍師先解決了 repo 私有認證、自主執行模式的建立（教練連續工作很久要求「不要再問我」）
   - 聯想機軍師負責技術判斷：評估佩佩 CLI 對 Chrome 架構的判斷（方向對但漏查巢狀 Junction，已提醒）、寫 Discord/GanJing/Microsoft 三項搬家指示（Discord/GanJing 給現成腳本，Microsoft 明確禁止盲搬要求先列清單）、修正指示對齊 Mac 已建立的自主模式（不用逐項回報）、讀取佩佩電腦回傳的執行報告並對 Microsoft 資料夾四個問題逐條拍板（Office 不動、TeamsMeetingAdd-in 不砍因為觸犯刪除紅線、不查 Program Files、整體跳過選項 A）
   - 全程透過 `knowledges/TASK_*_給佩佩電腦MiniMax_*.md` 雲端信箱慣例溝通，**沒有一次讓教練當轉貼的搬運工**

## 這場對話最重要的三個教訓

1. **查證方向七層系統**（最重要）：git log → 試金石案例庫 → memory 記憶檔 → HEARTBEAT/接力棒 → 每日蒸餾摘要 → 原始對話 jsonl → 即時系統現況。教練親口重話：「凡走過必留痕跡，如果我的腦袋能記那麼多細節，要你何用？」
2. **搬家前一定要查巢狀 Junction**：外層資料夾不是 Junction 不代表沒搬過家，可能內部子資料夾已個別搬移（案例 41），這個教訓在佩佩電腦協作中直接派上用場（提醒她同樣的檢查）
3. **不同 AI 系統協作要透過雲端信箱，不透過教練轉貼**：整場跟佩佩電腦的往來，教練只需要偶爾看結果、做真正需要人判斷的決定（例如要不要接受某項評估），技術層面的問答、指令、報告全部走 git commit，完全落實守則 #12

## 相關記憶檔案索引

- [[project_lenovo_c_drive_checkup_2026-07-08]] — C 槽瘦身技術細節完整記錄
- [[feedback_never_ask_coach_recall_self_verify]] — 查證方向七層系統
- [[reference_coach_common_toolbox]] — 教練常用工具箱
- 試金石案例 39（過期備份清理 SOP）、41（robocopy 巢狀 Junction 地雷）、42（查證方向七層系統）
- `knowledges/TASK_*_給佩佩電腦MiniMax_*.md`（4 封信）、`knowledges/REPORT_佩佩電腦*.md`（2 份報告）— 跨機協作完整記錄，在 `mac-openclaw-workflows` repo 裡

## Why / How to apply

**Why:** 這場對話從一個簡單查證問題，因為教練持續往下追問（「你怎麼知道」「這樣不合理」「查一下歷史紀錄」），逐步逼出好幾個系統性改進——包括一個會影響所有機器、所有未來對話的核心工作方法糾正。這證明教練追問到底不是找麻煩，是在逼出更紮實的系統。

**How to apply:** 下次任何機器接手新任務時，先讀查證方向七層系統 + 教練常用工具箱這兩份，能省下大量重新摸索的時間。跨機協作任務優先用雲端信箱慣例，不要覺得「叫教練傳句話比較快」就抄捷徑。
