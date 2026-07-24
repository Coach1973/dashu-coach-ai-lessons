## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立）

> 這張表**取代**逐棒散落的「vXX待辦」小表——舊表格散在v72/v73/v74/v75各自的段落裡，容易漏看、也看不出哪項是「卡住等教練」還是「該我自己動手」。**以後每一棒開工先看這裡，任務完成或狀態改變就更新這張表，不要再另開一張新的待辦表。**
>
> 狀態代碼：🔒卡住-等教練　⏳待軍師/小龍蝦動手　⚠️持續追蹤(非任務)　✅已完成待確認

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🔴🔴🔴 | BNI大台南小幫手「主動提醒」功能 | ⏳待動手 | v77已設計好事件驅動流程（cron --at --delete-after-run），下一場直接照設計實測，本場只寫了計畫沒動手 |
| 🔴🔴🔴 | 真誠分會／真愛分會／真實AI分會願景+產業分佈圖說明書 | 🔒卡住-等教練 | 連續v72起多棒未開始，教練還沒給細節 |
| 🔴🔴🔴 | Netlify部署額度 | ⚠️持續追蹤 | 真相源`state/netlify_deploy_quota.json`：剩10次（2026-07-25前到期），不是任務本身，是每次碰Netlify站台前要先查的約束條件 |
| 🟡 | coach888拖拉排序功能 | ⏳待教練回饋 | v72已用真實滑鼠事件測試交付，尚無教練實際使用回饋記錄，下一場先問「好用了嗎」 |
| 🟡 | 「全世界最優秀的團隊計畫」報名連結 | 🔒卡住-等教練 | 兩顆按鈕還沒掛真實報名連結，等教練給LINE或表單網址 |
| 🟡 | 企業健身房正式建站（coach1973.github.io/Business.gym） | 🔒卡住-等教練 | 網址教練已親貼確認，但尚未正式交辦開工 |
| 🟡 | 企業健身房4項文案修改 | 🔒卡住-等教練 | 已記錄commit 10c7b11cf，等教練繼續交辦下一步 |
| 🟡 | 兩個小工程教訓寫入試金石 | ⏳待軍師動手 | ①`.env`含`$`字元值要單引號包住 ②Jinja模板要guard None值（mentor100已修好，其他Flask小專案值得抽空檢查） |
| 🟡 | BNI小幫手教練親測多種問法 | ⏳待教練體驗 | 確認BNI小幫手實戰體驗OK |
| 🟡 | Coze舊機器人何時停用 | 🔒卡住-等教練 | 先保留當備援，等教練確認新系統穩定一陣子後裁示 |
| 🟡 | ACER/聯想備份刪除（ACER備份+聯想C槽94GB+ACER 36.3GB，觀察期皆已過） | 🔒卡住-需教練在ACER/聯想機器親自開對話執行 | 這台Mac無法代為執行，是本機執行限制不是任務被遺忘 |
| 🟡 | 光線尺顧問ATM NT$10,000入金(07-13)對帳 | 🔒卡住-等教練 | 待教練對帳 |
| 🟢 | 「連接」按鈕自動化點擊無反應（真人操作無此問題） | ✅已排除疑慮 | 教練親自兩台電腦實測「連接」按鈕正常，先前疑慮的bug只影響自動化工具合成點擊事件，教練不會遇到，暫不需修 |
| 🟡 | plugins.allow白名單未設定 | ⏳待軍師動手 | 07-24更新後新增警告：「plugins.allow is empty」，非阻斷性，建議之後找空檔補上明確允許清單（minimax/active-memory/memory-core/google/safety-locks/line/llama-cpp），非緊急 |

---

# 軍師接力棒 · 2026-07-23 v77（Mac終端機 Sonnet5，v76設計經教練挑戰後修正：提醒功能改事件驅動一次性排程/監看網址改bni.bymyway.com）

> 教練原話（v75尾聲，2026-07-23上午）：「這部分你可以先寫在交接簿裡面，等都寫完之後，我會開新的對話框並打完開工指令，到時候直接在下一個新的對話框去執行我現在說的這幾件事情。」——因為當時context已到73%，教練刻意要求「本場只寫計畫、下一場才動手」。

> **v76→v77修正記錄**：v76寫好的設計，教練開工後當場提兩點挑戰：①「每1分鐘掃一次」又是輪詢，這是同一個坑第5次犯（[[feedback_event_driven_not_polling_pattern.md]]）；②`coach.bymyway.com`教練貼出實際在用的VPS版連結，證明這個網址已經綁給VPS的Telegram版小龍蝦，Mac的LINE版不能再用同一個名字。以下是修正後的設計，**下一場直接照這個做，不要再用v76舊設計**。

## 🎯 任務一：BNI大台南小幫手「主動提醒」功能（v77修正：改事件驅動一次性排程，零輪詢）

教練原話：「例如說，使用者如果說『提醒我明天下午三點倒垃圾』...它在兩點半就會主動提示。」

**v77修正版設計（查證過`openclaw cron add --help`，`--at`本來就支援一次性未來時間點+`--delete-after-run`會在成功後自動刪除，完全不需要自己寫輪詢腳本）：**

