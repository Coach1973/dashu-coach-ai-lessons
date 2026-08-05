# 軍師接力棒 · 2026-08-03 v92（Mac終端機 Sonnet 5，龍蝦小助教LINE群組長期失效真根因+健檢cron權限誤傷修復+提醒功能推廣三帳號）

> 建立時間：2026-08-03 下午（台灣時間）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v91（Mac桌面版Sonnet5，CLAUDE.md規則健檢+ai-go教練專屬人設上線+新增「總結」收工暗號E17）
> 本棒主軸：**教練發現龍蝦小助教（LINE default帳號）Telegram/LINE都沒回應，且過去能用的群組互動也失效。第一輪查證方向被教練當場糾正（去查LINE官方後台是錯的），改用「合成真實簽章的LINE webhook直接測本機端點」查出真根因：`@openclaw/line`外掛對accountId==="default"完全忽略`accounts.default`底下的設定，群組互動從設定被搬進這個巢狀結構那一刻起就架構性失效，跟教練猜的一樣是「我們自己設定的問題」不是LINE後台問題。修復後教練又用一句話點出另一個問題：main agent的健檢cron失去exec/read/cron工具（昨天toolsBySender權限鎖的連帶副作用），教練進一步用VPS提醒功能反向挑戰「提醒功能根本不需要exec」，逼出一個更精準的修復方向：把「系統自動化需要exec」跟「用戶要求服務不需要exec」兩件事分開處理，最終健檢cron跟三帳號提醒功能都修好，同時老實跟教練報告一個技術限制（LINE群組工具鎖只能靠提示層，非技術硬鎖）。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 龍蝦小助教LINE群組長期失效真根因：`accounts.default`設定被外掛原始碼結構性忽略
教練回報Telegram/LINE都對他沒反應，且過去能用的群組互動（如「思伽與施樂恩討論區」）現在也失效。第一輪查證方向錯誤：先去查LINE官方後台webhook設定，教練當場指正「這個方向不對，如果後台設定壞了，現在小龍蝦就不會運作」。改走基礎設施逐層排除法（cloudflared tunnel→gateway→webhook→channelAccessToken全部實測健康），確認infra沒問題後，用**合成一個帶正確HMAC簽章的假LINE webhook直接打本機`/line/webhook`端點**這招，配合短暫開啟`OPENCLAW_LOG_LEVEL=debug`，抓到鐵證：`"Blocked line group message (groupPolicy: allowlist, no groupAllowFrom)"`——查原始碼確認`resolveLineAccount()`對accountId==="default"這個特例完全不讀`accounts.default`底下任何欄位（`dmPolicy`/`groupPolicy`/`groupAllowFrom`全部被忽略，只有具名帳號如bni_tainan/jiaolian_thoughts才會讀自己accounts下的設定），內建預設值剛好是「allowlist+空白名單」，等於這個設定被搬進accounts.default巢狀結構那一刻起就架構性失效，不分寄件人。已修復：改在`channels.line`頂層設定`groupPolicy: open`+`groupAllowFrom: ["*"]`+`dmPolicy: pairing`，`accounts.default`只留`webhookPath`（真正被使用的欄位）。commit `ec48b7bd`。

教練實測「帥帥養龍蝦」群組確認有回應；「思伽與施樂恩討論區」另一次沒反應，查證後發現是MiniMax API暫時過載的一次性問題（訊息確實送達並開始處理，只是模型呼叫失敗），跟權限無關，教練重試後應已恢復。過程中也順手回答教練「提醒需要記住LINE ID」的疑問：不是LINE平台分辨不出誰是誰（每則訊息本來就帶唯一身份碼），是agent想主動把「身份碼↔真實姓名」的對應記進GROUP_IDENTITY.md避免認錯人，跟平台限制無關。

