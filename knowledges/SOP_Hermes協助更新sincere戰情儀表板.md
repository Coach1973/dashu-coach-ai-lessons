# SOP：Hermes怎麼協助更新 sincere.bymyway.com 每週戰情資料

> 🗣️ **教練口語叫法**：「更新真誠數據」「更新真誠戰情」「真誠例會出席報告」「真誠這週的資料」
> ＝教練貼了真誠分會例會出席報告（應到/準時/缺席/早鳥/來賓名單）→ 照第5節總表，
> 用 `scripts/sincere_weekly_update_20261001.py` 複製改名單寫入（Mac本機才連得到資料庫；
> 聯想/宏碁收到這句話，把報告整理成信寄到Mac信箱 `cross-agent/inbox/mac/`），
> 寫完用網頁核對（不截圖，文字比對）。

> 2026-09-30建立（Mac桌面版軍師 Sonnet 5）。
> **對象更正**：原始接力棒寫「小龍蝦已派給軍師的任務」是轉述錯誤——19:49教練是在
> **Hermes桌面版**跟Hermes說「你寫一封信給軍師」，小龍蝦Telegram收到的是教練自己
> 貼過去的同一段話，不是小龍蝦主動發起。查證見記憶
> `feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22.md`。
> 本SOP因此是寫給**Hermes**看的，教練要Hermes協助更新每週出席/來賓資料。

## 1. sincere.bymyway.com 是誰管的

**軍師（Mac本機）自己管，不是VPS、不是其他人。**

- 原始碼：`~/github_repos/zhencheng-guests/`（git repo：`Coach1973/zhencheng-guests`，
  資料庫`zhencheng_guests.db`本身`.gitignore`排除，未版控——只有程式碼進git）
- 技術棟：Flask + SQLite，`app.py`跑在`localhost:5090`
- 常駐服務：launchd `com.coach.sincere-webapp`（跑Flask App，KeepAlive）+
  `com.coach.sincere-tunnel`（cloudflared tunnel，把`sincere.bymyway.com`轉到
  `localhost:5090`）——兩個都在跑，教練不用手動啟動任何東西
- **這是純檢視型儀表板，3個POST API目前沒有登入驗證/token**（路徑大全已記錄「網址
  本身視為半公開」）。這不是bug要修，是設計時就這樣定的——公開網址本身就是一種
  存取控制（教練/助理大使群裡才知道網址），暫不建議加驗證機制，除非教練要求。

## 2. 讀資料方式

- **看目前畫面**：直接瀏覽`https://sincere.bymyway.com/`，首頁會列出3組、在籍15位會員
  （資料庫16筆，其中1位`left_chapter=1`已離會、不列入）、每週來賓/121/咖啡會議/早鳥/
  出席統計、來賓完整名單、全國見證分享會出席、培訓出席。
- **查資料庫現況**（比看網頁更準，尤其要核對member_id時）：
  ```bash
  sqlite3 ~/github_repos/zhencheng-guests/zhencheng_guests.db \
    "SELECT id, name, team FROM members ORDER BY sort_order;"
  ```
  常用表：`members`（16筆、在籍15人）、`weeks`（週次+是否列入計算）、`weekly_data`
  （每人每週guests/ones/coffee/early_bird/attendance/proxy）、`guest_list`（來賓姓名/專業/邀約人，
  跟`weekly_data.guests`是分開兩份資料，見下方3.3）、`testimony_sessions`+
  `testimony_attendance`（全國見證分享會）、`training_sessions`+`training_attendance`
  （培訓出席）。

## 3. 更新payload——分三種情況，方法完全不同

### 3.1 會員自填（121、咖啡會議）——已有API，教練/軍師不用管

```
POST http://localhost:5090/api/update_metric
{ "member_id": 5, "week_date": "2026-09-24", "metric": "ones", "value": 2 }
```
`metric`只接受`"ones"`或`"coffee"`——**這是`db.MEMBER_EDITABLE_METRICS`寫死的白名單**，
會員自己在網頁上點格子填就會呼叫這個API，不需要Hermes或軍師介入。

### 3.2 全國見證分享會 / 培訓出席——已有API，教練提供名單時用這兩個

```
POST http://localhost:5090/api/update_testimony
{ "member_id": 5, "event_date": "2026-08-24", "attended": 1 }

POST http://localhost:5090/api/update_training
{ "member_id": 5, "session_id": 3, "attended": 1 }
```
`attended`：`1`=YES、`0`=NO、`null`=未填。`session_id`要先查`training_sessions`表
對應的id（不是日期）。這兩個API可以用curl直接打，不用碰資料庫。

