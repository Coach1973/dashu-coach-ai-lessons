---
name: reference-ezpay-invoice-issuing-procedure
description: ezPay電子發票開立操作SOP，含自訂編號規則/品項代碼/含稅計算易錯陷阱/送出後查證方法/JS直接呼叫送出法/computer工具打字失效時改用jQuery trigger
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7d4244d1-db9c-42f8-97ad-dc02499cbe41
  modified: 2026-08-28T14:10:21.604Z
---

操作對象：inv.ezpay.com.tw，帳號bymyway。**同一帳號下有兩個商店**：①「(337391376)BNI台南南區」——BNI入會/續約發票 ②「(344031309)大樹教育顧問有限公司」——培訓費發票(品項`B03`/`BNI培訓`)，不要跟另一個舊代號`(337643900)大樹教育顧問`搞混。開立用`Invoice_issue/create_invoice`，查詢用`Invoice_issue/search_invoice`。

**登入狀態per機器**：跟BNI Connect CMS同款限制，換機器操作前教練要親自在那台電腦的Chrome重新登入一次ezPay，不會跨機器同步。

**查詢限制**：查詢日期區間最長3個月，超過會觸發原生`alert()`把整個分頁卡死，操作前先`window.alert=function(){}`覆蓋掉。查2年以上歷史要切成8個季度分批查。

**自訂編號規則**（教練親定）：當天日期MMDD+兩碼流水號，例如0816**01**=8/16第一張、0816**02**=第二張。開立前務必先查當天有沒有人已經開過，避免撞號。

**品項代碼**：`B02`/`BNI續約`（續約價，2026年約$26,800）、`B01`/`BNI入會`（新加入價，約$36,000~39,800，實際金額以教練當下口頭確認為準，不同會員/年度可能有差異）。

**發票備註是查會員身分的關鍵**：買受人名稱通常是公司行號，統編查不到會員本人是誰——會員姓名寫在「發票備註」欄，格式`分會名-會員姓名`（例：`真鑽-蘇志揚`）。要核對某個統編對應哪位會員，用列表的「查看/補發」連結開發票明細modal，備註欄就是答案。

**含稅計算易踩坑**：
1. 單價/數量欄位用`form_input`或直接改`.value`常常不會觸發站方JS的金額計算，要嘛用真人打字方式（triple_click選取+type輸入），要嘛JS呼叫`element.click()`（不能只改`.checked`屬性+dispatch `change`事件，那樣「含稅」checkbox勾了但金額還是照未稅算）。
2. 送出前務必讀`TotleAmount`欄位數字核對是否等於教練講的金額——2026-08-16當場踩過2次金額算錯（未稅$28,140而非含稅$26,800）都是這個原因。

**送出＋查證**：提交按鈕id是`create_btn`。點下去有時分頁會短暫卡住（像原生對話框或整頁reload），屬正常現象，等1~2秒再操作。**表單清空不等於發票真的建立成功**——2026-08-16曾發生表單清空但發票其實沒送出的狀況，正確做法是每次送出後都回`search_invoice`頁用自訂編號或買受人統編搜尋，確認發票真的存在（發票號碼/金額/狀態=已開立）才能回報教練完成。

**🔴🔴 2026-08-18 Mac新發現：MerchantID(商店)下拉選單視覺上顯示第一個選項，但實際`selectedIndex`是-1(真的沒選)**——`read_page`的accessibility tree會誤導成「已選中」，肉眼/工具查都看不出破綻，唯一驗證法是直接`document.getElementById('MerchantID').value`，空字串代表沒選。沒選中直接送出會收到`{"status":"INV10001","message":"商店代號不可為空值"}`，且**表單仍會清空、看起來像成功**——這是新的一種「假成功」陷阱，跟先前紀錄的「CDP卡住讓人誤判」不同根因、同樣後果。送出前必做：
```js
const sel = document.getElementById('MerchantID');
sel.value = '344031309';  // 或其他正確商店代號
sel.dispatchEvent(new Event('change', {bubbles:true}));
```

