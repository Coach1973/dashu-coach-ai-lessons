# 專案卡：大樹小講（bigtree-tw）

- **🔴 詞彙（教練 2026-10-06 糾正、10/07 校對）**：「**官網**」＝大樹教育官方網站 **https://www.bymyway.com/**（repo `bymyway-website`，頁尾／署名用它）。**大樹小講網站**＝https://bigtree-tw.netlify.app（場次列表站，官網的「查看完整活動列表」連到它）——**不叫官網**。**活動報名系統**＝event.bymyway.com。三個是不同東西，對教練講話時不准混用。
- **場次狀態（10/07 查證）**：10/7、10/8 兩場（`bigtree-1007`／`bigtree-1008`）已取消（event.db `status=cancelled`），提醒與巡檢程式都已改成不理取消場次。`ema1017`（中華網紅協會零基礎學AI課 10/17 台北，獨立活動頁 event.bymyway.com/curated/ema1017/）在 event.db 登記為 `site=bigtree`，但**沒列在大樹小講網站**；是否要列上去是教練的內容決定，教練沒說就不動，巡檢每週只提一次。

- **🎯 owner：Hermes**（2026-08-31教練拍板，網站內容維運類任務預設交Hermes，完整操作手冊見`knowledges/2026-08-31_大樹小講四場活動維運SOP_備援指令給Hermes.md`；軍師只接需要JS/程式化select/截圖的BNI Connect等第三方後台任務）
- **repo**：`/Users/bymyway/github_repos/bigtree`（分支 main）
- **正式站**：https://bigtree-tw.netlify.app
- **部署型態**：🔴 Netlify 手動 zip 推型——改完先 GitHub commit，**教練親口說「推」才部署**（zip + API，走 netlify_deploy_guard 流程）
- **連動鐵律**（教練 2026-08-11 欽定）：新增/修改場次，後台 `event-signup/event.db` 的 events 表**必須同一輪同步更新**（含 start_time，同日多場次路由靠它）
- **報名管線（三路並行，fire-and-forget）**：
  1. `sme-register-fn.netlify.app`（舊版通知，觀察期後要拔）
  2. `xiaolongxia-notify.netlify.app`（轉發佩佩老師）
  3. `event.bymyway.com/api/register`（大樹小講網站雙寫落地 event.db + LINE 推播教練，2026-08-14 起）
- **深連結**：`?session=場次名&slot=晚半` 可預選場次（同日多場次要帶 slot）
- **教練特別交代**：場次一律顯示具體時間（14:00-16:30），不用早/午/晚/夜/全日代稱；8/25 台南場報名成功畫面要顯示匯款提示
- **近期場次**：8/21 金門西浦頭（60人）、8/22 金門向陽吉第、8/25 台南三道門午/晚兩場、8/26 高雄（古典音樂×AI，$100）、8/28 嘉義微論壇、9/23-24 台中微論壇
