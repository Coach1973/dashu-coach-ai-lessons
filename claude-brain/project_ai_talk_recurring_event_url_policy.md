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

## 相關

- Netlify site：`ai-talk-tw`，site_id `633b4b00-dae8-476c-a21b-9d0548bf1e66`
- GitHub repo：`Coach1973/ai-talk`（main分支，GitHub Pages來源）
- 部署方式見 [[feedback_netlify_deploy_zip_api]]（手動zip+API型，git push不會自動同步Netlify）
