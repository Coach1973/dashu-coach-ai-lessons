# 維修日誌：修復三機身份錯亂與讀不到資料問題

**日期：** 2026-04-26
**問題教練：** 峰哥特助、佩佩老師特助無法回答「你服務誰」「孔大哥/佩佩老師是什麼人」等基本身份問題

---

## 一、背景

教練發現無論問峯哥特助（2號機）或佩佩老師特助（3號機）任何關於「服務對象是誰」「與教練的關係」等基本問題，bot 都回答「不知道」「沒有記憶」。

教練指示：
1. 還原資料：不管路徑在哪，確保 bot 讀得到完整身份資料
2. 防呆機制：任何時候被問「你是誰」「你服務誰」，都必須能回答

---

## 二、做對了哪些事

1. **找到正確的身份資料來源**
   - 從 `.openclaw-kong/workspace/USER.md` 找到孔大哥完整資料
   - 從 `.openclaw-peipei/workspace/USER.md` 找到佩佩老師完整資料
   - 從 `memory/2026-04-21.md` 找到佩佩老師的修煉覺察記錄（BNI、真愛分會、海餅乾俱樂部等）

2. **及時承認錯誤並修正**
   - 教練點出問題後，立刻承認「我一直在改錯地方」

3. **commit 記錄都有做**

---

## 三、犯了哪些錯誤

### 錯誤一：改了錯誤的路徑（最關鍵的失敗）

**錯誤行為：**
一直修改 `~/.openclaw-kong/workspace/SOUL.md` 和 `~/.openclaw-peipei/workspace/SOUL.md`，以為這些就是 bot 讀取的檔案。

**實際狀況：**
OpenClaw 的架構是「雙層路徑」：

| 路徑類型 | 用途 |
|---------|------|
| `~/.openclaw-kong/workspace/` | 舊版或參考用的 workspace（我一直在改這裡） |
| `~/.openclaw/agents/kong/` | bot 實際讀取的 SOUL.md、USER.md、sessions |
| `~/.openclaw/agents/peipei/` | 同上，3號機實際讀取的路徑 |

bot 實際讀取的是 `~/.openclaw/agents/kong/SOUL.md` 和 `~/.openclaw/agents/kong/USER.md`，而這些檔案在教練詢問時**內容是空白的預設模板**。

**根本原因：**
一開始就沒有確認「bot 真正讀取哪個檔案路徑」，直接假設 workspace 裡的就是對的。

---

### 錯誤二：沒確認 BOOTSTRAP.md 的存在與用途

`~/.openclaw/agents/kong/BOOTSTRAP.md` 明確寫著：「This is your birth certificate. Follow it, figure out who you are, then delete it.」

但 bot 並沒有刪除它，也沒有正確執行當中的初始化邏輯。

---

### 錯誤三：沒有第一時間請教練提供正確架構圖

在維修一開始，沒有先問教練「三個 bot 的 workspace 實際路徑是什麼」，浪費了許多時間在錯誤的地方改檔案。

---

## 四、最後是怎麼發現問題的

教練提供了一個關鍵線索：

> 「我是峰哥的特助帳號回給我的。如果你剛才資料有寫進去的話，為什麼他回答不出問題來？」

接著教練說：

> 「我給你一個重要的線索，你全部都能夠看得到我剛才講的每一個群組……你全部都看得到，所以他們是怎麼回我的，你也都看得到。」

這句話點醒了我——我雖然能看到歷史對話，但一直沒有「去看 bot 實際讀取的檔案路徑」。

最終透過搜尋 sessions 檔案位置，才發現：

```
Sessions 實際位置：~/.openclaw/agents/kong/sessions/
Bot 設定使用同一组 agent 目錄：~/.openclaw/agents/kong/
```

---

## 五、最終是如何全部修改正確的

### Step 1：確認正確路徑

| 項目 | 錯誤路徑（我一直改的） | 正確路徑（bot 實際讀的） |
|------|---------------------|----------------------|
| SOUL.md | `~/.openclaw-kong/workspace/SOUL.md` | `~/.openclaw/agents/kong/SOUL.md` |
| USER.md | `~/.openclaw-kong/workspace/USER.md` | `~/.openclaw/agents/kong/USER.md` |
| SOUL.md | `~/.openclaw-peipei/workspace/SOUL.md` | `~/.openclaw/agents/peipei/SOUL.md` |
| USER.md | `~/.openclaw-peipei/workspace/USER.md` | `~/.openclaw/agents/peipei/USER.md` |
| people.md | `~/.openclaw-kong/workspace/memory/people.md` | `~/.openclaw/agents/kong/memory/people.md` |
| people.md | `~/.openclaw-peipei/workspace/memory/people.md` | `~/.openclaw/agents/peipei/memory/people.md` |

