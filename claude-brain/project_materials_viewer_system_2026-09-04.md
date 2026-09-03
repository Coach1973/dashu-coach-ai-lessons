---
name: project-materials-viewer-system
description: 教練課程教材線上觀看系統(event.bymyway.com/materials/)完整架構與狀態，2026-09-04從零建置
metadata: 
  node_type: memory
  type: project
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-03T21:37:59.834Z
---

教練要做一個「PPT/PDF上傳雲端、學員可線上觀看不用下載」的系統，2026-09-04 一次對話內從構想到完整上線。

**架構**：不自建轉檔/儲存管線，檔案留在教練Google Drive，靠Google Drive自己的embed viewer渲染（`https://drive.google.com/file/d/{id}/preview` 單檔嵌入，`https://drive.google.com/embeddedfolderview?id={id}#grid` 整個資料夾嵌入瀏覽器），我方只存檔案ID+標題於 `event-signup/event.db` 的 `materials` 表。

**兩個網址（2026-09-04教練發現舊版沒拆分才补）**：
- `event.bymyway.com/materials/admin` — 教練自己的後台：新增教材(貼Drive分享連結，自動判斷是單檔還是資料夾)、勾選要公開哪些(checkbox清單)、刪除、展開資料夾成個別檔案卡片
- `event.bymyway.com/materials/` — 學員看的乾淨頁面，只顯示 `visible=1` 的項目，沒有任何管理控制項

**Google Drive OAuth整合**：教練用 seabiscuitclub@gmail.com 帳號完成一次性授權(唯讀drive.readonly)，之後貼資料夾連結會自動用Drive API列出裡面每個檔案、各自建一張卡片(而非只嵌入整個資料夾瀏覽器)。授權設定細節見 [[reference_google_drive_oauth_setup_2026-09-04]]，憑證存 `workspace/credentials/google_drive_oauth.json`。

**現況數字**：教練上傳的「大樹教練精選資料庫」資料夾實際有42個檔案(PPT/PDF/圖片混合)，已全部匯入但**預設不公開**(資料夾整批匯入的教練特別要求，因為檔案沒特別篩選過)；其中11份原本是純英文檔名(AI生成簡報)，已逐一讀取投影片首頁封面圖確認正確中文標題並改名(因為封面標題是畫在圖片裡不是文字，靠親眼讀圖不是OCR)。

**待教練後續操作**：他要在 `/materials/admin` 的勾選清單裡自己選要公開哪幾份，勾完存檔後 `/materials/` 就會顯示那幾份給學員看。

**commit軌跡**：a4d967f06(OAuth整合)、4a1fd8aa7(公開/隱藏勾選機制)、5b4126ea2(拆分後台/前台)。

Related: [[feedback_public_admin_separation_default_2026-09-04]]
