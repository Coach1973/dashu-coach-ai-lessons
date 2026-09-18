# 軍師接力棒封存檔 v214+v215（2026-09-18，Mac桌面版 Sonnet 5）

> 封存原因：E16 接力棒瘦身鐵律（主檔超過 3 棒就把最舊的搬進 archive）
> 封存時間：2026-09-18 17:25（台灣時間）
> 主檔當前狀態：v216 / v217 / v218 共 3 棒

---

# 軍師接力棒 · 2026-09-18 v214（Mac桌面版 Sonnet 5，MiniMax額度徹夜追查：Remote Control確認為真實來源+industry-chain-sop hook「認錯人」根因修復，12%/500次新缺口未解交棒下一視窗）

> 建立時間：2026-09-17 21:34 ~ 2026-09-18 00:50（台灣時間）
> 上一棒：v213
> 本棒主軸：**教練徹夜追查MiniMax「5小時4500次」額度異常，本棒用截圖鐵證確認手機Remote Control背景session真的會打到MiniMax（教練已封存關閉3個背景session）；過程中意外發現孔大哥的industry-chain-sop hook設計錯誤（鎖senderId而非groupId，導致從未真正觸發過）並修復驗證成功；教練收工前回報額度突然飆到12%(~500次)，遠超過「兩個簡單指令」能解釋的量，缺口未查出，需下一個對話框接手查。**

## 🎯 本場戰果

### 1. MiniMax額度異常：Remote Control確認為真實貢獻源，教練已封存3個背景session
教練提出關鍵假設「手機沒下指令，會不會是Remote Control背景在燒」，本棒逐步查證：①查`~/.claude/settings.json`確認仍指向MiniMax②查`claude rc`host process(PID 97294)底下掛3個獨立spawned子session(PID 9265/52231/97302)，各自活了17~20小時③教練提供手機截圖，錯誤訊息`API Error: Request rejected (429)·Token Plan usage limit reached...(2056)`跟今晚v212已記錄的MiniMax錯誤格式一字不差，**證實手機Remote Control對話真的會打到MiniMax共用鑰匙**，不是教練自己Anthropic訂閱的額度④教練用手機App把3個連接到這台Mac的session全部「Archive」，本棒立即查證這3個背景process(9265/52231/97302)真的被砍掉了(只剩host骨架)，畫面同時跳出`[claude-code:unrecognized_model]{"model":"MiniMax-M3[1M]","query_source":"auto_mode"}`——`query_source:auto_mode`證實這些session裡真的存在非使用者觸發的自動查詢，且用的是殘留的MiniMax模型別名。**根因**：昨晚(9/17)設定Remote Control時用`env -u CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC ... claude rc`啟動，這個「關閉非必要流量」的開關對這3個process從啟動那刻起就整晚沒生效過。

**教練事後追查35分鐘窗口精確歸因**：主系統(main/kong/peipei/bni_tainan/jiaolian_thoughts)本機log顯示同窗口只有3次呼叫(2次是教練跟孔大哥的真實對話)、小二(test2)確認process已停止服務(23:38後無新log，原因未查)、Hermes(教練都在想什麼以外的另一個獨立系統，本棒才發現它也持有同一把MiniMax鑰匙)0次——本機五個可查來源加總對不上教練回報的量，佐證缺口主要在Remote Control那塊看不到的雲端session(`api.anthropic.com/v1/code/sessions/cse_*`，本機無法讀取逐次呼叫明細)。

### 2. industry-chain-sop hook「認錯人」根因修復：孔大哥從未真正收到過服務
教練糾正軍師「孔大哥做不到是邏輯錯」——佩佩老師/孔大哥用同一套機制，教練親自在群組下指令時sender是教練自己的ID不是孔大哥/佩佩老師本人的ID。查`hooks/industry-chain-sop/handler.js`證實：舊版`allowedSenderId`鎖死只認孔大哥(8689825759)/佩佩老師(8786886419)本人Telegram ID，但兩人的AI助理實際上跑在各自專屬群組(孔大哥`-5083547625`/佩佩老師`-5115910257`)，**`hook.log`檔案從2026-09-16建立以來從未存在過，證實這支hook從未真正觸發成功一次**——孔大哥的AI因此自己土法煉鋼呼叫內建`image_generate`工具，落到minimax/image-01(不支援中文)，這才是先前「生圖沒中文」的真正根因，非GPT Image 2本身5~10%出錯率問題。已改成`allowedGroupId`比對(群組本身已是受控私人群組)，kong+peipei兩邊同步修正，用合成事件直接呼叫handler()實測TRIGGER/PROMPT正確產生，並用真實lk888呼叫成功產生「企業教練」產業鏈圖+推送到孔大哥群組驗證端到端可用。