1. `agents/bni_tainan/scripts/send_line_push.py`：單一用途腳本，用法 `send_line_push.py --to <lineUserId> --message "..."`，只做一件事——呼叫LINE push API送一則訊息，**沒有狀態檔、沒有迴圈**。LINE push API：`POST https://api.line.me/v2/bot/message/push`，headers帶 `Authorization: Bearer <token>`（token讀 `credentials/line-bni_tainan-token.txt`），body `{"to": "<lineUserId>", "messages":[{"type":"text","text":"..."}]}`
2. **不再有`add_reminder.py`/`reminders.json`/`check_reminders.py`/每1分鐘cron**，全部刪掉這個設計。改成：教練說「提醒我...」→ 小幫手用exec跑python算出絕對ISO時間（不自己心算），直接呼叫 `exec` 執行：
   ```
   openclaw cron add --at "<算出來的ISO時間>" --delete-after-run \
     --name "BNI提醒-<lineUserId末4碼>-<時間>" \
     --command-argv '["python3","/Users/bymyway/.openclaw/agents/bni_tainan/scripts/send_line_push.py","--to","<lineUserId>","--message","<提醒內容>"]'
   ```
   用`--command-argv`（JSON陣列）而非`--command`（shell字串），避免會員輸入的中文/特殊字元造成shell escaping問題。
3. 每則提醒＝一個獨立的一次性cron job，時間到自動觸發、成功後`--delete-after-run`自動清掉，**cron list裡不會累積任何常駐項目**，跟教練自己的排程完全分開（用`BNI提醒-`前綴辨識）。
4. AGENTS.md新增一節「提醒功能」，寫上面這個流程，回覆會員「好的,我會在OO時OO分提醒您」
5. **關鍵注意**：會員LINE ID從inbound訊息的`origin.from`（`line:U開頭那串`）取得，不是自己編——v75已驗證session.json的route.target.to就是這個格式

### 驗證方式（照E12格式，下一場做完要能自己勾）
- [ ] 手動跑一次 `openclaw cron add --at "<5分鐘後的時間>" --delete-after-run --name "測試提醒" --command-argv '["python3",".../send_line_push.py","--to","line:U895a0ad8e49d75f8303dc3d067282dc0","--message","測試提醒"]'`，確認`openclaw cron list`看得到這個一次性job
- [ ] 等5分鐘，確認教練的LINE真的收到這則推播（教練親自確認收到，不是只看log），且該job從`cron list`消失（`--delete-after-run`生效）
- [ ] 用全新session問小幫手「提醒我30分鐘後喝水」，確認它自己算對時間、呼叫`cron add`、回覆教練
- [ ] `openclaw cron list`確認全程沒有任何常駐/每分鐘輪詢的job出現

## 🎯 任務二：對外監看網址（v77修正：改用 `bni.bymyway.com`，不用 `coach.bymyway.com`）

教練原話：「後臺的監控介面確實需要單獨幫我做出來...」（v75原提議`coach.bymyway.com`，但教練開工後親自貼出`coach.bymyway.com/chat?session=agent%3Amain%3Adreaming...`證明這個名字**已經是VPS版Telegram小龍蝦在用**，兩者衝突，改教練親自提的`bni.bymyway.com`）

**v75已確認好消息：這台Mac本來就有跟VPS版一模一樣的後臺（OpenClaw內建的Dashboard），本機已實測能完整看到bni_tainan每一段真實對話（問題+回答都在），不用重新開發，只差「對外開一個網址」這一步。**

**v77已查證**：`dig bni.bymyway.com`查無任何DNS紀錄，確認這個名字目前完全沒被佔用，可以安全使用。

### 現況（v75已驗證，下一場直接沿用不用重查）
- 本機網址：`http://127.0.0.1:18789/#token=fd9928d58f419937cf56ea1ab10c0830fbded6e64714a047`（gateway token，來自openclaw.json的`gateway.auth.token`）
- Session瀏覽路徑：`/sessions` 列出所有agent的對話（含bni_tainan），點進去`/chat?session=agent%3Abni_tainan%3A...`看完整逐字稿
- Gateway目前綁定：`bind=loopback (127.0.0.1)`，只有這台Mac本機能連，還沒對外

### ✅ 已完成子步驟（本場10:59，教練親自挑戰後現場做的）：登入方式改密碼制
教練問「聯想/宏碁能不能打這個網址進去看」「要不要帳號密碼」，查證`127.0.0.1`只有本機能連（這正是還沒做Cloudflare公開的直接後果）後，同時解決登入方式：查`openclaw gateway --help`確認系統原生支援`auth.mode=password`（不用自己造登入系統），教練選定密碼登入、密碼指定為`Bymyway7`。已執行：
- `openclaw config set gateway.auth.mode password`
- `openclaw config set gateway.auth.password "Bymyway7"`
- `openclaw gateway restart`
驗證：`gateway status`顯示`Runtime: running`、`Connectivity probe: ok`；`curl http://127.0.0.1:18789/`回200；LINE default/bni_tainan兩通道`channels status`皆`running`；Telegram三隻bot雖然`channels status`顯示`disconnected`，但用`scripts/telegram_channel_probe.sh`真相源探針測試回`OK:通道健康`（案例53教訓：不信衍生欄位，信真探針）。

