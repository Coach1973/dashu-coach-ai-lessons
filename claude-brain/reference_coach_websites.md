---
name: reference-coach-websites
description: 教練所有GitHub作品清單（41個repo，2026-07-09教練親自盤點分類，18個已封存，23個活躍；含2026-07-12大樹AI作品一覽表挑選來源）
metadata: 
  node_type: memory
  type: reference
  originSessionId: 16511bcd-5087-40ef-822c-1c9c29f266f9
---

2026-07-09 用 GitHub API 對 Coach1973 帳號實測拉出完整清單後，教練親自盤點指出：41個裡真正完稿、公開推廣、使用過的沒那麼多，很多是早期不熟悉AI操作時Netlify測試站整批同步過去的「無心插柳」。教練確認後，AI用`gh repo archive`把19個閒置的repo全部封存（GitHub原生功能，唯讀化+灰階顯示，完整歷史保留不刪，隨時可解封），並逐一用API驗證`archived:true`為真。全部都是教練動口、AI動手完成，教練自己寫的程式碼＝0行。

**真正公開、有推出、有使用過的（活躍，共11個確認+7個待教練說明）**：
1. bigtree（大樹小講．無話不談，含歷史講座紀錄+2026創業x政府xAI講座EDM）：coach1973.github.io/bigtree
2. jiesheng-leadership（結繩領導學）：coach1973.github.io/jiesheng-leadership
3. bni-dna（DnA出席戰情儀表板，實際追蹤會員出席）：coach1973.github.io/bni-dna
4. cool-case（特助心法實踐案例集）：coach1973.github.io/cool-case
5. ai-go（AI特助心法一鍵注入，教練說過的「永久網址」）：coach1973.github.io/ai-go
6. theunrestrictedwar（超限戰電影網站，教練確認過的「正式版」）
7. consultant（創業避坑掃雷講座，7/1台南場，謝扉榆合作）：coach1973.github.io/consultant
8. government-grow / government-subsidies（中小微企業多元發展說明會，台南場）
9. gold-excellence（金卓獎聚會）
10. bymyway-website（個人品牌官網，曾是bymyway.com首頁，2026-07-03後被bigtree取代）
11. goeasy-ai（AI一鍵起飛3小時實戰講座活動頁，coach1973.github.io/ai/品牌故事頁親自連結對外使用中，2026-07-12教練發現誤封存，已`gh repo unarchive`解封並驗證archived:false——這是「93天未更新=閒置」判斷法則的一次誤判，判斷閒置不能只看更新日期，要交叉比對是否被其他活躍頁面連結）
12. northern411（2026-07-13確認：對外網址`northern-tw.netlify.app`，「全球健康發展協會」智匯健康｜腦力長青｜2026失智防治與逆齡醫學跨界論壇，已辦3場，**GitHub自動部署型**——push main分支就會自動觸發Netlify部署，跟ai-talk等手動zip型不同，詳見[[project_ai_talk_recurring_event_url_policy]]）

**待教練確認用途是否算「公開活躍」**：vip-club、coach-vip-club（兩者內容相近，哪個是正式版？）、coach-case / coach-case2 / coach-case3 / coach-case4（獨立公開站還是cool-case草稿？）、teamwork（結繩領導學的獨立網站還是資源包？）、tainan-calender（說明留空，用途待補）

**純技術用途，本來就不是要公開的網站（has_pages=false，不算閒置）**：
dashu-coach-ai-lessons（AI經驗庫踩坑記錄）、claude-workflows（Claude AI自動化工作流腳本備份）

**已封存（2026-07-09，原19個，2026-04-06同一天建立、93天未更新，教練確認是早期Netlify測試整批誤同步；2026-07-12 goeasy-ai已解封移出，現存18個）**：
tubular-centaur-a769c4、comforting-salmiakki-356efb、deluxe-hamster-6a3525、lucky-fox-ce325e、courageous-scanstart、tourmaline-panda-82be5e（6個自動命名草稿站）、bniheroway、bni-traffic、bni-99999、bni-88888、bni-happy、bni-top10、worklucky-2026、everyday7、goeasy-ai88、peipeievent-411（10個BNI系列早期練習）、tree-coach-book、claude-test

**How to apply**：這份清單是[[project_media_resource_center_2026-07-09]]媒體資源中心的核心素材來源之一。之後若要重新盤點，直接用 `curl https://api.github.com/users/Coach1973/repos?per_page=100` 拉最新清單，用`gh api repos/Coach1973/<repo> --jq '.archived'`查封存狀態，不要只憑記憶。「待教練確認」那7個問清楚後要更新分類。這台聯想機的`gh`已用Coach1973帳號登入且有`repo`權限，之後封存/解封操作可直接用`gh repo archive`/`gh repo unarchive`。
