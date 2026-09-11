---
name: feedback-verify-public-visibility-not-just-api-success
description: 驗證FB貼文「真的上線」要用無登入/無關聯瀏覽器實測，不能只信管理員token查API/permalink_url成功
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a5f17e3-d7d6-4554-b945-cf61bff7d55e
  modified: 2026-09-11T02:25:17.696Z
---

過去(9/2, 9/16)驗證FB貼文成功的做法是：用發文用的同一組Page access_token去GET該post的`permalink_url`欄位，查得到就當作「已驗證真實上線」。**這個方法有盲點**——查詢用的token是App管理員身份，Facebook對Page擁有者/管理員的內容可見性是獨立通道，永遠查得到自己Page的貼文，跟「一般訪客看不看得到」完全是兩回事。教練朋友反映分享連結失效才發現：這4則貼文其實從發布當下就對一般大眾隱形，之前的驗證方法從沒抓到過這個問題。

**Why**：教練親口反映「朋友點連結說連結失效」才揭穿這個盲點，此前多次(9/2、9/5、9/16)用permalink_url驗證「成功」的貼文可能都有同樣風險沒被抓到。

**How to apply**：往後驗證任何用第三方App/Graph API發布的公開內容是否真的對外可見，要用一個完全獨立、未登入、跟該App/帳號無關聯的瀏覽器session實際訪問（不能用同一組管理員token或已登入教練帳號的分頁去查），才能代表訪客視角。若條件不允許，至少要明確告知教練「這只驗證了API層級成功，不代表一般人看得到」，不要用「已驗證上線」這種籠統措辭造成過度保證。

相關：[[reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11]]
