---
name: project-fb-fanpage-marketing-automation-2026-08-27
description: 教練交辦未來待辦——多個FB粉專需要AI操作瀏覽器，把大樹小講等活動現成的EDM/文案/照片自動發到各粉專宣傳，活動結束後也發現場照片；教練會陸續提供粉專名單，目前尚未開始執行
metadata: 
  node_type: memory
  type: project
  originSessionId: 65db632c-0f23-4fd8-aaf3-3f247ae2fd81
  modified: 2026-08-27T01:40:18.495Z
---

2026-08-27教練口頭交辦（尚未給粉專名單，屬於「先記著，之後陸續講」的待辦）：

教練原話大意：「我會陸續告訴你有哪幾個粉絲頁，需要你開始幫我寫粉絲頁文案，
建立自動化流程。因為我辦的活動多（像『大樹小講』裡面有那麼多活動），每場
活動都有現成的文案、照片和EDM題材。你可以操作我的網頁，看用什麼方式幫我
把EDM和行銷文案貼上去，發到各個FB粉絲頁做宣傳；活動結束後也可以發現場
照片。」

**現況（2026-08-27）**：教練尚未提供具體粉專名單，這是「記住、之後陸續
補齊」的階段，還不能真的動工——缺三個必要輸入：①哪些FB粉專（帳號/頁面
名稱）②AI操作這些粉專的權限方式（教練本人登入後用claude-in-chrome操作？
還是Facebook粉專管理工具的API存取權杖？）③素材庫的實際位置（[[project_bigtree_session_admin_backend_2026-08-23]]
提到的archive/歷史講座紀錄頁EDM圖片、bigtree repo裡的speakers-2026/等既有
文案照片，是否就是要用的素材源頭）。

**已知可用的素材基礎**：
- `bigtree` repo的`archive/大樹小講_歷史講座紀錄.html`：EVENTS陣列已有多場
  活動的宣傳圖(img欄位，位於`archive/edm/`)+完整文案(desc欄位)，格式現成
- 每場活動的SESSION_DATES資料（topic/venue/address/transport）可以組成
  貼文骨架
- 活動花絮輪播的現場照片(如`photos-carousel-0729/`)可作為活動後貼文素材

**Why**：教練辦活動頻率高（大樹小講/AI微論壇/結繩領導學等系列），現有
每場活動的文案/EDM/照片在完成後就沒有再被拿去做二次宣傳曝光，教練希望
把這些已經存在的素材自動化推廣出去，擴大觸及，而不是要求AI從零生成
全新素材。

**How to apply**：
1. 下次教練提供具體粉專名單時，第一步先確認上述三個必要輸入（粉專清單/
   操作權限方式/素材對應規則），不要在資訊不全時就開始寫程式碼
2. 操作真實FB帳號發文屬於「發送/發布公開內容」等級的動作，依安全規則
   需要教練逐次或一次性明確授權後才能執行貼文動作（不是單純唯讀查詢），
   落地前記得跟教練確認清楚每個粉專的發文頻率/審核方式期待
3. 優先評估用claude-in-chrome操作教練已登入的真實瀏覽器完成貼文（比照
   [[feedback_use_chrome_control_for_oauth_flows]]的既有模式），而非額外
   申請FB Graph API權杖（除非教練明確要走API路線）

Related: [[project_bigtree_session_admin_backend_2026-08-23]]（素材主要來源
bigtree系統）、[[feedback_browser_automation_ai_should_complete]]（教練對
瀏覽器自動化的一貫期待：卡住要精準定位障礙點而非整任務轉手動）