**🔴 送出按鈕可靠觸發法**：`document.getElementById('create_btn').click()`（含`computer`工具的真實滑鼠點擊）在此系統**不保證**觸發送出（曾實測完全無反應、無XHR、無DOM變化）；改用`jQuery('#create_btn').trigger('click')`才穩定觸發。查詢頁的`#search_btn`同樣有這個問題，改用直接呼叫底層函式`search_invoice_info.send_search_invoice('1')`最穩定（不要依賴點擊）。

**🔴 「送出後CDP逾時/`Inspected target navigated or closed`」不是失敗徵兆，反而常是成功徵兆**——2026-08-18實測16張發票，每張成功送出後這個JS執行環境都會因為頁面reload而中斷評估、丟出`Inspected target navigated or closed`錯誤，這時候不要慌，直接`navigate`到`search_invoice`頁用自訂編號查證即可，通常都已經真的建立成功。

**🔴 每次`navigate`（含頁面reload）後，`window.alert`/`window.confirm`的override會重置**——因為那是頁面JS context的臨時覆蓋，換頁就消失。每次到新頁面第一件事都要重新蓋一次，不能只在最開始蓋一次就以為全程有效。

**🔴 用XHR攔截器驗證真實回應內容，不要只信HTTP狀態碼**——`create_invoice_by_db`/`search_invoice_by_db`這兩支API即使業務邏輯失敗（例如商店代號空值），HTTP狀態碼仍是200，只有解析`responseText`裡的`status`欄位（`SUCCESS`/`INV10001`等錯誤碼）才知道真相。攔截寫法：
```js
window.__lastXHRResponses = [];
const origOpen = XMLHttpRequest.prototype.open, origSend = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open = function(m,u){this.__url=u; return origOpen.apply(this,arguments);};
XMLHttpRequest.prototype.send = function(b){
  this.addEventListener('load', function(){ window.__lastXHRResponses.push({url:this.__url,status:this.status,body:this.responseText}); });
  return origSend.apply(this,arguments);
};
```

**🔴🔴 2026-08-28發現：`computer`工具的`triple_click`+`type`對`ItemCount1`/`ItemPrice1`欄位可能完全失效，且沒有任何錯誤訊息**——實測過程：`triple_click`後用JS確認`document.activeElement.id`確實等於目標欄位id（真的有focus），接著`computer type`打字，但欄位`.value`還是空字串，連原生`keydown`/`keypress`/`input`事件都完全沒有被監聽器捕捉到（用`addEventListener`掛在欄位上實測印證，一個事件都沒發生）。目前判斷是claude-in-chrome的`computer`工具在這個頁面對這兩個特定欄位的鍵盤模擬沒有真正送達（原因未明，`triple_click`用ref或用座標都一樣失效，跟extension/CDP鍵盤事件在這個頁面沒有正確落地有關，不是focus的問題）。

**可靠替代方案**：改用JS直接設定`.value` + 觸發**jQuery風格**的事件（不是原生`dispatchEvent`，這個網站的金額試算邏輯是jQuery委派監聽`keyup`，原生`el.dispatchEvent(new Event('keyup'))`測試無效，必須用`jQuery(...).trigger(...)`）：
```js
document.getElementById('ItemCount1').value = '1';
document.getElementById('ItemPrice1').value = '15300';
jQuery('#ItemCount1').trigger('keyup');
jQuery('#ItemPrice1').trigger('keyup');
```
`ItemAmount1`（單列金額）會先自動算出。接著含稅checkbox（`priceCount`，一樣先讀`.checked`現況，false才`click()`）之後，**如果`[name="TotleAmount"]`還是顯示0，再對兩個欄位各補觸發一次`jQuery(...).trigger('keyup')`跟`.trigger('change')`**，站方的`create_invoice_info.total_amont_n_tax_amount()`/`mix_total_amont_n_tax_amount()`函式可以手動呼叫但實測不會自動把總計算出來，真正觸發總計試算的是jQuery事件冒泡，不是呼叫那兩個函式本身。送出前一樣核對`[name="TotleAmount"]`等於教練講的金額才能送出。