**🔴 追加發現＋已知未修bug（教練實測「沒看到登入畫面」抓到，本場用Claude in Chrome深挖到底）**：
1. 第一次`open -a Chrome`後教練回報「沒有看到它顯示登入或連結」——查證是瀏覽器殘留舊token模式的裝置身分快取(`localStorage.openclaw-device-identity-v1`)，跟新密碼模式衝突，導致連登入表單都顯示不出乾淨畫面。清掉localStorage後恢復乾淨的登入表單。
2. **真UI bug（未修，教練口頭同意先擱置）**：登入表單上的「連接」按鈕，不論用滑鼠座標點擊、accessibility ref點擊都完全沒反應（伺服器log證實：`reason=password_missing`，代表按下去根本沒把密碼欄位的值送出）。查到`openclaw-app`元件本身有`password`屬性和`connect()`方法，直接用JS呼叫`app.connect()`繞過按鈕、成功登入，登入後重整頁面會維持登入狀態（不用每次重打密碼）。懷疑根因：畫面上同時疊著一個「Control UI did not start」的過期錯誤提示框，可能蓋住了按鈕的可點擊區域（但`customElements.get('openclaw-app')`實測是true，元件其實有正常啟動，這個提示框本身可能才是過期/誤報）。
3. 系統右上角顯示有新版可更新（v2026.7.1-2，目前跑v2026.6.11），這個按鈕bug有機會已經在新版修掉。
4. **教練決定（本場已問過）**：先不處理，等他自己真的在別的瀏覽器/別台電腦第一次登入卡到這個bug再說——**下一場如果做Task 2（Cloudflare對外開通）之後教練第一次從聯想/宏碁登入卡住，這就是原因，直接用`app.connect()`這招或考慮版本更新，不用重新從頭查。**

**目前狀態**：這台Mac本機Chrome（Claude in Chrome操作的那個分頁）已經登入成功並保持登入，教練這台機器不會再卡到。密碼已改好，登入機制本身（伺服器端）驗證過是正常運作的，只是那顆按鈕本身有bug。

### ✅ Task 2 本場（07-24凌晨）已全部完成，用Claude in Chrome操作教練真實登入的Cloudflare帳號
1. 進Cloudflare Zero Trust後台，找到現有tunnel `openclaw-macmini`（ID `e35d30ec-45cf-4854-8afc-1bf92b163231`），Routes分頁點「Add route」→「Published application」→ subdomain `bni`、domain `bymyway.com`、service `http://localhost:18789`，成功新增`bni.bymyway.com`路由（跟`openclaw.bymyway.com`/`media.bymyway.com`同一顆tunnel，dashboard上三條route都看得到）
2. `dig bni.bymyway.com`回Cloudflare edge IP、`curl https://bni.bymyway.com/`回200 ✅
3. **🔴 過程中揪出並修好一個真的會擋登入的bug**：第一次訪問`bni.bymyway.com`顯示「瀏覽器來源不允許／Gateway在接受Control UI連線前拒絕了此頁面來源」——查schema發現`gateway.controlUi.allowedOrigins`是非loopback部署的必填白名單（教練之前只在`127.0.0.1`本機測過，從沒真正拿新網址連過，所以這個問題v75/本場之前完全沒被踩到）。已執行`openclaw config set gateway.controlUi.allowedOrigins '["https://bni.bymyway.com"]' --strict-json` + `openclaw gateway restart`，修好後這條錯誤訊息消失。
4. **🔴 又發現一層設計：裝置配對（device pairing）**——就算密碼對、來源也允許了，全新瀏覽器第一次連線還會卡在「需要裝置配對」，畫面上會顯示一組device ID，要在這台Mac執行`openclaw devices approve <該ID>`才能放行。這**不是bug，是刻意的安全機制**（`gateway.controlUi.dangerouslyDisableDeviceAuth`這個關掉它的選項本身就寫「dangerously」「只能短期debug用」，不建議關）。用全新分頁完整測過一輪：密碼登入→裝置配對卡住→`openclaw devices approve`→重新連線成功，看到跟本機一樣的完整session列表和對話記錄。
5. **「連接」按鈕點擊沒反應——教練實測結果：真人點擊沒有卡住**。教練在兩台電腦（其中一台Win32裝置確認、一台裝置標記MacIntel，可能是教練當下用RustDesk連的這台Mac、也可能是我先前測試分頁的殘留，未完全查清楚但不影響結果）都各自送出裝置配對請求（requestId `c54cfbf3-3373-4e54-bc01-a81b094d20fb`、`15655958-2d04-46aa-bd7b-bfeebc741a91`，皆已`openclaw devices approve`核准），代表**密碼+連接按鈕這一關教練真人操作完全正常**，我先前擔心的按鈕bug只是自動化工具合成點擊事件的問題，不是真的產品bug，教練這邊不會遇到。教練原話「總之，我現在兩台電腦都進去了」——**Task 2完全收尾，教練親口驗收通過。**

### 給教練的最終資訊（下一場開工先確認教練有沒有試過）
- **網址**：`https://bni.bymyway.com/`
- **密碼**：`Bymyway7`（不用帳號名稱）
- **在聯想/宏碁第一次連線流程**：打開網址 → 打密碼按連接 → 如果卡在「需要裝置配對」，把畫面上顯示的device ID回報給軍師/小龍蝦 → 軍師在這台Mac跑`openclaw devices approve <ID>` → 教練那邊重新整理/再按一次連接 → 應該就能看到完整監控畫面。**這個裝置核准只需要對每一台新電腦/新瀏覽器做一次，之後同一台機器同一個瀏覽器不用再重複。**