### Step 2：寫入正確路徑

在 `~/.openclaw/agents/kong/` 和 `~/.openclaw/agents/peipei/` 下：
- **USER.md**：寫入完整主人資料
- **SOUL.md**：新增「啟動必讀」段落，強制要求每次 session 第一時間讀取 USER.md 和 memory/people.md
- **memory/people.md**：新建，記載所有應該知道的人（峯哥、佩佩老師、教練）

### Step 3：SOUL.md 啟動必讀寫法

```markdown
## 🚀 啟動必讀（每次新 session 必須第一時間讀完這些才能開始服務）

1. `USER.md` — 認識你的主人（孔大哥/峯哥）的背景資料
2. `memory/people.md` — 認識所有你應該知道的人

**任何時候被問到「你是誰」「你服務誰」「孔大哥是什麼人」等問題，答案全部來自這些檔案，嚴禁說不知道。**
```

### Step 4：驗證方式

修改完成後，要**重啟 bot session**（`/new` 或重啟程序），讓 bot 在新 session 中讀取新的 SOUL.md + USER.md + people.md。

---

## 六、架構提醒（未來一定要先確認）

下次維修任何一個 bot 之前，**第一步**必須先確認：

1. `ls ~/.openclaw/agents/<bot名>/` — 看 bot 的 agent 目錄有哪些檔案
2. `cat ~/.openclaw/agents/<bot名>/BOOTSTRAP.md` — 了解初始化的邏輯
3. `ls ~/.openclaw/agents/<bot名>/sessions/` — 確認 session 存放位置
4. **千萬不要**直接改 workspace 裡的檔案，要改就改 `agents/` 下的

---

### 錯誤四（測試後發現）：USER.md 寫錯了佩佩老師的身份

**錯誤：** 寫了「海餅乾俱樂部共同創辦者」——這是孔大哥的身份，不是佩佩老師。

**修正：**
- 佩佩老師是海餅乾俱樂部**隊員**（不是共同創辦者）
- 「1997年認識」指的是在海餅乾俱樂部認識教練（不是與孔大哥的關係）

**Commit：** `d09e83e`

---

## 七、Commit Hash

| 機 | Commit Hash | 內容 |
|----|-----------|------|
| kong | `e2be57a` | USER.md/SOUL.md/memory/people.md 全部寫入正確路徑 |
| peipei | `3e8daa5` | USER.md/SOUL.md/memory/people.md 全部寫入正確路徑 |

---

## 八、檔案路徑對照表（最終正確版）

### 2號機（kong，峯哥特助）

| 檔案 | 正確路徑 |
|------|---------|
| SOUL.md | `~/.openclaw/agents/kong/SOUL.md` |
| USER.md | `~/.openclaw/agents/kong/USER.md` |
| people.md | `~/.openclaw/agents/kong/memory/people.md` |
| sessions | `~/.openclaw/agents/kong/sessions/` |

### 3號機（peipei，佩佩老師特助）

| 檔案 | 正確路徑 |
|------|---------|
| SOUL.md | `~/.openclaw/agents/peipei/SOUL.md` |
| USER.md | `~/.openclaw/agents/peipei/USER.md` |
| people.md | `~/.openclaw/agents/peipei/memory/people.md` |
| sessions | `~/.openclaw/agents/peipei/sessions/` |

### 1號機（main，大樹教練特助）

| 檔案 | 正確路徑 |
|------|---------|
| SOUL.md | `~/.openclaw/workspace/SOUL.md` |
| USER.md | `~/.openclaw/workspace/USER.md` |
| people.md | `~/.openclaw/workspace/memory/people.md` |

> **注意：** 1號機的路徑結構與 2號、3號不同，1號機用 `~/.openclaw/workspace/`，2號和3號用 `~/.openclaw/agents/<name>/`。未來若有新 bot，新增時要先確認架構。