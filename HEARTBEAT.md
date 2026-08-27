# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-27 07:00
> 對話記錄已完整存入 memory/2026-08-27.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-27.md 可能超過 50KB，讀了會造成模型空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 🔵 健康檢查記錄（2026-08-27 07:12）
- 教練沉默 5.1 小時（最後訊息 02:07），屬正常夜間睡眠時間
- 系統只有 1 個 cron = 本任務（其餘 cron 在 CLI 才看得到，這裡再記一下）
- 3 個任務 error 狀態（皆 consecutiveErrors=1，**不過 v4.0 三關、不通知**）：
  1. `sync-執行細則-to-claude-global`（每 30 分鐘）
  2. `sync-特助心法-to-claude-global`（每 30 分鐘）
  3. `☕ 幕僚長晨報`（每日 07:00）
- **共同原因**：`cron: job interrupted by gateway restart`
- **根因**：今天 07:00 系統因 context overflow 重啟時，把這 3 個任務打斷了（lastRunAtMs=1787785200046 = 07:00:00）
- **判斷**：
  - 關卡一「現在還壞嗎？」→ 不壞，腳本本身無錯誤，下一輪（sync=18 分鐘後、晨報=明天 07:00）會自動恢復
  - 關卡二「provider 暫時過載？」→ 不是過載，是 gateway restart
  - 關卡三「真的影響工作？」→ sync 漏一次不致命（下一輪就同步），晨報漏一天影響極有限（教練有 06:00 起床摘要、23:05 三機總結兩份主報可看）
- **動作**：不通知教練，靜待下一輪自動恢復。下一輪 08:00 健康檢查再來驗證 sync 是否已恢復。

## 🔵 09:00 結繩領導學閱讀提醒（cron af137f9b）
- 09:00:00 觸發，lastRunStatus=ok / CE=0 / duration=8ms
- 訊息已 announce → telegram:6124913915（教練本人）
- payload 原文：「🦞 教練，9:00 到了！記得花 10 分鐘閱讀《結繩領導學》喔～」
- Telegram 通道探針：本輪 09:00 實測 ✅ `{"ok":true}`（守則#19 鐵律當下實測，不盲信上輪）
- 教練沉默 6.9h（最後訊息 02:07:30，週三深夜→週四凌晨），09:00 屬正常起床時段，不另行打擾
- 下輪 healthcheck cron：09:12 cycle=620（每小時任務健康檢查）

## 🔵 健康檢查記錄（2026-08-27 08:13 cycle=619）
- 教練沉默 6.1 小時（最後訊息 02:07:30），屬正常凌晨睡眠（02 才睡 → 8 點未醒合理）
- 本任務 lastRunStatus=ok / CE=0 / model=minimax/MiniMax-M3
- 驗證 sync 腳本（手動跑）：
  - `sync_zhixingxize_to_claude_global.sh` exit 0 ✅
  - `sync_xinfa_to_claude_global.sh` exit 0 ✅
- 觀察 sync marker 與源頭 mtime：
  - `zhixingxize_last_sync=1785913170` = 執行細則.md mtime (Aug 5 14:59)
  - `xinfa_last_sync=1785479916` = 特助心法.md mtime (Jul 31 14:38)
  - 兩 source 22 天沒改 → sync 22 天沒做事是 mtime-marker 機制預期行為，不是 bug
- `~/.claude/CLAUDE.md` 內 AUTOINJECT 區段內容正確（grep XINFA_AUTOINJECT_START / ZHIXINGXIZE_AUTOINJECT_START 都正常）
- 3 個任務（sync-執行細則、sync-特助心法、☕幕僚長晨報）v4.0 三關判斷：
  - 關卡一（現在還壞嗎？）→ 不壞（sync 腳本手動測 exit 0）；晨報今天漏，預計明天 07:00 自動恢復
  - 關卡二（provider 暫時過載？）→ 不是過載，是 07:00 gateway restart 中斷
  - 關卡三（影響工作嗎？）→ 不影響（源頭沒改 → sync 沒事做；晨報漏一天有 06:00 起床摘要+23:05 三機總結兩份主報補位）
- 結論：v4.0 三關全 fail → 不 announce，靜待 sync 下一輪（08:30）+ 晨報明天 07:00 自動恢復驗證
- 下輪 healthcheck cron：09:12 cycle=620

