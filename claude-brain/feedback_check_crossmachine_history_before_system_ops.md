---
name: feedback-check-crossmachine-history-before-system-ops
description: 系統性/跨機共通操作（App搬家、還原腳本等）動手前，必須先查兩台以上機器的雲端歷史經驗，不能只憑單一文件或當下判斷
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1770c262-04fd-4812-9b49-c06f84deed0b
---

遇到「這台機器以前做過類似的事」的系統性操作（App資料搬家、junction、還原腳本等），動手前要先查**所有機器**在雲端（`mac-openclaw-workflows`）留下的歷史紀錄，不能只看剛好找到的第一份文件就動手，尤其是要找「最後測試成功的版本」，不是「第一次寫的版本」。

**Why：** 2026-07-11——幫教練把 Chrome 資料搬到 E 槽後，準備把 Chrome 加進 `restore_junctions.ps1`（一鍵還原後重建junction用），教練喊停：「你去找歷史資料，我們那三台機子裡面有兩台都做過這件事情⋯⋯你要去讀取宏碁和聯想的資料。」一查才發現：
1. 舊版 `restore_junctions.ps1` 寫死 `D:\Claude-Data`，但聯想實際是 `E:\Claude-Data`，路徑整個是錯的
2. ACER 那邊已經把同一套方法論反覆實測到非常成熟的版本（`restore_junctions_acer.ps1`），甚至真的做過「退回2026年5月」的大膽實測驗證過，還抓到「乾淨世界程式本體其實在Roaming不在Local」這種容易搬錯的細節
3. 如果沒有先查，我會用一份過時、路徑錯誤的腳本去「更新」，教練未來真的一鍵還原時腳本會直接失效

**How to apply：** 這類操作屬於「多機器共同踩過的坑」，正確順序是：① 先搜雲端 repo 找同類關鍵字（如 `restore_junctions`、軟體名稱）② 找到多個版本時，比對日期/更新記錄找出「最後測試成功、最多細節」的那份，不是隨便一份 ③ 確認建議前先問「這台機器現在的真實狀態」（`Get-Item -Force` 查 junction attribute），不要照抄別台機器的路徑細節 ④ 遇到教練提醒「另一台機器也做過」，代表這是已知的跨機共通問題，一定有更完整的紀錄在雲端，不要憑當下判斷硬做。這條跟 [[feedback-query-before-conclude-and-act-on-facts]]（下結論前先查歷史）同精神，適用範圍更窄但更具體：系統性操作類。
