# 軍師接力棒 · 2026-08-03 v91（Mac桌面版 Sonnet 5，CLAUDE.md規則健檢+ai-go教練專屬人設上線+新增「總結」收工暗號E17）

> 建立時間：2026-07-31～2026-08-03（台灣時間，跨多場對話）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v90（Mac桌面版Sonnet5，Mac版Web Search修復+VPS/LINE版全面盤點+bigtree高雄場部署）
> 本棒主軸：**教練看完一篇講「CLAUDE.md規則只進不出、悄悄過期」的文章，要求對照健檢——這場對話做了四件互不相同但都圍繞「讓系統指令保持可信、可執行」的事：①實測揪出`~/.claude/CLAUDE.md`兩個真過期案例並修好，進而授權對執行細則E01~E16逐條做證據型健檢，合併掉一組重複規則②幫教練寫了一份中英對照的個人溝通人設，發布成ai-go一鍵注入頁的新區塊③教練提出「以後說『總結』＝收工暗號」的新指令，比照既有「開工」機制做成真正的hook而非只靠記憶④用這次的「總結」收工暗號完成本篇接力棒撰寫，形成閉環驗證。全程貫穿同一個原則：教練不要口頭承諾或文件宣告，要看得到證據(pipe-test輸出、curl驗證、真實Chrome預覽)。**

## 🎯 本場戰果

### 1. 🎯🎯 CLAUDE.md健康檢查：揪出2個真過期案例並修復，執行細則E01~E16逐條證據型健檢
教練分享一篇文章（Anthropic自己砍掉系統提示詞80%舊規則的故事），要我對照`~/.claude/CLAUDE.md`做實測而非空談。查證發現兩個真問題：①「特助心法」段落是手動貼上去的，沒有像E01~E15那樣的自動同步機制，已跟源頭`特助心法.md`出現格式/日期標籤飄移——新增`scripts/sync_xinfa_to_claude_global.sh`（比照既有`sync_zhixingxize_to_claude_global.sh`的mtime-marker模式）根治②Netlify部署鐵律段落停留在2026-05-30版本，沒收錄2026-07-25才發生的`_headers`萬用字元蓋掉圖片Content-Type教訓（案例54），已補上三條具體規則。

教練接著把整個健檢任務正式授權給我：「你去評估哪些是必要的、有用的、可執行的，就留著；沒用的、過時的，就想辦法移到歷史備忘紀錄」。逐條查證E01~E16每一條是否有專屬skill或Stop/PreToolUse hook撐著（不是憑印象猜），發現：
- **E02跟E10幾乎逐字重複**（都在講「教練說的話自動記錄不用想」），且兩者都沒有專屬hook——判定為真過期，原文完整併入E02，E10編號保留空缺不重用，寫進執行細則.md既有的「刪除記錄」區塊
- 其餘14條（E01/03~09/11~16）逐一查證都有專屬skill或hook撐著（E11危險指令甚至有真的會攔指令的PreToolUse hook `delete_guard.sh`），判定持續有積極作用，保留不動
- 順手發現`特助心法.md`檔案內部自己也藏著一份過時的執行細則9條舊副本（引用的檔名`failure_cases_handbook.md`跟現況`試金石_案例庫.md`對不上），教練指示「留在歷史檔案，不要清掉」——完整原文搬進`_archive/xinfa_zhixingxize_9tiao_stale_duplicate_archived_2026-07-31.md`，原處留一句指向正確來源的說明
- 標題「E01~E15」也順手修正成「E01~E16」（內容其實7/26已到E16，標題沒跟上，本身就是活教材）

commit序列：`0f54af6b2`（封存9條副本）→`0d1cc9755`（E10併入E02，標題修正）。所有異動都重跑對應sync腳本驗證`~/.claude/CLAUDE.md`正確同步、二次執行冪等。

### 2. 🎯 教練個人溝通人設（中英對照）上線ai-go一鍵注入頁
教練要在新AI介面貼一份「怎麼跟我溝通」的人設，先在對話裡幫他擬好中英文兩版（涵蓋講人話/方向清楚直接做/解決問題優先/誠實說不知道/不當資訊搬運工/記住脈絡/比喻是線索/簡單優先八條原則）。教練接著提出更好的想法：既然`coach1973.github.io/ai-go/`這個一鍵注入頁本來就是公版特助心法給任何人用，應該在裡面加一個「教練專屬」的特別欄位，這樣以後不用每次重新請軍師擬一份。

