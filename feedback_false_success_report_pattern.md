---
name: 失敗卻假回報是反覆型錯誤指標
description: 腳本/工具忽略外部命令的 exit code 或 stderr，明明失敗卻寫「✅ 成功」是反覆型 bug 模式；遇到時必須抓 rc/stderr、加去重、跨 N 次失敗主動推播
type: feedback
originSessionId: ee38bf45-c771-4259-b93d-b6cd7db9f55b
---
腳本不檢查外部命令（osascript / curl / ssh / git push 等）的 exit code 或 stderr，失敗時仍寫「✅ 已完成」訊息——這是反覆型錯誤指標，必須當下立刻修，不能繞過。

**Why:** 2026-05-16 修 `~/.openclaw/scripts/terminal-watchdog.sh` 的真實案例。腳本每 30 分鐘呼叫 osascript 送 Enter 喚醒卡住的 claude，但 macOS 輔助使用權限沒給，osascript 連續失敗 5 次都回傳 1002 錯誤；腳本不抓 stderr 直接寫「✅ 已送出繼續指令」，整整兩小時靜默失敗沒人發現。違反 CORE_RULES R07（防幻覺）和 R13（交付前自測）。

**How to apply:** 看到/寫到「執行外部命令 → 寫 log」這個 pattern 時必檢三件事：
1. **抓 rc 和 stderr**：`ERR=$(cmd 2>&1 >/dev/null); RC=$?`，分別判斷
2. **失敗訊息去重**：用 `/tmp/<name>.state` 存 last_log_ts + last_reason，同訊息 24h 只寫一次，避免 log 灌爆把真問題埋掉
3. **連續失敗推播**：累計 ≥3 次寫進 workspace/HEARTBEAT.md（也要 24h 去重），讓小龍蝦下次心跳主動通知教練處理；成功時把 fail_count 歸零

任何「靜默重試」的 daemon/cron 腳本都套這套；這比事後查 log 抓 bug 省很多血。
