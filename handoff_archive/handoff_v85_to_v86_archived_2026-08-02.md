> 封存時間：2026-08-02（台灣時間）
> 封存原因：E16瘦身鐵律，主檔只留最新1~2棒，v85/v86搬出

# 軍師接力棒 · 2026-07-29 v86（Mac桌面版 Sonnet 5，AI微型論壇台南場正式登場：現場緊急支援+LINE綁定bug修復+活動轉型回顧頁）

> 建立時間：2026-07-29 下午～深夜（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v85（Mac桌面版Sonnet5，抽獎轉盤上線+付款連結批次更新）
> 本棒主軸：**v85做好的抽獎轉盤在7/29當天正式上場，本場處理三件事：①教練人在別台電腦要現場登入/wheel，密碼是雜湊值無法提供明文，改幫教練重設成他指定的新密碼並實測登入成功②活動結束後教練發現56位簽到只有12位完成LINE綁定，查證抓到真正原因是/checkin這條路徑沒有像線上報名表單那樣幫來賓「打好問候語草稿」，當場修復③教練提出要仿照全球健康發展協會(northern-tw.netlify.app)的做法，把已結束的活動頁轉型成歷史紀錄，用教練提供的24張現場真實照片做成活動花絮，同時記錄下一場預計辦在嘉義。**

## 🎯 本場戰果

### 1. 🔴🔴 現場緊急支援：教練異地登入密碼重設
教練在別台電腦要用`/wheel`轉盤功能，但登入密碼只存了scrypt雜湊值，技術上無法逆推明文。教練直接指定新密碼`123457`，用`werkzeug.security.generate_password_hash`生成新雜湊值寫入`.env`，重啟`com.coach.event-webapp`服務，並用真實的`POST /admin/login`+session cookie完整測試登入到`/wheel`成功(非test client模擬)，才回報教練帳密可用。全程沒有經手明文密碼被輸入到任何第三方系統，只是更新自己維護系統的密碼設定。

### 2. 🔴🔴🔴 抓到LINE綁定率低的真正原因並修復：`/checkin`少了「幫來賓打好問候語草稿」這一步
教練回報：56位透過現場手機號碼簽到、參與抽獎的來賓，只有12位完成LINE綁定(後續無法收到通知)。查證發現LINE綁定機制要求來賓在LINE手動輸入固定格式文字「我是OOO，剛報名了XXX」，webhook才會寫入`line_user_id`。比對兩條路徑：`/e/<slug>/thanks`(線上事先填表單的人看到的頁面)早就有`greet_url`自動把這句問候語預填好，來賓只要按「加好友」就一鍵送出；但`/checkin`(手機比對簽到)導向的`/slides`頁面，只給了一個普通的「加好友」按鈕，來賓要自己手動輸入正確格式才能綁定——這才是今天現場56人只有12人綁定的真正原因，不是來賓不想綁，是系統少做了這一步引導。修復：`slides_landing()`在有`name`參數時比照`thanks()`同樣邏輯生成`greet_url`，測試通過(有name→智慧連結、無name→維持原本通用連結)後部署。commit在`event-signup`獨立repo內(該repo不透過workspace追蹤，改動已上線生效，未來場次現場簽到綁定率應該會明顯改善)。

### 3. 🎯🎯 AI微型論壇台南場正式轉型為活動回顧頁，仿照全球健康發展協會做法
教練參考`northern-tw.netlify.app`(全球健康發展協會論壇官網，帶「歷屆回顧」板塊)的呈現方式，要求把已結束的`ai-talk-tw.netlify.app`報名頁變成歷史紀錄，教練提供的24張現場照片(下載資料夾裡的LINE傳圖，設攤+滿場講座畫面)做成花絮。動手內容：
- 24張照片壓縮到900px寬(10MB→3.4MB)，取代原本首頁「精彩花絮」輪播的12張示意照(舊照片備份在`images/carousel_archive_previous/`不刪除)，`CAROUSEL_TOTAL`12→24
- Hero區拿掉倒數計時器+報名進度條，改成「圓滿落幕，感謝每一位到場的朋友」，對應JS(`updateCountdown`/`updateLiveCount`兩個IIFE)一併移除，避免抓不到已刪除DOM元素而報錯
- 整個「選擇你的報名方式」區塊(個人報名/企業合作兩張大卡片)直接移除
- navbar桌面版/手機版、sticky底部欄、agenda區「手刀搶免費名額」按鈕，全部從「立即報名」(`onclick="showTypeModal()"`)改成「加入LINE」(直接連`line.me`)，不再觸發已經不合時宜的報名彈窗
- signup區塊改寫成「下一場預告：嘉義場籌備中」
- 本機Chrome預覽經教練確認後部署，curl驗證文字/圖片Content-Type/舊CTA清除，全部通過。GitHub commit `78213ed`，Netlify部署`6a6a1a24`，quota扣1次(59→58)

