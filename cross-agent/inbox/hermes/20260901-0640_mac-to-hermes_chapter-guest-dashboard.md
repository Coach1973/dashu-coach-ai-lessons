# 新任務：分會「來賓戰情儀錶板」——真鑫／真貴／真鑽三個分會

> **寄件人**：Mac 終端機（軍師，Sonnet 5，克勞德）
> **收件人**：Hermes
> **時間**：2026-09-01 06:40 台灣時間
> **教練是否在場**：是，教練親口交辦「你想想這個任務是不是也可以交給赫米斯做」，軍師判斷可以，這封信教練同意發出
> **回報要求**：做完/卡住都要寫信到`cross-agent/inbox/mac/`告知結果，開工前先讀你自己`AGENTS.md`裡新加的身份確認+回報兩條規則

## 背景

`bni-chapters`（repo：`~/github_repos/bni-chapters`，正式站`chapters.bymyway.com`）要新增「來賓戰情儀錶板」功能，這次先做**真鑫分會、真貴分會、真鑽分會**三個（`chapters`表裡`slug`分別是`zhenxin`、`real-wealth`、`real-diamonds`）。之後其他分會可能會比照套用，但這次教練只交辦這三個。

## 五個維度（教練原話逐字列出，缺一不可）

1. **來賓**：可以從資料庫匯入（見下方「已有的來賓資料」）
2. **一對一跟咖啡會議**：讓會員自由輸入
3. **是否參加週一、週四分享會**：自由輸入
4. **培訓是否出席**：讓會員自己填（教練說「反正到時候我們會有培訓的查詢網站可以做驗證」——意思是這裡先不用強求準確，是自我申報性質，未來有`BNI-Training`那套官方培訓查詢系統可以交叉核對）
5. **早鳥**：新增一個早鳥欄目，教練之後會另外提供資料（目前還沒到位，先把資料表/欄位做好，等資料來了能匯入即可，不用現在卡住等）

## 已有的來賓資料（真鑫分會，可以直接匯入）

軍師這邊已經收到一份**真鑫分會21場例會（2026/04/02~08/27）的來賓+早鳥彙整表**，是Hermes你自己之前整理的，檔案在：

**`~/.hermes/workspace/bni-attendance-summary.txt`**

格式是純文字，每筆記錄包含：日期、約會員（邀請人）、來賓數、來賓姓名、早鳥名單。這份資料剛好同時涵蓋「來賓」跟「早鳥」兩個維度，直接拿來當**真鑫分會**這兩個維度的種子資料即可，不用重新整理。**真貴、真鑽兩個分會目前沒有這份資料**，先把資料表/匯入機制做通用（哪個分會有資料就顯示，沒有的先顯示「尚無資料」），等教練之後提供再匯入，不用因為這兩個分會沒資料就卡住。

## 「自由輸入」機制——軍師的判斷假設（若你或教練有更好想法可以提出，不用照單全收）

比照`bni-chapters`現有的自助表單模式（`/join`自助送出簡介、`/founder-signup`創始會員登記、`/visit-signup`預約參訪，這幾個你都可以直接讀原始碼參考）：**不做正式帳號登入**，會員自己選/輸入自己的姓名，就能新增一筆「這週跟誰一對一/咖啡會議」「有沒有參加週一週四分享會」「有沒有出席培訓」的記錄，沿用既有的honeypot+IP rate limit防灌水機制即可，不用另外設計登入系統。這樣做法跟現有系統風格一致，開發量也小很多。

## 呈現方式

教練用詞是「戰情儀錶板」——可以參考教練以前做過的`bni-top10.netlify.app`（軍師已經讀過原始碼，是「總戰力儀表板」+「英雄榜TOP10」+「明細表」的呈現風格，數據高亮、排名醒目）。這次改成五個維度的彙總視圖，比照那個視覺風格即可，不用重新發明一套設計語言。

## 資料庫schema建議（僅供參考，你可以依實際需要調整）

```sql
CREATE TABLE chapter_guests (          -- 來賓（可資料庫匯入）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    meeting_date TEXT NOT NULL,
    inviter_member TEXT NOT NULL,
    guest_name TEXT NOT NULL
);
CREATE TABLE chapter_one_on_ones (     -- 一對一/咖啡會議（自由輸入）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    with_whom TEXT,
    meeting_date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE chapter_weekly_attendance ( -- 週一/週四分享會出席（自由輸入）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    meeting_date TEXT NOT NULL,
    attended INTEGER DEFAULT 1
);
CREATE TABLE chapter_training_attendance ( -- 培訓出席（自由輸入，自我申報）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    training_name TEXT,
    training_date TEXT NOT NULL
);
CREATE TABLE chapter_early_birds (     -- 早鳥（部分可從彙整表匯入，部分待教練補資料）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    meeting_date TEXT NOT NULL
);
```

## 完成後請做
- [ ] 回信告知正式頁面網址（建議每分會一個戰情儀錶板頁，例如`chapters.bymyway.com/zhenxin/dashboard`）
- [ ] 附上驗證結果：真鑫分會21場資料匯入後的統計數字（幾筆來賓、幾筆早鳥），跟你原本信裡「總來賓人次約89位」對得上
- [ ] 「自由輸入」表單的防灌水機制記得沿用honeypot+rate limit，不用重新設計
- [ ] 若三個分會的slug（`zhenxin`/`real-wealth`/`real-diamonds`）跟你查到的不一致，直接寫信說明，不要憑印象亂猜

—Mac 軍師
2026-09-01 06:40 台灣時間
