---
name: reference-bni-connect-credit-button-states-and-dialog-override-2026-08-28
description: BNI Connect信用証頁面「離開」狀態的三種按鈕型態判讀法+原生confirm()對話框卡住CDP的解法，下次操作信用証相關頁面直接套用
metadata: 
  node_type: memory
  type: reference
  originSessionId: 47fca155-b2ce-4fdb-a972-20c2d2ab1fe4
  modified: 2026-08-28T02:18:44.015Z
---

BNI Connect會員資料頁(`operationsRegionEditMembership?legacyPortal=true&memberId={ID}#tabs-6`)裡，離會會員的「目前狀態」欄位有三種不同的UI型態，點擊前肉眼看不出差異，必須看按鈕文字才能分辨：

1. **「離開 產生信用証」**（`id="genCocButton"`）：從未開立過信用証，可以嘗試產生新證。點擊有機率（實測近100%）成功產生真實、無法撤銷的正式證件。
2. **「離開 信用證」**（`id="certificateofcredit"`）：已經開過一張舊證，只是連結壞掉(`href="#"`)查不到內容，點擊會顯示「Please contact support for further assistance.」，這是真的過期，不會再產生新證。
3. **純「離開」無任何按鈕**：真的沒有剩餘會期額度，連隱藏的`genCocButton`元素都存在但點擊完全無反應，不會跳出任何錯誤訊息。

**關鍵發現：第①類按鈕點擊「失敗」不一定代表真的沒資格**——同一顆按鈕、同樣的畫面，實測中有記錄第一次點擊顯示「Please contact support」，重試第二次就成功產生真證（如「胡宗奇」案例）。這代表①類記錄若第一次失敗，值得重試1~2次再下結論，不要直接歸類成「沒有額度」。②③類記錄則測試多次結果一致，是真的無法開證。

**技術操作細節**：
- 點擊觸發用`jQuery('#genCocButton').trigger('click')`（純DOM `.click()`對jQuery綁定的事件無效）
- **點擊會跳出瀏覽器原生`confirm()`對話框，讓CDP的`Runtime.evaluate`整個卡住逾時(45秒)**——這不是bug，是頁面本身的確認機制。解法：點擊前先執行`window.confirm=function(){return true;}; window.alert=function(){};`把原生對話框函式覆蓋成no-op，讓頁面呼叫`confirm()`時直接拿到`true`，不會真的彈出需要真人按確定的原生視窗。這跟ezPay發票案例的`window.alert=function(){}`覆蓋技巧同源，但信用証這裡`confirm()`也要一併蓋掉。
- 產生成功後，抓取詳細內容(公司/信用額度/到期日)的做法：從畫面上找`textContent.trim()==='信用證'`的`<a>`元素，取其`href`用正則`memberCertificateOfCreditId=(\d+)`抓cert_id，再用`location.href=href`跳轉到`viewAdminRegionCertificateOfCredit?isFormSubmit=true&memberCertificateOfCreditId={certId}`頁面讀取全部欄位。

**適用場景**：任何BNI Connect信用証相關的批次查證/操作任務，直接套用這三種狀態判讀法+對話框覆蓋技巧，不用重新摸索。

Related: [[feedback_never_click_action_buttons_on_thirdparty_systems_2026-08-28]]（本次點擊是教練明確授權後才執行，跟該案例「未經授權誤觸」的情境不同，兩者不衝突——授權後才可以按，且要先確認「兩年效期即使誤產生也可接受」這個風險評估前提）
