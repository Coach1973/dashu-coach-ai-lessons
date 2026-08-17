---
name: reference-ezpay-bulk-invoice-scraping-procedure
description: ezPay發票查詢頁批次爬取歷史發票資料的可執行JS技巧(含分季查詢/分頁/alert攔截)，2026-08-17實測驗證可動
metadata: 
  node_type: memory
  type: reference
  originSessionId: ed21277a-b31b-465c-951d-965316ab4b7f
  modified: 2026-08-17T09:25:00.000Z
---

用途：抓取`inv.ezpay.com.tw`(帳號gtbctainan)過去所有發票歷史，供跨系統(如大樹教育培訓發票)核對統編用。本文件是2026-08-17在真實登入狀態下**逐步實測過**的技巧，不是憑印象寫的，任何機器(含聯想Windows的Claude Code/OpenClaw軍師)都可以直接照抄。

**前置**：教練需先在該機器的瀏覽器手動登入ezPay(跟BNI Connect CMS同款限制，登入狀態不跨機器同步)。

## 關鍵限制(兩層，容易搞混)

1. **單次查詢區間最長3個月**：超過會跳原生`alert('查詢期間最長以三個月為限')`卡住整頁，必須先執行 `window.alert = function(msg){ window.__lastAlert = msg; };` 覆蓋掉，否則自動化工具會卡在alert()上動彈不得。
2. **查詢起始日有下限**：2026-08-17實測，`2023-12-31`以前的日期會跳另一種alert『超過可查詢時間範圍』，即使區間本身沒超過3個月一樣擋。實測邊界是**2024-01-01**可查、更早不行(系統層級限制，不是資料真的不存在，但目前這個帳號目測資料本來就是從2024年初才開始累積)。**下次抓取時建議先用小區間(如當月)往回試探邊界，不要預設是2年前，我上次(2026-08-16)漏抓了2024-01~2024-07這5個月的61筆資料，就是因為沒有實際試探邊界、憑印象抓了「近2年」）**。

## 核心操作(F12開發者工具/瀏覽器自動化JS皆可執行同一段程式碼)

### 1. 先到查詢頁、覆蓋alert
```js
window.alert = function(msg){ window.__lastAlert = msg; console.log('ALERT:', msg); };
```

### 2. 找到日期欄位id(每次登入session可能不同，先查一次)
```js
[...document.querySelectorAll('input[type="text"]')]
  .filter(i=>i.offsetParent!==null)
  .map(i=>({id:i.id, name:i.name, value:i.value}));
// 找 name="StartInvDate" 跟 name="EndInvDate" 那兩個，記下它們的 id
```

### 3. 查詢觸發函式不是點按鈕，是呼叫全域物件方法
真正觸發查詢的是這行(按鈕id="search_btn"，onclick屬性寫死)：
```js
search_invoice_info.send_search_invoice('1');  // 參數是頁碼，'1'=第1頁
```
**不要用座標點擊按鈕**——實測按鈕的DOM ref容易在頁面重繪後失效，點擊沒反應但也不報錯，白白浪費時間；直接呼叫這個JS函式最穩定。

### 4. 完整的單一時間窗查詢+翻頁函式(2026-08-17實測可動的版本)
```js
window.__allInvoices = window.__allInvoices || [];

window.__extractRows = function() {
  const t = document.querySelectorAll('#show_search_result table')[1]; // 注意是第2個table(index 1)，第1個是空的容器
  if (!t) return [];
  return [...t.rows].slice(1).map(r => [...r.cells].map(c=>c.innerText.trim().replace(/\s+/g,' ')));
};

window.__getPagerInfo = function() {
  const txt = document.getElementById('show_search_result').innerText;
  // 千萬不要用「第X頁」這種pattern抓當前頁碼——畫面實際結構是「目前頁次第[1][2][3]頁/共3頁」，
  // 1/2/3是三個可點的頁碼連結擠在一起，regex會抓到頁碼連結的"1"而不是真正的當前頁，導致誤判只有1頁。
  // 只抓「共X筆」跟「共X頁」這兩個數字最穩，當前頁自己用迴圈變數追蹤就好。
  const mTotal = txt.match(/共\s*(\d+)\s*筆/);
  const mPages = txt.match(/共\s*(\d+)\s*頁/);
  return {total: mTotal? +mTotal[1] : 0, pages: mPages? +mPages[1] : 1};
};

window.__runWindow = async function(start, end, startFieldId, endFieldId) {
  $('#'+startFieldId).val(start);
  $('#'+endFieldId).val(end);
  search_invoice_info.send_search_invoice('1');
  await new Promise(r=>setTimeout(r, 1800));  // 至少1.5秒等AJAX回來，太快會抓到上一次查詢的殘留資料
  let info = window.__getPagerInfo();
  let collected = window.__extractRows();
  let page = 1;
  while (page < info.pages && page < 30) {
    page++;
    search_invoice_info.send_search_invoice(String(page));
    await new Promise(r=>setTimeout(r, 1500));
    collected = collected.concat(window.__extractRows());
  }
  const result = {start, end, total: info.total, pages: info.pages, gotRows: collected.length, rows: collected};
  window.__allInvoices.push(result);
  return {start, end, total: info.total, pages: info.pages, gotRows: collected.length};
};
```

