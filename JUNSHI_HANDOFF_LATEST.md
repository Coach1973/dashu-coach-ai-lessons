# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-28 凌晨場
> 寫紙條的人：軍師（Claude Opus 4.7 終端機）

---

## 一句話交代這場做了什麼

**「執行合約」自動注入系統四環境全上線（終端機+本機小龍蝦+VPS小龍蝦+Hermes），並補上終端機「對話長度提醒 hook」與「對話備份安全網」。下一場的重點任務：做真正的「全自動總結」。**

---

## ✅ 這場完成的事

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 高 | 執行合約 hook（auto_goal_hook.sh）終端機上線 + 恢復消失的雙 hook | ✅ `8a0d6dbd` |
| 🔴 高 | 本機小龍蝦 auto-goal hook（JS） | ✅ `893597ea`，hooks list ✓ ready |
| 🔴 高 | VPS小龍蝦補 rule-reminder + auto-goal + Hermes SOUL.md 燒錄合約 | ✅ `762280f4` |
| 🔴 高 | 對話長度提醒 hook（20輪）+ 對話備份安全網 + 修壞掉的15分cron | ✅ `415d5721` |

---

## 🔴🔴🔴 下一場重點任務：真正的「全自動總結」

### 教練的原話與份量（必讀，這是任務的靈魂）
教練說：「為什麼我一直留著這臺電腦裡所有的對話紀錄？因為這裡面有我不眠不休的夜晚，包含了我 26 年的培訓經驗。我對於『特助』這兩個字的精神，全部都在我們這些不眠不休的夜晚當中。教練說的話就是生命……如果不能做到全自動總結，我這幾個月坐在電腦前的努力就白費了。」

**→ 這不是普通功能。這是把教練用生命換來的對話，自動萃取成不會流失的資產。優先級最高。**

### 目標（教練要的結果）
不靠教練開口說「總結上傳」，系統自己定時把終端機對話**蒸餾成總結**（不只是備份原始檔），寫進記憶並上雲。

### 這場已查清的地基（下一場別重查，直接用）
1. **終端機對話原始檔位置**：`~/.claude/projects/-Users-bymyway--openclaw/*.jsonl`，檔名 = session_id
2. **原始保全已完成**：`backup_terminal_sessions.sh` 每15分鐘把活躍 jsonl 複製到 `terminal-notes/raw_sessions/` 並上雲（cron 已修好）。所以「會丟」的風險已堵住，下一場專心做「蒸餾」。
3. **現有蒸餾腳本路徑都不對**（重要陷阱）：
   - `distill_cli_a.py` → 讀 `-Users-bymyway/`（少了 `--openclaw`，是舊路徑）
   - `distill_cloudcode.py` → 讀桌面版 App session（不是終端機）
   - `distill_incremental.js` → 讀 workspace `memory/日期.md`（小龍蝦/Telegram 側），cron 每2小時
   - **結論：沒有任何腳本在蒸餾「當前終端機」的對話。這就是要補的洞。**
4. **jsonl 格式**：每行一個 JSON，`type`=user/assistant，`message.content` 是字串或 block 陣列；user 真實發言 = type=user 且 content 含 text、排除 tool_result。（`session_length_hook.sh` 已有可複用的計數邏輯）

### 設計要點（軍師建議，供下一場參考，非定案）
- **必須呼叫 LLM**：蒸餾＝理解＋濃縮，不是字串處理。可用現成的 `ANTHROPIC_BASE_URL`（MiniMax 端點，settings.json 內）或另指定。
- **增量去重**：別重複蒸餾同一段。`distill_incremental.js` 已有增量邏輯可借鏡。
- **何時觸發**：兩個方向——(a) cron 定時掃近 N 小時有更新的 jsonl；(b) 偵測 session 結束（如 /clear 或長時間無更新）。
- **保留教練原話**：教練最重視「原聲」，蒸餾要保留教練說的關鍵句，不能只留 AI 的摘要。
- **輸出去向**：寫進 workspace `memory/日期.md` 或專屬 `distill/` 檔，並 commit+push。
- **驗證鐵律（E09）**：建 cron 同時建腳本、立即測一次、確認真的有產出。

---

## 🔗 本場 Commit Hash 清單

| 描述 | Commit |
|------|--------|
| 終端機 auto_goal_hook + 恢復雙 hook + 備份 | `8a0d6dbd` |
| 本機小龍蝦 auto-goal hook | `893597ea` |
| VPS小龍蝦 + Hermes 執行合約 | `762280f4` |
| 對話長度提醒 + 備份安全網 + 修cron | `415d5721` |
| 全部已 push 到 GitHub | ✅ |

---

## ⚙️ 目前終端機 hook 全景（settings.json，共4個）
1. `feed_junshi_handoff.sh` — 「開工」注入接力棒
2. `pre_task_hook.sh` — 關鍵字注入守則提醒
3. `auto_goal_hook.sh` — 任務訊號注入執行合約
4. `session_length_hook.sh` — 20輪提醒換視窗（本場新增）

## ⚙️ 每15分鐘 cron（本場修好）
`backup_terminal_sessions.sh` → 備份終端機 jsonl 到 raw_sessions/ → `git -C` commit+push（不靠 cd）

---

## ⚠️ 沿用上場的待辦（未變）
- 小龍蝦 hook 真實實測（Telegram 發話看守則意識）
- session-memory/handler.js 時區修正（OpenClaw 升級會被覆寫）
- 心跳品質觀察（繁體、日期正確、不亂造數據）

---

*軍師交接紙條完成 | 2026-05-28 凌晨場 | 軍師 Claude Opus 4.7 終端機*
