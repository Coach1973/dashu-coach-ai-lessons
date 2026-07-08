# 軍師接力棒 · 2026-07-09 v52（Mac 終端機 Sonnet 5，結繩領導學BNI/工作坊邀請頁系列4站上線）

> 建立時間：2026-07-09 凌晨 04:52（台灣時間）
> 本棒執行者：Mac 終端機軍師 **Sonnet 5**
> 上一棒：v51（2026-07-08 晚上 21:15，Sonnet 5，佩佩電腦W03首跑+bni-dna網站更新）
> 本棒主軸：**從零做出結繩領導學工作坊邀請頁，一路迭代到4個獨立短網址上線 + RustDesk記憶體自動監控**

---

## 🎯 本場戰果

### 1. 結繩領導學工作坊邀請頁系列 — 4 個獨立短網址已上線

| 對象 | 大樹教練版 | 佩佩老師版 |
|---|---|---|
| BNI 會員 | bni-invite.netlify.app | bni-peipei.netlify.app |
| 一般夥伴 | workshop-invite.netlify.app | workshop-peipei.netlify.app |

- 從教練一段文案開始，做成套用「結繩領導學」官方深藍＋暖橘配色的一頁式手機滑動邀請文案，套版曜董完整資歷（37年工程經驗/BNI臺灣國家發展董事暨國家培訓董事/三家跨國外商）、識人育人用人留人大字方塊、浮動書封、回到頂部按鈕、滑鼠hover互動效果
- 教練逐條列 1~43 號字級清單，一次調整全部文字大小；情感核心段落重寫成「這不容易/但是/是值得的/因為/有了團隊/代表/有了一切」七行交替節奏
- 原本先推到 `jiesheng-leadership.netlify.app/invite-bni.html` 這種長路徑，後來教練要求改成獨立短網址；發現重複內容後，正確解法是「保留已驗證好的新短網址，刪掉舊repo裡對應的長網址檔案」（非砍掉重練）
- 又複製一版把「BNI」全部改「工作坊」、「BNI夥伴」改「優秀的領導人」，變成非BNI對象版本

**記憶已存**：`project_bni_invite_pages_2026-07-09.md`（完整過程+教練工作習慣）

### 2. 部署 SOP 血淚教訓與更正

- 一晚不知不覺對 jiesheng-leadership（GitHub 自動部署型 Netlify 站）push 了 6 次 = 6 次部署，教練事後才發現
- **教練親口定義正確邏輯**：判斷準則是「這個網頁有沒有已經公開推廣過」，不是「有沒有講到 Netlify」——已公開推廣站（結繩領導學、goeasy-ai）更新本來就該直接推 Netlify，這是必要行為；內部測試頁才先留 GitHub
- 查證確認：Netlify 改網站子網域名稱（非重新部署）不算 deploy、不扣點（官方文件+支援論壇佐證）

**記憶已修正**：`feedback_netlify_autodeploy_cost_awareness.md`（先寫錯後更正，記錄教練親口澄清的完整邏輯）

### 3. RustDesk 記憶體自動監控已建立

- 手動重啟一次即時解決（283MB→61MB）
- 建立 launchd 排程 `ai.openclaw.rustdesk-guard`，每天凌晨5點自動檢查，超過 **800MB** 才重啟（原訂200MB門檻太低，實測活躍連線1分鐘內就會自然漲到280~300MB，會誤殺正在使用中的連線，已修正）
- 腳本：`scripts/rustdesk_memory_guard.sh`，log：`logs/rustdesk_memory_guard.log`
- 本棒結束時實測：連續使用3.5小時後已到731MB，接近800MB門檻，下一棒開工時可查 log 確認有無自動觸發重啟

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🟡 | 4個邀請頁網址教練還在確認排版細節中，**都還沒正式對外發送過**，之後如還要繼續微調字級/文案，直接延續本場模式（本機Chrome預覽→教練確認→說「推」） |
| 🟡 | RustDesk 排程觀察：查 `logs/rustdesk_memory_guard.log` 有沒有新的自動觸發紀錄 |
| 🔴 | **2026-07-15**（v51遺留）：佩佩電腦觀察期滿，教練確認「運行沒問題」後才能砍 6 個 `.bak`/`.stale_backup`（約回收3.13GB），走 Safe-Remove 五道閘門 |
| 🟡 | （v51遺留）佩佩電腦 Zoom Roaming-data 933MB 不一致問題、桌面4個中文編碼資料夾待處理 |
| 🟡 | （v51遺留）bni-dna：8月(8/12)例會結束後，教練口述出席名單，比照流程更新 |
| 🟡 | （v51遺留）biz-gym 黑金新版等教練說「推」 |
| 🟢 | （v51遺留）聯想/ACER 兩機的同款系統稽核（需教練拍板） |

---

## 🔑 關鍵檔案索引（本場）
- `github.com/Coach1973/jiesheng-leadership` — 原始碼倉庫（teacher.jpg/book.png 素材、部署腳本參考）
- `scripts/rustdesk_memory_guard.sh` + `~/Library/LaunchAgents/ai.openclaw.rustdesk-guard.plist` — RustDesk 監控
- 記憶：`project_bni_invite_pages_2026-07-09.md`、`feedback_coach_sales_page_typography_style.md`、`feedback_netlify_autodeploy_cost_awareness.md`

---

## 📜 v51 精簡回顧（佩佩電腦W03首跑+bni-dna網站更新，完整內容見git歷史）
佩佩電腦成功搬移4個App共2.21GB，7天觀察期到7/15；bni-dna出缺席戰情儀表板全年改版上線（commit `8646ef2`），新增7月資料+移除7位夥伴+滾動式淘汰規則+全勤獎公告。

## 📜 v50 精簡回顧（教練休息前交辦佩佩電腦任務，完整內容見git歷史）
教練糾正軍師「叫他貼文字」的錯誤做法，改用雲端信箱慣例；信件三次迭代補齊真實障礙；commit `3cbf96a09`→`a31a8894e`→`38ca34611`。

---

> Sonnet 5 親筆，2026-07-09 凌晨 04:52。教練說「總結並上傳」，本棒收尾。這場從一段文案開始，一路迭代到4個獨立短網址上線，過程中發生過部署SOP誤判（先寫錯memory又更正）、RustDesk監控門檻設太低誤殺連線（實測後修正），都已誠實記錄。下一棒接手可直接從「下一棒待辦」表接續，4個邀請頁都還沒正式發出去，教練隨時可能繼續微調。