### 驗證方式
- [x] `curl -I https://bni.bymyway.com/` 回200，確認tunnel路由生效
- [x] 登入方式改密碼制
- [x] 用全新瀏覽器分頁完整測過密碼+裝置配對整套流程成功，看到完整session列表和對話記錄
- [x] 教練親自在兩台電腦實測——教練原話「總之，我現在兩台電腦都進去了」，Task 2驗收通過

---



> 建立時間：2026-07-23 凌晨（台灣時間）
> 本棒執行者：Mac 終端機 Sonnet 5（軍師）
> 上一棒：v74（聯想桌面版 Fable5，完整內容見下方）
> 本棒主軸：**教練原本用Coze串接LINE做「BNI大台南小幫手」機器人，要求評估並直接搬到小龍蝦本機、換用MiniMax-M3。過程中發現並修好一個真bug——LINE通道plugin從未在plugins.entries宣告啟用，導致webhook路徑404，教練個人LINE小龍蝦可能已silent斷線一段時間，此次順手修復。**

## 🎯 v75 本場戰果

### 1. 🎯🎯🎯 BNI大台南小幫手完整搬遷：Coze → 小龍蝦本機agent + MiniMax-M3
用教練授權的Chrome權限進Coze後台，完整擷取人設prompt（大台南小幫手總指令.txt，39.8KB）+3份知識庫文件（Podcast菁華錄/經典PODCAST/產業專業表，共約123KB），未動Coze任何現有設定（沒按Publish、沒Disconnect LINE）。

發現OpenClaw原生支援多LINE官方帳號（跟kong/peipei用同一套`channels.line.accounts`+`bindings`機制），於是：
- 新增agent `bni_tainan`（workspace `agents/bni_tainan/`，AGENTS.md放完整人設，`knowledge/`放3份補充資料）
- 用`openclaw channels add --channel line --account bni_tainan`註冊BNI官方帳號的Channel Secret/Access Token（存`credentials/line-bni_tainan-{token,secret}.txt`，未進git明文）
- 用`openclaw agents add bni_tainan --bind line:bni_tainan`建立agent綁定，教練個人LINE小龍蝦（default帳號）完全沒被動到

`openclaw agent --agent bni_tainan --message ...`本機測試3題（引薦單必填欄位/DnA防幻覺/曜董是誰），回答語氣、格式（LINE安全無**號）、案例引用（連Podcast集數都對得上）全部正確，其中DnA的「一字不改強制輸出」guardrail也正確生效。

### 2. 🔴🔴🔴 順手修好：LINE通道plugin從未宣告啟用，webhook 404（可能已影響教練個人LINE小龍蝦）
測試新帳號前先驗證現有LINE webhook端點，`curl -X POST localhost:18789/line/webhook`回404——不是我弄壞的，查`plugins.entries`發現從2026.6.1外掛啟用機制上線以來，**"line"從未被加進去**（只有minimax/active-memory/memory-core/google/safety-locks等有宣告），`channels list`/`channels status`因此完全不列LINE，教練個人LINE小龍蝦這條線实际上可能已經默默斷線一段時間（cloudflared tunnel本身活著，但gateway端根本沒mount這個路徑）。

補上`plugins.entries.line = {enabled:true}`，重啟gateway後webhook變成正常的400（非404），`channels status`正確顯示`LINE default: running, mode:webhook`，3個Telegram bot也順利重連無影響。

commit `bf560a96`（外層repo，已push）。

### 3. 🎯 webhook已切換上線（教練當場實測）
教練說「現在就切換」，登入LINE Developers Console把「大台南南區AI小幫手」(Channel 2008741664)的Webhook URL從Coze換成`https://openclaw.bymyway.com/line/webhook`（跟教練個人LINE小龍蝦共用同一條cloudflared tunnel，LINE官方Verify測試回應Success）。教練實測第一句話卡在OpenClaw的陌生人配對關卡(dmPolicy=pairing)——這是設計給個人助理用的機制，BNI要服務全體會員不該有這關。教練原話：「肯定是要開放，不然要累死我嗎？」，已改`channels.line.accounts.bni_tainan.dmPolicy=open`+`allowFrom=["*"]`，跟教練個人LINE(default帳號)的pairing設定分開處理。commit `07ee6418`。

### 4. 🎯🎯 追加三項強化：誠實鐵律、搜尋/製圖能力、行事曆真實資料
教練評估了coach1973.github.io/ai-go(教練自己的特助心法跨AI注入系統)能不能整份加進BNI小幫手——判斷後**沒有照抄**，因為ai-go是設計給「服務教練本人」的AI用的身份框架，直接塞會跟BNI小幫手「服務全體會員」的身份打架，且格式(**號)會炸掉LINE輸出规则。改成用BNI小幫手自己的語氣，把精神抽出來寫成AGENTS.md新增1.5節「誠實鐵律與三大信念」：不知道就說不知道、絕不編造，三大信念（真誠善良忍讓/時間就是生命善用OPE/對的事是長期有好處的事）。

同時實測確認agent本來就有網路搜尋(web_fetch，走DuckDuckGo)、圖片生成(image_generate，走MiniMax image-01)能力，不用額外申請key，AGENTS.md新增3.5節指引何時該用。

