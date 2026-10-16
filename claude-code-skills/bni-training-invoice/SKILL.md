---
name: bni-training-invoice
description: BNI 培訓費／入會續約發票相關時使用——「某某開過票沒」「是二聯還是三聯」「統編多少」「欠多少」「幫某某開發票」「開票」「ezPay」。先查紀錄再動手；開票前跟教練確認金額與買受人；開成功同一輪寫回紀錄。
---

# BNI 開票（完整做法在記憶 reference_ezpay_invoice_issuing_procedure、feedback_ezpay_invoice_sop）

## 只是查
`python3 ~/.openclaw/workspace/claude-brain/data/query_training_invoice.py "<姓名>"`，把輸出直接回教練。**不要反問二聯還是三聯**——開過票的人，類型／統編／載具／歷史發票都已記錄。

## 要開票
1. 先查（上面那支）有沒有開過、上次的統編與類型。
2. **送出前一定跟教練確認**：買受人、統編（或二聯）、品項、含稅金額。這是代表教練對外開立的單據，沒有確認不送出。
3. ezPay（inv.ezpay.com.tw，帳號 bymyway）兩個商店別選錯：`337391376` BNI 台南南區（入會／續約）、`344031309` 大樹教育顧問（培訓費）。商店下拉選單看起來選了其實沒選，要用程式設 `MerchantID` 再觸發 change。
4. 自訂編號＝當天 MMDD＋兩碼流水號，開前先查當天有沒有人開過。查詢區間最長 3 個月，超過會跳 alert 把分頁卡死——每到新頁先覆蓋 `window.alert`。
5. 送出前讀 `TotleAmount` 核對等於教練講的含稅金額；送出後「頁面重新整理／連線中斷」常是成功徵兆，要用查詢確認發票真的存在。
6. **確認存在的同一輪**，把這筆寫進 `claude-brain/data/build_bni_training_admin.py` 的 `TAX_INFO`／`PHONE`／`INVOICES` 並重跑產生頁面——不能拖到之後（9/7 張育慈那張就是沒當場記，卡了兩天）。
7. commit＋push（workspace 分支 main），回報教練：發票號碼＋金額＋commit hash。

## 登入
ezPay 登入狀態每台電腦分開。這台沒登入 → 請教練在這台的 Chrome 登入一次（密碼不經過 AI）。
