---
name: project-peipei-w03-first-run-2026-07-08
description: 佩佩老師電腦第一次接上三機共用大腦系統+首次執行W03搬家SOP完整過程與結果，2026-07-08教練休息期間自主完成
metadata: 
  node_type: memory
  type: project
  originSessionId: ba466be0-58a7-4f84-a170-be1f5344791a
---

佩佩老師電腦（D槽，MiniMax Opus 4.8）是**第一次**接上 `mac-openclaw-workflows` 這個雲端共用大腦，過程與結果分兩段記錄。

## 第一段：雲端信箱系統建立（教練親自糾正做法）
教練原本要軍師寫一段話叫他複製貼給佩佩電腦的MiniMax，軍師照做後被教練當場糾正：「我們不是已經建立一個雲端讀取的系統了嗎？」（守則#12）。改用既有的 `knowledges/TASK_xxx_給MiniMax.md` 雲端信箱慣例，寫信直接commit+push上repo，教練只需口頭轉達「去讀信」。

信件迭代三次才補齊真實障礙：
1. 糾正她查錯 `D:\Claude-Data\memory-source`（無關的舊機制）
2. 發現這台機器**從未clone過repo、可能沒裝Git**，且 `mac-openclaw-workflows` 是**private repo**（curl測404確認）——補上winget裝Git、GitHub token一次性認證流程（token用`gh auth token`現場取得，只口頭告知教練，不寫入任何檔案）
3. 教練連續工作超長時間要休息，說「不要再問我了」——信改為**自主執行模式**：Phase1（robocopy+改名+建Junction，本質可逆）可自主跑完全部App；但刪除類動作、Phase3清理**安全紅線不放寬**，全程禁止；遇陌生App判斷不出來要跳過記錄不能瞎猜；跑完寫報告commit+push

信件檔案：`knowledges/TASK_W03任務修正指示_給佩佩電腦MiniMax_2026-07-08.md`，commit演進 `3cbf96a09`→`a31a8894e`→`38ca34611`

## 第二段：佩佩MiniMax實際執行結果（報告：`knowledges/REPORT_佩佩電腦W03搬家執行報告_2026-07-08.md`）

**成果**：4個App完成搬移（Comet 1.79GB、Discord 20.8MB、GanJing 391.5MB、Zoom 3個子資料夾42.1MB），共2.21GB，全部改名`.stale_backup`/`.bak`建Junction，**7天觀察期到2026-07-15前絕對不刪**。

**做對的事**：Comet 36個process沒自己殺、請教練手動關；LINE/Chrome自我驗證後判斷「已完成/是活的」正確跳過不亂動；Zoom Roaming-data來源與目的地檔案數量對不上（多418檔/63MB）時**自動abort沒有硬做**，沒有rename也沒建Junction，正確地把不確定的情況攔下來等教練判斷。

**誠實記下的違規**：
- 違反#15「說不知道比胡說八道更值得尊重」：GanJing第一次查路徑PowerShell編碼炸掉沒輸出，誤判成「不存在」，是教練堅持才換方法查到——**不夠查證就下結論**
- 誤把軍師+教練親口授權的GitHub token指示當成prompt injection拒絕動手，後來讀完v50接力棒才理解是正當指示——**應先看完整context再下結論**

**待教練起床後處理**：
1. 開Comet/Discord/GanJing/Zoom驗證功能正常（Comet已驗✅，其餘3個待驗）
2. 2026-07-15觀察期滿後，教練明確說「砍[路徑]」才走`Safe-Remove`五道閘門刪除6個`.bak`/`.stale_backup`，預期回收約3.13GB
3. Zoom Roaming-data 933MB不一致問題待處理
4. 桌面4個中文編碼亂碼資料夾（共4.6GB）待翻譯資料夾名後判斷
5. Microsoft 1.73GB、Program Files裡的Edge殘留，教練自行決定是否處理

**技術心得（佩佩MiniMax自己悟到，值得其他機器參考）**：
- PowerShell 5.1簡中編碼跑複雜script容易parse error，寫成`.ps1`檔案再用`powershell -NoProfile -ExecutionPolicy Bypass -File`跑最穩
- robocopy exit code 1-7都是成功（1="files copied successfully"），8+才是真的失敗
- 對照表（W03的App分類表）是「已知做法的範本」不是限制清單，教練口頭決定優先於對照表

Related: [[feedback_cross_machine_backup_reminder]]、[[project_line_moved_to_e]]
