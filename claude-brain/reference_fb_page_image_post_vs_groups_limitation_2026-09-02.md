---
name: reference-fb-page-image-post-vs-groups-limitation-2026-09-02
description: FB粉專自動發文首次驗證可發圖片(不只文字)；FB社團(Groups)因Meta 2018年後政策全面鎖死一般App的發文權限
metadata:
  type: reference
  originSessionId: cbe8bfb7-5b8c-497d-b87b-3acdaf73d1b4
  modified: 2026-09-02T11:46:45.802Z
---

2026-09-02教練問「粉專能發文，那社團也可以嗎」+「圖片你也能發嗎」，兩個問題查證結果：

**粉專（Pages）：文字+圖片都能發，同一組權杖**
之前`fb_automation/post_bigtree_20260901.py`只驗證過純文字（`POST /{page-id}/feed`帶`message`）。本場首次驗證圖片+文案一起發：`POST /{page-id}/photos`帶`source`（multipart檔案，這台機器沒裝`requests`套件，改用`curl -F`處理）+`caption`（文案全文）+`access_token`。用`fb_automation/page_tokens_2026-09-01.json`裡任一粉專權杖即可，5個粉專實測全部成功，且用回傳`post_id`再查一次`permalink_url`欄位確認真的公開上線（不只信POST的成功回應）。

**社團（Groups）：一般App幾乎發不了**
Meta自2018年劍橋分析事件後大幅收緊`publish_to_groups`權限，一般開發者App幾乎申請不到、審核也很難過。這是Meta平台政策限制，不是這個App或這套自動化系統的缺陷。唯一潛在替代路徑是比照先前手動貼5個粉專那次的「瀏覽器模擬真人點擊」方式（claude-in-chrome操作教練本人已登入的Chrome），但教練個人帳號在社團裡跑自動化行為，被FB系統判定為機器人/洗版的風險比官方粉專API高很多（社團生態對垃圾訊息防範比粉專嚴格）。

**Why**：教練想擴大行銷曝光範圍到他加入的社團，需要先知道這條路在技術上走不通（API層級），才不會誤以為是AI能力不足。

**How to apply**：
- 教練問「粉專還能不能做什麼」→ 圖片、多圖片（先各自上傳成`published=false`拿`media_fbid`再包進同一則貼文用`attached_media`）都可以，純文字/單圖已驗證，多圖尚未實測過
- 教練問「社團可不可以自動發文」→ 直接引用本則查證結果回答「一般App層級發不了，是Meta政策鎖死不是我們系統的問題」，不用重新查證Meta文件；如果教練想冒風險用瀏覽器模擬硬做，要先講清楚帳號被限制發文/警示的風險再動手
- 發布後一定要用`permalink_url`欄位二次查證，不能只看POST回傳的`id`/`post_id`就算數（呼應[[feedback_verify_dont_relay_secondhand_claims]]同精神，這裡是「AI自己也要對自己的執行結果二次查證」）

Related: [[feedback_verify_dont_relay_secondhand_claims]]
