---
name: reference-bni-connect-guest-report-navigation
description: BNI Connect「地區-查看來賓」報表正確導覽路徑+職業/公司欄位存在證明+SpreadsheetML(.xls)解析技巧
metadata:
  node_type: memory
  type: reference
  originSessionId: 454fbcb4-70a8-4a88-832e-8ef2cbc35b65
  modified: 2026-08-26T16:33:14.573Z
---

2026-08-26第一次抓BNI Connect來賓資料時，只用瀏覽器JS從畫面上讀到姓名/電話/email三欄就以為抓完了，教練糾正「connect的來賓是有專業別的，不可能沒有」，查證後發現漏了報表本來就有的公司/職業/分會欄位。

**正確報表位置**：`https://www.bniconnectglobal.com/web/secure/reportsHome#reportsactiontabcontentstructureregional`（舊版classic app，非新版React dashboard`/web/dashboard`），地區結構分頁下的`#ui-tabs-5`＝「查看來賓」。表單本身就有**Profession**篩選欄位，證明系統設計上職業就是必填欄位。新版dashboard的隱藏漢堡選單(`id="menu-appbar"`)在桌面寬螢幕下`display:none`且無法用CDP合成點擊觸發真正的React onClick（用`el.click()`直接呼叫DOM方法反而有效，CDP座標點擊在這套MUI/舊版混合的app上常失效）。

**教練親自匯出的完整報表格式**：副檔名`.xls`但實際是「Excel 2003 XML」格式(`SpreadsheetML`，`file`指令會判斷成`XML 1.0 document`)，不是`xlrd`/`openpyxl`能直接讀的傳統xls/xlsx二進位格式。正確解析法：用`xml.etree.ElementTree`讀`Worksheet/Table/Row/Cell`，**每個Cell可能帶`ss:Index`屬性代表欄位位置**（空白儲存格會被跳過不佔位，若忽略這個屬性直接依序取值，欄位會全部錯位）。header row跟data row都要用同一套「依`ss:Index`建dict」邏輯解析，再用header名稱對照，不能假設欄位順序固定。

實際欄位：姓氏｜名字｜公司｜**職業**｜電子郵箱｜電話｜地址｜城市｜國家｜**分會**｜訪問日期｜Invited By｜Type。這份報表也揭露大台南南區實際有8個分會（真富/真愛/真誠/真鑫/真鑽/真心/真拾/真美），比先前只認得的5個多3個。

**How to apply**：下次任何要重新抓/驗證BNI Connect來賓或會員資料，先假設系統畫面上顯示的欄位不是全部——這套系統很多報表(分會來賓報告/地區查看來賓等)欄位比UI直接呈現的更豐富，直接匯出.xls用上述XML解析法最保險，不要只靠JS讀畫面上看得到的幾欄就當作抓完。

Related: [[project_namecard_manual_trigger_matching_design_2026-08-27]]、[[reference_browser_bulk_extraction_parallel_calls_2026-08-26]]（前一次抓來賓資料用的瀏覽器技巧，本次發現該次遺漏了欄位）
