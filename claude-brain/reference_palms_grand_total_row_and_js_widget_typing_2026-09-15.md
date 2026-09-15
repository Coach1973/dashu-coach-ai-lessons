---
name: reference-palms-grand-total-row-and-js-widget-typing
description: BNI Connect PALMS報表最後一列是官方總數列不能跟會員列相加；Angular Material/Draft.js類複雜輸入元件對合成打字無反應，要用日曆點擊或screenshot排錯
metadata:
  type: reference
---

## 1. PALMS摘要報告「總數」列陷阱

BNI Connect「分會-PALMS摘要報告」匯出的xls，最後一列固定是姓氏欄位寫死「總數」的官方彙總列，內容是該報表所有指標(來賓/引薦/TYFCB等)的BNI官方認證總計，**不是又一個會員**。

第一版解析腳本沒有排除這一列，把它跟其他真實會員列一起加總，導致每個指標都異常偏高(例如真鑽分會某一期來賓數，正確是356，誤加總數列後變成523)。用`vals[0] == '總數'`可以精準辨識該列並跳過，或直接讀取該列的值當作官方總數(比自己重新加總更可靠，因為BNI內部計算口徑有時跟表面欄位加總對不上，官方數字優先)。

**How to apply**：以後任何要解析PALMS報表(或其他BNI Connect匯出的xls)算總和，先檢查最後一列是不是「總數」，用官方總數列的值，不要自己重新對member列加總。

## 2. Angular Material 日期選擇器/Draft.js類複雜輸入元件，合成打字打不進去

這場對話連續在兩個不同網站(Meta Business Suite貼文編輯框、BNI Connect PALMS報表的日期輸入欄)遇到同一種現象：用`computer type`模擬打字，畫面上的值完全沒有變化(觸發`type`動作沒有拋錯，但欄位值/按鈕文字沒有跟著更新)。這類複雜JS框架的輸入元件(Angular Material datepicker、Draft.js富文本編輯器)通常只監聽框架內部的合成事件，不理會純鍵盤事件的模擬注入。

**修法**：
- 日期選擇器類：改用「點開日曆→切換年份選單(通常有一顆『switch to year view』的按鈕)→選年份(切換年份會保留原本顯示的月份)→用『Next month/Previous month』一次一步點擊並每次用`find`重新查詢當前月份標題核對，不要連續點同一個快取的ref好幾次而不驗證(這樣做過一次會亂跳，可能是DOM在動畫過程中重繪讓舊ref失效)→點選正確的日期格→用`find`確認按鈕文字已經真的變成期望日期後再往下一步」。
- 富文本編輯器類(如FB Business Suite的貼文內容框)：目前沒找到穩定的純文字/read_page排錯方法，卡住超過3次要停下來跟教練申請一次性截圖權限(案例已示範用AskUserQuestion問過教練)，不要盲目重試。

**How to apply**：往後遇到「用`computer type`打了字，但`find`/`get_page_text`確認畫面完全沒變化」，第一時間懷疑是這類框架元件排斥合成鍵盤事件，改用點擊式操作(日曆/下拉選單)取代打字，而不是重複嘗試同一種打字方式。
