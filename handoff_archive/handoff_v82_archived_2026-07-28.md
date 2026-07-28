# 軍師接力棒 · 2026-07-26 v82（Mac桌面版 Sonnet 5，結繩領導學戰報系統全功能上線+Cloudflare Token安全清理+下一場OCR工具交辦）

> 建立時間：2026-07-26 傍晚（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v81（Mac終端機Sonnet5，「教練都在想什麼」LINE帳號完整搬遷上線）
> 本棒主軸：**接手聯想機寫好的jiesheng-report程式碼，完成Mac端部署上線，過程中修好一個真bug（.env密碼雜湊被bash source吃掉導致密碼永遠登不進去），並依教練多輪追加需求把系統做完整（一次全部儲存/序號/姓名可編輯/排序/邀請人與資料提交人）。中途發現並清理2個先前seabiscuit任務遺留的Cloudflare臨時Token（安全debt清償）。尾聲教練提出Token成本疑慮，查證確認screenshot截圖真的貴，教練也回憶起namecard-db已有驗證過的PaddleOCR+MiniMax辨識管線可複用，本場對話長度已高（10+小時/30+輪）教練主動要求總結收尾，開新對話繼續做OCR通用工具。**

## 🎯 本場戰果

### 1. 🎯🎯🎯 結繩領導學工作坊戰報系統(jiesheng-report)完整部署上線
接手聯想機已寫好的Flask+SQLite程式碼，建venv+LaunchAgent(`com.coach.jiesheng-webapp.plist`)常駐port 5063(原建議5061跟既有peipei-event撞了)，Cloudflare Route(CLI+臨時API Token比照seabiscuit做法，用完即刪)接上`rpl-workshop.bymyway.com`。過程順手清掉2個seabiscuit任務遺留、忘記刪除的Cloudflare臨時API Token(安全debt清償)。

### 2. 🔴🔴🔴 真bug：.env密碼雜湊被bash source吃掉，密碼永遠登不進去
教練實測登入失敗、給出真實密碼(42710762)要我確認，本機雜湊比對(不經過網頁登入表單)發現密碼雜湊值裡的`$`符號被LaunchAgent的`bash -c "source .env"`當成shell變數展開吃掉一截。修復：`.env`裡含`$`的值一律加單引號。這條試金石早有記錄（[[feedback_settings_hook_verify]]附近文件曾提過.env含$要加引號）但這次是真的踩到才發現新專案沒套用到，教訓已寫進[[project_jiesheng_report_launch_2026-07-26]]。

### 3. 🎯🎯 歷史資料匯入15筆(台南4/台中1/台北10)
教練提供4張報名截圖(3張分場+1張金流總表)，交叉比對姓名+日期，台北10筆裡8筆有精確付款日期(比對金流總表)、2筆無金流紀錄的(含教練指定的「沒有金流的都標6/29」規則)。教練事後親自登入系統新增1筆(邱于騰)+修改1筆(林俊瑋改已繳費)，證實系統正常運作。

### 4. 🎯🎯🎯 教練多輪追加需求，系統做到「一次全部儲存」
教練反映「改一個欄位就要按一次儲存」太繁瑣，整個table改成單一表單設計，底部一個「💾全部儲存」按鈕一次送出所有列的變動；刪除維持各自獨立按鈕(不受影響)。另加序號欄#、姓名改可編輯(教練舉例「李俊國」打錯成「林俊偉」的情境)、排序改依報名日期(舊到新，最新報名排最下面)、新增「資料提交人」欄位(同帳號共用登入，用這欄記錄誰實際操作，四選一曜董/大樹/佩君/Lavi)、新增表單直接支援金流欄位(已繳費/繳費方式/金額，一次到位不用事後補)。標題「後台」字樣依教練指示全數移除，只留「即時戰報」。全部功能均用真實瀏覽器互動測試(非DOM操作)驗證通過。

### 5. 🎯 Token成本意識+找到更好的圖片辨識方案
教練發現本場截圖近40張，質疑Token消耗，查證後誠實回報「無法給精確Token數字」（沒有即時計數器）。教練指示「智慧地截圖」——同批功能改完再截一次，不要每改一處截一次，已寫入[[feedback_screenshot_rules_consolidated]]。教練接著提出用Hermes/MiniMax做圖片辨識省Token的構想，查證MiniMax-M3確實支援原生視覺輸入，但更進一步教練想起`namecard-db`已有驗證過、比直接視覺辨識更準的**PaddleOCR+MiniMax兩階段管線**(本機OCR免費+MiniMax不限流量整理成JSON，零Token成本)，已寫入[[reference_namecard_ocr_pipeline_reusable]]。

## 📋 下一場直接開工任務（教練已交辦，方向清楚不用再問）

**把`namecard-db/extract.py`的兩階段OCR管線抽成通用小工具**，不綁死名片欄位，讓「讀圖片建檔」這類任務都能複用（不用AI自己盯圖片瞇眼看，且免費/不耗Token）。
- 核心參考：`namecard-db/extract.py`的`extract_card_fields()`函式（PaddleOCR→MiniMax兩階段）、`paddle_extract.py`（獨立Python3.11環境跑PaddleOCR的子行程）
- `.env`裡已有`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`(指向MiniMax端點)/`NAMECARD_MODEL`設定可直接沿用
- 設計方向：把SYSTEM_PROMPT參數化（不寫死名片JSON schema），讓呼叫端可以傳入「這次要辨識什麼欄位」
- 下一場直接讀[[reference_namecard_ocr_pipeline_reusable]]這份記憶+上述兩支程式碼即可開工，不用重新查證能力/找檔案
