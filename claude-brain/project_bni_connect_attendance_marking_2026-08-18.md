---
name: project-bni-connect-attendance-marking-2026-08-18
description: BNI Connect活動出席勾選任務首次在Mac上線，完整SOP+8場活動101人次標記結果+claude-in-chrome跨機連線陷阱
metadata: 
  node_type: memory
  type: project
  originSessionId: 7ed2146b-db6f-4aab-9f0f-32b45b9ab8c0
  modified: 2026-08-17T21:01:22.482Z
---

2026-08-18凌晨，聯想Windows操作BNI Connect活動出席勾選頁面反覆502/CDP卡頁，教練裁示改到Mac桌面版試試看。Mac完整跑完8場活動、101人次標記出席（含新增出席者），全部重新整理頁面驗證是伺服器持久化狀態，非暫存表單。

**Why**：教練用GitHub Pages公開統計表(`coach1973.github.io/BNI-Training`)當作簽到表真相源，判斷標準明定「系統已註冊≠已出席，一律依簽到表為準」；「會員沒事先線上註冊但實際出席，要用增加出席者方式加進系統」。統計表範圍目前只涵蓋真誠/真鑫/真鑽三個分會。

**How to apply**：下次任何機器要處理BNI Connect活動出席，直接套用本場摸出的SOP（見下），不用重新摸索。查無對應活動的幾筆（4/13進階MSP15人、6/12曜董DnA、6/8+7/6工作坊）仍卡著待教練裁示，見[[JUNSHI_HANDOFF_LATEST]] v119。

## 完整操作SOP

1. 活動清單頁 `appsManageEvents`：勾「顯示一個月之前的活動」+顯示100筆+用DataTables搜尋框打日期(如`13/04/2026`)或關鍵字找到eventId
2. 標記出席頁 `appsEventsRecordAttendance?eventId=X`：讀已註冊名單checked狀態，比對GitHub清冊
   - 吻合的：JS勾選checkbox + `jQuery('#recordAttendance_BTN').trigger('click')` 送出（**必須用jQuery trigger，普通`.click()`或computer真人點擊常常不觸發AJAX**）
3. 清冊有但系統未註冊的人：進 `appsEventsFindAddAttendee?eventId=X` 頁面
   - 選地區(大台南南區`23268`)+分會，姓名欄位打**「%」通配符**（教練提供的訣竅，可列出整分會會員）
   - `jQuery('#searchMembers').trigger('click')`：會導致**整頁顯示原始JSON**（系統本身AJAX拦截失敗的既有行為，不是bug），但JSON裡含完整分會會員名單+checkbox id，正好拿來用
   - 導回乾淨頁面，用JS動態建立`<input type=checkbox>`插入`editform`表單並勾選，`jQuery('#recordAttendance_BTN').trigger('click')`送出，一次新增多人+自動視為已出席
4. 每場結束後重新`navigate`載入頁面讀checkbox狀態，確認是伺服器持久化

分會ID對照：真富42515／真愛44080／真誠31215／真鑫44081／真鑽23528／真心31243／真拾31242／真美32932

**瀏覽器原生對話框**：「保存變更」confirm跳出時會卡住整個tab的JS執行緒（含read_page/javascript_tool），要嘛請教練手動點掉，要嘛在每個頁面操作前先執行`window.onbeforeunload = null;`預防。

## claude-in-chrome跨機連線陷阱（詳見試金石案例60）

`claude-in-chrome`連線的是「目前配對成功的瀏覽器」，不是「這段對話跑在哪台電腦」。教練用RustDesk遠端從Windows操作Mac時，若Mac的Chrome沒開過，擴充功能從未配對，`navigate`可能連到教練慣用的Windows Edge而非Mac本機——頁面渲染正常不代表連對裝置。**任何「跨機比較」「這台機器操作是否正常」類任務，動手前先跑`list_connected_browsers`確認`isLocal:true`且裝置是預期的那台。**

## 本場8場活動結果摘要

| 場次 | eventId | 結果 |
|---|---|---|
| 5/11初階MSP | 519188 | 26人出席(17打勾+9新增) |
| 4/13 MSP-進階 | 517941 | 教練先前已勾好11人吻合 |
| 6/11主題培訓 | 519187 | 15人出席(9打勾+6新增) |
| 6/15進階MSP | 524592 | 27人出席(10打勾+17新增) |
| 8/17主題培訓 | 524594 | 10人出席(全部新增) |
| 6/27臺灣年會 | 520453 | 10人出席(2打勾+8新增) |
| 6/28 DnA培訓 | 520454 | 4人出席(2打勾+2新增) |

查無對應活動：4/13進階MSP15人、6/12曜董DnA季度培訓15人、6/8簡報+PT工作坊2人、7/6引薦+1對1工作坊3人。
