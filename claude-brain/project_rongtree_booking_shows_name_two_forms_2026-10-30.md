---
name: project-rongtree-booking-shows-name-two-forms-2026-10-30
description: 榮樹下官網預約改成直接顯示預約人姓名；「預約表單」和「來賓資料表」是兩張，教練以為填了預約就是填了資料表
metadata:
  node_type: memory
  type: project
  originSessionId: 2007a746-146d-46f9-a412-c018e0eb3d3f
  modified: 2026-10-30T12:58:51.722Z
---

2026-10-30 教練說張瓊方「明明有寫」卻在前置作業與來賓卡後台看不到。查到：她填的是「我要預約」表單（留資料後台 18:21:14 那筆），第二張「來賓資料表」(/rongtree/guest/<form_token>，故事＋照片）沒填。當時預約人姓名只存在私人備註，所以公開清單寫「待確認」；來賓卡後台只列交了資料表的人。

已改（workspace d860a3224、rongtree 6cbe817）：
- `coach_schedule_view.book(..., guest=)`：官網預約把姓名寫進 guest（單位、電話仍只放私人備註）
- `/api/rongtree/hold` 回應附 `form`，成功畫面出現「下一步：填寫來賓資料表 →」，巴哈群通知也附網址
- 來賓卡後台 `/rongtree/a/<代碼>` 最上面加「接下來的訪談」：已預約／已填寫資料表狀態
- guest 欄位空時從標題「榮樹下訪談：某某」讀名字（巴哈登記的趙敏玄就是這樣）

**Why:** 教練要的流程是：預約→看得到是誰→發資料表→填完自動標已填。兩張表分開又沒講清楚，就會以為系統漏了。
**How to apply:** 教練說某來賓「填了卻沒出現」時，先分清楚是哪張表（works_contact_leads 是預約／留資料，rongtree_guest_forms 才是資料表），回話時用「預約表單」「來賓資料表」兩個名稱，不要說「她沒寫」。相關：[[project-rongtree-booking-hold-and-saturday-930-2026-10-23]]
