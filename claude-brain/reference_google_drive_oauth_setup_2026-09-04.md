---
name: reference-google-drive-oauth-setup
description: Google Cloud Console(現改名Google Auth Platform)設定OAuth用戶端讓伺服器讀取Google Drive檔案清單的完整步驟+常見坑
metadata: 
  node_type: memory
  type: reference
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-03T21:37:42.350Z
---

2026-09-04 為 `event.bymyway.com/materials/admin` 建立 Google Drive 唯讀 API 存取，走完整套 OAuth 設定，記錄步驟與踩過的坑，之後任何專案要串 Google Drive/其他 Google API 都可以照抄。

**設定步驟（Google Cloud Console → 現在叫 Google Auth Platform）：**
1. console.cloud.google.com 建立新專案
2. 啟用對應 API（這次是 Google Drive API）
3. `/auth/branding` 頁面填應用程式名稱/支援信箱/開發人員聯絡信箱
4. **`/auth/audience` 頁面（不是branding頁）新增測試使用者**——這是最容易漏掉的一步，測試使用者跟品牌設定是兩個獨立頁面，只填品牌沒加測試使用者，授權時會直接跳 403 access_denied
5. `/auth/clients` 建立 OAuth 用戶端 ID，型態選「網頁應用程式」，重新導向URI**只能填在「已授權的重新導向URI」欄位（可以有路徑），不能填在「已授權的JavaScript來源」欄位（只能是裸網域，不能有路徑/斜線結尾，填錯會報「來源無效」）**
6. 拿到 client_id/client_secret 後，伺服器端寫 `/oauth/start`(導去Google同意畫面) + `/oauth/callback`(用code換token，`access_type=offline`+`prompt=consent`才會拿到refresh_token) 兩個路由
7. 教練本人點完授權連結、選對測試帳號、按「允許」，refresh_token 就會存進伺服器（這次存在 `workspace/credentials/google_drive_oauth.json`，.gitignore已排除）

**常見坑：**
- 帳號有多個Google帳戶登入同一個Chrome時，Cloud Console網址要帶 `&authuser=1`(或對應數字)才會切到正確帳號的專案，不然會看到「您需要額外存取權」的IAM錯誤
- Console頁面偶爾會出現「無法從www.gstatic.com載入JavaScript來源」導致頁面卡在骨架狀態(儲存/新增按鈕在DOM裡但沒hydrate)，錯誤訊息本身提示可能是「自動要求過多，Google暫時封鎖」——遇到這狀況先暫停自動化重複嘗試、等幾秒鐘、開新分頁重試，不要在同一頁狂點
- Google帳號選擇器(accountchooser)頁面的帳號選項用ref-based click有時不會觸發真正的導航，需要真人等級的座標點擊才會生效
- Drive API的folder listing只回傳直屬子項(不遞迴)，用`'{folder_id}' in parents and trashed = false`查詢，`fields=files(id,name,mimeType)`

**下載檔案內容**：`GET https://www.googleapis.com/drive/v3/files/{fileId}?alt=media` + Bearer token，對pptx這類非Google原生格式檔案，回傳的就是原始pptx(zip)位元組，可以直接`zipfile`解析`ppt/slides/slide1.xml`拿文字內容——但如果投影片首頁是整張圖片(AI生成封面)，XML裡不會有文字，要改抓`ppt/slides/_rels/slide1.xml.rels`裡的圖片關聯、取出`ppt/media/`底下的實際圖檔，用有圖片能力的工具親眼讀出標題文字(比硬上OCR更準，尤其是藝術字體)。

Related: [[project_materials_viewer_system_2026-09-04]]
