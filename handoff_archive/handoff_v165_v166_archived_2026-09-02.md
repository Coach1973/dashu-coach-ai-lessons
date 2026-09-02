# 軍師接力棒 · 2026-09-02 v165（聯想Windows Sonnet 5，新增「大樹教練待辦事項」系統，事碼已完成待Mac部署上線）

> 建立時間：2026-09-02 12:56 ~ 13:40（台灣時間）
> 上一棒：v164（聯想Windows，coach888作品總覽表重整）
> 本棒主軸：**教練交辦仿Microsoft To Do的個人待辦提醒系統，要嵌進作品總覽獨立分頁+到期主動發Telegram提醒。程式碼已寫完、本機測試通過，但這台機器碰不到event.bymyway.com的正式服務，需要Mac那邊pull+重啟+註冊cron才算真正上線。**

## 🎯 本場戰果

### 1. 待辦事項系統程式碼完成，路由掛在event-signup（不新增獨立子網域）
教練確認三個方向：①放coach888獨立分頁（不擠進首頁）②核心夠用版（標題/到期日/提醒時間/完成/備註，先不做子步驟/重複規則）③提醒沿用教練個人Telegram通道(`chat_id 6124913915`，跟mentor100/信用証到期提醒同一條)。比照既有bymyway動態渲染架構，掛在`event-signup`這支24小時跑的Flask app底下（不新增子網域/Tunnel/launchd，同一套「降低服務被遺忘風險」邏輯）：
- `schema.sql`新增`todos`表
- `app.py`新增`/todo`(列表+新增表單)、`/todo/add`、`/todo/<id>/toggle`、`/todo/<id>/delete`四個路由，到期日徽章分四級（逾期紅/今天橘/3天內金/其餘灰）
- `templates/todo.html`新模板，沿用`wheel.html`同款深色主題CSS變數
- `scripts/todo_reminder_check.py`：獨立cron腳本，比照`bni_credit_expiry_reminder.py`同款設計（查remind_at到期未通知項目→`notify_coach.sh`發送→成功才寫回`reminder_sent`，避免送達失敗卻誤記已通知）

### 2. 本機測試方法+驗證結果
這台機器沒有正式`event.db`（只在Mac上是活的），用舊備份`event.db.bak-before-session-admin-20260823-085851`複製成臨時測試db、`EVENT_PORT=5099 python app.py`起本機Flask dev server，經由瀏覽器/curl實測：新增待辦（真實表單送出，含中文標題/備註/到期日/提醒時間）、到期徽章正確判斷「已逾期13天」、完成勾選切換（含已完成清單展開/取消完成）、刪除，全部正常；`todo_reminder_check.py --dry-run`正確抓到到期未通知項目並組出訊息。測試完已刪除臨時db，git status確認乾淨才commit。過程中發現`print()`遇到emoji在這台Windows主控台的cp950 codepage會UnicodeEncodeError（純Windows console限制，Mac預設UTF-8不會發生），順手加了`sys.stdout.reconfigure(encoding="utf-8")`防呆。

### 3. coach888作品總覽新增連結，過程中合併衝突+意外揪出真的資料遺失
新增「大樹教練待辦事項（特助主動提醒版）」到「四、bymyway自架版」分區（第6項），順手修正該分區ai-talk項目殘留的過時文字「9/22台南場更新中」（已於9/1由Mac完成上線，見v153/v155）。push時發現遠端同時有另一場session上線了收合/刪除項目/新增項目的編輯UI功能，手動解衝突保留兩邊改動。**過程中意外發現「大樹常用」分區的`BNI-Training`(BNI培訓紀錄總資料庫)整筆消失**，但該分區仍標「17項」跟實際16項目對不上——判斷是那次UI升級測試「刪除項目」按鈕時誤刪、複製排序貼回AI固化時沒發現少一筆，非教練或任何人刻意移除，已補回並確認全部8個分區「宣告項目數＝實際項目數＝連續編號」三者一致才收工。

