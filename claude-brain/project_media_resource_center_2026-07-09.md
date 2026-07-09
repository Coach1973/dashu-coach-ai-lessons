---
name: project-media-resource-center-2026-07-09
description: 教練「媒體資源中心／媒體倉庫」已在Amber私有雲建立初步框架並上線，含GitHub作品備份+活動存檔結構+收件匣機制
metadata: 
  node_type: memory
  type: project
  originSessionId: 16511bcd-5087-40ef-822c-1c9c29f266f9
---

2026-07-09，教練提出要建立「媒體資源中心」（媒體倉庫），把過去累積的素材（GitHub作品、大樹小講歷史紀錄、其他散落資料）整合到一起，方便日後創作取用，未來也讓AI能直接進去撈素材協作。同一天內從評估規劃一路做到實際建置完成。

**最終定案（已執行，非草案）**：

儲存位置：Amber私有雲（`\\amber-Coach\home\媒體資源中心`），不搬公有雲。多電腦存取用SMB（不是WebDAV，這台機器根本沒有WebDAV功能，過程教訓見[[feedback_self_verify_before_directing_user]]），Windows/Mac都能直接掛網路磁碟機，教練手機用Amber LiFE App也已實測遠端連線+上傳正常。詳見[[reference_amber_nas]]。

**教練明確的使用原則（2026-07-09親口拍板）**：
- **只手動上傳，不開手機自動備份**。原因：手機拍的照片/影片沒整理過、容量大，自動同步很快會塞滿Amber的500GB空間。這是教練主動評估後的判斷，不是AI的建議，AI原本建議開自動備份被教練否決並說明理由。

**資料夾結構（已建立，套用PARA分類法+日期優先命名慣例，查證來源見下）**：
```
媒體資源中心/
├── 00_索引.md（整個資源中心的地圖）
├── 01_品牌素材庫/（通用素材：Logo、教練照片——已去重篩選出10張照片+1個QR code）
├── 02_歷史活動存檔/（核心！每場活動一個「YYYY-MM-DD_活動名稱」資料夾，EDM/簽到表/名單/照片同場放一起）
├── 03_網站原始碼備份/（GitHub 22個活躍repo的本地鏡像；19個已閒置的搬進`_已封存_早期測試站(19個)`子資料夾）
├── 04_影音素材/（錄音、影片、Podcast母帶，等教練手動上傳）
├── 05_文案庫/（可重複使用的金句、開場白）
└── 06_待整理收件匣/（教練手動上傳但還沒決定歸類的東西先丟這，AI定期整理歸位）
```

**GitHub作品盤點結果（教練親自盤點，見[[reference_coach_websites]]）**：41個repo裡教練確認19個是早期不熟悉AI操作時Netlify測試站整批誤同步的「無心插柳」，2026-04-06同一天建立、93天沒動過。已用`gh repo archive`封存（GitHub原生功能，唯讀化不刪除，隨時可解封），AI逐一用API驗證`archived:true`為真，Amber裡對應的本地備份也同步搬進封存子資料夾。剩22個活躍，其中9個用途需教練補充說明。

**尚待進行**：
- 教練整理完D槽/Mac/Acer散落資料後，再協助分類搬進對應資料夾（教練說這部分他要自己先整理出乾淨的資料夾再給AI搬）
- 9個「待補充用途」的repo確認後更新分類

Related: [[reference_amber_nas]], [[reference_coach_websites]], [[project_matrix_marketing_plan_2026-07-09]], [[feedback_self_verify_before_directing_user]]