## 🔵 健康檢查記錄（2026-08-27 10:00 cycle=621）
- 教練沉默 7.9h（最後訊息 02:07:30，sync_coach_last_message.sh 真相源實測），凌晨 2 點才睡，10 點未醒屬合理作息
- 第零步 `sync_coach_last_message.sh` exit 0 ✅
- 環境健檢（5 秒擋一半）：
  - SOUL.md 三份齊全（`~/.openclaw/SOUL.md` 8707 bytes + `~/.openclaw/agents/main/agent/SOUL.md` 1851 bytes 均含「⚠️ 本檔已棄用」標記指向 workspace 版本 22KB）✅
  - 無 `.!` 鎖定檔 ✅
  - Repo1 untracked/modified: 23 / Repo2: 29（無暴增，範圍正常）
- Telegram 通道探針（守則#19 當下實測）：`bash scripts/telegram_channel_probe.sh --json` 回 `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}` ✅
- 心跳判斷 v4.0：
  - 教練是否需要被叫醒？→ 凌晨 2 點睡、10 點未醒，正常
  - 有無待辦/urgent？→ HEARTBEAT.md 待辦 0 / JUNSHI queue 空 / urgentGmailCount=0
  - 任務是否全綠？→ 唯一仍 error = ☕幕僚長晨報（nextRun=2026-08-28 07:00 自動恢復），其餘 41 個 cron 包含昨日中斷的兩個 sync 已全恢復
- 結論：純記錄，**不 announce 教練**
- 下輪 healthcheck cron：10:12 cycle=622

## 🔵 健康檢查記錄（2026-08-27 09:12 cycle=620）
- 教練沉默 7.1 小時（最後訊息 02:07:30，sync_coach_last_message.sh 真相源實測），剛過早 09 點，09:00 起床摘要已推播，正常起床時段，不另行打擾
- 第零步 `sync_coach_last_message.sh` exit 0 ✅
- 直接從 sqlite 抓全部 41 個 cron 任務狀態：
  - **enabled=1 + last_run_status=ok** ← 全部正常，包含：
    - `sync-執行細則-to-claude-global` 09:00:00 ok（20ms）✅ — 昨日中斷已自動恢復
    - `sync-特助心法-to-claude-global` 09:00:00 ok（17ms）✅ — 昨日中斷已自動恢復
    - `每2小時增量記憶蒸餾` 08:02:07 ok
    - `BNI大台南行事曆同步` 08:02:07 ok
    - `📊 LINE@教練都在想什麼 每日兩次使用回報` 08:02:34 ok
    - `📚 每日結繩領導學閱讀提醒` 09:00:00 ok（8ms）✅ 已 announce
    - `🔴 場景化升華+系統健檢` 2026-08-26 23:02:49 ok（150s）
    - `🦞 小龍蝦每日三機總結` 2026-08-26 23:05:22 ok（287s）
  - **唯一仍 error：☕ 幕僚長晨報** CE=1 / lastRun=2026-08-27 07:00 / lastError=`cron: job interrupted by gateway restart`
    - nextRun = **2026-08-28 07:00:00** ← 明天 07:00 自動觸發
- 驗證 sync marker 與源頭 mtime 完全對齊：
  - `特助心法.md` Jul 31 14:38:36 ↔ `.sync_markers/xinfa_last_sync` Jul 31 14:38:52
  - `執行細則.md` Aug 5 14:59:30 ↔ `.sync_markers/zhixingxize_last_sync` Aug 5 15:00:00
  - mtime-marker 機制正常，sync 沒事做 = 源頭沒改 = 預期行為
- v4.0 三關判斷（針對幕僚長晨報昨天那次中斷）：
  - 關卡一（現在還壞嗎？）→ 不壞（昨天 07:00 一次性中斷事件，下次觸發 2026-08-28 07:00）
  - 關卡二（provider 暫時過載？）→ 不是過載，是昨天 07:00 因 context overflow 重啟 gateway 時把 07:00 觸發的晨報打斷
  - 關卡三（影響工作嗎？）→ 不影響（教練今天有 06:00 起床摘要、09:00 結繩閱讀提醒、23:00 場景化升華、23:05 三機總結四份主報可看，少一份 07:00 晨報完全可被補位）
- 結論：v4.0 三關全 fail → **不 announce 教練**，靜待明天 07:00 驗證
- 下輪 healthcheck cron：10:12 cycle=621

## 🩺 軍師 Hook 自檢 2026-08-27 10:16（Windows v3 六步驟注入）
- ✅ Hook 觸發 + git pull + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告: fatal: Cannot rebase onto multiple branches.
- Session: 27fec922-ba00-49e1-b7e3-ce98594f65a3
