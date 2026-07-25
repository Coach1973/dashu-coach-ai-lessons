# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-25 17:37
> 對話記錄已完整存入 memory/2026-07-25.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-25.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-25 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-25 20:55
- ✅ 同步成功
- HANDOFF mtime: 1784984072
- 雲端同步：✅ 已推上雲端（commit 80e8bee93）

## 🩺 軍師 Hook 自檢 2026-07-25 21:00（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 041ebe68-b185-4a9d-8bc0-a08b5e0b56d8

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-25 21:00
- ✅ 同步成功
- HANDOFF mtime: 1784984339
- 雲端同步：✅ 已推上雲端（commit ac542386f）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-26 02:55
- ✅ 同步成功
- HANDOFF mtime: 1785005713
- 雲端同步：✅ 已推上雲端（commit 71ec9f547）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-26 03:00
- ✅ 同步成功
- HANDOFF mtime: 1785005791
- 雲端同步：✅ 已推上雲端（commit 52660b28c）

## 🩺 健康檢查 2026-07-26 03:00（每30分鐘任務健康檢查）
- 掃描 28 個 cron jobs（15 啟用 + 13 disabled）
- 異常數：2（皆為 consecutiveErrors=1，未達3次門檻，屬暫時性）
  - 🦞 每30分鐘任務健康檢查（自身）：reason=overloaded，AI 服務暫時過載
  - 🦞 小龍蝦每日三機總結（每日23:05）：reason=✉️ Message: 1 failed，Telegram 訊息送出失敗（昨日23:05）
- HEARTBEAT.md 待辦 ⬜ 項目檢查：無 ⬜ 項目，無需評估
- 結論：✅ 無需自動修復、無需通知教練，下次定檢 03:30

## 🩺 健康檢查 2026-07-26 03:35（每30分鐘任務健康檢查）
- 掃描 17 個 cron jobs（17 啟用 + 0 disabled）
- 異常數：2（皆未達3次門檻，暫時性，無需自動修復）
  - 🦞 每30分鐘任務健康檢查（自身）：reason=overloaded，AI 服務暫時過載（duration 144.7s ≠ timeout 600s，非逾時）；consecutiveErrors=2，下一次再失敗就會到3次門檻
  - 🦞 小龍蝦每日三機總結（每日23:05）：reason=✉️ Telegram 訊息送出失敗（昨日23:11）；consecutiveErrors=1，下次今晚23:05會自動重試
- HEARTBEAT.md 待辦 ⬜ 項目檢查：無 ⬜ 項目
- 結論：✅ 無需自動修復、無需通知教練；持續觀察自身下次執行是否解除連錯

## 🩺 健康檢查 2026-07-26 04:04（每30分鐘任務健康檢查）
- 系統可見 cron job：1 個（健康檢查本身；先前 17/28 計數可能含已清理/disabled 任務）
- 上一場 04:00 fire ❌（115.998s，`FailoverError: AI service temporarily overloaded`）
- 本場 04:04 ✅ 正常完成（本次任務當下執行）
- **consecutiveErrors: 1**（< 3 次紅線，安穩）
- lastDurationMs 116s ≪ payload.timeoutSeconds 600s → 不是設定問題
- model=`minimax/MiniMax-M3` ✅ 正確，無 INVALID_API_KEY
- 無 timeout 過短、無 scp/ssh VPS、無 CE ≥ 3 → 無需自動修復
- HEARTBEAT.md 待辦 ⬜ 項目：無（grep 計數 0）
- alternating fail/recover 模式 130+ 場次穩定（minimax provider 端常態波動）
- 不 commit/push（遵循 2026-07-05 教練拍板）
- delivery.mode=none，安靜處理不打擾教練（週日凌晨 04:04）
- ⚠️ 警戒：04:30 fire 若再失敗 → CE=2；05:00 fire 又失敗 → CE=3 紅線 → 屆時必須 announce 教練

## 🩺 健康檢查 2026-07-26 06:04（每30分鐘任務健康檢查）
- 掃描 18 個 cron jobs（17 啟用 + 1 disabled 未列出）
- 異常數：4（皆 CE=1，未達3次紅線門檻，皆為 transient 錯誤，無需自動修復）
  - 🦞 健康檢查（自身）：reason=overloaded（duration 81.9s ≪ timeout 600s）
  - ☀️ 每日 06:00 起床摘要：reason=overloaded（duration 90.6s）
  - 每2小時增量記憶蒸餾：reason=overloaded（duration 157.3s，FailoverError）
  - 🦞 小龍蝦每日三機總結（每日23:05）：reason=✉️ Telegram 訊息送出失敗（昨夜23:05）
- 分析：3 個 overloaded 為同一時段 (06:00 fire) 集中爆發，皆為 provider 端 transient 過載，**無法自動修復**（非設定問題），下次自動重試
- model 已是 minimax/MiniMax-M3，無 apiKey 問題
- HEARTBEAT.md 待辦 ⬜ 項目：無
- 06:00 起床摘要失敗 - 但是 delivery.mode=announce → 失敗未通知教練
- 結論：✅ 無需自動修復、無需通知教練，下次定檢 06:30

