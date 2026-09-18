---
name: reference-cron-job-disappear-root-cause-sop-2026-09-18
description: 教cron job從active store消失時的根因調查SOP（從state失敗記錄/git log/SQLite磁碟備份三路併查）
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5876ed8b-e8aa-57aa-a324-b2e2e2d54d6f
  modified: 2026-09-18T08:26:38.708Z
---

# cron job 從 active store 消失的根因調查 SOP

2026-09-18 教練問「幕僚長晨報 cron（b73845c9）消失了，是怎麼不見的？」，花了一場對話查出根因，這套調查順序建議未來直接套用。

**Why：** cron job 從 active store 消失的原因可能是 ①gateway 重啟時磁碟讀不到 ②doctor --fix 標準化時漏掉 ③人工 openclaw cron rm ④整個 cron store 被某個動作 reset。不同原因對應不同處置（rebuild vs 找 git 救 vs 確認教練有意刪除）。

**How to apply：三路併查法**

### 1. 看 minimax_overload_retry.json / 同類 state retry 檔
- 路徑：`state/minimax_overload_retry.json`
- 找 `cron:<job-id>:failure` 區塊的 `lastTs` — 那個時間點之後沒有新紀錄，就是 cron 從 active store 消失的時間下限
- 範例：本場查得 b73845c9 最後失敗 lastTs = `2026-09-08T22:03:10.709Z`，9/8 22:01 之後消失

### 2. 看磁碟備份（SQLite / .bak / .db）
- 路徑：`state/openclaw_cron.db` / `state/cron.db` / `state/crontab.bak*`
- `ls -la` 看檔案大小跟 mtime — 0 bytes 從某天起 = 磁碟根本沒記錄，active cron 在 gateway 記憶體，無法靠磁碟救
- 範例：本場 `state/openclaw_cron.db` 從 Aug 20 起就是 0 bytes

### 3. 看 git log 找同期 commit 線索
- `git log --all --since=<lastTs日> --until=<今天> --grep="cron\|doctor --fix\|<job-id 前8碼>"` 找可疑 commit
- 特別注意 commit message 寫「doctor --fix」「cron store 標準化」「格式標準化」這類字眼 — `doctor --fix` 是已知會動 cron store 的危險操作（試金石案例73/74已記錄過副作用）
- 範例：本場 9/16 commit `054148ab2` message 明確寫「`openclaw.json`變更含`doctor --fix`格式標準化(cron store等)」，且同時清空 TOOLS.md，強烈暗示是這次

### 結論分三類
- **磁碟有備份 + git 有 commit** → 可重建（拿 commit 裡的 cron job definition 重灌）
- **磁碟 0 bytes + git 沒明確 cron 改動** → 多半是 `doctor --fix` 副作用，無法精準反推刪除 commit，需教練裁示是否重建
- **人工 `openclaw cron rm`** → 看 git log 是否有對應 commit message，或 grep openclaw 操作歷史

### 不要做的事
- 不要直接重建 — 教練可能要的是「不要再建」（因為 b73845c9 對應的「幕僚長晨報」可能已被新流程取代）
- 不要在 handoff 寫「待查明」結案 — 上面三路查下來即使沒 100% 確定 commit 時間點，也能給出「合理推測 + 後續動作選項」
- 不要把「找不到磁碟備份」當作「系統 bug」回報 — 0 bytes 是 Aug 20 起的事實，期間系統可能在某次 reset 後才進 active store

### 已驗證：本場結論
b73845c9 + 06:00 morning_digest 都消失，根因強烈指向 `doctor --fix`（commit 054148ab2）但無法精準反推時間點，需教練裁示是否重建。