## ⚠️ 下一場開工先做（Mac優先，這是本棒唯一待完成的事）
**`/todo`要真正上線，需要有Mac終端機存取權限的軍師做完以下步驟**（這台聯想機器碰不到`event.bymyway.com`正式服務跟Mac的OpenClaw cron系統）：
1. `cd ~/.openclaw/workspace && git pull`（拉到本棒的`todos`表schema+四個路由+`todo.html`+`todo_reminder_check.py`）
2. 重啟`com.coach.event-webapp`（`launchctl kickstart -k`或教練慣用指令）——`db.init_db()`會自動幫`event.db`補上`todos`表，不用手動下SQL
3. `curl https://event.bymyway.com/todo`確認200，瀏覽器實測新增一筆待辦+切換完成+刪除，跟本機測試流程一樣跑一次
4. 註冊OpenClaw cron，每15分鐘跑一次`python3 ~/.openclaw/workspace/scripts/todo_reminder_check.py`（比照信用証提醒cron`8211e054`的建法），先用`--dry-run`確認邏輯正常再拿掉
5. 完成後回coach888確認`/todo`連結真的能點得進去，這棒才算真正結案
**教練尚未提供任何真實待辦事項**，上線後是空清單，等教練自己輸入第一筆。

## 🔑 本場commit
`workspace`：`57d53268`（todos表+路由+模板+cron腳本）→`14d51a67`（pull merge，含namecard-db其他session的並行改動）。`coach888`：`54620ec`（新增待辦連結+ai-talk文字修正）→`0119f76`（解衝突+補回BNI-Training遺失項目）。

---

# 軍師接力棒 · 2026-09-02 v166（Mac終端機 Sonnet 5，名片系統來賓完整訪問歷程+帳號審核機制(2輪設計)+coach888批量搬移/改名功能+RustDesk卡頓診斷+讀跨機信）

> 建立時間：2026-09-02 12:40 ~ 17:02（台灣時間）
> 上一棒：v165（聯想Windows，待辦提醒系統程式碼完成待Mac部署）
> 本棒主軸：**名片系統(namecard-db)兩項重大功能——來賓完整分會訪問歷程(取代只顯示最新一筆)、帳號審核機制(教練需求歷經2輪簡化定案為全站需登入)；coach888新增批量搬移分類+項目改名功能；診斷並修復RustDesk記憶體異常，教練登出重登入後系統恢復正常；讀取聯想軍師來信但依教練指示暫不執行部署。**

## 🎯 本場戰果

### 1. namecard-db：來賓完整訪問歷程上線
教練回報`/find`搜尋來賓只看得到現任/前會員標記，看不到「這是哪個分會的來賓、什麼時候來過」。查明`guests`表原本只保留「最新一次」訪問的分會、無日期欄位。新增`guest_visits`子表，從BNI Connect完整歷史報表（2018-08-08~2026-09-01全部訪問紀錄）重建，`/find`搜尋結果會列出每位來賓完整的分會+日期清單。3222位不重複來賓（依電話去重），320人有多筆歷史紀錄，最多7次橫跨2分會。已用真實資料在瀏覽器驗證（葉俊麟3次真鑽、黃建豪橫跨真富/真鑫共7次）。commit`db21d10a5`。教練隨後確認「不同電話號碼才是精準」數字口徑（namecard-db的3222 vs 另一套BNI-Training系統的3718是不同口徑：去重人數 vs 訪問紀錄總筆數，非誤差）。

### 2. namecard-db：帳號審核機制，歷經2輪簡化才定案
教練最初構想是完整的「AI資源媒合系統」品牌入口：正規申請審核+BNI分會/職稱/email欄位。經討論後教練親自簡化：**申請只要姓名+行動電話，密碼統一預設88888，不做email驗證**。第一版實作只鎖「跟進」功能需要登入（查詢/瀏覽維持公開），commit`bb25684eb`。上線後教練回報「如果他們上傳名片，我才知道是誰上傳的」，**推翻改成全站都要登入**（含`/`、`/find`、`/chains`、`/matches`、`/card/<id>/match`、`/guest/<id>/match`、`/upload`），`cards`表新增`uploaded_by`欄位記錄上傳者，commit`1aa5ddfba`。過程中發現`team_login_required`裝飾器原本定義在使用它的路由之後，Python裝飾器載入時期就要能解析到，已搬移到檔案最前面。教練自己(bymyway)＋既有夥伴帳號(佩君老師)透過schema遷移自動標記approved，完全不受影響，已用真實HTTP流程驗證申請→核准→登入→上傳全流程。詳見記憶`project_namecard_login_gate_and_guest_history_2026-09-02`（含更新舊記憶`project_namecard_manual_trigger_matching_design_2026-08-27`附加說明）。

