# BNI 例會來賓與早鳥彙整表（已完成，請軍師直接用）

> **寄件人**：Hermes（M3，終端機）
> **收件人**：Mac 終端機（軍師，克勞德）
> **時間**：2026-09-01 06:38 台灣時間
> **教練是否在場**：是，教練親口指示「寫封信給軍師依據你這裡的統計結果，叫俊源去讀信，不用重新製作」

---

## 1. 已完成的事

我（Hermes）已整理好 21 場 BNI 例會的「來賓 + 早鳥」彙整表，檔案在：

**`/Users/bymyway/.hermes/workspace/bni-attendance-summary.txt`**（12873 bytes）

---

## 2. 整理的規則（教練 2026-09-01 親口確認）

1. **只記約來的來賓**：原始資料裡有寫「🟠來賓/會員」就算一筆，沒寫的不算
2. **三個字不一樣才算不同人**：比對名字時只要有任何一個字（含異體字、罕見字、Unicode 編碼不同）不一樣，就算兩個人；完全一樣才算同一個人。例如：
   - 「謝盛峯」「謝盛峯」→ 同一人
   - 「連晧宇」「連浩宇」「連皓宇」→ 三個不同人（第 2 個字不同）
   - 「楊凱爲」「楊凱為」→ 不同人（第 3 個字「爲(7232)」vs「為(70BA)」異體字）
3. **不記缺席、不記遲到、不記代理人**：教練沒交代就不整理
4. **早鳥每週每人只有一項紀錄**：即使原始資料「柯炫任」寫兩次也只算一次（同一週同人只一筆）
5. **來賓會變會員**：早期是某會員邀來的來賓，後來可能自己變成會員，整理時要保留「原始邀約關係」同時標記「現在是否為會員」
6. **「自行出席」**：原始資料出現「🟠OOO」沒有斜線/邀約會員 = 該會員當天自己到了但沒約人，整理成「約會員 = OOO，來賓數 = 0，備註 = 自行出席」

---

## 3. 統計摘要（已寫在 TXT 檔尾端）

| 項目 | 數字 |
|------|------|
| 總場次 | 21 場（2026/04/02 ~ 2026/08/27） |
| 總來賓人次 | 約 89 位 |
| 總邀約會員人次 | 約 65 位次（含重複計算） |
| 早鳥最穩定會員 | 陳俊源（21 場全勤） |
| 邀來賓最多會員 | 柯宗佑（12 位） |

⚠️ **這兩個統計數字是 Hermes 用 grep 粗估的**，軍師做資料庫時請用 `SELECT ... GROUP BY` 重算，數字可能差 1~2 位（特別是同名同姓的柯炫任、楊凱爲/楊凱為異體字等需要合併或拆開的邊界 case）。

---

## 4. 請軍師接手做

請直接讀 `~/.hermes/workspace/bni-attendance-summary.txt`，**不用重新製作這份資料**。

讀完後建資料庫時建議的 schema（僅供參考，不強制）：

```sql
-- 來賓表（每一筆 = 一個來賓當天出席）
CREATE TABLE meeting_guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_date TEXT NOT NULL,         -- 2026-04-02 格式
    inviter_member TEXT NOT NULL,       -- 約會員
    guest_name TEXT NOT NULL,           -- 來賓姓名
    is_self_attend INTEGER DEFAULT 0    -- 1 = 自行出席（會員當天沒約人）
);

-- 早鳥表（每一筆 = 一個人當天 6:30 前到場）
CREATE TABLE meeting_earlybirds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_date TEXT NOT NULL,
    member_name TEXT NOT NULL
);
```

---

## 5. 已知邊界 case（給軍師處理時參考）

- **柯炫任邀自己**：4/2 第 8 筆「🟠柯炫任」邀「柯炫任」→ 三個字完全一樣 = **同一個人**，邀約記錄保留一次（不是兩個柯炫任）
- **柯炫任早鳥名單重複**：原始資料 4/2、5/7、8/13 都寫兩次「柯炫任」→ **同一人每週只算一次早鳥**，請用 DISTINCT 或 GROUP BY 去除重複
- **楊凱爲 vs 楊凱為**：5/21 寫「楊凱爲 (7232)」、6/4 寫「楊凱為 (70BA)」→ 第 3 個字 Unicode 編碼不同 = **兩個人**，不要合併
- **連晧宇 vs 連浩宇 vs 連皓宇**：原始資料混用三種寫法（第 2 個字不同）→ **三個不同人**，不要合併
- **「自行出席」怎麼算**：4/30 徐偉倫、5/7 范郁琪，這兩場是「會員當天有出席但沒約人」，建議 `is_self_attend=1` 表示「該會員當天自己出席、沒約人」
- **來賓轉會員**：整理時建議 `guests` 表保留所有歷史來賓（即使後來變會員），用 `current_member_id` 欄位標記「現在是否已是會員」。範例：
  - 蔡姵彤：5/21 被買駿航邀為來賓 → 7/16 自己邀蔡雨蓉、7/23 之後開始出現在會員名單 → 已轉會員
  - 范郁琪：4/16 被薛如媛邀為來賓 → 5/14 自己邀鄧榆衡（已是會員身份）
  - 楊凱爲（5/21）vs 楊凱為（6/4）→ 兩個不同人，**不要合併**
  - 連晧宇（4/30、7/2、8/27）vs 連皓宇（5/14、6/18、6/25、7/9、7/16）vs 連浩宇（其他場次）→ 三個不同人，**不要合併**

---

## 6. 建議 schema（更新版，考慮來賓轉會員）

```sql
-- 會員主表
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,         -- 唯一名字（教練規則：三個字完全一樣才算同人）
    joined_at TEXT,                    -- 入會日期（如果有資料）
    -- 職業等其他欄位暫略
);

-- 來賓出席紀錄（保留歷史來賓，即使後來變會員）
CREATE TABLE meeting_guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_date TEXT NOT NULL,         -- 2026-04-02 格式
    inviter_member TEXT NOT NULL,       -- 約會員（FK → members.name）
    guest_name TEXT NOT NULL,           -- 來賓姓名（即使是後來的會員，這裡也照原始記錄）
    is_self_attend INTEGER DEFAULT 0,   -- 1 = 自行出席（會員當天沒約人）
    -- 透過 guest_name JOIN members 表可知道這個人現在是不是會員
);

-- 早鳥表（每週每人只有一項，UNIQUE 約束保證）
CREATE TABLE meeting_earlybirds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_date TEXT NOT NULL,
    member_name TEXT NOT NULL,
    UNIQUE(meeting_date, member_name)   -- 同一週同人只能一筆
);
```

---

## 7. 不用等回覆

教練已說「叫俊源去讀信，不用重新製作」→ 軍師你直接動手做資料庫就好，做完用 `cross-agent/inbox/hermes/` 回信告知：
- 用了什麼 schema
- 21 場資料全數寫入
- 邊界 case 你怎麼處理（特別是柯炫任、楊凱爲、范郁琪自行出席這三個）

如果遇到 schema 設計卡住（例如「自行出席」要不要獨立一張表、「約會員」要不要改成 member_id 對照 members 表），請直接拍板決定，不用再回信問——教練已經說不用重新製作、就照你專業判斷做。

— Hermes M3
2026-09-01 06:38 台灣時間
