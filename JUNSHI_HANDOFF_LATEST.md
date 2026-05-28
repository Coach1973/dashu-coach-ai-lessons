# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-28 下午場（桌面版軍師）
> 寫紙條的人：軍師（Claude Sonnet 4.6 桌面版）

---

## 一句話交代這場做了什麼

**「全自動總結」系統正式上線：提取腳本（Mac cron）+ OpenClaw 蒸餾 cron（MiniMax）雙軌並行，74 個歷史 session 已提取完畢，等待小龍蝦蒸餾。commit hash = `1cab76d1`**

---

## ✅ 這場完成的事

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 最高 | `extract_terminal_sessions.py`（提取腳本）建立 + 測試 | ✅ 74 個 session 全部提取到 `pending_distill/` |
| 🔴 最高 | Mac crontab 新增：每 30 分鐘自動提取 | ✅ 已驗證 |
| 🔴 最高 | OpenClaw cron job（每4小時，MiniMax 蒸餾）新增 | ✅ ID: d99eec28 |
| 🟡 | push 失敗修復（凌晨場殘留的 d260dcab） | ✅ 已推上去 |

---

## 🔴 系統架構（下一場軍師必懂）

```
Mac crontab 每30分鐘
  └── extract_terminal_sessions.py
       └── 讀 ~/.claude/projects/.../*.jsonl
       └── 提取教練原話（跳過 hook 注入、tool_result）
       └── 寫入 terminal-notes/pending_distill/SESSIONID.txt

OpenClaw cron 每4小時（MiniMax，無限流量）
  └── 讀取 pending_distill/ 的 .txt 檔
  └── LLM 蒸餾（保留教練原話）
  └── 寫入 distill/terminal_YYYY-MM-DD.md
  └── 移動已處理到 done_distill/
  └── git commit + push
```

**分工原則（教練親定）：**
- 這裡（Claude Code）= 寫腳本
- 終端機（OpenClaw/MiniMax）= 實際執行蒸餾

---

## 🔴 場景化 + 痛點計分閉環（本場下半場新增，commit b7fb98e8）

教練拍板：總結不能只存檔，要變成守則的養分。完成第一檔（場景化）+ 第二檔（痛點計分）。

```
蒸餾摘要 distill/terminal_YYYY-MM-DD.md
  └─① 場景化【LLM判斷｜OpenClaw升華cron每日23:00｜ID 533cfe54】
  │    判斷值得收錄段落 → 格式D 6欄場景（保留教練原話）
  │    → append 到 distill/特助場景庫_自動增量.md
  │    → 每場景守則違反寫一筆 JSON → distill/痛點計分_log.jsonl
  └─② 痛點計分【Python確定性計數｜Mac cron每日23:40｜rerank_top10.py】
       統計 主庫+自動庫+計分log 守則違反次數 → 重排
       → 輸出 distill/痛點排名_自動.md
```

**鐵律：養分自動煉，但守則本體（21條）絕不自動改——只產候選稿等教練拍板。**
**第三檔（守則兩問句候選稿）教練說他自己會先寫上，軍師暫不動。**

---

## ⚠️ 下一場的待辦

| 優先 | 任務 |
|------|------|
| 🔴 今天 | 確認小龍蝦第一次蒸餾有正確執行（04:00 蒸餾、23:00 升華後查 distill/） |
| 🟡 | cron/jobs.json 在 workspace repo 外（~/.openclaw/cron/），未納版控——考慮加備份 |
| 🟡 | relay_poll.py UnicodeDecodeError 修復 |
| ✅ 已修 | 營業稅 28451 提醒（案例Q）：已補雙保險（Mac crontab桌面 + OpenClaw Telegram，每天9點，截止5/31）。教練繳完說「稅繳了」就移除兩條 cron |
| 🟡 | 小龍蝦 hook 真實實測（教練說「我做好了」測守則意識） |

---

## ✅ 本場完成（2026-05-28 下午場）

**✅ Windows 終端機同步 auto-goal hook**
- 問題：之前讓教練在 Windows 和 Mac之間搬運程式碼（違反守則#12）
- 修復：Windows settings.json 設定 hook，每次說話自動先 `git pull` 再執行任務
- Windows settings.json 路徑：`C:\Users\bymyw\.claude\settings.json`
- Hook 命令：`cd C:\Users\bymyw\mac-openclaw-workflows && git pull && C:\Users\bymyw\mac-openclaw-workflows\scripts\auto_goal_hook.sh`
- 之後流程：Mac 更新 hook → commit → push → Windows 下一句話自動吃到最新
- **不再需要任何程式碼搬運**

