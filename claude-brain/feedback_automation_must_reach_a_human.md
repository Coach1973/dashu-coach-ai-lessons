---
name: feedback_automation_must_reach_a_human
description: 檢查自動化時要問「結果有沒有人看到」而不只是「有沒有在跑」——2026-08-25 全系統體檢揪出一整批跑了幾個月但成果倒進沒人開的檔案的自動化
metadata:
  type: feedback
---

2026-08-25 教練要求做賈維斯式全系統體檢，揪出的問題有一個共同形狀：
**自動化「有在跑」不等於「有在發揮作用」**。判斷一支自動化是否健康，要問三層，缺一層就是白做工。

## 三層檢查（往後查任何排程／hook／監控都照這個順序問）

1. **它有在跑嗎？** — 最表面。LaunchAgent 顯示 running、cron 有紀錄，都只證明這一層。
2. **它的判斷邏輯真的有執行嗎？** — `auto-fix-session-lock.sh` 每 2 分鐘跑一次、狀態顯示正常，
   但判斷式寫錯（`grep -c ... || echo 0` 零匹配時會產生 "0\n0" 兩行），**累計噴 549 次錯誤**，
   「額度用盡自動換模型」這道保護從頭到尾沒判斷成功過。這叫靜默失效。
3. **🔴 結果有沒有送到該看的人手上？** — 最常被漏掉的一層。體檢當天抓到一整批：
   - 桌面 `reminder.txt` 堆積 61 行，教練從沒開過（而且排程是「每天」卻寫「今天是最後繳費日」＝每天喊狼來了）
   - `checkpoint_audit.sh` 每 15 分鐘偵測到「資料沒備份」，只寫 `/tmp/*.log`，這道防線從沒真的示警過
   - 試金石策展提醒只寫進 `HEARTBEAT.md`——那是 AI 看的，不是教練看的
   - `distill_watchdog.sh` 的 `openclaw message send` 少了 `--channel`，訊息其實一則都送不出去

## 送通知給教練的正確寫法（本次踩過三次才通）

`openclaw message send` 從 cron／腳本這種外部環境呼叫會失敗兩次：
① 系統同時接 telegram + line，不給 `--channel` 會報 `Channel is required`
② 給了 `--channel` 還是會報 `Telegram bot token missing`（token 在 gateway 進程裡，不在環境變數）

✅ 統一走 `~/.openclaw/workspace/scripts/notify_coach.sh`：從 `openclaw.json` 讀 token 直接打 Telegram API，
支援節流、送出失敗一定寫 log。⚠️ 注意 `~/.openclaw/scripts/notify-coach.sh`（連字號版）是壞的已棄用，
兩者只差一個符號，選錯會靜默失敗——[[試金石案例62]] 近似名稱沒逐字核對的同款坑。

## 通知的門檻要高，不是有事就吵

教練 2026-08-05 親口：「不影響工作就別吵我，浪費我注意力」。
所以 checkpoint_audit 的門檻刻意設成「超過 3 小時沒備份」才通知（正常每小時自動備份，永遠不會觸發），
peipei 自動重啟節流 1 小時、試金石策展節流 7 天。**寧可漏報一次，不要天天狼來了**——
桌面 reminder.txt 就是「每天提醒」最後變成「完全沒人看」的實例。

## 本次自己踩的坑：檢查不能擋，就等於沒有

納管檔案時我「有做金鑰掃描」，也確實掃出 2 個 token，
但掃描跟 commit 寫在同一串指令裡，結果只是印出來、沒有阻斷，token 照樣被 commit + push。
→ 已做成 `scripts/git_secret_guard.sh` 掛進兩個 repo 的 pre-commit，命中直接擋下。
呼應 [[feedback_lock_must_be_hook_not_optin]]：防呆必須是機關，不能是「規矩」。

Related: [[feedback_alert_only_when_actually_broken]]（警報三關判定）、
[[feedback_false_success_report_pattern]]（不抓 rc/stderr 卻寫「成功」）、
[[feedback_event_driven_not_polling_pattern]]（事件驅動優於輪詢）
