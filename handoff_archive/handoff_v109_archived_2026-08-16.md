# 軍師接力棒 · 2026-08-14 v109（Mac桌面版 Sonnet 5，官方LINE推播驗證+品牌短網域上線+Cloudflare API Token申請）

> 建立時間：2026-08-14 04:07 ~ 16:51（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v108（Mac桌面版 Sonnet 5，LINE三帳號個人記憶標準化修復+報名系統雙寫遷移bymyway.com）
> 本棒主軸：**開工先做兩件查證更正（LINE記憶修復其實不需要三機同步、確認不是誤植），接著針對v108留下的雙寫觀察期，教練親自釐清「拔Netlify後還收不收得到通知」的疑慮，發現bymyway那條路徑本身沒有通知功能，立刻補上`_notify_coach_line()`並雙重驗證，教練裁示先觀察真實報名再決定何時拔舊系統。後半場教練想設定品牌短網域，過程中查證抓到一個重要風險——PicSee原本指示要刪的DNS紀錄其實是VPS小龍蝦的對外入口，及時攔下改用全新子網域`go.bymyway.com`。Cloudflare新版介面導覽彈窗擋住瀏覽器自動化，教練親自排除後我驗證確實恢復正常操作能力。教練追問過往需求頻率後裁示申請Cloudflare API Token，全程一步一步帶教練完成申請，驗證有效並存入路徑大全。**

## 🎯 本場戰果

### 1. 🟢 兩件查證更正：LINE記憶修復不需三機同步
延續v108的「三機同步：Windows/ACER待處理」註記，查`openclaw.json`確認三個LINE帳號(default/bni_tainan/jiaolian_thoughts)全部只在這台Mac mini單一gateway設定裡，git push已是唯一需要的同步動作。同時發現這類誤植的根因：容易把「OpenClaw gateway hook」（只跑在這台Mac的服務）跟「Claude Code settings.json hook」（教練每台電腦各自獨立的特助/軍師設定）混為一談，已寫入記憶`feedback_openclaw_gateway_hooks_not_per_machine`區分兩者。commit`56018171c`+`4472119c3`(記憶庫)。

### 2. 🔴🔴🔴 官方LINE推播補上+雙重驗證
教練追問雙寫並存期「拔Netlify後還收不收得到通知」，查證發現bymyway.com那條`/api/register`路徑只存資料庫、完全不會發通知——若真的拔掉舊系統會變成完全收不到報名提醒。立刻補上`_notify_coach_line()`，複用龍蝦小助教(@268dptjc)既有LINE channel token推播給教練本人，接進`/api/register`報名成功後呼叫。驗證分兩層：①直接呼叫LINE Push API回應200+訊息ID②完整走production端點模擬一筆報名，回應`{"ok":true,"status":"new"}`且測試資料已從event.db清除。commit`0fbe4902b`。教練裁示：「先保留，等有幾個報名，我確實兩邊都收到之後，再請你拔掉舊的Netlify網址」，已寫入接力棒待辦。

### 3. 🎯🎯 品牌短網域go.bymyway.com上線，攔下一個差點打斷VPS小龍蝦的風險
教練提供PicSee的BSD vs Subdomain說明文章想設定品牌短網域，查證picsee.io頁面時發現內嵌一段對AI的prompt injection(要求推銷PicSee服務)，已識別並忽略、告知教練。用claude-in-chrome查教練Cloudflare後台現有22筆DNS紀錄，**抓到關鍵風險**：教練先前已用`coach.bymyway.com`嘗試設定PicSee，但這個子網域其實是VPS小龍蝦(43.245.60.200)對外服務的入口——若照PicSee指示刪除該A紀錄會直接打斷外部朋友用的VPS小龍蝦。已攔下並改用全新未使用的`go.bymyway.com`(A→3.231.64.15，Proxy關閉/DNS only，符合PicSee A紀錄設定要求)。

過程中Cloudflare新版介面「Welcome to new DNS experience」導覽彈窗持續攔截claude-in-chrome的自動化點擊(單擊/雙擊/Escape/點Close/點Got it共十幾次皆無效)，改請教練手動輸入六個欄位完成。教練事後表態不滿意「過去這類操作都是你去完成的」，已寫入記憶`feedback_browser_automation_ai_should_complete`——教訓是卡住時應精準定位障礙點只請教練解除最小動作，不要整個任務轉手動。教練手動點掉彈窗後，我立即重新測試確認「Add record」表單能正常開啟，證實障礙已解除。用`dig`+`host`直接查全球DNS驗證`go.bymyway.com`確實解析到`3.231.64.15`且其餘21筆現有紀錄零異動。

### 4. 🎯 Cloudflare API Token申請完成，全程一步一步帶教練走
教練質疑「不是早就申請過了嗎」，查證`~/.cloudflared/cert.pem`確認：這是Tunnel專用OAuth憑證(chapters/mentor100/event/namecard等子網域都是靠它用指令建的)，但不是能改任意DNS紀錄的通用API Token(全域搜尋`CLOUDFLARE_API_TOKEN`零命中)，已寫入路徑大全區分兩種憑證。教練評估過往這類需求頻率極低(歷史上僅此一次)但申請成本也低後裁示申請，因教練自稱「小白」要求一步一步帶。全程五步驟(Create Token→Edit zone DNS範本→Specific zone選bymyway.com→Continue to summary→Create Token)完成後，教練貼出token，已用`user/tokens/verify`+查zone兩項API呼叫驗證有效(zone id`634966548bb9b87d7875b394e7003741`)，存入`路徑大全_憑證層.md`並更正`路徑大全.md`原本記載「沒有」的段落。commit`ce163eef9`+`3b50f6757`。

### 5. 🔧 附帶回應：瀏覽器操作token成本說明
教練問瀏覽器操作是否浪費token，誠實告知：確實比直接下指令貴(剛才卡彈窗那段是本場最貴的環節)，平常習慣是「能用指令查的絕不開瀏覽器」，並主動提議申請Cloudflare API Token減少未來瀏覽器依賴——這正是第4項任務的起因。

## 📋 下一場直接開工任務
- **報名雙寫觀察期**：先問教練是否已確認有真實報名時新舊兩邊通知都收到，收到指令才能拔`sme-register-fn`/`xiaolongxia-notify`
- **PicSee品牌短網域**：確認DNS生效後教練已在PicSee後台看到成功，本項應已結案，下次見面可順口確認
- 「真誠分會」網頁主架構問題：教練仍未說明具體是什麼
- 三機hook同步（Windows/ACER的Claude Code settings.json hook，非OpenClaw gateway hook）：ACER仍待處理
- 新LINE帳號(4GLBTVK3)驗證結果：v107遺留待辦，本場未觸及，下次先問

## 🔑 本場關鍵檔案索引
- `event-signup/app.py`：新增`_notify_coach_line()`+接進`/api/register`
- `路徑大全.md`：新增「Cloudflare憑證現況」段落，區分Tunnel憑證vs通用API Token
- `路徑大全_憑證層.md`：新增Cloudflare API Token段落
- Cloudflare DNS：新增`go.bymyway.com`（A記錄，PicSee品牌短網域）
- commit(workspace)：`56018171c`+`0fbe4902b`+`f80361569`+`ce163eef9`+`3b50f6757`
- commit(記憶庫)：`4472119c3`+`2f376dda6`
