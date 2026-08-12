---
name: reference_mac_hook_scheduler_architecture_2026-08-12
description: Mac端hook與排程的真實架構（Stop檢查已合併成單一總管、時間注入已合併、系統crontab並未被daemon全部接管），改任何hook或排程前先看這份
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6bf670cc-d91d-434c-8604-176dc6a9794a
  modified: 2026-08-12T12:01:30.096Z
---

2026-08-12 教練要求全面體檢後，Mac 端的 hook 與排程架構已經改變，**動手改任何 hook 或排程前先看這份，不要照舊印象操作**。

## 🔴 settings.json 何時生效（2026-08-12 同場對話實測更正）

改完 `~/.claude/settings.json` **不需要開新對話框**——同一場對話內，下一次 UserPromptSubmit
或 Stop 事件觸發時就會讀到新設定並立刻生效。實測證據：合併 Stop hook 進
`stop_rules_master.sh` 後，同一場對話教練下一句話就被新腳本正確攔下（時間鎖判斷邏輯與
原版一致），不是要等下一場全新 session 才生效。修好 hook 後想驗證，直接在同一場對話裡
講一句會觸發的話測試即可，不用叫教練特地開新視窗。

## Claude Code hook（`~/.claude/settings.json`，本機專屬不進 git）

- **Stop 事件只剩 3 支**：`stop_rules_master.sh`（總管）+ `session_end_auto_push.sh` + `session_end_distill_push.sh`。
  原本 12 支、其中 10 支各自重讀同一份 transcript，已合併進總管一次讀完。
  10 支原檔**沒有刪除**，還在 `workspace/scripts/`，只是不再註冊——要回退把它們填回 settings.json 即可。
  要新增一條 Stop 檢查規則，**改 `stop_rules_master.py` 裡的區塊（A~J）**，不要再新增獨立腳本，否則又會回到重複讀檔的老路。
- **UserPromptSubmit 第一支是 `inject_time_context.sh`**（合併了舊的 `inject_taiwan_time.sh` + `session_time_context.sh`，兩支原檔同樣保留未刪）。
  時間鐵律全文改成「每場 session 只講一次」，marker 在 `/tmp/time_rule_injected_<session_id>`。
- 驗證工具：`scripts/test_stop_rules_master.sh`，11 種情境把合併版跟原版逐一比對擋/不擋是否一致。**改過總管一定要跑這支再上**。

## 排程系統：Mac 上同時有三套，不是一套

過去接力棒寫「已從系統 crontab 接管」，實測**只接管了部分**，三套都還活著：

1. **openclaw cron**（`openclaw cron list`）——23 個任務（2026-08-12 從 32 個整併後）
2. **LaunchAgent**（`~/Library/LaunchAgents/ai.openclaw.*.plist`）——含 gateway、cron-daemon、vps-polling-healthcheck 等
3. **系統 crontab**（`crontab -l`）——8 條仍在跑，含 `checkpoint_audit.sh`（每15分）、`peipei_stuck_force_restart.sh`（每5分）、`rerank_top10.py`（每日23:40）

**查「某個自動化到底是誰在跑」時，三個地方都要查**，只查其中一個會得到錯誤結論。
2026-08-12 就是靠三邊比對才抓到 `vps_polling_healthcheck.sh` 被 LaunchAgent 跟 cron-daemon 各跑一次（已修）。

## cron-daemon 內的排程規則（`scripts/openclaw_cron_daemon.sh`）

每分鐘醒來一次，依分鐘數決定做什麼。2026-08-12 改動：
- 終端機對話**複製備份**維持每 15 分鐘（資料安全不打折）
- **commit 上雲**改成每小時整點才做（原本每 15 分鐘，活躍日產生 79 筆 auto commit 淹沒人工紀錄）
- 改這支腳本後**必須** `launchctl kickstart -k gui/$(id -u)/ai.openclaw.cron-daemon`，否則舊的 while 迴圈還在跑舊邏輯

相關：[[project_cross_machine_hook_sync_todo_2026-08-08]]（Windows/ACER 端對應 hook 尚未套用這次合併）
