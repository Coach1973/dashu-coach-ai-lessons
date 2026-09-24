---
name: feedback-search-namecard-db-before-claiming-taxonomy-missing
description: 誤報「查無700多類BNI專業分類資料庫」，其實是查證範圍太窄漏了namecard-db目錄；教練親定「AI推理出的節點」跟「BNI真實案例驗證過的節點」可信度不同，產業鏈出圖要優先用後者
metadata:
  node_type: memory
  type: feedback
  originSessionId: f5284690-7a90-4097-9918-9cbfb59c5ce2
  modified: 2026-09-23T14:28:36.123Z
---

被教練問「產業鏈SOP怎麼運作」時，只查了`scripts/`、`claude-brain/`、`knowledges/`就回報「找不到700多類資料庫」，教練立刻指正並點出正確位置：`namecard-db/taxonomy.json`（905個不重複BNI標準專業名稱，整合自「大台南南區AI小幫手」682+產業資料庫+BNI官方533項清單）。查證範圍沒有涵蓋`namecard-db/`這整個目錄，是這次誤判的直接原因。

**Why：** 教練直接點破「我跟你保證我們絕對有700多種專業類別的分類系統」「你去查對話紀錄，一定有這個資料」——教練記得清楚，是我自己查證動作做得不夠廣，不是資料真的不存在。這跟[[feedback_check_master_index_before_claiming_cant_find]]是同一種模式：說「找不到」之前，查證範圍要夠廣，不能只查幾個常用目錄就下結論。

**教練同時親自定義了一條更深層的原則（2026-09-23）**：AI自己推理出來的候選節點（例如「這個行業旁邊應該會有OO角色」）即使邏輯合理，沒有真實案例佐證，說服力就弱；BNI taxonomy.json裡的905項則是「真的有人用這個專業類別加入過BNI」，可信度遠高於AI憑空聯想。往後任何「產業鏈出圖/媒合」類任務，節點名稱要優先跟這份905項真實清單比對，查核工具已建：`scripts/check_industry_chain_names.py`。完整SOP見`knowledges/SOP_產業鏈.md`（新建）。

## How to apply

1. 教練問「某個資料庫/檔案存不存在」時，查證範圍要涵蓋整個workspace的主要目錄（包括`namecard-db/`這類功能性子系統目錄），不能只查印象中「常用」的幾個資料夾就回報「找不到」。
2. 教練說「你去查對話紀錄」時，這通常代表他對某件事有明確記憶，值得認真擴大查證範圍再回答，不要用「我查過workspace沒找到」就直接否定教練的記憶。
3. 任何要幫BNI相關任務(產業鏈出圖、名片媒合、分類建議)想出「候選專業角色名稱」時，先用`scripts/check_industry_chain_names.py`比對`namecard-db/taxonomy.json`的905項真實清單，能命中就優先用命中的名稱，查無再考慮是否保留(需自知沒有真實案例背書)。

Related: [[feedback_check_master_index_before_claiming_cant_find]]
