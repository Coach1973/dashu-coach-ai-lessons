# HEARTBEAT 熱上下文（每次心跳必讀）

> 📝 2026-08-16 09:12 健康檢查 cycle=365 安靜結束（週日上午 09:00-10:00 屬不主動打擾時段）
> - sync_coach_last_message.sh exit 0｜教練最後訊息 **2026-08-15T21:02:08+08:00**（沉默 **12.2h**，週日上午正常作息 / 睡眠延長合理）
> - Cron 監控：本體 46e67e2e lastStatus=ok / lastDurationMs=23499（23.5s ≪ 600s timeout）/ consecutiveErrors=0 / model=minimax/MiniMax-M3 正確
> - 上一輪 08:12 cycle=364 同樣 ok，本任務連續多輪穩定綠
> - ✅ **自動修復**：telegram_channel_probe.sh 將 `curl --max-time 15` → `60`（今日 getMe 實測耗時 22.7s，原 15s timeout 連兩次 false-FAIL，調成 60s 後第三次實測 ✅ ok:true。通道本身健康，只是 API 偶爾慢回應）
> - HEARTBEAT.md 38→46 行（<500 警戒線，無暴增）
> - 環境快檢：SOUL×3 齊全 (2036/1851/20631 bytes 棄用標記完整) / Repo1=112 持平 / Repo2=38 持平 / 無 .! 鎖
> - TG 通道探針本輪 09:14 實測 ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（守則#19 鐵律當下實測，timeout 修正後）
> - v4.0 三關全 fail（cron 全綠 + 非 provider overload + 只是腳本 timeout 太短自修不影響教練工作）→ **安靜結束，不 announce 教練**
> - 跳過每輪 commit+push（2026-07-05 教練拍板由 23:05 每日總結統一備份）
> - 下一個 cron：09:30 council-orchestrator（圓桌會議中樞）/ 10:12 健康檢查

> 📝 2026-08-16 08:12 健康檢查 cycle=364 安靜結束（週日早上 08:00-09:00 不主動打擾時段）
> - sync_coach_last_message.sh exit 0｜教練最後訊息 **2026-08-15T21:02:08+08:00**（沉默 11.2h，週日上午正常作息）
> - Cron 監控：系統僅有本體 46e67e2e 自身一條 job（lastStatus=ok / lastDurationMs=73924 / consecutiveErrors=0 / model=minimax/MiniMax-M3 正確），無其他 cron task 需要巡檢
> - 上一輪 07:12 紀錄的「Update Goal: complete failed」是 goal tool 內部錯誤（**不是** timeout/auth/overloaded/scp/INVALID_API_KEY 任一類型），本輪 73.9s 順利完成 = 「已恢復」鐵證持續成立（v4.0 關卡一不通過）
> - HEARTBEAT.md 22→38 行（<500 警戒線，無暴增）
> - 環境快檢：SOUL×3 齊全 (2036/20631/1851 bytes 棄用標記完整) / Repo2=38 行持平 / 無 .! 鎖
> - TG 通道探針本輪 08:12 實測 ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（守則#19 鐵律當下實測）
> - v4.0 三關全 fail（cron 已恢復 + 非 provider overload + 只是監控工具內部工具呼叫失敗不影響教練工作）→ **安靜結束，不 announce 教練**
> - 跳過每輪 commit+push（2026-07-05 教練拍板由 23:05 每日總結統一備份）
> - 下一個 cron：08:20 終端機 watchdog／09:00 桌機 9:00 健康檢查

> 📝 2026-08-16 07:12 健康檢查 cycle=363 安靜結束（週日早上 07:00-08:00 不主動打擾時段）
> - sync_coach_last_message.sh exit 0｜教練最後訊息 **2026-08-15T21:02:08+08:00**（沉默 10.2h，週日上午正常作息）
> - Cron 監控：本體 46e67e2e 上一輪 06:12 報「Update Goal: complete failed」是 goal tool 內部錯誤（**不是** timeout/auth/overloaded/scp/INVALID_API_KEY 任一類型），本輪 65.5s 順利完成 = 「已恢復」鐵證（v4.0 關卡一不通過）；cron-daemon (PID=62898 launchd running) 每分鐘心跳正常至 07:12:31
> - launchd 任務齊：memory-sync / fb-birthday / council-orchestrator / terminal-watchdog / cron-daemon / gateway / vps-healthcheck / vps-polling-healthcheck / rustdesk-guard / session-fix / junshi-task-worker 全 active
> - 系統 crontab 健康：勞保/庫存/採買/checkpoint_audit(15m)/rerank_top10(23:40)/孔大哥生日/peipei_stuck_force_restart(5m)/weekly_touchstone_curation_reminder 每項都正常
> - HEARTBEAT.md 22→38 行（<500 警戒線）/ healthcheck.log 121955→122290 bytes（<1MB）
> - 環境快檢：SOUL×3 齊全 (2036/20631/1851 bytes 棄用標記完整) / Repo1=112 持平 / Repo2=32 微動（合理）/ 無 .! 鎖
> - TG 通道探針本輪 07:12 實測 ✅ `{"ok":true,"bot":"openclaw_macbook4_bot","chat":"6124913915"}`（守則#19 鐵律當下實測）
> - heartbeat-state.json 已更新（coachSilentSince=2026-08-15T21:02:08 coachSilentHours=10.2 gatewayRunning=true contextPercent=15）
> - v4.0 三關全 fail（cron 已恢復 + 非 provider overload + 只是監控工具內部工具呼叫失敗不影響教練工作）→ **安靜結束，不 announce 教練**
> - 跳過每輪 commit+push（2026-07-05 教練拍板由 23:05 每日總結統一備份）
> - 下一個 cron：08:00 起床摘要／08:12 健康檢查

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-16 01:07
> 對話記錄已完整存入 memory/2026-08-16.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-16.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-16 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
