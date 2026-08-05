---
name: project-bni-chapters-public-launch-2026-08-03
description: BNI大台南南區9分會後台管理系統(bni-chapters)實況——2026-08-03深夜對外開通chapters.bymyway.com後，8/3~8/4密集迭代加了核心價值/常用連結/傳統與道德規範/參訪須知(線上vs實體分流)，10組帳號仍是預設密碼待改
metadata: 
  node_type: memory
  type: project
  originSessionId: a7a813d3-3d3a-47de-831f-20836ed149a6
  modified: 2026-08-05T01:37:40.225Z
---

`bni-chapters`是教練另一個對話框在2026-08-01建置的真實系統（Flask+SQLite，repo: `github_repos/bni-chapters`），這場對話之前完全沒被記錄進接力棒/HEARTBEAT，是靠git log現場查出來的——不是這場對話新建的。

**系統結構：**
- 本機跑在port 5064（不是預設值5063，.env明確覆寫；5063被另一套`jiesheng-report`系統占用，兩者曾造成混淆，查證時要注意）
- 根路徑「/」= 大台南南區分會總表（公開頁，9個分會：真誠sincere/真AI籌備會real-ai/真富true-rich/真愛true-love/真鑫/真鑽real-diamonds/真功夫籌備會real-kungfu/真樂齡籌備會real-age/真貴籌備會real-wealth）
- 「/admin」= 後台管理，總管理員(Admin)可管全部分會，每個分會也有自己獨立登入網址(`/admin/<slug>/login`)只能編輯自己範圍
- launchd常駐：`com.coach.bni-chapters-webapp`

**2026-08-03本場完成的事：** 教練要求把這套系統的網址列出來加進`coach1973.github.io/coach888/`，查證後發現系統本身沒問題，但從沒對外開通過（只有localhost）。已比照mentor100/namecard等既有系統的模式，申請`chapters.bymyway.com`：
- 建立新cloudflared tunnel `bni-chapters-app`（過程中發現cert.pem已過期，重新走OAuth登入才修好，見[[feedback_use_chrome_control_for_oauth_flows]]）
- DNS route + `com.coach.bni-chapters-tunnel` launchd常駐服務
- coach888新增第13/14項：`chapters.bymyway.com`(總表)、`chapters.bymyway.com/admin`(後台)，commit `a3c7cad`

**Why:** 教練想要「動嘴就能找到系統」，之前這套系統做完卻沒接上公開網址，等於白做——查證+開通這一步才是真正讓教練能用上的關鍵。

**How to apply:**
1. **7/29的靜態mockup草稿已過時**：`knowledges/2026-07-29_bni-nantai-mockup/`底下的`大台南南區_index.html`、`真誠分會_index.html`、`真AI籌備會_index.html`三個檔案，內容已經被灌進真正的`bni-chapters`資料庫當初始值（8/1那場做的），之後如果教練提到「大台南南區網站」，應該先確認是指這個真實系統(chapters.bymyway.com)還是那三個舊草稿，不要再對著舊草稿做修改。
2. **安全性待辦（尚未處理）**：全部10組帳號（總管理員+9分會）都還是建置時的預設密碼`Admin/88888`，現在系統已經對外公開，這組預設密碼理論上任何人都能透過`chapters.bymyway.com/admin/login`猜到——教練尚未裁示是否/何時要求各分會改密碼，下次提到這套系統應該主動提醒這件事。
3. 不要跟`reference_bni_connect_cms_structure`搞混——那是BNI官方的Connect CMS後台(bniconnectglobal.com)，這個`bni-chapters`是教練自己另外做的系統，兩者服務同一批分會但完全獨立。

**2026-08-04密集迭代（同一場對話延續）：**
- **核心價值**：從真誠分會零散1~2條佔位文字，統一改成BNI官方9大核心價值（逐字取自bnidahan.com.tw，後改用教練提供的官方定義+英文對照，含2條隱藏版「感恩/謙遜」），加上立體懸浮hover效果。後台的新增/刪除功能已完全移除（含後端路由），改唯讀顯示——因為這是官方固定內容，不該讓分會各自改動。`db.py`的`MAX_VALUES`從3→9。
- **常用連結**：導覽列新增「常用連結」按鈕（改成漢堡圖示樣式☰），點擊彈窗顯示紅綠燈看板/LINE AI小幫手/培訓行事曆，後來又加了教練陸續提供的6項BNI教育資源（FB貼文+4支YouTube+1集Podcast，YouTube標題用oEmbed API自動抓取，省去教練手動打字）。
- **六項傳統與道德規範**：歷經3次改版定案——一開始做成常用連結彈窗裡的文字區塊→教練嫌不夠正式改成獨立彈窗（左右雙欄）→最終定案為「分會之光」下方的**永久展示區塊**（不用點擊），並加上`chapters.show_traditions`欄位讓每個分會自己勾選開關。
- **參訪須知（重要，多次修正）**：教練要求依「線上/實體」分流顯示不同內容。**血淚教訓**：一開始用`status`欄位（active/forming）猜測實體/線上對應，結果錯了——真誠分會、真愛分會雖是`active`但實際是**線上**分會，真功夫/真樂齡籌備會雖是`forming`但實際是**實體**分會。教練逐一糾正後，正確名單是：**線上**=真誠／真AI籌備會／真愛／真貴籌備會（4個），**實體**=真富／真鑫／真鑽／真功夫籌備會／真樂齡籌備會（5個）。`status`(正式營運/籌備中)只代表分會成立階段，跟聚會是線上或實體是兩件獨立的事，不能互相推論。最終版：實體分會顯示「請著正式服裝/準備50張名片/20秒自我精彩簡介/入席費650元/分會地址(永康桂田酒店+Google地圖連結)」5張卡；線上分會顯示「使用ZOOM(附下載連結)/請著正式服裝/開鏡頭融入會議/20秒自我精彩簡介」4張卡。
- **響應式設計**：手機版導覽列文字連結整組隱藏，只留Logo(可點回首頁)+漢堡圖示常用連結按鈕+CTA按鈕；hero/section字級與間距手機版縮小。
- **差點出的包**：測試「勾選顯示/隱藏傳統區塊」表單時，用curl送出一個不完整的POST（漏了hero_title/hero_desc/about_desc等欄位），因為`update_chapter()`是整批覆寫，把真誠分會這幾個欄位直接清空了。當場發現+從`seed.py`原始種子資料查回正確內容補救，沒有造成永久損失，但這是**測試表單前一定要先讀出完整既有資料再送出**的教訓，見[[feedback_test_form_post_read_before_write]]。

Related: [[feedback_use_chrome_control_for_oauth_flows]]、[[reference_bni_connect_cms_structure]]、[[project_bni_three_chapters_vision_pending]]、[[feedback_test_form_post_read_before_write]]、[[feedback_dont_infer_unrelated_attribute]]
