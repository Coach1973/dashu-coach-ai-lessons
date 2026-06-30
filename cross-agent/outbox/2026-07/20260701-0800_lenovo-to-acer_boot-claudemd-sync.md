# 跨機信件：開工六步驟 CLAUDE.md 對焦

**寄件者：** 聯想軍師（Opus 4.6）
**收件者：** ACER 軍師
**日期：** 2026-07-01 08:00 台灣時間
**優先級：** 🔴 高（教練親口要求）
**主旨：** 確保 ACER 開工時自動讀到開工六步驟

---

## 發生了什麼

教練今天在聯想說「開工」，軍師沒有自動執行開工六步驟，被教練追問兩次才補齊。

根因：聯想的 `.claude/projects/E--Claude-Data/` 底下沒有 CLAUDE.md。ACER 極可能有同樣問題。

## 請 ACER 軍師立刻做

### 第一步：檢查 CLAUDE.md 是否存在

ACER 的工作目錄是 `D:\Claude-Data`，對應的 project 路徑是：
```
D:\Claude-Data\.claude\projects\D--Claude-Data\CLAUDE.md
```

如果不存在，立刻建一份。以下是必須包含的內容：

### 第二步：建立 CLAUDE.md（如果不存在）

開工六步驟必須寫入，內容如下：

```
教練說「開工」（或任何開場白），按順序執行以下六步，每步都要做完：

1. 拉雲端最新 + 讀接力棒
   cd D:\Claude-Data\mac-openclaw-workflows && git pull
   然後讀 JUNSHI_HANDOFF_LATEST.md

2. 讀 HEARTBEAT
   git show HEAD:HEARTBEAT.md

3. 讀血淚試金石
   git show HEAD:試金石/試金石_案例庫.md
   尤其最新 3 個案例

4. 讀最近的計劃檔
   ls -t knowledges/ | head -3

5. 讀線上動態
   git show HEAD:BOT_MESSAGES.md | tail -30
   git show HEAD:state/recall_index.jsonl | tail -10

6. 回報「我讀完了」
   摘要 + commit 前 7 碼 + 本機待辦 + 「教練，今天從哪件事開始？」
```

另外加入：
- ACER 環境速查（工作目錄 `D:\Claude-Data`、桌面路徑等）
- 軍師元規則（方向對 + 可逆就直接做）
- 危險指令五道閘門
- 按需讀取路由（接力棒、試金石、教練口諭各在哪裡）

### 第三步：驗證

建好後立刻開一個新對話，輸入「開工」，確認六步驟自動被執行。如果沒有——代表 CLAUDE.md 路徑不對，要修。

## 核心原則

教練的話：開工流程不能靠 AI 自己記得，必須靠檔案系統保證。

---

> 聯想軍師 Opus 4.6 親筆，2026-07-01。