### 3. coach888：新增批量搬移分類+項目改名功能
教練提出兩個UI痛點：①想勾選多個項目一次搬到某分類，不想一個個拖 ②想自己修改項目顯示名稱（把「BNI｜出席戰情儀表板」改成「DNA出席」，因為那顆儀表板其實是追蹤DNA出席狀況）。新增「☑️批量搬移模式」按鈕（開啟後每項目旁出現checkbox，勾選後下方浮現搬移列）+每個項目名稱旁新增✏️改名圖示，皆沿用既有localStorage固化模式(跟現有badge/title編輯機制一致)。「DNA出席」已直接改在原始碼。已用本機http server+瀏覽器JS互動測試驗證：勾選搬移1項到「BNI專用」分類，來源/目標分類編號+項目數正確更新；改名功能DOM+localStorage正確持久化；「複製排序」按鈕正確反映改名和搬移結果。commit`99dcff3`，已用Chrome實際打開確認畫面。同場也補上namecard-db帳號審核頁的coach888直達連結（`f35fc2f`+合併`5aff51c`，過程撞到聯想同時推送的收合/刪除功能merge衝突，已妥善解決）。

### 4. RustDesk記憶體異常診斷+教練登出重登入排除卡頓
教練回報Mac很卡，查證找到RustDesk（教練遠端操控這台Mac用的程式）記憶體膨脹到761MB，用既有`scripts/rustdesk_free_memory.sh`重啟後降回30MB，系統可用記憶體回到76~80%健康水準。教練詢問「登出再登入」是否可行，查證確認這台Mac已裝RustDesk系統層級unattended-access服務（`/Library/LaunchDaemons/com.carriez.RustDesk_service.plist`），登出後仍能透過RustDesk連到登入畫面，屬安全操作。教練登出重登入後，系統負載從瞬間飆升的43（多程式同時重啟造成的正常尖峰）在2.5分鐘內回落到12左右，記憶體維持80%健康水位，確認恢復正常。

### 5. 讀取聯想軍師跨機來信，依教練指示暫不執行
教練說「請收信，聯想軍師有任務，可以先讀，然後，我新開對話再執行」。已讀完v165交接信全文（待辦提醒系統部署5步驟），摘要回報教練，**依指示不執行部署**，信件保留在`inbox/mac/`未歸檔，等教練開新對話框時再走部署流程。

## ⚠️ 下一場開工先做
1. **最優先**：教練待辦提醒系統部署5步驟（詳見本表最上方新增列＋v165接力棒完整內容）。
2. namecard-db後續：教練若反映其他分會(真誠/真鑫)PALMS資料或帳號審核流程有問題，優先處理。
3. v161之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、12月主題培訓內容等）本場均未觸及，繼續掛著。
4. **本場無新教訓寫入試金石**——過程順利，教練兩次推翻設計是正常需求釐清（先簡化申請流程、後推翻存取範圍），非AI犯錯。

## 🔑 本場commit
`namecard-db`（workspace repo內）：`db21d10a5`（guest_visits來賓完整訪問歷程）→`bb25684eb`（帳號審核第一版，跟進限定）→`1aa5ddfba`（帳號審核最終版，全站需登入+uploaded_by）。`coach888`：`f35fc2f`（帳號審核直達連結）+合併`5aff51c`→`99dcff3`（批量搬移+改名功能，DNA出席改名）。記憶：新增`project_namecard_login_gate_and_guest_history_2026-09-02`+更新`project_namecard_manual_trigger_matching_design_2026-08-27`。

---

