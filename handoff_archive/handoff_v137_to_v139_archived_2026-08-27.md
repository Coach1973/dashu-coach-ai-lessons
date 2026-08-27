# 軍師接力棒 · 2026-08-26 v137（Mac桌面版 Sonnet 5，媒合改手動觸發設計定案+來賓職業資料補正+/find搜尋頁上線+4人分類遺漏修復）

> 建立時間：2026-08-26 13:45 ~ 2026-08-27 00:28（台灣時間，長場）
> 上一棒：v136（Mac桌面版，同日上午）
> 本棒主軸：**教練針對案例65額度事故拍板永久解法——媒合全面改成人點按鈕才觸發，AI不再自動批次跑；過程中發現並修正兩個資料品質問題：來賓漏抓職業欄位、4位會員BNI分類被靜默漏寫。**

## 🎯 本場戰果

### 1. MiniMax媒合設計定案：只留現任會員預先媒合，其餘一律手動觸發（commit`f7b4c1b52`）
教練裁示「不要再把我的額度占完...重新製作一個按鈕，叫媒合，改成手動觸發，誰需要時再媒合。需要預先媒合的就是現有的92個會員」。查證發現`/card/<id>/match`手動按鈕其實早就存在(index.html已有連結)，真正的問題是`run_chain_match.py`被拿去對全部428人批次硬跑。已把該腳本改成只鎖定現任會員(SQL加`bni_note LIKE '%現任%'`)，補跑剩餘23人後**92位現任會員100%媒合完成、0失敗**；前會員336人從此不會再被批次腳本掃到，只能靠網頁手動點擊觸發。

### 2. 來賓資料重大補正：職業/公司/分會欄位補齊（commit`a16323030`）
教練糾正「connect的來賓是有專業別的，所以請您重新查詢，不可能沒有專業別」——查證屬實，v136只抓了姓名/電話/email三欄，漏了「地區-查看來賓」報告本來就有的公司/職業/分會欄位。花了不少時間才在BNI Connect介面裡重新定位到正確報表(`reportsHome`→地區結構→`ui-tabs-5`查看來賓，含Profession篩選欄位)，最後教練直接匯出完整報表(.xls，實為SpreadsheetML格式)給我解析，3216人全數比對回填、3210人(99.8%)已有職業資料。同時擴充`query.py`搜尋範圍涵蓋`guests`表（commit`f2b0cb778`），教練點明任務本質：「方便我隨時可以找到人，來組成產業服務鍊或是連絡一起來組團隊」。

### 3. 新增/find簡約搜尋頁+來賓版媒合入口（commit`8fb15419d`）
教練要求「簡約大方好看的搜尋界面...我按媒合時，就可以去使用AI，這才不會爆掉」。新增：
- `/find`：統一搜尋cards+guests，結果卡片含身分標籤(🟢現任/🔵前會員/🧑‍🤝‍🧑來賓/📇名片)+聯絡方式+媒合按鈕，純瀏覽零AI呼叫
- `/guest/<id>/match`：來賓版媒合，首次點擊才把該來賓轉一筆card(`cards.source_guest_id`+partial unique index防重複轉入)，接著沿用既有card媒合邏輯不重造一套
- 已用真實guest(id=1)端到端測試：首次點擊建立媒合結果，重複點擊確認302導回同筆card不重複扣token

### 4. 🔴資料品質bug：4位會員BNI分類被靜默漏寫，已修復+硬化腳本（commit`36648c277`）
教練從`/find`頁面親自發現田伸強(前會員/真富)、林尹渰(現任/真鑫)完全沒標示BNI身分，查證後在430人名單裡揪出4筆(另含王聖凱/朱正文)`bni_status='unknown'`且`bni_note`空白。**根因**：`parse_and_import.py`用`INSERT OR IGNORE`寫入，遇到`image_filename`(分會+姓名組成)撞到既有列時被靜默跳過，且完全沒有UPDATE補救路徑——無法百分之百確認歷史上是哪個環節造成撞名(git只有一次提交紀錄，不像是重跑造成)，但用`raw_*.txt`重新跑`consolidate()`驗證出正確標籤後直接UPDATE修正4筆，並對全部428人重新稽核(0筆遺漏、0筆重複)。已修復腳本邏輯：`INSERT OR IGNORE`後檢查`cursor.rowcount==0`，是的話改用同一把filename做UPDATE，確保以後同款撞名不會再靜默漏寫。

## ⚠️ 本場最重要教訓

