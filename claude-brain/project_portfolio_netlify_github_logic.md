---
name: project-portfolio-netlify-github-logic
description: 大樹AI作品一覽表的分類邏輯——GitHub Pages是構思測試階段，Netlify.app才是對外公開的正式作品，兩者必然對應
metadata: 
  node_type: memory
  type: project
  originSessionId: 2ce84fc7-8f65-4c4f-ba82-ee34b77d76aa
  modified: 2026-08-24T16:52:20.313Z
---

教練 2026-07-12 親自定調「大樹AI作品一覽表」的建置邏輯，往後任何一台機器的軍師處理教練作品清單，一律照這套規則走，不用每次重新解釋或重新判斷。

## 核心邏輯（教練原話整理）

1. **構思階段／測試階段** → 一律用 `coach1973.github.io/<repo>/`（免費、零成本，隨便測不心疼）
2. **成熟到可以大量對外公開** → 才部署到 `<repo>.netlify.app`（有自訂短網址，是正式對外門面）
3. 因此：**能公開到 Netlify 的作品，必然有對應的 GitHub repo**——因為都是先在 GitHub 測試成功，才推到 Netlify
4. **「作品表」的認定標準只有一個**：能點進去 `xxx.netlify.app` 的，才算「對外公開作品」，單純掛在 GitHub Pages 上的不算數（可能還在測試、還沒定案）

## 例外：19個已封存repo的由來（歷史背景，不是邏輯例外）

教練早期（還不熟悉GitHub操作前）做法是反過來的：**先在 Netlify 做出成品**（那時每次測試都扣Netlify點數，很心疼），**後來才學會用GitHub，把已經做好的網頁另外複製一份到GitHub當備份**。所以這19個repo在GitHub上顯示archived，但它們對應的Netlify網址本身可能還是活的、還在用的舊BNI教材（例：`bni-traffic.netlify.app`真誠猜猜猜、`worklucky-2026.netlify.app`職涯測試等）。**GitHub封存狀態不代表Netlify網址跟著失效，兩邊要分開判斷。**

## Netlify 點數消耗規則（教練詢問，AI依既有教訓`feedback_netlify_autodeploy_cost_awareness.md`確認）

- **改網址名稱（slug）本身不扣點**——純後台設定變更，沒有真的上傳新內容
- **真正扣點的是「部署」這個動作本身**，不論是全新網站的第一次部署、還是舊網站的更新部署，扣的點數一樣
- 推論：想用舊網址做新專案，「改名字+重新部署」跟「刪掉重建」點數消耗沒有差別，改名字只是操作上省事（不用重新申請新網站），不是省點數
- 真正該省的環節是「不要在測試階段就往Netlify部署」，測試一律留在GitHub Pages

## 教練目前對「隨機亂碼」殘留repo的處置方向（尚未拍板，2026-07-12仍在評估）

那些自動命名的草稿站（如`tubular-centaur-a769c4`這類）教練還在考慮：要嘛直接刪掉，要嘛留著網址、之後有新專案時直接改名重新部署上去。因為改名不扣點，教練傾向後者（保留、之後複用），但還沒最終拍板，遇到相關任務先問教練當下決定，不要自己假設。

## Why

教練要把AI實戰經驗做成一份可信、可對外展示的完整作品集（`bymyway.com/ai/`頁面已經有一版精選），需要一套穩定、可重複套用的判斷標準，不希望每次盤點都重新想一遍規則，也不希望不同機器的軍師各自判斷出不一樣的結果。

## How to apply

- 之後教練要求「列出作品」「更新作品表」，直接用「有沒有Netlify.app網址」當唯一篩選標準，不用再問教練「這個算不算」
- 看到某個repo在GitHub上是archived狀態，**不能直接假設它的Netlify網址也失效**，兩邊要分開查證（[[reference_coach_websites]]記錄了2026-07-12 `goeasy-ai`就是一次「archived但Netlify還在活跳跳用」的真實案例）
- 教練問「改名字要不要扣點」這類Netlify操作成本問題，答案已經確認：改名免費，部署才扣點，可以直接引用不用重查
- 遇到列表裡「名稱」跟「網址」對不上的情況（如本場`cool-case`vs`大台南BNI培訓行事曆`的錯位疑雲），比照[[feedback_markdown_link_mismatch_verify]]的標準：先查證兩邊網址真實內容再回報教練，不要照單全收也不要自己默默改掉

## 🔴 2026-08-25更正：作品總覽的更新現在是SOP的一部分，不是「Netlify才算數」而已

教練當場糾正：AI微論壇台中場先推GitHub Pages測試、後推Netlify正式上線，兩個階段都沒有主動同步更新`coach888/index.html`（作品總覽），教練親口拍板往後這是SOP：
1. **構想/製作階段先推GitHub測試** → 當下就要把GitHub Pages網址加進作品總覽（可放「不公開／個人檢索用」區）
2. **測試完成推Netlify** → 同一時間把作品總覽該筆項目的網址改成Netlify正式網址，並依內容性質搬到對應公開區（本次案例搬進「大樹常用」，跟同系列的[[微型論壇]]放一起）

**How to apply**：往後任何一個網站專案走到「推GitHub測試」或「推Netlify」這兩個動作，都要在同一輪順手打開`/Users/bymyway/github_repos/coach888/index.html`同步更新，不能等教練事後問「有沒有放進作品總覽」才想起來。這條跟上面「只有Netlify.app算作品」的舊邏輯不衝突——舊邏輯講的是「哪些算對外公開作品」的判斷標準，這條講的是「不管哪個階段，只要用戶看得到，作品總覽都要跟著更新」的執行紀律。

Related: [[reference_coach_websites]]、[[feedback_netlify_autodeploy_cost_awareness]]、[[feedback_markdown_link_mismatch_verify]]
