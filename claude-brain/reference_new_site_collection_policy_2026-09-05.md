---
name: reference_new_site_collection_policy_2026-09-05
description: 新網站要收錄在coach888(教練自己作品)還是tainan-shangquan(朋友/客戶店家)的判斷規則，2026-09-05教練親定
metadata: 
  node_type: memory
  type: reference
  originSessionId: bdb4d3d8-b2a2-477a-bea7-9c4e596abd45
  modified: 2026-09-05T14:01:06.919Z
---

2026-09-05教練拍板新規則，區分兩種收錄去處：

- **coach888作品一覽**（`coach1973.github.io/coach888/`）：只收教練自己的作品/後台系統/常用連結，例如BNI相關系統、教練自己主講的活動網站。
- **tainan-shangquan店家名冊**（`event.bymyway.com/tainan-shangquan/`首頁「店家名冊」區塊）：收「教練朋友/客戶的一次性網站」——不限台南、不限「大台南商圈整合計劃」正式參與店家，教練原話「南北串聯，不限台南，我的朋友都可以放進來，多多益善」。2026-09-05當天已把lin-beiyi(林貝羿逸心生技)、66-harbour(66街道咖啡)、tainan-pickleball-art-rotary(臺南匹克藝術扶輪社)、kingmauii(金茂宜咖啡)四個原本誤放進coach888的客戶案網站revert掉，改收進tainan-shangquan店家名冊(commit`9eca3f0`)。

**How to apply**：以後小龍蝦/ACER/聯想任一台軍師做完教練朋友的客戶案網站（非教練本人的活動/作品），收尾步驟一律是「寫信通知Mac軍師收進tainan-shangquan店家名冊」，不要收coach888。真正屬於教練自己主講/主辦的活動或後台系統，才收coach888。

技術細節：tainan-shangquan的`index.html`裡有`SHOP_CARDS_INSERT_POINT`標記，程式化插入新店家卡片時找這個標記；卡片模板見`event-signup/app.py`的`_shop_directory_card_html()`函式（自動化流程用）或參考`~/github_repos/tainan-shangquan/index.html`裡既有卡片的HTML結構（手動新增時）。

關聯：[[feedback_new_public_site_must_register_coach888_2026-09-04]]（舊規則，本篇是2026-09-05的更新版，教練朋友客戶案不再收coach888）