1. **教練糾正「查不到不代表不存在」時，先假設自己漏抓欄位，而非急著查證失敗**——來賓職業欄位一開始就在報表裡，是我抓取範圍不夠廣，不是資料源頭真的沒有。
2. **手動觸發媒合的設計，優先重用既有基礎設施**——`/card/<id>/match`早就是手動按鈕，不需要重新發明；guest的媒合改成「首次點擊時轉一筆card」而非另建一套平行邏輯，複用了chain_matcher/card_match.html全部既有程式碼。
3. **`INSERT OR IGNORE`沒有搭配rowcount檢查等於埋了一顆不會報錯的地雷**——這次4人分類遺漏完全零錯誤訊息，是教練自己肉眼比對搜尋結果才發現的，任何用`OR IGNORE`類SQL語法的批次寫入都該養成檢查受影響筆數的習慣。
4. **教練在瀏覽器裡帶著我一起找到正確報表入口(`reportsHome`的地區結構`ui-tabs-5`)**——BNI Connect介面極深，光靠自己盲點很花時間，教練最終直接給URL片段+匯出檔案，比我自己摸索更有效率。

## 📋 下一場開工先做

1. 產業鏈媒合剩127人(前會員，428人中現任92人已100%完成)，維持**只能靠`/find`頁面手動點擊觸發**，不再批次跑
2. 3216位來賓現在都有職業資料，理論上都能透過`/guest/<id>/match`按需媒合，但尚未大量測試——教練或使用者實際用起來若有問題再回報
3. 承接v135/v136舊待辦：3支孤兒hook要不要啟用、bni-chapters「真誠分會」架構問題、OpenClaw 6.34升級教練決定、孔大哥/佩佩老師備份repo衝突、VPS缺.gitignore、event-signup後台8/26早半場event.db同步

## 🔑 本場commit
`f7b4c1b52`(run_chain_match.py只鎖現任會員)／`a16323030`(guests表補職業/公司/分會)／`f2b0cb778`(query.py搜尋擴及guests)／`8fb15419d`(/find搜尋頁+guest媒合路由)／`36648c277`(4人分類遺漏修復+腳本硬化)

---

# 軍師接力棒 · 2026-08-26 v138（聯想Windows Sonnet 5，跨機同步四層根因全修+ai-talk嘉義場攤商05~10上線+Netlify額度校正）

> 建立時間：2026-08-26 09:20 ~ 10:29（台灣時間）
> 上一棒：v134（聯想Windows，同日凌晨）— 中間v135~v137是Mac桌面版並行工作，聯想這台從10:29後閒置至今（33小時視窗開著但無新動作，git log已查證確認）
> 本棒主軸：**教練凌晨質問「三台又各自為政」，查出聯想這端有四層獨立根因疊在一起，全修並驗證；接著處理教練臨時交辦的ai-talk嘉義場設攤廠商新增，過程中教練糾正額度同步設計過度工程化。**

## 🎯 本場戰果

### 1. 「三台各自為政」四層根因全修（詳見`claude-brain/project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26.md`）
①聯想從沒裝過標準七支對齊hook（含收工自動push）②所有hook讀的`workspace`是7/23的死clone，已確認零未推送內容後改名封存、原路徑改建junction指向活的`mac-openclaw-workflows` ③PS5.1在`-File`模式讀stdin中文被Big5讀壞（「開工」變亂碼），`feed_junshi_handoff.ps1`/`scan_cross_machine_commits.ps1`/`delete_guard_hook.ps1`已補`[Console]::InputEncoding=UTF8`修復 ④`session_end_auto_push.ps1`commit後沒先pull就push，Mac常在推，必被拒，已補stash→`pull --rebase`→push→stash pop。四項均已pipe-test驗證＋settings.json從5支hook補到12支。已寫信通知Mac/ACER（`cross-agent/inbox/mac`+`inbox/acer`）各自要查的事（ACER要查`workspace`是否也是死clone；Mac的`.sh`版也中push-before-pull同款問題）。

### 2. ai-talk嘉義場新增設攤廠商05~10並上線（教練親口「推」確認）
教練貼EDM要求整理現場設攤編號：乾淨世界補上編號05、toooAI改06，新增07孫承宣(TimeWaver Pro)、08凌榆舜(iSmart)、09李明燦(台灣模型車博物館)、10 KR廚房(金門高粱酒喜宴酒)，共10家。逐張處理EDM圖片(EXIF/尺寸校正)+本機預覽教練確認+GitHub commit+Netlify手動zip部署，全程curl驗證文字與圖片。台南場封存區01~09未受影響。

