---
name: feedback-delegate-bulk-browser-ops-to-background-agent
description: 大量重複性瀏覽器操作(如逐一查詢上百筆memberId)要委派背景Agent接續執行，不要自己逐輪手動跑browser_batch
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8a2ee41-544f-4fb8-8653-363802ff54d3
  modified: 2026-08-27T14:20:13.068Z
---

遇到「同一套SOP要對上百筆對象重複執行、且需要活躍瀏覽器session（無法簡化成純腳本）」的任務時，查完少量樣本驗證SOP可行後，應立刻把剩餘大量重複部分打包成完整指令（含SOP、判讀邏輯、資料庫寫入格式、範例）交給背景Agent（`Agent`工具，`run_in_background: true`）繼續執行，自己回到前台跟教練互動或處理其他事，不要自己逐輪手動跑`browser_batch`一批批啃完。

**Why**：2026-08-27 BNI信用証清查任務（查真鑽分會231位離會會員的信用証開立狀況），先手動查了10人驗證SOP無誤後，改為委派背景Agent查剩餘211人，教練當場肯定「很棒，你早該這麼做，這樣就不會浪費資源及流量了」。跟既有記憶[[feedback_junshi_token_economy_outsource]]（耗token動作寫腳本丟終端機跑）同一信念，但情境更精確：那條講的是「可以簡化成純腳本」的情境（grep/log掃描），這條講的是「需要活的瀏覽器session、不能簡化成純腳本、但仍然是機械性重複」的情境——正確做法不是自己硬扛，也不是寫死腳本，而是委派背景Agent（Agent本身有完整工具權限，能接手瀏覽器操作），讓前台軍師的對話輪次跟token留給真正需要判斷力的事。

**How to apply**：
1. 遇到「一套流程要對N個對象（N≥30~50這種量級）重複執行」且流程包含瀏覽器互動（navigate/click/javascript_exec等）時，不要預設自己要逐批手動跑完
2. 先手動跑一小批（5~10筆）驗證SOP判讀邏輯正確、資料庫寫入格式正確
3. 驗證通過後，把「完整SOP＋剩餘對象清單＋資料庫schema與寫入範例＋最終交付格式要求」整理成一份自足的prompt，委派給`general-purpose`背景Agent，`run_in_background: true`
4. 委派指令要包含：瀏覽器裝置選擇方式（isLocal:true device的deviceId，如果同一場對話已經選過就直接給，不用再讓Agent重新問一次）、每批次筆數建議（避免單次輸出過長難以核對）、每N筆存一次資料庫（避免斷線遺失）、完成後如何更新接力棒/commit/回報格式
5. 自己回到前台等待完成通知，不要用Bash `tail`背景Agent的輸出檔案（會塞爆自己的context），也不要重複做背景Agent正在做的事

Related: [[feedback_junshi_token_economy_outsource]]（同一信念：軍師流量稀缺，耗token動作要外包，但這條是「可寫成純腳本」情境；本條是「需要活瀏覽器session、只能委派Agent」情境）
