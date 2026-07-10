---
name: project-bni-invite-pages-2026-07-09
description: 結繩領導學BNI/工作坊邀請頁系列——從無到有做出4個獨立短網址版本的完整過程與教練工作習慣
metadata: 
  node_type: memory
  type: project
  originSessionId: 2be4fc3d-0468-40ed-9dee-dd84f711a9f1
---

# 結繩領導學工作坊邀請頁系列（2026-07-09 凌晨）

## 最終成果：4 個獨立短網址

| 對象 | 大樹教練版 | 佩佩老師版 |
|---|---|---|
| BNI 會員 | bni-invite.netlify.app | bni-peipei.netlify.app |
| 一般夥伴 | workshop-invite.netlify.app | workshop-peipei.netlify.app |

全部套用「結繩領導學」官方深藍(#0b2742/#123a63)＋暖橘(#f28c28/#ffb25b)配色，一頁式手機滑動邀請文案，內容涵蓋：情感訴求（有了團隊就有了一切）、8/19-20台南維悅酒店活動資訊、識人育人用人留人大字方塊、《結繩領導學》浮動書封、講師蔡曜隆完整資歷（37年工程經驗/BNI臺灣國家發展董事暨國家培訓董事/三家跨國外商經歷）、四個「為了」理由卡、多場次報名按鈕（台南/台中/台北）、回到頂部按鈕。

原始碼倉庫：`github.com/Coach1973/jiesheng-leadership`（invite-bni.html/invite-peipei.html 曾短暫存在，後因避免與獨立短網址重複內容而刪除，改由 /tmp 部署包直接上傳到 4 個獨立 Netlify site）。

## 這次驗證過的教練工作習慣（同步存進 [[feedback-coach-sales-page-typography-style]]）

1. **逐條編號下指令**：教練會把頁面所有文字列成 1~43 號清單，直接說「第9條放大到36」這樣調整，比起用文字描述位置快很多。
2. **一次要多版本**：同一版型，換邀請人身分（大樹教練/佩佩老師）、換受眾措辭（BNI/工作坊夥伴→領導人），是常見量產模式，之後遇到類似需求可以直接問「這次要哪幾個版本組合」。
3. **部署節奏**：本機 Chrome 預覽 → 教練確認 → 說「推」才 commit+push；已公開推廣的站直接推 Netlify 是正常行為，不需要每次都提醒扣點成本（詳見 [[feedback-netlify-autodeploy-cost-awareness]]）。
4. **網址要簡短獨立**：不喜歡長路徑（如 `jiesheng-leadership.netlify.app/invite-bni.html`），偏好簡短好記的獨立 `*.netlify.app` 子網域，命名會直接指定（BNI-invite、workshop-peipei 這種）。

## 技術教訓

- **Netlify 改網站子網域名稱不算 deploy、不扣點**（已用官方文件+支援論壇查證，見 feedback memory）；但「新建 site + 上傳部署」是真正的部署動作，會計入。
- **同一份內容不要有兩個網址同時存在**：發現重複後的正確解法是「保留已驗證好的新短網址，刪掉舊 repo 裡對應的長網址檔案」，不是砍掉重練，也不是放著不管。
- **RustDesk `--server` process 記憶體會隨連線時數持續攀升**（不是7天累積的洩漏，是活躍連線期間就會漲，實測3.5小時內從60MB漲到731MB），已建立每天凌晨5點自動檢查、800MB才重啟的 launchd 排程（`scripts/rustdesk_memory_guard.sh`），避免門檻設太低誤殺正在使用中的連線。

## 相關記憶
[[feedback-coach-sales-page-typography-style]]、[[feedback-netlify-autodeploy-cost-awareness]]、[[reference-netlify-token]]

---

## 2026-07-10 更新：姓名個人化功能上線 + bigtree 手機版優化

### 1. 邀請頁新增「姓名取代 BNI」個人化功能

教練提出挑戰：能否讓每則邀請連結顯示收件人姓名。解法：URL 參數(`?name=姓名`)+ JavaScript，純前端、免資料庫。

- 網址後面加 `?name=王小明`，頁面自動把導覽列「BNI 專屬邀請」的「BNI」換成姓名，下方「BNI 專屬價值」徽章換成「{姓名} 專屬邀請」——教練逐步微調成「換字不加行」的協調版本，不是額外插入一行問候語
- **4 個網站已正式部署**（`0dcb9f34`/`2ecef0da`/`ac6c851e`/`2aadd382` 四個 Netlify site ID，用 zip+API 推送，帶 `_headers` 檔避免顯示原始碼）
- 用教練提供的 Google 試算表名單（BNI 分會會員，姓名格式「姓名-分會名」需拆分），示範產生前 10 位正式連結
- **踩過一個假象坑**：第一次用 `open -a "Google Chrome" "file://...?name=..."` 開本機預覽，網址參數被 macOS `open` 指令吃掉，教練說「沒有」看不到效果——查 Chrome 分頁網址發現參數真的不見了，改用 `osascript -e 'open location ...'` 才正確保留參數。**教訓：本機 Chrome 預覽帶查詢字串時，`open -a` 不可靠，要用 `osascript open location`。**

### 2. bigtree 手機版導覽列漢堡選單 + 回到最上面按鈕

`coach1973.github.io/bigtree/` 手機版原本完全看不到導覽連結（只有 `hidden md:flex` 的桌面版選單）。新增三線漢堡按鈕展開 7 項（品牌故事/主題領域/近期場次/學員見證/常見問答/歷史紀錄/立即報名），教練口語「進行場次」「歷史記錄」直接對應既有的「近期場次」「歷史紀錄」，不用多問。另加浮動回頂按鈕，滾動 400px 後浮現。

- **commit `424ce52`**，push 前先 `git pull --rebase` 處理遠端有其他新 commit 的情況
- GitHub Pages 是 `legacy` build type，push 後用 `gh api repos/.../pages/builds/latest` 輪詢確認 `status: built` 才算真正上線，不能只看 `git push` 成功就結案

## 相關記憶（更新）
[[feedback-coach-sales-page-typography-style]]、[[feedback-netlify-autodeploy-cost-awareness]]、[[reference-netlify-token]]、[[project-mobile-claude-sync-2026-07-10]]