### 3. Netlify額度校正+教練糾正設計過度工程化
教練截圖回報真實帳單949.9/1000(過期2026-09-25)，同時指出聯想這台部署完全沒被扣點過。查證根因是Mac的`netlify_deploy_guard.sh`從沒移植到聯想。**第一版做法**：照抄寫`netlify_deploy_guard.ps1`註冊成PreToolUse自動攔截hook——結果**這支hook因BOM編碼問題把自己下一個指令攔到報錯**，教練隨即糾正「你這一次用了幾次之後，你就會總結上傳，軍師那邊讀到之後就會扣掉你這個用掉的次數，就這麼簡單啊！你要算那麼久，算什麼？」。已撤掉自動化hook，改成手動記數：本場部署2次(攤商09+10)，949.9→934.9，寫回`state/netlify_deploy_quota.json`供三機git pull同步。教訓寫入[[feedback_netlify_quota_sync_simplify_2026-08-26]]。

### 4. 教練交辦：釋放聯想本機記憶體
記憶體75.1%，查證無單一失控程式，是Comet瀏覽器(32分頁程序)+多個閒置Claude背景程序+一般通訊軟體疊加。逐項確認後關閉：8個凌晨03:27起閒置無視窗標題的Claude背景程序(教練確認「不記得開著幹嘛」)、Signal/Zoom/Typeless三個確認沒在用的程式，共釋放約2.5GB，75.1%→67.8%。過程有先追溯本次bash session的程序祖先鏈，確認不誤殺自己這個對話框。

## ⚠️ 本場教訓
1. **新寫的Windows PowerShell hook上線前務必檢查BOM編碼**——這是本週第二次同款坑（第一次是`summary_upload_trigger.ps1`缺jq，這次是`netlify_deploy_guard.ps1`寫入時PowerShell的`Set-Content -Encoding UTF8`自動加了BOM，導致下游python讀取失敗；本檔本身無BOM時PS5.1會用系統codepage誤讀中文字面量，連带把here-string終止符號讀壞）。
2. **多機共享一個緩慢變動的數字，不必為了「絕對即時」建自動化攔截層**——教練親口糾正的核心判斷原則，跟先前「Netlify額度每7~10天校正一次」是同一種「別過度即時查證」的思維。

## 📋 下一場開工先做
1. 承接v135~v137舊待辦：3支孤兒hook要不要啟用（已由Mac於v135啟用，可核對）、bni-chapters「真誠分會」架構問題、OpenClaw 6.34升級教練決定、孔大哥/佩佩老師備份repo衝突（Mac v135疑似已解決，待核對）、VPS缺.gitignore（Mac v135疑似已解決，待核對）
2. ACER若查出`workspace`也是死clone，需要同款封存+junction處理（信已寄出，等ACER回報）
3. Mac的`session_end_auto_push.sh`是否也要補push-before-pull修復，等Mac自行評估

## 🔑 本場commit
`6b121713`(跨機同步四層根因全修)／`41b67ec`+`060c172`(ai-talk嘉義場攤商05~10，獨立repo)／`25b4b61d`(Netlify額度校正934.9)

---

> 📦 v137完整內容已封存：`handoff_archive/handoff_v137_archived_2026-08-27.md`（Mac桌面版，媒合改手動觸發+來賓職業補正+/find上線+4人分類修復）

# 軍師接力棒 · 2026-08-27 v139（Mac桌面版 Sonnet 5，長場：RustDesk監控修復+MiniMax紅線防護+bigtree密集迭代）

> 建立時間：2026-08-27 00:55 ~ 10:40（台灣時間，長場，教練「總結」觸發收工）
> 上一棒：v138（聯想Windows，同日上午）
> 本棒主軸：**教練逐項拆解待決定清單教會軍師更果斷後，連續處理RustDesk記憶體監控/MiniMax批次呼叫永久防線/結繩戰報系統/bigtree-tw多輪場次資訊更新，過程中兩次被教練當場糾正（輪詢設計、擅自用素材湊數）並即時修正。**

## 🎯 本場戰果

### 1. RustDesk記憶體監控真根因修復＋改事件觸發（commit`b13232eb1`／`b73ede5d`）
教練回報RustDesk用了5.48GB，查出2026-07-09建的監控腳本用`ps -o rss`量測，比Activity Monitor真實數字低估11.5倍，門檻6週來形同虛設。改用`top -stats mem`修復+立即重啟釋放記憶體。**教練隨即糾正**改成的10分鐘輪詢排程太浪費，改為：日曆型每日05:00背景安全網(維持教練原本接受的頻率)＋新增`hooks/rustdesk-free-memory-trigger`事件觸發（教練說「釋放記憶體」直接執行`scripts/rustdesk_free_memory.sh`）。

