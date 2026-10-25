---
name: reference-openclaw-compaction-timeout-infinite-retry-root-fix-2026-10-25
description: 小龍蝦分身（巴哈等）每8分鐘重試同一則訊息、整天不回話的根因與根治（midTurnPrecheck、群組每天4點重開、卡死看門員）；全部分身共用同一個 gateway 所以一次全套用
metadata:
  node_type: memory
  type: reference
  originSessionId: 3ef1508f-b970-4e6f-8cc6-f68f8c9e8255
  modified: 2026-10-25T08:11:29.690Z
---

**症狀**：某分身不回話，Telegram 每 8 分鐘出現同一句；日誌 `/tmp/openclaw/openclaw-今天.log` 有 `stalled for event N ... handler-timeout`、`compaction-diag ... outcome=failed reason=timeout durationMs≈300000`、`cause=skipped:reply_operation_aborted`。

**根因（2026-10-25 查證，openclaw 2026.9.4 原始碼＋文件）**：
1. `agents.defaults.compaction.midTurnPrecheck` 預設關 → 一則訊息觸發的長工作（10/25 04:08「正常了吧」後巴哈自己跑 245 個工具步驟）中途完全不整理，對話撐到 83 萬 token（上限 20.48 萬的 4 倍）。
2. 太大的對話整理（compaction）每次都超過 Telegram 處理上限 300 秒（`adoptionStallTimeoutMs` 寫死 3e5）→ 被中斷、什麼都沒存。
3. 內建重試（`ingress-retry-policy`）要「失敗 8 次 **且** 滿 24 小時」才放棄（寫死，設定檔改不了）→ 每 8 分鐘重試一整天，每次都燒 MiniMax（很可能就是案例133額度燒光的同一機制）。
4. `session.reset` 預設 none，群組對話只靠整理控制長度；整理一壞就無上限。
另：`openclaw sessions archive` 只是原地封存、身份與內容不變，**不會變短**；真的重開要 `openclaw sessions delete <key> --agent <id> --yes`（原紀錄自動封存成 `agents/<id>/sessions/*.deleted.*.zst`）。

**根治（已上線）**：openclaw.json 開 `compaction.midTurnPrecheck.enabled=true`、`session.resetByType.group={mode:daily, atHour:4}`（外層 repo 8f90e9b5f）；卡死看門員 `workspace/scripts/openclaw_stall_watchdog.py`＋launchd `com.coach.openclaw-stall-watchdog`（跟著日誌，同一則訊息第 2 次逾時就 delete 該聊天室對話並 Telegram 通知教練；紀錄 `state/openclaw_stall_watchdog.log`），已接進每日點名（workspace 4e9e74e5c）。8 個分身（main、kong、peipei、yijing、yang、rongshuxia、bni_tainan、jiaolian_thoughts）共用同一個 gateway，defaults 一改全套用。備份在 `workspace/state/backup_20261025_compaction_loop_fix/`。

**How to apply**：分身不回話先看日誌有沒有 handler-timeout；看門員應已自動處理，看 `state/openclaw_stall_watchdog.log`。看門員本身沒真實觸發過（只做過假日誌行自測），第一次真觸發時確認有沒有通知到教練。

相關：[[reference-peipei-group-context-overflow-blocks-main-lane]]、[[feedback-bot-instructions-must-block-old-path-and-measure-tokens-2026-10-25]]

**10/25 晚第二輪（18:00～18:10）**：巴哈對話不大（6.8 萬）也卡——是被背景工作佔住：內建「自動技能整理」(skills.workshop.autonomous 預設 auto) 會自己開工作、用 sessions_send 叫頂級特助，頂級特助再回傳巴哈，群組真人訊息排在後面。已設 `skills.workshop.autonomous.mode=off`（外層 repo ed06e68e0）。看門員 v2（workspace 4c6d25126）：第 1 次逾時 → `openclaw gateway call sessions.abort --params '{"key":…,"agentId":…}'` 中斷背景工作並通知教練它在忙什麼；第 2 次才刪對話。分身判斷改用「收到訊息的機器人 @名稱 → getMe 對帳號 → bindings」，**不可用最近更新排序**（測試時同群組選到 agent:main，差點動錯頂級特助）。手動中斷實測：18:04 中斷後排隊 7 分多的訊息立刻被接手。v2 的自動中斷還沒真實觸發過。
