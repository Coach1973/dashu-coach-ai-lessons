---
name: reference_bni_connect_cms_structure
description: BNI Connect CMS後台網站ID索引與存取方法，教練BNI官方網站(大台南南區+5分會)維護用
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7aced64d-2909-4abb-aed9-aca35e4414c5
  modified: 2026-07-30T16:11:36.402Z
---

教練BNI Connect CMS後台：`https://www.bniconnectglobal.com/bnicms/v3/backend/website/list/regions`，帳號吳大樹，Taiwan, China國家層級下。

**區域網站**：大台南南區 Greater Tainan South，網域`bnitainan.com.tw`，網站ID `12261`（Settings頁：`/bnicms/v3/backend/website/view/12261`）。Settings欄位含Location/Area、Executive Director、Contact Telephone、Contact Email等，改完按Save即可，另有Publish按鈕發布上線，也有Delete連結（區域層級才有刪除功能）。

**分會網站**（清單：`/bnicms/v3/backend/website/list/chapters`）：

| 分會 | 網站ID | 建立者 | 備註 |
|---|---|---|---|
| 真富分會 | 25503 | 吳大樹 | |
| 真愛分會 | 26706 | 吳大樹 | |
| 真誠分會（舊） | 18487 | 吳大樹 | 重複記錄，Last Published停在2023/10/24，2026-07-31查出兩筆重複後教練指示保留最新一筆；此筆待處理（CMS無Delete/Unpublish可用，需教練決定改名標註或聯絡BNI客服） |
| 真誠分會（新，保留使用） | 18640 | 吳大樹 | 2025/10/05發布，這筆才是要用的 |
| 真鑫分會 | 28446 | 吳大樹 | |
| 真鑽分會 | 12262 | Outback Global | 建立者非教練本人，是第三方代理商帳號 |

**⚠️ 查無「真AI分會」**：2026-07-31查證CMS時，實際分會只有上述5個，沒有教練接力棒原先記錄的「真實AI分會」。教練當場澄清：這個分會他還沒在BNI Connect登記，且正式名稱應該是**「真AI分會」**（不是「真實AI分會」，是先前記錄名稱有誤/語音誤植），登記後才會出現在這份清單裡。之前做的網站草稿（`knowledges/2026-07-29_bni-nantai-mockup/`）若有用到「真實AI」這個名稱，之後要統一改成「真AI」。

**分會網站結構**：每個分會的Settings頁（`/bnicms/v3/backend/website/view/{ID}`）都有Pages（Home/Chapter Members/Gallery/News等，含Edit Page可編輯內容）+ Settings表單（Website Name、Contact Name/Number、Franchise Name、Contact Email等）+ Publish按鈕。**分會層級沒有Delete或Unpublish功能**（跟區域層級不同，區域層級才有這兩個按鈕），如果真的要下架或刪除分會網站，目前這個帳號權限做不到，要透過BNI客服或Outback Global代理商帳號。

**存取方法（給任何一台機器的Claude參考）**：
1. 不要開Claude自己獨立的瀏覽器分頁去操作（那是跟教練畫面隔離的假環境，即使教練登入了也不會同步，2026-07-31已實際踩過這個坑，教練形容為「平行時空」）
2. 改用`claude-in-chrome`工具，先呼叫`list_connected_browsers`確認有連線的瀏覽器（`isLocal:true`代表是這台機器本機的真實Chrome），再用`navigate`/`read_page`/`get_page_text`/`find`操作
3. 全程用純文字（accessibility tree／page text）讀取，不截圖——這類CMS表格/表單頁面的DOM結構完整，文字讀取比截圖辨識精準、快、且Token消耗遠低於影像辨識
4. 登入本身教練要在該機器的Chrome親自輸入帳密完成（AI不可代打，見[[feedback_password_boundary_vs_courier_resolution]]），這是每台機器每次都要有的物理動作，不是記憶檔能取代的
