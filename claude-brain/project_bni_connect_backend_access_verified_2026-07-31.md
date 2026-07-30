---
name: project_bni_connect_backend_access_verified_2026-07-31
description: BNI Connect官方網站CMS後台已驗證教練帳號可編輯，Claude可透過claude-in-chrome直接操作管理
metadata: 
  node_type: memory
  type: project
  originSessionId: 7aced64d-2909-4abb-aed9-aca35e4414c5
  modified: 2026-07-30T16:11:14.114Z
---

2026-07-31教練登入BNI Connect CMS後台（bniconnectglobal.com/bnicms/v3），Claude透過`claude-in-chrome`瀏覽器擴充功能連上教練本人已登入的真實Chrome（不是Claude自己另開的隔離分頁），確認可讀取並編輯：
- 大台南南區（區域層級）網站設定：地址/執行總監/聯絡電話/Email等，Settings表單+Save可用
- 分會層級（chapters）：真富/真愛/真誠(重複2筆)/真鑫/真鑽，共5個真實分會，每個分會都有Pages(可編輯頁面內容)+Settings(可編輯聯絡資訊)
- 全程用DOM/accessibility tree純文字讀取（`read_page`/`get_page_text`/`find`）操作，沒有截圖，Token消耗屬文字級而非影像級

過程中一度用Claude自己獨立的瀏覽器分頁去開BNI Connect，教練登入後Claude那邊仍顯示session invalid——因為那是兩個不同的瀏覽器工作階段（「平行時空」，教練原話），教練當場糾正「同樣的事情你不要在背景執行，你得讓我肉眼看得到」。改用`claude-in-chrome`連上教練本機真實Chrome後才真正同步，教練確認畫面上出現綠色圖示代表接管成功。

具體站台ID索引見[[reference_bni_connect_cms_structure]]。

**Why**：教練理念「動嘴就能讓AI做事」的具體驗證——證明AI特助能實際接管教練對外官方網站的日常維護（改地址/電話/聯絡人/分會董事會等），不只是內部工具開發。教練原話：「這樣對於我的理念——我只要動嘴，就可以讓AI做事——有很大的進度跟幫助。」

**How to apply**：之後教練口頭交辦「BNI網站改XX」，可直接用`claude-in-chrome`操作，不需要教練自己動手改，改完發布前口頭提醒一聲即將上線即可（不用每個小欄位都停下來問可不可以，教練已明確授權這個工作流程）。但**登入狀態是per瀏覽器/per機器**，教練換到聯想或宏碁電腦時，那台機器的Claude需要：①教練在那台機器的Chrome親自重新登入一次BNI Connect（帳密只能教練自己輸入，AI不可代打，見[[feedback_password_boundary_vs_courier_resolution]]）②那台機器要有claude-in-chrome擴充功能並連線。這兩件事本身不是「記憶」能解決的，是每台機器每次要用時的物理動作；但**操作方法本身**（哪裡有Settings、哪裡有Pages可編輯、Token怎麼省）已經寫進[[reference_bni_connect_cms_structure]]，透過.claude/projects記憶庫的git同步，三機的Claude都能讀到同一套SOP，不用重新摸索。