新增`github_repos/ai-go/coach-persona.md`（中英對照人設全文）+ `index.html`頁尾前新增獨立區塊（綠色系跟公版橘色區隔，標示「不是公版方法論，你不是教練本人可以跳過」，獨立的一鍵複製按鈕）。過程中踩到並修好一個問題：本機Python `http.server`預設對`.md`檔案不宣告charset，教練點開連結看到亂碼——查證確認這**只是本機預覽伺服器的bug**（用README.md對照組證實正式站的`_headers`萬用規則`/*.md`早就有正確宣告`charset=utf-8`），但仍動手把本機預覽伺服器也修好讓教練能眼見為憑再放行推送。教練確認後說「推」，commit `4d38936`（獨立ai-go repo），已用curl+輪詢確認正式站`coach1973.github.io/ai-go/coach-persona.md`真的上線且Content-Type正確。**已知缺口**：這個系統其實有雙入口（見`project_ai_go_xinfa_system`記憶），另一個`www.bymyway.com/ai-go/`鏡像走獨立部署腳本，本場沒有同步，已記錄進待辦狀態表。

### 3. 🎯🎯 新增「總結」收工暗號（E17），比照「開工」做成真正的hook
教練提出新指令：以後只要說「總結」兩個字，就代表要執行「總結並上傳」全部步驟，同時代表他要開新的對話框——就像「開工」這個既有暗號一樣。沒有停在「記住這個規則」，而是查證了「開工」實際上是靠`scripts/feed_junshi_handoff.sh`（UserPromptSubmit hook）偵測關鍵字、在session開始時注入六步驟內容做到的，於是做了一支對稱設計的新hook。

用Skill(`update-config`)取得hook配置正確格式後，寫`scripts/summary_upload_trigger.sh`：偵測「總結」「總結上傳」「總結一下」等短語pattern（刻意用錨定寫法，避免「幫我寫年度總結報告」這種長句子順口提到總結被誤觸發），命中就注入收工四步驟提醒（總結本場守則#14/更新接力棒E05/判斷記憶寫入E12六條清單/commit+push E01）。用5組真實prompt做pipe-test驗證：三種應觸發的都觸發、兩種不該觸發的都沒觸發，才註冊進`~/.claude/settings.json`並用`jq -e`驗證schema正確。寫進`執行細則.md`正式列為**E17**，標題同步更新，重跑同步腳本確認`~/.claude/CLAUDE.md`正確反映。commit `c0a9f30ac`。

**本篇接力棒本身就是這個新機制的第一次真實驗證**——教練說「總結」後，hook確實注入了提醒，我依提醒的四步驟寫這篇總結+更新接力棒，形成完整閉環。

## 📋 下一場直接開工任務
- **ai-go雙入口同步**：`www.bymyway.com/ai-go/`鏡像尚未同步新增的教練人設區塊，若教練需要對外分享這個版本，執行`projects/bymyway-bridge/examples/deploy_ai_go_to_bymyway.py`
- BNI真誠/真愛/真AI分會＋大台南南區網站、Email自動發送系統、嘉義場籌備：仍卡在等教練給細節，多場未更新
- 小龍蝦紀律移植計劃階段二/三：仍待排時機（v83已完成階段一）

## 🔑 本場關鍵檔案索引
- `scripts/sync_xinfa_to_claude_global.sh`：新增，特助心法.md核心內容自動同步
- `執行細則.md`：E02合併E10、標題E01~E16→E01~E17、新增E17
- `_archive/xinfa_zhixingxize_9tiao_stale_duplicate_archived_2026-07-31.md`：封存的過時9條副本
- `github_repos/ai-go/coach-persona.md`＋`index.html`：教練專屬人設區塊（獨立repo）
- `scripts/summary_upload_trigger.sh`：新增，「總結」收工暗號hook
- `~/.claude/settings.json`：新增summary_upload_trigger.sh進UserPromptSubmit陣列（該檔含密鑰不進git）
- commit序列（workspace main分支）：`0f54af6b2`→`0d1cc9755`（CLAUDE.md健檢）→`c0a9f30ac`（E17）
- commit（ai-go獨立repo）：`4d38936`（教練人設區塊）