### 2. 🔴🔴 main agent健檢cron失去exec/read/cron工具，真根因是cron沒有「傳話人身分」
電報版小龍蝦回報「🦞健康檢查14:37—⚠️無法執行」，工具全部缺漏。查證發現：昨天(commit 2f498962)幫main/kong/peipei上的`tools.toolsBySender`萬用deny規則，設計上比對「傳話人身分」，但cron觸發的agent turn完全沒有傳話人身分（空senderId，實測驗證——manual cron run 5次皆重現同一筆deny記錄），永遠落到`"*"`那條deny規則，導致main agent所有需要exec/read/cron的定時任務被誤判成陌生發送者擋掉。教練追問VPS版的「提醒我禮拜三下午喝咖啡」功能，逼出更精準的思路：教練指出「提醒」功能根本不需要exec（VPS版每個用戶各自獨立、伺服器端程式直接處理），點破軍師一開始把「健檢cron需要exec」跟「用戶提醒功能」錯誤地綁在一起建議「放寬定時任務權限」的方向錯誤。

教練裁決「健檢cron是我個人的問題,跟其他用戶無關,那就去做啊」後，改用**群組層級鎖取代agent層級萬用鎖**：Telegram外掛schema支援群組層級`toolsBySender`（已在`channels.telegram.accounts.bot_main.groups["*"]`補上，技術硬鎖，只保護真人群組聊天不影響cron，因cron沒有群組context）；但查證`@openclaw/line`外掛(2026.6.33)的`LineGroupConfigSchema`不支援`tools`/`toolsBySender`欄位，LINE群組這邊技術上做不到硬鎖，改在`workspace/SOUL.md`新增鐵律五（系統提示層防護：非教練本人一律只提供對話服務，不執行系統操作）。commit `56c0efe3`。手動觸發健檢cron驗證：`lastRunStatus: ok`，連續錯誤歸零，exec/read/cron三個工具正常運作無deny記錄。**已老實告知教練這個LINE側的殘留風險**（提示層非技術硬鎖），教練知情。

### 3. 🎯🎯 主動提醒功能推廣到三個LINE帳號
延續上一項的思路，教練指示「當然現在就立刻把提醒功能推廣到三個帳號」。原本`hooks/bni-reminder-schedule/handler.js`寫死只認bni_tainan一個帳號的sessionKey格式（`agent:<accountId>:line:direct:<userId>`），推廣時發現一個新bug：default帳號綁在main agent，其session key實際是`agent:main:line:group:<groupId>`（群組）或直接共用`agent:main:main`（私訊，跟Telegram同一把key），兩種情況`parts[agentIdx+1]`抓到的都是"main"而非"default"，若不處理會讓default帳號的提醒請求被靜默略過。已修復：加上main→default正規化；`send_line_push.py`從寫死bni_tainan token改成`--account`參數化，default帳號走`channels.line`共用的channelAccessToken；順手補上`--no-deliver`旗標避免cron系統自己的announce機制誤報error（實際訊息已送達，只是完成回報機制找不到明確投遞對象而拒絕）。commit `41ffac6b`。用真實簽章的合成webhook逐一測試bni_tainan+default兩帳號，皆確認cron job正確建立、command exitCode=0、LINE Push API回應200，測試job事後清除不留殘留。

### 4. ⚠️ 教練一段修改回饋被中斷，內容未送達
教練在15:18說「好，這個需要更改的幾個點我說一下。首先，先肯定做得不錯！」後被系統標記中斷，緊接著改下達「總結」指令。**這段回饋的具體內容從未真正送達**，下一場開工不能假設已經知道要改什麼，需請教練重新講一次。

## 📋 下一場直接開工任務
- **🔴 優先：教練15:18中斷的回饋內容**，請教練重新完整講一次
- LINE群組工具鎖技術限制：待`@openclaw/line`外掛未來版本支援群組層級`toolsBySender`後，補上硬鎖取代目前的SOUL.md提示層防護
- ai-go雙入口同步、BNI真誠/真愛/真AI分會網站、Email自動發送系統、嘉義場籌備：仍卡在等教練，多場未更新

## 🔑 本場關鍵檔案索引
- `openclaw.json`（`~/.openclaw`外層master分支）：LINE default帳號群組設定搬遷、main/telegram群組層級toolsBySender
- `workspace/SOUL.md`：新增鐵律五（系統指令只認教練本人）
- `hooks/bni-reminder-schedule/handler.js`＋`agents/bni_tainan/scripts/send_line_push.py`：推廣三帳號
- `試金石/試金石_案例庫.md`：新增案例56
- commit（`~/.openclaw`外層master分支）：`ec48b7bd`（LINE default群組修復）→ `56c0efe3`（cron權限修復）→ `41ffac6b`（提醒功能推廣）

