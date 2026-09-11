---
name: reference-fb-graph-api-app-review-required-for-public-visibility
description: 用Graph API直接發文的粉專貼文，一般訪客(非App角色成員)可能完全看不到，需App Review才能對外可見
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0a5f17e3-d7d6-4554-b945-cf61bff7d55e
  modified: 2026-09-11T02:24:57.236Z
---

用來幫14個粉專發文的App「大樹教練粉專發文小幫手」(App ID `1050871501278089`)目前處於Meta「可供測試」等級，尚未通過App Review。實測證實：**用這個App透過Graph API發的貼文，只有App角色成員(教練本人)看得到，一般訪客連在Page動態時報裡都看不到該則貼文（不只是分享連結失效），管理員自己打開Page後台或動態牆卻完全正常**——因為Page擁有者/管理員的瀏覽權限是獨立通道，不受App Review狀態影響。

**時間序列證據**：2026-09-01用`/feed`分享外部連結(`status_type=shared_story`)發的貼文，一般訪客可見；但2026-09-02之後用`/photos`上傳圖片(`status_type=added_photos`)或純文字(`mobile_status_update`)發的貼文，訪客一律看不到。兩種端點都受影響，代表根因不是端點類型差異，較可能是9/1~9/2之間這個App被Facebook系統標記/降級（可能因短時間對多個Page發相似格式內容觸發反濫用偵測），但未100%確認確切機制。

**要修復需要App Review，但代價很高**：點進「新增到應用程式檢閱」流程，Meta要求先變成「Tech Provider」身份才能提升權限等級，且明確警告「**這個決定無法撤銷**」，還要求商業驗證(提供商業登記文件)+存取權驗證(這步驟設計給"需要存取別人商業資產"的技術服務商，不是教練這種自用情境)+完整App Review問卷。教練評估後認為代價遠超過需求，**裁示放棄App Review這條路**。

**改用做法**：往後這類活動宣傳貼文，改由教練本人或軍師操作已登入的真實瀏覽器(Meta Business Suite或Page首頁「建立貼文」)手動發布，不再透過這個Graph API App。

**已知受影響、對訪客隱形的歷史貼文**：2026-09-02兩則(KR養生廚房返場+9/16高雄場)、2026-09-11發的9/16跟9/23-24兩則文案，共4篇需要重貼。

相關：[[feedback_verify_public_visibility_not_just_api_success]]
