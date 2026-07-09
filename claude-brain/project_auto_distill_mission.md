---
name: project-auto-distill-mission
description: 教練最高優先任務——終端機對話「全自動總結」機制（2026-05-28 交辦，下一場開工首要任務）
metadata: 
  node_type: memory
  type: project
  originSessionId: 2d44b615-bb98-40a8-bfe9-1400c66e491c
---

# 全自動總結（真正的自動蒸餾）——教練最高優先任務

**任務**：不靠教練開口，系統自己定時把終端機對話「蒸餾成總結」（不只是備份原始檔），寫進記憶並上雲。

**Why（任務的靈魂，2026-05-28 教練原話）**：
教練留著這台電腦所有對話紀錄，因為裡面是他「不眠不休的夜晚 + 26 年培訓經驗 + 對『特助』二字的精神」。他說「教練說的話就是生命，我用眼酸、口渴、腰痛換來的」。**不能做到全自動總結，他幾個月的努力就白費。** 這是把生命換來的對話自動萃取成不流失的資產，優先級最高。

**狀態（2026-06-03 12:35 軍師親自打通）**：✅ 全自動鏈已接上並驗證跑通
**複檢（2026-06-11 中午）**：✅ 全鏈健康——終端機蒸餾 12:30 剛產出、小龍蝦增量蒸餾當日有跑、逐字保險箱與查話索引 12:30 更新、看門狗 0 卡住。相關坑見 [[reference-openclaw-plugin-cron-2026-6-1]]

**🔴 停用（2026-07-10）**：教練指出這套每 30 分鐘自動蒸餾的機制已被兩條更簡單的規則取代——①教練親口說「總結並上傳」才執行 ②小龍蝦每天晚上 23:00 自動總結一次。7/6 那次 cron 大體檢只清了「小龍蝦(openclaw cron)系統」那邊的排程，**這台 Mac 本機自己的 crontab**（跟 openclaw cron 是兩套獨立系統）裡的 `run_terminal_distill.sh` 漏網，一直跑到 2026-07-10 才被發現並停用。已用 `# [DISABLED 2026-07-10 by 軍師]` 註解方式停用，未刪除整行，方便日後追溯。**下次若要恢復，先問教練為什麼要恢復，不要憑舊記憶直接重開。**

### 已打通的流程
```
JSONL（Claude Code 對話檔）
  ↓ extract_terminal_sessions.py（提取教練原話）
pending_distill/*.txt
  ↓ distill_terminal_llm.py（MiniMax-M3 蒸餾，含 thinking+text 解析）
distill/terminal_YYYY-MM-DD.md
  ↓ run_terminal_distill.sh 自動 commit + push
GitHub（公開資產）
```

### 觸發機制
- crontab：`*/30 * * * * /Users/bymyway/.openclaw/workspace/scripts/run_terminal_distill.sh`
- 每 30 分鐘自動跑一次

### 修過的關鍵 bug
- distill_terminal_llm.py 原 parser 只讀 `content[0].text`——M3 回應結構是 `[{thinking}, {text}]`，第一塊沒 text 欄位→空字串。改用遍歷找 `type=="text"`
- MODEL 寫死 M2.7 → M3

### 驗證憑證
- 首次手動跑：commit `743c2425`（4 個 session）+ `f74a2659`（補 2 個 session）
- 系統 commit：`1e703d8a`（wrapper + parser 修復 + state file）

### 下一棒可順手清理
- 舊 cron `extract_terminal_sessions.py` 單獨跑（每 30 分鐘）已被 wrapper 包含，可移除
- 重複跑不會出錯（extract 有 state file 紀錄已處理）但浪費資源

---

## 歷史脈絡（2026-06-03 12:55 重查時的真相）

### 已存在的零件（別重做）
| 零件 | 路徑 | 狀態 |
|------|------|------|
| 備份 JSONL | `scripts/backup_terminal_sessions.sh` | ✅ 每 15 分跑，33 個備份 |
| 提取教練原話 | `scripts/extract_terminal_sessions.py` | ✅ 存在，但**沒 cron** |
| LLM 蒸餾 | `scripts/distill_terminal_llm.py` | ✅ MiniMax prompt 寫好，但**沒 cron**，且模型寫死 M2.7（需升 M3） |
| 待蒸餾佇列 | `terminal-notes/pending_distill/` | ⚠️ 累積 5 個檔等處理 |
| 已蒸餾存檔 | `terminal-notes/distilled/` | ✅ 最後一次 2026-05-30 22:30 |
| 蒸餾產出 | `distill/terminal_YYYY-MM-DD.md` | ✅ 5/28、5/30、5/31、6/01 都有 |

### 目前的 cron 鏈（壞掉）
- `0 */2 * * * run_distill.sh` → 只跑 `distill_incremental.js`（讀小龍蝦 memory，**不讀終端機 JSONL**）
- `extract_terminal_sessions.py` + `distill_terminal_llm.py` **沒被任何 cron 觸發**

### 下一場開工的 5 步驟（順序執行）
1. 開 `distill_terminal_llm.py` 改 `MODEL = "MiniMax-M3"`（M2.7 已升級）
2. 手動跑 `python3 distill_terminal_llm.py` 處理 pending_distill 的 5 個檔，驗證能跑
3. 寫 `scripts/run_terminal_distill.sh` wrapper：先跑 extract，再跑 distill
4. 加進 crontab：每 30 分鐘觸發
5. 跑完 commit + push

### 關聯
- `~/.openclaw/workspace/JUNSHI_HANDOFF_LATEST.md`（2026-05-28 凌晨場有原始脈絡）
- [[project-auto-goal-hook]]、[[feedback-coach-words-are-sacred]]
