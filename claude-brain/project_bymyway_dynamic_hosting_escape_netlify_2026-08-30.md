---
name: project_bymyway_dynamic_hosting_escape_netlify_2026-08-30
description: 教練確認的新方向——用event.bymyway.com即時讀取git repo+DB動態渲染取代Netlify手動部署，逐步脫離部署次數限制
metadata: 
  node_type: memory
  type: project
  originSessionId: 4df163f9-7212-4a42-948a-b7105107ac31
  modified: 2026-08-30T08:46:38.522Z
---

教練2026-08-30拍板：大樹小講（bigtree）、AI微論壇（半天制/兩天制兩條系列）從Netlify逐步移到自架的`event.bymyway.com`，**目標是完全不用再管Netlify部署次數**，GitHub Pages＋Netlify暫時保留同步、穩定後才退場。教練原話：「這樣的話就漸漸脫離Netlify的依賴，我們可以自主地來做這些事情，不用在那邊計算次數了」——明確肯定這個方向，非單次任務。

**技術做法（已驗證上線，可複製到其他Netlify站台）**：
不複製一份新內容，是在`event-signup`這支既有Flask app（本來就在跑`event.bymyway.com`）裡加路由，請求當下直接讀取對應github_repos的原始index.html＋圖片，需要場次資料的（如bigtree）額外疊上`event.db`即時查詢結果（沿用`bigtree_publish.py`既有的`read_sessions`/`render_session_dates`函式，不重複造輪子）。改DB或改repo原始碼都立刻反映在bymyway版本，**完全不需要「發佈」這個動作**，等於零成本無限次更新。

**網址命名鐵律（教練當場糾正過一次才定案）**：網址代表「活動格式/系列」，不代表某一次的地點或年份——跟`ai-talk-tw.netlify.app`過去台南場直接被嘉義場覆寫內容是同一套邏輯：
- `event.bymyway.com/bigtree/` — 大樹小講（多場次矩陣，DB驅動）
- `event.bymyway.com/ai-forum/` — 兩天制系列（目前台中9/23-24，之後10/7-8換台南場**沿用同一網址**，舊的變歷史紀錄）
- `event.bymyway.com/ai-talk/` — 半天制系列（目前仍是8/28嘉義場內容，教練提供另兩位講師(凌榆舜/李明燦)完整資料後要改成9/22台南場，8/28內容依既有慣例封存到頁面下方當歷史紀錄，不刪除）

**安全設計**：新增的`_serve_repo_file()`共用函式擋掉`.git`與不相關的草稿資料夾（如bigtree repo裡的biz-gym），靠Werkzeug `send_from_directory`內建防目錄穿越，不用自己重寫。

**Why**：Netlify手動zip部署每次扣15點額度，過去多次因為小改動（改個時間、拿掉一段文案）就要走git commit+推GitHub+打包+呼叫API的完整流程，且有嚴格的「教練親口說推才部署」SOP擋著，任何小修改都要等確認。改成bymyway動態渲染後，這類小改動可以直接改DB或repo原始碼，立刻生效，不再消耗Netlify額度也不用等教練確認部署——但GitHub Pages/Netlify正式站仍會保留一段觀察期才退場。

**How to apply**：之後教練提到任何現有Netlify站台想要「不受部署次數限制」「隨時能改」，優先考慮比照這套模式（讀活repo+視需要疊DB即時渲染，架在既有的event.bymyway.com或類似已有launchd看護的Flask app底下），不需要為每個新站台申請新子網域/新Cloudflare Tunnel/新launchd（那樣反而增加了「服務被遺忘」的風險，見[[reference_bymyway_subdomain_530_missing_launchd_2026-08-29]]同類教訓）。

**同場後續擴充（教練當場追加）**：教練確認方向後緊接著要求盤點「BNI相關、常用的」Netlify站台一併搬過去，已完成兩個：
- `event.bymyway.com/bni-traffic/` — 紅綠燈看板（BNI Connect PALMS報表上傳分析工具，純client端CDN依賴，零本機資源，最簡單的一種）
- 同步把`bni-chapters`資料庫（`chapter_links`表）9個分會的「紅綠燈看板」「培訓行事曆」連結全部改指向新網址（`chapters.bymyway.com`每個分會頁面的常用連結彈窗會顯示這兩條）
- `bni_tainan`小幫手（BNI大台南南區LINE小幫手）的`AGENTS.md`（4處member-facing連結）+`knowledge/tainan_calendar.md`來源引用+`scripts/sync_calendar.py`實際抓取來源，全部改成新網址，讓小幫手回覆會員時給的連結也同步更新

**踩到的坑**：`sync_calendar.py`改抓`event.bymyway.com`後直接403，查出是Cloudflare擋掉urllib預設User-Agent，詳見[[reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30]]。

Related: [[project_netlify_deploy_quota_2026-07]]（額度追蹤SOP，本次之後這幾個站台的額度壓力會逐漸消失）、[[feedback_netlify_autodeploy_cost_awareness]]、[[project_bigtree_session_admin_backend_2026-08-23]]（`event.db`場次後台是這次能做到DB即時渲染的基礎建設）、[[reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30]]
