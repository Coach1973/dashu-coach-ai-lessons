---
name: project-2026-07-09-full-session-summary
description: 2026-07-09整場session總結——bigtree場次更新→陸海空矩陣行銷評估→媒體資源中心建置→GitHub作品盤點封存→結繩領導學6站文案同步
metadata: 
  node_type: memory
  type: project
  originSessionId: cb7ca9a0-f6af-4595-a452-a688a54624cb
---

2026-07-09這場session橫跨多個主題，脈絡如下（詳細各自獨立記憶見Related）：

**1. bigtree（大樹小講）場次更新**：新增7/18線上讀書會（Zoom會議），7/22/29、8/1三場加註高雄場/臺南場地點徽章，地點顯示位置從獨立一行改成跟日期同行。過程中發現另一位助教同時推了手機版漢堡選單，用`git pull --rebase`順利合併未衝突。

**2. 陸海空矩陣行銷提案**：教練構想以大樹小講為中央廚房同步發布到FB/IG/LINE/Threads/乾淨世界/Dcard/Podcast。AI WebSearch查證後給出分階段建議（LINE最快可做、FB個人頁技術上做不到、乾淨世界/Dcard無官方API）。**教練說不急，先記錄方向**。詳見[[project_matrix_marketing_plan_2026-07-09]]。

**3. 媒體資源中心建置**：教練要用家用Amber私有雲（192.168.0.35）整合散落素材。過程中發生本場最大教訓——AI連續兩次憑網路查到的文件（可能是別型號）叫教練去點錯的選單找WebDAV，教練正面糾正「你該自我驗證」。AI改用PowerShell直接測試，10秒內確認：這台根本沒有WebDAV，內建SMB已經夠用。教訓寫入[[feedback_self_verify_before_directing_user]]與試金石案例43。最終在Amber建立PARA分類法+收件匣機制的資料夾骨架，教練明確拍板「只手動上傳，不開手機自動備份」。詳見[[project_media_resource_center_2026-07-09]]、[[reference_amber_nas]]。

**4. GitHub作品盤點與封存**：教練指出41個repo裡很多是早期不熟悉AI操作時Netlify測試整批誤同步的「無心插柳」。AI用GitHub API拉出完整清單並依最後更新時間分類，教練確認19個（2026-04-06同一天建立、93天未動）為閒置，AI用`gh repo archive`逐一封存並API驗證，Amber本地備份同步搬進封存子資料夾。詳見[[reference_coach_websites]]。

**5. 結繩領導學工作坊邀請頁6站文案同步**：新建workshop-richard（蔡曜隆）、workshop-lavi（LAVi）兩個個人化邀請頁（AI一度誤解「邀請人」指被邀請客人，教練糾正後修好），並把文案修正（6條長框、講師介紹句、願景句）同步套用到原本4個站台（bni-invite/bni-peipei/workshop-invite/workshop-peipei），嚴格保留各站原本的LINE按鈕跟頁尾掛名不動。全部6站zip部署上線並逐一驗證。詳見[[project_jiesheng_workshop_invite_personalized_2026-07-09]]。

**本場最大教訓**：有能力自己驗證時，不能叫教練當試錯的手腳——網路查到的文件只能當參考方向。這條已收進試金石案例43跟永久記憶規則。

Related: [[project_matrix_marketing_plan_2026-07-09]], [[project_media_resource_center_2026-07-09]], [[reference_amber_nas]], [[feedback_self_verify_before_directing_user]], [[reference_coach_websites]], [[project_jiesheng_workshop_invite_personalized_2026-07-09]]