**行事曆真實bug修復**：教練發現問「7月MSP幾號、9月M1幾號」小幫手答不出來/亂碼。查出根因：`tainan-calender.netlify.app`頁面內嵌一個巨大base64字型檔案在CSS裡，AI用網頁擷取工具讀整頁時常在讀到真正活動資料前就被截斷，誤判成「JS動態載入抓不到」（其實活動資料是寫死的靜態HTML）。治本：新建`agents/bni_tainan/scripts/sync_calendar.py`，直接解析該頁面HTML的event-item區塊，輸出乾淨的`knowledge/tainan_calendar.md`（按月份列日期/課程/時間/地點），openclaw cron每4小時自動重跑一次（job `99bdac4a`，已用「先刪檔案→手動觸發cron→確認重新產生」驗證過真的會跑，不是假成功）。重測「7月MSP哪天」「9月M1幾號」用全新session都答對(07/20初階MSP；09/14-15+09/19-20兩場M1)。

過程中也把AGENTS.md的`bootstrapMaxChars`從預設20000調高到40000（`bootstrapTotalMaxChars`100000），避免內容持續增加時被系統靜默截斷。commit `5f00f921`。

## 📋 v75 待辦
| 優先 | 項目 | 誰動手 |
|---|---|---|
| 🟡 | 教練親自在LINE多測幾種問法，確認BNI小幫手實戰體驗OK | 教練 |
| 🟡 | Coze那個舊機器人先保留不要動，當備援，等教練確認新系統穩定一陣子後再考慮停用 | 教練 |
| 🟢 | tainan_calendar.md目前是「教練改網站→最長4小時後同步」，若教練覺得太慢可以縮短cron間隔 | 教練提出需求再改 |

---


> 建立時間：2026-07-22 上午（台灣時間），與Mac v73同一天、教練同一句「Fable5最高等級全面體檢」指令的**聯想機這一側**
> 本棒執行者：聯想（Windows）桌面版 Fable 5
> 上一棒：v73（Mac桌面版 Fable5，Telegram假警報/cron去重/設定清理，完整見下方）
> 本棒主軸：**這場對話從教練Google Meet「攝影機被占用」求助開始，一路延伸到全面電腦體檢。三個實際成果：①查出並排除攝影機占用（Comet殘留Meet分頁）；②體檢揪出結構性病灶——這台機器根本沒有在運作的自動同步（舊ClaudeMemorySync/Heartbeat排程6/14起就Disabled、指向4月老腳本），治本建了新的LenovoBrainSync自動拉取排程；③Comet資源黑洞（51行程/8GB）安全釋放約4.5GB，但因偵測到教練正在用的分頁而刻意點到為止不強關**

## 🎯 v74 本場戰果（聯想機側）

### 1. 🟢 攝影機占用排除
教練用Google Meet說攝影機被占用。查Windows攝影機使用記錄（`ConsentStore\webcam`，LastStop=0=占用中），揪出是Comet殘留一個沒關的Google Meet分頁（PID標題「Meet - rgk-fjwt-nzx」）霸著鏡頭。單獨關分頁行程會被Comet復活，改整個關Comet才釋放。教練確認Meet鏡頭恢復正常。

