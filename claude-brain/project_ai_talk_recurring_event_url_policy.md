---
name: project_ai_talk_recurring_event_url_policy
description: AI微型論壇是持續舉辦的系列活動，GitHub是每場改稿用的工作稿，Netlify固定網址ai-talk-tw.netlify.app才是永久對外公開網址，換場次不換網址
metadata: 
  node_type: memory
  type: project
  originSessionId: 6478f86b-2a53-4ef1-9aba-41c3d1ba22f5
---

## 規則（2026-07-13 教練親口交代）

「AI微型論壇」這個活動會持續辦下去（台南場之後還會有台中場、高雄場等），但**對外
公開推廣的網址永遠只有一個**：`https://ai-talk-tw.netlify.app/`。

**How to apply（下一場籌備時，不管哪台機器/哪個軍師接手）：**
1. GitHub repo `Coach1973/ai-talk`（本機clone在聯想 `E:\Claude-Data\github_repos\ai-talk`）
   是工作稿——每次新場次直接在同一份 `index.html` 上改時間、地點、講師陣容，
   套用同一套版型，不需要另建新repo
2. 教練確認新場次內容OK後，走既有流程推：先commit+push GitHub（存歷史），
   再zip+Netlify API推同一個site（site_id `633b4b00-dae8-476c-a21b-9d0548bf1e66`），
   **不要新開Netlify站**，永遠覆蓋同一個 `ai-talk-tw.netlify.app`
3. GitHub Pages那邊因此會隨場次不斷變化（可能某天是台南場內容、某天變台中場），
   這是正常的、預期中的行為，不代表版本混亂——GitHub本來就只是工作稿，唯一
   要當作「正典/對外事實」的只有Netlify當下顯示的內容
4. 對照既有邏輯 [[project_portfolio_netlify_github_logic]]（GitHub=測試/Netlify=
   對外公開）——這個專案是同一套邏輯的具體實例，只是換成「同一網址反覆覆蓋」
   而非「多個獨立作品各自一個網址」

## 已有先例驗證（教練 2026-07-13 親口補充，7/13查證修正）

「全球健康發展協會」（正確網址 `https://northern-tw.netlify.app/`，網站標題「智匯
健康｜腦力長青｜2026失智防治與逆齡醫學跨界論壇」，repo為 `Coach1973/northern411`）
已經照這套模式辦過**3場**——GitHub後端跟著每場活動內容改了3次，但對外公開的固定
網址從頭到尾都是同一個，群眾點的連結不變、只有內容跟著換。AI微型論壇是複製這套
已經驗證跑通的模式，不是新發明。

⚠️ **這裡曾經錯誤引用過「全球健康發展協會」（goeasy-ai）當案例，教練指出「這個才
是」點名northern-tw後才發現搞混——兩個名稱一字之差（全國 vs 全球）、但是完全不同
的兩個專案，日後聽到類似機構名稱要留意逐字核對，不能靠印象快速匹配。**

🔴 **順帶查證發現一個修正舊記憶的重點**：`northern-tw` 是**GitHub自動部署型**
（Netlify後台直接接 `Coach1973/northern411` main分支，git push就會自動觸發部署），
不是手動zip上傳型。這代表 [[feedback_netlify_deploy_zip_api]] 裡「23個站只有1個
是GitHub自動部署（health-news-tw）」這筆舊記憶已經過時/不完整，至少還有northern-tw
這個第二個自動部署站，該記憶檔已同步修正。

## 相關

- Netlify site：`ai-talk-tw`，site_id `633b4b00-dae8-476c-a21b-9d0548bf1e66`
- GitHub repo：`Coach1973/ai-talk`（main分支，GitHub Pages來源）
- 部署方式見 [[feedback_netlify_deploy_zip_api]]（手動zip+API型，git push不會自動同步Netlify）
- 已驗證同模式先例：`northern-tw`/`northern411`（全球健康發展協會，已辦3場，
  GitHub自動部署型）、`jiesheng-leadership`（結繩領導學）——見
  [[feedback_netlify_autodeploy_cost_awareness]]
