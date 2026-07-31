# 軍師接力棒 · 2026-07-28 v84（Mac桌面版 Sonnet 5，AI微型論壇7/29籌備衝刺：簽到系統重構+多站內容更新）

> 建立時間：2026-07-27 深夜～07-28 上午（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v83（Mac桌面版Sonnet5，系統權限缺口解決+開工額度瘦身）
> 本棒主軸：**教練密集為7/29「AI微型論壇」籌備做最後衝刺，本場處理6件獨立任務，多數當場教練實測/確認後結案。核心戰果是event-signup簽到系統重構——教練發現來賓線上報名後現場掃碼還要重填資料，設計出「手機號碼比對」新流程，免重填又保留集點功能，教練親自實測通過。另完成bymyway.com/ai/品牌頁三輪內容改版、event.bymyway.com場次資料校正、ai-talk-tw.netlify.app兩次數據更新(甜點份額、報名人數)、OCR通用工具教練驗收確認採用。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 event-signup簽到系統重構：手機號碼比對，免重填資料又保留集點功能
教練指出`event.bymyway.com/qr/checkin-print.html`(現場簽到QR立牌)的問題：來賓在`bigtree-tw`/`ai-talk-tw`網站報名時已留過姓名/電話，現場掃碼進`/checkin`卻要整份表單重填一次，多此一舉。過程分三階段收斂：
1. 第一版直接把QR改指向`/slides`(加好友+下載簡報，零輸入)，但教練指出這樣會失去「集滿5次活動送禮物」的簽到紀錄功能
2. 教練提出「我的紙本簽到表本來就有手機號碼」的思路，追問是否還需要數位輸入
3. 最終定案：`/checkin`拆成GET(手機輸入頁)+POST(比對邏輯)——輸入手機號碼比對`attendees`表，比對成功記進`signups`表(集點功能保留)+導向`/slides`顯示個人化「OOO，簽到成功」；查無資料的現場臨時來賓才導去完整表單(手機號碼已預填，只需補姓名)。用真實資料(已知電話/未知電話/格式錯誤)三種情境本機測試通過，教練實測確認採用。commit序列：`fd480212a`→`022051eba`→`0ef5ee98a`。7/29立牌已印好，QR網址沒變不用重印。

### 2. 🎯🎯 bymyway.com/ai/ 品牌頁三輪內容改版
GitHub Pages(`coach1973.github.io/bymyway-website/ai.html`)透過iframe嵌入`bymyway.com/ai/`。教練分三輪交辦：①案例清單新增「大樹小講．無話不談」、移除「AI特助案例集」「特助心法專屬頁面」兩項舊連結 ②CTA區塊文字簡化為「真實案例公開上線」，按鈕改連`coach1973.github.io/coach-case4/` ③新增「近期活動」按鈕連到大樹小講。每次改動都先用Chrome本機預覽給教練看過才推，commit `f8a7a89`，GitHub Pages約1分鐘內自動生效。

### 3. 🎯 event.bymyway.com/admin 場次資料校正
教練告知8/1場次已取消，改為8/26、9/5、9/19三場，比對`bigtree-tw.netlify.app`線上場次資料(topic/時段/地點)校正到`event.db`。確認8/1場次0人報名可安全刪除，三個新場次的`/e/<slug>`報名頁curl驗證正常顯示。同時回答教練「綁定/未綁定」判斷邏輯的疑問——查證LINE webhook原始碼確認：綁定要求來賓傳送固定格式文字「我是OOO，剛報名了」，webhook只處理`message.type=="text"`，**單純傳貼圖/表情符號不會觸發綁定**(教練原本以為表情符號算數，已當場更正)。

### 4. 🎯 ai-talk-tw.netlify.app 兩次數據更新
①甜點下午茶限量份數60→50份(兩處：入門禮段落+煦多午茶設攤卡片同步)，commit `52ff47a`；②已報名人數重新校準為88、遞增速率從「每6小時+1人」改「每3小時+2人」(教練回報現場報名超過88位)，commit `16d72b4`。部署前發現本機GitHub工作稿落後聯想機4個commit(缺現場設攤廠商卡片)，先`git pull`同步再改，避免蓋掉別台機器的成果。兩次都用Chrome本機預覽+curl驗證文字/圖片Content-Type後才推，Netlify quota紀錄同步更新(`state/netlify_deploy_quota.json`)，目前剩64次。

### 5. 🎯 OCR通用工具教練驗收+使用範圍界定
教練詢問建置OCR工具的原始動機，查證`reference_namecard_ocr_pipeline_reusable`記憶檔確認源頭(教練親自讀截圖時看錯陳慧雯→陳薏雯的真實案例)後準確回答。教練確認「之後讀圖片文字改用OCR」的方向，本場也順手釐清使用界線：**讀字→用OCR；看畫面(排版/設計判斷)→AI還是要自己看**，避免教練誤以為所有圖片任務都能靠OCR繞過。

## 📋 下一場直接開工任務

教練本場結束時表示「有新的Netlify的更新要做」，**但尚未說明具體內容**——會開新對話框交辦，下一場先問教練這次要更新哪個站、改什麼，不用預先假設。另外仍有queue中的舊任務：
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，多場未動手，優先度最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）

## 🔑 本場關鍵檔案索引
- `event-signup/app.py`：`/checkin`拆GET+POST、`/slides`新增`name`參數個人化、`/e/<slug>`支援`phone`預填
- `event-signup/templates/checkin.html`：新模板，單一手機號碼欄位
- `event-signup/make_qr.py`：`make_checkin()`新增`event_label`參數
- `github_repos/bymyway-website/ai.html`：案例清單+CTA三輪改版
- `github_repos/ai-talk/index.html`：甜點份數+報名人數公式
- `state/netlify_deploy_quota.json`：本場3次部署紀錄(ai-talk-tw×3)
- commit序列：`f8a7a89`(bymyway.com/ai) → `52ff47a`(甜點份數) → `fd480212a`→`022051eba`→`0ef5ee98a`(簽到系統) → `16d72b4`(報名人數)