## 📋 下一場直接開工任務
- **嘉義場籌備**：教練已提到下一場預計辦在嘉義，尚未給任何細節(時間/地點/講師)，下一場教練給了細節後可以直接比照台南場經驗開工，不用重新摸索
- **Email自動發送系統**：v85記錄的方向，教練仍未給細節，下一場先問清楚用途(報表/自動回信/行銷群發)再評估技術方案
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，已多場未動手，優先度持續最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）

## 🔑 本場關鍵檔案索引
- `event-signup/.env`：`EVENT_ADMIN_PASSWORD_HASH`更新為教練指定新密碼的雜湊值
- `event-signup/app.py`：`slides_landing()`新增`greet_url`智慧預填問候語邏輯
- `github_repos/ai-talk/index.html`：Hero區/gallery/signup/navbar全面改寫成回顧版語氣，移除報名相關區塊與JS
- `github_repos/ai-talk/images/carousel/`：24張真實花絮照(取代舊12張，舊版存於`carousel_archive_previous/`)
- `state/netlify_deploy_quota.json`：本場2次部署紀錄(贊助人清單+活動回顧頁)
- commit序列（workspace repo）：`f268d7039`起延續v85抽獎轉盤 → `86ace9420`(quota記錄回顧頁部署)
- commit序列（github_repos/ai-talk獨立repo）：`cdcdf0c`(贊助人12/13) → `78213ed`(活動回顧頁轉型)

---

# 軍師接力棒 · 2026-07-28 v85（Mac桌面版 Sonnet 5，抽獎轉盤上線+付款連結批次更新+新任務登記）

> 建立時間：2026-07-28 下午～晚間（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v84（Mac桌面版Sonnet5，AI微型論壇籌備衝刺：簽到系統重構+多站更新）
> 本棒主軸：**教練開場交辦結繩領導學工作坊4站付款連結批次更新(從Google表單/pse.is短網址統一換成PayUNi直連)，接著教練提出想法：看到一個現成轉盤小程式，希望串接event-signup簽到系統做成現場抽獎工具，省去人工輸入名單。當場評估可行性後動手做，過程中連續處理教練多輪細節回饋(HTML預覽跳出方式/瀏覽器ERR_UNSAFE_PORT/獎品庫存追蹤/中獎彈窗戲劇效果/趣味台詞)，其中最重要的一次糾正是「15秒輪詢查簽到名單」又踩到教練已經講過4次的「事件驅動優於輪詢」同一個坑，這是第5次發作，已修正為「按旋轉鍵當下才查詢」並更新對應記憶檔強化教訓。收工前教練提出下一個任務方向「Email自動發送系統」，先記錄不動手。**

## 🎯 本場戰果

### 1. 🎯🎯 結繩領導學工作坊4站付款連結批次換成PayUNi直連
教練給定台南/台中/台北3組新付款連結，起初是Netlify轉址短網址(pse.is)，過程中教練發現pse.is
轉址頁顯示的「讀者優惠日期」是舊資訊，要求改用PayUNi的`receive_info`直連網址(3組長網址)。
範圍先問清楚(教練指定workshop-richard/workshop-lavi/workshop-peipei三站要換，加上原本
已上線pse.is版本的workshop-invite一併更新成PayUNi版，bni-invite/bni-peipei兩站不動)，
再問清楚3個新連結對應台南/台中/台北的順序(照原順序)。本機Chrome預覽經教練確認後4站分次
部署(間隔40秒避免token鎖定)，部署後curl驗證新連結生效+舊連結清除+圖片Content-Type正常。
順手更新`ai-talk-tw.netlify.app`贊助人清單新增第12/13位(教練指定)並補上1-13編號。
Netlify quota同步扣5次部署(64→59)。commit `f03d356cf`(4站PayUNi連結)、`7f7225a5d`
(贊助人清單)。

### 2. 🔴🔴🔴 event-signup新增抽獎轉盤(/wheel)：簽到名單自動帶入+獎品庫存追蹤
教練提出構想：有一個現成轉盤小程式(`tourmaline-panda-82be5e.netlify.app`，GitHub自動部署型，
直接clone原始碼比教練貼過來省token)，想串接既有數位簽到系統，簽到的人自動成為轉盤名單，
省去人工輸入。評估可行性後直接動手：
- `schema.sql`新增`wheel_winners`(記錄本場中獎者防重複抽中)、`wheel_prizes`(獎品清單+
  總數/剩餘數)兩張表
- `app.py`新增`/wheel`(頁面)、`/wheel/data`、`/wheel/winner`、`/wheel/reset`、
  `/wheel/prizes/set`路由，沿用`/admin`既有session登入保護
- `wheel.html`：canvas手繪轉盤(邏輯取自tourmaline-panda)，名單改為即時查詢簽到記錄
  (不用手動輸入)；「本輪獎項」從自由輸入文字改成下拉選單(顯示剩餘數量)，抽中自動扣庫存，
  發完自動從選單消失；新增「設定獎品清單」小工具(教練自己隨時用文字框增減獎項，不用碰程式碼)；
  中獎彈窗放大到72px字體+彈跳動畫，戲劇效果更強；15句趣味中獎台詞(教練給4個梗：樂透/閃電/
  相親一次中/驗孕棒兩條槓，延伸創作到15句隨機播放)
