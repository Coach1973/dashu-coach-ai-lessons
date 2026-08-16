---
name: reference-ezpay-invoice-issuing-procedure
description: ezPay電子發票開立操作SOP，含自訂編號規則/品項代碼/含稅計算易錯陷阱/送出後查證方法
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7d4244d1-db9c-42f8-97ad-dc02499cbe41
  modified: 2026-08-16T13:59:03.921Z
---

操作對象：inv.ezpay.com.tw，帳號gtbctainan，商店固定「(337391376)BNI台南南區」。開立用`Invoice_issue/create_invoice`，查詢用`Invoice_issue/search_invoice`。

**登入狀態per機器**：跟BNI Connect CMS同款限制，換機器操作前教練要親自在那台電腦的Chrome重新登入一次ezPay，不會跨機器同步。

**查詢限制**：查詢日期區間最長3個月，超過會觸發原生`alert()`把整個分頁卡死，操作前先`window.alert=function(){}`覆蓋掉。查2年以上歷史要切成8個季度分批查。

**自訂編號規則**（教練親定）：當天日期MMDD+兩碼流水號，例如0816**01**=8/16第一張、0816**02**=第二張。開立前務必先查當天有沒有人已經開過，避免撞號。

**品項代碼**：`B02`/`BNI續約`（續約價，2026年約$26,800）、`B01`/`BNI入會`（新加入價，約$36,000~39,800，實際金額以教練當下口頭確認為準，不同會員/年度可能有差異）。

**發票備註是查會員身分的關鍵**：買受人名稱通常是公司行號，統編查不到會員本人是誰——會員姓名寫在「發票備註」欄，格式`分會名-會員姓名`（例：`真鑽-蘇志揚`）。要核對某個統編對應哪位會員，用列表的「查看/補發」連結開發票明細modal，備註欄就是答案。

**含稅計算易踩坑**：
1. 單價/數量欄位用`form_input`或直接改`.value`常常不會觸發站方JS的金額計算，要嘛用真人打字方式（triple_click選取+type輸入），要嘛JS呼叫`element.click()`（不能只改`.checked`屬性+dispatch `change`事件，那樣「含稅」checkbox勾了但金額還是照未稅算）。
2. 送出前務必讀`TotleAmount`欄位數字核對是否等於教練講的金額——2026-08-16當場踩過2次金額算錯（未稅$28,140而非含稅$26,800）都是這個原因。

**送出＋查證**：提交按鈕id是`create_btn`。點下去有時分頁會短暫卡住（像原生對話框或整頁reload），屬正常現象，等1~2秒再操作。**表單清空不等於發票真的建立成功**——2026-08-16曾發生表單清空但發票其實沒送出的狀況，正確做法是每次送出後都回`search_invoice`頁用自訂編號或買受人統編搜尋，確認發票真的存在（發票號碼/金額/狀態=已開立）才能回報教練完成。

參見 [[project_ezpay_invoice_task_delegated_to_lenovo_2026-08-16]]。
