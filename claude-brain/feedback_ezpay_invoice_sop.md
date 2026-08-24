---
name: feedback-ezpay-invoice-sop
description: 教練說「開票」「開發票」時立刻啟動的ezPay電子發票開立SOP——跟網頁推SOP同款設計，一步到位不用每次重找線索
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e15817d4-1997-4a92-8dde-f4de975df4aa
  modified: 2026-08-24T08:18:47.570Z
---

教練說「開票」「開發票」「幫我開＿＿的發票」= 啟動本SOP。

**Why:** 2026-08-24教練當場點名「就像網頁推，要有一個完整的SOP，不然每次開發票都重新找線索，浪費我的時間跟好心情」。本場光是「連上正確的瀏覽器」這一步就卡了半小時、教練連續動怒3次，事後查證發現：連線裝置選錯、欄位ID每次重找、含稅checkbox陷阱等，過去都各自留在零散的對話記錄裡，沒有整理成一份能一次照做到底的清單。這份SOP的存在，就是不讓教練再為同一件事第二次生氣。

**How to apply:** 聽到觸發詞，不用問「要不要做」，直接照下列六步驟走。

---

## 開票 SOP

### 第零步：資料是否齊全（缺一個都不能開）

每個人需要：①姓名 ②分會/公司 ③類型（二聯 or 三聯）④買受人資訊（二聯：手機條碼**要帶`/`前綴**，或「無載具僅Email」；三聯：公司抬頭+統編）⑤Email ⑥金額 ⑦自訂編號

- 缺類型：**教練2026-08-24裁示「只要給的是手機條碼，一律直接判定二聯式，不用再問」**——收到「姓名+手機條碼」格式可直接定案二聯，不用往返確認
- 缺Email/金額：先查`bni_region_members_contact_2026-08-18.csv`（BNI 94人現任會員庫）+ 當期「培訓出席與開票總清冊」權威表，自己查得到就不要問教練
- 自訂編號規則：當天日期MMDD+兩碼流水號（例：0824**01**）。**開票前務必先查當天有沒有人已經開過**（查詢頁搜自訂編號前綴），避免撞號

### 第一步：確認瀏覽器連線裝置（本場最大坑，必做）

```
list_connected_browsers
```

- **只接受`isLocal:true`的裝置**（name通常顯示"MAC MiNI"）。教練親定：「這台電腦永遠都是第一個」，不用再問教練要選哪個
- 若只看到`isLocal:false`（顯示Windows等），代表這台Mac本機Chrome的擴充功能連線斷了——**不是沒裝，是斷線**，修法：
  ```bash
  osascript -e 'tell application "Google Chrome" to quit'
  sleep 3
  open -a "Google Chrome"
  sleep 3
  ```
  重開後再跑一次`list_connected_browsers`，會多出`isLocal:true`的裝置，`select_browser`選它
- 連上後用`navigate`到`Invoice_issue/create_invoice`，`get_page_text`確認畫面顯示「bymyway您好」且看得到完整表單（不是登入頁）。**若是登入頁，請教練在這個視窗親自登入一次**（帳密AI不可代打），不要自己另開分頁或用其他瀏覽器工具測試——那些教練都看不到，只會製造更多混亂

### 第二步：填表（欄位ID已固定，不用每次重找）

先設定JS環境（每次換頁都要重設，alert override是per-page的）：
```js
window.alert=function(){};
window.confirm=function(){return true;};
const sel = document.getElementById('MerchantID');
sel.value = '344031309';  // 培訓費固定商店代號，BNI入會/續約用337391376
sel.dispatchEvent(new Event('change', {bubbles:true}));
```

**中文姓名/公司名欄位一律用JS直接賦值**（`form_input`工具對中文字偶爾會錯置字元，2026-08-24實測「劉彥彬」被寫成「劉彥櫃」）：
```js
function setVal(id, val){
  const el = document.getElementById(id);
  el.value = val;
  el.dispatchEvent(new Event('input',{bubbles:true}));
  el.dispatchEvent(new Event('change',{bubbles:true}));
}
```
每次setVal完，**務必`document.getElementById(id).value`讀回來核對逐字正確**，不能只信工具的「Set text value to...」回報。

三聯（B2B）：`document.getElementById('2b').click()` → `setVal('BuyerIdentify', 統編)` + `setVal('BuyerName', 公司抬頭)`
二聯（B2C）：`document.getElementById('2c').click()` → `document.getElementById('carry_mobile').click()`（有載具時）→ `setVal('CarruerNumber', '/載具號碼')` + `setVal('BuyerName', 姓名)`（選填但建議填）

共同欄位：`setVal('CustomNum', 自訂編號)`、`setVal('BuyerMail', email)`、`setVal('ItemNum1','B03')`、`setVal('ItemName1','BNI培訓')`、`setVal('ItemWord1','式')`

**數量/單價欄位JS賦值不會觸發金額計算，必須真人打字方式**：
```
triple_click ref(數量欄) → type "1"
triple_click ref(單價欄) → type 金額 → key "Tab"
```
（用`find`工具找當下的ref，每次換頁ref會變）

### 第三步：含稅勾選 + 送出前金額核對（不可省略）

```js
if(!document.getElementById('priceCount').checked){ document.getElementById('priceCount').click(); }
await new Promise(r=>setTimeout(r,500));
({
  TotleAmount: document.querySelector('[name="TotleAmount"]').value,
  ItemAmount1: document.getElementById('ItemAmount1').value
})
```
**`priceCount`有時預設已勾選，直接click()反而會取消勾選**（未稅630變成不等於含稅600）——一定要先讀`.checked`現況，false才click，click完重讀`TotleAmount`確認等於教練講的金額，對不上絕對不能送出。

### 第四步：送出

```js
jQuery('#create_btn').trigger('click');
```
（純`.click()`或真實滑鼠點擊都不保證觸發，唯一穩定方法是jQuery trigger）送出後畫面常會reload、JS執行環境中斷報錯（`Inspected target navigated or closed`），**這是常見的成功徵兆，不是失敗**，不用慌。

### 第五步：查證（每張都要，缺這步不算完成）

換頁到`Invoice_issue/search_invoice`：
```js
window.alert=function(){};window.confirm=function(){return true;};
document.querySelector('select[name="SearchItem"]').value = 'CustomNum';
document.querySelector('select[name="SearchItem"]').dispatchEvent(new Event('change',{bubbles:true}));
const box = document.querySelector('input[placeholder="請輸入查詢條件"]');
box.value = 自訂編號;
box.dispatchEvent(new Event('input',{bubbles:true}));
search_invoice_info.send_search_invoice('1');
```
`get_page_text`確認查到1筆、狀態「已開立」、姓名/金額/自訂編號都對得上才算這張真的完成。**這個查詢框只吃精確比對，不支援前綴/部分搜尋**，一次只能查一個自訂編號。

多人一起開時，重複第二~五步，自訂編號自然遞增（081925、081926...）。

---

**鐵律：第三步的金額核對、第五步的查證，兩個都不可跳過。「表單清空」不等於「發票真的建立成功」**——2026-08-16曾發生表單清空但發票其實沒送出的真實案例，只看表單狀態會漏掉這種假成功。

**鐵律：第一步的裝置確認每次開票都要做，不能假設連線還在**——本場開到第8張時連線一度整個斷線歸零(`list_connected_browsers`回傳空陣列)，等幾秒重試通常會自動恢復，不需要教練介入。

相關記憶：[[reference-ezpay-invoice-issuing-procedure]]（欄位ID完整對照表+更多技術陷阱細節）、[[feedback-web-push-sop]]（同款設計的姊妹SOP）