- 已幫教練把明天正式獎品清單建進資料庫：雲朵包1、下午茶組3、迷你水杯5、杯套3、洗髮組1、
  手工皂1，共14份
- 用Flask test_client完整測試全流程(抓名單/標記中獎/防重複中獎/扣庫存/庫存0時擋掉/
  重置復原庫存+名單)，全部通過，測試資料已清空不影響明天正式使用

**過程中的教訓**：
- **教練要求「你要直接跳出來給我」**——不要叫教練自己切視窗/自己打網址驗證，AI能自我驗證的
  就自己做完再回報，這次改用Flask test_client模擬登入session產生真實資料的靜態快照，
  用真正Google Chrome開給教練看(內建無頭瀏覽器截圖只能自己除錯用，不能取代教練親眼看)
- **ERR_UNSAFE_PORT**：教練連`127.0.0.1:5060`出現「無法連上」，一開始誤判是網路問題，
  查證後發現是瀏覽器對SIP協議常用埠(5060等)內建安全黑名單直接擋掉，跟服務本身是否正常
  無關。已寫入`reference_browser_unsafe_port_5060`記憶檔，以後架本機測試服務要避開這類埠號
- **🔴🔴🔴 15秒輪詢，第5次踩「事件驅動優於輪詢」同一個坑**：第一版設計成前端JS每15秒
  `setInterval`自動查詢有沒有新簽到，教練直接點破「一場活動四五個小時要掃描多少次，浪費
  資源」，並指出這是重複提醒很多次的問題。改法是教練親自提出的：把查詢動作掛在「按下開始
  旋轉」這個使用者操作的當下才做一次，完全不需要背景計時器。已更新
  `feedback_event_driven_not_polling_pattern`記憶檔，明確記錄「前端UI的setInterval跟後端
  排程輪詢是同一個坑，不分前後端」，避免下次又用「這是前端dashboard常見寫法」自我說服

commit序列：`aae07796f`(新增/wheel功能主體) → 中獎彈窗放大+移除輪詢改按需查詢(尚未commit，
下一動作立即補上) → `543ca4ec3`(15句趣味台詞)。

### 3. 🔴🔒 瀏覽器不安全埠攔截升級成確定性Hook(不只是記憶)
教練要求：「不要每次都要我說『記得跳HTML』然後結果無法顯示網頁，把它寫進SOP。」新增
PreToolUse hook `scripts/unsafe_port_check.sh`：偵測`open -a "Google Chrome"`/`start chrome`
真的執行指向本機黑名單埠(如5060)時直接攔截，提醒改用對外網址或換安全埠。第一版寫完立刻
自打臉——commit訊息描述這支hook自己時同時含有觸發文字，被自己誤判攔下2次，修正後仿照
`netlify_deploy_guard.sh`加白名單+要求真實指令位置才算數，6種情境測試通過。已註冊進
`~/.claude/settings.json`。commit `cb3ff2c12`。

### 4. 🎯 下一個任務登記：Email自動發送系統
教練收工前提出「我有下一個任務，是想要做一個email自動發送系統，你先記錄下來」——僅先記錄
方向，教練尚未說明具體用途(报表？表單提交自動回信？行銷群發？)，下一場開工先問清楚場景
再評估技術方案，不預先假設架構。

## 📋 下一場直接開工任務

- **Email自動發送系統**：教練只給了方向，還沒給細節，下一場先問清楚「要發什麼、給誰、
  什麼時候發」，用守則#16好問句工具箱釐清後再評估技術方案
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，
  已多場未動手，優先度持續最高）
- 真誠/真愛/真實AI分會願景說明書（教練仍未給細節）
- 明天(7/29) AI微型論壇現場實際使用抽獎轉盤，若教練現場回報任何問題，優先處理

## 🔑 本場關鍵檔案索引
- `event-signup/schema.sql`：新增`wheel_winners`/`wheel_prizes`兩張表
- `event-signup/db.py`：新增`get_wheel_roster`/`add_wheel_winner`/`get_wheel_prizes`/
  `set_wheel_prizes`/`decrement_wheel_prize`/`clear_wheel_winners`(含復原庫存)
- `event-signup/app.py`：新增`/wheel`、`/wheel/data`、`/wheel/winner`、`/wheel/reset`、
  `/wheel/prizes/set`
- `event-signup/templates/wheel.html`：轉盤主頁面，獎品下拉選單+設定小工具+中獎動畫+
  15句趣味台詞
- `github_repos/ai-talk/index.html`：贊助人清單12/13編號
- `state/netlify_deploy_quota.json`：本場5次部署紀錄
- commit序列：`f03d356cf`(PayUNi連結) → `7f7225a5d`(贊助人清單) → `aae07796f`(轉盤獎品庫存) →
  `543ca4ec3`(趣味台詞)