### 3.3 🔴 教練口述提供的資料（來賓人數、來賓名單、早鳥、新會員）——**沒有API，
必須直接寫SQL，絕對不能重跑`seed.py`**

**這是教練最常提供、也最容易出錯的一種。三個子項目：**

**① 每週來賓人數**（`weekly_data.guests`，每位會員一個整數）：
```bash
sqlite3 ~/github_repos/zhencheng-guests/zhencheng_guests.db \
  "INSERT INTO weekly_data (member_id, week_date, guests) VALUES (5, '2026-10-01', 2)
   ON CONFLICT(member_id, week_date) DO UPDATE SET guests=excluded.guests;"
```
用`INSERT...ON CONFLICT DO UPDATE`（UPSERT），不會動到同一列的`ones`/`coffee`
（那兩欄是會員自己填的真實資料，絕對不能被洗掉）。

**② 完整來賓名單**（`guest_list`表，姓名/專業/邀約人，跟①是分開的兩份資料，
一份是數字統計、一份是完整名單，兩份都要補才算做完）：
```bash
sqlite3 ~/github_repos/zhencheng-guests/zhencheng_guests.db \
  "INSERT INTO guest_list (week_date, name, profession, inviter)
   VALUES ('2026-10-01', '王小明', '保險業', '陳佩君');"
```
**單純INSERT，不要用DELETE，一個來賓一筆。**

**③ 早鳥**（`weekly_data.early_bird`，1=有上線、0=沒有）：
```bash
sqlite3 ~/github_repos/zhencheng-guests/zhencheng_guests.db \
  "INSERT INTO weekly_data (member_id, week_date, early_bird) VALUES (5, '2026-10-01', 1)
   ON CONFLICT(member_id, week_date) DO UPDATE SET early_bird=excluded.early_bird;"
```

**④ 新會員加入**（比照09-10新增黃秀麗/張玉盞的既有案例）：
```bash
sqlite3 ~/github_repos/zhencheng-guests/zhencheng_guests.db \
  "INSERT INTO members (name, team, sort_order, active_from) VALUES ('新會員姓名', '羽宙奇蹟', 6, '2026-10-08');"
```
`active_from`填「下一週」（比照張育慈8/27加入、張玉盞/黃秀麗9/10加入都是從下一週
才起算統計的既有慣例），`team`要是`teams`表已有的三個組名之一。

### 🔴🔴 危險：`seed.py`已經過期，現在絕對不能重跑

`~/github_repos/zhencheng-guests/seed.py`是09/12更新09/03+09/10資料之後就沒人再
同步過的**舊版種子腳本**——它的`WEEKS`/`GUEST_DATA`/`GUEST_LIST`常數只到08/27，
`MEMBERS`只有14人（沒有黃秀麗/張玉盞）。實際資料庫早就是16位會員、`guest_list`
有94筆到09/10。

`seed.py`裡`guest_list`的寫法是**先`DELETE FROM guest_list`清空全部，再照腳本裡的
`GUEST_LIST`字典重新灌**——如果現在誰跑了`python3 seed.py`，會把09/03之後所有
新增的來賓名單（超過60筆真實資料）整個刪光，只剩腳本裡舊的29筆。這符合執行細則
N6「危險指令零容忍」裡「DELETE FROM...(無WHERE)」的等級。

**規則：往後都用3.3的直接SQL INSERT/UPSERT個別更新，不要再碰`seed.py`。**
如果哪天真的要讓`seed.py`重新變成「可信的完整重建腳本」，必須先把它的四個常數
從目前資料庫內容重新產生一份對照更新，這是一次性的技術債整理，不是日常流程，
需要另外評估、不要順手做。

## 4. 權限邊界

- 3個POST API**沒有登入驗證**，任何知道網址的人理論上都能打——目前教練接受
  這個風險（純檢視型儀表板，網址半公開，教練圈子裡才知道），**不用主動加驗證**，
  除非教練明確要求。
- 直接寫資料庫（3.3的SQL）**只有軍師（Mac本機）能做**——Hermes若要更新來賓/早鳥
  /新會員這三類資料，做法是：Hermes把教練口述的原始文字整理成結構化內容（比照
  本SOP格式），寫進`JUNSHI_HANDOFF_LATEST.md`或`cross-agent/outbox/`，軍師收到後
  執行SQL、瀏覽器核對、回報完成。**Hermes不需要、也不應該自己嘗試連進這台Mac的
  SQLite檔案**（除非確認Hermes跟軍師是同一台Mac上兩個獨立能存取檔案系統的助理，
  這點目前未驗證，先走「Hermes整理、軍師執行」的分工比較保險）。