### 2. 🔴🔴🔴 治本：這台機器根本沒有自動同步（本週17天落後的真根源）
體檢發現兩主倉庫昨晚同步後幾小時又落後遠端76 commit。查排程：本該自動同步的`ClaudeMemorySync`、`ClaudeHeartbeat`從**2026-06-14就是Disabled**（五週），且指向`E:\Claude-Data\scripts\`裡4月/6月的舊架構老腳本（現在倉庫早改用mac-openclaw-workflows）。這就是[[project_windows_workspace_git_sync_gap_2026-07-17]]落後17天/1711commit的**結構性根源，非偶發**。
**治本已完成**：新建`E:\Claude-Data\scripts\auto_git_sync.ps1`（純英文避編碼陷阱，只`pull --ff-only`、工作區髒就跳過、絕不自動push）+ schtasks排程`LenovoBrainSync`（每2小時+StartWhenAvailable開機補跑；ONLOGON觸發要管理員權限失敗，改HOURLY/MO 2免權限成功）。已實測排程器能正確呼叫→拉取→寫log。詳見記憶`project_lenovo_auto_git_sync_2026-07-22.md`。以後這台最多落後2小時。

### 3. 🟡 Comet資源黑洞安全釋放約4.5GB（點到為止，守不可逆線）
Comet爆51行程/8GB。優雅關閉主視窗（CloseMainWindow，觸發session存檔）降到33行程/4.1GB後，偵測到**視窗復活且是教練正在用的分頁**（購買Mac mini頁、0729貸款說明會簽到表Google文件）——踩到「不可逆」線（強關可能弄丟簽到表編輯），依教練「只避開不可逆」指示**主動停手**，最終28行程/3.4GB，教練分頁全保留。血淚鐵律[[feedback_force_kill_browser_data_loss.md]]這次有守住。

### 4. Zoom：教練說運作正常，不動（不冒重裝風險）。空junction是案例51刪除事故留下的殼，機械原因已對教練解釋清楚。

## 📋 v74 待辦補充（併入v73待辦，不重複）
| 優先 | 項目 | 誰動手 |
|---|---|---|
| 🟢 | 舊死排程ClaudeMemorySync/ClaudeHeartbeat可擇日刪除（已被LenovoBrainSync取代，留著無害） | 軍師 |
| 🟡 | 聯想C槽94GB待刪（觀察期滿，跟v73同項） | 教練在聯想開對話 |

---

# 軍師接力棒 · 2026-07-22 v73（Mac桌面版 Fable5，全面深度體檢+三項系統修復：Telegram假警報治本/cron去重/設定清理）

> 建立時間：2026-07-22 上午（台灣時間），教練流量到期前授權「自動自發把系統修好」
> 本棒執行者：Mac 桌面版 Fable 5（最高思考等級）
> 上一棒：v72（Mac Sonnet5，teamwork銷售頁上線+coach888拖拉排序，完整見下方）
> 本棒主軸：**教練要求用Fable5最高思考等級對整台電腦做全面深度體檢（本週工作+Mac小龍蝦+VPS小龍蝦），並授權直接動手修，不用問。全程守「不信任何中繼/系統注記、一律用真相源實測」原則。**

## 🎯 v73 本場戰果

### 1. 🔴🔴🔴 抓出並治本 Telegram「失效133h」假警報（試金石案例53）
HEARTBEAT `telegramChannelOk=false` 誤報Telegram通道死了5.5天，害系統「安靜結束、不主動打擾」把11項待辦全憋著。實測推翻：3個bot token全活、bot→教練chat getChat正常、polling沒卡。**這是本週第三次踩「盲信衍生旗標不查真相源」**（案例50 VPS polling、案例52 記憶斷層、今天Telegram）。治本：新增`scripts/telegram_channel_probe.sh`確定性探針+清旗標+SOUL#19加「通道健康鐵律」逼未來心跳先跑探針。commit `40767f727`。

### 2. 🟡 cron去重：23→16啟用（commit `9a6ab9974`）
根因查證：SQLite有26筆cron，store_key全指向已不存在的jobs.json=儲存遷移產生的假重複。用`cron disable`（可逆非刪除）停用7個雙胞胎，每組留announce+model那筆。教練不再收重複起床摘要/行事曆訊息、記憶蒸餾不再跑兩遍。全定義備份`state/cron-backups/`。`cron rm`會報id not found（走store_key），要用disable。

### 3. 🟡 設定殘留清理（外層倉庫commit `a7a7f601`）
移除openclaw.json 5個失效/未安裝外掛殘留設定（memsearch等，全enabled=false），status 5條警告全消。備份`openclaw.json.bak-before-plugin-cleanup-*`。

### 4. 🟢 VPS小龍蝦體檢：健康，7/20記憶修復已鐵證生效
9個試用帳號從chunks=0→現在每個都有內容（最多767筆）dirty=false。7/20那份5-7hr的SOP大部分已不需要（B/C系統本來就有）。VPS報告已落地`knowledges/vps-reports/`。

### 完整體檢報告：`knowledges/2026-07-22_Fable5全面深度體檢報告.md`（commit `57e2a1b7a`）

### 5. 🟢 大書小講兩場活動改名「當古典音樂遇到AI科技」（後段任務）
教練要7/22+8/1兩場統一改名，牽動兩系統：①後台event-signup `event.db` events表id=2/3改名（Flask讀DB即時生效，實測`/checkin`→`/e/bigtree-0722`吐新名，備份`event.db.bak-before-rename-*`）；②bigtree公開站`index.html`兩場topic+`qr-0722.html`大標題（原7/22寫「現代科技」、8/1寫「零基礎學AI」），GitHub commit `a622bfd`，Netlify zip+API部署`bigtree-tw`(手動上傳型,site_id 40e580f0)deploy `6a602d3b`，線上實測兩場皆新名、舊名0殘留。**Netlify額度13→12(7/25前)** commit `4c5acf667`。checkin-print.html通用頁不寫死場次名不用動。

## 📋 v73 待辦（教練回神後）
| 優先 | 項目 | 誰動手 |
|---|---|---|
| 🟢 | 「場景化升華」兩不同名排程都23:00推播(533cfe54+dc9bdf5c)，教練若嫌吵一句話停一個 | 軍師 |
| 🟡 | 聯想C槽94GB待刪(觀察期滿) | 教練在聯想開對話 |
| 🟡 | ACER 36.3GB待刪(觀察期過) | 教練在ACER開對話 |
| 🟡 | 光線尺顧問ATM NT$10,000入金(07-13)待對帳 | 教練 |
| 🟡 | 企業健身房4項文案修改(已記錄10c7b11cf) | 教練繼續交辦 |
| 🔴🔴🔴 | 真誠/真愛/真實AI分會願景說明書 | 教練給細節 |
| 🟢 | Netlify剩12次(7/25前) | 部署前查額度 |

---

<details><summary>📜 v72 完整內容（點開）</summary>

# 軍師接力棒 · 2026-07-20 v72（Mac桌面版 Sonnet 5，三機總結誤報真bug修復+「全世界最優秀的團隊計畫」黑金銷售頁從零上線+coach888拖拉排序系統）

> 建立時間：2026-07-20（台灣時間，實際對話發生於7/19深夜~7/20凌晨）
> 本棒執行者：Mac 桌面版 Sonnet 5（後段一度切到 Fable 5）
> 上一棒：v71（聯想桌面版 Sonnet 5，17天同步斷線修復+tainan-calender/bigtree兩站部署，完整內容見下方精簡回顧）
> 本棒主軸：**這場對話橫跨多個獨立任務。開場先回答mentor100後台修改權限的疑問，接著查出並修好一個真bug——三機每日總結cron連續誤報「聯想連續11天沒有對話」，根因是判斷邏輯依賴一個從未真正運作的中繼蒸餾檔案，已改用git commit真相源查證（試金石案例52）。中段裝了Claude in Chrome擴充套件，讀取教練NotebookLM裡整理的商業比喻素材，從零打造「全世界最優秀的團隊計畫」黑金銷售頁，經教練多輪實質內容修訂後正式上線於教練保留網址`coach1973.github.io/teamwork`。後段圍繞教練的「AI作品總覽」(coach888)反覆調整分類與排序，最終做成一套教練可以自己拖拉排序的介面——中途一度因為用了錯誤的測試方法（自己呼叫函式而非真正模擬滑鼠操作）誤判功能正常，被教練實測抓包「都會被打回原位」，回頭查出根因是HTML5原生拖放API跟連結元素衝突，改用滑鼠事件手刻邏輯修復，這次真正用模擬滑鼠事件測試過三種情境才回報**

---

## 🎯 本場戰果

### 1. 🎯 mentor100後台修改權限疑問——4位原始導師其實早就有編輯代碼

教練問最早4位種子導師（王彤/蘇秦/燒茶/大樹教練）沒有後台權限要怎麼改自己資料。查db.py發現schema升級時已自動幫舊資料補齊`edit_token`，這4人其實早就各自有專屬修改連結，只是沒人交給他們——直接把4條`mentor100.bymyway.com/join/edit/<token>`連結整理給教練。

### 2. 🔴🔴🔴 三機每日總結cron誤報「聯想連續11天無對話」——試金石案例52

教練當晚指出23:05自動推播的總結報告「聯想連續11天沒有對話」不合理，他明明一直在聯想用Claude助教。查證cron payload發現：判斷邏輯只憑`memory/verbatim/{acer,lenovo}/YYYY-MM-DD.md`這個中繼蒸餾檔案存不存在來下結論，但這個檔案要靠`distill_and_push_*.sh`在ACER/聯想端排程執行才會產生——查證發現ACER目錄從建立以來從未真正寫入過、聯想只成功寫過一次(7/8)之後11天沒有新檔案。同時查真實workspace git log，發現聯想軍師當天下午15:26才剛真實commit過一筆工作（`[Win]`前綴），直接推翻cron的誤判。

**修復**：`openclaw cron edit bbb7a348-...`，把判斷邏輯改成「先查git log有沒有`[ACER]`/`[Win]`前綴或機器關鍵字的commit，有=今天有對話；沒有才退回去看verbatim中繼檔案」，「連續N天」的統計也改用git log逐日反推。試金石新增案例52，workspace commit `afc09589d`，記憶檔commit `2b4843891`。

### 3. 🟢 ai-talk-tw.netlify.app：已報名人數公式重新校準

教練發現「已報名87人」跟真實20多人報名數落差太大。查證發現這個數字是一個跟真實報名資料完全脫勾的假動態公式（起始18人、每3小時+1）。照教練提供的邏輯（現在約50、9天後約90）重新校準參數：起始50人、7/19起每6小時+1人。commit `f2cf45c`（ai-talk repo），已用瀏覽器實測畫面顯示52人，並推上Netlify驗證線上生效（本場Netlify部署quota第2次，剩14）。

### 4. 🎯🎯🎯 裝Claude in Chrome擴充套件，讀取NotebookLM素材，從零打造「全世界最優秀的團隊計畫」黑金銷售頁

教練問能不能讀取他已登入的NotebookLM筆記本內容——確認一開始沒有連接，引導教練裝好「Claude in Chrome」擴充套件後成功連上，讀取「真實AI團隊計劃」筆記本裡三份AI整理的商業比喻精華素材（20個經典案例+隱藏版金句+團隊組建金句彙編）。

**首版**：融合教練口述的六大核心元素（BNI 41年76國全球系統、遊戲化組隊、體育競賽紀律、SOP執行、版權聲明），寫成`~/github_repos/true-ai-team/index.html`黑底金字銷售頁，commit `c1e7d54`。

**教練多輪實質內容修訂**（不是排版微調，是重寫比喻本身）：
1. AI比喻從「泥板與鍵盤」改成「智慧型手機浪潮」（躲不掉的現實不是選擇）；木工故事改「水電師傅修馬桶」；博士故事加「思想的轉換」；角色卡新增「補血輔助」；「頂級SEO」升級+VIP貴賓室80吋螢幕視覺化；「為夢想奮鬥」拉出來做成全站最大標題的獨立強調區塊——commit `04f56c4`
2. 主標題整個改名「全世界最優秀的團隊計畫」（原叫真實AI團隊計畫）；副標題改「一個人可以走得快，但一群人可以走得遠」；SEO文案再統一用詞——commit `92afd79`

**正式上線**：教練指示直接用之前保留給「企業健身房」的網址`coach1973.github.io/teamwork`（原本只有一份暫存報告，沒動到任何舊資料），clone該repo、複製首頁進去、commit `047e496`推上線，curl+Chrome雙重驗證。企業健身房另外要用的網址教練後來親貼確認是`coach1973.github.io/Business.gym`（尚未建站，先記錄）。

### 5. 🔴🔴🔴 coach888「AI作品總覽」多輪重整，最終做成拖拉排序系統（含一次真bug修復）

教練多輪要求調整coach888分類與排序，過程：
1. 新增「大樹常用」分類置頂（12/24/25/46等指定項目）、保留網址+工具箱併入——commit `f3ce852`、`580a6aa`
2. 「對外公開」1-5移入大樹常用，全站1~46重新連續編號——commit `d3de360`
3. 新增「後臺系統」獨立分類，大樹常用內部重排——commit `79d432c`
4. **教練提出一勞永逸方案**：做一個側欄讓他自己拖拉排序，不用每次口述。決定改成「每個大項各自獨立編號」（教練評估後拍板：這樣講「第幾大項第幾項」永遠不會因為別的分類增減而跳號）——commit `203b542`

**真bug修復（教練親自實測抓到）**：第一版拖拉功能用HTML5原生`draggable`API，教練實測「都會被打回原來的位置」。查根因：`.item`內部包了`<a href>`連結，瀏覽器對連結有自己的原生拖曳行為，跟外層draggable搶主導權，放開時被瀏覽器判定無效拖放而彈回。**我自己先前的測試方法有問題**——用`dispatchEvent(new Event(...))`直接觸發事件，繞過了瀏覽器真實拖放判定機制，導致誤判「已測試通過」。修復：整個拖拉邏輯改成手刻滑鼠事件（mousedown/mousemove/mouseup），完全不碰原生drag&drop API；並增加跨組拖拉支援（項目數與編號自動同步更新）+ 舊版localStorage排序資料相容遷移。commit `6bec1f2`（新增跨組功能）→ `a760fde`（真正修好bug）。這次用程式模擬真實的MouseEvent序列（mousedown→多段mousemove→mouseup，非直接呼叫自己的函式）測試過組內排序、跨組移動、重整後保留三種情境才回報。

**教訓寫入待辦**：驗證拖拉/互動類功能不能只呼叫自己寫的事件處理函式，要模擬「使用者真實操作路徑」（滑鼠事件序列或至少帶DataTransfer的DragEvent），否則會像這次一樣自信回報「已測試」卻在教練手上失敗。

---

## 📋 下一棒待辦（依優先度）

| 優先 | 任務 |
|------|------|
| 🔴🔴🔴 | 教練預告的真誠分會、真愛分會、真實AI分會願景+產業分佈圖說明書——連續多棒未開始，教練還沒給細節 |
| 🔴🔴🔴 | **Netlify部署額度：剩13次（7/25前）**——teamwork/coach888走GitHub Pages不消耗額度；下次碰Netlify站台先查`state/netlify_deploy_quota.json` |
| 🟡 | coach888拖拉排序功能請教練親自驗收——這次雖然用真實滑鼠事件模擬測試過，但終究不是教練本人的手感操作，開工第一件事應該先問「拖拉排序好用了嗎」 |
| 🟡 | 「全世界最優秀的團隊計畫」頁面兩顆按鈕還沒掛真實報名連結，等教練給LINE或表單網址 |
| 🟡 | 企業健身房正式建站（`coach1973.github.io/Business.gym`）教練還沒交辦，只是先記錄網址 |
| 🟡 | 兩個小工程教訓待寫進試金石：①`.env`裡含`$`字元的值要單引號包住，②Jinja模板要guard None值（mentor100已修好，其他Flask小專案若有類似寫法值得抽空檢查） |
| 🟢 | ACER備份刪除已逾期（原訂7/15），需在ACER那台開對話親自執行 |

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `~/github_repos/true-ai-team/index.html`（全新，全世界最優秀的團隊計畫黑金銷售頁）
- `~/github_repos/teamwork/index.html`（正式上線頁面，教練保留網址挪用）
- `~/github_repos/coach888/index.html`（多輪重整+拖拉排序系統，含滑鼠事件手刻邏輯）
- `~/github_repos/ai-talk/index.html`（已報名人數公式重新校準）
- `試金石/試金石_案例庫.md`（新增案例52：三機總結誤報bug）
- `~/.claude/projects/-Users-bymyway--openclaw/memory/feedback_verify_activity_via_git_log_not_relay_file.md`（新增）
- `scripts/rule_html_chrome_check.sh`（強化偵測範圍，涵蓋cp/mv/git add等Bash部署動作，不只認Edit/Write）
- openclaw cron `bbb7a348-59dc-41fd-879b-91b4d0522e18`（三機每日總結payload邏輯改用git log查證）

---

## 📜 v71 精簡回顧（聯想桌面版 Sonnet 5，完整內容見git歷史）

1. 聯想機兩份git clone同時落後遠端17天（最長1711個commit），當場修復
2. 語音糾偏再確認「真誠分會、真愛分會、真實AI分會」
3. tainan-calender.netlify.app：9/21場次改9/14
4. bigtree-tw歷史紀錄頁：圖片下載過慢診斷修復+新增4場活動+線上座談會補連結
5. HTML驗收流程一度漏做（試金石案例46再犯），教練當場糾正改用Comet

---

> Mac桌面版 Sonnet 5 親筆，2026-07-20。這場對話有個值得記住的教訓：拖拉排序功能第一次交付時，我用「自己呼叫事件處理函式」的方式測試，邏輯上看起來沒問題就回報教練驗收，結果教練一用就失敗——這不是我沒測試，是我測試的方法本身沒有真正驗證到「使用者實際操作」這件事，跟守則#03「思考就是問問題」講的自我驗證是同一個層次的問題：驗證要驗證到真正會發生的路徑，不能驗證一個自己方便呼叫、但跟真實情境不同的簡化版本。修好之後改用模擬真實滑鼠事件序列測試，這才是對的做法，以後任何涉及使用者互動（拖拉、點擊、輸入）的功能，都要用這個標準去測試，不能只驗證「程式邏輯」，要驗證「操作路徑」。下一棒開工，先問教練拖拉排序這次是不是真的好用了。

</details>
