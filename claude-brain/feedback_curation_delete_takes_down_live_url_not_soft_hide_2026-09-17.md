---
name: feedback-curation-delete-takes-down-live-url-not-soft-hide-2026-09-17
description: "/curation/admin/delete/<slug>是整套退役(GitHub repo改名+關Pages+registry移除)，不是「只拔掉店家名冊卡片」的軟性隱藏——動手前先想清楚要的到底是哪一種"
metadata:
  type: feedback
---

**發生什麼**：2026-09-17，大樹小講10/3(KR養生廚房)活動頁因缺少報名頁上架SOP被佩佩老師誤走策展SOP上架，變成大台南策展中心一張「食」類店家卡片。軍師想「只是要拿掉這張錯的卡片」，用了`delete_curated_site()`（`/curation/admin/delete/<slug>`），結果這個函式做的是**整套退役**：GitHub repo改名成`_archived_<slug>`+關閉Pages+從registry移除，連帶讓已經公開發出去的`event.bymyway.com/curated/bigtree-1003/`網址直接變404——這個網址是教練已經公告過的，等於誤刪了一個正在使用中的公開頁面。事後靠`delete_curated_site()`自己函式註解裡寫的「資料只搬不刪」逐步復原：repo改名復原、重開Pages、本機資料夾搬回、registry補回（分類改標避免同款誤判）。

**Why 這條很重要**：「移除店家名冊上的一張卡片」跟「整個網站退役」是完全不同量級的操作，但在這個系統裡剛好共用同一個函式/同一顆按鈕。動手前沒有先讀函式的docstring/實際邏輯，只看函式名稱「delete」就直覺對應到「我要的效果」，是典型的「以為做小動作，結果做了大動作」。

**How to apply**：任何要「拿掉/隱藏/下架」某個已上線項目前，先讀對應函式的實際實作（不只看名稱/註解摘要），確認它的真實影響範圍跟自己想要的效果是不是同一件事——尤其當這個項目牽涉到「已經公開發出去、外部可能已經在引用的網址」時，任何操作前都要先問「這個網址会不会因此變成404」，不能假設「聽起來是軟性操作」就真的是軟性操作。同一套邏輯適用於這個系統裡任何叫「下架/刪除/移除/退役」的按鈕——名稱相似不代表影響範圍相同。

Related: [[reference_curation_sop_2026-09-06]]、[[feedback_agent_soul_files_not_synced_2026-09-17]]

**🟢 2026-10-07 已改機制（同類錯第二次，教練糾正：下架只是不展示，不能讓網站不見）**：後台 `/curation/admin` 現在是「下架（只收起策展中心卡片、網站保留）／重新上架／刪除（重複或上錯才用）」，程式 `unlist_curated_site()`／`relist_curated_site()`，測試 `event-signup/test_curation_unlist.py`。以後要「不展示」＝按下架，千萬別用刪除。過去被舊下架搬走的救回腳本 `scripts/curation_restore_archived.py`。見試金石案例107。