## 5. 會員自填 vs 教練/軍師提供，怎麼分（總表）

| 資料 | 表/欄位 | 誰填 | 怎麼填 |
|---|---|---|---|
| 121次數 | `weekly_data.ones` | 會員自己 | 網頁點格子→`/api/update_metric` |
| 咖啡會議次數 | `weekly_data.coffee` | 會員自己 | 網頁點格子→`/api/update_metric` |
| 全國見證分享會出席 | `testimony_attendance` | 會員自己 | 網頁點YES/NO→`/api/update_testimony` |
| 培訓出席 | `training_attendance` | 會員自己 | 網頁點打勾/打叉→`/api/update_training` |
| 來賓人數 | `weekly_data.guests` | 教練口述→軍師寫入 | 直接SQL UPSERT（3.3①） |
| 來賓名單(姓名/專業/邀約人) | `guest_list` | 教練口述→軍師寫入 | 直接SQL INSERT（3.3②） |
| 早鳥 | `weekly_data.early_bird` | 教練口述→軍師寫入 | 直接SQL UPSERT（3.3③） |
| 新會員加入 | `members` | 教練確認→軍師寫入 | 直接SQL INSERT（3.3④） |
| 例會出席狀態 | `weekly_data.attendance`（`present`/`late`/`absent`）＋`proxy`（代理人，只有出席時才算） | 教練口述報告→軍師寫入 | 該週`weeks`已建立→`POST /api/update_attendance`（`{member_id,week_date,value,proxy}`）；`weeks`還沒有該週就回「此週次不開放填寫」，要先建週次（見下） |

**出席欄位（2026-10-01 起已有，舊版寫「系統沒有出席欄位」已過時）**：儀表板的出席統計
是從`07/23`起逐週算的，教練貼的「真誠例會出席報告」(P)準時/(A)缺席/(L)遲到/(M)病假/
(S)代理要拆成每人每週的`attendance`。**每週新增例會要先在`weeks`表建一筆**
（`week_date`/`label`/`is_active=1`/`sort_order`＝目前最大值+1），之後才寫得進去。

**每週例會一次寫入範本**：`scripts/sincere_weekly_update_20261001.py`
（2026-10-05 寫入10/01那週，聯想軍師寫、Mac軍師跑）——一支腳本做完建週次＋全員出席＋
早鳥＋來賓人數＋來賓名單，`--dry-run`先看、正式跑會先備份資料庫、重跑不會重複也不會洗掉
會員自填的121/咖啡、在籍人數不對或找不到會員名就中止不寫。下週複製一份改`WEEK`/
`EARLY_BIRD`/`GUESTS`/出席例外名單即可，**不要碰`seed.py`**。

**仍然沒有的**：參訪人員（例如教練本人「大樹執董」不是來賓，不寫）、6個月累計
代理/缺席/遲到（累計沒有發生日期，對不上哪一週，系統沒有地方放）。教練若要這些上
儀表板屬新功能，另外跟教練確認。

## 6. 失敗處置

- 每次寫入後**務必打開`https://sincere.bymyway.com/`實際核對數字/名單真的換新**
  （2026-09-12的信裡就強調過這點：不要只信SQL執行成功，要親眼看網頁）。
- `INSERT INTO members`時`team`打錯字（不是三個組名之一）不會報錯但畫面會把該
  會員歸到「待指派」區——寫入後順便確認畫面分組正確。
- `member_id`或`session_id`填錯查無此人/場次，`update_testimony`/`update_training`
  API會回`404 查無此會員或場次`，先用`sqlite3 ... "SELECT id,name FROM members"`
  查對id再打。
- SQLite寫入是逐筆生效，Flask每次讀取都是即時查詢（沒有快取），寫完不用重啟
  `com.coach.sincere-webapp`服務，網頁重新整理就會看到新資料。

## 相關

- 舊案例（09-12聯想Windows軍師→Mac軍師的信，已完整驗證「來賓」欄位網頁上沒有
  可編輯輸入框的結論，本SOP延續同一個結論）：
  `cross-agent/outbox/2026-09/20260912-1344_lenovo-to-mac_sincere-guest-record-update-0903.md`
- 身份歸屬更正記錄：`feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22.md`