### 5. 逐季呼叫，不要一次迴圈跑完
```js
await window.__runWindow('2024-01-01','2024-01-31', 'dpXXXXXX', 'dpYYYYYY');
```
**重要教訓**：把8~12個時間窗包在同一個`for`迴圈裡、一次性`await`執行，我第一次這樣做時整段在45秒逾時（瀏覽器自動化工具的單次JS執行有上限，通常在40~50秒），且逾時後`window.__allInvoices`是空的（迴圈中途被砍斷、狀態沒保留）。**改成每個時間窗獨立呼叫一次`__runWindow()`**（一次工具呼叫只處理一季）完全沒問題，雖然要多呼叫幾次，但每次都在時限內完成、資料確實累積進`window.__allInvoices`。

### 6. 抓完後合併匯出CSV並觸發下載(避免JS執行結果的文字回傳被截斷)
瀏覽器自動化工具把JS執行結果回傳成文字時，內容太長(超過約1000~2000字)會被自動截斷，看不到完整資料。**不要指望用JS回傳值直接拿到全部原始資料**，改成在頁面裡組好CSV字串後，用Blob+隱藏`<a>`標籤觸發真正的檔案下載：
```js
function csvField(s){ s = String(s??''); if (/[",\n]/.test(s)) return '"' + s.replace(/"/g,'""') + '"'; return s; }
const header = ['開立日期','發票號碼','商店代號','買受人統編','買受人名稱','發票金額','自訂編號_ezPay序號','發票狀態','上傳狀態','是否折讓','發票通知'];
let allRows = [];
for (const w of window.__allInvoices) allRows = allRows.concat(w.rows);
const lines = [header.map(csvField).join(',')].concat(allRows.map(r=>r.map(csvField).join(',')));
const csvText = '﻿' + lines.join('\n');  // 開頭BOM，Excel開才不會中文亂碼
const blob = new Blob([csvText], {type: 'text/csv;charset=utf-8'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url; a.download = 'ezpay_invoices_導出檔名.csv';
document.body.appendChild(a); a.click(); document.body.removeChild(a);
```
下載完成後，檔案會落在該機器的下載資料夾，直接用檔案系統工具讀取即可，不用再靠JS回傳。

## 2026-08-17實測結果(供比對驗證用)
分12個時間窗(2024-01-01~2026-08-17)查完，總計**238筆**(2026-08-16當時只抓177筆，少了2024-01~2024-07這段61筆，是漏抓邊界導致，不是資料變動)。已存檔`claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv`。

## 進階：批次查每張發票的「發票備註」欄(2026-08-17實測，跟上面的清單抓取是兩個獨立步驟)

清單抓取只拿得到`發票號碼`/`買受人統編`等欄位表，**買受人所屬會員分會+姓名要另外開每張發票的明細modal才看得到**(藏在「發票備註」欄，格式`分會-姓名`)。技巧：

1. **明細modal的token藏在「查看/補發」連結的`onclick`屬性**，格式`onclick="search_invoice_info.search_invoice_detail('一長串token')"`，每張發票的token不同、無法預先推算，必須先查到那筆發票在列表裡的那一列(用日期查詢)才能抓到token。
2. **頁面同時存在兩個modal，都叫`class="modal_div"`，容易抓錯**：`#invoice_detail`才是真正的發票明細(含備註欄)，`#notify_detail`是開立通知記錄(不含備註)。讀取時務必鎖定`document.querySelector('#invoice_detail .modal_div')`，不要用`document.querySelector('.modal_div')`(會抓到不確定是哪一個)。
3. **modal內容欄位是`<td>`標籤/值配對**，穩定的讀法是找`textContent.trim()==='發票備註'`的`<td>`，取它下一個`<td>`的`innerText`，不要用innerText整段regex(不同發票的HTML縮排/是否有作廢欄位會讓文字結構不一致，regex常抓錯)。
4. **modal內容是AJAX非同步載入，固定等待時間不可靠**：呼叫`search_invoice_info.search_invoice_detail(token)`後，內容不會立刻出現，實測固定等1.6秒常常抓到「上一筆殘留內容」。正確做法是**輪詢直到讀到的`發票號碼`欄位等於你剛剛請求的那筆**才算真的載入完成(最多等5秒)，讀完後點`.close`按鈕關閉modal再處理下一筆。
5. **⚠️長時間批次作業務必邊查邊寫檔，不要只累積在瀏覽器分頁的JS記憶體裡**——2026-08-17查108筆統編備註時，查到51筆後Chrome擴充功能連線中斷(教練閒置1.5小時觸發)，重新連線後整個分頁的JS執行環境已重置，`window.xxx`存的所有中間結果全部消失，只好從頭重查。改成「每查完一批(約10~12筆)就把JS回傳的資料直接寫進本機檔案」才安全，即使斷線重連，最多只需要補救最後一批。

**2026-08-17實測結果**：238筆篩到163筆B2B(買受人統編非空)，再依「同一統編只查一次代表性發票」去重到108個不同統編，全部查完存於`claude-brain/data/ezpay_invoice_remarks_108taxid_2026-08-17.csv`。

參見 [[reference_ezpay_invoice_issuing_procedure]]（單張發票開立SOP，跟本文件互補：一個是開新發票、一個是查歷史發票）。
