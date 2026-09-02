---
name: feedback-bni-invoice-two-independent-systems-sop
description: BNI相關發票是兩套完全獨立的系統(大樹教育培訓費 vs 聚寶盆入會續約)，教練已提供全部會員資料+2年發票歷史，開票前不用再問資料在不在，直接查
metadata:
  node_type: memory
  type: feedback
  originSessionId: fa97ce20-02cc-40c2-aaad-1ba7f3961669
  modified: 2026-09-03T01:58:00.000Z
---

**教練原話（2026-09-03）**：「我要強調的是，你本來就擁有全部的資料。過去讓你開過發票的，都有讓你搜尋近兩年已經開過發票的會員，而且近兩年有開過發票的會員，備註欄上面一定會寫他是哪個分會、叫什麼名字。換句話說，你那邊擁有了整整兩年我曾經開過新加入或續約發票的資料庫。你不能跟我說你沒有這個資料。」「本來開發票這件事情，我們並沒有特定的網頁，我都是直接在我們的APP裡面對你下指令……你作為賈維斯的系統，這些曾經做過的事情，你都不應該在這個時候來問我。」

**Why：** 我在被問「BNI培訓紀錄後台是什麼」時，把「入會續約發票」跟「培訓費發票」混著問，讓教練覺得我不知道自己早就擁有2年發票歷史資料。這跟[[feedback_dont_reverify_stated_requirements_2026-08-28]]、[[feedback_jarvis_outcome_delegation_style]]是同一種模式的再次發作——只是這次不是「重新查證教練說過的話」，而是「該用的資料明明手上就有，卻表現得像沒有」。

## 兩套完全獨立的發票系統（禁止互相比對/混用）

| | 大樹教育・培訓費 | 聚寶盆・入會續約 |
|---|---|---|
| 商店代號 | 337643900 / 344031309 | 337391376 |
| 金額量級 | $300 ~ $1,800 | $24,000 ~ $39,800 |
| 頻率 | 每月（每次培訓場次都可能開） | 每年一次 |
| 對象 | 只有「有上培訓」的會員，不是每個會員都有；教練會主動告知哪些人上了培訓 | 全體會員，新加入或續約 |
| 二聯式規則 | 要區分「有條碼」vs「無條碼（僅Email）」 | 同左，看買受人是否提供手機條碼 |
| 三聯式規則 | 一定有抬頭（公司統編） | 同左 |
| 現有資料 | `claude-brain/data/build_bni_training_admin.py`（61人出席+統編+電話+歷史發票比對，重跑腳本可更新） | `claude-brain/data/ezpay_invoices_2024-01-01_to_2026-08-17.csv`（238筆2年完整發票匯出，含發票號碼/統編/金額/日期）+ `ezpay_invoice_remarks_108taxid_2026-08-17.csv`（108個統編→分會+姓名備註對照，公司發票靠這份查回是誰）+ 各批`ezpay_bni_*完成清單.json`（最新一批開票明細） |
| 私有後台網址 | `namecard.bymyway.com/invoice-admin/training`（教練帳號登入） | `namecard.bymyway.com/invoice-admin/membership`（教練帳號登入） |

**兩者的唯一交集**：一個人要能收到培訓費發票，前提是他必須先是會員（=入會續約系統裡有他）。但這只是「人」的交集，不是「發票資料」的交集——**培訓費歷史發票不能拿來核對入會續約有沒有開過，反之亦然**，這是教練2026-09-03明確裁示的鐵律，`build_bni_training_admin.py`腳本裡也早就寫死這條警語。

## How to apply

1. 教練說「開票」「續約發票」「入會發票」時，**不要問「這個資料你有嗎」**——直接去查上面對應的資料源，或直接開`/invoice-admin`底下對應頁面搜尋姓名。
2. 兩份私有後台都掛`namecard-db`既有的`owner_only_required`真登入（跟`/bni-credit`同一套帳密機制），2026-09-03之前的舊版`bni_training_admin.html`只靠`<meta robots noindex>`裸奔，已改為真的登入保護——因為裡面是全體會員的統編/電話/Email等個資。
3. 資料要更新時：培訓費改`claude-brain/data/build_bni_training_admin.py`裡的`PEOPLE_RAW`/`TAX_INFO`等字典重跑；入會續約改`claude-brain/data/build_bni_membership_admin.py`（新增更多`COMPLETION_FILES`批次或重新匯出2年CSV），重跑`python3 build_bni_membership_admin.py`後兩份html會自動更新，Flask路由直接讀最新檔案內容，不需要重啟服務。
4. 入會續約發票的姓名比對邏輯（可能還會踩到）：CSV裡「買受人統編」="-"代表個人發票，買受人名稱本身就是會員姓名；統編不是"-"代表公司發票，姓名要查remarks CSV的「發票備註」欄位（格式不一致，可能是「OO分會-姓名」或「OO-姓名」，也可能寫的是業務描述而非人名，查不到就誠實列在「無法比對」清單，不硬猜）。

Related: [[feedback_dont_reverify_stated_requirements_2026-08-28]]、[[feedback_jarvis_outcome_delegation_style]]、[[reference_ezpay_invoice_issuing_procedure]]、[[reference_bni_membership_fee_history_and_chapter_transfer]]