### 2. MiniMax批次呼叫紅線防護（commit`19116a313`→`bc6a33516`）
案例65事故後教練要求「畫一條紅線」，新建`scripts/minimax_batch_guard.py`，所有批次AI呼叫先過此關，5小時滾動窗口超過上限直接中止+Telegram通知。已接上namecard-db三個實際呼叫點(chain_matcher/extract/match)。教練回饋400次上限太保守會限制他自己用AI，當場拍板調整成2000次(批次)/2500次(即時互動)分配，已重新測試驗證。

### 3. 結繩領導學戰報改免登錄（commit`ec7af2d62`）
教練拍板「除了我們不會有其他人看」，`_logged_in()`永遠回傳True，登入頁程式碼保留可回退。

### 4. bigtree-tw多輪迭代（僅commit到GitHub，未推Netlify，等教練「推」）
- 補齊5場地址（再耕園/KR養生廚房/台中場/新增9/16高雄場/10/7-8台南場）
- 修正9/16場地樓層錯誤：教練確認郭音樂廳主會場在2樓(100人)非4樓(僅20人)，歷史紀錄與現場資料同步改正
- 9/16拆上午/下午兩場方便報名(各300元，合報500元)；9/23/24/10/7/8補上1800元票價；9/22下午場主題改AI微論壇+晚場價格888→500元
- 新建`scripts/check_archive_gaps.py`找出歷史紀錄缺漏，教練提供5張EDM後補上8/21/8/22金門+8/26兩場，歷史紀錄16→20場
- **教練當場糾正**：8/28佔位圖片(借用ai-talk-tw既有照片湊數)已撤回——教練說「稍等我一下，828做完了會提供給你，不要瞎跑」，只保留9/5(教練已提供真EDM)這筆參考紀錄

### 5. 新建活動前提醒SOP＋兩項FB/提醒待辦記憶
`scripts/event_reminder_day_before.py`每天09:00檢查明天有無場次，整理報名名單發Telegram給教練，教練再到LINE@後台手動私訊(回覆不扣額度)。已用真實8/28嘉義場40人資料驗證送達成功。另記錄教練規劃中的「FB粉專行銷自動化」(待教練提供粉專名單才開工)。

### 6. 意外發現：Stop hook輪詢偵測機關瞎眼35天（已拆成背景任務task_6a5d5cde處理中）
教練糾正RustDesk 10分鐘輪詢設計時，查證發現本機專門攔截「每N分鐘檢查」話術的Stop hook自2026-08-12合併重構後，真實對話中從未再攔到過任何違規(log最後一筆是08-12的測試session)，即使教練這次抓到的案例regex明明命中也沒被攔下。已拆成獨立背景任務調查修復，不佔用本場時間。

## ⚠️ 本場最重要教訓

1. **教練明講「我在做/我會提供」某素材時，等於明確劃出「這部分不用AI代勞」的界線**——即使用既有正當素材湊數也不行，教練要的是他準備的東西，不是AI覺得堪用的替代品。
2. **輪詢vs事件驅動的原則不因為「這次是背景安全網」就自動免死**——RustDesk案例證明就算改成低頻率(10分鐘)也可能被視為浪費，真正的判斷標準要回到「教練自己有沒有更好的觸發時機點」。
3. **記錄「已建立防呆機關」不能只憑腳本檔案存在**——這是本場第7次抓到「機制看似運作實則失效」的形狀(RustDesk用錯量測單位、Stop hook輪詢偵測瞎眼)，任何自稱已有的防護都要找真實觸發證據，不能只看log格式正常。

## 📋 下一場開工先做

1. bigtree-tw等教練看過GitHub確認後說「推」，一次性部署Netlify（目前commit`ce46737`已是最新）
2. 教練有空時提供8/28正式EDM/網頁，再補進歷史紀錄
3. Stop hook輪詢偵測修復進度查看background task結果
4. MEMORY.md索引檔已接近讀取上限，已拆背景任務(task_b6f4e1a5)進行整併瘦身
5. 承接舊待辦：3支孤兒hook已啟用完畢、bni-chapters「真誠分會」架構問題仍卡教練說明、孔大哥/佩佩老師備份repo已解決、VPS缺.gitignore已解決

## 🔑 本場commit
`b13232eb1`+`b73ede5d`+`3aa9ba201`(RustDesk監控修復+事件觸發)／`19116a313`+`bc6a33516`(MiniMax紅線防護)／`ec7af2d62`(結繩戰報免登錄)／`5779162`~`ce46737`(bigtree多輪，共約8個commit，詳見bigtree repo log)／`22f1d5faf`(活動前提醒SOP)

---