## 🩺 健康檢查 2026-07-26 06:35（每30分鐘任務健康檢查）
- 掃描 18 個 cron jobs（17 啟用 + 1 disabled）
- 異常數：2（皆未達3次紅線門檻，無需自動修復）
  - 🦞 健康檢查（自身）：reason=overloaded（duration 137.1s ≪ timeout 600s）；consecutiveErrors=2，當前 06:35 fire 正在跑（runningAtMs 1785018905178），若這次成功則 CE 會 reset 為 0
  - 🦞 小龍蝦每日三機總結（每日23:05）：reason=✉️ Telegram 訊息送出失敗（昨夜23:05 duration 144s）；consecutiveErrors=1，下次今晚23:05會自動重試
- 分析：兩者皆為 provider 端 transient 錯誤，非設定問題
  - 自身 overloaded 是 130+ 場次以來的 alternating fail/recover 常態，minimax 端常態波動
  - 每日三機總結的 Telegram 送出失敗是昨夜 service 暫時不通，下次會自動重試
- model 皆是 minimax/MiniMax-M3，無 apiKey 問題
- 無 timeout 過短、無 scp/ssh VPS、無 CE ≥ 3 → 無需自動修復
- HEARTBEAT.md 待辦 ⬜ 項目：無（grep 4 個皆為歷史報告「無 ⬜ 項目」描述，非真實待辦）
- 不 commit/push（遵循 2026-07-05 教練拍板）
- delivery.mode=none，安靜處理不打擾教練（週日清晨 06:35）
- 警戒：自身健康檢查若這次沒跑成功 → CE=3 紅線 → 下一場 07:00 必須 announce 教練

## 🩺 健康檢查 2026-07-26 07:02（每30分鐘任務健康檢查）
- 系統可見 cron job：1 個（健康檢查本身）
- 上一場 07:00 fire ❌（143.7s，`FailoverError: AI service temporarily overloaded`）
- 本場 07:02 正在完成（CE 升到 1，<< 3 紅線，安穩）
- lastDurationMs 143.7s ≪ payload.timeoutSeconds 600s → 不是設定問題
- model=`minimax/MiniMax-M3` ✅ 正確，無 INVALID_API_KEY
- 無 timeout 過短、無 scp/ssh VPS、無 CE ≥ 3 → 無需自動修復
- HEARTBEAT.md 待辦 ⬜ 項目：無（grep 5 個皆為歷史報告「無 ⬜ 項目」描述，非真實待辦）
- 不 commit/push（遵循 2026-07-05 教練拍板）
- delivery.mode=none，安靜處理不打擾教練（週日上午 07:02）
- 06:35 預測的「07:00 失敗 → CE=3 必須 announce」未發生：實際 CE=1（06:35 retry 已成功 reset 過一次，07:00 失敗從 0 升到 1），遠低於紅線
- 警戒：07:30 fire 若再失敗 → CE=2；08:00 fire 又失敗 → CE=3 紅線 → 屆時必須 announce 教練

## 🩺 健康檢查 2026-07-26 07:35（每30分鐘任務健康檢查）
- 掃描 18 個 cron jobs（17 啟用 + 1 disabled）
- 異常數：2（皆未達3次紅線門檻，無需自動修復）
  - 🦞 健康檢查（自身）：reason=overloaded（duration 180.25s ≪ timeout 600s）；consecutiveErrors=2（**接近紅線 3**），本場 07:35 fire 正在跑（runningAtMs 1785022552842），若這次成功則 CE 會 reset 為 0
  - 🦞 小龍蝦每日三機總結（每日23:05）：reason=✉️ Telegram 訊息送出失敗（昨夜23:05）；consecutiveErrors=1，今晚23:05會自動重試
- 分析：兩者皆為 provider 端 transient 錯誤，非設定問題
  - 自身 overloaded 是 130+ 場次以來的 alternating fail/recover 常態，minimax 端常態波動
- 自身 model 已是 minimax/MiniMax-M3，無 apiKey 問題
- 無 timeout 過短、無 scp/ssh VPS
- HEARTBEAT.md 待辦 ⬜ 項目：無（grep 6 個皆為歷史報告「無 ⬜ 項目」描述，非真實待辦）
- 不 commit/push（遵循 2026-07-05 教練拍板）
- delivery.mode=none，安靜處理不打擾教練（週日上午 07:35）
- 警戒：自身健康檢查若這次沒跑成功 → CE=3 紅線 → 下一場 08:05 必須 announce 教練

## 🩺 軍師 Hook 自檢 2026-07-26 07:40（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 64b61285-7bd1-4265-a6fa-f6993c82b955

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-26 07:40
- ✅ 同步成功
- HANDOFF mtime: 1785022805
- 雲端同步：✅ 已推上雲端（commit fffa13972）