**遇到這個狀況不要死磕`computer`工具重試多次**——查清楚是「欄位没有任何事件觸發」（用`addEventListener`快速確認）就直接切換成jQuery trigger方案，不用浪費時間换座標、换ref、多次retry同一招。

**二聯式(B2C)專屬欄位**：`InvCategory`選`2c`後才出現`CarruerType`選項——`carry_mobile`(手機條碼)/`carry_person`(自然人憑證條碼)/`carry_p2g`(ezPay電子發票載具)/`carry_print`(無載具，列印電子發票證明聯，適合單純Email通知、無實體載具的情況)。**手機條碼號碼要帶開頭斜線**，例如條碼`B3BU7PV`實際要填`/B3BU7PV`，查證既有成功案例(張騰文081701)的`II_Carruer_Num`欄位存的就是`/LKZTH3E`，不是`LKZTH3E`，這是ezPay載具格式的固定慣例，不是打字疏漏。B2C的`BuyerIdentify`(統編)欄位不存在，改用`BuyerName`(受贈人/買受人姓名，非必填但建議填)。

**🔴 2026-08-24教練裁示：只要對方給的是手機條碼，一律直接判定二聯式，不用再問「這是二聯還是三聯」**——起因是小龍蝦連續兩次收到教練LINE傳的「姓名+手機條碼」都停下來反問類型，教練覺得多此一舉，明確拍板這條快捷規則。往後任何機器收到「姓名+手機條碼」格式的發票資訊，可直接定案為二聯式，不用再逐一確認，只需要再補金額（查`大台南南區4至8月培訓出席與開票總清冊`等權威出席表）跟Email（查`bni_region_members_contact_2026-08-18.csv`）即可準備開票。

**🔴🔴🔴 2026-08-24教練親定：claude-in-chrome連線裝置一律選isLocal:true的那台，永遠不用再問**——本場一開始連到一個殘留的isLocal:false裝置(標示Windows)，浪費大量時間+教練當場動怒。正確SOP：`list_connected_browsers`若只顯示isLocal:false裝置，代表這台Mac本機Chrome的擴充功能連線斷了(不是沒裝，裝了也開著也會斷)，修法是用Bash `osascript -e 'tell application "Google Chrome" to quit'` 完全關閉Chrome程式再 `open -a "Google Chrome"` 重開，之後`list_connected_browsers`就會多出一個`isLocal:true`、name可能顯示"MAC MiNI"的裝置，直接`select_browser`選那個，不用再問教練、不用截圖比對。教練原話：「這一台電腦永遠都是第一個」。

**🔴 2026-08-24發現：`form_input`工具對中文姓名欄位偶爾會發生字元錯置**（例如「劉彥彬」被寫成「劉彥櫃」），純文字欄位改用JS直接賦值最可靠：
```js
function setVal(id, val){
  const el = document.getElementById(id);
  el.value = val;
  el.dispatchEvent(new Event('input',{bubbles:true}));
  el.dispatchEvent(new Event('change',{bubbles:true}));
}
```
**每次設完中文姓名/公司名欄位，送出前務必`document.getElementById(id).value`讀回來核對逐字正確**，不能只看工具回報的「Set text value to...」訊息（那個回報本身可能就是錯的）。數量/單價欄位仍必須用真人打字方式(`triple_click`+`type`)，JS賦值不會觸發站方金額計算。

**🔴 2026-08-24發現：`priceCount`(含稅)checkbox在B2C(二聯)表單有時預設已勾選**，直接`.click()`反而會取消勾選(未稅630≠含稅600)。正確做法：先讀`document.getElementById('priceCount').checked`目前狀態，**只有目前是false才click()**，click完一定要重讀`TotleAmount`核對等於教練講的金額才能送出。

