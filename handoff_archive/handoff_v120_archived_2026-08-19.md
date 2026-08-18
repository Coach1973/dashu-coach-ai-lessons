# 軍師接力棒 · 2026-08-18 v120（Mac桌面版 Sonnet 5，讀跨機信箱接手ezPay培訓費發票，16張全部開立完成）

> 建立時間：2026-08-18 14:13 ~ 15:55（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v119（同機同日，已在主檔保留）
> 本棒主軸：**教練指示「讀跨機信箱，接手ezPay發票任務」，讀`cross-agent/outbox/2026-08/20260818-1516_lenovo-to-mac_ezpay-training-invoice-17-handoff.md`得知聯想那邊操作培訓費發票開立卡在原生彈窗+分頁凍結，教練裁示改Mac接手剩餘16張(1張林宜宏需重開+15張全新)。過程中意外抓到一個新的「假成功」陷阱——商店(MerchantID)下拉選單視覺上顯示已選第一個選項，但`selectedIndex`實際是-1，沒explicit設值送出會後端回傳「商店代號不可為空值」但表單仍清空、外觀看起來像成功。改用XHR攔截器逐張讀取伺服器真實回應+`search_invoice`複查，18張(含聯想已完成的2張)全部確認真實存在，發票號碼連號DQ92662303~DQ92662320。**

## 🎯 本場戰果

### 1. 🔴 瀏覽器裝置確認：3台connected browser，依系統提示走AskUserQuestion選對Mac本機
連線瞬間偵測到3台connected browser(2台Windows+1台macOS)，工具本身要求先問教練逐一列出選擇，避免案例60(連錯到Windows)重演。教練選"Browser 3(macOS,isLocal:true)"後`select_browser`切過去才開始操作。

### 2. 🔴🔴 新發現「假成功」陷阱：MerchantID下拉選單視覺已選≠真的選中
第一次送出林宜宏(081703)發票時，畫面顯示商店已選「(344031309)大樹教育顧問有限公司」、其餘欄位含稅計算都正確(稅14/銷售286/總計300)，送出後表單清空、看起來像成功，但回頭`search_invoice`查081703卻查無資料。用XHR攔截器直接讀取`create_invoice_by_db`的真實回應才抓到根因：`{"status":"INV10001","message":"商店代號不可為空值"}`——`document.getElementById('MerchantID').selectedIndex`實際是`-1`，`read_page`的accessibility tree跟肉眼看到的「已選中」都是假象。修法：送出前務必`sel.value='344031309'; sel.dispatchEvent(new Event('change',{bubbles:true}))`明確賦值，之後15張皆比照辦理、逐張核對`MerchantID`真實value後才送出，全部成功。已寫入`reference_ezpay_invoice_issuing_procedure.md`。

### 3. 🔧 送出按鈕可靠觸發法：`jQuery('#create_btn').trigger('click')`，非`.click()`
`document.getElementById('create_btn').click()`（含`computer`工具真實滑鼠點擊）在此系統測試中完全無反應(0筆新增XHR、0筆DOM變化)，改用`jQuery('#create_btn').trigger('click')`才穩定觸發送出。查詢頁`#search_btn`同款問題，改用直接呼叫`search_invoice_info.send_search_invoice('1')`最穩定。另發現送出成功後常見`Inspected target navigated or closed`的CDP錯誤——這其實是頁面reload的副作用，不是失敗訊號，回`search_invoice`查證即可。

### 4. 🎯🎯🎯 18張培訓費發票全部確認完成（2張聯想已完成+16張Mac本場完成）
商店固定「(344031309)大樹教育顧問有限公司」，品項`B03`/`BNI培訓`，含稅checkbox(`priceCount`)每張皆用`element.click()`確實勾選並核對稅額/銷售額/總計三欄吻合教練金額才送出。三聯式(B2B)13張走`BuyerName`/`BuyerIdentify`(統編)/`BuyerMail`+`InvoiceRemark`(格式「分會-姓名」)；二聯式(B2C)2張改走`InvCategory=2c`後才出現的`CarruerType`欄位——**發現手機條碼號碼要帶開頭斜線**(查證已成功案例張騰文081701的`II_Carruer_Num`存的是`/LKZTH3E`不是`LKZTH3E`)，康文彬(081717)比照填`/B3BU7PV`；傅恩平(081718)無實體載具改選`carry_print`(無載具-列印電子發票證明聯)。全部18張自訂編號081701~081718對應發票號碼DQ92662303~DQ92662320，逐張用XHR攔截器讀真實JSON回應(`status:"SUCCESS"`)+核對姓名/統編/自訂編號三項吻合才記錄完成，總表存於`claude-brain/data/ezpay_training_invoices_2026-08-18_18張完成清單.json`。

| 自訂編號 | 姓名 | 發票號碼 | 執行者 |
|---|---|---|---|
| 081701 | 張騰文 | DQ92662303 | 聯想 |
| 081702 | 陳佳玲 | DQ92662304 | 聯想 |
| 081703 | 林宜宏 | DQ92662305 | Mac(重開) |
| 081704 | 許朝竣 | DQ92662306 | Mac |
| 081705 | 顏淳峯 | DQ92662307 | Mac |
| 081706 | 陳淑玲 | DQ92662308 | Mac |
| 081707 | 柯朝陽 | DQ92662309 | Mac |
| 081708 | 張晴晴 | DQ92662310 | Mac |
| 081709 | 楊在珍 | DQ92662311 | Mac |
| 081710 | 楊博丞 | DQ92662312 | Mac |
| 081711 | 邱南寅 | DQ92662313 | Mac |
| 081712 | 宋映璇 | DQ92662314 | Mac |
| 081713 | 楊仁豪 | DQ92662315 | Mac |
| 081714 | 吳志煒 | DQ92662316 | Mac |
| 081715 | 薛如媛 | DQ92662317 | Mac |
| 081716 | 郭馨文 | DQ92662318 | Mac |
| 081717 | 康文彬 | DQ92662319 | Mac |
| 081718 | 傅恩平 | DQ92662320 | Mac |

## 📋 下一場直接開工任務
- ezPay培訓費發票18張任務本場結案，無延續待辦
- 承接v119未完事項：「真誠分會」架構問題(擱置中)、三機hook同步(ACER待處理)、賈維斯Phase2 9/1月度cron觀察

## 🔑 本場關鍵檔案索引
- `claude-brain/data/ezpay_training_invoices_2026-08-18_18張完成清單.json`：18張發票完整對照表
- `claude-brain/reference_ezpay_invoice_issuing_procedure.md`：新增MerchantID假成功陷阱/送出可靠觸發法/XHR攔截驗證法/手機條碼斜線前綴
- `cross-agent/outbox/2026-08/20260818-1516_lenovo-to-mac_ezpay-training-invoice-17-handoff.md`：聯想交接單原文
- 本場純瀏覽器+記憶檔操作，無程式碼commit（記憶檔更新將於本棒commit一併送出）
