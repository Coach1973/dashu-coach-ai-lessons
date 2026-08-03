---
name: project-bni-chapters-public-launch-2026-08-03
description: BNI大台南南區9分會後台管理系統(bni-chapters)實況——已於2026-08-03深夜正式對外開通chapters.bymyway.com，取代7/29的靜態mockup草稿，10組帳號仍是預設密碼待改
metadata: 
  node_type: memory
  type: project
  originSessionId: a7a813d3-3d3a-47de-831f-20836ed149a6
  modified: 2026-08-03T17:48:02.035Z
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

Related: [[feedback_use_chrome_control_for_oauth_flows]]、[[reference_bni_connect_cms_structure]]、[[project_bni_three_chapters_vision_pending]]
