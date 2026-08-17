---
name: project-bni-training-records-db-2026-08-17
description: BNI培訓紀錄總資料庫，公開版(GitHub Pages)+私有版(開票後台)雙軌架構，2026-08-17聯想機建置
metadata: 
  node_type: memory
  type: project
  originSessionId: a2d56982-4a3f-4d1d-ac83-1ccd1e463040
  modified: 2026-08-17T11:59:40.636Z
---

教練要求仿照 [[project_bni_dna_attendance_dashboard_2026-07-08]] 建一份「1月至今」BNI培訓出席資料庫。整併三份資料源（出席原始資料61人次6場次、會員發票統編對照docx、ezPay培訓費發票CSV）後，教練當場拍板兩層架構：

**公開版**：`github.com/Coach1973/BNI-Training`（GitHub Pages，`https://coach1973.github.io/BNI-Training/`），只放姓名/分會/6場次出席狀態，教練親口「完全公開像bni-dna」。

**私有後台**：`mac-openclaw-workflows/claude-brain/data/bni_training_admin.html`（私有repo，GitHub上is private），多帶統編/個人ezPay載具/email/累計應收金額/歷史發票比對，教練原話「後台要方便我做事，我需要統編或手機條碼、電郵、電話，以方便開立發票」。電話欄位目前完全沒有資料來源，留空待補。

**Why**：會員的統一編號/個人載具/email屬於他人的財務個資，公開曝光跟教練自己的隱私立場（[[user_privacy_risk_posture]]，優先便利不介意公開）是兩回事——那份是教練談自己，這份牽涉61位BNI會員的個資，先問過教練才決定架構是正確判斷，不能直接套用bni-dna的完全公開precedent。

**How to apply**：以後任何「仿照XX既有站台」的需求，如果新資料裡包含「原站台沒有的個人financial/聯絡資訊」，先問公開範圍，不要預設沿用舊站台的公開程度。兩份資料的出席事實(PEOPLE_RAW)要保持同步，改一邊記得改另一邊，各自有build script（`build_data.py`+`build_html.py` in BNI-Training；`build_bni_training_admin.py` in claude-brain/data）。

**踩過的坑**：
- 整理時發現原本「另一視窗」做的60人交叉比對報告(`cross_ref_report.md`)漏收「陳穗青」1人（她有7/20出席記錄+個人載具代碼），已更正為61人，並在兩份頁面的說明區塊誠實揭露這個修正。
- ezPay發票CSV有兩種完全不同類別要分清楚：`damushu_jiaoyu_invoices_1year`（店代337643900/344031309，培訓費$300~$3000量級）才是這次要比對的；另一份`ezpay_invoices_2024-01-01_to_2026-08-17`（店代337391376/BNI台南南區，$24,000~$39,800量級）是入會/續約費，完全不同類別，不能混用去比對培訓應收。
- Windows bash的cwd若停在某個目錄裡，`mv`該目錄會報「Device or resource busy」，要先cd出去或改用cp+新目錄的方式繞過。

**2026-08-17同日second round擴充**：教練緊接著貼出`D:\Users\Downloads\培訓紀錄.xlsx`——這是BNI Connect官方匯出的「地區會員培訓報告」，涵蓋大台南南區全部5分會(真富/真愛/真誠/真鑫/真鑽)、2018~2026共753筆、87位會員，跟先前的MSP資料完全是不同track（官方董事培訓/領導團隊培訓/會員成功專案/Workshop，不是教練自訂的MSP課程）。教練要求做成「網頁App」：首頁時間窗篩選(3/6/12/18/24個月/全部，預設6個月)+TOP10個人排行(要有「表揚」感，podium+金銀銅牌)+分會排名比較。已建置：
- `BNI-Training/index.html`（新首頁，取代原本的MSP頁面成為主要入口）+ `region_build_data.py`/`region_build_html.py`/`region_template.html`，純前端JS即時運算（753筆瀏覽器算綽綽有餘，不用後端）。
- 原MSP版本改名保留在`BNI-Training/msp.html`（`msp_build_data.py`/`msp_build_html.py`），兩頁互相有連結，沒有丟失舊工作。
- 原始xlsx+完整欄位(含電話/email)存進私有repo：`claude-brain/data/bni_region_training_raw.json` + `bni_region_training_report_source.xlsx`（備份，避免依賴Downloads資料夾可能被清掉）。
- **意外之喜**：這份官方報表帶電話+email，跟MSP 61人名單比對姓名後45人對上號，直接填補了私有後台`bni_training_admin.html`原本「電話完全無來源」的缺口（用`build_bni_training_admin.py`的`PHONE`字典，姓名比對，非100%涵蓋，還有16人查無比對）。

**How to apply(更新)**：教練給新資料源時，先確認這是不是同一個「培訓」概念下的不同track（這次MSP vs BNI官方培訓是兩條平行資料，不能合併成一份，但可以互相補值，例如這次用官方報表的電話回填MSP名單）。「首頁」這個詞教練是指真正的入口頁(index.html)，舊內容不刪除但要讓路、改用次頁保留。

Related: [[project_bni_dna_attendance_dashboard_2026-07-08]]、[[reference_ezpay_invoice_issuing_procedure]]