### 3. 🔴 教練收工前回報：額度突然飆到12%(~500次)，遠超「兩個簡單指令」能解釋範圍，未查出
教練在本棒即將收工時報告：僅對孔大哥/佩佩老師下達兩個簡單指令，額度卻從先前的個位數百分比跳到12%(接近500次)。**誠實揭露干擾因子**：軍師本棒為修復上述hook做了2~3次真實MiniMax/lk888呼叫驗證測試(合成事件觸發1次MiniMax prompt生成呼叫+1次lk888生圖、手動直接重跑1次lk888生圖)，這些會混進教練回報的窗口內，但2~3次不可能解釋500次量級的暴增，**真正缺口在收工前未查出**，教練指示先做總結交接、開新對話框繼續查。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_hook_sender_id_vs_group_id_gating_2026-09-18`：任何鎖定「服務特定人」的hook，動手前要先查證那個人的訊息實際上是1對1私訊還是群組訊息——群組場景下`senderId`會是任何成員，必須改用`groupId`/`chatId`比對，不能假設「本人ID」就等於「這個人在用」。
2. （沿用）`feedback_assert_before_verify_pattern_2026-09-17`：本棒教練再次糾正軍師「不對不對，你的邏輯不對」——一開始直接引用孔大哥AI助理自己的診斷報告當成結論，沒有先查證孔大哥的hook到底有沒有真的觸發過，屬於同一種「有查證管道卻先講結論」的模式，這次教練點破後才回頭查`hook.log`不存在的鐵證。

## 📋 下一場開工先做（教練已明確指示：新對話框優先查這個）
1. **🔴🔴🔴 最優先：12%/~500次額度暴增查不出來源**——已排除main/kong/peipei/bni_tainan/jiaolian_thoughts(本機log僅3次)、test2(process已停止服務)、Hermes(0次)，Remote Control 3個背景session已被教練封存關閉（理論上不該再燒）。建議下一場：①先問教練現在額度百分比是否還在漲，若漲代表還有活躍來源沒找到②檢查test2的gateway process為何在23:38後停止服務，是否又是NO_REPLY迴圈或其他crash③考慮教練是否要重置`sk-cp-`共用金鑰以徹底排除疑慮(不可逆，需教練親口此刻授權)。
2. **驗證孔大哥/佩佩老師端industry-chain-sop hook修復是否真的解決問題**：本棒僅用合成事件+手動腳本驗證，尚未讓孔大哥本人在真實對話中重新測試一次「XX的產業鍊SOP」；佩佩老師端理論上同步修好但完全未實測。
3. **workspace git status發現115行未commit異常**（含`D TOOLS.md`+多個`workspace-state.json.migrated.*`孤兒檔案），本棒未深查，疑似延續案例73 `doctor --fix`遷移的殘留，需要下一場評估是否要清理或救回。
4. 沿用既有待辦：大樹小講「歷史講座紀錄」補EDM連結、等教練喊「推」跑bigtree靜態版一鍵發佈、「幕僚長晨報」cron消失原因、FB App Review、OpenClaw 2.0後續評估、`stop_rules_master.py`規則#07誤判regex、峰哥的產業服務鏈SOP待教練提供Telegram ID/群組資訊後建置。

## 🔑 本場commit
外層`.openclaw`repo：`hooks/industry-chain-sop/handler.js`(senderId→groupId修復，本次commit)。`workspace`repo：`claude-brain/feedback_hook_sender_id_vs_group_id_gating_2026-09-18.md`(新記憶檔)+`JUNSHI_HANDOFF_LATEST.md`(本次接力棒)+MEMORY.md索引，本次commit。Remote Control 3個背景session的封存關閉是教練手機端操作，非git版控範圍，已用process清單(PID 9265/52231/97302消失)驗證取代commit hash為證。

---

# 軍師接力棒 · 2026-09-18 v215（Mac桌面版 Sonnet 5，MiniMax額度懸案結案：小二第二種無限重試bug活逮+官方issue #122261佐證+2.0評估暫停）

> 建立時間：2026-09-18 00:44 ~ 02:09（台灣時間）
> 上一棒：v214
> 本棒主軸：**承接v214交棒的「12%/~500次額度暴增查不出來源」懸案，本棒活逮小二第二種無限重試bug(寫記憶檔oldText不符觸發)並止血，用「教練洗澡20分鐘完全靜默、額度穩住不跳」的乾淨實驗證實稍早的攀升只是顯示器延遲追上舊帳；查官方GitHub確認這正是尚未關閉的issue #122261「工具重試斷路器」已知洞；教練最終裁示test2/OpenClaw 2.0評估正式暫停，等官方修復或有測差異化功能的需求再重啟。**

## 🎯 本場戰果

### 1. 額度懸案破案：小二兩種無限重試bug + 官方issue佐證
承接v214交棒的死結，本棒精算出小二(test2)9/17全天**488次「Telegram sendMessage was suppressed before delivery」**失敗——這正是v213已修復的NO_REPLY迴圈同一款bug，但發作範圍比原記錄的18:00~19:25(229次)廣得多，從16:21第一次生圖指令就開始斷續發作，488次幾乎完全對上教練回報的~500次跳動。接著01:06:14教練一句測試訊息又活逮**第二種變體**：小二嘗試寫`memory/2026-09-17.md`+`USER.md`時「oldText跟檔案實際內容對不上」導致無限重試(邊生成邊寫入失敗)，48秒內連打7次同一traceId，已用正確指令(`node ... openclaw --profile test2 gateway --port 53141`，非`cd`進目錄，這是先前踩過的坑)kill+重啟test2止血。查官方GitHub(`github.com/openclaw/openclaw`，39萬星82萬fork的正規大型專案)確認：**issue #122261「Tool retry loops can saturate gateway event loop — propose per-tool circuit breaker」**正是這整類問題的官方未關閉bug單，2週前回報至今未修。

### 2. 關鍵驗證實驗：教練洗澡20分鐘完全靜默，額度穩住證實非新漏洞
test2重啟後確認安靜11分鐘(01:12:54起)，但額度仍14%→17%→18%持續攀升(速度遞減：17%→18%花6分鐘)，一度懷疑Remote Control或其他隱藏來源。教練親自執行決定性測試：洗澡20分鐘完全不跟任何機器人互動(含確認手機已完全退出App、無背景任務)，回來回報**額度穩定停在18%沒有再跳**——證實稍早的攀升是顯示器延遲追上稍早已發生的舊帳(呼應案例74記錄過的顯示不穩定)，不是新的活躍漏洞，懸案正式結案。

### 3. OpenClaw 2.0評估教練裁示：暫停，非沙盒限制純粹任務類型沒對到
教練追問「2.0到底比1.0好在哪，測不出來是不是沙盒限制」，本棒誠實分析：查官方版本紀錄(2026.9.4所在版本線12天內連發6版：8.2/9.1/9.2/9.3/6.35/9.4，294貢獻者/1558PR規模)，2.0真正差異化功能(Mermaid圖表、Skill Workshop、會議紀錄搜尋庫、多裝置session接續、GPT-6 Astra模型)本場測試的任務(生圖/改行事曆/聊SOP/寫記憶檔)完全沒觸及，並非沙盒閹割功能，是任務類型剛好落在1.0/2.0表現一致的交集。教練裁示：既然近期不會主動使用，比起維護一支自製斷路器補丁(還得跟著test2版本升級持續驗證)，更划算的做法是**直接停用test2 gateway**，等官方issue #122261真正上線或未來想測差異化功能時再重啟評估。已執行：kill test2 gateway(PID 38338/port 53141確認不再監聽)，寫到一半的`~/.openclaw-test2/hooks/edit-retry-loop-guard/watcher.js`半成品已刪除(經delete_guard五道閘門正常流程，非教練資料，已示範`DELETE_APPROVED`需與`rm -rf`分開兩個獨立指令執行，同一指令字串內連寫會被guard整串擋下)，`no-reply-loop-guard`保留原位不動(下次重啟test2仍生效)。

## ⚠️ 本場教訓（已寫入記憶）
1. **診斷速度教訓（教練親自提出的覆盤）**：額度異常查證不該先套理論(累加桶/背景漏洞)，第一步該問「教練最近跟哪個機器人講過話」，直接拉該機器人最近5~10分鐘原始log找同一traceId密集重複的爆發訊號——這是機械、廉價的檢查，比繞去算歷史累加/猜測手機背景快得多，本棒繞了一大圈才回到這條路上。
2. **`delete_guard.sh`的攔截是對整個指令字串做前置掃描**：`touch DELETE_APPROVED && rm -rf ...`寫在同一個bash指令裡，即使touch排在rm前面，guard依然整串擋下(不會先執行touch再擋rm)，必須拆成兩個完全獨立的工具呼叫。
3. **WebFetch在這台Mac的小模型摘要步驟目前會失敗**(`MiniMax-M3`模型無法辨識的錯誤)，改用`curl`直接抓原始HTML/呼叫GitHub API取代，本場靠這招查到官方release notes+issue搜尋結果，之後遇到WebFetch失敗可直接繞道curl不用重試。

## 📋 下一場開工先做
1. **沿用v214既有待辦**：workspace git status的115行未commit異常(疑似案例73 `doctor --fix`遷移殘留)、確認孔大哥/佩佩老師端industry-chain-sop hook真人實測、峰哥的產業服務鏈SOP待Telegram ID、大樹小講EDM連結、bigtree靜態版一鍵發佈、幕僚長晨報cron消失原因、FB App Review、`stop_rules_master.py`規則#07誤判regex。
2. **test2/2.0評估已暫停**，非待辦，除非教練主動提起或官方issue #122261狀態更新，不用主動追蹤。
3. **E16接力棒瘦身**：主檔已累積v207~v215共9棒，下次開工優先把v207~v210搬進`handoff_archive/`。

## 🔑 本場commit
`workspace`：本次commit含`JUNSHI_HANDOFF_LATEST.md`(本棒)+`claude-brain/MEMORY.md`索引+新記憶檔(見下)。系統層級操作(test2 gateway kill、watcher.js刪除)非git版控範圍，已用`lsof -i :53141`無輸出+`ls`目錄確認取代commit hash為證。

---