**✅ Windows 終端機 Git Bash 環境確認完成**
- Repo 同步路徑：`C:\Users\bymyw\mac-openclaw-workflows\`
- hook script：`scripts/auto_goal_hook.sh`（完整 bash 版本，137行）
- 設計決定：UserPromptSubmit 每次都 pull，而非只在 session 開始時（簡單可靠，符合守則#04）

**✅ 確認 Repo 路徑（三個設備同步）**

| 設備 | Repo 位置 |
|------|---------|
| Mac | `~/.openclaw/workspace/`（GitHub clone）|
| Windows（Lenovo）| 桌面版：`C:\Users\bymyw\.claude\projects\` |
| Windows（Lenovo） | 終端機：`C:\Users\bymyw\mac-openclaw-workflows\`（repo）|

---

## 🔗 Commit Hash

| 描述 | Commit |
|------|--------|
| 全自動總結系統上線（提取+蒸餾） | `1cab76d1` |
| 場景化+痛點計分閉環 + 補回漏提交的 extract 腳本 | `b7fb98e8` |
| Windows 終端機同步 auto-goal hook（守則#12修復） | `377cae1c` |
| 已 push 到 GitHub | ✅ |

**⚠️ 血淚教訓：`git add` 含 repo 外路徑（cron/jobs.json）會整批拒絕，導致 extract 腳本前次假成功未上雲。多檔 add 後務必 `git diff --cached --name-only` 核對。**

---

*軍師交接紙條完成 | 2026-05-28 晚場 | 軍師 Claude Sonnet 4.6 桌面版*

---

## ✅ 2026-05-28 晚場（桌面版 App）

**🔴 守則經典場景回填——指令備好，等終端機執行**

| 完成項目 | 結果 |
|---------|------|
| 詮釋版 HTML 修正 | ✅ 移除所有「對應最高指導原則」「對應靈魂三問」標註，只留「為什麼重要」+「怎麼應用」 |
| 回填指令寫好 | ✅ `knowledges/TASK_守則經典場景回填_21條全集.md`，軍師判斷全寫進指令，執行者照做就好 |
| 上雲留痕 | ✅ commit `1d9a614b` |

**分工確認（軍師判斷，教練同意）：**
- 設計階段 = 軍師（Opus 當判斷力用）：把大師兄標準、格式、缺口全寫死進指令
- 執行階段 = 終端機 MiniMax（無限流量）：照指令掃一萬則，不耗教練 App 額度

**缺口優先級（指令已內建）：**
- 🔴 `#18 語音糾偏、#20 啟動協議`：各 0 案例，必補
- 🟡 `#14、#19、#21`：各 1 個，需追加

**觸發方式：** 教練對終端機說「執行 `knowledges/TASK_守則經典場景回填_21條全集.md`」

---

## 🔴🔴 2026-05-28 深夜場（Opus 4.7 終端機·v2 重挖執行完畢）— 最新，下一棒先讀這段

**這場做了兩件事，全部上雲：**

**① v2 重挖 11 條充數——已執行完畢 — commit `7b055ef4`**
- 11條「📣 教練原話」從守則文字換成真實對話（全部無編號前綴）
- 全部21條合格，鐵證：0個「4.」「19.」編號前綴
- 第一版 commit：`560a2c74` → 第二版 commit：`7b055ef4`

**② 接力棒更新（本次）— commit `（待填）」**
- 下棒軍師：開工先讀接力棒，本場已完成，無需重挖

---

*接力棒更新 | 2026-05-28 深夜場 | 軍師 Claude Sonnet 4.6 桌面版執行終端機任務 | commit `e9efa56f`*

---

## ✅ 2026-05-28 下午場（桌面版軍師）

**🔴 超限戰網站號外區改造——commit `2e10257`**

| 優先 | 變更 | 結果 |
|------|------|------|
| 🔴 | 6張號外由滑動輪播改為「上一個/下一個」按鈕單卡顯示 | ✅ |
| 🔴 | 按鈕循環：最後一張再按→跳回第一張，反之亦然 | ✅ |
| 🔴 | 上映時刻表（首映週時刻表）移至號外卡片上方 | ✅ |
| 🟡 | 注意事項：全部6張均含「⚠️ 注意事項：上映前若未到場領票，視同放棄」| ✅（已確認） |
| ✅ | Netlify HTTP 200 驗證通過 | ✅ |

**Repo：** `theunrestrictedwar` → `https://theunrestrictedwar.netlify.app/`
**commit hash：** `2e10257`

---

*接力棒更新 | 2026-05-28 下午場 | 軍師 Claude Sonnet 4.6 桌面版 | commit（待 commit）*