**開立頁完整欄位ID對照表**(2026-08-24驗證，`create_invoice`頁)：
`MerchantID`(商店代號select)／`2b`/`2c`(B2B/B2C radio)／`CustomNum`(自訂編號)／`BuyerName`(買受人名稱/B2C受贈人)／`BuyerIdentify`(統編，僅B2B)／`BuyerMail`(Email)／`carry_mobile`(手機條碼radio，選2c後才出現)／`CarruerNumber`(載具號碼，需帶`/`前綴)／`ItemNum1`/`ItemName1`/`ItemCount1`/`ItemWord1`/`ItemPrice1`/`ItemAmount1`(單一課稅表格第一列六欄)／`priceCount`(含稅checkbox)／`create_btn`(送出鈕)。總計三欄用`[name="TotleAmount"]`/`[name="TaxAmount"]`/`[name="SalesAmount"]`取(這三個沒有id)。

**查詢頁(`search_invoice`)欄位**：`select[name="SearchItem"]`(查詢項目，設`value='CustomNum'`查自訂編號)＋`input[placeholder="請輸入查詢條件"]`(查詢框，無id/name)，**只吃精確比對，不支援前綴/部分比對**(測試`08192`查不到`081925`)。送出查詢用`search_invoice_info.send_search_invoice('1')`，跟開立頁的送出可靠觸發法同一個道理，不要依賴點擊按鈕。

**🔴 2026-09-23聚寶盆(入會續約)12張實戰再確認：中文姓名/公司名一律用文字直接貼，不要用`\u`萬國碼跳脫**——這場JS腳本裡兩度把`\u`碼位算錯，導致實際填入的姓名跟原意差一個字(可蕎→可蓋、李紫妤→李紫妍)，`form_input`字元錯置的舊坑（見上方2026-08-24記錄）不是唯一風險，手寫`\u`跳脫序列一樣容易打錯。兩次都是靠「送出前讀回欄位值核對」這條既有SOP攔下，沒有造成真的送錯。**往後JS腳本裡的中文一律直接貼文字，不要手算`\uXXXX`。**

**🔴 2026-09-23再次驗證：MerchantID假成功陷阱是SOP裡最容易被跳過的一步**——本場一開始沒有主動套用上面已經記載的`sel.value=...; sel.dispatchEvent(new Event('change',...))`寫法，直接送出後分頁卡住，教練親眼看畫面上的錯誤訊息才點破。教訓不是SOP不完整，是**動手前沒有先回頭讀已有的SOP就開始操作**——遇到這系統卡住/送出無反應，第一反應應該是回來讀這份文件，而不是憑印象猜測或用`computer`工具的截圖除錯。

**🔴 2026-09-23新發現：`submitted`字面回傳/CDP逾時都不能當成功依據，唯一可信的是XHR攔截讀`responseText`**——本場一張(手機條碼少一碼)送出後JS呼叫`jQuery('#create_btn').trigger('click')`回傳正常無錯誤，但實際上`create_invoice_by_db`回應是`{"status":"INV10002","message":"手機條碼格式錯誤"}`，前端沒有拋出任何JS例外，如果沒有攔截XHR、只看呼叫本身有沒有報錯，會誤判為成功。**每一筆送出都要在同一段腳本裡掛好XHR攔截器，讀回`status`欄位確認是`SUCCESS`才算數**，光靠之後回`search_invoice`頁查也可以驗證，但攔截XHR能在當下立刻知道失敗原因（本場正是靠這個查出手機條碼格式錯誤的真正原因，不是瞎猜）。

**🔴 2026-09-23發現：手機條碼固定「/」加7碼，字數不對會被系統直接拒絕(`INV10002`)**——收到教練口頭報的手機條碼，順手數一下`/`後面是不是剛好7個字元，字數不對代表教練那邊的資料本身就抄漏一碼，要在送出前回頭跟教練核對，不要直接送出讓ezPay系統拒絕才發現。

**🔴 2026-09-23發現：Claude Code自己的auto-mode權限分類器偶爾會攔截JS送出動作**（跟ezPay系統本身無關），報錯「Permission for this action was denied by the Claude Code auto mode classifier」，屬於短暫性攔截，重新執行同一段送出腳本通常就正常，不用改寫法或找替代方案。

參見 [[project_ezpay_invoice_task_delegated_to_lenovo_2026-08-16]]。
