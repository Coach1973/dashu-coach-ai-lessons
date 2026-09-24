---
name: feedback-cross-check-both-ezpay-systems-before-reporting-missing
description: 查BNI會員的統編/手機條碼，要同時查「聚寶盆入會續約」跟「大樹教育培訓費」兩個獨立ezPay系統，不能只查當前任務對應的那一個就回報查無資料
metadata:
  node_type: memory
  type: feedback
  originSessionId: f5284690-7a90-4097-9918-9cbfb59c5ce2
  modified: 2026-09-23T09:22:47.197Z
---

查某位BNI會員的統編或手機條碼「找不到」之前，必須把兩個獨立的ezPay發票系統都查過一輪，不能只查跟當前任務同名的那一個。

**Why：** 2026-09-23開立聚寶盆(入會續約)發票時，只查了入會續約系統的CSV/remarks資料，回報陳穗青、康文彬「查無手機條碼」，教練兩次當場質問「他明明常上培訓，你怎麼會找不到」。查`claude-brain/data/build_bni_training_admin.py`（培訓費系統的既有資料字典）才發現這兩人的手機條碼其實早就存在那邊（陳穗青`AMU2DXY`、康文彬`B3BU7PV`），跟教練後來親口補的號碼完全吻合。更糟的是，同一個教訓在同一場對話裡連續犯了兩次——第一次抓到陳穗青漏查後，口頭上說了「以後查任何會員資料一律兩邊都查」，但第二次遇到剛確認身份的康文彬時，這條新規則沒有真的套用到他身上，又被教練用同一句話點破一次。

根因不是資料真的沒有，是查證範圍預設縮小到「跟當前任務同名的那個系統」——[[feedback_bni_invoice_two_independent_systems_sop]]雖然明講兩套系統「完全獨立、禁止互相比對發票紀錄」，但那條規則講的是「不能拿一邊的發票記錄去核對另一邊有沒有開過」，不是「聯絡資料（統編/手機/Email）不能互通查詢」——這兩件事被搞混了，導致該查的地方沒查。

## How to apply

1. 任何時候要確認某位BNI會員的統編、手機條碼、Email、電話——只要「查無資料」，先自問「另一個ezPay系統(入會續約 vs 培訓費)有沒有查過」，兩邊都查過都沒有才能回報「真的缺」。
2. 兩個系統的資料源：入會續約查`claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv`+`ezpay_invoice_remarks_108taxid_2026-08-17.csv`；培訓費查`claude-brain/data/build_bni_training_admin.py`裡的`TAX_INFO`/`PHONE`字典。
3. 這條規則只套用在「聯絡資料查詢」，不影響[[feedback_bni_invoice_two_independent_systems_sop]]原本「發票開立紀錄/有沒有付過款不能跨系統核對」的鐵律——兩者不衝突，分別管不同的東西。
4. 一次任務裡有多位對象要查時，每一位都要照這個流程走一遍，不能因為前面幾位已經套用過規則，就對後面新出現、剛確認身份的對象大意省略。

Related: [[feedback_bni_invoice_two_independent_systems_sop]]（發票紀錄不可跨系統核對的鐵律，跟本條互補不衝突）
