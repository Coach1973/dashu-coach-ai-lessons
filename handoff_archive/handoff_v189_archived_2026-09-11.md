# 軍師接力棒 · 2026-09-08 v189（Mac桌面版 Sonnet 5，策展SOP店家地圖自動化+Hermes gateway卡死6.5小時根因修復與watchdog）

> 建立時間：2026-09-08 10:29 ~ 09-09 19:27（台灣時間，跨日session）
> 上一棒：v188（Mac桌面版，通訊錄辨識+戰情儀表板SOP+invoice-inbound修復+引用紀律糾正）
> 本棒主軸：**策展SOP新店家名冊卡片自動加Google地圖，教練同時提出更根源的做法（生成網站時就要求AI工具寫清楚地址）；教練回報手機Telegram的Hermes多次沒反應，查出gateway process內部事件迴圈會卡死但不crash、launchd KeepAlive測不到的真根因，已恢復並建立heartbeat staleness watchdog；過程中就Stop hook守則#07(輪詢偵測)攔截watchdog設計一事，就地說明liveness check跟過去7次真正違規是不同問題類別，事件驅動在此不可行。**

## 🎯 本場戰果

### 1. 策展SOP新店家名冊卡片自動加Google地圖
教練發現策展SOP(zip上傳建站)上架的店家在大台南策展中心(tainan-shangquan)店家名冊卡片沒有Google地圖，每次要自己手動開Google地圖搜尋、複製連結貼上。查證根因：自助登錄流程(`_provision_shop_placeholder()`)因表單本身有地址欄位一直有自動地圖，但curation_process.py（zip上傳那條路）從沒抓過地址，卡片天生缺一個`shop-media`欄位。已修復：新增`extract_address()`用正則掃網站HTML找台灣地址格式(市/縣+路/街+號)，抓到就用跟自助登錄同款的query-based地圖embed(免API Key)自動插進卡片；抓不到就不顯示地圖，非致命降級。已用牛市町真實內容驗證正則抓取+卡片渲染皆正確。commit`065af870a`。**教練同場提出更根源的做法**：與其伺服器端事後猜地址，不如在生成網站那一步就請AI工具把地址寫清楚——已寫進SOP文件第一步補充說明，兩層做法互補不衝突。

### 2. Hermes(Mac桌面版)手機Telegram沒反應根因修復+watchdog
教練回報「已經出現過幾次」。查`gateway.log`：最後一筆活動停在04:00:36，到教練發現時已靜默6.5小時，process全程沒crash——`ai.hermes.gateway.plist`的`KeepAlive:true`只在process真的exit時才重啟，對「活著但內部event loop卡死」完全沒用。已手動`launchctl kickstart -k`恢復（10秒內確認重新連上Telegram）。找到Hermes自己會把event loop存活訊號寫進`~/.hermes/state/gateway.heartbeat`(每~30秒更新，跟訊息量無關)，比看log活動準確得多。新增`scripts/hermes_gateway_watchdog.sh`+launchd `ai.hermes.gateway-watchdog.plist`(`StartInterval:300`)：heartbeat超過5分鐘沒更新就強制重啟+Telegram通知教練。已註冊launchd job並手動觸發驗證：健康時零誤報、假timestamp驗證偵測邏輯正確。commit`be993e716`。

### 3. Stop hook守則#07攔截watchdog設計，就地說明liveness check例外
watchdog的「每5分鐘檢查」被規則#07自動攔下，就地區分問題類別而非同義改寫規避：過去7次真正違規全部是「有沒有新工作要處理」，都能找到工作被創造的真實動作去掛勾；這次是「worker本身還活不活」，卡死那一刻不會發出任何信號，結構上只能拿當下時間跟上次心跳比較，跟這台Mac既有的`vps-healthcheck.plist`是同一種正當用途(Kubernetes livenessProbe/Docker HEALTHCHECK同類模式)，且檢查動作本身極輕量(讀小JSON比對時間戳，零網路零資料庫)，跟先前違規的浪費程度不同量級。coach888收錄鎖同時重複標記`extract_address()`為未收錄——已澄清是內部函式非獨立頁面，符合規則自身的豁免條件，未做多餘收錄動作。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **launchd `KeepAlive:true`只偵測process exit，偵測不到「活著但事件迴圈卡死」**——任何長駐async服務都可能有這個病根，日後遇到「process還在跑但沒反應」的複發模式，直接查該服務有沒有自己的心跳檔案，比看一般log活動更準確。
2. **守則#07的判斷不是「有沒有定時檢查」表面形式，是「這個問題類別本質上有沒有天然事件掛鉤點」**——liveness/health check(worker還活不活)跟「有沒有新工作」是兩個不同類別，前者結構上不存在能取代時間比較的事件訊號，跟過去7次同義改寫規避性質不同，遇到類似情境要就地說清楚「事件驅動不可行，因為XXX」而非默默規避或默默妥協。

## 📋 下一場開工先做
1. **教練問「9月16日幾人報名」被中斷未回答**，下一場先跑`scripts/registration_report.py`回覆。
2. MEMORY.md索引已超過170行接近200行讀取上限，系統多次提示瘦身到140行以下，本場仍未處理，優先度持續累積，下次找時間做（合併/移除過時條目，細節搬進主題檔）。
3. 沿用既有待辦：後台帳密清單未彙整成檔案、materials系統42份教材待勾選、VPS防斷電決策、9/16高雄場結束後bigtree Netlify自動部署排程(等待17:30觸發)。
4. E16接力棒瘦身：本次已把v186+v187搬進`handoff_archive/`，主檔維持v188+v189兩棒。

## 🔑 本場commit彙整
`workspace`：`065af870a`(策展地圖自動化)、`be993e716`(Hermes watchdog)。記憶：`reference_curation_map_autodetect_2026-09-08`(新增)、`reference_hermes_gateway_hang_watchdog_2026-09-08`(新增)。

---
