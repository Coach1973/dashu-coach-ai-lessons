---
name: feedback-test-script-must-mock-side-effects
description: 寫測試腳本驗證hook邏輯時，凡是會打真實網路/發真實通知的呼叫都必須mock掉，不然每次重跑測試都會真的轟炸教練Telegram
metadata:
  type: feedback
  originSessionId: 84150fda-42bc-4356-acc0-ad3d3b4a8c7a
  modified: 2026-08-25T14:17:36.282Z
---

2026-08-25建立`session-summary-trigger`hook時寫的`test_session_summary_trigger_hook.js`，用假event物件跑過handler驗證觸發邏輯，但沒有攔截`sendTelegramDirect()`裡真正的`https.request`呼叫。同一天稍晚寫`context-overflow-guard`的測試時有做攔截（因為那個測試會一次跑過4個門檻，若不攔截等於自己送4則通知），但**沒有回頭把同款防護補進更早寫的那支測試**。

**後果**：這支沒攔截的測試腳本當天被重跑了3次（建功能時/修一個信封格式bug後/加賈維斯標籤驗證後），每次都真的發送7~8則「收到總結」訊息到教練Telegram。第一次重跑時有跟教練說明是測試副作用，但後兩次因為忙著處理別的事，忘記提醒，教練看到連續8則一模一樣的訊息以為系統故障，親自問「怎麼一次發這麼多則」。

**Why：** 測試的價值在於「可以隨時安心重跑」，一旦測試本身有真實副作用（發通知、寫真實資料、觸發外部API），重跑測試就變成一種賭博——賭這次重跑會不會意外打擾到人。這是可預防、模式化的坑，不是單一次疏忽。

**How to apply：**
1. 任何測試腳本，只要handler內部呼叫了`https.request`/`fetch`/`curl`等真實網路動作，寫測試的當下就要順手加攔截（monkey-patch該函式，記錄呼叫次數但不真的送出），不能拖到「之後有空再補」。
2. 寫新測試時，若專案裡已經有類似性質的測試（同樣會觸發外部副作用），先看那支測試怎麼做防護，直接抄同一套模式，不要重新設計一次卻漏掉關鍵步驟。
3. 測試最後要斷言「副作用真的被攔截了」（例如`sentCount === N`），不能只驗證業務邏輯本身，這樣才能在未來如果攔截失效時第一時間被測試本身抓到，而不是等教練回報才發現。
4. 若真的需要重跑一支「已知會產生真實副作用」的測試，重跑前先提醒使用者，不要假設「上次講過一次以後就不用再講」。

Related: [[feedback_ezpay_confirm_before_submit_2026-08-18]]（同樣是「送出前確認」精神的延伸——這裡是「送出（測試）前先確認有沒有攔截」）

---
## 🛟 2026-10-16 從自動暫存救回的段落（原本在 2026-09-11 02:30 寫進來，被自動同步放回失敗弄丟；照原樣補回，未改寫）

**2026-09-10二度發生（不同腳本，同根因）：** 驗證invoice-inbound誤報修復(commit `5dd58e7bf`)時重跑`scripts/test_invoice_inbound_hook.js`，發現該腳本的`INVOICE_HOOK_TEST=1`只攔截了`sendTelegram()`（避免真的發通知），卻沒攔截`fs.appendFileSync()`落地寫檔——導致5筆測試假資料混進正式的`state/invoice_inbox/2026-09.jsonl`，污染真實對帳資料。當場發現後用`git checkout`清乾淨，並根治：`INVOICE_HOOK_TEST=1`時改把落地目錄整個換成`invoice_inbox_test`（handler.js跟測試腳本同步改），測試腳本結尾自動`rmSync`清掉該目錄，commit`906d39ed4`(外層repo)+`45258482b`(workspace)。**新教訓**：本條守則第1點寫的是「呼叫https.request/fetch要攔截」，但沒提醒「寫真實檔案（fs.appendFileSync/writeFileSync）同樣算副作用」——凡是測試會操作正式資料檔案路徑的，都要考慮改寫獨立測試路徑，不能只想到網路呼叫這一種副作用。
