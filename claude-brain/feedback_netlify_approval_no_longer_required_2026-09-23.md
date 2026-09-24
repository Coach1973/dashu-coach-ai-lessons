---
name: netlify-approval-no-longer-required
description: "教練2026-09-23親口鬆綁：Netlify現在很少用、點數夠，不用每次先問教練同意才推，跟[[feedback_netlify_autodeploy_cost_awareness]]的舊鐵律(每次要教練說「推」)互相取代"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 055522b8-9175-4e6b-8d08-d83e98515a06
  modified: 2026-09-23T05:16:36.275Z
---

Netlify部署不再需要每次先取得教練同意才能推送。

**Why:** 2026-09-23教練原話：「Netlify我們目前基本上已經很少在用了，裡面的點數夠，該扣就扣，現在不用經過我同意了。因為我們已經沒有在用它更新資料，絕對足夠扣，我們接下來的重心都會放到自己的系統當中。」——起因是bigtree-tw.netlify.app因為`event.db`資料沒同步而顯示過期活動，我問要不要先經教練確認才重新一鍵發佈(照舊SOP)，教練直接鬆綁這條規則。

**How to apply:** 舊的「教練說『推』才能部署Netlify」鐵律(2026-05-30訂定，[[feedback_netlify_autodeploy_cost_awareness]])**在這個時間點之後不再需要逐次確認**——但不代表可以隨便亂推：仍然要先確認內容正確(本機驗證/資料庫比對)，也要留意`netlify_deploy_guard.sh`這支hook本身的攔截機制還在(需要`NETLIFY_DEPLOY_CONFIRMED=1`前綴才會放行，語法上這個前綴必須是整個bash指令字串的最開頭，不能跟`cd xxx &&`之類的指令串在一起，否則regex比對不到)，這個前綴現在可以視同「教練已授權」直接使用，不用真的等教練在對話裡打「推」才動用。如果未來Netlify的角色又變重要(教練會重新開始用它更新正式資料)，這條鬆綁可能需要教練重新收緊，屆時留意教練是否有新指示。
